# ITK-SNAP Integration

Manual segmentation tool for radiology imaging.

## Installation

```bash
pip install itksnap-wrappers
# Or download from https://www.itksnap.org
```

## Python Integration

### 3D Slicer Compatible
```python
import SimpleITK as sitk

# Load image
reader = sitk.ImageFileReader()
reader.SetFileName('ct.nrrd')
image = reader.Execute()

# Convert for ITK-SNAP export
sitk.WriteImage(image, 'ct_for_labeling.nrrd')
```

### Label Statistics
```python
import numpy as np

def label_stats(label_image, original_image):
    """Calculate statistics per label."""
    labels = np.unique(label_image)
    stats = []
    
    for label in labels:
        mask = label_image == label
        intensity = original_image[mask]
        stats.append({
            'label': label,
            'count': mask.sum(),
            'mean': intensity.mean(),
            'std': intensity.std(),
            'volume': mask.sum() * voxel_volume
        })
    return stats
```

## Command Line
```bash
# Batch processing
itksnap -nt -l labels.nii.gz -i ct.nii.gz -o output

# Auto-segmentation
itksnap -autosegmentation AI -i input.nii.gz
```

## Integration Workflow

```python
def segmentation_pipeline(ct_path, organ='liver'):
    """ITK-SNAP enhanced segmentation workflow."""
    import subprocess
    
    # Preprocess
    preprocess(ct_path)
    
    # Launch ITK-SNAP for manual refinement
    subprocess.run(['itksnap', '-l', f'{organ}_initial.nii.gz', 
                    '-i', ct_path])
    
    # Load refined labels
    refined = sitk.ReadImage(f'{organ}_refined.nii.gz')
    
    # Calculate volume
    stats = label_stats(refined, sitk.ReadImage(ct_path))
    
    return refined, stats
```

## Tool Registration

```json
{
  "name": "itksnap",
  "description": "ITK-SNAP manual segmentation tool integration",
  "category": "visualization",
  "endpoints": ["manual_segmentation", "label_stats", "batch_processing"]
}
```
