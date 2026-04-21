# MaxQ AI Integration

Neuro and pulmonary AI detection for critical care imaging.

## Connection

```yaml
api_base: https://api.maxq.ai/v1
client_id: ${MAXQ_CLIENT_ID}
client_secret: ${MAXQ_CLIENT_SECRET}
facility_id: ${MAXQ_FACILITY_ID}
```

## Authentication

OAuth 2.0 client credentials:
```bash
POST /oauth/token
{
  "grant_type": "client_credentials",
  "client_id": "{client_id}",
  "client_secret": "{client_secret}"
}
```

## Key Endpoints

### Accipio AI Suite

#### Intracranial Hemorrhage
```bash
# Submit CT head for analysis
POST /v1/analysis/hemorrhage
{
  "study_uid": "1.2.3.4.5",
  "series_uid": "1.2.3.4.6",
  "priority": "stat"
}

# Get results
GET /v1/results/{analysis_id}
```

#### Pulmonary Embolism
```bash
POST /v1/analysis/pe
{
  "study_uid": "...",
  "modality": "CTPA"
}
```

### Notifications
```bash
# Configure webhooks
POST /v1/webhooks
{
  "event": "finding.detected",
  "url": "https://your-system.com/webhooks/maxq",
  "secret": "{webhook_secret}"
}
```

## Supported Findings

| Finding | Modality | FDA Cleared |
|---------|----------|:-----------:|
| Intracranial Hemorrhage | CT Head | ✓ |
| Pulmonary Embolism | CTPA | ✓ |
| Incidental Pulmonary Nodules | Chest CT | ✓ |
| Cervical Spine Fractures | CT C-spine | ✓ |

## Rate Limits

Webhook-based for alerts. API polling: 60 requests/minute.

## Tool Registration

```json
{
  "name": "maxq_ai",
  "description": "MaxQ AI Accipio for hemorrhage, PE, and spine detection",
  "category": "ai_detection",
  "endpoints": ["hemorrhage_analysis", "pe_analysis", "webhook_alerts", "results"]
}
```
