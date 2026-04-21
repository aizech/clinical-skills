# Radiology Context Reference

## Radiology Context in Practice

### Common Configuration Scenarios

#### Academic Medical Center
```json
{
  "pacs": {
    "type": "dcm4chee",
    "url": "https://pacs.university-hospital.edu/dcm4chee-arc",
    "ae_title": "UNIVHOSP_PACS",
    "auth": { "type": "basic" }
  },
  "ehr": {
    "type": "epic",
    "url": "https://fhir.epic.com/interconnect-fhir-oauth"
  },
  "modalities": ["CT", "MRI", "X-ray", "US", "NM", "MG", "XA", "RF"],
  "ai_tools": {
    "enabled": ["aidoc", "maxq"],
    "config": {}
  },
  "workflow": {
    "default_search_days": 90,
    "report_template": "structured"
  }
}
```

#### Community Hospital
```json
{
  "pacs": {
    "type": "orthanc",
    "url": "http://pacs.hospital.local:8042",
    "auth": { "type": "basic", "username": "admin" }
  },
  "ehr": {
    "type": "allscripts",
    "url": "https://allscripts.hospital.local"
  },
  "modalities": ["CT", "MRI", "X-ray", "US", "Mammography"],
  "ai_tools": { "enabled": [] },
  "workflow": {
    "default_search_days": 30,
    "report_template": "hybrid"
  }
}
```

#### Private Radiology Practice
```json
{
  "pacs": {
    "type": "orthanc",
    "url": "https://pacs.radpractice.com",
    "auth": { "type": "api_key", "api_key": "env:PACS_API_KEY" }
  },
  "modalities": ["CT", "MRI", "X-ray", "US", "Mammography", "DEXA"],
  "ai_tools": {
    "enabled": ["radai", "qure"],
    "config": {}
  },
  "workflow": {
    "default_search_days": 60,
    "report_template": "structured"
  }
}
```

#### Research Institution
```json
{
  "pacs": {
    "type": "orthanc",
    "url": "http://research-pacs.lab.edu:8042",
    "auth": { "type": "basic" }
  },
  "modalities": ["CT", "MRI", "X-ray", "US", "PET"],
  "ai_tools": {
    "enabled": ["clara", "medpalm"],
    "config": {}
  },
  "workflow": {
    "default_search_days": 365,
    "report_template": "research"
  },
  "preferences": {
    "data_format": "dicom_anon",
    "storage_path": "/data/research_imaging"
  }
}
```

## PACS Configuration Details

### Orthanc
```json
{
  "type": "orthanc",
  "url": "http://localhost:8042",
  "endpoints": {
    "dicom": "/dicom-web",
    "patients": "/patients",
    "studies": "/studies",
    "series": "/series"
  }
}
```

### DCM4CHEE
```json
{
  "type": "dcm4chee",
  "url": "http://localhost:8080/dcm4chee-arc/aets/YOUR_AET",
  "ae_title": "YOUR_AET",
  "endpoints": {
    "qido": "/rs",
    "wado": "/wado",
    "stow": "/rs"
  }
}
```

### OHIF Viewer
```json
{
  "type": "ohif",
  "url": "https://viewer.ohif.org",
  "dataSource": "dicomweb",
  "config": {
    "servers": {
      "dicomWeb": ["https://pacs.example.com/dicomweb"]
    }
  }
}
```

## AI Tool API References

### Aidoc
- API Endpoint: `https://api.aidoc.com/v1`
- Auth: API Key in header
- Env: `AIDOC_API_KEY`
- Docs: https://docs.aidoc.com

### RadAI
- API Endpoint: `https://api.radai.ai/v1`
- Auth: OAuth 2.0
- Env: `RADAI_CLIENT_ID`, `RADAI_CLIENT_SECRET`
- Docs: https://developers.radai.ai

### Nvidia Clara
- API Endpoint: `https://api.clara.nvidia.com/v1`
- Auth: API Key
- Env: `CLARA_API_KEY`
- Docs: https://docs.nvidia.com/clara

### MedPaLM
- API Endpoint: `https://api.google.com/v1beta1/medpalm`
- Auth: API Key (Google Cloud)
- Env: `GOOGLE_CLOUD_API_KEY`
- Docs: https://developers.google.com/malaria

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| PACS unreachable | Wrong URL, firewall | Verify URL, check network |
| Auth failed | Wrong credentials | Re-enter, check env vars |
| No results | Wrong AE title | Check AE title config |
| Slow queries | Large dataset | Add date filters |

### Validation Commands

```bash
# Test Orthanc connection
curl http://localhost:8042/system

# Test DICOMweb
curl "http://localhost:8042/dicom-web/servers"

# Test authentication
curl -u user:pass http://localhost:8042/patients
```

## Environment Variables Template

Create `.env.example`:

```bash
# PACS
ORTHANC_PASSWORD=your_password
PACS_API_KEY=your_api_key

# AI Tools
AIDOC_API_KEY=your_key
RADAI_CLIENT_ID=your_id
RADAI_CLIENT_SECRET=your_secret
CLARA_API_KEY=your_key
ZEBRA_API_KEY=your_key
MAXQ_API_KEY=your_key
QURE_API_KEY=your_key

# EHR
EPIC_CLIENT_ID=your_client_id
EPIC_CLIENT_SECRET=your_secret

# LLMs
GOOGLE_CLOUD_API_KEY=your_key
AZURE_OPENAI_KEY=your_key
AWS_ACCESS_KEY=your_key
AWS_SECRET_KEY=your_key

# Webhooks
WEBHOOK_URL=https://hooks.example.com/radiology
```
