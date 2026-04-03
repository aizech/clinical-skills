# Radiology Research Skill

Access and synthesize medical imaging research literature.

## Triggers

- "recent research on"
- "literature review"
- "published studies"
- "evidence for"
- "systematic review"
- "clinical trials"
- "accuracy metrics"
- "what does the evidence say"

## Parameters

- `research_type` (required): Type of research query
  - `recent_papers` - Latest publications
  - `evidence_summary` - Synthesized evidence
  - `accuracy_metrics` - Performance benchmarks
  - `guidelines_review` - Professional society guidelines
  - `clinical_trials` - Ongoing trials
  - `systematic_review` - Comprehensive literature review
- `topic` (required): Research topic or clinical question
- `time_range` (optional): Publication date filter (e.g., last 2 years)
- `modality` (optional): Specific imaging modality

## Research Quality Levels

| Level | Evidence Type |
|-------|--------------|
| 1 | Randomized controlled trials, meta-analyses |
| 2 | Cohort studies, case-control |
| 3 | Case series, expert opinion |
| 4 | Anecdotal reports |

## Key Research Areas

### AI/ML in Radiology
- Diagnostic accuracy studies
- Performance benchmarking
- External validation results
- Clinical implementation outcomes

### Imaging Techniques
- Protocol optimization
- New sequence development
- Contrast agent innovations
- Dose reduction techniques

### Clinical Applications
- Screening effectiveness
- Diagnostic accuracy by condition
- Treatment monitoring
- Prognostic imaging markers

## Literature Sources

- PubMed/MEDLINE (primary)
- RSNA Radiology (journal)
- Academic Radiology (journal)
- European Radiology (journal)
- arXiv (preprints)
- ClinicalTrials.gov (trials)

## Output Format

Returns structured JSON with:
- Citation list with relevance scores
- Key findings summary
- Accuracy metrics (sensitivity, specificity, AUC)
- Study quality indicators
- Clinical applicability notes

## Usage Examples

```
research_type: recent_papers
topic: deep learning chest X-ray pneumonia
time_range: last_2_years

research_type: evidence_summary
topic: MRI vs CT for appendicitis diagnosis
modality: CT, MRI
```

## Integration

Links to:
- pubmed-search for detailed literature access
- guideline-integration for society recommendations
- cross-reference-linking for related cases
