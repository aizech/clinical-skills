# Model Validation Skill

Designs and executes validation studies for radiology AI models to ensure clinical reliability and regulatory compliance.

## Triggers

- "validate model performance"
- "external validation"
- "statistical analysis"
- "clinical validation"
- "model comparison"
- "regulatory submission"
- "performance benchmarking"
- "fairness audit"

## Parameters

- `validation_type` (required): Type of validation needed
  - `internal` - Retrospective internal dataset
  - `external` - Prospective/out-of-distribution testing
  - `prospective` - Clinical deployment study
  - `regulatory` - FDA/EMA submission prep
  - `fairness` - Subgroup disparity analysis
  - `comparison` - Head-to-head model comparison
- `model_task` (required): Model's intended use
  - `detection` - Sensitivity, specificity, PPV, NPV
  - `segmentation` - Dice, IoU, Hausdorff distance
  - `classification` - Accuracy, AUC, F1 score
  - `regression` - MAE, RMSE, correlation
- `modality` (optional): Imaging modality
- `regulatory_path` (optional): Target clearance pathway

## Validation Framework

### Performance Metrics
| Task | Primary Metrics | Secondary |
|------|-----------------|-----------|
| Detection | Sensitivity, Specificity, AUC | PPV, NPV, FROC |
| Segmentation | Dice, IoU | Hausdorff, ASD |
| Classification | Accuracy, AUC, F1 | Sensitivity, Specificity |
| Regression | MAE, RMSE | Correlation, Bland-Altman |

### Statistical Methods
- Confidence intervals (bootstrap, binominal)
- Significance testing (McNemar, DeLong for AUC)
- Power analysis for sample sizing
- Multiple comparison correction
- Subgroup interaction testing

### Regulatory Standards
- FDA 510(k) predicate comparison
- FDA De Novo requirements
- EU MDR clinical evaluation
- IMDRF clinical evidence framework
- ACR-SIIM AI performance standards

## Output Format

Returns structured JSON with:
- Validation protocol and methodology
- Required sample size with power analysis
- Statistical test selection and rationale
- Results template with standard metrics
- Interpretation guidelines
- Regulatory compliance checklist

## Usage Examples

```
validation_type: external
model_task: detection
modality: CT

validation_type: regulatory
model_task: classification
regulatory_path: 510k
```
