---
name: guideline-integration
description: Access and apply professional radiology society guidelines. Use when user mentions "ACR criteria", "appropriateness rating", "guideline for", "society recommendation", "BI-RADS update", "dose reference levels", or "protocol guidelines".
---

# Guideline Integration Skill

## Triggers

- "ACR criteria"
- "appropriateness rating"
- "guideline for"
- "society recommendation"
- "BI-RADS update"
- "dose reference levels"
- "protocol guidelines"

## Parameters

- `guideline_type` (required): Type of guideline needed
  - `appropriateness` - ACR Appropriateness Criteria
  - `reporting` - Structured reporting standards (BI-RADS, LI-RADS)
  - `dose` - Radiation dose guidelines
  - `protocol` - Imaging protocol recommendations
  - `screening` - Screening eligibility guidelines
- `clinical_scenario` (required): Brief description of clinical question
- `modality` (optional): Specific imaging modality
- `age_group` (optional): Adult, pediatric, geriatric

## Major Guideline Sources

### ACR (American College of Radiology)
- Appropriateness Criteria (200+ scenarios)
- BI-RADS Atlas (mammography)
- LI-RADS (liver imaging)
- PI-RADS (prostate)
- TI-RADS (thyroid)
- Dose Reference Levels

### Society Guidelines
- RSNA (Radiological Society of North America)
- ESR (European Society of Radiology)
- ASNR (American Society of Neuroradiology)
- SPR (Society for Pediatric Radiology)
- SRU (Society of Radiologists in Ultrasound)

## Appropriateness Rating Scale

| Rating | Meaning |
|--------|---------|
| Usually Appropriate | 7-9 |
| May Be Appropriate | 4-6 |
| Usually Not Appropriate | 1-3 |

## Output Format

Returns structured JSON with:
- Guideline source and version
- Relevant rating or recommendation
- Clinical context
- Alternative considerations
- Evidence level (if available)

## Usage Examples

```
guideline_type: appropriateness
clinical_scenario: acute flank pain suspected kidney stone
modality: CT

guideline_type: reporting
clinical_scenario: liver imaging surveillance
```

## Integration

Links to:
- structured-reporting for template integration
- ai-detection-pipeline for protocol recommendations
- radiology-context for institution-specific protocols
