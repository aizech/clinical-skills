# Contributing to Clinical Skills

Thanks for your interest in contributing to Clinical Skills! This guide will help you add new skills or improve existing ones.

## Requesting a Skill

You can suggest new skills by [opening a skill request](https://github.com/aizech/clinical-skills/issues/new?template=skill-request.yml).

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir -p skills/category/your-skill-name
mkdir -p skills/category/your-skill-name/evals
mkdir -p skills/category/your-skill-name/references
```

### 2. Create the SKILL.md file

Every skill needs a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: When to use this skill. Include trigger phrases and keywords that help agents identify relevant tasks.
---

# Your Skill Name

Instructions for the agent go here...
```

Optional frontmatter fields: `license` (default: MIT), `metadata` (author, version, etc.)

### 3. Follow the naming conventions

- **Directory name**: lowercase, hyphens only (e.g., `ai-detection-pipeline`)
- **Name field**: must match directory name exactly
- **Description**: 1-1024 characters, include trigger phrases

### 4. Structure your skill (TDD approach)

```
skills/category/your-skill-name/
├── SKILL.md           # Required - main instructions
├── evals/             # Required for TDD - test cases
│   └── evals.json
├── references/        # Optional - additional documentation
│   └── guide.md
├── scripts/           # Optional - executable code
│   └── helper.js
└── assets/           # Optional - templates, images, data
    └── template.json
```

### 5. Write effective instructions

- Keep `SKILL.md` under 500 lines
- Move detailed reference material to `references/`
- Include step-by-step instructions
- Add examples of inputs and outputs
- Cover common edge cases

### 6. Write evals (TDD approach)

Create `evals/evals.json` with test cases:

```json
{
  "tests": [
    {
      "id": "test-1",
      "input": "Example input that triggers this skill",
      "expected": "Expected behavior or output"
    }
  ]
}
```

## Improving Existing Skills

1. Read the existing skill thoroughly
2. Review the evals to understand expected behavior
3. Test your changes locally
4. Keep changes focused and minimal
5. Update the version in metadata if making significant changes

## Submitting Your Contribution

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-skill-name`)
3. Make your changes
4. Test locally with an AI agent
5. Submit a pull request using the appropriate template:
   - [New Skill](?template=new-skill.md)
   - [Skill Update](?template=skill-update.md)
   - [Documentation](?template=documentation.md)

## Skill Quality Checklist

- [ ] `name` matches directory name
- [ ] `description` clearly explains when to use the skill
- [ ] Instructions are clear and actionable
- [ ] Evals defined in `evals/evals.json`
- [ ] No sensitive data or credentials
- [ ] Follows existing skill patterns in the repo

## Questions?

Open an issue if you have questions or need help with your contribution.
