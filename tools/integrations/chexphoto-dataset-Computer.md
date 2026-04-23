# CheXphoto Dataset

Chest X-ray augmentation dataset with synthetic transformations.

## Connection

```yaml
base_url: https://aimi.stanford.edu
dataset_path: /CheXpert-v1.0-small/CheXphoto-v1.0/
```

## Dataset Details

- **Task**: Domain adaptation, augmentation research
- **Images**: ~65,000 image pairs (original + synthetic)
- **Transformations**: Synthetically degraded images from CheXpert
- **Use Case**: Model robustness to different acquisition conditions

## Dataset Structure

```
CheXphoto-v1.0/
├── train/
│   ├── synthetic/
│   │   └── 00000000_synthetic.jpg
│   └── original/
│       └── 00000000.jpg
├── valid/
│   └── ...
└── chexphoto.csv  # Pair mappings
```

## CSV Format

```csv
Image Index,View Position,synthetic_file,original_file
00000001,PA,00000001_synthetic.jpg,00000001.jpg
```

## Download

```bash
# Via Stanford AIMI
# Register at https://aimi.stanford.edu
# Download CheXphoto-v1.0.zip

wget https://api.aimi.stanford.edu/v1/download/CheXphoto-v1.0.zip
```

## Transformations Applied

| Type | Description |
|------|-------------|
| Brightness | ±20% intensity variation |
| Contrast | Low/high contrast simulation |
| Noise | Gaussian and Poisson noise |
| Blur | Motion and Gaussian blur |
| Artifact | Grid lines, overlay simulation |

## Loading Pairs

```python
import pandas as pd
from PIL import Image

def load_chexphoto_pairs(csv_path, base_dir):
    """Load original/synthetic image pairs."""
    df = pd.read_csv(csv_path)
    
    pairs = []
    for _, row in df.iterrows():
        original = Image.open(f"{base_dir}/original/{row['original_file']}")
        synthetic = Image.open(f"{base_dir}/synthetic/{row['synthetic_file']}")
        pairs.append((original, synthetic))
    
    return pairs
```

## Use Cases

1. **Domain Adaptation**: Train on synthetic, test on real
2. **Robustness Training**: Multi-domain training
3. **Image Enhancement**: Learn restoration from degraded
4. **Data Augmentation**: Increase effective dataset size

## Citation

```
Irvin, J. et al. (2019). CheXpert and CheXphoto Datasets.
Stanford AI Lab.
```

## Tool Registration

```json
{
  "name": "chexphoto_dataset",
  "description": "CheXphoto synthetic chest X-ray augmentation pairs",
  "category": "dataset",
  "endpoints": ["dataset_download", "pair_loading", "augmentation"]
}
```
