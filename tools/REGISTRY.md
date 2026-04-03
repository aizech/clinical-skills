# Clinical Radiology Tools Registry

Quick reference for AI agents to discover clinical imaging tools, AI platforms, datasets, and integration methods.

## How to Use This Registry

1. **Find tools by category** - Browse sections below for tools in each domain
2. **Check integration methods** - See what APIs, CLIs, or SDKs are available
3. **Read integration guides** - Detailed setup and common operations in `integrations/`

---

## Tool Index

| Tool | Category | API | CLI | Guide |
|------|----------|:---:|:---:|:-----:|
| **PACS Systems** |||||
| orthanc | PACS | ✓ | - | [orthanc.md](integrations/orthanc.md) |
| dcm4chee | PACS | ✓ | - | [dcm4chee.md](integrations/dcm4chee.md) |
| **DICOMweb** |||||
| dicomweb | DICOM | ✓ | ✓ | [dicomweb-standard.md](integrations/dicomweb-standard.md) |
| ohif-viewer | DICOM | ✓ | - | [ohif-viewer.md](integrations/ohif-viewer.md) |
| dicom-conformance | DICOM | ✓ | - | [dicom-conformance.md](integrations/dicom-conformance.md) |
| **AI Detection Platforms** |||||
| aidoc | AI Detection | ✓ | - | [aidoc.md](integrations/aidoc.md) |
| nvidia-clara | AI Detection | ✓ | - | [nvidia-clara.md](integrations/nvidia-clara.md) |
| zebra-medical | AI Detection | ✓ | - | [zebra-medical.md](integrations/zebra-medical.md) |
| **AI Reporting** |||||
| radai | AI Reporting | ✓ | - | [radai.md](integrations/radai.md) |
| **LLM Platforms** |||||
| medpalm-api | LLM | ✓ | - | [medpalm-api.md](integrations/medpalm-api.md) |
| google-health | LLM | ✓ | - | [google-health.md](integrations/google-health.md) |
| amazon-healthlake | LLM | ✓ | - | [amazon-healthlake.md](integrations/amazon-healthlake.md) |
| **Datasets** |||||
| rsna-data | Dataset | ✓ | ✓ | [rsna-data.md](integrations/rsna-data.md) |
| nih-chestxray14 | Dataset | ✓ | ✓ | [nih-chestxray14.md](integrations/nih-chestxray14.md) |
| physionet-mimic | Dataset | ✓ | - | [physionet-mimic.md](integrations/physionet-mimic.md) |
| chexpert | Dataset | ✓ | - | [chexpert.md](integrations/chexpert.md) |
| luna16-dataset | Dataset | ✓ | - | [luna16-dataset.md](integrations/luna16-dataset.md) |
| brats-dataset | Dataset | ✓ | - | [brats-dataset.md](integrations/brats-dataset.md) |
| **Reference & Interop** |||||
| pubmed-ncbi | Literature | ✓ | ✓ | [pubmed-ncbi.md](integrations/pubmed-ncbi.md) |
| fhir-r4 | Interop | ✓ | - | [fhir-r4.md](integrations/fhir-r4.md) |
| hl7-v2 | Interop | ✓ | - | [hl7-v2.md](integrations/hl7-v2.md) |
| **Frameworks** |||||
| monai | ML Framework | - | - | [monai-framework.md](integrations/monai-framework.md) |
| itksnap | Segmentation | - | - | [itksnap.md](integrations/itksnap.md) |

---

## By Category

### PACS Systems

Picture Archiving and Communication Systems for managing imaging data.

| Tool | Best For | Open Source | API |
|------|----------|:-----------:|:---:|
| **Orthanc** | Research, small practices, learning | ✓ | REST |
| **DCM4CHEE** | Enterprise, HL7 integration | ✓ | REST + DICOM |

### DICOMweb Services

RESTful DICOM operations for query, retrieve, and storage.

| Tool | Best For | QIDO | WADO | STOW |
|------|----------|:----:|:----:|:----:|
| **DICOMweb Standard** | All DICOMweb operations | ✓ | ✓ | ✓ |
| **OHIF Viewer** | Zero-footprint viewing | ✓ | ✓ | - |

### AI Detection Platforms

AI-powered medical imaging detection for triage and diagnosis assistance.

| Platform | Focus Areas | Modality | FDA Cleared |
|----------|-------------|----------|:-----------:|
| **Aidoc** | Hemorrhage, PE, C-spine | CT | ✓ |
| **Nvidia Clara** | Multi-modal detection | CT, MRI, X-ray | ✓ |
| **Zebra Medical** | Multi-finding, chest | X-ray, CT | ✓ |

### AI Reporting Platforms

Structured reporting automation with AI assistance.

| Platform | Best For | Modality |
|----------|----------|----------|
| **RadAI** | CT structured reporting | CT, X-ray |

### LLM Platforms

Large language models for medical imaging reasoning and analysis.

| Platform | Best For | Capabilities |
|----------|----------|--------------|
| **MedPaLM** | Medical reasoning | Report analysis, QA |
| **Google Health** | Multi-modal reasoning | Imaging + EHR |
| **HealthLake** | FHIR data + ML | Imaging + clinical data |

