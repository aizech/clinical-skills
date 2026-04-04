#!/usr/bin/env node
/**
 * Generate llms.txt for AI agent discovery
 * 
 * Outputs a markdown file that helps AI agents discover and understand
 * the clinical-skills repository.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '../..');
const SKILLS_DIR = path.join(ROOT_DIR, 'skills');
const TOOLS_DIR = path.join(ROOT_DIR, 'tools');
const OUTPUT_FILE = process.argv[2] || path.join(ROOT_DIR, 'public/llms.txt');

// Category display names
const CATEGORY_NAMES = {
  'core': 'Core Skills',
  'clinical-documentation': 'Clinical Documentation',
  'patient-communication': 'Patient Communication',
  'workflow-coordination': 'Workflow Coordination',
  'platform-integration': 'Platform Integration',
  'ai-assistants': 'AI Assistants',
  'analytics-quality': 'Analytics & Quality',
  'research-evidence': 'Research & Evidence',
  'dataset': 'Dataset Management'
};

/**
 * Parse YAML frontmatter from a markdown file
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();

    // Remove quotes if present
    if ((value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    frontmatter[key] = value;
  }

  return frontmatter;
}

/**
 * Get all skills with their metadata
 */
function getSkills() {
  const skills = [];

  if (!fs.existsSync(SKILLS_DIR)) {
    return skills;
  }

  const categories = fs.readdirSync(SKILLS_DIR);

  for (const category of categories) {
    const categoryPath = path.join(SKILLS_DIR, category);
    if (!fs.statSync(categoryPath).isDirectory()) continue;

    const categorySkills = fs.readdirSync(categoryPath);

    for (const skill of categorySkills) {
      const skillPath = path.join(categoryPath, skill);
      if (!fs.statSync(skillPath).isDirectory()) continue;

      const skillMd = path.join(skillPath, 'SKILL.md');
      if (!fs.existsSync(skillMd)) continue;

      const content = fs.readFileSync(skillMd, 'utf8');
      const frontmatter = parseFrontmatter(content);

      skills.push({
        name: frontmatter.name || skill,
        description: frontmatter.description || '',
        category: category,
        path: `./skills/${category}/${skill}`
      });
    }
  }

  return skills;
}

/**
 * Get integration docs
 */
function getIntegrations() {
  const integrationsDir = path.join(TOOLS_DIR, 'integrations');
  const integrations = [];

  if (!fs.existsSync(integrationsDir)) {
    return integrations;
  }

  const files = fs.readdirSync(integrationsDir);

  for (const file of files) {
    if (!file.endsWith('.md')) continue;

    const filePath = path.join(integrationsDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const frontmatter = parseFrontmatter(content);

    // Extract first paragraph as description
    const bodyMatch = content.match(/^---\n[\s\S]*?\n---\n\n([\s\S]*)/);
    const body = bodyMatch ? bodyMatch[1].split('\n\n')[0].trim() : '';

    integrations.push({
      name: file.replace('.md', ''),
      description: body.slice(0, 200) + (body.length > 200 ? '...' : ''),
      path: `./tools/integrations/${file}`
    });
  }

  return integrations;
}

/**
 * Get CLI tools
 */
function getCLITools() {
  const clisDir = path.join(TOOLS_DIR, 'clis');
  const tools = [];

  if (!fs.existsSync(clisDir)) {
    return tools;
  }

  const files = fs.readdirSync(clisDir);

  for (const file of files) {
    if (!file.endsWith('.py')) continue;

    const filePath = path.join(clisDir, file);
    const content = fs.readFileSync(filePath, 'utf8');

    // Extract description from docstring or first comment
    const descMatch = content.match(/#\s*(.+)/);
    const description = descMatch ? descMatch[1].trim() : file.replace('.py', '');

    tools.push({
      name: file.replace('.py', ''),
      description: description,
      path: `./tools/clis/${file}`
    });
  }

  return tools;
}

/**
 * Format category name for display
 */
function formatCategory(category) {
  return CATEGORY_NAMES[category] || category.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Generate llms.txt content
 */
function generateLlms() {
  const skills = getSkills();
  const integrations = getIntegrations();
  const cliTools = getCLITools();

  let content = `# Clinical Skills for Radiology

AI agent skills for radiological analytics by Corpus Analytica.

## About

Clinical Skills provides specialized knowledge for AI agents working in healthcare and radiology contexts:
- Radiology workflow automation (PACS queries, report analysis)
- Clinical documentation (structured reporting, patient communication)
- AI integration (detection pipelines, LLM assistance)
- Quality assurance (metrics, audits, compliance)
- Research support (literature search, dataset management)

**Repository:** https://github.com/aizech/clinical-skills
**License:** MIT

## Skills

`;

  // Group skills by category
  const skillsByCategory = {};
  for (const skill of skills) {
    if (!skillsByCategory[skill.category]) {
      skillsByCategory[skill.category] = [];
    }
    skillsByCategory[skill.category].push(skill);
  }

  // Output skills by category
  const categoryOrder = Object.keys(CATEGORY_NAMES);
  for (const category of categoryOrder) {
    if (!skillsByCategory[category]) continue;

    content += `### ${CATEGORY_NAMES[category]}\n\n`;

    for (const skill of skillsByCategory[category]) {
      // Truncate description if too long
      let desc = skill.description;
      if (desc.length > 200) {
        desc = desc.slice(0, 200).trim() + '...';
      }
      content += `- **${skill.name}**: ${desc}\n`;
    }

    content += '\n';
  }

  content += `## Integration Tools

Clinical Skills supports integration with various radiology platforms and tools.

| Tool | Description |
|------|-------------|
`;

  for (const int of integrations) {
    content += `| ${int.name} | ${int.description} |\n`;
  }

  content += `

## CLI Tools

Command-line tools for clinical imaging operations.

| Tool | Description |
|------|-------------|
`;

  for (const tool of cliTools) {
    content += `| ${tool.name} | ${tool.description} |\n`;
  }

  content += `

## Contributing

See [CLAUDE.md](CLAUDE.md) for contribution guidelines.
See [CHANGELOG.md](CHANGELOG.md) for version history.

## Quick Reference

### TDD Workflow
1. Write evals in evals/evals.json first
2. Implement skill to pass evals
3. Run ./scripts/validate-skills.sh
4. Submit PR with test results

### Skill Naming
- Lowercase with hyphens: \`modality-detection\`
- name field must match directory name
- description: 1-1024 chars with trigger phrases

---

Generated: ${new Date().toISOString()}
`;

  return { content, skills };
}

// Main execution
const { content, skills } = generateLlms();

// Ensure output directory exists
const outputDir = path.dirname(OUTPUT_FILE);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(OUTPUT_FILE, content);

console.log(`Generated llms.txt: ${skills.length} skills, ${OUTPUT_FILE}`);
