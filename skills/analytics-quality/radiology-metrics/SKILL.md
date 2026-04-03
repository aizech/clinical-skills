# Radiology Metrics Skill

Retrieves and analyzes operational metrics from radiology information systems.

## Triggers

- "radiology KPIs"
- "productivity metrics"
- "turnaround time analysis"
- "workload distribution"
- "RVU tracking"
- "department dashboard"
- "volume forecasting"

## Parameters

- `metric_type` (required): Type of metrics to retrieve
  - `turnaround_time` - Report TAT analysis
  - `productivity` - Studies per radiologist, modality counts
  - `utilization` - Equipment and room utilization rates
  - `quality` - Accuracy, discrepancy, critical result rates
  - `financial` - RVUs, revenue, cost per study
  - `volume` - Historical and forecasted volumes
- `time_range` (optional): Analysis period - defaults to last 30 days
- `group_by` (optional): Segmentation - radiologist, modality, location, urgency
- `compare_previous` (optional): Include period-over-period comparison

## Data Sources

- RIS (Radiology Information System) for report data
- PACS for study volumes and workflow timestamps
- Scheduler for utilization and capacity data
- Historical databases for trend analysis

## Output Format

Returns structured JSON with:
- Primary metrics (requested type)
- Trend indicators (vs. previous period)
- Benchmark comparisons where available
- Anomaly alerts for statistical outliers
- Recommended actions for improvement areas

## Usage Examples

```
metric_type: turnaround_time
time_range: last_month
group_by: [modality, urgency]

metric_type: productivity
time_range: last_quarter
compare_previous: true
```

## Error Handling

- Missing RIS data: Report partial results with data gap indicators
- Insufficient history: Expand time range suggestion
- Permission denied: Request escalated access with justification
