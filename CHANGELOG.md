# Changelog

All notable changes to clinical-skills are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]

### Added

#### Documentation
- `docs/DEVELOPMENT.md` - Comprehensive development setup guide with local dev environment, validation, and testing instructions
- `docs/TROUBLESHOOTING.md` - Common issues and solutions for validation failures, CLI errors, and installation problems
- `docs/WORKFLOW_EXAMPLES.md` - End-to-end workflow examples covering PACS query, literature search, quality metrics, dataset analysis, AI integration, documentation automation, security auditing, and skill development
- `docs/CLI_API.md` - API reference documentation for all CLI tools including shared utilities
- `docs/DOCKER.md` - Docker support and usage guide
- `tools/integrations/INTEGRATION_TEMPLATE.md` - Standardized template for integration documentation

#### Testing & Quality
- `tools/clis/tests/` directory with comprehensive test suite:
  - `test_radiology_metrics.py` (16 tests)
  - `test_dicom_info.py` (15 tests)
  - `test_image_qc.py` (23 tests)
  - `test_dicom_qido.py` (10 tests, updated for refactored code)
  - `test_pubmed_search.py` (14 tests, updated for refactored code)
  - `test_cli_integration.py` (7 integration tests)
- Total: 85 passing tests (78 unit + 7 integration) with 59% CLI coverage
- `pytest.ini` - Test configuration with coverage settings
- `.pre-commit-config.yaml` - Pre-commit hooks for validation, linting, and formatting
- `.yamllint.yml` - YAML linting configuration
- `requirements.txt` - Python dependencies for CLI tools and testing

#### Infrastructure & Tooling
- `tools/clis/shared/` module with common utilities:
  - `base_cli.py` - Common argparse setup, logging, error handling
  - `api_client.py` - HTTP client with retry logic, rate limiting, timeout handling
  - `json_formatter.py` - JSON output formatting utilities
- `Dockerfile` - Python 3.13 base image for consistent environment
- `docker-compose.yml` - CLI tools and test services
- `.dockerignore` - Docker build exclusions
- `.github/workflows/cli-tests.yml` - CI workflow for running CLI tests with pip caching
- `.github/branch-ruleset.json` - Branch protection rules

#### Generated Assets
- `public/llms.txt` - Generated llms.txt for AI agent discovery
- `security-report.json` - Security baseline audit report (committed for CI)

### Changed

#### Code Refactoring
- Refactored `dicom_qido.py` to use shared utilities (APIClient, create_base_parser, setup_logging, handle_error, print_json)
- Refactored `pubmed_search.py` to use shared utilities (APIClient, create_base_parser, setup_logging, handle_error, print_json)
- Updated `scripts/validate-skills.sh` with additional validation checks:
  - evals.json existence check (TDD requirement)
  - evals.json JSON validation
  - code block language specification check
  - basic internal link validation

#### Documentation Updates
- Standardized integration docs with new template structure:
  - Updated `orthanc.md` to follow INTEGRATION_TEMPLATE.md
  - Updated `dicomweb-standard.md` to follow INTEGRATION_TEMPLATE.md
- Updated `README.md` Resources section to reference new documentation files

#### Workflow Updates
- Updated all GitHub Actions workflows to use `main` branch instead of `master`
- Updated `.github/workflows/security-baseline.yml` to commit `security-report.json` reliably via `stefanzweifel/git-auto-commit-action` using `file_pattern`
- Added Node.js setup to `.github/workflows/sync-skills.yml`

### Deprecated

### Fixed

#### Workflow Fixes
- Fixed `generate-llms`/Node workflow failures caused by `actions/setup-node` npm cache usage without a lockfile by removing `cache: 'npm'` from Node-only workflows (generate-llms.yml, security-baseline.yml, sync-skills.yml)
- Fixed security report auto-commit failures caused by ignored `security-report.json` in `.gitignore`
- Fixed `security-baseline.yml` workflow by adding missing checkout step
- Fixed unsupported `overwrite` parameter from artifact upload actions
- Fixed ReferenceError in `generate-llms.js` - skills variable not in scope
- Fixed branch name references from `master` to `main` across workflows

