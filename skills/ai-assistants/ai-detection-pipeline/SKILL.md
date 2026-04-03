---
name: ai-detection-pipeline
description: Integrate AI detection into PACS workflow. Also use when setting up, configuring, or optimizing AI detection systems for medical imaging. Also covers Aidoc, Nvidia Clara, Zebra Medical, MaxQ AI, and Qure AI integration.
---

# AI Detection Pipeline

You are an expert in AI medical imaging detection pipelines. Your role is to help users integrate, configure, and optimize AI detection systems.

## Supported AI Platforms

| Platform | Focus Areas | Modality |
|----------|-------------|----------|
| Aidoc | Triage, hemorrhage, PE, C-spine | CT |
| Nvidia Clara | Multi-modal, general detection | CT, MRI, X-ray |
| Zebra Medical | Multi-finding, chest | X-ray, CT |
| MaxQ AI | Neuro, PE, chest | CT |
| Qure AI | Chest, head | X-ray, CT |
| Lunit | Chest, mammography | X-ray, MG |
| Riverain | Chest, lung nodules | X-ray |

## Pipeline Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PACS       │────▶│  AI Engine │────▶│  Results    │────▶│  Worklist  │
│  (Source)   │     │  (Detect)  │     │  (Store)    │     │  (Alert)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
  DICOM Send         Inference          Database             Notification
  C-STORE           GPU Compute         Results Store        Pager/Email
```

## Aidoc Integration

### API Configuration

```python
import requests

AIDOC_API = "https://api.aidoc.com/v1"

def configure_aidoc(api_key):
    """Configure Aidoc API."""
    return {
        "base_url": AIDOC_API,
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    }

def submit_study_aidoc(config, study_uid, study_url):
    """Submit study for Aidoc analysis."""
    response = requests.post(
        f"{config['base_url']}/studies",
        headers=config["headers"],
        json={
            "study_uid": study_uid,
            "study_dicom_url": study_url,
            "priority": "normal"
        }
    )
    return response.json()
```

### Detection Types

```python
AIDOC_DETECTIONS = {
    "ct_head": [
        "intracranial_hemorrhage",
        "mass_effect",
        "midline_shift",
        "fracture"
    ],
    "ct_chest": [
        "pulmonary_embolism",
        "pneumothorax",
        "cervical_spine_fracture"
    ],
    "ct_angiography": [
        "aortic_dissection",
        "pulmonary_embolism"
    ]
}
```

### Retrieve Results

```python
def get_aidoc_results(config, study_id):
    """Get AI detection results."""
    response = requests.get(
        f"{config['base_url']}/studies/{study_id}/results",
        headers=config["headers"]
    )
    return response.json()

# Response structure
{
    "study_id": "123",
    "status": "complete",
    "findings": [
        {
            "type": "intracranial_hemorrhage",
            "location": "right_temporal",
            "severity": "critical",
            "confidence": 0.95,
            "bounding_box": {"x": 100, "y": 200, "w": 50, "h": 60}
        }
    ],
    "triage_priority": "STAT"
}
```

## Nvidia Clara Integration

### Configuration

```python
import requests

CLARA_API = "https://api.clara.nvidia.com/v1"

def configure_clara(api_key):
    """Configure Nvidia Clara."""
    return {
        "base_url": CLARA_API,
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "NVIDIA-CLARA-Tenant-ID": "your-tenant"
        }
    }

def submit_clara_analysis(config, dicom_data, model="medical_imaging"):
    """Submit for Clara analysis."""
    response = requests.post(
        f"{config['base_url']}/infer/{model}",
        headers=config["headers"],
        data=dicom_data
    )
    return response.json()
```

### Available Models

```python
CLARA_MODELS = {
    "clara_organ_s segmentation": "Organ segmentation",
    "clara_lung_nodule": "Lung nodule detection",
    "clara_brain_tumor": "Brain tumor segmentation",
    "clara_carotid": "Carotid artery analysis"
}
```

## Zebra Medical Integration

### API Setup

```python
ZEBRA_API = "https://api.zebra-med.com/v1"

def configure_zebra(api_key):
    """Configure Zebra Medical."""
    return {
        "base_url": ZEBRA_API,
        "api_key": api_key
    }

def analyze_chest_xray(config, dicom_url):
    """Analyze chest X-ray for multiple findings."""
    response = requests.post(
        f"{config['base_url']}/chestxray/analyze",
        headers={"Zebra-API-Key": config["api_key"]},
        json={"dicom_url": dicom_url}
    )
    return response.json()

# Available findings
ZEBRA_CHEST_FINDINGS = [
    "cardiomegaly", "lung_opacity", "pleural_effusion",
    "pneumothorax", "calcification", "pneumonia",
    "atelectasis", "lung_lesion", "fracture", "enlarged_cardiomediastinum"
]
```

## MaxQ AI Integration

### Stroke and PE Detection

```python
MAXQ_API = "https://api.maxq.ai/v1"

