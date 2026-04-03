# AGENTS.md

Guidelines for AI agents working in this repository.

## Repository Overview

This repository contains **Agent Skills** for AI agents following the [Agent Skills specification](https://agentskills.io/specification.md). Skills install to `.agents/skills/` (the cross-agent standard). This repo also serves as a **Claude Code plugin marketplace** via `.claude-plugin/marketplace.json`.

- **Name**: Clinical Skills
- **GitHub**: [aizech/clinical-skills](https://github.com/aizech/clinical-skills)
- **Creator**: Corpus Analytica
- **Focus**: Radiological Analytics
- **License**: MIT

## Repository Structure

```
clinical-skills/
├── .claude-plugin/
│   └── marketplace.json   # Claude Code plugin marketplace manifest
├── skills/               # Agent Skills
│   ├── core/             # Foundational skills (always loaded)
│   ├── clinical-documentation/
│   ├── patient-communication/
│   ├── workflow-coordination/
│   ├── analytics-quality/
│   ├── research-evidence/
│   ├── platform-integration/
│   ├── ai-assistants/
│   └── dataset/
├── tools/
│   ├── connectors/       # MCP servers and API clients
│   ├── integrations/     # Platform integration docs
│   └── clis/            # Zero-dependency Node.js CLI tools
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Build / Lint / Test Commands

**Skills** are content-only (no build step). Verify manually:
- YAML frontmatter is valid
- `name` field matches directory name exactly
- `name` is 1-64 chars, lowercase alphanumeric and hyphens only
- `description` is 1-1024 characters

**CLI tools** (`tools/clis/*.js`) are zero-dependency Node.js scripts (Node 18+). Verify with:
```bash
node --check tools/clis/<name>.js   # Syntax check
node tools/clis/<name>.js           # Show usage (no args = help)
node tools/clis/<name>.js <cmd> --dry-run  # Preview request without sending
```

## Agent Skills Specification

Skills follow the [Agent Skills spec](https://agentskills.io/specification.md).

### Required Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

### Frontmatter Field Constraints

| Field         | Required | Constraints                                                      |
|---------------|----------|------------------------------------------------------------------|
| `name`        | Yes      | 1-64 chars, lowercase `a-z`, numbers, hyphens. Must match dir.   |
| `description` | Yes      | 1-1024 chars. Describe what it does and when to use it.          |
| `license`     | No       | License name (default: MIT)                                      |
| `metadata`    | No       | Key-value pairs (author, version, etc.)                          |

### Name Field Rules

- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match parent directory name exactly

**Valid**: `modality-detection`, `pacs-workflow`, `ai-detection-pipeline`
**Invalid**: `Modality-Detection`, `-modality`, `modality--detection`

### Optional Skill Directories

```
skills/skill-name/
├── SKILL.md        # Required - main instructions (<500 lines)
├── references/     # Optional - detailed docs loaded on demand
├── scripts/        # Optional - executable code
├── evals/          # Optional - test cases for TDD
└── assets/         # Optional - templates, data files
```

## Writing Style Guidelines

### Structure

- Keep `SKILL.md` under 500 lines (move details to `references/`)
- Use H2 (`##`) for main sections, H3 (`###`) for subsections
- Use bullet points and numbered lists liberally
- Short paragraphs (2-4 sentences max)

### Tone

- Direct and instructional
- Second person ("You are a radiology workflow expert")
- Professional but approachable

### Formatting

- Bold (`**text**`) for key terms
- Code blocks for examples and templates
- Tables for reference data
- No excessive emojis

### Clarity Principles

- Clarity over cleverness
- Specific over vague
- Active voice over passive
- One idea per section

### Description Field Best Practices

The `description` is critical for skill discovery. Include:
1. What the skill does
2. When to use it (trigger phrases)
3. Related skills for scope boundaries

```yaml
description: Auto-detect imaging modality (CT, MRI, X-ray, US, etc.) from user input or DICOM file analysis. Also use when the user mentions "what modality", "detect from file", or needs to identify imaging type. For PACS integration, see pacs-workflow.
```

## Claude Code Plugin

This repo also serves as a plugin marketplace. The manifest at `.claude-plugin/marketplace.json` lists all skills for installation via:

```bash
/plugin marketplace add aizech/clinical-skills
/plugin install clinical-skills
```

See [Claude Code plugins documentation](https://code.claude.com/docs/en/plugins.md) for details.

## Git Workflow

### Branch Naming

- New skills: `feature/skill-name`
- Improvements: `fix/skill-name-description`
- Documentation: `docs/description`

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat: add modality-detection skill`
- `fix: improve clarity in pacs-workflow`
- `docs: update README`

### Pull Request Checklist

- [ ] `name` matches directory name
- [ ] `name` follows naming rules (lowercase, hyphens, no `--`)
- [ ] `description` is 1-1024 chars with trigger phrases
- [ ] `SKILL.md` is under 500 lines
- [ ] Evals defined in `evals/evals.json` (TDD approach)
- [ ] No sensitive data or credentials

## Tool Integrations

This repository includes a tools registry for radiology and healthcare integrations.

- **Tool discovery**: Read `tools/REGISTRY.md` to see available tools and their capabilities
- **Integration details**: See `tools/integrations/{tool}.md` for API endpoints, auth, and common operations
- **MCP connectors**: pacs-mcp, dicomweb-client, hl7-fhir-r4, llm-client
- **AI Platforms**: RadAI, Aidoc, Nvidia Clara, Zebra Medical, MaxQ AI, Qure AI, MedPaLM, etc.

### Registry Structure

```
tools/
├── REGISTRY.md              # Index of all tools with capabilities
├── connectors/              # MCP servers and API clients
│   ├── pacs-mcp/
│   ├── dicomweb-client/
│   ├── hl7-fhir-r4/
│   └── llm-client/
└── integrations/            # Detailed integration guides
    ├── pacs/
    ├── ehr/
    ├── ai-platforms/
    ├── datasets/
    └── reference/
```

### When to Use Tools

Skills reference relevant tools for implementation. For example:
- `pacs-workflow` skill → orthanc, ohif, dcm4chee guides
- `ai-detection-pipeline` skill → aidoc, nvidia-clara, zebra-medical guides
- `pubmed-search` skill → pubmed, radiopaedia guides
- `radiology-metrics` skill → metrics extraction CLIs

## TDD Workflow

Each skill follows Test-Driven Development:

1. **Define evals first**: Write `evals/evals.json` with test cases
2. **Write skill**: Implement to pass the evals
3. **Test & iterate**: Run evals, fix failures
4. **Document**: Add integration docs if needed

```bash
# Run evals for a skill
scripts/validate-skills.sh skills/skill-name
```

## Checking for Updates

When using any skill from this Repository:

1. **Once per session**, on first skill use, check for updates:
   - Fetch `VERSIONS.md` from GitHub: https://raw.githubusercontent.com/aizech/clinical-skills/main/VERSIONS.md
   - Compare versions against local skill files

2. **Only prompt if meaningful**:
   - 2 or more skills have updates, OR
   - Any skill has a major version bump (e.g., 1.x to 2.x)

3. **Non-blocking notification** at end of response:
   ```
   ---
   Skills update available: X clinical skills have updates.
   Say "update skills" to update automatically, or run `git pull` in your clinical-skills folder.
   ```

4. **If user says "update skills"**:
   - Run `git pull` in the clinical-skills directory
   - Confirm what was updated

## Skill Categories

See `README.md` for the current list of skills organized by category. When adding new skills, follow the naming patterns of existing skills in that category.

## Claude Code-Specific Enhancements

These patterns are **Claude Code only** and must not be added to `SKILL.md` files directly, as skills are designed to be cross-agent compatible (Codex, Cursor, Windsurf, etc.). Apply them locally in your own project's `.claude/skills/` overrides instead.

### Dynamic content injection with `!`command``

Claude Code supports embedding shell commands in SKILL.md using `` !`command` `` syntax. When the skill is invoked, Claude Code runs the command and injects the output inline — the model sees the result, not the instruction.

**Most useful application: auto-inject the radiology context file**

Instead of every skill telling the agent "go check if `.agents/radiology-context.md` exists and read it," you can inject it automatically:

```markdown
Radiology context: !`cat .agents/radiology-context.md 2>/dev/null || echo "No radiology context found — ask the user about their PACS, EHR, and workflow setup before proceeding."`
```

Place this at the top of a skill's body (after frontmatter) to make context available immediately without any file-reading step.

**Other useful injections:**

```markdown
# Inject today's date for recency-sensitive tasks
Today's date: !`date +%Y-%m-%d`

# Inject current git branch (useful for workflow skills)
Current branch: !`git branch --show-current 2>/dev/null`

# Inject recent commits for context
Recent commits: !`git log --oneline -5 2>/dev/null`
```

**Why this is Claude Code-only**: Other agents that load skills will see the literal `` !`command` `` string rather than executing it, which would appear as garbled instructions. Keep cross-agent skill files free of this syntax.
