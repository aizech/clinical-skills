---
name: structured-reporting
description: Create and optimize structured radiology reports using standardized templates. Also use when the user mentions BI-RADS, LI-RADS, PI-RADS, TI-RADS, or needs to convert free-text reports to structured format. For free-text analysis, see radiology-report-analysis.
---

# Structured Reporting

You are an expert in structured radiology reporting. Your role is to help create, convert, and optimize standardized radiology reports.

## Reporting Standards

### By Modality/Body Part

| Standard | Modality | Use Case |
|----------|----------|----------|
| BI-RADS | Mammography | Breast imaging assessment |
| LI-RADS | MRI/CT | Liver imaging reporting |
| PI-RADS | MRI | Prostate imaging |
| TI-RADS | Ultrasound | Thyroid imaging |
| Lung-RADS | CT | Lung cancer screening |
| RADS | Various | Multiple standardized systems |

## BI-RADS Templates

### BI-RADS Assessment Categories

| Category | Assessment | Management |
|---------|------------|------------|
| 0 | Incomplete | Additional imaging |
| 1 | Negative | Routine screening |
| 2 | Benign | Routine screening |
| 3 | Probably Benign | Short interval follow-up |
| 4A | Suspicious | Biopsy |
| 4B | Suspicious | Biopsy |
| 4C | Suspicious | Biopsy |
| 5 | Highly Suspicious | Biopsy |
| 6 | Known Malignancy | Treatment |

### BI-RADS Report Template

```markdown
## MAMMOGRAPHY REPORT

**Patient:** [Name] | **DOB:** [Date] | **Accession:** [Number]

### Clinical History:
[History]

### Technique:
[Standard views, supplementary views]

### Comparison:
[Prior studies compared]

### Findings:

**Left Breast:**
- [Location]: [Finding] [size if applicable]

**Right Breast:**
- [Location]: [Finding] [size if applicable]

### Assessment:
**BI-RADS: [Category]** - [Description]

### Recommendations:
[Follow-up recommendations]
```

## LI-RADS Templates

### LI-RADS Categories

| Category | Definition |
|----------|------------|
| LR-1 | Definitely benign |
| LR-2 | Probably benign |
| LR-3 | Intermediate probability of malignancy |
| LR-4 | Probably HCC |
| LR-5 | Definitely HCC |
| LR-M | Probably malignant, not HCC specific |

### LI-RADS Report Template

```markdown
## LIVER IMAGING REPORT

**Study:** MRI Liver with contrast | **Accession:** [Number]

### Clinical History:
[ cirrhosis surveillance / elevated AFP / etc. ]

### Technique:
[ MRI sequences, contrast agent ]

### Liver Observations:

| # | Size (mm) | Segment | Category | APHE | Washout | Capsule | Threshold Growth |
|---|-----------|--------|----------|------|---------|--------|-----------------|
| 1 | 25 | S8 | LR-5 | Yes | Yes | Yes | - |

### Additional Findings:
[Other benign findings, etc.]

### Impression:
1. [LR-X] - [Size] hemodynamically [characteristic] in [Location]

### Recommendations:
[Follow-up imaging / biopsy / treatment]
```

## PI-RADS Templates

### PI-RADS Assessment

| Category | Assessment |
|----------|------------|
| PI-RADS 1 | Very low |
| PI-RADS 2 | Low |
| PI-RADS 3 | Intermediate |
| PI-RADS 4 | High |
| PI-RADS 5 | Very high |

### PI-RADS Report Template

```markdown
## PROSTATE MRI REPORT

**Study:** Multiparametric MRI Prostate | **Accession:** [Number]

### Clinical History:
[PSA level, previous biopsies, clinical suspicion]

### Technique:
[T2W, DWI, DCE sequences]

### Prostate Volume:
[Volume in cc]

### Findings:

**Transition Zone:**
- [Location, size, PIRADS score, description]

**Peripheral Zone:**
- [Location, size, PIRADS score, description]

**Extra-prostatic Extension:**
[Present / Not identified]

**Seminal Vesicles:**
[Involved / Not involved]

**Lymph Nodes:**
[Suspicious / Not suspicious]

### Assessment:
**PI-RADS: [Score]** - [Clinical significance]

### Recommendations:
[Biopsy guidance / follow-up]
```

## TI-RADS Templates

### TI-RADS Categories

| Category | Risk | Recommendation |
|----------|------|----------------|
| TR1 | None | None |
| TR2 | Very low | None |
| TR3 | Low | Follow-up |
| TR4 | Intermediate | FNA if criteria met |
| TR5 | High | FNA recommended |

