# Clinical Skills - Contributing Guide

## Welcome to Clinical Skills

Thank you for contributing to Clinical Skills! This repository provides AI agent skills for medical imaging and healthcare workflows, developed by [Corpus Analytica](https://github.com/aizech).

## Purpose

Clinical Skills provides specialized knowledge for AI agents working in healthcare and radiology contexts:
- **Radiology workflow automation** - PACS queries, report analysis
- **Clinical documentation** - Structured reporting, patient communication
- **AI integration** - Detection pipelines, LLM assistance
- **Quality assurance** - Metrics, audits, compliance
- **Research support** - Literature search, dataset management

## Contribution Philosophy

We welcome contributions that:
- Follow Test-Driven Development (TDD) principles
- Include evals.json for skill validation
- Benefit radiology AI broadly
- Maintain high quality standards

## Before Opening a PR

Please complete these steps before submitting:

- [ ] **Search first** - Check existing issues and PRs (open and closed)
- [ ] **One change per PR** - Each PR should address one skill or improvement
- [ ] **Test locally** - Run validation scripts before submitting
  - Skills: `./scripts/validate-skills.sh`
  - CLI tools: `pytest tools/clis/tests/ -v`
- [ ] **Human review** - Ensure a human has reviewed your changes
- [ ] **Clear description** - Explain what problem this solves

## What Makes a Great Contribution

### Skill Changes

1. **Start with evals** - Write test cases in `evals/evals.json` first
2. **Keep SKILL.md under 500 lines** - Move details to references/
3. **Use clear naming** - Lowercase with hyphens (e.g., `ct-brain-analysis`)
4. **Include triggers** - Add phrases that should activate the skill
5. **No secrets** - Never commit API keys, credentials, or PHI

### Integration Docs

1. **Complete coverage** - Include auth, endpoints, examples
2. **Verify accuracy** - Test endpoints work as documented
3. **Use standard formats** - Follow existing integration doc patterns
4. **Use the template** - Start from `tools/integrations/INTEGRATION_TEMPLATE.md`

### CLI Tools

1. **Document purpose** - Clear description of what it does
2. **Include examples** - Show common usage patterns
3. **Handle errors** - Meaningful error messages
4. **Write tests** - Add unit tests in `tools/clis/tests/`
5. **Use shared utilities** - Leverage `tools/clis/shared/` when possible

### Documentation

1. **Follow existing patterns** - Match style and format of existing docs
2. **Include examples** - Provide clear, runnable examples
3. **Keep it current** - Update docs when code changes
4. **Use the template** - For integration docs, use INTEGRATION_TEMPLATE.md

## What Doesn't Fit in Core

These contributions may be better as separate plugins:

- **Very specialized clinical workflows** - For specific institutions only
- **Platform-specific integrations** - Target specific vendors uniquely
- **Third-party promotions** - Commercial services should have separate repos
- **Highly experimental features** - Consider marking as alpha

**Not sure?** Open an issue first to discuss!

## Skill Changes Require Evaluation

Skills shape AI agent behavior. Changes should be tested:

1. Write evals in `evals/evals.json`
2. Run `./scripts/validate-skills.sh`
3. Test on multiple scenarios (happy path + edge cases)
4. Document test results in your PR

## Testing Your Changes

### Local Validation

```bash
# Validate skills
./scripts/validate-skills.sh                    # All skills
./scripts/validate-skills.sh skills/my-new-skill # Specific skill

# Test CLI tools
pytest tools/clis/tests/ -v                    # All CLI tests
pytest tools/clis/tests/test_dicom_qido.py     # Specific test

# Check YAML syntax
find skills -name "*.md" -exec head -10 {} \; | grep -q "^---" || echo "Frontmatter error"

# Run with Docker
docker-compose run cli-tools pytest tools/clis/tests/ -v
```

### Development Setup

Before testing, set up your development environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run pre-commit hooks
pre-commit run --all-files

# See docs/DEVELOPMENT.md for complete setup guide
```

### Required Checks

Before submitting, verify:

#### For Skill Changes
- [ ] SKILL.md has valid frontmatter (`name`, `description`)
- [ ] `name` field matches directory name
- [ ] `description` is 1-1024 characters
- [ ] evals.json exists with test cases
- [ ] No hardcoded secrets or credentials
- [ ] No patient health information (PHI)
- [ ] External links are valid and safe

#### For CLI Tool Changes
- [ ] Unit tests added in `tools/clis/tests/`
- [ ] Tests pass with pytest
- [ ] Uses shared utilities from `tools/clis/shared/` when applicable
- [ ] Error handling is robust
- [ ] Documentation updated in docs/CLI_API.md

#### For Documentation Changes
- [ ] Follows existing style and format
- [ ] Examples are tested and accurate
- [ ] Links are valid
- [ ] Markdown renders correctly

## Human Review Requirements

All contributions require human review:

1. Show the complete diff to your human collaborator
2. Explain the purpose and testing performed
3. Get explicit approval before submitting
4. Include a note that human reviewed the changes

## Code Style

### YAML Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Skill directories | lowercase with hyphens | `ct-brain-analysis` |
| evals files | `evals/evals.json` | |
| CLI tools | `snake_case.py` | `dicom_qido.py` |
| Integration docs | `kebab-case.md` | `epic-radiant.md` |

## File Locations

```
clinical-skills/
├── skills/                    # Agent skills
│   └── {category}/
│       └── {skill-name}/
│           ├── SKILL.md       # Main skill file
│           ├── evals/
│           │   └── evals.json # Test cases
│           └── references/    # Additional docs
├── tools/
│   ├── integrations/          # Platform integration docs
│   └── clis/                # CLI tools
│       ├── shared/          # Shared utilities
│       └── tests/           # CLI tool tests
├── docs/                      # Development documentation
│   ├── DEVELOPMENT.md
│   ├── TROUBLESHOOTING.md
│   ├── WORKFLOW_EXAMPLES.md
│   ├── CLI_API.md
│   └── DOCKER.md
├── scripts/                  # Validation scripts
└── .github/                 # GitHub config
```

## Reporting Issues

Before reporting:
1. Search existing issues
2. Check if it's a platform issue vs clinical-skills issue
3. Include environment details (harness, version, OS)

## Questions?

- Open an issue for bugs or feature requests
- Check existing discussions
- Reference CLAUDE.md for contributing guidelines
- See docs/DEVELOPMENT.md for development setup
- See docs/TROUBLESHOOTING.md for common issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve Clinical Skills!**
