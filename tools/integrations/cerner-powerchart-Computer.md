# Cerner PowerChart Integration

Oracle Health (formerly Cerner) radiology information system.

## Connection

```yaml
base_url: https://powerchart.cerner.com
millennium_url: https://millennium.cerner.com
client_id: ${CERNER_CLIENT_ID}
client_secret: ${CERNER_CLIENT_SECRET}
```

## Authentication

OAuth 2.0 with SMART on FHIR:
```bash
# Authorization request
GET {base_url}/oauth2/authorize?
  response_type=code&
  client_id={client_id}&
  redirect_uri={uri}&
  scope=system/Patient.read system/Observation.read&
  state=...

# Token exchange
POST {base_url}/oauth2/token
{
  "grant_type": "authorization_code",
  "code": "{auth_code}",
  "redirect_uri": "{uri}",
  "client_id": "{client_id}",
  "client_secret": "{client_secret}"
}
```

## Key Endpoints

### FHIR R4 Resources
```bash
# Patient
GET /fhir/r4/Patient?identifier={mrn}

# ImagingStudy
GET /fhir/r4/ImagingStudy?patient={patient_id}

# DiagnosticReport
GET /fhir/r4/DiagnosticReport?patient={patient_id}&category=RAD
```

### Millennium Objects (Proprietary)
```bash
# Get RadOrder
GET / Millennium/cdr/1/RadOrder?patientId={mrn}

# Get RadResult
GET / Millennium/cdr/1/RadResult?orderId={order_id}

# PowerNote creation
POST / Millennium/powernotes
{
  "author": "Dr. {name}",
  "template": "CT_Abdomen_Report",
  "content": "..."
}
```

## RIS Operations

### Worklist
```bash
GET /fadiology/r4/Task?owner={location}&status=ready
```

### Report Signing
```bash
POST /fadiology/r4/DiagnosticReport/{id}
{
  "status": "final",
  "conclusion": "Normal study"
}
```

## Rate Limits

Varies by Cerner/Oracle Health deployment.

## Tool Registration

```json
{
  "name": "cerner_powerchart",
  "description": "Oracle Health (Cerner) PowerChart RIS integration",
  "category": "ehr",
  "endpoints": ["fhir_r4", "millennium", "worklist", "reporting"]
}
```