def configure_maxq(api_key):
    """Configure MaxQ AI."""
    return {"base_url": MAXQ_API, "api_key": api_key}

def submit_ct_neuro(config, dicom_data):
    """Submit CT neuro for stroke detection."""
    response = requests.post(
        f"{config['base_url']}/neuro/ct",
        headers={"X-API-Key": config["api_key"]},
        data=dicom_data
    )
    return response.json()
```

## Qure AI Integration

### Chest X-ray Analysis

```python
QURE_API = "https://api.qure.ai/v1"

def configure_qure(api_key):
    """Configure Qure AI."""
    return {"base_url": QURE_API, "api_key": api_key}

def analyze_cxr(config, dicom_url, type="comprehensive"):
    """Analyze chest X-ray."""
    response = requests.post(
        f"{config['base_url']}/cxr/analyze",
        headers={"Authorization": f"Bearer {config['api_key']}"},
        json={
            "dicom_url": dicom_url,
            "analysis_type": type
        }
    )
    return response.json()

# Analysis types
QURE_TYPES = ["tb_screening", "comprehensive", "chest_comprehensive"]
```

## PACS Integration

### DICOM Filtered SCU

```python
def configure_pacs_filter(pacs_url, ae_title, ai_platform="aidoc"):
    """Configure PACS to filter studies for AI."""
    return {
        "pacs": {
            "url": pacs_url,
            "ae_title": ae_title,
            "modality": "CT"
        },
        "filter_criteria": {
            "Modality": "CT",
            "BodyPart": ["HEAD", "CHEST", "ABDOMEN"]
        },
        "forward_to": ai_platform,
        "receive_results": True
    }
```

### Worklist Integration

```python
def configure_worklist_alerts(config, alert_config):
    """Configure worklist priority alerts."""
    return {
        "worklist": config["pacs"],
        "alert_on": alert_config.get("critical_findings", True),
        "priority_override": alert_config.get("priority", "STAT"),
        "notification": {
            "method": alert_config.get("method", "worklist"),
            "integrate": alert_config.get("integrate_with", "pacs")
        }
    }
```

## Critical Findings Alerting

### Alert Configuration

```python
def configure_alerts(config, alert_settings):
    """Configure critical findings alerts."""
    return {
        "findings": {
            "hemorrhage": {"priority": "STAT", "notify": True},
            "pulmonary_embolism": {"priority": "STAT", "notify": True},
            "pneumothorax": {"priority": "STAT", "notify": True},
            "aortic_dissection": {"priority": "STAT", "notify": True},
            "stroke": {"priority": "STAT", "notify": True}
        },
        "methods": {
            "email": alert_settings.get("email", True),
            "sms": alert_settings.get("sms", False),
            "pager": alert_settings.get("pager", False),
            "worklist": alert_settings.get("worklist", True)
        },
        "recipients": alert_settings.get("recipients", [])
    }
```

## Batch Processing

### Backlog Processing

```python
def configure_batch_processing(config, batch_settings):
    """Configure batch processing for backlog."""
    return {
        "mode": "batch",
        "source": {
            "pacs": batch_settings.get("pacs_url"),
            "date_range": {
                "from": batch_settings.get("start_date"),
                "to": batch_settings.get("end_date")
            },
            "modality": batch_settings.get("modality", "CT")
        },
        "ai_platform": config["base_url"],
        "priority": "background",
        "results_storage": batch_settings.get("results_db")
    }
```

## Performance Monitoring

### Metrics to Track

```python
DETECTION_METRICS = {
    "volume": ["studies_processed", "studies_per_day"],
    "timing": ["avg_processing_time", "p95_time"],
    "accuracy": ["sensitivity", "specificity", "ppv", "npv"],
    "workflow": ["alerts_sent", "alerts_responded", "time_to_read"]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results received | Check PACS forwarding config |
| Slow processing | Check GPU availability |
| False positives high | Adjust confidence threshold |
| Integration failing | Verify DICOM connectivity |

## Related Skills

- **pacs-workflow**: For PACS integration details
- **ai-quality-review**: For AI output QA
- **radiology-metrics**: For performance monitoring
- **hl7-fhir-radiology**: For results notification

## Examples

### Example 1: Set Up Aidoc CT Head

```
Configure Aidoc for CT head hemorrhage detection with worklist alerts
```

```python
config = configure_aidoc("your-api-key")
pacs_config = configure_pacs_filter("http://pacs:8042", "AIDOC")
alert_config = configure_alerts(config, {
    "email": True,
    "recipients": ["radiologist@hospital.com"]
})
```

### Example 2: Batch Processing

```
Process backlog of 500 chest CT studies for PE detection
```

```python
batch_config = configure_batch_processing(config, {
    "pacs_url": "http://pacs:8042",
    "start_date": "2026-01-01",
    "end_date": "2026-03-31",
    "modality": "CT",
    "results_db": "postgresql://ai-results/db"
})
```
