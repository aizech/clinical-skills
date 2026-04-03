# DICOMweb Standard Integration

DICOMweb RESTful services for medical imaging.

## Endpoints Overview

### QIDO-RS (Query)
```
GET {base}/studies
GET {base}/studies/{uid}
GET {base}/studies/{uid}/series
GET {base}/studies/{uid}/series/{uid}
GET {base}/studies/{uid}/series/{uid}/instances
GET {base}/studies/{uid}/series/{uid}/instances/{uid}
```

### WADO-RS (Retrieve)
```
GET {base}/studies/{uid}/metadata
GET {base}/studies/{uid}/series/{uid}/metadata
GET {base}/studies/{uid}/series/{uid}/instances/{uid}/metadata
GET {base}/studies/{uid}/series/{uid}/instances/{uid}/frames/{n}
GET {base}/studies/{uid}/series/{uid}/instances/{uid}
```

### WADO-URI (Legacy)
```
GET {base}/wado?studyUID={uid}&seriesUID={sid}&objectUID={oid}
```

### STOW-RS (Store)
```
POST {base}/studies
```

## Authentication

```bash
# Basic Auth
curl -u user:pass {base}/studies

# Bearer Token
curl -H "Authorization: Bearer {token}" {base}/studies

# DICOM Transfer (for binary)
--header "Accept: application/dicom"
```

## Common Queries

### Patient Name Search
```bash
GET /studies?PatientName=SMITH
GET /studies?PatientName=*DOE*
```

### Modality Filter
```bash
GET /studies?ModalitiesInStudy=CT,MR
GET /series?Modality=SR
```

### Date Range
```bash
GET /studies?StudyDate=20240101-20240131
GET /studies?StudyDate=ge20240101
```

### Multiple Parameters
```bash
GET /studies?
  PatientName=SMITH&
  ModalitiesInStudy=CT&
  StudyDate=20240101-20240131
```

## Response Headers

### Success
```http
200 OK
Content-Type: application/dicom+json
X-Request-Id: abc123
```

### Error
```http
4xx/5xx Error
Content-Type: application/dicom+json
```

## Transfer Syntaxes

| Syntax | UID | Description |
|--------|-----|-------------|
| Explicit VR Little Endian | 1.2.840.10008.1.2.1 | Lossless |
| JPEG Baseline | 1.2.840.10008.1.2.4.50 | Lossy 8-bit |
| JPEG 2000 | 1.2.840.10008.1.2.4.90 | Lossless JP2K |
| JPEG 2000 | 1.2.840.10008.1.2.4.91 | Lossy JP2K |

## Rate Limits

Server-dependent. Typical: 100-1000 req/min.

## Tool Registration

```json
{
  "name": "dicomweb",
  "description": "DICOMweb QIDO, WADO, STOW operations",
  "category": "dicomweb",
  "endpoints": ["qido_search", "wado_retrieve", "wado_render", "stow_store"]
}
```
