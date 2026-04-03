# Zebra Medical Vision Integration

AI.Ready health imaging analytics platform.

## Connection

```yaml
api_base: https://api.zebra-med.com/v2
api_key: ${ZEBRA_API_KEY}
client_id: ${ZEBRA_CLIENT_ID}
```

## Authentication

API key authentication:
```bash
X-API-Key: {api_key}
```

## Key Endpoints

### Study Analysis
```bash
# Submit for AI analysis
POST /studies/analyze
{
  "study_uid": "1.2.3.4.5",
  "modality": "CT",
  "body_part": "CHEST",
  "ai_packages": ["bone_covid", "lung_nodule"]
}

# Get analysis results
GET /studies/{study_id}/results
```

### Available AI Packages
- `bone_density` - Vertebral fracture detection, BMD
- `lung_nodule` - Pulmonary nodule detection
- `bone_covid` - COVID-19 pneumonia quantification
- `coronary_calcium` - Agatston score
- `liver_ai` - Liver fat quantification, segmentation
- `brain_bleed` - Intracranial hemorrhage

### Webhook Configuration
```bash
POST /webhooks
{
  "url": "https://your-system.com/webhooks/zebra",
  "events": ["analysis.complete", "finding.detected"],
  "secret": "${ZEBRA_WEBHOOK_SECRET}"
}
```

## Rate Limits

Standard: 100 studies/hour. Enterprise: Negotiated.

## Tool Registration

```json
{
  "name": "zebra_medical",
  "description": "AI imaging analytics across multiple body systems",
  "category": "ai_detection",
  "endpoints": ["study_analyze", "results_retrieve", "package_list", "webhook_config"]
}
```
