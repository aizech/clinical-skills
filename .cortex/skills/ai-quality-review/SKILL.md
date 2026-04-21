---
name: ai-quality-review
description: QA AI outputs, detect false positives/negatives, and validate AI results. Also use when evaluating AI system performance, reviewing AI-assisted findings, or conducting quality assurance on AI detection and reporting tools.
---

# AI Quality Review

You are an expert in AI quality assurance for medical imaging. Your role is to help users validate, review, and improve AI system performance.

## Quality Metrics

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Sensitivity | True Positive / (TP + FN) | >95% for critical |
| Specificity | True Negative / (TN + FP) | >90% |
| PPV | TP / (TP + FP) | Varies by use case |
| NPV | TN / (TN + FN) | >95% |
| Accuracy | (TP + TN) / Total | >90% |

### Detection-Specific Metrics

```python
def calculate_detection_metrics(tp, fp, tn, fn):
    """Calculate detection quality metrics."""
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0
    
    return {
        "sensitivity": sensitivity,
        "specificity": specificity,
        "ppv": ppv,
        "npv": npv,
        "accuracy": (tp + tn) / (tp + tn + fp + fn)
    }
```

## False Positive Analysis

### Detection Patterns

```python
FALSE_POSITIVE_PATTERNS = {
    "anatomical_mimics": [
        "vessels mistaken for nodules",
        "bone for hemorrhage",
        "artifact for pathology"
    ],
    "technical_artifacts": [
        "motion artifact",
        "beam hardening",
        "partial volume"
    ],
    "algorithm_errors": [
        "threshold too low",
        "segmentation error",
        "classification mistake"
    ]
}

def analyze_false_positives(findings, ground_truth):
    """Analyze false positive patterns."""
    fp_analysis = {
        "count": len(findings) - len(ground_truth.intersection(findings)),
        "patterns": [],
        "anatomical_location": [],
        "recommendations": []
    }
    
    for finding in findings:
        if finding not in ground_truth:
            fp_analysis["patterns"].append(categorize_fp(finding))
            fp_analysis["anatomical_location"].append(finding.get("location"))
    
    return fp_analysis
```

### Common FP Causes

| Finding Type | Common FP Cause | Mitigation |
|-------------|----------------|------------|
| Lung Nodule | Vessel, scar | Review with contrast phases |
| Hemorrhage | Beam hardening | Check timing, artifact patterns |
| PE | Motion, flow artifact | Review multiple phases |
| Fracture | Lucency, suture | Compare to prior |

## False Negative Analysis

### Missed Finding Patterns

```python
FALSE_NEGATIVE_PATTERNS = {
    "small_findings": "Lesions below detection threshold",
    "atypical_appearance": "Unusual presentation",
    "location": "Difficult anatomical location",
    "technical_quality": "Suboptimal image quality",
    "cognitive_bias": "Satisfaction of search"
}

def analyze_false_negatives(ai_missed, human_found):
    """Analyze false negative patterns."""
    fn_analysis = {
        "count": len(ai_missed),
        "patterns": [],
        "characteristics": []
    }
    
    for finding in ai_missed:
        fn_analysis["patterns"].append(
            categorize_fn_pattern(finding)
        )
        fn_analysis["characteristics"].append({
            "size": finding.get("size_mm"),
            "location": finding.get("location"),
            "type": finding.get("finding_type")
        })
    
    return fn_analysis
```

## Confidence Assessment

### Score Interpretation

```python
CONFIDENCE_THRESHOLDS = {
    "high": {"min": 0.9, "action": "Auto-accept"},
    "moderate": {"min": 0.7, "action": "Review"},
    "low": {"min": 0.5, "action": "Mandatory review"},
    "uncertain": {"min": 0, "action": "Escalate"}
}

def assess_confidence(score, threshold_type="standard"):
    """Assess AI confidence score."""
    thresholds = CONFIDENCE_THRESHOLDS
    
    for level, info in thresholds.items():
        if score >= info["min"]:
            return {
                "level": level,
                "action": info["action"],
                "score": score
            }
```

### Calibration Assessment

```python
def assess_calibration(predicted_probs, observed_outcomes, bins=10):
    """Assess if predicted probabilities match observed rates."""
    import numpy as np
    
    bin_edges = np.linspace(0, 1, bins + 1)
    calibration_errors = []
    
    for i in range(bins):
        bin_min = bin_edges[i]
        bin_max = bin_edges[i + 1]
        
        mask = (predicted_probs >= bin_min) & (predicted_probs < bin_max)
        if mask.sum() > 0:
            predicted = predicted_probs[mask].mean()
            observed = observed_outcomes[mask].mean()
            calibration_errors.append({
                "bin": f"{bin_min:.1f}-{bin_max:.1f}",
                "predicted": predicted,
                "observed": observed,
                "error": abs(predicted - observed)
            })
    
    return calibration_errors
```

## Comparative Analysis

### AI vs Radiologist

```python
def compare_ai_radiologist(ai_findings, radiologist_findings):
    """Compare AI and radiologist findings."""
    agreement = {
        "total_ai_findings": len(ai_findings),
        "total_radiologist_findings": len(radiologist_findings),
        "agreed_findings": [],
        "ai_only": [],
        "radiologist_only": [],
        "disagreed_characteristics": []
    }
    
    ai_set = set([f["uid"] for f in ai_findings])
    rad_set = set([f["uid"] for f in radiologist_findings])
    
    agreement["agreed_findings"] = list(ai_set & rad_set)
    agreement["ai_only"] = list(ai_set - rad_set)
    agreement["radiologist_only"] = list(rad_set - ai_set)
    
    agreement["agreement_rate"] = len(agreement["agreed_findings"]) / len(ai_set | rad_set)
    
    return agreement
```

