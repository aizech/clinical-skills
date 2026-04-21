---
name: pacs-workflow
description: Query PACS, retrieve studies, manage worklists, and integrate with PACS workflows. Also use when the user needs to interact with picture archiving systems, search for imaging studies, retrieve DICOM data, or manage radiologist worklists. For DICOMweb REST queries, see dicom-web-query.
---

# PACS Workflow

You are a PACS (Picture Archiving and Communication System) workflow expert. Your role is to help users query, retrieve, and manage imaging studies.

## Supported PACS Systems

| PACS Type | DICOM Support | API Style |
|-----------|---------------|-----------|
| Orthanc | Full | REST API, DICOMweb |
| DCM4CHEE | Full | REST API, DICOMweb |
| Conquest | Full | DICOM, limited REST |
| OHIF Viewer | Full | DICOMweb client |
| Commercial PACS | Varies | Vendor-specific |

## DICOM Query (C-FIND)

### Query Models

| Level | Description | Key Tags |
|-------|-------------|----------|
| Patient | Find patients | Patient Name, ID, DOB |
| Study | Find studies | Study Date, Modality, Accession |
| Series | Find series | Series Number, Body Part |
| Instance | Find images | SOP Instance UID |

### Common Query Filters

```python
# Patient Level Query
patient_query = {
    "PatientName": "DOE^JOHN",
    "PatientID": "12345",
    "PatientBirthDate": "19800115"
}

# Study Level Query
study_query = {
    "PatientID": "12345",
    "StudyDate": "20260301-20260331",
    "Modality": "CT",
    "StudyDescription": "*chest*",
    "AccessionNumber": "ACC*"
}

# Series Level Query
series_query = {
    "StudyInstanceUID": "1.2.840.12345",
    "SeriesNumber": "*",
    "BodyPartExamined": "CHEST",
    "Modality": "CT"
}
```

## Orthanc PACS

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools/find` | POST | Query studies |
| `/patients` | GET | List patients |
| `/studies` | GET | List all studies |
| `/studies/{id}` | GET | Get study |
| `/studies/{id}/archive` | GET | Download ZIP |
| `/modalities` | GET | List modalities |

### Example: Find Studies

```python
import requests

def orthanc_find_studies(base_url, filters):
    """
    Query Orthanc for studies.
    
    Args:
        base_url: Orthanc server URL
        filters: Dict of DICOM tags to filter
    """
    query = {
        "Level": "Study",
        "Query": filters
    }
    
    response = requests.post(
        f"{base_url}/tools/find",
        json=query
    )
    
    return response.json()

# Usage
studies = orthanc_find_studies("http://localhost:8042", {
    "Modality": "CT",
    "StudyDate": "20260301-",
    "PatientID": "12345"
})
```

### Example: Retrieve Study

```python
def orthanc_retrieve_study(base_url, study_id):
    """Download entire study as ZIP."""
    response = requests.get(
        f"{base_url}/studies/{study_id}/archive"
    )
    return response.content
```

## DCM4CHEE PACS

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rs/studies` | GET | Query studies (QIDO-RS) |
| `/rs/studies/{uid}` | GET | Get study metadata |
| `/wado/rs/studies/{uid}` | GET | Retrieve study (WADO-RS) |
| `/aets/{ae_title}/worklist` | GET | Modality worklist |

### Example: QIDO-RS Query

```python
def dcm4chee_find_studies(base_url, ae_title, filters):
    """Query DCM4CHEE using QIDO-RS."""
    params = {
        "includefield": "00080020,00080030,00080050,00080090",
    }
    params.update(filters)
    
    response = requests.get(
        f"{base_url}/aets/{ae_title}/rs/studies",
        params=params
    )
    
    return response.json()
```

## Modality Worklist (MWL)

### Query Worklist

```python
def query_worklist(pacs_url, ae_title, date=None):
    """
    Query modality worklist for scheduled procedures.
    
    Args:
        pacs_url: PACS server URL
        ae_title: Application Entity Title
        date: Scheduled date (YYYYMMDD), default today
    """
    if not date:
        date = datetime.now().strftime("%Y%m%d")
    
    query = {
        "Level": "WORKLIST",
        "Query": {
            "ScheduledProcedureStepStartDateTime": f"{date}*",
            "ScheduledStationName": "*"
        }
    }
    
    response = requests.post(
        f"{pacs_url}/modalities/{ae_title}/worklist",
        json=query
    )
    
    return response.json()
```

