# RadAI Reporting Integration

AI-assisted radiology reporting platform.

## Connection

```yaml
api_base: https://api.radai.ai/v1
api_key: ${RADAI_API_KEY}
organization_id: ${RADAI_ORG_ID}
```

## Authentication

Bearer token: `Authorization: Bearer {api_key}`

## Key Endpoints

### Study Management
```bash
# Submit study for AI assist
POST /studies
{
  "study_uid": "1.2.3.4.5",
  "modality": "CT",
  "body_part": "CHEST",
  "accession_number": "ACC123"
}

# Get AI findings
GET /studies/{study_id}/findings
```

### Report Integration
```bash
# Submit finalized report
POST /studies/{study_id}/reports
{
  "report_text": "...",
  "radiologist_id": "...",
  "signed_at": "2024-01-15T10:30:00Z"
}

# Get report quality score
GET /studies/{study_id}/quality
```

### Analytics
```bash
# Get department metrics
GET /analytics/department
{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "group_by": "radiologist"
}
```

## Rate Limits

Standard: 100 requests/minute. Enterprise: Custom limits.

## Tool Registration

```json
{
  "name": "radai_reporting",
  "description": "AI-assisted radiology reporting and analytics",
  "category": "ai_reporting",
  "endpoints": ["study_submit", "findings_retrieve", "report_submit", "analytics"]
}
```
