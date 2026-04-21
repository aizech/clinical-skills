---
name: radiology-context
description: Establish and manage user's clinical radiology environment configuration - PACS, EHR, modality types, AI tools, and workflow settings. Also use when setting up or updating radiology workflow context, configuring PACS connections, or managing clinical environment settings.
---

# Radiology Context Management

You are a radiology workflow configuration expert. Your role is to help users establish and manage their clinical radiology environment settings.

## Purpose

Radiology context stores the user's:
- PACS configuration
- EHR integration settings
- Modality types used
- AI tool configurations
- Workflow preferences

This context is used by all other radiology skills to provide personalized, environment-specific assistance.

## Context File Location

Default: `.agents/radiology-context.json`

Alternative locations checked in order:
1. `.agents/radiology-context.json`
2. `.claude/radiology-context.json`
3. `./radiology-context.json`

## Context Schema

```json
{
  "version": "1.0",
  "pacs": {
    "type": "orthanc|dcm4chee| Conquest| OHIF |custom",
    "url": "https://pacs.example.com",
    "port": 8042,
    "auth": {
      "type": "none|basic|api_key|oauth2",
      "username": "optional",
      "api_key": "optional or env var reference"
    },
    "ae_title": "YOUR_AE",
    "default_study_uid": null
  },
  "ehr": {
    "type": "epic|cerner|allscripts|mirth|custom",
    "url": "https://ehr.example.com",
    "auth": {
      "type": "oauth2|saml|api_key",
      "client_id": "optional"
    }
  },
  "modalities": ["CT", "MRI", "X-ray", "Ultrasound"],
  "ai_tools": {
    "enabled": ["aidoc", "radai", "clara"],
    "config": {
      "aidoc": { "api_key": "env:AIDOC_API_KEY" },
      "radai": { "api_key": "env:RADAI_API_KEY" }
    }
  },
  "workflow": {
    "default_search_days": 30,
    "report_template": "default",
    "notification_email": "radiology@example.com"
  },
  "preferences": {
    "timezone": "America/New_York",
    "date_format": "YYYY-MM-DD",
    "units": "metric"
  }
}
```

## Commands

### Initialize Context

Create a new radiology context:

```
Initialize radiology context with:
- PACS: [type] at [url]
- Modalities: [list]
- EHR: [type] (optional)
```

**Prompt sequence:**
1. Ask for PACS type and URL
2. Ask for authentication method
3. Ask for modalities used
4. Ask for EHR type (optional)
5. Ask for AI tools (optional)
6. Create context file

### Update Context

Modify existing context:

```
Update radiology context:
- PACS: [new values]
- Add modality: [modality]
```

**Supported updates:**
- `set pacs <type> <url>`
- `add modality <modality>`
- `remove modality <modality>`
- `set ehr <type> <url>`
- `add ai <ai_tool>`
- `update workflow <setting> <value>`

### Display Context

Show current context:

```
Show my radiology context
```

Returns formatted, redacted context (no secrets displayed).

### Validate Context

Check context validity:

```
Validate my radiology context
```

Checks:
- Required fields present
- URLs reachable
- Auth credentials valid
- Modalities valid
- AI tools accessible

### Clear Context

Reset context to empty:

```
Clear radiology context
```

Removes all context. User must re-initialize.

## PACS Types

| Type | Description | Default Port |
|------|-------------|--------------|
| orthanc | Open source DICOM server | 8042 |
| dcm4chee | Enterprise Java PACS | 8080 |
| Conquest | Windows DICOM server | 5678 |
| OHIF | OHIF Viewer backend | 3000 |
| dicomweb | Generic DICOMweb | 80/443 |
| custom | User-defined | varies |

### PACS Configuration Examples

**Orthanc:**
```json
{
  "type": "orthanc",
  "url": "http://localhost:8042",
  "auth": { "type": "basic", "username": "orthanc", "password": "env:ORTHANC_PASSWORD" }
}
```

**DCM4CHEE:**
```json
{
  "type": "dcm4chee",
  "url": "http://192.168.1.100:8080/dcm4chee-arc/aets",
  "ae_title": "DCM4CHEE",
  "auth": { "type": "basic" }
}
```

**DICOMweb:**
```json
{
  "type": "dicomweb",
  "url": "https://pacs.example.com/dicomweb",
  "auth": { "type": "oauth2", "client_id": "env:DICOMWEB_CLIENT_ID" }
}
```

## Authentication Types

| Type | Config Fields | Use Case |
|------|---------------|----------|
| none | - | Local/internal PACS |
| basic | username, password | Basic auth |
| api_key | api_key | Token-based auth |
| oauth2 | client_id, client_secret | Enterprise systems |

**Security best practices:**
- Store secrets in environment variables: `"api_key": "env:VAR_NAME"`
- Never commit secrets to files
- Use `.env` file for local development

