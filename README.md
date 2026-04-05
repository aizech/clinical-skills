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
│  Imaging │ │Clinical  │ │Patient   │ │  Platform  │ │   AI     │ │ Research &  │ │Analytics  │
│Analysis  │ │Document  │ │Communicat│ │Integration │ │Assistants│ │  Evidence   │ │ Quality   │
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
| [modality-detection](skills/core/modality-detection/) | Auto-detect imaging modality (CT, MRI, X-ray, US, etc.) from user input or DICOM file analysis. Also use when the user mentions "what modality", "detect from file", or needs to identify imaging type. |
| [radiology-context](skills/core/radiology-context/) | Establish and manage user's clinical environment configuration - PACS, EHR, modality types, and workflow settings. Also use when setting up or updating radiology workflow context. |
| [radiology-report-analysis](skills/clinical-documentation/radiology-report-analysis/) | Analyze structured/free-text radiology reports, extract key findings, measurements, and impressions. Also use when the user provides a report for review, summary, or data extraction. |
| [structured-reporting](skills/clinical-documentation/structured-reporting/) | Create and optimize structured radiology reports using standardized templates (RadElement, IHE, BI-RADS, LI-RADS, PI-RADS). Also use when converting free-text to structured format. |
| [impression-generation](skills/clinical-documentation/impression-generation/) | Generate clinical impressions from radiology findings following best practices. Also use when the user wants AI-assisted impression writing or report finalization. |
| [findings-extraction](skills/clinical-documentation/findings-extraction/) | Extract structured data from radiology reports - measurements, measurements, anatomy, pathology codes. Also use for data mining, research, or report analysis. |
| [imaging-study-review](skills/clinical-documentation/imaging-study-review/) | Systematic review of imaging studies with structured reporting format. Also use for QA reviews, tumor boards, or comprehensive case analysis. |
| [patient-results-letter](skills/patient-communication/patient-results-letter/) | Generate patient-friendly radiology result communications in plain language. Also use when the user needs to explain findings to patients without medical jargon. |
| [patient-education-material](skills/patient-communication/patient-education-material/) | Create patient education materials for specific imaging procedures and findings. Also use when developing handouts, FAQs, or educational content about radiology. |
| [imaging-referral](skills/workflow-coordination/imaging-referral/) | Create, optimize, and manage imaging referrals between providers. Also use when the user needs to improve referral quality, add relevant clinical info, or track referral status. |
| [followup-tracking](skills/workflow-coordination/followup-tracking/) | Track incidental findings, schedule follow-up imaging, and manage reminder workflows. Also use when the user mentions "follow-up", "incidental finding", or "reminder". |
| [care-gap-closure](skills/workflow-coordination/care-gap-closure/) | Ensure recommended imaging is completed and close care gaps in radiology. Also use when optimizing imaging completion rates or tracking screening compliance. |
| [protocol-optimization](skills/workflow-coordination/protocol-optimization/) | Optimize imaging protocols for clinical indications. Also use when the user needs protocol selection guidance or protocol customization recommendations. |
| [pacs-workflow](skills/platform-integration/pacs-workflow/) | Query PACS, retrieve studies, manage worklists, and integrate with PACS workflows. Also use when the user needs to interact with picture archiving systems. |
| [dicom-web-query](skills/platform-integration/dicom-web-query/) | Query and retrieve DICOM objects via DICOMweb REST API. Also use when the user needs to work with DICOMweb servers or web-based imaging access. |
| [hl7-fhir-radiology](skills/platform-integration/hl7-fhir-radiology/) | Work with HL7 messages and FHIR resources for radiology workflows. Also use for EHR integration, order/result exchange, or imaging-related FHIR operations. |
| [filesystem-imaging](skills/platform-integration/filesystem-imaging/) | Handle local DICOM files and imaging folders. Also use when the user provides file paths, needs to scan directories, or work with local imaging data. |
| [ai-report-assist](skills/ai-assistants/ai-report-assist/) | Guidance for AI-assisted structured reporting tools (RadAI, Abba, DeepRad). Also use when the user mentions AI reporting, automated templating, or speech-to-report systems. |
| [ai-detection-pipeline](skills/ai-assistants/ai-detection-pipeline/) | Integrate AI detection into PACS workflow (Aidoc, Nvidia Clara, Zebra Medical, MaxQ AI, Qure AI). Also use when the user needs to set up, configure, or optimize AI detection systems. |
| [llm-radiology-use](skills/ai-assistants/llm-radiology-use/) | Use LLM APIs for radiology tasks (MedPaLM, MedLM, Google Health, Amazon HealthLake). Also use when the user wants to integrate or optimize LLM-based radiology workflows. |
| [ai-quality-review](skills/ai-assistants/ai-quality-review/) | QA AI outputs, detect false positives/negatives, and validate AI results. Also use when evaluating AI system performance or reviewing AI-assisted findings. |
| [pubmed-search](skills/research-evidence/pubmed-search/) | Evidence-based literature search for radiology. Also use when the user needs to find relevant studies, guidelines, or clinical evidence for imaging findings. |
| [radiology-research](skills/research-evidence/radiology-research/) | Design and conduct radiology research studies. Also use when the user wants to plan a study, extract data, or analyze imaging research. |
| [guideline-integration](skills/research-evidence/guideline-integration/) | Apply ACR, ESR, and specialty imaging guidelines and appropriateness criteria. Also use when the user needs to verify compliance or select appropriate imaging. |
| [cross-reference-linking](skills/research-evidence/cross-reference-linking/) | Link findings to related cases, literature, and reference materials. Also use when cross-referencing imaging with research or case databases. |
| [radiology-metrics](skills/analytics-quality/radiology-metrics/) | Dashboard metrics for imaging - volume, turnaround times, accuracy, quality. Also use when the user needs to track, analyze, or report radiology KPIs. |
| [image-quality-audit](skills/analytics-quality/image-quality-audit/) | QC/QA review of imaging protocols and image quality. Also use for quality assurance programs, accreditation prep, or protocol optimization. |
| [report-quality-review](skills/analytics-quality/report-quality-review/) | Review and improve radiology reporting accuracy and consistency. Also use for QA programs, peer review, or reporting optimization. |
| [radiology-dataset-guide](skills/dataset/radiology-dataset-guide/) | Guide to accessing public radiology datasets (RSNA, NIH, MIMIC, CheXpert, LUNA16, BraTS, etc.). Also use when the user needs to find or access imaging datasets. |
| [dataset-preprocessing](skills/dataset/dataset-preprocessing/) | Prepare DICOM/images for AI training and analysis. Also use when the user needs to preprocess imaging data, convert formats, or prepare datasets. |
| [model-validation](skills/dataset/model-validation/) | Validate AI model performance on local data. Also use for model testing, benchmark comparison, or clinical validation studies. |
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

