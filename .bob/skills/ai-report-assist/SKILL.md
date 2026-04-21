---
name: ai-report-assist
description: Guidance for AI-assisted structured reporting tools. Also use when the user mentions AI reporting, automated templating, speech-to-report, or wants to configure or optimize AI-assisted radiology reporting systems (RadAI, Abba, DeepRad).
---

# AI Report Assistance

You are an expert in AI-assisted radiology reporting. Your role is to help users configure, integrate, and optimize AI reporting tools.

## Supported Platforms

| Platform | Focus | Modality |
|----------|-------|----------|
| RadAI | Structured reporting automation | CT, X-ray |
| Abba | Speech recognition + structured reporting | CT, MRI |
| DeepRad | Multi-modality structured reporting | CT, MRI, X-ray |
| DeepScribe | Ambient AI documentation | All |
| ScribeAnywhere | Voice-powered reporting | All |

## Key Concepts

### AI Reporting Workflow

```
Image → AI Analysis → Finding Detection → Template Population → Radiologist Review → Signed Report
```

### Structured Reporting Benefits

- Consistent terminology
- Complete documentation
- Data extraction for analytics
- Quality metrics
- Research queries

## RadAI Integration

### API Configuration

```python
import requests

RADAI_API = "https://api.radai.ai/v1"

def configure_radai(api_key, modality="ct"):
    """Configure RadAI API connection."""
    return {
        "base_url": RADAI_API,
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        "default_modality": modality
    }

def submit_study_for_ai_report(config, study_uid, modality="ct"):
    """Submit study for AI-assisted reporting."""
    response = requests.post(
        f"{config['base_url']}/studies",
        headers=config["headers"],
        json={
            "study_uid": study_uid,
            "modality": modality,
            "report_type": "structured"
        }
    )
    return response.json()
```

### Template Configuration

```python
def configure_template(config, template_type="default"):
    """Configure reporting template."""
    templates = {
        "ct_chest": {
            "sections": ["lungs", "mediastinum", "pleura", "bones", "impression"],
            "required_fields": ["lungs.findings", "impression"],
            "measurement_fields": ["size", "attenuation", "volume"]
        },
        "ct_abdomen": {
            "sections": ["liver", "gallbladder", "pancreas", "spleen", "kidneys", "bowel", "impression"]
        },
        "ct_head": {
            "sections": ["brain", "ventricles", "basal_ganglia", "vessels", "bones", "impression"]
        }
    }
    return templates.get(template_type, templates["ct_chest"])
```

### Retrieve AI Suggestions

```python
def get_ai_suggestions(config, study_id):
    """Get AI-generated report suggestions."""
    response = requests.get(
        f"{config['base_url']}/studies/{study_id}/suggestions",
        headers=config["headers"]
    )
    return response.json()

# Response structure
{
    "study_id": "123",
    "findings": [
        {
            "anatomy": "right_upper_lobe",
            "finding": "nodule",
            "size_mm": 12,
            "location_detail": "RUL",
            "characteristics": {
                "margins": "spiculated",
                "attenuation": "solid"
            }
        }
    ],
    "impression_suggestion": "12mm spiculated nodule in right upper lobe, suspicious for malignancy.",
    "confidence": 0.89
}
```

## Abba Integration

### Speech Recognition Setup

```python
def configure_abba(api_key, specialty="radiology"):
    """Configure Abba speech recognition."""
    return {
        "base_url": "https://api.abba.ai",
        "headers": {
            "Authorization": f"Bearer {api_key}"
        },
        "specialty": specialty,
        "format": "structured"
    }

def transcribe_dictation(config, audio_file):
    """Transcribe dictation with structured output."""
    with open(audio_file, "rb") as f:
        files = {"audio": f}
        response = requests.post(
            f"{config['base_url']}/transcribe",
            headers=config["headers"],
            files=files,
            data={"specialty": config["specialty"]}
        )
    return response.json()
```

## DeepRad Integration

### Multi-Modality Configuration

