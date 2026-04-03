# Image Quality Audit Skill

Assesses medical image quality against clinical standards and identifies optimization opportunities.

## Triggers

- "image quality audit"
- "artifact review"
- "dose analysis"
- "protocol deviation"
- "quality metrics"
- "diagnostic adequacy"
- "technique optimization"

## Parameters

- `audit_type` (required): Type of quality assessment
  - `artifact` - Motion, noise, streak artifacts
  - `dose` - Radiation dose optimization and DRL compliance
  - `protocol` - Protocol adherence and deviation analysis
  - `adequacy` - Diagnostic sufficiency for intended purpose
  - `technique` - Technical parameters review
  - `comprehensive` - Full quality review
- `modality` (required): Imaging modality to audit
- `time_range` (optional): Audit period - defaults to last 7 days
- `sample_size` (optional): Studies to review - defaults to all in range
- `severity_threshold` (optional): Minimum severity to flag

## Evaluation Criteria

- **Artifacts**: Type, severity (1-5), impact on diagnostic utility
- **Dose**: DLP, CTDIvol vs. ACR reference levels, size-adjusted metrics
- **Protocol**: Coverage completeness, sequence selection, contrast timing
- **Adequacy**: Signal-to-noise, spatial resolution, positioning

## Output Format

Returns structured JSON with:
- Quality metrics summary
- Severity distribution
- Contributing factors analysis
- Improvement recommendations ranked by impact
- Training priorities for technologist/site issues

## Usage Examples

```
audit_type: artifact
modality: CT
time_range: last_week
severity_threshold: 3

audit_type: dose
modality: CT
time_range: last_month
```

## Standards Reference

- ACR Physical Parameters for CT, MRI, Ultrasound, Mammography
- ICRP and ACR dose reference levels
- modality-specific practice guidelines
