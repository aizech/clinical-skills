# DICOMweb Standard Integration

DICOMweb is a set of RESTful web services for accessing medical imaging data defined by the DICOM standard. It provides modern HTTP-based alternatives to traditional DICOM network protocols.

## Overview

DICOMweb defines three main service types:

- **QIDO-RS** (Query Instance, Object, and Retrieve Service): Search and query DICOM objects
- **WADO-RS** (Web Access to DICOM Objects via REST): Retrieve DICOM objects and metadata
- **STOW-RS** (Store Over the Web): Upload/store DICOM objects
- **WADO-URI** (Legacy): Retrieve DICOM objects via URI parameters

**Key Benefits:**
- RESTful API using standard HTTP methods
- JSON metadata for easy parsing
- Support for partial content retrieval (frames)
- Browser-compatible access to images
- No need for DICOM network protocol implementation

**Key Use Cases:**
- Modern web-based PACS viewers
- AI model integration
- Cloud-based medical imaging platforms
- Mobile applications for radiology
- Research data access

## Connection

### Configuration

```yaml
# Required fields
base_url: https://pacs.example.com/dicomweb
api_key: ${DICOMWEB_API_KEY}

# Optional fields
timeout: 30
verify_ssl: true
accept: application/dicom+json
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DICOMWEB_API_KEY` | No | Bearer token for authentication |
| `DICOMWEB_BASE_URL` | No | Override default base URL |
| `DICOMWEB_TIMEOUT` | No | Request timeout in seconds |

## Authentication

DICOMweb supports multiple authentication methods.

```bash
# Basic Auth
curl -u user:pass https://pacs.example.com/dicomweb/studies

# Bearer Token
curl -H "Authorization: Bearer ${DICOMWEB_API_KEY}" \
  https://pacs.example.com/dicomweb/studies

# OAuth2
curl -H "Authorization: Bearer ${OAUTH_TOKEN}" \
  https://pacs.example.com/dicomweb/studies

# DICOM Transfer (for binary data)
curl -H "Accept: application/dicom" \
  https://pacs.example.com/dicomweb/studies/{uid}/series/{uid}/instances/{uid}
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/studies` | GET | List all studies |
| `/studies/{uid}` | GET | Get study metadata |
| `/studies/{uid}/series` | GET | List series in study |
| `/studies/{uid}/series/{uid}` | GET | Get series metadata |
| `/studies/{uid}/series/{uid}/instances` | GET | List instances in series |
| `/studies/{uid}/series/{uid}/instances/{uid}` | GET | Get instance metadata |
| `/studies/{uid}/series/{uid}/instances/{uid}/frames/{n}` | GET | Get specific frame |
| `/studies/{uid}/metadata` | GET | Get bulk study metadata |
| `/studies/{uid}/series/{uid}/metadata` | GET | Get bulk series metadata |
| `/studies/{uid}/series/{uid}/instances/{uid}` | GET | Retrieve DICOM object (WADO) |
| `/studies` | POST | Store DICOM object (STOW) |

## Common Operations

### Patient Name Search

Search for studies by patient name using wildcards.

```bash
# Exact match
GET /studies?PatientName=SMITH

# Wildcard match (any characters)
GET /studies?PatientName=*SMITH*

# Partial match
GET /studies?PatientName=SMITH*
```

**Parameters:**
- `PatientName`: DICOM tag (0010,0010)
- Supports wildcards: `*` (any characters), `?` (single character)

### Modality Filter

Filter studies or series by imaging modality.

```bash
# Studies with specific modality
GET /studies?ModalitiesInStudy=CT

# Studies with multiple modalities
GET /studies?ModalitiesInStudy=CT,MR

# Series by modality
GET /series?Modality=SR
```

**Common Modalities:**
- `CT`: Computed Tomography
- `MR`: Magnetic Resonance
- `XR`: X-Ray
- `US`: Ultrasound
- `PT`: Positron Emission Tomography
- `SR`: Structured Report

### Date Range Queries

Filter by study date using DICOM date format (YYYYMMDD).

```bash
# Specific date
GET /studies?StudyDate=20240403

# Date range
GET /studies?StudyDate=20240101-20240131

# Greater than or equal
GET /studies?StudyDate=ge20240101

# Less than or equal
GET /studies?StudyDate=le20240131

# Recent studies (last 30 days)
GET /studies?StudyDate=-30
```