```python
def configure_deeprad(api_key):
    """Configure DeepRad for multi-modality."""
    return {
        "base_url": "https://api.deeprad.ai",
        "api_key": api_key,
        "modalities": ["ct", "mri", "xray", "pet"]
    }

def get_structured_report(config, study_data, modality):
    """Get structured report for any modality."""
    response = requests.post(
        f"{config['base_url']}/report/{modality}",
        headers={"Authorization": f"Bearer {config['api_key']}"},
        json=study_data
    )
    return response.json()
```

## Template Types

### By Modality

| Modality | Template Type | Key Elements |
|----------|--------------|--------------|
| CT Chest | Lung-RADS | Nodule tracking, comparison |
| CT Abdomen | LI-RADS | Liver lesion assessment |
| CT Head | No specific | Hemorrhage, stroke |
| MRI Prostate | PI-RADS | PI-RADS scoring |
| MRI Liver | LI-RADS | LI-RADS scoring |
| Mammography | BI-RADS | Assessment categories |
| X-ray Chest | No specific | Critical findings |

### Template Structure

```python
STANDARD_TEMPLATE = {
    "header": {
        "patient_id": "required",
        "study_date": "required",
        "accession": "required",
        "modality": "required",
        "clinical_history": "required"
    },
    "findings": {
        "anatomy": "free_text",
        "finding": "structured",
        "size": "measurement",
        "location": "structured",
        "characteristics": "structured"
    },
    "impression": {
        "primary": "required",
        "secondary": "optional",
        "recommendations": "optional"
    }
}
```

## Integration with PACS

### Workflow Integration

```python
def setup_pacs_integration(pacs_url, ai_platform="radai"):
    """Set up PACS integration for AI reporting."""
    integration = {
        "pacs": {
            "url": pacs_url,
            "auto_submit": True,
            "receive_results": True
        },
        "ai_platform": ai_platform,
        "workflow": {
            "auto_populate": True,
            "require_review": True,
            "sign_immediately": False
        }
    }
    return integration
```

### Auto-Populate Configuration

```python
def configure_auto_populate(settings):
    """Configure auto-population behavior."""
    return {
        "populate_findings": settings.get("findings", True),
        "populate_impression": settings.get("impression", True),
        "populate_measurements": settings.get("measurements", True),
        "highlight_changes": settings.get("highlight_changes", True),
        "require_acknowledgment": settings.get("require_ack", True)
    }
```

## Optimization Strategies

### High Volume Practice

```python
HIGH_VOLUME_CONFIG = {
    "auto_accept_normal": True,  # Accept normal AI reports
    "auto_populate": True,
    "require_review_abnormal": True,
    "batch_processing": True,
    "templates": "standardized"
}
```

### Quality Focus

```python
QUALITY_FOCUSED_CONFIG = {
    "auto_accept_normal": False,
    "auto_populate": True,
    "require_review_all": True,
    "double_read_option": True,
    "templates": "comprehensive"
}
```

## Best Practices

1. **Start with standardized templates** - Ensure consistency
2. **Enable auto-population gradually** - Train radiologists on workflow
3. **Monitor accuracy** - Track AI vs final report differences
4. **Customize templates** - Adapt to your practice patterns
5. **Regular review** - QA AI suggestions periodically

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI not submitting | Check PACS integration |
| Slow responses | Enable caching |
| Incorrect findings | Retrain with local data |
| Template mismatch | Update template mapping |

## Related Skills

- **structured-reporting**: For report template details
- **pacs-workflow**: For PACS integration
- **ai-quality-review**: For AI output QA
- **radiology-report-analysis**: For report analysis

## Examples

### Example 1: Enable AI Reporting

```
Enable AI-assisted reporting for CT chest studies using RadAI
```

Configuration:
```python
config = configure_radai(api_key="your-key", modality="ct")
template = configure_template(config, "ct_chest")
```

### Example 2: Review AI Suggestions

```
Review AI suggestions for study ACC123
```

```python
suggestions = get_ai_suggestions(config, "ACC123")
# Present to radiologist for review
# Accept or modify suggestions
```
