# End-to-End Workflow Examples

This document provides complete, runnable examples of common radiology workflows using clinical-skills tools and integrations.

## Workflow 1: PACS Query and Report Analysis

**Use Case:** Query a DICOMweb PACS for recent CT studies, analyze radiology reports for findings, and generate a summary.

### Prerequisites

- DICOMweb server accessible at `https://pacs.example.com/dicomweb`
- API token for authentication stored in `PACS_TOKEN` environment variable

### Steps

```bash
# 1. Search for recent CT studies from the last 30 days
python tools/clis/dicom_qido.py \
  https://pacs.example.com/dicomweb \
  --modality CT \
  --date $(date -d "30 days ago" +%Y%m%d)-$(date +%Y%m%d) \
  --token $PACS_TOKEN \
  --json > studies.json

# 2. Extract study UIDs for detailed analysis
jq -r '.[].["0020000D"].Value[0]' studies.json > study_uids.txt

# 3. Get detailed metadata for each study
while read uid; do
  python tools/clis/dicom_qido.py \
    https://pacs.example.com/dicomweb \
    --study-uid "$uid" \
    --token $PACS_TOKEN \
    --json >> study_details.json
done < study_uids.txt

# 4. Load radiology-context skill for AI agent analysis
# (This would be done in your AI agent workflow)
```

### Expected Output

```json
{
  "0020000D": {"Value": ["1.2.3.4.5"]},
  "00100020": {"Value": ["PATIENT001"]},
  "00100010": {"Value": [{"Alphabetic": "John Smith"}]},
  "00080020": {"Value": ["20240403"]},
  "00080061": {"Value": ["CT"]}
}
```

## Workflow 2: Literature Search for Clinical Decision Support

**Use Case:** Search PubMed for recent literature on lung nodule classification and summarize findings.

### Prerequisites

- NCBI API key (optional, increases rate limits) stored in `NCBI_API_KEY`
- Internet connectivity

### Steps

```bash
# 1. Search for lung nodule classification articles from last 90 days
python tools/clis/pubmed_search.py \
  "lung nodule classification AI deep learning" \
  --days 90 \
  --type clinical-trial \
  --max 20 \
  --json > articles.json

# 2. Fetch article summaries
jq -r '.[].pmid' articles.json > pmids.txt

# 3. Get detailed summaries for each article
python tools/clis/pubmed_search.py \
  "lung nodule classification AI deep learning" \
  --max 20 \
  --json > article_summaries.json

# 4. Filter for high-impact journals
jq '[.[] | select(.journal | test("Radiology|Lancet|NEJM|JAMA"))]' \
  article_summaries.json > high_impact.json

# 5. Display results
jq -r '.[] | "\(.title)\n\(.journal) (\(.pub_date))\nDOI: \(.doi)\n"' \
  high_impact.json
```

### Expected Output

```
Deep learning for lung nodule classification in CT scans
Radiology (2024-03-15)
DOI: 10.1148/radiol.2024234567
```

## Workflow 3: Quality Metrics Generation and Analysis

**Use Case:** Generate radiology productivity metrics for a specific time period and analyze trends.

### Steps

```bash
# 1. Generate metrics for Q1 2024
python tools/clis/radiology_metrics.py \
  --start-date 2024-01-01 \
  --end-date 2024-03-31 \
  --json > q1_2024_metrics.json

# 2. Generate metrics for Q2 2024
python tools/clis/radiology_metrics.py \
  --start-date 2024-04-01 \
  --end-date 2024-06-30 \
  --json > q2_2024_metrics.json

# 3. Compare metrics between quarters
jq -s '{
  q1: .[0],
  q2: .[1],
  change: {
    studies: (.[1].total_studies - .[0].total_studies),
    reports: (.[1].total_reports - .[0].total_reports),
    turnaround_avg: (.[1].avg_turnaround - .[0].avg_turnaround)
  }
}' q1_2024_metrics.json q2_2024_metrics.json > comparison.json

# 4. Display comparison
jq '.' comparison.json
```

### Expected Output

```json
{
  "q1": {
    "total_studies": 1250,
    "total_reports": 1180,
    "avg_turnaround": 4.5
  },
  "q2": {
    "total_studies": 1320,
    "total_reports": 1280,
    "avg_turnaround": 4.2
  },
  "change": {
    "studies": 70,
    "reports": 100,
    "turnaround_avg": -0.3
  }
}
```

## Workflow 4: Multi-Platform Dataset Analysis

**Use Case:** Query multiple public datasets for chest X-ray images and prepare for AI model training.

### Prerequisites

- Access to NIH ChestX-ray14, CheXpert, and MIMIC-CXR datasets
- Sufficient storage for downloaded images

### Steps

```bash
# 1. Query NIH ChestX-ray14 dataset metadata
# (Refer to tools/integrations/nih-chestxray14.md for specific API calls)

# 2. Query CheXpert dataset metadata
# (Refer to tools/integrations/chexpert.md for specific API calls)

# 3. Query MIMIC-CXR dataset metadata
# (Refer to tools/integrations/physionet-mimic.md for specific API calls)

# 4. Combine metadata and deduplicate by patient ID
jq -s 'flatten | unique_by(.patient_id)' \
  nih_metadata.json chexpert_metadata.json mimic_metadata.json \
  > combined_metadata.json

# 5. Filter for frontal view images only
jq '[.[] | select(.view_position == "Frontal")]' \
  combined_metadata.json > frontal_only.json

# 6. Generate statistics
jq '{
  total_images: length,
  patients: [.[] | .patient_id] | unique | length,
  views: [.[] | .view_position] | group_by(.) | map({view: .[0], count: length}),
  labels: [.[] | .findings] | flatten | group_by(.) | map({label: .[0], count: length})
}' frontal_only.json
```