## Modality Configuration

List supported modalities:

```json
{
  "modalities": [
    "CT", "MRI", "X-ray", "CR", "DX",
    "Ultrasound", "US", "Mammography", "MG",
    "Nuclear", "NM", "PET", "PT",
    "Fluoroscopy", "RF", "Angiography", "XA"
  ]
}
```

Add specific scanner types:
```json
{
  "modalities": [
    { "type": "CT", "scanner": "Siemens SOMATOM" },
    { "type": "MRI", "scanner": "GE SIGNA Premier 3T" }
  ]
}
```

## AI Tool Configuration

Supported AI platforms:

| Platform | Skill Reference | API Env Var |
|----------|----------------|-------------|
| Aidoc | ai-detection-pipeline | AIDOC_API_KEY |
| RadAI | ai-report-assist | RADAI_API_KEY |
| Nvidia Clara | ai-detection-pipeline | CLARA_API_KEY |
| Zebra Medical | ai-detection-pipeline | ZEBRA_API_KEY |
| MaxQ AI | ai-detection-pipeline | MAXQ_API_KEY |
| Qure AI | ai-detection-pipeline | QURE_API_KEY |
| MedPaLM | llm-radiology-use | MEDPALM_API_KEY |
| HealthLake | llm-radiology-use | HEALTHLAKE_KEY |

```json
{
  "ai_tools": {
    "enabled": ["aidoc", "radai"],
    "config": {
      "aidoc": {
        "endpoint": "https://api.aidoc.com",
        "api_key": "env:AIDOC_API_KEY"
      },
      "radai": {
        "endpoint": "https://api.radai.ai",
        "api_key": "env:RADAI_API_KEY"
      }
    }
  }
}
```

## EHR Integration

| EHR | HL7/FHIR | Notes |
|-----|----------|-------|
| Epic | FHIR R4 | Radiant module |
| Cerner | FHIR R4 | PowerChart |
| Allscripts | HL7 v2 | Professional EHR |
| Meditech | HL7 v2 | Exported PACS |

```json
{
  "ehr": {
    "type": "epic",
    "url": "https://fhir.epic.com/interconnect-fhir-oauth",
    "auth": {
      "type": "oauth2",
      "client_id": "env:EPIC_CLIENT_ID"
    }
  }
}
```

## Workflow Settings

```json
{
  "workflow": {
    "default_search_days": 30,
    "max_results": 100,
    "report_template": "structured",
    "auto_populate_patient": true,
    "notification_webhook": "env:WEBHOOK_URL"
  }
}
```

## Error Handling

| Error | Response |
|-------|----------|
| Missing context | Prompt to initialize |
| Invalid URL | Ask for correction |
| Auth failed | Prompt for credentials |
| PACS unreachable | Check network, suggest troubleshooting |

## Example Interactions

### Example 1: First-time Setup

**User**: Set up my radiology context
**Agent**: I'll help you set up your radiology environment. Let's start:

1. **PACS Type**: What PACS system do you use? (orthanc, dcm4chee, epic-radiant, custom)

2. **PACS URL**: What's the base URL for your PACS?

3. **Authentication**: How do you authenticate? (none, basic, API key)

4. **Modalities**: What imaging modalities do you work with?

5. **EHR**: Do you use an EHR system? (optional)

6. **AI Tools**: Any AI detection/reporting tools? (optional)

**User**: I use Orthanc at localhost:8042 with no auth, CT and MRI, no EHR, no AI
**Agent**: ✓ Context created at `.agents/radiology-context.json`

### Example 2: Query with Context

**User**: Find recent CT head studies
**Agent**: Using your configured Orthanc PACS...

```
✓ Query: CT Head
✓ Date: Last 30 days
✓ Results: 12 studies
```

### Example 3: Update Context

**User**: Add dcm4chee as my PACS
**Agent**: I'll update your PACS configuration.

**Current**: Orthanc at localhost:8042
**New**: DCM4CHEE at [Enter URL]

Please provide the DCM4CHEE URL:
**User**: http://192.168.1.100:8080/dcm4chee
**Agent**: ✓ PACS updated. Would you like me to validate the connection?

## Related Skills

- **pacs-workflow**: For PACS-specific queries
- **dicom-web-query**: For DICOMweb operations
- **hl7-fhir-radiology**: For EHR integration
- **ai-detection-pipeline**: For AI tool configuration
- **llm-radiology-use**: For LLM configuration

## Tips

1. **Start simple**: Begin with basic PACS config, add complexity as needed
2. **Use environment variables**: Never hardcode secrets
3. **Validate regularly**: Run `validate context` to check settings
4. **Document changes**: Note why you changed settings
5. **Test connections**: Verify PACS/EHR after configuration
