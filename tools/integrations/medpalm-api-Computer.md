# MedPaLM API Integration

Google's medical LLM for radiology report analysis.

## Connection

```yaml
api_base: https://generativelanguage.googleapis.com/v1beta2
model: medpaalm
api_key: ${GOOGLE_AI_API_KEY}
```

## Authentication

API key in request: `?key={api_key}`

## Key Operations

### Report Analysis
```bash
POST /models/medpaalm:generateContent
{
  "contents": [{
    "role": "user",
    "parts": [{
      "text": "Analyze this radiology report and extract key findings:\n\n[Report text here]"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "topP": 0.8,
    "maxOutputTokens": 1024
  }
}
```

### Structured Extraction
```bash
POST /models/medpaalm:generateContent
{
  "contents": [{
    "role": "user", 
    "parts": [{
      "text": "Extract findings as structured data:\n\nReport: [text]\n\nOutput JSON with: findings[], impressions[], critical_findings boolean, followup_recommended boolean"
    }]
  }]
}
```

### Comparison Analysis
```bash
POST /models/medpaalm:generateContent
{
  "contents": [{
    "role": "user",
    "parts": [{
      "text": "Compare current and prior findings:\n\nCurrent: [report]\nPrior: [prior report]\n\nProvide change assessment and significance."
    }]
  }]
}
```

## Prompt Templates

### Chest X-ray Interpretation
```
You are an expert radiologist. Analyze this chest X-ray report and:
1. Identify primary findings
2. Assess severity (normal/mild/moderate/severe)
3. Flag critical findings requiring immediate attention
4. Recommend follow-up if indicated

Report: {report_text}
```

### Oncology Assessment
```
Review this imaging report for oncologic assessment:
1. Tumor response (CR/PR/SD/PD per RECIST)
2. New lesions or progression
3. Treatment-related changes
4. Next imaging recommendations

Report: {report_text}
```

## Rate Limits

- Standard: 60 requests/minute
- Enterprise: Custom limits via Vertex AI

## Tool Registration

```json
{
  "name": "medpalm_api",
  "description": "Google MedPaLM for radiology report analysis and extraction",
  "category": "llm_radiology",
  "endpoints": ["report_analyze", "structured_extract", "comparison", "clinical_summary"]
}
```
