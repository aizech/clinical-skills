---
name: report-quality-review
description: Monitors and improves radiology report quality through systematic audit and feedback. Use when user mentions "report quality review", "discrepancy audit", "report completeness", "addendum analysis", or needs quality assurance.
---

# Report Quality Review Skill

## Triggers

- "report quality review"
- "discrepancy audit"
- "report completeness"
- "addendum analysis"
- "quality improvement"
- "peer review"
- "report turnaround"

## Parameters

- `review_type` (required): Type of quality review
  - `completeness` - Required element adherence
  - `discrepancy` - Error and miss analysis
  - `turnaround` - TAT compliance monitoring
  - `communication` - Critical result documentation
  - `attribution` - Report signature verification
  - `cqi` - Continuous quality improvement tracking
- `modality` (optional): Filter by imaging type
- `time_range` (optional): Review period - defaults to last 30 days
- `urgency` (optional): Filter by clinical setting (ED, inpatient, outpatient)

## Quality Metrics Tracked

- **Completeness**: Required elements, comparison documentation, impression presence
- **Accuracy**: Discrepancy rates, addendum rates, amended findings
- **Timeliness**: TAT by setting, protocol compliance, pending report alerts
- **Communication**: Critical result documentation, escalation compliance
- **Format**: Structured data presence,标准化 terminology use

## Output Format

Returns structured JSON with:
- Quality score by metric category
- Trend analysis (improving/declining)
- Individual radiologist feedback (anonymized aggregates)
- Improvement recommendations
- Peer review learning points

## Usage Examples

```
review_type: completeness
modality: CT
time_range: last_month

review_type: discrepancy
time_range: last_quarter
urgency: ED
```

## Integration Points

- RIS for report content and timestamps
- PACS for comparison study tracking
- Communication logs for critical result verification
- Peer review system for discrepancy classification
