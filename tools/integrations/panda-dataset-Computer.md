# PANDA (Prostate Cancer Grade Assessment) Dataset

Whole-slide histopathology images for prostate cancer grading.

## Connection

```yaml
base_url: https://www.kaggle.com/c/prostate-cancer-grade-assessment/data
tcga_url: https://portal.gdc.cancer.gov
```

## Dataset Details

- **Task**: Gleason grading classification
- **Images**: ~10,616 whole-slide images
- **Resolution**: Various (typically 10-40x)
- **Annotations**: Gleason grade groups (1-5)
- **Format**: TIF, PNG (converted)

## Download

```bash
# Via Kaggle API
kaggle competitions download -c prostate-cancer-grade-assessment

# Via The Cancer Imaging Archive (TCIA)
# Download from: https://doi.org/10.7937/tcia.9ba4-8d65
```

## Label Distribution

| Grade Group | Gleason Score | Description |
|-------------|---------------|-------------|
| 1 | ≤6 | Low risk |
| 2 | 3+4 | Intermediate favorable |
| 3 | 4+3 | Intermediate unfavorable |
| 4 | 8 | High risk |
| 5 | 9-10 | Highest risk |

## Preprocessing

```python
from openslide import OpenSlide
from PIL import Image

def extract_patch(slide_path, x, y, size=512):
    """Extract patch from whole-slide image."""
    slide = OpenSlide(slide_path)
    level = min(3, slide.level_count - 1)  # Downsample if needed
    patch = slide.read_region((x, y), level, (size, size))
    return patch

def tissue_mask(slide_path):
    """Generate tissue region mask."""
    # Extract RGB and threshold for tissue
    pass
```

## Limitations

- Whole-slide images very large (>1GB each)
- Requires specialized libraries (openslide, libvips)
- Color normalization needed across labs

## Citation

```
Bulten, W. et al. (2022). Automated Gleason grading of 
prostate cancer using deep learning and histopathology. 
Scientific Reports, 12, 3382.
```

## Tool Registration

```json
{
  "name": "panda_dataset",
  "description": "PANDA prostate cancer grading histopathology dataset",
  "category": "dataset",
  "endpoints": ["dataset_download", "slide_loading", "patch_extraction"]
}
```