## Query Patterns

### By Patient

```python
# Find all studies for patient
def find_patient_studies(pacs_url, patient_id):
    """Find all studies for a patient."""
    return pacs_query(pacs_url, {
        "PatientID": patient_id,
        "Level": "Study"
    })

# Find patient by name
def find_patient_by_name(pacs_url, last_name, first_name):
    """Find patient by name."""
    return pacs_query(pacs_url, {
        "PatientName": f"{last_name}^{first_name}",
        "Level": "Patient"
    })
```

### By Date Range

```python
def find_studies_by_date_range(pacs_url, start_date, end_date, modality=None):
    """
    Find studies within date range.
    
    Args:
        start_date: YYYYMMDD
        end_date: YYYYMMDD
        modality: Optional modality filter
    """
    filters = {
        "StudyDate": f"{start_date}-{end_date}",
        "Level": "Study"
    }
    
    if modality:
        filters["Modality"] = modality
    
    return pacs_query(pacs_url, filters)
```

### By Modality and Body Part

```python
def find_by_modality_body(pacs_url, modality, body_part):
    """Find studies by modality and body part."""
    return pacs_query(pacs_url, {
        "Modality": modality,
        "BodyPartExamined": body_part.upper(),
        "Level": "Study"
    })
```

## Study Retrieval

### Download Study as ZIP

```python
def retrieve_study_zip(pacs_url, study_uid):
    """Download complete study as ZIP archive."""
    response = requests.get(
        f"{pacs_url}/studies/{study_uid}/archive",
        stream=True
    )
    return response.content

# Save to file
with open(f"{study_uid}.zip", "wb") as f:
    f.write(retrieve_study_zip(pacs_url, study_uid))
```

### Retrieve Specific Series

```python
def retrieve_series(pacs_url, study_uid, series_uid):
    """Download specific series."""
    response = requests.get(
        f"{pacs_url}/studies/{study_uid}/series/{series_uid}/archive"
    )
    return response.content
```

## Workflow Integration

### Radiologist Worklist

```python
def get_radiologist_worklist(pacs_url, radiologist_name, date=None):
    """
    Get worklist for specific radiologist.
    
    Filters by Performing Physician or Reading Physician.
    """
    filters = {
        "StudyDate": date or datetime.now().strftime("%Y%m%d"),
        "ReferringPhysicianName": radiologist_name,
        "Level": "Study"
    }
    
    return pacs_query(pacs_url, filters)
```

### Priority Studies

```python
def find_priority_studies(pacs_url, priority="STAT"):
    """Find emergent/priority studies."""
    return pacs_query(pacs_url, {
        "StudyPriority": priority,
        "Level": "Study"
    })
```

## Common Queries

| Task | Query |
|------|-------|
| Today's CT scans | Modality=CT, StudyDate=today |
| Brain MRI for patient | PatientID=X, Modality=MR, BodyPart=BRAIN |
| Lung nodule follow-up | StudyDescription=*nodule*, Modality=CT |
| STAT reads | StudyPriority=STAT |
| Chest X-rays this week | Modality=DX, StudyDate=last 7 days |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Wrong URL/port | Verify PACS URL |
| Auth failed | Wrong credentials | Check auth config |
| No results | Query too specific | Broaden filters |
| Timeout | Large dataset | Add date limits |

## Related Skills

- **dicom-web-query**: For DICOMweb REST operations
- **filesystem-imaging**: For local file handling
- **radiology-context**: For PACS configuration
- **modality-detection**: For modality identification

## Examples

### Example 1: Find Recent CT Studies

**Request**: "Find CT chest studies from the last week"
```python
find_studies_by_date_range(
    "http://localhost:8042",
    start_date="20260325",
    end_date="20260403",
    modality="CT"
)
```

### Example 2: Patient History

**Request**: "Show all imaging for patient 12345"
```python
find_patient_studies("http://localhost:8042", "12345")
```

### Example 3: Urgent Worklist

**Request**: "Get STAT reads for today"
```python
find_priority_studies("http://localhost:8042", "STAT")
```
