# Google Health AI Integration

Medical imaging AI via Google Cloud Healthcare API.

## Connection

```yaml
project_id: ${GCP_PROJECT_ID}
location: us-central1
dataset_id: ${GCP_DATASET_ID}
credentials: ${GCP_SERVICE_ACCOUNT_KEY}
```

## Authentication

```bash
# Via gcloud
gcloud auth activate-service-account --key-file=key.json

# Or set environment
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

## Healthcare API Endpoints

### DICOMweb Operations
```bash
# Store instance
POST https://healthcare.googleapis.com/v1/projects/{project}/locations/{location}/datasets/{dataset}/dicomStores/{store}/dicomWeb/studies

# QIDO-RS search
GET https://healthcare.googleapis.com/v1/.../dicomWeb/studies?PatientName=SMITH

# WADO-RS retrieve
GET https://healthcare.googleapis.com/v1/.../dicomWeb/studies/{uid}/metadata
```

### FHIR Resources
```bash
# Patient lookup
GET /fhir/Patient?identifier={mrn}

# ImagingStudy
GET /fhir/ImagingStudy?patient={patient_id}
```

## Vertex AI Integration

### Medical Imaging API
```bash
# Submit for AI analysis
curl -X POST \
  "https://vision.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/cxr_interpretation:predict" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d @request.json
```

## BigQuery Analytics
```bash
# Query imaging metrics
bq query --use_legacy_sql=false \
  "SELECT modality, COUNT(*) as count 
   FROM `{project}.radiology.studies` 
   GROUP BY modality"
```

## Rate Limits

- Healthcare API: 1000 requests/minute
- Vertex AI: Varies by model tier

## Tool Registration

```json
{
  "name": "google_health",
  "description": "Google Cloud Healthcare API and Vertex AI medical imaging",
  "category": "ai_platform",
  "endpoints": ["dicomweb", "fhir", "vertex_inference", "bigquery"]
}
```
