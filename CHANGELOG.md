# Changelog

All notable changes to clinical-skills are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Fixed

### Security

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