## Workflow 5: AI Model Integration with DICOMweb

**Use Case:** Deploy an AI detection model as a DICOMweb service and integrate with PACS.

### Prerequisites

- AI model containerized with DICOMweb interface
- Orthanc or compatible PACS server
- Network connectivity between components

### Architecture

```
PACS (Orthanc) ←→ AI Model (DICOMweb) ←→ Monitoring
```

### Steps

```bash
# 1. Configure AI model as DICOMweb service
# (Model should expose QIDO-RS, WADO-RS, STOW-RS endpoints)

# 2. Register AI model with PACS
curl -X POST http://orthanc:8042/modalities/ai-model \
  -H "Content-Type: application/json" \
  -d '{
    "AET": "AI-MODEL",
    "Host": "ai-model.example.com",
    "Port": 8080
  }'

# 3. Test connectivity
python tools/clis/dicom_qido.py \
  http://ai-model.example.com:8080/dicomweb \
  --modality CT

# 4. Create automated pipeline
# (This would typically be a script or workflow engine task)

# 5. Monitor AI model performance
# (Use radiology-metrics tool to track detection rates)
```

## Workflow 6: Clinical Documentation Automation

**Use Case:** Automatically generate structured radiology reports from unstructured free text.

### Prerequisites

- Load `clinical-documentation/radiology-report-analysis` skill
- Sample radiology reports in text format

### Steps

```bash
# 1. Load radiology-context skill for domain knowledge
# (Done by AI agent)

# 2. Process unstructured report
report_text=$(cat sample_report.txt)

# 3. Use AI agent with radiology-report-analysis skill
# (This would be done in your AI agent workflow)
# The skill will extract:
# - Findings
# - Impressions
# - Measurements
# - Anatomy
# - Critical findings
# - Incidental findings

# 4. Validate extracted information
# (Manual review or automated checks)

# 5. Generate structured output
# (Output format depends on your EHR integration requirements)
```

### Example Input

```
CT CHEST WITH CONTRAST:
Findings: 1.5 cm nodule in right upper lobe. No pleural effusion.
Impression: Right upper lobe nodule, recommend follow-up.
```

### Example Output

```json
{
  "findings": ["1.5 cm nodule in right upper lobe", "No pleural effusion"],
  "impressions": ["Right upper lobe nodule, recommend follow-up"],
  "measurements": [{"location": "RUL", "value": "1.5 cm", "type": "nodule"}],
  "anatomy": ["chest", "lungs", "pleura"],
  "critical_findings": [],
  "incidental_findings": []
}
```

## Workflow 7: Security Baseline Audit

**Use Case:** Run security baseline check on all skills and integrations to ensure compliance.

### Steps

```bash
# 1. Run security baseline check
node .github/scripts/security-baseline.js security-report.json

# 2. Review report
cat security-report.json | jq '.summary'

# 3. Check for any issues
cat security-report.json | jq '.skills[] | select(.securityStatus != "pass")'

# 4. Fix any identified issues
# (Common fixes: remove secrets, add proper frontmatter, fix broken links)

# 5. Re-run validation
./scripts/validate-skills.sh

# 6. Commit fixes
git add .
git commit -m "fix: address security baseline findings"
```

## Workflow 8: Skill Development and Testing

**Use Case:** Create a new skill following TDD principles and validate it.

### Steps

```bash
# 1. Create skill directory
mkdir -p skills/new-category/new-skill/evals

# 2. Write test cases first (TDD)
cat > skills/new-category/new-skill/evals/evals.json << EOF
{
  "tests": [
    {
      "input": "test input",
      "expected_output": "expected output"
    }
  ]
}
EOF

# 3. Create SKILL.md with proper frontmatter
cat > skills/new-category/new-skill/SKILL.md << EOF
---
name: new-skill
description: What this skill does and when to use it. Include trigger phrases like 'when', 'mention', 'use'.
---

# Skill Content

(Keep under 500 lines, move details to references/)
EOF

# 4. Validate the skill
./scripts/validate-skills.sh

# 5. Run security baseline check
node .github/scripts/security-baseline.js security-report.json

# 6. Commit and submit PR
git add skills/new-category/new-skill
git commit -m "feat: add new-skill for [use case]"
```

## Tips and Best Practices

1. **Always use environment variables** for secrets and API keys
2. **Validate JSON outputs** before piping to other tools
3. **Use `--json` flag** for programmatic consumption of CLI outputs
4. **Rate limit API calls** when working with external services
5. **Test workflows locally** before deploying to production
6. **Keep SKILL.md under 500 lines** - move details to `references/`
7. **Write evals first** when creating new skills (TDD)
8. **Run validation scripts** before committing changes

## Troubleshooting

### Common Issues

**Connection timeouts:**
- Check network connectivity
- Increase timeout in CLI tools
- Verify API endpoint is accessible

**Authentication failures:**
- Verify environment variables are set
- Check API key/token validity
- Ensure correct auth method (Basic vs Bearer)

**JSON parsing errors:**
- Validate JSON output with `jq empty file.json`
- Check for incomplete responses
- Verify API is returning proper JSON

**Rate limiting:**
- Implement exponential backoff
- Use API keys for higher limits
- Cache results when possible

For more troubleshooting help, see [docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md).