### Public Datasets

Annotated medical imaging datasets for research and validation.

| Dataset | Modality | Size | Focus |
|---------|----------|------|-------|
| **RSNA** | X-ray, CT | Various | Multiple challenges |
| **NIH ChestX-ray14** | X-ray | ~112k | 14 chest pathologies |
| **MIMIC-CXR** | X-ray | ~377k | ICU chest imaging |
| **CheXpert** | X-ray | ~224k | Chest reporting |
| **LUNA16** | CT | ~888 scans | Lung nodule detection |
| **BraTS** | MRI | ~2k | Brain tumor segmentation |

### Reference & Interoperability

Literature search and healthcare data exchange standards.

| Tool | Purpose | Access |
|------|---------|--------|
| **PubMed/NCBI** | Medical literature | Free API |
| **HL7 FHIR R4** | Imaging data exchange | Standard |
| **HL7 v2** | Legacy messaging | EMR integration |

---

## CLI Tools

Python-based CLIs for clinical imaging operations.

| CLI | Purpose | Category |
|-----|---------|----------|
| [dicom_qido.py](clis/dicom_qido.py) | QIDO-RS search | DICOM |
| [dicom_wado.py](clis/dicom_wado.py) | WADO-RS retrieve | DICOM |
| [fetch_study.py](clis/fetch_study.py) | Full study download | PACS |
| [dicom_anonymizer.py](clis/dicom_anonymizer.py) | PHI removal | Compliance |
| [dicom_info.py](clis/dicom_info.py) | DICOM metadata viewer | Utilities |
| [image_qc.py](clis/image_qc.py) | Image quality metrics | QC |
| [tat_analyzer.py](clis/tat_analyzer.py) | Turnaround time analysis | Metrics |
| [radiology_metrics.py](clis/radiology_metrics.py) | Productivity metrics | Metrics |
| [pubmed_search.py](clis/pubmed_search.py) | Literature search | Research |
| [dataset_downloader.py](clis/dataset_downloader.py) | Dataset access guide | Dataset |
| [structured_report.py](clis/structured_report.py) | Report templating | Documentation |
| [trial_matcher.py](clis/trial_matcher.py) | Clinical trial matching | Research |

### CLI Installation

```bash
# Make executable
chmod +x tools/clis/*.py

# Run directly
python tools/clis/dicom_qido.py --help

# Or install globally
pip install -e tools/clis/
```

---

## Quick Start by Use Case

### Query PACS for Studies
1. Read [orthanc.md](integrations/orthanc.md) for PACS setup
2. Use `dicom_qido.py` CLI for queries

### Set Up AI Detection
1. Read [aidoc.md](integrations/aidoc.md) for CT triage
2. Configure PACS integration for automated processing

### Search Literature
1. Read [pubmed-ncbi.md](integrations/pubmed-ncbi.md) for API access
2. Use `pubmed_search.py` CLI for searches

### Analyze Report Quality
1. Use `radiology_metrics.py` for TAT analysis
2. Use `image_qc.py` for quality metrics

### Download Training Data
1. Read [rsna-data.md](integrations/rsna-data.md) for RSNA data
2. Use `dataset_downloader.py` for guidance

### Analyze Reports with LLM
1. Read [medpalm-api.md](integrations/medpalm-api.md) for setup
2. Use structured_report.py for templating

---

## Integration Connectors

### MCP Servers (Future)

| Connector | Purpose |
|-----------|---------|
| `pacs-mcp/` | MCP server for PACS interaction |
| `dicomweb-client/` | DICOMweb REST client |

### Integration Docs by Category

**PACS & DICOM:**
- orthanc.md, dcm4chee.md, ohif-viewer.md
- dicomweb-standard.md, dicom-conformance.md

**AI Platforms:**
- aidoc.md, nvidia-clara.md, zebra-medical.md, radai.md
- medpalm-api.md, google-health.md, amazon-healthlake.md

**Datasets:**
- rsna-data.md, nih-chestxray14.md, physionet-mimic.md
- chexpert.md, luna16-dataset.md, brats-dataset.md

**Reference & Interop:**
- pubmed-ncbi.md, fhir-r4.md, hl7-v2.md

**Frameworks:**
- monai-framework.md, itksnap.md

---

## Skills Reference

These tools are referenced by the agent skills:

| Skill | Tools Used |
|-------|------------|
| pacs-workflow | orthanc, dcm4chee, dicom_qido, fetch_study |
| dicom-web-query | dicomweb, ohif, dicom_qido, dicom_wado |
| ai-detection-pipeline | aidoc, nvidia-clara, zebra-medical |
| ai-report-assist | radai |
| llm-radiology-use | medpalm-api, google-health |
| pubmed-search | pubmed-ncbi, pubmed_search |
| radiology-metrics | tat_analyzer, radiology_metrics |
| image-quality-audit | image_qc |
| radiology-dataset-guide | dataset_downloader, luna16, brats |
| dataset-preprocessing | monai, dicom_anonymizer |