### TI-RADS Report Template

```markdown
## THYROID ULTRASOUND REPORT

**Study:** Thyroid Ultrasound | **Accession:** [Number]

### Clinical History:
[Indication for study]

### Findings:

**Right Lobe:**
- [Size], [echogenicity], [margins], [calcifications], [TI-RADS: TR-X]

**Left Lobe:**
- [Same parameters]

**Isthmus:**
- [Findings]

**Central Neck:**
- [Lymph nodes, if visible]

### Assessment:
**TI-RADS: [Category]** - [Description]

### Recommendations:
[FNA if indicated, follow-up schedule]
```

## Lung-RADS Templates

### Lung-RADS Categories

| Category | Findings | Management |
|----------|----------|------------|
| 0 | Incomplete | Additional evaluation |
| 1 | No nodules | Continue annual screening |
| 2 | Benign | Continue annual screening |
| 3 | Probably benign | 6-month follow-up |
| 4A | Suspicious | 3-month follow-up or PET |
| 4B | Very suspicious | Chest CT with/without PET |
| 4C | - | Evaluate as 4B |
| S | Significant incidental finding | - |

### Lung-RADS Report Template

```markdown
## CT CHEST LUNG CANCER SCREENING REPORT

**Study:** Low-dose CT Chest | **Accession:** [Number]

### Clinical History:
[Age, smoking history, eligibility criteria]

### Findings:

**Lungs:**
- [Nodules identified with characteristics]
  - Location: [Lobe]
  - Size: [mm]
  - Type: [Solid/GGS/Mixed]
  - Margins: [Smooth/irregular/spiculated]

**Nodule Analysis:**
| Nodule | Location | Size | Type | Lung-RADS |
|--------|----------|------|------|-----------|
| 1 | RLL | 6mm | Solid | 2 |

### Assessment:
**Lung-RADS: [Category]**

### Recommendations:
[Based on category - follow-up/CT/PET/biopsy]

### Additional Findings:
[Any significant incidental findings]
```

## Free-Text to Structured Conversion

```python
def convert_free_to_structured(free_text_report):
    """Convert free-text report to structured format."""
    
    # Extract key sections
    sections = {
        "clinical_history": extract_section(free_text_report, "CLINICAL|HISTORY|INDICATION"),
        "findings": extract_findings(free_text_report),
        "impression": extract_section(free_text_report, "IMPRESSION|CONCLUSION"),
    }
    
    # Identify modality and body part
    modality = detect_modality(free_text_report)
    body_part = detect_body_part(free_text_report)
    
    # Select appropriate template
    if "BREAST" in free_text_report.upper():
        template = "BI-RADS"
    elif "LIVER" in free_text_report.upper():
        template = "LI-RADS"
    elif "PROSTATE" in free_text_report.upper():
        template = "PI-RADS"
    elif "THYROID" in free_text_report.upper():
        template = "TI-RADS"
    else:
        template = "GENERAL"
    
    return {
        "original": free_text_report,
        "structured": sections,
        "template": template,
        "modality": modality,
        "body_part": body_part
    }
```

## Report Quality Checklist

- [ ] All required sections present
- [ ] Clinical indication documented
- [ ] Comparison with priors noted
- [ ] All findings described with size/characteristics
- [ ] Appropriate standard scoring used (BI-RADS, LI-RADS, etc.)
- [ ] Impression clearly states most significant findings
- [ ] Recommendations actionable and specific
- [ ] Incidental findings addressed

## Related Skills

- **radiology-report-analysis**: For analyzing existing reports
- **impression-generation**: For AI-assisted impression writing
- **patient-results-letter**: For patient communication
- **guideline-integration**: For standard compliance

## Examples

### Example 1: BI-RADS Report

```
Generate a BI-RADS 4A report for a spiculated mass
```

```markdown
**Left Breast:**
- 2 o'clock: 15mm spiculated mass with suspicious calcifications

**Assessment:**
BI-RADS: 4A - Low suspicion for malignancy

**Recommendations:**
Ultrasound-guided biopsy recommended
```

### Example 2: Free-Text to Structured

```
Convert: "CT chest shows 2.5cm mass in right upper lobe. No mediastinal lymphadenopathy. Suspicion for malignancy."
```

```markdown
**Findings:**
- Lungs: 25mm spiculated mass, right upper lobe
- Mediastinum: No lymphadenopathy

**Assessment:**
- Lung mass, concerning for malignancy

**Recommendations:**
- PET/CT for staging
- CT-guided biopsy
```
