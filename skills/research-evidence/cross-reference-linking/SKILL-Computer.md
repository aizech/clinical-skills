---
name: cross-reference-linking
description: Links current findings to priors, related literature, and correlated data. Use when user mentions "compare to priors", "find prior studies", "correlate with", "longitudinal comparison", or needs historical context.
---

# Cross-Reference Linking Skill

## Triggers

- "compare to priors"
- "find prior studies"
- "correlate with"
- "longitudinal comparison"
- "followup from"
- "related findings"
- "pathology correlation"

## Parameters

- `reference_type` (required): Type of cross-reference needed
  - `prior_studies` - Historical imaging comparison
  - `literature` - Relevant published cases or studies
  - `followup` - Sequential study comparison
  - `multimodality` - Different modality correlation
  - `pathology` - Radiology-pathology correlation
  - `clinical` - EHR/clinical data correlation
- `finding_summary` (required): Current finding to cross-reference
- `patient_id` (optional): Patient identifier for prior search
- `date_range` (optional): Time window for prior search

## Cross-Reference Types

### Prior Study Comparison
- Modality, date, and key findings of historical studies
- Size/dimension comparisons for measurable findings
- Density/signal intensity comparisons
- Change assessment (stable, improved, progressed)

### Literature Correlation
- Similar published cases
- Expected imaging appearances
- Atypical presentations
- Prognostic implications

### Pathology Correlation
- Common pathologies for imaging appearance
- Staging implications (TNM, etc.)
- Molecular markers and imaging correlates
- Treatment response patterns

### Clinical Correlation
- Lab values relevant to imaging findings
- Symptoms and clinical history
- Treatment history and timeline

## Output Format

Returns structured JSON with:
- Prior finding references with dates
- Comparison metrics (size, characteristics)
- Change assessment with confidence
- Recommendations for followup
- Related literature citations

## Usage Examples

```
reference_type: prior_studies
finding_summary: 2.5 cm lung nodule right upper lobe
patient_id: MRN12345

reference_type: pathology
finding_summary: irregular spiculated mass left lower lobe

reference_type: followup
finding_summary: 1.2 cm thyroid nodule compared to 6 months prior
```

## Data Sources

- PACS for prior imaging studies
- RIS for structured reports
- EHR for clinical correlation
- Literature databases for research correlation
- Pathology system for radiology-pathology correlation