### Concordance Metrics

```python
def calculate_concordance(ai_results, radiologist_results):
    """Calculate AI-radiologist concordance."""
    comparison = compare_ai_radiologist(ai_results, radiologist_results)
    
    return {
        "sensitivity": (
            len(comparison["agreed_findings"]) / 
            len(comparison["radiologist_only"] | comparison["agreed_findings"])
        ),
        "ai_precision": (
            len(comparison["agreed_findings"]) / 
            len(comparison["ai_only"] | comparison["agreed_findings"])
        ),
        "agreement_rate": comparison["agreement_rate"]
    }
```

## Error Pattern Analysis

### Aggregate Review

```python
def analyze_error_patterns(study_results, time_period="monthly"):
    """Analyze patterns in AI errors over time."""
    patterns = {
        "false_positives": [],
        "false_negatives": [],
        "by_modality": {},
        "by_finding_type": {},
        "by_anatomy": {}
    }
    
    for result in study_results:
        if result["outcome"] == "fp":
            patterns["false_positives"].append(categorize_error(result))
        elif result["outcome"] == "fn":
            patterns["false_negatives"].append(categorize_error(result))
        
        # Categorize by modality
        mod = result.get("modality", "unknown")
        patterns["by_modality"][mod] = patterns["by_modality"].get(mod, 0) + 1
    
    return patterns
```

### Trend Analysis

```python
def analyze_trends(error_data, date_range):
    """Analyze error trends over time."""
    import pandas as pd
    
    df = pd.DataFrame(error_data)
    df["date"] = pd.to_datetime(df["date"])
    
    return {
        "daily_avg_errors": df.groupby("date").size().mean(),
        "error_rate_trend": calculate_trend(df["date"], df["error_rate"]),
        "common_patterns": df["pattern"].value_counts().head(5)
    }
```

## Quality Reporting

### Generate QA Report

```python
def generate_qa_report(ai_results, radiologist_results, date_range):
    """Generate comprehensive QA report."""
    metrics = calculate_detection_metrics(
        tp=len(agreed),
        fp=len(ai_only),
        fn=len(rad_only),
        tn=0
    )
    
    concordance = calculate_concordance(ai_results, radiologist_results)
    fp_analysis = analyze_false_positives(ai_results, radiologist_results)
    fn_analysis = analyze_false_negatives(ai_results, radiologist_results)
    
    return {
        "period": date_range,
        "total_studies": len(ai_results),
        "detection_metrics": metrics,
        "concordance": concordance,
        "false_positives": fp_analysis,
        "false_negatives": fn_analysis,
        "recommendations": generate_recommendations(metrics, concordance)
    }
```

### Report Template

```
AI QUALITY ASSURANCE REPORT
==========================
Period: March 2026
Generated: 2026-04-03

SUMMARY
-------
Total Studies Reviewed: 500
AI Findings: 150
Radiologist Findings: 145
Agreement Rate: 92%

DETECTION METRICS
-----------------
Sensitivity: 94.5%
Specificity: 89.2%
PPV: 91.3%
NPV: 93.1%

ERROR ANALYSIS
--------------
False Positives: 12 (8%)
  - Vessels: 5
  - Artifacts: 4
  - Other: 3

False Negatives: 7 (5%)
  - Small nodules: 3
  - Atypical appearance: 2
  - Technical quality: 2

RECOMMENDATIONS
---------------
1. Adjust confidence threshold for lung nodules
2. Add motion correction preprocessing
3. Review vessel-mimic patterns
```

## Quality Assurance Workflow

### Review Process

```python
QA_WORKFLOW = {
    "1_initial": {
        "ai_results": "All studies",
        "action": "Automatic collection"
    },
    "2_sampling": {
        "method": "Random sampling",
        "rate": "10% of normal, 100% of critical",
        "action": "Random selection"
    },
    "3_comparison": {
        "process": "AI vs final report",
        "action": "Flag discrepancies"
    },
    "4_review": {
        "reviewer": "QA radiologist",
        "action": "Adjudicate disagreements"
    },
    "5_feedback": {
        "loop": "AI model update",
        "action": "Continuous improvement"
    }
}
```

## Related Skills

- **ai-detection-pipeline**: For AI system configuration
- **radiology-metrics**: For metric tracking
- **radiology-report-analysis**: For finding validation
- **dataset-preprocessing**: For test data preparation

## Examples

### Example 1: Review AI Finding

```
Is this AI-detected lung nodule a false positive?
```

```python
review = review_ai_finding(
    ai_finding={"location": "RLL", "size": 8, "confidence": 0.75},
    priors={"prior_ct": "6mm stable nodule RLL"},
    imaging={"images": ["series1.dcm"]}
)
```

### Example 2: Generate Monthly Report

```
Generate QA report for AI performance in March 2026
```

```python
report = generate_qa_report(
    ai_results=monthly_ai_results,
    radiologist_results=monthly_rad_results,
    date_range={"start": "2026-03-01", "end": "2026-03-31"}
)
```

### Example 3: Analyze Error Patterns

```
Identify error patterns in recent AI detections
```

```python
patterns = analyze_error_patterns(
    study_results=last_30_days,
    time_period="monthly"
)
```
