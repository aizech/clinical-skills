---
name: radiology-report-analysis
description: Analyze structured/free-text radiology reports, extract key findings, measurements, and impressions. Also use when the user provides a report for review, summary, data extraction, critical findings identification, or report quality assessment. For structured reporting templates, see structured-reporting.
---

# Radiology Report Analysis

You are a radiology report analysis expert. Your role is to extract, interpret, and structure information from radiology reports.

## Report Structure

### Standard Report Sections

```
RADIOLOGY REPORT
├── Header Information
│   ├── Patient ID
│   ├── Study Date
│   ├── Modality
│   ├── Referring Physician
│   └── Accession Number
├── Clinical History
├── Examination/Study Description
├── Findings
│   ├── Organ System 1
│   ├── Organ System 2
│   └── ...
└── Impression
    ├── Primary Finding (numbered)
    ├── Secondary Finding
    └── Recommendations
```

## Extraction Patterns

### Findings Extraction

Extract findings from free-text reports:

```python
def extract_findings(report_text):
    sections = parse_report_sections(report_text)
    findings = []
    
    # Pattern: Finding descriptions often start with bullets, numbers, or organ names
    finding_patterns = [
        r'[-•]\s*(.+)',           # Bullet points
        r'\d+\.\s+([A-Z][^:]+):\s*(.+)',  # Numbered with colon
        r'([A-Z][a-z]+(?:\s+[a-z]+)?):\s*(.+)',  # Organ: description
    ]
    
    for pattern in finding_patterns:
        matches = re.finditer(pattern, report_text)
        for match in matches:
            findings.append({
                'organ': extract_organ(match),
                'description': match.group(1) if match.lastindex else match.group(0),
                'severity': classify_severity(match)
            })
    
    return findings
```

### Impression Extraction

```python
def extract_impression(report_text):
    # Look for IMPRESSION section
    impression_pattern = r'IMPRESSION[:\s]+(.+?)(?:\n\n|\Z)'
    match = re.search(impression_pattern, report_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        impression_text = match.group(1)
        # Parse numbered impressions
        impressions = re.findall(r'\d+\.\s*(.+?)(?=\n\d+\.|\Z)', impression_text)
        return impressions
    
    # Fallback: last paragraph is often impression
    paragraphs = report_text.split('\n\n')
    return [paragraphs[-1]] if paragraphs else []
```

## Finding Classification

### Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Life-threatening, immediate action | STAT communication |
| Urgent | Significant, timely action needed | Within hours |
| Routine | Non-urgent, follow-up as appropriate | Standard scheduling |
| Normal | No significant abnormality | None |
| Incidental | Unexpected but not clinically significant | Document, consider follow-up |

### Finding Categories

```python
FINDING_CATEGORIES = {
    'mass': ['mass', 'lesion', 'nodule', 'tumor', 'growth'],
    'inflammation': ['inflammation', 'edema', 'swelling'],
    'fluid': ['effusion', 'ascites', 'hemorrhage', 'bleeding'],
    'calcification': ['calcification', 'stone', 'calculus'],
    'fracture': ['fracture', 'break', ' discontinuity'],
    'occlusion': ['occlusion', 'stenosis', 'blockage', 'embolism'],
    'infection': ['infection', 'abscess', 'pneumonia'],
    'deformity': ['deformity', 'dislocation', 'subluxation']
}
```

## Measurement Extraction

Extract measurements and dimensions:

```python
def extract_measurements(text):
    measurements = []
    
    # Pattern: Number + unit combinations
    measurement_pattern = r'(\d+\.?\d*)\s*(cm|mm|mm|mL|mg|%|°|bpm)'
    matches = re.finditer(measurement_pattern, text, re.IGNORECASE)
    
    for match in matches:
        measurements.append({
            'value': float(match.group(1)),
            'unit': match.group(2).lower(),
            'context': extract_context_around(text, match.start(), 50)
        })
    
    return measurements
```

### Anatomy Extraction

```python
def extract_anatomy(text):
    anatomy_patterns = {
        'brain': r'\b(brain|cerebral|intracranial|frontal|parietal|temporal|occipital|cerebellar)\b',
        'lung': r'\b(lung|pulmonary|pleural|mediastinal|hilar|bronchial)\b',
        'liver': r'\b(liver|hepatic|hepatobiliary)\b',
        'kidney': r'\b(kidney|renal|adrenal)\b',
        'spine': r'\b(spine|vertebral|disc|spinal|cord)\b',
        'heart': r'\b(heart|cardiac|pericardial|aortic|valvular)\b',
        'abdomen': r'\b(abdomen|abdominal|bowel|intestinal|mesenteric|peritoneal)\b'
    }
    
    findings = {}
    for organ, pattern in anatomy_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            findings[organ] = True
    
    return list(findings.keys())
```

## Critical Findings Detection

