# MONAI Framework Integration

Medical Open Network for AI (PyTorch-based).

## Installation

```bash
pip install monai
```

## Core Components

### Transforms
```python
from monai.transforms import (
    LoadImage, EnsureChannelFirst, ScaleIntensity,
    RandRotate, RandZoom, ToTensor
)

transforms = Compose([
    LoadImage(image_only=True),
    EnsureChannelFirst(),
    ScaleIntensity(),
    RandRotate(range_x=15, prob=0.5),
    RandZoom(prob=0.3),
    ToTensor()
])
```

### Networks
```python
from monai.networks.nets import (
    ResNet, DenseNet121, EfficientNet,
    UNet, SegResNet, AttentionUnet
)

# Classification
model = DenseNet121(spatial_dims=2, in_channels=3, out_classes=14)

# Segmentation
model = UNet(
    spatial_dims=3,
    in_channels=1,
    out_channels=2,
    channels=(32, 64, 128, 256, 512),
    strides=(2, 2, 2, 2)
)
```

### Inference
```python
from monai.inferers import SlidingWindowInferrer

inferer = SlidingWindowInferrer(
    roi_size=(96, 96, 96),
    sw_batch_size=4,
    overlap=0.5
)

pred = inferer(inputs, model)
```

## Data Loading

```python
from monai.data import CacheDataset, DataLoader

dataset = CacheDataset(
    data=train_files,
    transform=train_transforms,
    cache_rate=0.8
)

loader = DataLoader(dataset, batch_size=4, num_workers=4)
```

## Metrics
```python
from monai.metrics import DiceMetric, MeanHarmonicDice

dice = DiceMetric(include_background=False, reduction="mean")
```

## Bundles

```python
from monai.apps import download_model

# Download pretrained model
model_path = download_model("wholeBody_ct_segmentation")
```

## Common Pipelines

| Task | Network | Loss |
|------|---------|------|
| Segmentation | UNet | Dice + CE |
| Classification | DenseNet | CrossEntropy |
| Detection | RetinaNet | Focal Loss |
| Reconstruction | Autoencoder3D | MSE |

## Tool Registration

```json
{
  "name": "monai_framework",
  "description": "MONAI medical imaging deep learning framework",
  "category": "ai_framework",
  "endpoints": ["transforms", "networks", "inference", "bundles"]
}
```
