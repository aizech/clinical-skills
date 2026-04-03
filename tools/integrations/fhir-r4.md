# HL7 FHIR R4 Integration

Healthcare interoperability via FHIR REST API.

## Connection

```yaml
fhir_base: https://fhir.example.com/r4
auth: OAuth 2.0 / SMART
patient_scope: patient/*.read
```

## Authentication

SMART on FHIR OAuth 2.0:
```bash
# Authorization request
GET /oauth2/authorize?
  response_type=code&
  client_id={client_id}&
  redirect_uri={uri}&
  scope=patient/Observation.read&
  state=abc123

# Token exchange
POST /oauth2/token
{
  "grant_type": "authorization_code",
  "code": "{auth_code}",
  "redirect_uri": "{uri}",
  "client_id": "{client_id}",
  "client_secret": "{secret}"
}
```

## Radiology Resources

### ImagingStudy
```bash
# Search studies
GET /ImagingStudy?patient={patient_id}&modality=CT

# Get study
GET /ImagingStudy/{id}

# Series in study
GET /ImagingStudy/{id}/series
```

### DiagnosticReport
```bash
# Patient reports
GET /DiagnosticReport?patient={patient_id}&category=RAD

# By date
GET /DiagnosticReport?date=ge2024-01-01&status=final

# Report content
GET /DiagnosticReport/{id}
```

### Observation
```bash
# Imaging measurements
GET /Observation?subject={patient_id}&category=laboratory

# Critical results
GET /Observation?subject={patient_id}&interpretation=critical
```

### Patient
```bash
# Search by MRN
GET /Patient?identifier={mrn}

# Demographics
GET /Patient/{id}
```

## Bundle Operations
```bash
# Transaction
POST /
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "resource": {...},
      "request": {"method": "POST", "url": "DiagnosticReport"}
    }
  ]
}
```

## Error Handling

```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "invalid",
    "diagnostics": "Patient identifier format invalid"
  }]
}
```

## Rate Limits

Varies by FHIR server. Typically 1000/minute per client.

## Tool Registration

```json
{
  "name": "fhir_r4",
  "description": "FHIR R4 radiology resources (ImagingStudy, DiagnosticReport)",
  "category": "interoperability",
  "resources": ["ImagingStudy", "DiagnosticReport", "Patient", "Observation"]
}
```
