# LUNA16 Dataset Integration

Lung Nodule Analysis 2016 challenge dataset.

## Connection

```yaml
base_url: https://luna16.grand-challenge.org
api_url: https://luna16.aisnet.org
```

## Dataset Details

- **Task**: Pulmonary nodule detection in CT
- **Scans**: 888 low-dose CT scans
- **Annotations**: 1,186 nodules >=3mm diameter
- **Format**: MetaImage (.mhd/.raw) or DICOM

## Download

```bash
# Via LUNA16 website registration
wget https://luna16.grand-challenge.org/media/data/luna16.zip

# Extract
unzip luna16.zip -d luna16/
```

## Data Structure

```
luna16/
├── CSV/
│   ├── candidates_V2.csv     # All candidates (true + false positives)
│   └── annotations.csv       # Ground truth nodule centers
├── imgs/
│   └── subset0/
│       └── 1.3.6.1.4...mhd
└── subset1/ ... subset9/
```

## Annotation Format

### annotations.csv
```csv
seriesuid,coordX,coordY,coordZ,diameter_mm
1.3.6.1.4...,-53.36,-12.91,-87.53,4.24
```

### candidates.csv
```csv
seriesuid,coordX,coordY,coordZ,class,diameter_mm
1.3.6.1.4...,-53.36,-12.91,-87.53,1,4.24
1.3.6.1.4...,23.45,45.67,-98.12,0,3.12
```

## Loading Data
```python
import pandas as pd
import SimpleITK as sitk

def load_scan(series_uid, data_path):
    """Load CT scan and annotations."""
    # Load image
    img_path = f"{data_path}/imgs/{series_uid}.mhd"
    image = sitk.ReadImage(img_path)
    
    # Load annotations
    ann = pd.read_csv(f"{data_path}/CSV/annotations.csv")
    nodules = ann[ann.seriesuid == series_uid]
    
    return image, nodules
```

## Evaluation

### FROC Score
Free-response ROC (lesion-level sensitivity):
- 8 points per scan (average 1/8 FP/scan)
- 1/4, 1/2, 1, 2, 4, 8 FPs/scan

### CAMELYON Benchmark
```
# Calculate FROC
from luna16.evaluation import evaluate

froc, fps = evaluate(predictions, ground_truth)
print(f"CAMELYON17 AUC: {froc:.4f}")
```

## Citation

```
Setio, A. et al. (2017). Pulmonary Nodule Detection in CT Images: 
False Positive Reduction Using Multi-View Convolutional Networks. 
IEEE TMI, 35(5), 1160-1169.
```

## Tool Registration

```json
{
  "name": "luna16_dataset",
  "description": "LUNA16 lung nodule detection challenge dataset",
  "category": "dataset",
  "endpoints": ["dataset_download", "annotation_loading", "froc_evaluation"]
}
```
