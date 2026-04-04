# Orthanc PACS Integration

Lightweight, open-source DICOM server for PACS query/retrieve operations. Orthanc provides a RESTful API and DICOMweb interface for medical imaging workflows.

## Overview

Orthanc is a standalone DICOM server that turns any computer into a PACS (Picture Archiving and Communication System). It provides:

- DICOM protocol support (C-STORE, C-FIND, C-MOVE, C-GET)
- RESTful API for easy integration
- DICOMweb standard implementation (QIDO-RS, WADO-RS, STOW-RS)
- Web UI for study viewing and management
- Plugin system for extending functionality

**Key Use Cases:**
- On-premises PACS for small to medium practices
- Development and testing environment
- DICOM routing and forwarding
- Research data management
- AI model integration gateway

## Connection

### Configuration

```yaml
# Required fields
host: orthanc.example.com
port: 8042
username: orthanc
password: ${ORTHANC_PASSWORD}

# Optional fields
timeout: 30
verify_ssl: true
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ORTHANC_PASSWORD` | Yes | Password for authentication |
| `ORTHANC_HOST` | No | Override default host |
| `ORTHANC_PORT` | No | Override default port (default: 8042) |

## Authentication

HTTP Basic Auth is the default method. Bearer token authentication is also supported via the `--token` parameter.

```bash
# Basic Auth
curl -u orthanc:${ORTHANC_PASSWORD} http://orthanc:8042/patients

# Using the CLI tool with token
python tools/clis/dicom_qido.py \
  http://orthanc:8042/dicomweb \
  --token ${ORTHANC_PASSWORD}
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/patients` | GET | List all patients |
| `/studies` | GET | List all studies |
| `/studies/{id}` | GET | Get study details |
| `/series` | GET | List all series |
| `/series/{id}` | GET | Get series details |
| `/instances` | GET | List all instances |
| `/instances/{id}` | GET | Get instance details |
| `/instances/{id}/file` | GET | Download DICOM file |
| `/tools/find` | POST | Advanced DICOM query |
| `/modalities` | GET | List configured DICOM modalities |
| `/queries/{id}/answers` | GET | Get C-FIND query results |

## Common Operations

### Find Patient by Name

Search for patients matching a name pattern.

```bash
# Find patient by name (partial match)
curl -u orthanc:${ORTHANC_PASSWORD} \
  "http://orthanc:8042/patients?expand" | \
  jq '.[] | select(.PatientName | contains("Smith"))'
```

**Parameters:**
- `expand`: Include full patient details (default: false)
- `limit`: Maximum number of results
- `since`: Offset for pagination

**Response:**
```json
{
  "ID": "abc123",
  "PatientID": "PATIENT001",
  "PatientName": "Smith^John",
  "Studies": ["study1", "study2"]
}
```

### Get Study Details

Retrieve complete metadata for a specific study.

```bash
# Get study details
curl -u orthanc:${ORTHANC_PASSWORD} \
  http://orthanc:8042/studies/{study_id} \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "ID": "study1",
  "MainDicomTags": {
    "StudyDescription": "CT Chest",
    "StudyDate": "20240403",
    "StudyTime": "143000"
  },
  "Series": ["series1", "series2"],
  "PatientMainDicomTags": {
    "PatientID": "PATIENT001",
    "PatientName": "Smith^John"
  }
}
```

### Download DICOM File

Download a specific DICOM instance to disk.

```bash
# Download instance
curl -u orthanc:${ORTHANC_PASSWORD} \
  http://orthanc:8042/instances/{instance_id}/file \
  -o image.dcm

# Verify downloaded file
dcm2json image.dcm | jq .
```

### Advanced DICOM Query

Perform complex DICOM queries using the `/tools/find` endpoint.

```bash
# Find CT studies from specific date range
curl -u orthanc:${ORTHANC_PASSWORD} \
  http://orthanc:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Study",
    "Query": {
      "Modality": "CT",
      "StudyDate": "20240101-20240331"
    }
  }'
```

**Parameters:**
- `Level`: "Patient", "Study", "Series", or "Instance"
- `Query`: DICOM tag key-value pairs
- `Expand`: Include full details in response

## Rate Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Requests/second | 100 | Default configuration |
| Concurrent connections | 50 | Configurable in `Orthanc.json` |
| Query timeout | 30 seconds | Per request |

Rate limits can be adjusted in the Orthanc configuration file:

```json
{
  "HttpServer": {
    "TcpPort": 8042,
    "RemoteAccessAllowed": true,
    "KeepAlive": true
  }
}
```

## Error Handling

| Status Code | Meaning | Resolution |
|-------------|---------|------------|
| 401 | Unauthorized | Verify username and password |
| 404 | Not Found | Check resource ID exists |
| 415 | Unsupported Media Type | Ensure correct Content-Type header |
| 500 | Internal Server Error | Check Orthanc logs |

