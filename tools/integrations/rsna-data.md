# RSNA Data Portal Integration

Access to RSNA AI challenge datasets.

## Connection

```yaml
base_url: https://data.rsna.ai
auth: RSNA credentials
```

## Authentication

RSNA username/password or API token:
```bash
curl -X POST https://api.rsna.ai/auth/token \
  -d "username={user}&password={pass}"
```

## Available Datasets

### RSNA Bone Age
- **Task**: Regression
- **Modality**: Hand X-ray
- **Annotations**: Bone age in months
- **Size**: ~12,600 images training, 2,000 test

### RSNA Pneumonia Detection
- **Task**: Detection
- **Modality**: Chest X-ray
- **Annotations**: Bounding boxes for pneumonia
- **Size**: ~30,000 images

### RSNA Intracranial Hemorrhage
- **Task**: Detection/Classification  
- **Modality**: CT Head
- **Annotations**: Hemorrhage type + bounding boxes
- **Size**: ~25,000 images

### RSNA Mammography (TB/multi-reader)
- **Task**: Classification
- **Modality**: Mammography
- **Annotations**: Biopsy-proven labels

## Key Operations

### Dataset Download
```bash
# List available datasets
GET /api/datasets

# Request access
POST /api/datasets/{id}/access

# Get download links
GET /api/datasets/{id}/downloads
```

### Challenge Participation
```bash
# Register for challenge
POST /api/challenges/{id}/register

# Submit predictions
POST /api/challenges/{id}/submissions
{
  "test_set_version": "1.0",
  "predictions_file": "s3://bucket/preds.csv"
}

# Get leaderboard
GET /api/challenges/{id}/leaderboard
```

## Data Format

Training labels provided as CSV with columns:
- `image_id`: Unique image identifier
- `annotation`: Label/bounding boxes
- `patient_id`: De-identified patient ID
- `study_id`: Study identifier

## Rate Limits

- API: 100 requests/hour
- Downloads: 10 concurrent

## Tool Registration

```json
{
  "name": "rsna_portal",
  "description": "RSNA AI challenge datasets and leaderboard access",
  "category": "dataset",
  "endpoints": ["dataset_list", "access_request", "download", "leaderboard"]
}
```
