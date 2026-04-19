---
name: llm-radiology-use
description: Use LLM APIs for radiology tasks. Also use when integrating medical LLMs (MedPaLM, MedLM, Google Health, Amazon HealthLake) for report analysis, clinical reasoning, or radiology AI workflows.
---

# LLM for Radiology

You are an expert in medical large language models (LLMs) for radiology applications. Your role is to help users integrate and optimize LLM-based radiology workflows.

## Supported LLM Platforms

| Platform | Focus | Capabilities |
|----------|-------|--------------|
| MedPaLM/MedLM | Medical reasoning | Report analysis, QA |
| Google Health | Medical imaging | Multi-modal reasoning |
| Amazon HealthLake | Healthcare data | FHIR integration |
| Azure AI Health | Medical NLP | Clinical insights |
| Claude Health | Medical reasoning | Report analysis |

## Key Concepts

### Medical LLM Capabilities

- Report summarization
- Finding extraction
- Clinical reasoning
- Prior study comparison
- Structured data extraction
- Quality assessment

### Prompt Engineering

```python
SYSTEM_PROMPT = """You are an expert radiologist assistant. 
Your role is to analyze radiology reports and provide insights.
Always be clinically accurate and evidence-based.
Prioritize patient safety in all recommendations."""
```

## MedPaLM Integration

### API Configuration

```python
import requests
import json

MEDPALM_API = "https://generativelanguage.googleapis.com/v1beta1"

def configure_medpalm(api_key):
    """Configure MedPaLM API."""
    return {
        "base_url": MEDPALM_API,
        "api_key": api_key,
        "model": "medpalm-2"
    }

def query_medpalm(config, prompt, context=None):
    """Query MedPaLM for radiology insights."""
    url = f"{config['base_url']}/models/{config['model']}:generateContent"
    
    contents = [{"parts": [{"text": prompt}]}]
    
    if context:
        contents[0]["parts"][0]["text"] = f"Context: {context}\n\nQuestion: {prompt}"
    
    response = requests.post(
        f"{url}?key={config['api_key']}",
        headers={"Content-Type": "application/json"},
        json={
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.8,
                "maxOutputTokens": 1024
            }
        }
    )
    
    return response.json()
```

### Report Analysis Prompt

```python
REPORT_ANALYSIS_PROMPT = """Analyze the following radiology report and provide:
1. Key findings summary
2. Critical findings (if any)
3. Clinical recommendations
4. Suggested follow-up

Report:
{report_text}

Respond in structured format."""

def analyze_report(config, report_text):
    """Analyze radiology report with MedPaLM."""
    prompt = REPORT_ANALYSIS_PROMPT.format(report_text=report_text)
    return query_medpalm(config, prompt)
```

## Google Health Integration

### Medical Imaging API

```python
GOOGLE_HEALTH_API = "https://health.googleapis.com/v1"

def configure_google_health(credentials_path):
    """Configure Google Health API."""
    return {
        "base_url": GOOGLE_HEALTH_API,
        "credentials": credentials_path
    }

def medical_insights(config, study_data):
    """Get medical imaging insights."""
    response = requests.post(
        f"{config['base_url']}/projects/{config['project']}/locations:improve",
        headers={"Authorization": f"Bearer {get_token(config)}"},
        json=study_data
    )
    return response.json()
```

## Amazon HealthLake Integration

### FHIR-Based Integration

```python
import boto3

def configure_healthlake(region="us-east-1"):
    """Configure Amazon HealthLake."""
    return {
        "client": boto3.client("healthlake", region_name=region),
        "datastore_id": None  # Set after creation
    }

def query_imaging_history(config, patient_id):
    """Query patient imaging history from HealthLake."""
    response = config["client"].search_by_range(
        AssetId=patient_id,
        SearchParameters={
            "filters": {
                "DocumentType": {"Value": "DiagnosticReport", "Type": "String"}
            }
        }
    )
    return response["Results"]
```

### Send Imaging Results

```python
def send_results_to_healthlake(config, patient_id, report_data):
    """Send radiology report to HealthLake."""
    config["client"].create_fhir_resource({
        "ResourceType": "DiagnosticReport",
        "subject": {"reference": f"Patient/{patient_id}"},
        "status": "final",
        "code": {"text": report_data["study_type"]},
        "conclusion": report_data["impression"]
    })
```

## Azure AI Health

### Health NLP Configuration

