# Clinical Skills - Contributing Guide

## Welcome to Clinical Skills

Thank you for contributing to Clinical Skills for Radiology! This repository provides AI agent skills for radiological analytics, developed by [Corpus Analytica](https://github.com/aizech).

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
- [ ] **Test locally** - Run `./scripts/validate-skills.sh` before submitting
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

### CLI Tools

1. **Document purpose** - Clear description of what it does
2. **Include examples** - Show common usage patterns
3. **Handle errors** - Meaningful error messages

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
# Validate all skills
./scripts/validate-skills.sh

# Validate specific skill
./scripts/validate-skills.sh skills/my-new-skill

# Check YAML syntax
find skills -name "*.md" -exec head -10 {} \; | grep -q "^---" || echo "Frontmatter error"
```

### Required Checks

Before submitting, verify:

- [ ] SKILL.md has valid frontmatter (`name`, `description`)
- [ ] `name` field matches directory name
- [ ] `description` is 1-1024 characters
- [ ] evals.json exists with test cases
- [ ] No hardcoded secrets or credentials
- [ ] No patient health information (PHI)
- [ ] External links are valid and safe

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

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve Clinical Skills for Radiology!**
