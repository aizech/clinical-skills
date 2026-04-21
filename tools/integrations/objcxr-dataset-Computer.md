# OBX-CXR (Pneumothorax) Dataset

Chest X-rays with pneumothorax bounding boxes for detection.

## Connection

```yaml
base_url: https://www.kaggle.com/c/siim-acr-pneumothorax-segmentation/data
```

## Dataset Details

- **Task**: Pneumothorax detection and segmentation
- **Images**: ~12,000 chest X-rays (DICOM)
- **Annotations**: Pixel-level segmentation masks + bounding boxes
- **Source**: SIIM-FISABIO-RSNA (RSNA/SIIM competition)
- **Format**: DICOM + RLE-encoded masks

## Download

```bash
# Via Kaggle API
kaggle competitions download -c siim-acr-pneumothorax-segmentation

# Extract
unzip siim-acr-pneumothorax-segmentation.zip -d objcxr/
```

## Data Structure

```
objcxr/
├── train/
│   ├── dicom_train/
│   │   ├── 1.2.826.0.1.3680043.10644.dcm
│   │   └── ...
│   └── rle/
│       ├── 1.2.826.0.1.3680043.10644.png  # RLE-encoded mask
│       └── ...
└── test/
    └── dicom_test/
```

## RLE Mask Encoding

```python
import numpy as np

def rle_decode(rle_string, shape):
    """Decode RLE string to binary mask."""
    if pd.isna(rle_string) or rle_string == '-1':
        return np.zeros(shape, dtype=np.uint8)
    
    s = rle_string.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    
    mask = np.zeros(shape[0] * shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        mask[lo:hi] = 1
    
    return mask.reshape(shape, order='F')

def rle_encode(mask):
    """Encode binary mask to RLE string."""
    pixels = mask.T.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)
```

## Detection Format

Bounding boxes extracted from segmentation:
```python
def mask_to_bbox(mask):
    """Convert binary mask to bounding box [x, y, width, height]."""
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return None
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return [cmin, rmin, cmax - cmin, rmax - rmin]
```

## Citation

```
SIIM-FISABIO-RSNA. (2019). SIIM-ACR Pneumothorax Segmentation. 
Kaggle Competition.
```

## Tool Registration

```json
{
  "name": "objcxr_dataset",
  "description": "SIIM-ACR pneumothorax chest X-ray detection dataset",
  "category": "dataset",
  "endpoints": ["dataset_download", "rle_decoding", "bbox_extraction"]
}
```
