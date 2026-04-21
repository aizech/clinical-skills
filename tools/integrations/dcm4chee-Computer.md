# DCM4CHEE Archive Integration

Enterprise-grade DICOM archive with HL7 integration.

## Connection

```yaml
host: dcm4chee.example.com
port: 8080
dicom_port: 11112
username: admin
password: ${DCM4CHEE_PASSWORD}
realm: Radiology
```

## Authentication

WS-Authentication (Dimse) or Basic Auth for REST API.

## Key Operations

### DICOM C-FIND (Query)
```bash
# Query worklist
findscu -xcr 192.168.1.100 11112 -cmove SCU \
  - PatientName="*" -Modality=CT -ScheduledDateTime=20240115
```

### DICOM C-MOVE (Retrieve)
```bash
# Retrieve to configured AE
movscu -xcr 192.168.1.100 11112 \
  -cget SCU - ProposedTransferContexts=1.2.840.10008.1.2.4.50
```

### REST API
- `GET /dcm4chee-arc/aets` - Application entities
- `GET /dcm4chee-arc/rs/mpps` - Performed procedures
- `POST /dcm4chee-arc/rs/mpps/{id}/n-create`

## HL7 Integration

```yaml
hl7_port: 2575
accept_mllp: true
forward_orders: true
```

## Tool Registration

```json
{
  "name": "dcm4chee_archive",
  "description": "Enterprise DICOM archive with full query/retrieve",
  "category": "pacs",
  "protocols": ["dicom", "hl7", "rest"]
}
```
