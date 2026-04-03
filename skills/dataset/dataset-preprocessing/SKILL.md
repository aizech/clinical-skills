---
name: dataset-preprocessing
description: Provides preprocessing pipelines and techniques for radiology datasets used in AI development. Use when user mentions "preprocess radiology data", "DICOM preprocessing", "image normalization", "data augmentation", or needs to prepare datasets.
---

# Dataset Preprocessing Skill

## Triggers

- "preprocess radiology data"
- "DICOM preprocessing"
- "image normalization"
- "data augmentation"
- "quality control pipeline"
- "mask generation"
- "multi-site harmonization"
- "training data preparation"

## Parameters

- `input_format` (required): Source data format
  - `dicom` - DICOM files
  - `nifti` - NIfTI volumes
  - `metadata` - Header/excel data
  - `mixed` - Multiple formats
- `task_type` (required): Downstream ML task
  - `detection` - Object/bounding box detection
  - `segmentation` - Pixel-level segmentation
  - `classification` - Image classification
  - `regression` - Continuous value prediction
- `modality` (optional): Imaging modality
- `multi_vendor` (optional): Boolean for multi-site/multi-vendor data
- `dataset_scale` (optional): Small (<1K), medium (1K-100K), large (>100K)

## Preprocessing Components

### Image Processing
- Intensity normalization (z-score, min-max, percentile-based)
- Windowing/leveling for CT/MRI
- Resampling to isotropic voxel size
- Brain extraction (skull stripping)
- Bias field correction for MRI

### Quality Control
- Automated quality scoring
- Artifact detection
- Contrast-to-noise ratio
- Resolution verification
- Human-in-the-loop review for edge cases

### Augmentation
- Geometric: rotation, flip, scale, elastic deformation
- Intensity: noise, contrast, brightness
- Modality-specific: CT windowing variants, MRI sequence mixing
- Generative: synthetic data augmentation

### Format Conversion
- DICOM to NumPy/PyTorch/TensorFlow
- DICOM to NIfTI for volumetric data
- Annotation format conversion (CSV, COCO, YOLO, Pascal VOC)

## Output Format

Returns structured JSON with:
- Processing pipeline steps
- Code snippets for each transformation
- Validation checks and statistics
- Expected output specifications
- Common pitfalls and mitigations

## Usage Examples

```
input_format: dicom
task_type: detection
modality: CT
multi_vendor: true

input_format: nifti
task_type: segmentation
dataset_scale: large
```
