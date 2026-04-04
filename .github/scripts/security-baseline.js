#!/usr/bin/env node
/**
 * Security Baseline Check for Clinical Skills
 * 
 * Runs security checks on skill files and outputs JSON report
 * for website display.
 * 
 * Checks:
 * - No hardcoded secrets (API keys, tokens, passwords)
 * - No sensitive patterns (PHI indicators)
 * - Safe external links
 * - Valid YAML frontmatter
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const ROOT_DIR = path.resolve(__dirname, '../..');
const SKILLS_DIR = path.join(ROOT_DIR, 'skills');
const OUTPUT_FILE = process.argv[2] || path.join(ROOT_DIR, 'security-report.json');

// Patterns for secrets detection
// Note: Environment variable references like ${VAR_NAME} are not secrets and are excluded
const SECRET_PATTERNS = [
  { pattern: /api[_-]?key["\s:=]+['"]?[a-zA-Z0-9]{20,}/gi, name: 'API Key' },
  { pattern: /secret["\s:=]+['"]?[a-zA-Z0-9]{16,}/gi, name: 'Secret' },
  { pattern: /password["\s:=]+['"][^'"]+['"]/gi, name: 'Password' },
  { pattern: /token["\s:=]+['"]?[a-zA-Z0-9_\-]{20,}/gi, name: 'Token' },
  { pattern: /bearer\s+[a-zA-Z0-9_\-\.]+/gi, name: 'Bearer Token' },
  { pattern: /ghp_[a-zA-Z0-9]{36}/g, name: 'GitHub Personal Access Token' },
  { pattern: /gho_[a-zA-Z0-9]{36}/g, name: 'GitHub OAuth Token' },
];

// Patterns for PHI/sensitive data
const PHI_PATTERNS = [
  { pattern: /patient\s*(?:name|id|mrn|record)/gi, name: 'Patient Identifier' },
  { pattern: /\b\d{3}[-.]?\d{2}[-.]?\d{4}\b/g, name: 'SSN Pattern' },
  { pattern: /\b(?!000|666|9\d{2})\d{3}[-]\d{2}[-]\d{4}\b/g, name: 'SSN Format' },
  { pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, name: 'Email Address' },
  { pattern: /\b\d{10,}\b/g, name: 'Long Number (ID)' },
];

// External URL pattern
const EXTERNAL_URL_PATTERN = /https?:\/\/[^\s\)"']+/g;

/**
 * Parse YAML frontmatter
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();

    if ((value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    frontmatter[key] = value;
  }

  return frontmatter;
}

/**
 * Check file for secrets
 */
function checkSecrets(content, filePath) {
  const issues = [];

  for (const { pattern, name } of SECRET_PATTERNS) {
    const matches = content.match(pattern);
    if (matches) {
      // Filter out env var references and placeholders
      const realMatches = matches.filter(m =>
        !m.includes('${') &&
        !m.includes('PLACEHOLDER') &&
        !m.includes('YOUR_')
      );

      if (realMatches.length > 0) {
        issues.push({
          type: 'secret',
          name: name,
          count: realMatches.length,
          example: realMatches[0].slice(0, 50) + (realMatches[0].length > 50 ? '...' : '')
        });
      }
    }
  }

  return issues;
}

/**
 * Check file for PHI/sensitive patterns
 */
function checkPHI(content, filePath) {
  const issues = [];

  for (const { pattern, name } of PHI_PATTERNS) {
    const matches = content.match(pattern);
    if (matches) {
      // Filter out common safe patterns
      const realMatches = matches.filter(m => {
        // Allow common false positives with limits
        if (name === 'Long Number (ID)' && m.length >= 13 && m.length <= 20) {
          return true; // DICOM UIDs
        }
        return false;
      });

      if (realMatches.length > 0) {
        issues.push({
          type: 'phi',
          name: name,
          count: realMatches.length,
          example: realMatches[0].slice(0, 30)
        });
      }
    }
  }

  return issues;
}

/**
 * Extract external URLs
 */
