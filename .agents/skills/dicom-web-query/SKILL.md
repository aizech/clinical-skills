---
name: dicom-web-query
description: Query and retrieve DICOM objects via DICOMweb REST API. Also use when the user needs to work with DICOMweb servers, retrieve imaging studies via REST, or perform web-based DICOM operations. For traditional DICOM queries, see pacs-workflow.
---

# DICOMweb Query

You are a DICOMweb expert. Your role is to help users interact with DICOMweb-enabled servers for imaging data retrieval.

## DICOMweb Overview

### RESTful DICOM Services

| Service | Method | Description |
|---------|--------|-------------|
| QIDO-RS | GET | Query DICOM images (Query-based ID Retrieve) |
| WADO-RS | GET | Retrieve DICOM objects (Web Access to DICOM) |
| STOW-RS | POST | Store DICOM objects (Store Over the Web) |
| WADO-URI | GET | Retrieve via URI (legacy) |

### Base URL Structure

```
https://pacs.example.com/dicomweb
```

## QIDO-RS (Query)

### Study Search

```python
import requests

BASE_URL = "https://pacs.example.com/dicomweb"

def qido_studies(filters=None, include_fields=None):
    """
    Query for studies using QIDO-RS.
    
    Args:
        filters: Dict of DICOM tags to filter
        include_fields: Specific tags to return
    """
    params = {}
    
    if filters:
        for key, value in filters.items():
            params[f"includefield={key}"] = value
    
    response = requests.get(
        f"{BASE_URL}/studies",
        params=params
    )
    
    return response.json()
```

### Common Query Parameters

| Parameter | DICOM Tag | Description |
|-----------|-----------|-------------|
| 00100010 | PatientName | Patient name |
| 00100020 | PatientID | Patient ID |
| 00080020 | StudyDate | Study date (YYYYMMDD) |
| 00080030 | StudyTime | Study time |
| 00080050 | AccessionNumber | Accession number |
| 00080060 | Modality | Imaging modality |
| 00081030 | StudyDescription | Study description |
| 00200010 | StudyInstanceUID | Study UID |

### Query by Patient

```python
def find_studies_by_patient(patient_id):
    """Find all studies for a patient."""
    params = {
        "PatientID": patient_id,
        "includefield": "00080020,00080030,00080060"
    }
    
    response = requests.get(f"{BASE_URL}/studies", params=params)
    return response.json()
```

### Query by Date Range

```python
def find_studies_by_date(start_date, end_date, modality=None):
    """Find studies within date range."""
    params = {
        "StudyDate": f"{start_date}-{end_date}"
    }
    
    if modality:
        params["Modality"] = modality
    
    response = requests.get(f"{BASE_URL}/studies", params=params)
    return response.json()
```

### Query by Modality

```python
def find_ct_studies(limit=100):
    """Find CT studies."""
    params = {
        "Modality": "CT",
        "limit": limit
    }
    
    response = requests.get(f"{BASE_URL}/studies", params=params)
    return response.json()
```

## WADO-RS (Retrieve)

### Retrieve Study

```python
def retrieve_study(study_uid, format="application/dicom+json"):
    """
    Retrieve study metadata.
    
    Args:
        study_uid: Study Instance UID
        format: Response format
    """
    headers = {"Accept": format}
    
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}",
        headers=headers
    )
    
    return response.json()
```

### Retrieve as DICOM (ZIP)

```python
def download_study_dicom(study_uid, output_path=None):
    """Download complete study as DICOM ZIP."""
    headers = {"Accept": "application/zip"}
    
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/archive",
        headers=headers,
        stream=True
    )
    
    if output_path:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    return response.content
```

### Retrieve Series

```python
def retrieve_series(study_uid, series_uid):
    """Retrieve specific series."""
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/series/{series_uid}",
        headers={"Accept": "application/dicom+json"}
    )
    return response.json()
```

### Retrieve Single Instance

```python
def retrieve_instance(study_uid, series_uid, instance_uid):
    """Retrieve single DICOM instance metadata."""
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}",
        headers={"Accept": "application/dicom+json"}
    )
    return response.json()
```

### Retrieve Pixel Data

```python
def retrieve_image_pixels(study_uid, series_uid, instance_uid, frame=1):
    """
    Retrieve image pixel data.
    
    Args:
        study_uid: Study Instance UID
        series_uid: Series Instance UID
        instance_uid: SOP Instance UID
        frame: Frame number (1-indexed for multi-frame)
    """
    url = f"{BASE_URL}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/frames/{frame}"
    
    response = requests.get(
        url,
        headers={"Accept": "image/jpeg"}
    )
    
    return response.content  # JPEG image data
```

## WADO-RS Metadata

### Study Metadata

```python
def get_study_metadata(study_uid):
    """Get complete study metadata."""
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/metadata",
        headers={"Accept": "application/dicom+json"}
    )
    return response.json()
```

