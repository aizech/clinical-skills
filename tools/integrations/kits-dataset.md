# KiTS (Kidney Tumor Segmentation) Dataset

Multi-phase CT kidney and tumor segmentation dataset.

## Connection

```yaml
base_url: https://kits19.sfo2.digitaloceanspaces.com
synapse_id: syn34940363
```

## Dataset Details

- **Task**: Kidney and tumor segmentation in CT
- **Cases**: 300 patients
- **Phases**: Non-contrast, arterial, venous
- **Annotations**: Kidney (class 1), tumor (class 2), cyst (class 3)
- **Format**: NIfTI (.nii.gz)

## Download

```bash
# Via Python package
pip install kits19

python -m kits19.generate_kits_data \
  --output_dir ./kits_data

# Direct download
wget https://kits19.sfo2.digitaloceanspaces.com/data/train_*.zip
```

## Data Structure

```
kits19/
├── case_00000/
│   ├── imaging.nii.gz      # Multi-phase CT
│   └── segmentation.nii.gz # Labels
├── case_00001/
└── ...
```

## Label Encoding

| Value | Structure |
|-------|-----------|
| 0 | Background |
| 1 | Kidney |
| 2 | Tumor |
| 3 | Cyst |

## Loading Data

```python
import nibabel as nib
import numpy as np

def load_case(case_id, data_dir):
    case_path = f"{data_dir}/case_{case_id:05d}"
    imaging = nib.load(f"{case_path}/imaging.nii.gz")
    segmentation = nib.load(f"{case_path}/segmentation.nii.gz")
    
    return imaging.get_fdata(), segmentation.get_fdata()
```

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Dice (Kidney) | Kidney segmentation accuracy |
| Dice (Tumor) | Tumor segmentation accuracy |
| Hausdorff95 | Boundary distance |

## Citation

```
Heller, N. et al. (2019). The KiTS19 Challenge Data: 
Kidney and Kidney Tumor Segmentation in CT Imaging. 
arXiv:1912.01076.
```

## Tool Registration

```json
{
  "name": "kits_dataset",
  "description": "KiTS kidney tumor segmentation dataset",
  "category": "dataset",
  "endpoints": ["dataset_download", "nifti_loading", "segmentation"]
}
```
