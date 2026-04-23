# Clinical Skills for AI Agents

A collection of AI agent skills focused on medical imaging and healthcare workflows. Built for radiologists, healthcare IT professionals, and researchers who want AI coding agents to help with imaging workflows, clinical documentation, AI integration, and radiology research. Works with Claude Code, OpenAI Codex, Cursor, Windsurf, and any agent that supports the [Agent Skills spec](https://agentskills.io).

![Version](https://img.shields.io/badge/version-1.0.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Skills](https://img.shields.io/badge/skills-26-orange)
![Integrations](https://img.shields.io/badge/integrations-34-purple)
![Tests](https://img.shields.io/badge/tests-85-brightgreen)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/aizech/clinical-skills)

> ⚠️ **Security Notice**: These skills work with healthcare concepts. Never input patient-identifiable information (PHI). Use de-identified or synthetic data only.

Built by [Corpus Analytica](https://corpusanalytica.com). Special skills created and verified by Corpus Analytica for healthcare and medical AI applications.

**Contributions welcome!** Found a way to improve a skill or have a new one to add? [Open a PR](CONTRIBUTING.md).

Run into a problem or have a question? [Open an issue](https://github.com/aizech/clinical-skills/issues) — we're happy to help.

## What are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you add these to your project, your agent can recognize when you're working on a radiology task and apply the right frameworks and best practices.

## How Skills Work Together

Skills reference each other and build on shared context. The `radiology-context` skill is the foundation — every other skill checks it first to understand your imaging environment, PACS setup, and clinical workflow before doing anything.

```
                            ┌──────────────────────────────────────┐
                            │       radiology-context              │
                            │   (read by all other skills first)   │
                            └──────────────────┬───────────────────┘
                                               │
    ┌──────────────┬─────────────┬─────────────┼─────────────┬──────────────┬──────────────┐
    ▼              ▼             ▼             ▼             ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌─────────────┐ ┌───────────┐
│ Imaging  │ │ Clinical │ │ Patient  │ │  Platform  │ │   AI     │ │ Research &  │ │ Analytics │
│ Analysis │ │ Document │ │  Comm    │ │Integration │ │Assistants│ │  Evidence   │ │  Quality  │
├──────────┤ ├──────────┤ ├──────────┤ ├────────────┤ ├──────────┤ ├─────────────┤ ├───────────┤
│modality  │ │report    │ │results   │ │pacs-work   │ │ai-report │ │pubmed-search│ │radiology  │
│detect    │ │analysis  │ │letter    │ │dicom-web   │ │assist    │ │guideline    │ │metrics    │
│imaging   │ │struct    │ │imaging   │ │hl7-fhir    │ │ai-detect │ │radiology    │ │image      │
│study     │ │report    │ │referral  │ │filesystem  │ │pipeline  │ │research     │ │quality    │
│review    │ │impression│ │followup  │ │            │ │llm-radiol│ │cross-ref    │ │audit      │
│          │ │findings  │ │care-gap  │ │            │ │use       │ │linking      │ │report     │
│          │ │extract   │ │closure   │ │            │ │ai-quality│ │             │ │quality    │
│          │ │          │ │          │ │            │ │review    │ │             │ │review     │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬──────┘ └────┬─────┘ └──────┬──────┘ └─────┬─────┘
     │            │            │             │             │              │              │
     └────────────┴─────┬──────┴─────────────┴─────────────┴──────────────┴──────────────┘
                        │
         Skills cross-reference each other:
           report-analysis ↔ structured-reporting ↔ findings-extraction
           pacs-workflow ↔ dicom-web-query ↔ filesystem-imaging
           ai-detection-pipeline ↔ ai-quality-review ↔ llm-radiology-use
           pubmed-search ↔ guideline-integration ↔ cross-reference-linking
           followup-tracking ↔ care-gap-closure ↔ patient-results-letter
```

See each skill's **Related Skills** section for the full dependency map.

## Available Skills

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [ai-detection-pipeline](skills/ai-detection-pipeline/) | Integrate AI detection into PACS workflow. Also use when setting up, configuring, or optimizing AI detection systems... |
| [ai-quality-review](skills/ai-quality-review/) | QA AI outputs, detect false positives/negatives, and validate AI results. Also use when evaluating AI system... |
| [ai-report-assist](skills/ai-report-assist/) | Guidance for AI-assisted structured reporting tools. Also use when the user mentions AI reporting, automated... |
| [care-gap-closure](skills/care-gap-closure/) | Ensure recommended imaging is completed and close care gaps in radiology. Also use when optimizing imaging completion... |
| [cross-reference-linking](skills/cross-reference-linking/) | Links current findings to priors, related literature, and correlated data. Use when user mentions "compare to priors",... |
| [dataset-preprocessing](skills/dataset-preprocessing/) | Provides preprocessing pipelines and techniques for radiology datasets used in AI development. Use when user mentions... |
| [dicom-web-query](skills/dicom-web-query/) | Query and retrieve DICOM objects via DICOMweb REST API. Also use when the user needs to work with DICOMweb servers,... |
| [followup-tracking](skills/followup-tracking/) | Track incidental findings, schedule follow-up imaging, and manage reminder workflows. Also use when the user mentions... |
| [guideline-integration](skills/guideline-integration/) | Access and apply professional radiology society guidelines. Use when user mentions "ACR criteria", "appropriateness... |
| [image-quality-audit](skills/image-quality-audit/) | Assesses medical image quality against clinical standards and identifies optimization opportunities. Use when user... |
| [imaging-referral](skills/imaging-referral/) | Create, optimize, and manage imaging referrals between providers. Also use when the user needs to improve referral... |
| [imaging-study-review](skills/imaging-study-review/) | Performs comprehensive review of imaging studies for clinical, QA, tumor board, or comparison purposes. Use when user... |
| [llm-radiology-use](skills/llm-radiology-use/) | Use LLM APIs for radiology tasks. Also use when integrating medical LLMs (MedPaLM, MedLM, Google Health, Amazon... |
| [modality-detection](skills/modality-detection/) | Auto-detect imaging modality (CT, MRI, X-ray, US, etc.) from user input, DICOM file headers, or file analysis. Also use... |
| [model-validation](skills/model-validation/) | Designs and executes validation studies for radiology AI models to ensure clinical reliability and regulatory... |
| [pacs-workflow](skills/pacs-workflow/) | Query PACS, retrieve studies, manage worklists, and integrate with PACS workflows. Also use when the user needs to... |
| [patient-education-material](skills/patient-education-material/) | Create patient education materials for imaging procedures and findings. Also use when developing handouts, FAQs, or... |
| [patient-results-letter](skills/patient-results-letter/) | Generate patient-friendly radiology result communications in plain language. Also use when the user needs to explain... |
| [radiology-context](skills/radiology-context/) | Establish and manage user's clinical radiology environment configuration - PACS, EHR, modality types, AI tools, and... |
| [radiology-dataset-guide](skills/radiology-dataset-guide/) | Guides researchers and developers through radiology dataset selection, access, and utilization for AI development. Use... |
| [radiology-metrics](skills/radiology-metrics/) | Retrieves and analyzes operational metrics from radiology information systems. Use when user mentions "radiology KPIs",... |
| [radiology-report-analysis](skills/radiology-report-analysis/) | Analyze structured/free-text radiology reports, extract key findings, measurements, and impressions. Also use when the... |
| [radiology-research](skills/radiology-research/) | Access and synthesize medical imaging research literature. Use when user mentions "recent research on", "literature... |
| [report-quality-review](skills/report-quality-review/) | Monitors and improves radiology report quality through systematic audit and feedback. Use when user mentions "report... |
| [structured-reporting](skills/structured-reporting/) | Create and optimize structured radiology reports using standardized templates. Also use when the user mentions BI-RADS,... |
<!-- SKILLS:END -->

## Quick Start

1. **Install skills**: `npx skills add aizech/clinical-skills`
2. **Load context first**: Ask your agent to "read radiology-context" (this sets up your clinical environment)
3. **Use a skill**: "Analyze this CT report for pulmonary nodules"

> **Tip**: Always load `radiology-context` before other skills. It configures your imaging environment and ensures other skills work correctly.

## Installation

### Claude Code (via Plugin Marketplace)

Install via Claude Code's built-in plugin system:

```bash
# Add the marketplace
/plugin marketplace add aizech/clinical-skills

# Install all clinical skills
/plugin install clinical-skills
```

### Cursor (via Plugin Marketplace)

In Cursor Agent chat, install from marketplace:

```text
/add-plugin clinical-skills
```

or search for "clinical-skills" in the plugin marketplace.

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/aizech/clinical-skills/refs/heads/main/.codex/INSTALL.md
```

**Detailed docs:** [.codex/INSTALL.md](.codex/INSTALL.md)

### OpenCode

Tell OpenCode:

```
Fetch and follow instructions from https://raw.githubusercontent.com/aizech/clinical-skills/refs/heads/main/.opencode/INSTALL.md
```

**Detailed docs:** [.opencode/INSTALL.md](.opencode/INSTALL.md)

### GitHub Copilot CLI

```bash
copilot plugin marketplace add aizech/clinical-skills-marketplace
copilot plugin install clinical-skills@clinical-skills-marketplace
```

### Gemini CLI

```bash
gemini extensions install https://github.com/aizech/clinical-skills
```

To update:

```bash
gemini extensions update clinical-skills
```

### Manual Installation Options

If the platform-specific methods above don't work for your setup, use these manual options:

#### CLI Install

Use [npx skills](https://github.com/vercel-labs/skills) to install skills directly:

```bash
# Install all skills
npx skills add aizech/clinical-skills

# Install specific skills
npx skills add aizech/clinical-skills --skill modality-detection radiology-report-analysis

# List available skills
npx skills add aizech/clinical-skills --list
```

This automatically installs to your `.agents/skills/` directory (and symlinks into `.claude/skills/` for Claude Code compatibility).

#### Clone and Copy

Clone the entire repo and copy the skills folder:

```bash
git clone https://github.com/aizech/clinical-skills.git
cp -r clinical-skills/skills/* .agents/skills/
```

#### Git Submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/aizech/clinical-skills.git .agents/clinical-skills
```

Then reference skills from `.agents/clinical-skills/skills/`.

#### Fork and Customize

1. Fork this repository
2. Customize skills for your specific needs
3. Clone your fork into your projects

### Verify Installation

Start a new session in your chosen platform and ask for something that should trigger a clinical skill:

```
Analyze this CT report for pulmonary nodules
```

or

```
Query my PACS for recent chest CTs
```

The agent should automatically invoke the relevant clinical skill. Always load `radiology-context` first — it configures your clinical environment and ensures other skills work correctly.

## Usage

Once installed, just ask your agent to help with radiology tasks:

```
"Analyze this CT report for key findings"
→ Uses radiology-report-analysis skill

"Query my PACS for recent chest CTs"
→ Uses pacs-workflow skill

"Find recent literature on lung nodule AI detection"
→ Uses pubmed-search skill

"Set up AI detection pipeline for my PACS"
→ Uses ai-detection-pipeline skill
```

You can also invoke skills directly:

```
/modality-detection
/radiology-report-analysis
/pubmed-search
/pacs-workflow
```

## Development

For development setup, testing, and Docker usage:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tools/clis/tests/ -v

# Run with Docker
docker-compose run cli-tools python tools/clis/dicom_qido.py --help

# Validate skills
./scripts/validate-skills.sh
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for complete development guide.

## CLI Tools

The repository includes **12 command-line tools** for DICOM operations, metrics, and research:

| Tool | Purpose |
|------|---------|
| `dicom_qido.py` | Query DICOM objects via QIDO-RS |
| `dicom_wado.py` | Retrieve DICOM via WADO-RS |
| `fetch_study.py` | Download complete imaging studies |
| `pubmed_search.py` | Search medical literature |
| `tat_analyzer.py` | Turnaround time metrics |
| `radiology_metrics.py` | Dashboard KPI generation |

**Features:**

- Comprehensive test suite (85 tests: 78 unit + 7 integration)
- Shared utilities module for common functionality
- Docker support for consistent environments
- See `docs/CLI_API.md` for complete API documentation
- See `tools/clis/` for all available tools and tests

## Integration Registry

Browse **30+ integration docs** covering PACS, EHR, AI platforms, datasets, and standards:

| Category | Integrations |
|----------|--------------|
| **PACS** | Orthanc, dcm4chee, OHIF Viewer |
| **EHR** | Epic Radiant, Cerner PowerChart |
| **AI Platforms** | Aidoc, Nvidia Clara, Zebra Medical, RadAI |
| **Datasets** | RSNA, NIH ChestX-ray14, MIMIC, CheXpert |

See [tools/REGISTRY.md](tools/REGISTRY.md) for the complete catalog and integration template.

## Skill Categories

### Core (Always-Load)

- `modality-detection` - Auto-detect imaging modality
- `radiology-context` - User environment configuration
- `product-context` - Clinical context management

### Clinical Documentation

- `radiology-report-analysis` - Report analysis and review
- `structured-reporting` - Standardized report templates
- `impression-generation` - AI-assisted impression writing
- `findings-extraction` - Structured data extraction
- `imaging-study-review` - Systematic study review

### Patient Communication

- `patient-results-letter` - Patient-friendly result letters
- `patient-education-material` - Patient education content
- `referral-response` - Referral response communications

### Workflow Coordination

- `imaging-referral` - Imaging referral management
- `followup-tracking` - Follow-up and reminder workflows
- `care-gap-closure` - Care gap optimization
- `protocol-optimization` - Protocol selection guidance

### Platform Integration

- `pacs-workflow` - PACS interaction and worklists
- `dicom-web-query` - DICOMweb REST operations
- `hl7-fhir-radiology` - HL7/FHIR integration
- `filesystem-imaging` - Local file handling

### AI Assistants

- `ai-report-assist` - AI reporting tools guidance
- `ai-detection-pipeline` - AI detection integration
- `llm-radiology-use` - LLM API integration
- `ai-quality-review` - AI output QA

### Research & Evidence

- `pubmed-search` - Literature search
- `radiology-research` - Research study design
- `guideline-integration` - Guideline application
- `cross-reference-linking` - Case/literature linking

### Analytics & Quality

- `radiology-metrics` - KPI dashboards
- `image-quality-audit` - QC/QA protocols
- `report-quality-review` - Reporting accuracy

### Dataset

- `radiology-dataset-guide` - Public dataset access
- `dataset-preprocessing` - Data preparation
- `model-validation` - AI model testing
- `filesystem-imaging` - Local data handling

## Resources

| Document | Purpose |
|----------|---------|
| [VERSIONS.md](VERSIONS.md) | Current skill versions and update history |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Development setup, validation, testing guide |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [docs/WORKFLOW_EXAMPLES.md](docs/WORKFLOW_EXAMPLES.md) | End-to-end workflow examples |
| [docs/CLI_API.md](docs/CLI_API.md) | CLI tools API documentation |
| [docs/DOCKER.md](docs/DOCKER.md) | Docker support and usage guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or improve skills |
| [AGENTS.md](AGENTS.md) | Guidelines for AI agents working in this repo |
| [CLAUDE.md](CLAUDE.md) | Claude Code specific contribution guide |
| [CHANGELOG.md](CHANGELOG.md) | Version history and updates |
| [tools/REGISTRY.md](tools/REGISTRY.md) | Full integration catalog |
| [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/aizech/clinical-skills) | DeepWiki documentation |


## Contributing

Found a way to improve a skill? Have a new skill to suggest? PRs and issues welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding or improving skills.

## License

[MIT](LICENSE) - Use these however you want.