### Series Metadata

```python
def get_series_metadata(study_uid, series_uid):
    """Get series metadata."""
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/series/{series_uid}/metadata",
        headers={"Accept": "application/dicom+json"}
    )
    return response.json()
```

### Instance Metadata

```python
def get_instance_metadata(study_uid, series_uid, instance_uid):
    """Get single instance metadata."""
    response = requests.get(
        f"{BASE_URL}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/metadata",
        headers={"Accept": "application/dicom+json"}
    )
    return response.json()
```

## Thumbnail Retrieval

```python
def get_thumbnail(study_uid, series_uid=None):
    """
    Retrieve study or series thumbnail.
    
    Args:
        study_uid: Study Instance UID
        series_uid: Optional series UID
    """
    if series_uid:
        url = f"{BASE_URL}/studies/{study_uid}/series/{series_uid}/thumbnail"
    else:
        # Get first series thumbnail
        url = f"{BASE_URL}/studies/{study_uid}/thumbnail"
    
    response = requests.get(
        url,
        headers={"Accept": "image/jpeg"}
    )
    
    return response.content
```

## STOW-RS (Store)

### Store DICOM File

```python
def store_dicom(file_path, study_uid=None):
    """
    Store DICOM file to server.
    
    Args:
        file_path: Path to DICOM file
        study_uid: Optional existing study UID to add to
    """
    with open(file_path, "rb") as f:
        data = f.read()
    
    headers = {
        "Content-Type": "application/dicom",
        "Accept": "application/dicom+json"
    }
    
    response = requests.post(
        f"{BASE_URL}/studies{'/' + study_uid if study_uid else ''}/instances",
        headers=headers,
        data=data
    )
    
    return response.json()
```

## Pagination

### Limit Results

```python
def qido_with_pagination(filters, limit=100, offset=0):
    """Query with pagination."""
    params = {
        "limit": limit,
        "offset": offset,
        **filters
    }
    
    response = requests.get(f"{BASE_URL}/studies", params=params)
    
    # Check for more results
    total = response.headers.get("X-Total-Count", "unknown")
    
    return {
        "results": response.json(),
        "total": total,
        "has_more": (offset + limit) < int(total) if total.isdigit() else True
    }
```

## Common Patterns

### Find and Download Study

```python
def find_and_download(patient_id, output_dir):
    """Find patient's latest study and download."""
    # Find studies
    studies = find_studies_by_patient(patient_id)
    
    if not studies:
        return None
    
    # Get most recent
    latest = studies[0]
    study_uid = latest["0020000D"]["Value"][0]
    
    # Download
    download_path = f"{output_dir}/{study_uid}.zip"
    download_study_dicom(study_uid, download_path)
    
    return download_path
```

### Bulk Retrieve by Date

```python
def download_studies_by_date(start_date, end_date, modality, output_dir):
    """Download all studies for date range."""
    studies = find_studies_by_date(start_date, end_date, modality)
    
    downloaded = []
    for study in studies:
        study_uid = study["0020000D"]["Value"][0]
        try:
            path = f"{output_dir}/{study_uid}.zip"
            download_study_dicom(study_uid, path)
            downloaded.append(path)
        except Exception as e:
            print(f"Failed to download {study_uid}: {e}")
    
    return downloaded
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Study/series doesn't exist | Verify UID |
| 401 Unauthorized | Auth required | Add credentials |
| 403 Forbidden | Insufficient permissions | Check user roles |
| 500 Server Error | Server issue | Retry later |

## Authentication

### Basic Auth

```python
from requests.auth import HTTPBasicAuth

def authenticated_request(url, auth):
    """Make authenticated request."""
    response = requests.get(
        url,
        auth=HTTPBasicAuth(auth["username"], auth["password"])
    )
    return response
```

### Bearer Token

```python
def token_auth_request(url, token):
    """Make request with bearer token."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response
```

## Related Skills

- **pacs-workflow**: For PACS-specific operations
- **filesystem-imaging**: For local file handling
- **radiology-context**: For configuration

## Examples

### Example 1: Query and Download CT Study

```python
# Find CT studies from last week
studies = find_studies_by_date("20260325", "20260403", "CT")

# Download first result
if studies:
    study_uid = studies[0]["0020000D"]["Value"][0]
    download_study_dicom(study_uid, "ct_study.zip")
```

### Example 2: Get Study Metadata

```python
metadata = get_study_metadata("1.2.840.12345.67890")
for item in metadata:
    print(f"{item['0020000D']['vr']}: {item['00080018']['Value']}")
```

### Example 3: Retrieve Image for Viewing

```python
# Get thumbnail
thumb = get_thumbnail("1.2.840.12345.67890")

# Save as JPEG
with open("thumbnail.jpg", "wb") as f:
    f.write(thumb)
```