```python
AZURE_ENDPOINT = "https://<resource>.cognitiveservices.azure.com"

def configure_azure_health(endpoint, api_key):
    """Configure Azure AI Health."""
    return {
        "endpoint": endpoint,
        "api_key": api_key
    }

def extract_medical_entities(config, text):
    """Extract medical entities from report."""
    response = requests.post(
        f"{config['endpoint']}/text/analytics/v3.1/entities/health",
        headers={
            "Ocp-Apim-Subscription-Key": config["api_key"],
            "Content-Type": "application/json"
        },
        json={"documents": [{"id": "1", "text": text}]}
    )
    return response.json()
```

## Structured Data Extraction

### Report to Structured Format

```python
EXTRACTION_PROMPT = """Extract structured data from this radiology report:

Report: {report_text}

Extract and format as JSON:
{{
    "patient_id": "...",
    "study_type": "...",
    "findings": [
        {{
            "anatomy": "...",
            "finding": "...",
            "size": "...",
            "location": "..."
        }}
    ],
    "impression": "...",
    "critical_findings": [...],
    "recommendations": [...]
}}"""

def extract_structured(config, report_text):
    """Extract structured data from report."""
    prompt = EXTRACTION_PROMPT.format(report_text=report_text)
    response = query_llm(config, prompt)
    
    # Parse JSON from response
    return json.loads(extract_json(response))
```

## Clinical Reasoning

### Comparison Analysis

```python
COMPARISON_PROMPT = """Compare these two CT reports and identify changes:

Current Report:
{current}

Prior Report:
{prior}

Identify:
1. New findings
2. Resolved findings
3. Changed findings (with details)
4. Stable findings
5. Clinical significance"""

def compare_reports(config, current, prior):
    """Compare current and prior reports."""
    prompt = COMPARISON_PROMPT.format(current=current, prior=prior)
    return query_llm(config, prompt)
```

### Differential Diagnosis

```python
DIFFERENTIAL_PROMPT = """Based on these imaging findings, provide differential diagnosis:

Findings: {findings}
Modality: {modality}
Clinical history: {history}

For each differential:
1. Diagnosis
2. Key supporting features
3. Most likely ranking
4. Recommended additional imaging (if needed)"""

def get_differential(config, findings, modality, history):
    """Get differential diagnosis."""
    prompt = DIFFERENTIAL_PROMPT.format(
        findings=findings,
        modality=modality,
        history=history
    )
    return query_llm(config, prompt)
```

## Batch Processing

### Bulk Report Analysis

```python
def batch_analyze_reports(config, reports, batch_size=10):
    """Analyze multiple reports in batch."""
    results = []
    
    for i in range(0, len(reports), batch_size):
        batch = reports[i:i + batch_size]
        batch_results = []
        
        for report in batch:
            try:
                result = analyze_report(config, report["text"])
                batch_results.append({
                    "report_id": report["id"],
                    "analysis": result
                })
            except Exception as e:
                batch_results.append({
                    "report_id": report["id"],
                    "error": str(e)
                })
        
        results.extend(batch_results)
    
    return results
```

## Best Practices

1. **Validate outputs** - Always review LLM-generated content
2. **Use appropriate temperature** - Lower (0.2-0.3) for factual analysis
3. **Provide context** - Include clinical history when available
4. **Set confidence thresholds** - Flag low-confidence responses
5. **Monitor for hallucinations** - Verify against source data

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow responses | Use batch processing |
| Inaccurate output | Refine prompt with examples |
| Missing data | Ensure context is complete |
| Rate limits | Implement backoff strategy |

## Related Skills

- **radiology-report-analysis**: For report analysis basics
- **llm-radiology-use**: For LLM integration (this skill)
- **ai-quality-review**: For output validation
- **guideline-integration**: For evidence-based recommendations

## Examples

### Example 1: Analyze Report

```
Use MedPaLM to analyze this chest CT report
```

```python
report = "CT CHEST: 2.5cm mass right upper lobe..."
analysis = analyze_report(config, report)
```

### Example 2: Compare Studies

```
Compare this CT with the prior study from 3 months ago
```

```python
comparison = compare_reports(
    config,
    current="Current report text...",
    prior="Prior report text..."
)
```

### Example 3: Extract Structured Data

```
Extract findings from this report to structured format
```

```python
structured = extract_structured(config, report_text)
# Returns JSON with findings, measurements, etc.
```
