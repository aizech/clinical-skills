# Qure.ai Integration

Chest X-ray and CT AI analysis for resource-limited settings.

## Connection

```yaml
api_base: https://api.qure.ai/v1
api_key: ${QURE_API_KEY}
organization_id: ${QURE_ORG_ID}
```

## Authentication

API key authentication:
```bash
X-API-Key: {api_key}
```

## Key Endpoints

### Chest X-ray Analysis (qXR)
```bash
# Submit CXR for AI analysis
POST /cxr/analyze
{
  "study_uid": "...",
  "image_url": "https://pacs.example.com/dcm.dcm",
  "priority": "normal"
}

# Get analysis results
GET /cxr/results/{analysis_id}
```

### Tuberculosis Screening
```bash
POST /cxr/tb-screening
{
  "image_path": "/path/to/image.dcm",
  "population": "screening"  # or "clinical"
}
```

### CT Analysis (qCT)
```bash
POST /ct/lung-nodule
{
  "series_uid": "...",
  "analysis_type": "nodule_detection"
}

GET /ct/results/{analysis_id}
```

## Response Format

```json
{
  "study_id": "...",
  "findings": [
    {
      "type": "nodule",
      "location": "right upper lobe",
      "diameter_mm": 8.5,
      "volume_mm3": 320,
      "risk_level": "moderate"
    }
  ],
  "priority_alert": false,
  "report_text": "AI-generated draft impression..."
}
```

## Available Modules

| Module | Description | Modality |
|--------|-------------|----------|
| qXR | Chest X-ray triage | X-ray |
| qXR-TB | Tuberculosis screening | X-ray |
| qCT-Lung | Lung nodule detection | CT |
| qXR-Covid | COVID-19 detection | X-ray |

## Rate Limits

Standard: 100 requests/minute. Enterprise: Custom limits.

## Tool Registration

```json
{
  "name": "qure_ai",
  "description": "Qure.ai chest X-ray and CT AI analysis",
  "category": "ai_detection",
  "endpoints": ["cxr_analyze", "tb_screening", "ct_analysis", "results"]
}
```
