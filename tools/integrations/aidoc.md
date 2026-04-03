# Aidoc AI Triage Integration

Real-time AI triage for critical findings.

## Connection

```yaml
api_base: https://api.aidoc.com/v1
client_id: ${AIDOC_CLIENT_ID}
client_secret: ${AIDOC_CLIENT_SECRET}
facility_id: ${AIDOC_FACILITY_ID}
```

## Authentication

OAuth 2.0 client credentials flow:
```bash
POST /oauth/token
{
  "grant_type": "client_credentials",
  "client_id": "...",
  "client_secret": "..."
}
```

## Key Endpoints

### Alert Webhooks
Configure webhooks for real-time alert delivery:
```json
{
  "event": "critical_findings.detected",
  "url": "https://your-system.com/webhooks/aidoc",
  "secret": "${AIDOC_WEBHOOK_SECRET}"
}
```

### REST API
```bash
# List pending alerts
GET /alerts?status=open&modality=CT

# Alert details
GET /alerts/{alert_id}

# Acknowledge alert
POST /alerts/{alert_id}/acknowledge
{
  "acknowledged_by": "dr.smith",
  "action": "reviewed"
}

# Mark alert resolved
POST /alerts/{alert_id}/resolve
{
  "confirmed": true,
  "finding_type": "pe_positive"
}
```

### Patient Context
```bash
# Get patient history
GET /patients/{patient_id}/imaging_history

# Get prior comparisons
GET /studies/{study_id}/priors
```

## Rate Limits

Webhook-based (no polling limits). REST API: 60 requests/minute.

## Supported Findings

- Pulmonary embolism (CTPA)
- Intracranial hemorrhage (CT Head)
- C-spine fractures
- Aortic dissection
- Large vessel occlusion

## Tool Registration

```json
{
  "name": "aidoc_triage",
  "description": "Real-time AI triage and critical finding alerts",
  "category": "ai_detection",
  "endpoints": ["alerts_list", "alerts_ack", "patient_context", "webhook_receive"]
}
```
