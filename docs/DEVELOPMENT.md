# Development Guide

This guide covers setting up a development environment, running validation, testing skills, and contributing to clinical-skills.

## Prerequisites

- **Node.js** v22+ (for security baseline scripts)
- **Python** 3.8+ (for CLI tools)
- **Git** (for version control)
- **Bash** (for validation scripts on Unix/Linux/macOS) or WSL on Windows

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aizech/clinical-skills.git
cd clinical-skills
```

### 2. Install Dependencies

**Python (for CLI tools):**
```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # If requirements.txt exists
# Or install CLI tool dependencies manually
pip install requests
```

**Node.js (for security scripts):**
```bash
# No npm dependencies currently required
# Security scripts use only built-in Node.js modules
```

### 3. Verify Installation

```bash
# Test CLI tools
python tools/clis/dicom_qido.py --help
python tools/clis/pubmed_search.py --help

# Test security script
node .github/scripts/security-baseline.js security-report.json
```

## Running Validation

### Validate All Skills

```bash
./scripts/validate-skills.sh
```

This checks:
- YAML frontmatter validity
- Name/description constraints
- SKILL.md line count (<500)
- Directory structure compliance

### Validate Specific Skill

```bash
./scripts/validate-skills.sh skills/core/radiology-context
```

### Run Security Baseline Check

```bash
node .github/scripts/security-baseline.js security-report.json
cat security-report.json | jq '.summary'
```

This checks for:
- Hardcoded secrets (API keys, tokens, passwords)
- PHI/sensitive data patterns
- Valid YAML frontmatter
- External links

## Creating a New Skill

### 1. Create Directory Structure

```bash
mkdir -p skills/{category}/{skill-name}
cd skills/{category}/{skill-name}
```

### 2. Create SKILL.md

```bash
touch SKILL.md
```

Add frontmatter:
```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

### 3. Add Content

Keep SKILL.md under 500 lines. Move detailed documentation to `references/` if needed.

### 4. Create Evals

```bash
mkdir -p evals
touch evals/evals.json
```

Add test cases:
```json
{
  "tests": [
    {
      "id": "test-id",
      "input": "User input",
      "expected_action": "expected_result"
    }
  ]
}
```

### 5. Validate

```bash
./scripts/validate-skills.sh skills/{category}/{skill-name}
```

## Testing CLI Tools

### Manual Testing

```bash
# Test DICOM QIDO
python tools/clis/dicom_qido.py https://pacs.example.com/dicomweb --modality CT

# Test PubMed search
python tools/clis/pubmed_search.py "lung nodule AI detection" --max 5
```

### Unit Tests (Coming Soon)

Unit tests are planned for CLI tools. See Phase 3 of the improvement plan.

## Debugging Validation Issues

### Frontmatter Errors

**Error:** `Missing YAML frontmatter`
**Solution:** Ensure SKILL.md starts with `---` on line 1

**Error:** `Name mismatch: directory='x' but frontmatter='y'`
**Solution:** Ensure `name` field matches directory name exactly

**Error:** `Description length invalid`
**Solution:** Keep description between 1-1024 characters

### Security Check Warnings

**Warning:** `Password` or `Bearer Token` detected
**Solution:** Use environment variable references: `password: "env:VAR_NAME"`

**Warning:** `External link` detected
**Solution:** Links are OK, but ensure they're safe and not pointing to internal resources

## Running GitHub Actions Locally

### Using act (GitHub Actions Runner)

```bash
# Install act
brew install act  # macOS
# or: https://github.com/nektos/act

# Run specific workflow
act -W .github/workflows/validate-skill.yml
```

### Manual Workflow Simulation

```bash
# Simulate validate-skill workflow
./scripts/validate-skills.sh

# Simulate security-baseline workflow
node .github/scripts/security-baseline.js security-report.json
```

## Common Development Tasks

### Update Integration Doc

1. Edit file in `tools/integrations/`
2. Validate markdown: `find tools/integrations -name "*.md" -exec echo {} \;`
3. Test examples if applicable
4. Commit with message: `docs: update {platform} integration doc`

### Add New CLI Tool

1. Create file in `tools/clis/`
2. Add shebang: `#!/usr/bin/env python3`
3. Use argparse for CLI arguments
4. Add error handling with try/except
5. Add `--help` documentation
6. Make executable: `chmod +x tools/clis/{tool}.py`
7. Update `tools/REGISTRY.md`

### Update Validation Script

1. Edit `scripts/validate-skills.sh`
2. Test on all skills: `./scripts/validate-skills.sh`
3. Test on specific skill: `./scripts/validate-skills.sh skills/{path}`
4. Commit with message: `chore: update validation script`

## Code Style

### Python (CLI Tools)

- Use `black` for formatting: `black tools/clis/`
- Use `ruff` for linting: `ruff check tools/clis/`
- Use type hints on function signatures
- Follow PEP 8 guidelines

### JavaScript (Security Scripts)

- Use 2-space indentation
- Use const/let instead of var
- Add JSDoc comments for functions
- Follow existing patterns in `security-baseline.js`

### Markdown (Skills & Docs)

- Use consistent heading levels
- Use code blocks with language specification
- Keep lines under 100 characters
- Use bullet lists for items
- Number lists only for sequential steps

## Pre-commit Hooks (Recommended)

Install pre-commit hooks to automatically validate changes:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

See `.pre-commit-config.yaml` for hook configuration.

## Troubleshooting

### Validation Script Fails on Windows

**Issue:** Bash script doesn't run on Windows
**Solution:** Use WSL or Git Bash, or run validation manually

### Security Script Permission Denied

**Issue:** `node .github/scripts/security-baseline.js` fails
**Solution:** `chmod +x .github/scripts/security-baseline.js`

### CLI Tool Import Errors

**Issue:** `ModuleNotFoundError: No module named 'requests'`
**Solution:** Install dependencies: `pip install requests`

### Skill Not Detected by Agent

**Issue:** Agent doesn't recognize skill
**Solution:**
1. Check frontmatter is valid
2. Check name matches directory
3. Check description includes trigger phrases
4. Run validation script

## Resources

- [Agent Skills Specification](https://agentskills.io/specification.md)
- [CLAUDE.md](../CLAUDE.md) - Contribution guide
- [AGENTS.md](../AGENTS.md) - Agent guidelines
- [README.md](../README.md) - User guide
