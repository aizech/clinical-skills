# Orthanc PACS Integration

Lightweight DICOM server for PACS query/retrieve operations.

## Connection

```yaml
host: orthanc.example.com
port: 8042
username: admin
password: ${ORTHANC_PASSWORD}
```

## Authentication

HTTP Basic Auth or token-based with `--token` parameter.

## Key Endpoints

- `GET /patients` - List all patients
- `GET /studies?patient={id}` - Studies for patient
- `GET /series?study={id}` - Series for study
- `GET /instances?series={id}` - Instances for series
- `POST /tools/find` - Advanced DICOM query
- `GET /download={instance_id}` - Download DICOM file

## Common Queries

```bash
# Find patient by name
curl -u admin:pass http://orthanc:8042/patients?search=Smith

# Get study details
curl -u admin:pass http://orthanc:8042/studies/{study_id}

# Download instance
curl -u admin:pass http://orthanc:8042/instances/{id}/file -o image.dcm
```

## Rate Limits

Default: 100 requests/second. Configurable in Orthanc.json.

## Tool Registration

```json
{
  "name": "orthanc_pacs",
  "description": "Query and retrieve DICOM studies from Orthanc PACS",
  "category": "pacs",
  "endpoints": ["dicom_query", "dicom_retrieve", "study_search"]
}
```
