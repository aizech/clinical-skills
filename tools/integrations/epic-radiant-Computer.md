# Epic Radiant Integration

Epic's radiology information system with full EMR integration.

## Connection

```yaml
host: radiant.epic.com
port: 443
tenant_id: ${EPIC_TENANT_ID}
client_id: ${EPIC_CLIENT_ID}
client_secret: ${EPIC_CLIENT_SECRET}
```

## Authentication

OAuth 2.0 SMART Backend Services:
```bash
# Get access token
POST https://radiant.epic.com/oauth2/token
{
  "grant_type": "client_credentials",
  "client_id": "{client_id}",
  "client_secret": "{client_secret}",
  "scope": "system/Patient.read system/Observation.read"
}
```

## Key Endpoints

### Patient Lookup
```bash
GET /fhir/r4/Patient?identifier={mrn}
Authorization: Bearer {token}
```

### Imaging Studies
```bash
GET /fhir/r4/ImagingStudy?patient={patient_id}
GET /fhir/r4/ImagingStudy?subject={patient_id}&modality=CT
```

### Diagnostic Reports
```bash
GET /fadiology/fhir/r4/DiagnosticReport?patient={id}&category=RAD
POST /fadiology/fhir/r4/DiagnosticReport
```

### Order Management
```bash
# Create imaging order
POST /fadiology/fhir/r4/ServiceRequest
{
  "resourceType": "ServiceRequest",
  "subject": {"reference": "Patient/{id}"},
  "code": {"coding": [{"system": "http://loinc.org", "code": "24627-5"}]},
  "orderDetail": [{"code": {"text": "CT Chest with contrast"}}
}
```

## Radiant-Specific Features

### Worklist Access
```bash
GET /fadiology/radiant/v1/worklists
GET /fadiology/radiant/v1/worklists/{id}/cases
```

### Critical Results
```bash
# Send critical result
POST /fadiology/radiant/v1/results/{report_id}/critical
{
  "finding": "Critical finding description",
  "communicationMethod": "verbal",
  "recipientName": "Dr. Smith",
  "communicationTime": "2024-01-15T10:30:00Z"
}
```

## Rate Limits

Varies by Epic tenant. Contact Epic for limits.

## Tool Registration

```json
{
  "name": "epic_radiant",
  "description": "Epic Radiant RIS with full EMR integration",
  "category": "ehr",
  "endpoints": ["patient_lookup", "imaging_studies", "reports", "orders", "worklist"]
}
```
