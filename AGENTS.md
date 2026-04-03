# AGENTS.md

Guidelines for AI agents working in this repository. For contributing guidelines, see [CLAUDE.md](CLAUDE.md).

## Repository Overview

- **Name**: Clinical Skills
- **GitHub**: [aizech/clinical-skills](https://github.com/aizech/clinical-skills)
- **Creator**: Corpus Analytica
- **Focus**: Radiological Analytics
- **License**: MIT

## Repository Structure

```
clinical-skills/
├── .claude-plugin/
│   └── marketplace.json   # Plugin marketplace manifest
├── skills/               # Agent Skills (26 skills)
│   ├── core/             # Foundational skills
│   ├── clinical-documentation/
│   ├── patient-communication/
│   ├── workflow-coordination/
│   ├── analytics-quality/
│   ├── research-evidence/
│   ├── platform-integration/
│   ├── ai-assistants/
│   └── dataset/
├── tools/
│   ├── integrations/     # 30+ platform integration docs
│   └── clis/            # 12 Python CLI tools
├── scripts/              # Validation scripts
└── .github/             # GitHub config
```

## Skill Categories

| Category | Skills |
|----------|--------|
| **Core** | modality-detection, radiology-context |
| **Clinical Documentation** | radiology-report-analysis, structured-reporting, imaging-study-review |
| **Patient Communication** | patient-results-letter, patient-education-material |
| **Workflow Coordination** | imaging-referral, followup-tracking, care-gap-closure |
| **Platform Integration** | pacs-workflow, pubmed-search, dicom-web-query |
| **AI Assistants** | ai-report-assist, ai-detection-pipeline, llm-radiology-use, ai-quality-review |
| **Analytics Quality** | radiology-metrics, image-quality-audit, report-quality-review |
| **Research Evidence** | guideline-integration, cross-reference-linking, radiology-research |
| **Dataset** | radiology-dataset-guide, dataset-preprocessing, model-validation |

## Skill Specification

Skills follow the [Agent Skills spec](https://agentskills.io/specification.md).

### Required Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

### Field Constraints

| Field | Constraints |
|-------|-------------|
| `name` | 1-64 chars, lowercase a-z, numbers, hyphens. Must match directory. |
| `description` | 1-1024 characters with trigger phrases. |

### Valid Directory Structure

```
skills/{category}/{skill-name}/
├── SKILL.md           # Required (<500 lines)
├── evals/
│   └── evals.json     # Test cases (TDD)
└── references/        # Optional detailed docs
```

## TDD Workflow

1. **Define evals first** - Write `evals/evals.json` with test cases
2. **Write skill** - Implement to pass evals
3. **Test & iterate** - Run validation, fix failures
4. **Document** - Add integration docs if needed

```bash
# Validate all skills
./scripts/validate-skills.sh

# Validate specific skill
./scripts/validate-skills.sh skills/{category}/{skill-name}
```

## Tool Registry

See `tools/REGISTRY.md` for all available tools.

| Category | Tools |
|----------|-------|
| **PACS** | orthanc, dcm4chee, ohif-viewer |
| **AI Detection** | aidoc, nvidia-clara, zebra-medical, maxq-ai, qure-ai |
| **AI Reporting** | radai |
| **LLM Platforms** | medpalm-api, google-health, amazon-healthlake |
| **EHR** | epic-radiant, cerner-powerchart |
| **Datasets** | rsna-data, nih-chestxray14, physionet-mimic, chexpert, luna16, brats, etc. |
| **Reference** | pubmed-ncbi, radiopaedia, fhir-r4, hl7-v2 |

## Validation Commands

### Skills
```bash
./scripts/validate-skills.sh                    # All skills
./scripts/validate-skills.sh skills/{path}     # Specific skill
```

### CLI Tools
```bash
python tools/clis/dicom_qido.py --help         # DICOM query
python tools/clis/pubmed_search.py --help      # Literature search
```

## Git Workflow

### Branch Naming
- `feature/skill-name` - New skills
- `fix/skill-description` - Improvements
- `docs/description` - Documentation

### Commit Messages
```
feat: add pacs-workflow skill
fix: improve modality-detection accuracy
docs: update orthanc integration doc
```

## Checking for Updates

1. **Once per session** - Check VERSIONS.md for updates:
   ```
   https://raw.githubusercontent.com/aizech/clinical-skills/main/VERSIONS.md
   ```

2. **Notify if meaningful**:
   - 2+ skills updated, OR
   - Major version bump (1.x → 2.x)

3. **Update command**:
   ```
   git pull in clinical-skills directory
   ```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
