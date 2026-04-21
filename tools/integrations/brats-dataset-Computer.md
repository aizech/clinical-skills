# BraTS Dataset Integration

Multi-institutional brain tumor MRI segmentation dataset.

## Connection

```yaml
base_url: https://www.synapse.org
tcga_url: https://portal.gdc.cancer.gov
```

## Dataset Variants

### BraTS 2023/2024
- **Task**: Glioma segmentation (WT, TC, ET)
- **Modalities**: T1, T1ce, T2, FLAIR
- **Annotations**: Whole tumor, tumor core, enhancing tumor
- **Size**: ~1,250 subjects training

### BraTS Pediatric
- **Population**: Children (pediatric tumors)
- **Annotations**: Same as adult

### BraTS-OS
- **Task**: Overall survival prediction
- **Includes**: Clinical data + imaging

## Data Format

NIfTI files (.nii.gz):
```
BraTS2023_Training_001/
├── BraTS2023_Training_001_t1.nii.gz
├── BraTS2023_Training_001_t1ce.nii.gz
├── BraTS2023_Training_001_t2.nii.gz
├── BraTS2023_Training_001_flair.nii.gz
├── BraTS2023_Training_001_seg.nii.gz  # Labels
```

## Label Encoding

| Value | Label |
|-------|-------|
| 0 | Background |
| 1 | Necrotic/Core |
| 2 | Edema |
| 4 | Enhancing Tumor |

### Combined Labels
- **Whole Tumor (WT)**: 1 + 2 + 4
- **Tumor Core (TC)**: 1 + 4
- **Enhancing Tumor (ET)**: 4

## Key Operations

### Download
```bash
# Via Synapse
pip install synapseclient
synapse login -u {user} -p {pass}
synapse get syn51336643

# Via TCIA
wget "https://www.cancerimagingarchive.net/collections/{collection}/"
```

### Preprocessing
```python
import nibabel as nib
import numpy as np

def load_brats(path):
    t1 = nib.load(f'{path}_t1.nii.gz')
    t1ce = nib.load(f'{path}_t1ce.nii.gz')
    t2 = nib.load(f'{path}_t2.nii.gz')
    flair = nib.load(f'{path}_flair.nii.gz')
    seg = nib.load(f'{path}_seg.nii.gz')
    
    return {
        't1': t1.get_fdata(),
        't1ce': t1ce.get_fdata(),
        't2': t2.get_fdata(),
        'flair': flair.get_fdata(),
        'seg': seg.get_fdata()
    }
```

### Normalization
```python
def normalize(volume):
    # Clip to percentile
    p99 = np.percentile(volume, 99)
    volume = np.clip(volume, 0, p99)
    
    # Z-score per modality
    mean = volume.mean()
    std = volume.std()
    return (volume - mean) / (std + 1e-8)
```

## Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Dice (WT) | 2×TP/(2×TP+FP+FN) | >0.90 |
| Dice (TC) | | >0.80 |
| Dice (ET) | | >0.75 |
| HD95 | 95th percentile Hausdorff | <10mm |

## Tool Registration

```json
{
  "name": "brats_dataset",
  "description": "BraTS brain tumor MRI segmentation dataset",
  "category": "dataset",
  "endpoints": ["dataset_download", "nifti_loading", "preprocessing", "metrics"]
}
```
