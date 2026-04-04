# CLI Tools API Documentation

This document provides API documentation for the CLI tools in the `tools/clis/` directory.

## Table of Contents

- [Radiology Metrics](#radiology-metrics)
- [DICOM Info](#dicom-info)
- [DICOM QIDO](#dicom-qido)
- [Image QC](#image-qc)
- [PubMed Search](#pubmed-search)
- [Shared Utilities](#shared-utilities)

---

## Radiology Metrics

### Module: `tools/clis/radiology_metrics.py`

#### Functions

##### `generate_sample_metrics(base_url=None, days=30, radiologists=None, modalities=None)`

Generate sample radiology productivity metrics.

**Parameters:**
- `base_url` (str, optional): Base URL for metrics API
- `days` (int, optional): Number of days to generate data for (default: 30)
- `radiologists` (list[str], optional): List of radiologist names
- `modalities` (list[str], optional): List of imaging modalities

**Returns:**
- `dict`: Dictionary containing metrics data

**Example:**
```python
from tools.clis.radiology_metrics import generate_sample_metrics

metrics = generate_sample_metrics(days=7, radiologists=["Dr. Smith", "Dr. Jones"])
```

##### `print_metrics(metrics, verbose=False)`

Print radiology metrics in formatted output.

**Parameters:**
- `metrics` (dict): Metrics dictionary from `generate_sample_metrics`
- `verbose` (bool, optional): Enable verbose output (default: False)

**Returns:**
- `None`

---

## DICOM Info

### Module: `tools/clis/dicom_info.py`

#### Functions

##### `format_value(value)`

Format DICOM tag values for display.

**Parameters:**
- `value`: DICOM tag value

**Returns:**
- `str`: Formatted string representation

##### `print_dicom_info(ds, sections=None, search_tag=None)`

Print DICOM dataset information.

**Parameters:**
- `ds` (pydicom.Dataset): DICOM dataset
- `sections` (dict, optional): Dictionary of sections to display
- `search_tag` (str, optional): Tag keyword to search for

**Returns:**
- `None`

---

## DICOM QIDO

### Module: `tools/clis/dicom_qido.py`

#### Functions

##### `search_studies(base_url, patient_name=None, modality=None, date_from=None, date_to=None, auth_token=None)`

Search for studies via QIDO-RS.

**Parameters:**
- `base_url` (str): DICOMweb server base URL
- `patient_name` (str, optional): Patient name filter
- `modality` (str, optional): Modality filter
- `date_from` (str, optional): Start date (YYYYMMDD)
- `date_to` (str, optional): End date (YYYYMMDD)
- `auth_token` (str, optional): Bearer authentication token

**Returns:**
- `list[dict]`: List of study metadata

**Example:**
```python
from tools.clis.dicom_qido import search_studies

studies = search_studies(
    "https://example.com/dicomweb",
    patient_name="Smith",
    modality="CT",
    date_from="20240101",
    date_to="20241231"
)
```

##### `get_study_details(base_url, study_uid, auth_token=None)`

Get detailed metadata for a study.

**Parameters:**
- `base_url` (str): DICOMweb server base URL
- `study_uid` (str): Study instance UID
- `auth_token` (str, optional): Bearer authentication token

**Returns:**
- `list[dict]`: Study metadata

##### `search_series(base_url, study_uid, modality=None, auth_token=None)`

Search for series within a study.

**Parameters:**
- `base_url` (str): DICOMweb server base URL
- `study_uid` (str): Study instance UID
- `modality` (str, optional): Modality filter
- `auth_token` (str, optional): Bearer authentication token

**Returns:**
- `list[dict]`: List of series metadata

---

## Image QC

### Module: `tools/clis/image_qc.py`

#### Functions

##### `analyze_ct_quality(ds)`

Analyze CT image quality metrics.

**Parameters:**
- `ds` (pydicom.Dataset): DICOM dataset

**Returns:**
- `dict`: Quality metrics including noise, CNR, dose metrics

**Example:**
```python
from tools.clis.image_qc import analyze_ct_quality
import pydicom

ds = pydicom.dcmread("ct_scan.dcm")
metrics = analyze_ct_quality(ds)
```

##### `analyze_mr_quality(ds)`

Analyze MR image quality metrics.

**Parameters:**
- `ds` (pydicom.Dataset): DICOM dataset

**Returns:**
- `dict`: Quality metrics including SNR, uniformity

##### `analyze_xray_quality(ds)`

Analyze X-ray image quality metrics.

**Parameters:**
- `ds` (pydicom.Dataset): DICOM dataset

**Returns:**
- `dict`: Quality metrics including contrast, dynamic range

##### `analyze_file(file_path)`

Analyze a DICOM file and determine modality.

**Parameters:**
- `file_path` (str or Path): Path to DICOM file

**Returns:**
- `dict`: Quality metrics for the appropriate modality

---

## PubMed Search

### Module: `tools/clis/pubmed_search.py`

#### Functions

##### `search_pubmed(query, max_results=20, api_key=None, article_type=None, date_from=None)`

Search PubMed for articles.

**Parameters:**
- `query` (str): Search query
- `max_results` (int, optional): Maximum results to return (default: 20)
- `api_key` (str, optional): NCBI API key
- `article_type` (str, optional): Article type filter
- `date_from` (str, optional): Date filter (e.g., "30" for last 30 days)

**Returns:**
- `list[str]`: List of PubMed IDs

**Example:**
```python
from tools.clis.pubmed_search import search_pubmed

pmids = search_pubmed("lung nodule", max_results=50, date_from="30")
```

##### `get_article_summary(pmids, api_key=None)`

Get article summaries for PMIDs.

**Parameters:**
- `pmids` (list[str]): List of PubMed IDs
- `api_key` (str, optional): NCBI API key

**Returns:**
- `list[dict]`: List of article summaries with title, authors, journal, etc.

##### `fetch_articles(pmids, return_type="medline", api_key=None)`

Fetch full article details.

**Parameters:**
- `pmids` (list[str]): List of PubMed IDs
- `return_type` (str, optional): Return format (default: "medline")
- `api_key` (str, optional): NCBI API key

**Returns:**
- `str`: Article data in requested format

---

## Shared Utilities

### Module: `tools/clis/shared/api_client.py`

#### Classes

##### `APIClient`

HTTP client with retry logic for API requests.

**Methods:**
- `__init__(base_url, timeout=30, max_retries=3)`: Initialize client
- `get(endpoint, params=None, headers=None)`: GET request with retry
- `post(endpoint, data=None, json=None, headers=None)`: POST request with retry
- `close()`: Close the HTTP session

**Example:**
```python
from tools.clis.shared.api_client import APIClient

client = APIClient("https://api.example.com", timeout=30)
response = client.get("/endpoint", params={"key": "value"})
client.close()
```

##### `BearerTokenAuth`

Bearer token authentication helper.

**Methods:**
- `__init__(token)`: Initialize with token
- `get_headers()`: Return Authorization header

**Example:**
```python
from tools.clis.shared.api_client import BearerTokenAuth

auth = BearerTokenAuth("my-token")
headers = auth.get_headers()  # {"Authorization": "Bearer my-token"}
```

---

### Module: `tools/clis/shared/base_cli.py`

#### Functions

##### `create_base_parser(description)`

Create base argparse parser with common arguments.

**Parameters:**
- `description` (str): Tool description

**Returns:**
- `argparse.ArgumentParser`: Configured parser

##### `setup_logging(level="INFO")`

Setup logging configuration.

**Parameters:**
- `level` (str, optional): Log level (default: "INFO")

**Returns:**
- `None`

##### `handle_error(message, exit_code=1)`

Handle and display errors.

**Parameters:**
- `message` (str): Error message
- `exit_code` (int, optional): Exit code (default: 1)

**Returns:**
- `None`

---

### Module: `tools/clis/shared/json_formatter.py`

#### Functions

##### `print_json(data, indent=2)`

Print data as formatted JSON.

**Parameters:**
- `data`: Data to serialize
- `indent` (int, optional): JSON indentation (default: 2)

**Returns:**
- `None`

##### `format_json(data, indent=2)`

Format data as JSON string.

**Parameters:**
- `data`: Data to serialize
- `indent` (int, optional): JSON indentation (default: 2)

**Returns:**
- `str`: JSON formatted string

---

## Error Handling

All CLI tools use consistent error handling:

- Network errors are caught and re-raised with context
- File I/O errors are caught and reported gracefully
- Invalid input is validated and reported with clear messages
- All functions document expected exceptions

---

## Dependencies

### Required Python Packages:
- `pydicom` - DICOM file parsing
- `numpy` - Numerical operations for image processing
- `requests` - HTTP client (used by APIClient)

### Development Dependencies:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities

---

## Usage Examples

### Example 1: Query DICOMweb for Studies

```python
from tools.clis.dicom_qido import search_studies

studies = search_studies(
    base_url="https://pacs.example.com/dicomweb",
    patient_name="Smith",
    modality="CT",
    date_from="20240101",
    date_to="20240131"
)

for study in studies:
    print(f"Study UID: {study['0020000D']['Value'][0]}")
```

### Example 2: Analyze DICOM Image Quality

```python
from tools.clis.image_qc import analyze_file
import json

metrics = analyze_file("scan.dcm")
print(json.dumps(metrics, indent=2))
```

### Example 3: Search PubMed Literature

```python
from tools.clis.pubmed_search import search_pubmed, get_article_summary

pmids = search_pubmed("artificial intelligence radiology")
summaries = get_article_summary(pmids)

for article in summaries:
    print(f"{article['title']} - {article['journal']}")
```

---

## Version History

- v1.0.0 - Initial API documentation