### Multiple Parameters

Combine multiple query parameters for complex searches.

```bash
GET /studies?
  PatientName=SMITH&
  ModalitiesInStudy=CT&
  StudyDate=20240101-20240131&
  limit=100&
  offset=0
```

**Common Parameters:**
- `limit`: Maximum number of results
- `offset`: Pagination offset
- `includefield`: Include specific fields in response

### Retrieve Specific Frame

Retrieve a single frame from a multi-frame image.

```bash
# Get frame 5 from instance
GET /studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/frames/5

# With content negotiation
GET /studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/frames/5
Accept: image/jpeg
```

## Rate Limits

Rate limits vary by server implementation. Typical values:

| Limit | Value | Notes |
|-------|-------|-------|
| Requests/minute | 100-1000 | Server-dependent |
| Concurrent connections | 10-50 | Server-dependent |
| Payload size | 1GB+ | Depends on server |

Check your specific PACS vendor documentation for actual limits.

## Error Handling

| Status Code | Meaning | Resolution |
|-------------|---------|------------|
| 400 | Bad Request | Check query parameters, DICOM date format |
| 401 | Unauthorized | Verify authentication credentials |
| 403 | Forbidden | Check user permissions |
| 404 | Not Found | Verify study/series/instance UID exists |
| 406 | Not Acceptable | Check Accept header values |
| 415 | Unsupported Media Type | Verify Content-Type for STOW |
| 429 | Too Many Requests | Implement backoff, check rate limits |
| 500 | Internal Server Error | Retry with exponential backoff |

## Tool Registration

```json
{
  "name": "dicomweb",
  "description": "DICOMweb QIDO, WADO, STOW operations for medical imaging",
  "category": "dicomweb",
  "endpoints": [
    "qido_search",
    "wado_retrieve",
    "wado_render",
    "stow_store"
  ],
  "auth_method": "bearer",
  "rate_limit": 100
}
```

## Troubleshooting

### Empty Query Results

**Symptom:** QIDO queries return empty arrays despite data existing

**Solution:**
- Verify base URL includes `/dicicomweb` suffix
- Check authentication credentials
- Verify query parameter names match DICOM tags
- Use `includefield=*` to see all available fields
- Check server logs for query processing errors

### Large Response Times

**Symptom:** Queries take excessive time or timeout

**Solution:**
- Use `limit` parameter to reduce result size
- Add specific filters to narrow search scope
- Use metadata-only endpoints when full objects not needed
- Increase client timeout value
- Consider pagination for large result sets

### Authentication Failures

**Symptom:** 401 Unauthorized responses

**Solution:**
- Verify token is not expired
- Check token has required permissions
- Ensure correct header format: `Authorization: Bearer {token}`
- Test with basic auth if supported
- Contact PACS administrator for access

## References