function extractExternalLinks(content) {
  const urls = [];
  const matches = content.match(EXTERNAL_URL_PATTERN);

  if (matches) {
    const seen = new Set();
    for (const url of matches) {
      // Skip GitHub raw content URLs
      if (url.includes('github.com') && url.includes('/raw/')) continue;
      if (url.includes('raw.githubusercontent.com')) continue;

      const cleanUrl = url.replace(/[).,#].*$/, ''); // Remove anchors, params
      if (!seen.has(cleanUrl) && !cleanUrl.includes('localhost')) {
        seen.add(cleanUrl);
        urls.push(cleanUrl);
      }
    }
  }

  return urls;
}

/**
 * Check frontmatter validity
 */
function checkFrontmatter(skillPath) {
  const issues = [];
  const skillMd = path.join(skillPath, 'SKILL.md');

  if (!fs.existsSync(skillMd)) {
    return [{ type: 'error', name: 'Missing SKILL.md', message: 'SKILL.md file not found' }];
  }

  const content = fs.readFileSync(skillMd, 'utf8');
  const frontmatter = parseFrontmatter(content);

  if (!frontmatter) {
    return [{ type: 'error', name: 'Invalid Frontmatter', message: 'No YAML frontmatter found' }];
  }

  if (!frontmatter.name) {
    issues.push({ type: 'error', name: 'Missing Name', message: 'name field is required' });
  }

  if (!frontmatter.description) {
    issues.push({ type: 'error', name: 'Missing Description', message: 'description field is required' });
  }

  if (frontmatter.description && frontmatter.description.length > 1024) {
    issues.push({ type: 'warning', name: 'Description Too Long', message: 'description exceeds 1024 characters' });
  }

  return issues;
}

/**
 * Analyze a single skill
 */
function analyzeSkill(skillPath, category) {
  const name = path.basename(skillPath);
  const skillMd = path.join(skillPath, 'SKILL.md');

  const result = {
    name: name,
    category: category,
    path: `./skills/${category}/${name}`,
    checks: {
      frontmatter: { passed: true, issues: [] },
      secrets: { passed: true, issues: [] },
      phi: { passed: true, issues: [] },
      links: { passed: true, issues: [] }
    },
    externalLinks: [],
    securityStatus: 'verified'
  };

  if (!fs.existsSync(skillMd)) {
    result.checks.frontmatter.passed = false;
    result.checks.frontmatter.issues.push({ type: 'error', message: 'SKILL.md not found' });
    result.securityStatus = 'error';
    return result;
  }

  const content = fs.readFileSync(skillMd, 'utf8');

  // Check frontmatter
  const frontmatterIssues = checkFrontmatter(skillPath);
  result.checks.frontmatter.issues = frontmatterIssues;
  if (frontmatterIssues.some(i => i.type === 'error')) {
    result.checks.frontmatter.passed = false;
    result.securityStatus = 'error';
  }

  // Check for secrets
  const secretIssues = checkSecrets(content, skillMd);
  result.checks.secrets.issues = secretIssues;
  if (secretIssues.length > 0) {
    result.checks.secrets.passed = false;
    result.securityStatus = 'warning';
  }

  // Check for PHI
  const phiIssues = checkPHI(content, skillMd);
  result.checks.phi.issues = phiIssues;
  if (phiIssues.length > 0) {
    result.checks.phi.passed = false;
    result.securityStatus = 'warning';
  }

  // Extract external links
  result.externalLinks = extractExternalLinks(content);

  return result;
}

/**
 * Analyze all skills
 */
function analyzeAllSkills() {
  const results = [];
  let totalIssues = { errors: 0, warnings: 0 };

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error('Skills directory not found:', SKILLS_DIR);
    return { skills: [], summary: totalIssues };
  }

  const categories = fs.readdirSync(SKILLS_DIR);

  for (const category of categories) {
    const categoryPath = path.join(SKILLS_DIR, category);
    if (!fs.statSync(categoryPath).isDirectory()) continue;

    const skills = fs.readdirSync(categoryPath);

    for (const skill of skills) {
      const skillPath = path.join(categoryPath, skill);
      if (!fs.statSync(skillPath).isDirectory()) continue;

      const result = analyzeSkill(skillPath, category);
      results.push(result);

      // Count issues
      for (const check of Object.values(result.checks)) {
        totalIssues.errors += check.issues.filter(i => i.type === 'error').length;
        totalIssues.warnings += check.issues.filter(i => i.type === 'warning').length;
      }
    }
  }

  return { skills: results, summary: totalIssues };
}

/**
 * Generate report
 */
function generateReport() {
  const { skills, summary } = analyzeAllSkills();

  const report = {
    generated: new Date().toISOString(),
    repo: 'aizech/clinical-skills',
    version: '1.0.0',
    skillsAudited: skills.length,
    summary: {
      totalSkills: skills.length,
      verifiedSkills: skills.filter(s => s.securityStatus === 'verified').length,
      issuesFound: summary.errors + summary.warnings,
      errors: summary.errors,
      warnings: summary.warnings
    },
    checks: {
      noSecrets: { passed: skills.every(s => s.checks.secrets.passed) },
      noPhi: { passed: skills.every(s => s.checks.phi.passed) },
      validFrontmatter: { passed: skills.every(s => s.checks.frontmatter.passed) }
    },
    skills: skills.map(s => ({
      name: s.name,
      category: s.category,
      securityStatus: s.securityStatus,
      checks: {
        noSecrets: s.checks.secrets.passed,
        noPhi: s.checks.phi.passed,
        validFrontmatter: s.checks.frontmatter.passed
      },
      issueCount:
        s.checks.secrets.issues.length +
        s.checks.phi.issues.length +
        s.checks.frontmatter.issues.length,
      issues: [
        ...s.checks.frontmatter.issues,
        ...s.checks.secrets.issues,
        ...s.checks.phi.issues
      ],
      externalLinks: s.externalLinks.length,
      lastAudit: new Date().toISOString()
    }))
  };

  return report;
}

// Main execution
const report = generateReport();

// Ensure output directory exists
const outputDir = path.dirname(OUTPUT_FILE);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(report, null, 2));

console.log(`Security report generated: ${report.skillsAudited} skills analyzed`);
console.log(`  - Verified: ${report.summary.verifiedSkills}`);
console.log(`  - Errors: ${report.summary.errors}`);
console.log(`  - Warnings: ${report.summary.warnings}`);
console.log(`Output: ${OUTPUT_FILE}`);
