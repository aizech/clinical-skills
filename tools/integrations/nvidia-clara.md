# NVIDIA Clara AI Integration

GPU-accelerated medical imaging AI platform.

## Connection

```yaml
clara_base_url: https://clara.monitor.example.com/api/v1
api_key: ${CLARA_API_KEY}
model_registry: clara-models.example.com
```

## Authentication

API key in header: `Nvidia-Clara-Api-Key: {api_key}`

## Key Endpoints

### AI Model Inference
```bash
# Submit inference job
POST /inference/jobs
{
  "model_name": "clara_pt_covid_ct_1",
  "input_series": ["1.2.3.4.5.6.7"],
  "priority": "normal"
}

# Job status
GET /inference/jobs/{job_id}

# Get results
GET /inference/jobs/{job_id}/results
```

### Model Management
```bash
# List available models
GET /models

# Model metadata
GET /models/{model_id}

# Model performance metrics
GET /models/{model_id}/metrics
```

### Data Pipeline
```bash
# Register data for processing
POST /data/register
{
  "dicom_series_uid": "...",
  "modality": "CT",
  "annotations": [...]
}

# Get processing status
GET /data/{data_id}/status
```

## Available Models

- Clara PT COVID-19 CT (lung segmentation)
- Clara AIAA (brain aneurysm)
- Clara Mondo (organ segmentation)
- Clara Deploy (custom deployment)

## Rate Limits

Varies by tier. Contact NVIDIA for enterprise limits.

## Tool Registration

```json
{
  "name": "nvidia_clara",
  "description": "GPU-accelerated AI inference and model deployment",
  "category": "ai_platform",
  "endpoints": ["inference_submit", "results_retrieve", "model_list", "metrics"]
}
```