```python
CRITICAL_FINDINGS = {
    'pneumothorax': {'severity': 'critical', 'urgency': 'STAT'},
    'tension pneumothorax': {'severity': 'critical', 'urgency': 'STAT'},
    'large pleural effusion': {'severity': 'urgent', 'urgency': 'within_hours'},
    'pulmonary embolism': {'severity': 'critical', 'urgency': 'STAT'},
    'aortic dissection': {'severity': 'critical', 'urgency': 'STAT'},
    'aortic aneurysm rupture': {'severity': 'critical', 'urgency': 'STAT'},
    'bowel obstruction': {'severity': 'urgent', 'urgency': 'within_hours'},
    'bowel perforation': {'severity': 'critical', 'urgency': 'STAT'},
    'intracranial hemorrhage': {'severity': 'critical', 'urgency': 'STAT'},
    'stroke': {'severity': 'critical', 'urgency': 'STAT'},
    'brain herniation': {'severity': 'critical', 'urgency': 'STAT'},
    'fracture': {'severity': 'routine', 'urgency': 'standard'},
    'tumor': {'severity': 'routine', 'urgency': 'standard'},
    'metastasis': {'severity': 'urgent', 'urgency': 'within_days'}
}

def detect_critical_findings(text):
    text_lower = text.lower()
    critical = []
    
    for finding, info in CRITICAL_FINDINGS.items():
        if finding in text_lower:
            critical.append({
                'finding': finding,
                'severity': info['severity'],
                'urgency': info['urgency']
            })
    
    return critical
```

## Comparison Detection

Detect comparison with prior studies:

```python
def detect_comparison(text):
    comparison_indicators = [
        'compared to', 'comparison with', 'compared with',
        'prior study', 'previous', 'old study',
        'stable', 'unchanged', 'improved', 'worsened',
        'new', 'interval change', 'developed'
    ]
    
    text_lower = text.lower()
    
    has_comparison = any(indicator in text_lower for indicator in comparison_indicators)
    
    if has_comparison:
        return {
            'has_comparison': True,
            'new_findings': extract_new_findings(text),
            'stable_findings': extract_stable_findings(text),
            'changed_findings': extract_changed_findings(text)
        }
    
    return {'has_comparison': False}
```

## Incidental Findings

Detect incidental findings requiring follow-up:

```python
INCIDENTAL_FINDINGS = {
    'renal cyst': {'followup': 'usually none for simple cysts <3cm'},
    'gallbladder polyps': {'followup': 'ultrasound if >5mm or high risk'},
    'thyroid nodules': {'followup': 'ultrasound if >1cm or suspicious features'},
    'adrenal nodule': {'followup': 'CT or MRI for characterization if >1cm'},
    'lung nodule': {'followup': 'depends on size and risk factors'},
    'liver hemangioma': {'followup': 'usually none for classic appearance'}
}

def detect_incidental_findings(text):
    incidentals = []
    text_lower = text.lower()
    
    for finding, info in INCIDENTAL_FINDINGS.items():
        if finding in text_lower:
            incidentals.append({
                'finding': finding,
                'followup_recommendation': info['followup']
            })
    
    return incidentals
```

## Report Quality Assessment

```python
def assess_report_quality(report):
    issues = []
    
    # Check for required sections
    if 'IMPRESSION' not in report.upper():
        issues.append('Missing impression section')
    
    # Check impression length
    impression = extract_impression(report)
    if len(' '.join(impression)) < 10:
        issues.append('Impression too brief')
    
    # Check for specificity
    if 'normal' in report.lower() and len(report) < 200:
        issues.append('Normal report may lack sufficient detail')
    
    # Check for comparison when expected
    if 'follow-up' in report.lower() or 'f/u' in report.lower():
        if not detect_comparison(report)['has_comparison']:
            issues.append('Follow-up requested without prior comparison')
    
    return {
        'quality_score': max(0, 100 - len(issues) * 20),
        'issues': issues,
        'recommendation': 'Acceptable' if len(issues) <= 2 else 'Needs revision'
    }
```

## Output Formats

### Structured JSON Output

```json
{
  "report_type": "CT Chest",
  "accession_number": "ACC123456",
  "study_date": "2026-04-03",
  "findings": [
    {
      "organ_system": "lung",
      "finding": "2.5 cm mass in right upper lobe",
      "measurements": {"size": "2.5 cm"},
      "location": "right upper lobe",
      "severity": "routine",
      "critical": false
    },
    {
      "organ_system": "mediastinum",
      "finding": "No mediastinal lymphadenopathy",
      "severity": "normal",
      "critical": false
    }
  ],
  "impression": [
    "Lung mass, concerning for malignancy"
  ],
  "critical_findings": [],
  "incidental_findings": [],
  "comparison": null,
  "followup_recommended": true,
  "recommendations": [
    "CT-guided biopsy of lung mass",
    "PET/CT for staging"
  ],
  "quality_assessment": {
    "score": 100,
    "issues": []
  }
}
```

### Summary Format

```
ANALYSIS SUMMARY
================

Study: CT Chest with Contrast
Date: 2026-04-03

KEY FINDINGS:
• Lung: 2.5 cm mass, right upper lobe
• No lymphadenopathy
• Small pleural effusion (right)

IMPRESSION:
Lung mass, concerning for malignancy

RECOMMENDATIONS:
• CT-guided biopsy
• PET/CT for staging

Critical Findings: None
Follow-up Needed: Yes

Quality: Acceptable
```

## Related Skills

- **structured-reporting**: For structured report templates
- **impression-generation**: For AI-assisted impression writing
- **findings-extraction**: For detailed data extraction
- **patient-results-letter**: For patient-friendly communication
- **followup-tracking**: For managing incidental findings

## Examples

### Example 1: Lung Mass Analysis
**Input**: Full CT chest report with mass
**Output**: Structured findings, impression, measurements extracted

### Example 2: Normal Study
**Input**: Normal chest X-ray report
**Output**: Findings verified as normal, no critical findings

### Example 3: Critical Finding
**Input**: CT head showing hemorrhage
**Output**: Critical finding flagged, urgency identified

### Example 4: Incidental Findings
**Input**: CT abdomen with multiple incidental findings
**Output**: Incidental findings listed with follow-up recommendations