## Tool Registration

```json
{
  "name": "orthanc_pacs",
  "description": "Query and retrieve DICOM studies from Orthanc PACS server",
  "category": "pacs",
  "endpoints": [
    "dicom_query",
    "dicom_retrieve",
    "study_search",
    "patient_search"
  ],
  "auth_method": "basic",
  "rate_limit": 100
}
```

## Troubleshooting

### Connection Refused

**Symptom:** `curl: (7) Failed to connect to orthanc:8042`

**Solution:**
- Verify Orthanc is running: `systemctl status orthanc`
- Check port is open: `netstat -tlnp | grep 8042`
- Ensure firewall allows traffic on port 8042

### Authentication Failed

**Symptom:** `401 Unauthorized`

**Solution:**
- Verify username and password in environment variables
- Check `Orthanc.json` configuration for registered users
- Reset password if necessary

### Empty Query Results

**Symptom:** Queries return empty arrays

**Solution:**
- Verify data exists in Orthanc: check web UI
- Check query parameters match DICOM tags
- Use `expand=true` to see available fields
- Verify date format (YYYYMMDD)

## References

- [Official Documentation](https://book.orthanc-server.com/)
- [REST API Reference](https://book.orthanc-server.com/users/rest.html)
- [DICOM Conformance](https://book.orthanc-server.com/users/dicom-conformance.html)
- [GitHub Repository](https://github.com/jodogne/Orthanc)

## Examples

### Example 1: Complete Study Retrieval Workflow

Retrieve all CT studies for a specific patient and download images.

```bash
# Step 1: Find patient by ID
PATIENT_ID="PATIENT001"
curl -u orthanc:${ORTHANC_PASSWORD} \
  "http://orthanc:8042/patients?expand" | \
  jq ".[] | select(.PatientID == \"$PATIENT_ID\")" > patient.json

# Step 2: Get study IDs
STUDY_IDS=$(jq -r '.[].Studies[]' patient.json)

# Step 3: For each study, get series
for study_id in $STUDY_IDS; do
  curl -u orthanc:${ORTHANC_PASSWORD} \
    "http://orthanc:8042/studies/$study_id?expand" | \
    jq '.Series[]' > series_ids.txt
done

# Step 4: Download all instances
while read series_id; do
  curl -u orthanc:${ORTHANC_PASSWORD} \
    "http://orthanc:8042/series/$series_id?expand" | \
    jq -r '.Instances[]' > instance_ids.txt

  while read instance_id; do
    curl -u orthanc:${ORTHANC_PASSWORD} \
      "http://orthanc:8042/instances/$instance_id/file" \
      -o "${instance_id}.dcm"
  done < instance_ids.txt
done < series_ids.txt
```

### Example 2: DICOMweb Query Using CLI Tool

Use the shared CLI utility to query Orthanc via DICOMweb.

```bash
# Search for CT studies from last 7 days
python tools/clis/dicom_qido.py \
  http://orthanc:8042/dicomweb \
  --modality CT \
  --date $(date -d "7 days ago" +%Y%m%d)-$(date +%Y%m%d) \
  --token ${ORTHANC_PASSWORD} \
  --json

# Get specific study details
python tools/clis/dicom_qido.py \
  http://orthanc:8042/dicomweb \
  --study-uid "1.2.840.10008.1.2.3.4" \
  --token ${ORTHANC_PASSWORD}
```

### Example 3: Automated Backup

Backup all studies from Orthanc to external storage.

```bash
#!/bin/bash
# backup_orthanc.sh

BACKUP_DIR="/backup/orthanc/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Get all study IDs
curl -u orthanc:${ORTHANC_PASSWORD} \
  http://orthanc:8042/studies | jq -r '.[]' > studies.txt

# Download each study
while read study_id; do
  echo "Backing up study: $study_id"
  mkdir -p "$BACKUP_DIR/$study_id"
  
  # Get all instances in study
  curl -u orthanc:${ORTHANC_PASSWORD} \
    "http://orthanc:8042/studies/$study_id?expand" | \
    jq -r '.Series[].Instances[].ID' > instances.txt
  
  # Download instances
  while read instance_id; do
    curl -u orthanc:${ORTHANC_PASSWORD} \
      "http://orthanc:8042/instances/$instance_id/file" \
      -o "$BACKUP_DIR/$study_id/$instance_id.dcm"
  done < instances.txt
done < studies.txt

echo "Backup complete: $BACKUP_DIR"
```

## Notes

- Orthanc stores data in a SQLite database by default (not suitable for production)
- For production, use PostgreSQL or MySQL plugin
- The web UI is available at `http://orthanc:8042/app/explorer.html`
- Orthanc supports DICOM protocol on port 4242 by default
- Consider using the DICOMweb interface for modern integrations
- Enable HTTPS in production for secure communications
