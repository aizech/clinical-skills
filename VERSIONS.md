# Clinical Skills Versions

Current versions of all skills. Agents can compare against local versions to check for updates.

| Skill | Version | Last Updated |
|-------|---------|--------------|
| modality-detection | 1.0.0 | 2026-04-04 |
| radiology-context | 1.0.0 | 2026-04-04 |
| radiology-report-analysis | 1.0.0 | 2026-04-04 |
| structured-reporting | 1.0.0 | 2026-04-04 |
| imaging-study-review | 1.0.0 | 2026-04-04 |
| patient-results-letter | 1.0.0 | 2026-04-04 |
| patient-education-material | 1.0.0 | 2026-04-04 |
| imaging-referral | 1.0.0 | 2026-04-04 |
| followup-tracking | 1.0.0 | 2026-04-04 |
| care-gap-closure | 1.0.0 | 2026-04-04 |
| pacs-workflow | 1.0.0 | 2026-04-04 |
| dicom-web-query | 1.0.0 | 2026-04-04 |
| pubmed-search | 1.0.0 | 2026-04-04 |
| ai-report-assist | 1.0.0 | 2026-04-04 |
| ai-detection-pipeline | 1.0.0 | 2026-04-04 |
| llm-radiology-use | 1.0.0 | 2026-04-04 |
| ai-quality-review | 1.0.0 | 2026-04-04 |
| radiology-research | 1.0.0 | 2026-04-04 |
| guideline-integration | 1.0.0 | 2026-04-04 |
| cross-reference-linking | 1.0.0 | 2026-04-04 |
| radiology-metrics | 1.0.0 | 2026-04-04 |
| image-quality-audit | 1.0.0 | 2026-04-04 |
| report-quality-review | 1.0.0 | 2026-04-04 |
| radiology-dataset-guide | 1.0.0 | 2026-04-04 |
| dataset-preprocessing | 1.0.0 | 2026-04-04 |
| model-validation | 1.0.0 | 2026-04-04 |

## Recent Changes

### 2026-04-04
- Version 1.0.1 release - Comprehensive improvements
- Added 6 documentation files (DEVELOPMENT.md, TROUBLESHOOTING.md, WORKFLOW_EXAMPLES.md, CLI_API.md, DOCKER.md, INTEGRATION_TEMPLATE.md)
- Added comprehensive test suite (85 tests: 78 unit + 7 integration) with 59% CLI coverage
- Added shared CLI utilities module (base_cli, api_client, json_formatter)
- Added Docker support (Dockerfile, docker-compose.yml, .dockerignore)
- Added development tooling (pytest.ini, requirements.txt, pre-commit hooks, yamllint)
- Added GitHub Actions workflow for CLI tests
- Refactored CLI tools to use shared utilities
- Fixed workflow issues (npm cache, security-baseline auto-commit, branch references)
- Updated REGISTRY.md with new documentation and development tools

### 2026-04-03
- Initial release of Clinical Skills for Radiology
- Created 26 skills across 9 categories
- Focus: Radiological analytics
- Built by Corpus Analytica
- TDD workflow with evals for all skills