### Windsurf

Windsurf (Cascade) automatically discovers skills from `.agents/skills/`, so if you've already installed clinical-skills via npx skills, they're already available in Windsurf.

#### Option 1: Workspace Installation (Recommended for projects)

Clone skills to your project's `.windsurf/skills/` directory:

```bash
git clone https://github.com/aizech/clinical-skills.git ~/.clinical-skills-temp
cp -r ~/.clinical-skills-temp/skills .windsurf/
rm -rf ~/.clinical-skills-temp
```

Skills are now available in this workspace and committed with your repo.

#### Option 2: Global Installation

Install globally for all workspaces:

```bash
git clone https://github.com/aizech/clinical-skills.git ~/.codeium/windsurf/clinical-skills
ln -s ~/.codeium/windsurf/clinical-skills/skills ~/.codeium/windsurf/skills/clinical-skills
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/aizech/clinical-skills.git $env:USERPROFILE\.codeium\windsurf\clinical-skills
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.codeium\windsurf\skills\clinical-skills" -Target "$env:USERPROFILE\.codeium\windsurf\clinical-skills\skills"
```

#### Option 3: Use npx skills (Cross-platform)

The npx skills method installs to `.agents/skills/`, which Windsurf also discovers:

```bash
npx skills add aizech/clinical-skills
```

This works across Windsurf, Claude Code, Cursor, and other agents.

#### Usage

Once installed, use skills in Windsurf Cascade:

```
@radiology-context
```

Then use any clinical skill:

```
Analyze this CT report for pulmonary nodules
```

Cascade will automatically invoke the relevant skill based on your request.

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