#### Code Fixes
- Fixed unpacking of tags in `dicom_info.py` to handle 3-element tuples (tag, keyword, description)
- Fixed path insertion logic in CLI test files to use `Path(__file__).parent.parent` for proper module import
- Fixed `test_main_search_tag` in `test_dicom_info.py` to assert against lowercased output
- Fixed `test_main_file_not_found` in `test_dicom_info.py` to check for error message instead of SystemExit

#### Security Fixes
- Fixed false positives in security-baseline.js by removing env var pattern from secrets detection

### Security

- Security baseline workflow now consistently publishes and commits `security-report.json` for auditable CI reporting
- Removed `security-report.json` from `.gitignore` to enable CI commits

## [1.0.0] - 2026-04-03

### Added

- **26 Agent Skills** across 9 categories
- **34 Integration Docs** covering PACS, EHR, AI platforms, datasets, and interoperability
- **12 CLI Tools** for DICOM operations, literature search, metrics, and QC
- **Validation Scripts** for skill testing

### Skills

#### Core
- `modality-detection` - Auto-detect imaging modality
- `radiology-context` - Configure clinical environment

#### Clinical Documentation
- `radiology-report-analysis` - Analyze reports
- `structured-reporting` - BI-RADS, LI-RADS, PI-RADS templates
- `imaging-study-review` - Systematic review

#### Patient Communication
- `patient-results-letter` - Patient-friendly communications
- `patient-education-material` - Procedure/condition education

#### Workflow Coordination
- `imaging-referral` - Create/improve referrals
- `followup-tracking` - Track incidental findings
- `care-gap-closure` - Ensure recommended imaging completed

#### Platform Integration
- `pacs-workflow` - Query PACS, retrieve studies
- `pubmed-search` - Literature search
- `dicom-web-query` - DICOMweb REST operations

#### AI Assistants
- `ai-report-assist` - AI reporting tools (RadAI, Abba, DeepRad)
- `ai-detection-pipeline` - AI detection (Aidoc, Clara, Zebra, MaxQ, Qure)
- `llm-radiology-use` - LLM API integration (MedPaLM, HealthLake, Google Health)
- `ai-quality-review` - AI output QA

#### Analytics Quality
- `radiology-metrics` - Dashboard metrics
- `image-quality-audit` - QC review
- `report-quality-review` - Reporting accuracy

#### Research Evidence
- `guideline-integration` - ACR/ESR criteria
- `cross-reference-linking` - Link to literature/cases
- `radiology-research` - Medical imaging literature

#### Dataset
- `radiology-dataset-guide` - Public dataset guide
- `dataset-preprocessing` - Prepare data for AI training
- `model-validation` - Validate AI model performance

### Integration Docs

#### PACS
- orthanc, dcm4chee, ohif-viewer

#### EHR
- epic-radiant, cerner-powerchart

#### AI Platforms
- aidoc, nvidia-clara, zebra-medical, maxq-ai, qure-ai, radai, medpalm-api, google-health, amazon-healthlake

#### Datasets
- rsna-data, nih-chestxray14, physionet-mimic, chexpert, chexphoto, luna16, kits, brats, panda, objcxr

#### Reference
- pubmed-ncbi, radiopaedia, fhir-r4, hl7-v2, dicomweb-standard, dicom-conformance

#### Frameworks
- monai, itksnap

### CLI Tools
- DICOM: dicom_qido.py, dicom_wado.py, fetch_study.py, dicom_anonymizer.py, dicom_info.py
- Metrics: tat_analyzer.py, radiology_metrics.py, image_qc.py
- Research: pubmed_search.py, trial_matcher.py
- Documentation: structured_report.py, dataset_downloader.py

### Infrastructure
- GitHub Actions: validate-skill.yml, sync-skills.yml
- Claude Code plugin marketplace
- Comprehensive documentation (CLAUDE.md, AGENTS.md, README.md, CONTRIBUTING.md)