- [DICOMweb Standard](https://www.dicomstandard.org/using/dicomweb)
- [NEMA DICOMweb Implementation Guide](https://www.dicomstandard.org/using/dicomweb)
- [DICOM Conformance Statements](https://www.dicomstandard.org/using/transition-to-the-web)
- [Google Healthcare API DICOMweb](https://cloud.google.com/healthcare-api/docs/dicom)

## Examples

### Example 1: Complete Study Retrieval Workflow

Retrieve a complete study including all series and instances.

```bash
# Step 1: Search for studies
BASE_URL="https://pacs.example.com/dicomweb"
TOKEN="${DICOMWEB_API_KEY}"

# Search for recent CT studies
curl -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/dicom+json" \
  "$BASE_URL/studies?ModalitiesInStudy=CT&StudyDate=20240401-20240430" \
  > studies.json

# Step 2: Extract study UIDs
jq -r '.[].["0020000D"].Value[0]' studies.json > study_uids.txt

# Step 3: For each study, retrieve series
while read study_uid; do
  echo "Processing study: $study_uid"
  
  curl -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/dicom+json" \
    "$BASE_URL/studies/$study_uid/series" \
    > "${study_uid}_series.json"
    
  jq -r '.[].["0020000E"].Value[0]' "${study_uid}_series.json" > "${study_uid}_series_uids.txt"
done < study_uids.txt

# Step 4: Retrieve instance metadata
while read study_uid; do
  while read series_uid; do
    curl -H "Authorization: Bearer $TOKEN" \
      -H "Accept: application/dicom+json" \
      "$BASE_URL/studies/$study_uid/series/$series_uid/instances" \
      > "${study_uid}_${series_uid}_instances.json"
  done < "${study_uid}_series_uids.txt"
done < study_uids.txt
```

### Example 2: Using Shared CLI Tool

Use the `dicom_qido.py` CLI tool for simplified DICOMweb queries.

```bash
# Search for studies with CLI tool
python tools/clis/dicom_qido.py \
  https://pacs.example.com/dicomweb \
  --modality CT \
  --date 20240401-20240430 \
  --token ${DICOMWEB_API_KEY} \
  --json > studies.json

# Get specific study details
python tools/clis/dicom_qido.py \
  https://pacs.example.com/dicomweb \
  --study-uid "1.2.840.10008.1.2.3.4" \
  --token ${DICOMWEB_API_KEY}
```

### Example 3: Render Image Frame

Retrieve and render a specific frame as JPEG.

```bash
# Get frame as JPEG
STUDY_UID="1.2.840.10008.1.2.3"
SERIES_UID="1.2.840.10008.1.2.4"
INSTANCE_UID="1.2.840.10008.1.2.5"
FRAME_NUM="1"

curl -H "Authorization: Bearer ${DICOMWEB_API_KEY}" \
  -H "Accept: image/jpeg" \
  "https://pacs.example.com/dicomweb/studies/${STUDY_UID}/series/${SERIES_UID}/instances/${INSTANCE_UID}/frames/${FRAME_NUM}" \
  --output frame.jpg

# Get frame as PNG
curl -H "Authorization: Bearer ${DICOMWEB_API_KEY}" \
  -H "Accept: image/png" \
  "https://pacs.example.com/dicomweb/studies/${STUDY_UID}/series/${SERIES_UID}/instances/${INSTANCE_UID}/frames/${FRAME_NUM}" \
  --output frame.png
```

### Example 4: Store DICOM Object (STOW-RS)

Upload a DICOM file to the server.

```bash
# Upload single file
curl -X POST \
  -H "Authorization: Bearer ${DICOMWEB_API_KEY}" \
  -H "Content-Type: application/dicom" \
  -H "Accept: application/dicom+json" \
  --data-binary @image.dcm \
  "https://pacs.example.com/dicomweb/studies"

# Upload multiple files in multipart
curl -X POST \
  -H "Authorization: Bearer ${DICOMWEB_API_KEY}" \
  -H "Content-Type: multipart/related; type=\"application/dicom\"" \
  -H "Accept: application/dicom+json" \
  -F "file=@image1.dcm" \
  -F "file=@image2.dcm" \
  "https://pacs.example.com/dicomweb/studies"
```

## Transfer Syntaxes

DICOMweb servers support various transfer syntaxes for compression.

| Syntax | UID | Description | Lossless |
|--------|-----|-------------|---------|
| Explicit VR Little Endian | 1.2.840.10008.1.2.1 | Default uncompressed | Yes |
| Implicit VR Little Endian | 1.2.840.10008.1.2 | Legacy uncompressed | Yes |
| JPEG Baseline | 1.2.840.10008.1.2.4.50 | Lossy 8-bit JPEG | No |
| JPEG Lossless | 1.2.840.10008.1.2.4.70 | Lossless JPEG | Yes |
| JPEG 2000 Lossless | 1.2.840.10008.1.2.4.90 | Lossless JP2K | Yes |
| JPEG 2000 Lossy | 1.2.840.10008.1.2.4.91 | Lossy JP2K | No |
| RLE Lossless | 1.2.840.10008.1.2.5 | Run-length encoding | Yes |

## Notes

- DICOMweb uses standard HTTP status codes for error handling
- Metadata is returned in DICOM JSON Model format
- Binary data (pixel data) requires separate retrieval
- Not all servers implement all DICOMweb services
- Check server conformance statement for supported features
- Use `Accept` headers to control response format
- QIDO-RS results are typically paginated
- WADO-RS supports partial content for large objects
