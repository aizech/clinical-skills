# CheXpert Dataset Integration

Stanford CheXpert chest X-ray dataset access.

## Connection

```yaml
base_url: https://compute.aimi.stanford.edu
dataset_path: /CheXpert-v1.0/
```

## Authentication

Stanford AIMI credentialed access:
```bash
# Download access requires:
# 1. AIMI account
# 2. CheXpert data use agreement
# 3. CITI data training completion

export CHEXPERT_USER={username}
export CHEXPERT_PASS={password}
```

## Dataset Structure

```
CheXpert-v1.0/
├── train.csv          # Training labels
├── valid.csv          # Validation set
├── train/             # Training images
│   ├── patient00001/
│   │   ├── study1/
│   │   │   └── 00000000.dcm
├── valid/             # Validation images
└── Stanford_chest_x_ray_phenotypes.csv
```

## Label Format

```csv
Path,Patient Age,Sex,AP/PA,Lateral,Frontal,Enlarged Cardiomediastinum,Cardiomegaly,...
CheXpert-v1.0/train/patient00001/study1/00000000.dcm,68,M,AP,,1,1.0,0.0,0.0,...
```

## Label Values

| Value | Meaning |
|-------|---------|
| 0.0 | Negative |
| 1.0 | Positive |
| -1.0 | Uncertain |
| blank | Not mentioned |

## Conditions (Labels)

- Support Devices
- No Finding
- Enlarged Cardiomediastinum
- Cardiomegaly
- Lung Opacity
- Lung Lesion
- Edema
- Consolidation
- Pneumonia
- Atelectasis
- Pneumothorax
- Pleural Effusion
- Pleural Other
- Fracture
- Observer

## Key Operations

### Download via API
```bash
# List available files
curl -X GET https://api.aimi.stanford.edu/v1/datasets \
  -H "Authorization: Bearer {token}"

# Download images
curl -X GET "https://api.aimi.stanford.edu/v1/download" \
  -o CheXpert.zip
```

### Label Processing
```python
import pandas as pd

df = pd.read_csv('train.csv')

# Filter uncertain labels
df['Pneumonia'] = df['Pneumonia'].replace(-1.0, float('nan'))

# Convert to binary
df['Pneumonia_binary'] = df['Pneumonia'].fillna(0).astype(int)
```

## Model Training

```python
# Common approach
import torchxrayvision as xrv

model = xrv.models.DenseNet(weights="all")
```

## Citation

```
Irvin, J., Rajpurkar, P., Ko, M., et al. (2019). 
CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels 
and Expert Competition. arXiv.
```

## Tool Registration

```json
{
  "name": "chexpert_dataset",
  "description": "CheXpert chest X-ray dataset access and processing",
  "category": "dataset",
  "endpoints": ["dataset_access", "labels_processing", "uncertainty_handling"]
}
```
