# Medical Open Network for AI (MONAI) Integration

PyTorch-based framework for medical imaging AI.

## Core Components

### Transforms
```python
from monai.transforms import (
    LoadImage, EnsureChannelFirst, ScaleIntensity,
    RandRotate, RandZoom, ToTensor, Compose
)

train_transform = Compose([
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
from monai.networks.nets import DenseNet121, UNet, SegResNet

# Classification
model = DenseNet121(spatial_dims=2, in_channels=3, out_classes=14)

# Segmentation  
model = UNet(
    spatial_dims=3,
    in_channels=1,
    out_channels=2,
    channels=(32, 64, 128, 256),
    strides=(2, 2, 2)
)
```

### Data Loading
```python
from monai.data import CacheDataset, DataLoader, decollate_batch

dataset = CacheDataset(data=train_files, transform=train_transform)
loader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)
```

## Model Training
```python
from monai.engines import SupervisedTrainer

trainer = SupervisedTrainer(
    device="cuda",
    max_epochs=100,
    train_data_loader=loader,
    network=model,
    optimizer=optim.Adam(model.parameters(), lr=1e-4),
    loss_function=loss
)
trainer.run()
```

## Inference
```python
from monai.inferers import SlidingWindowInferrer

inferer = SlidingWindowInferrer(roi_size=(128, 128, 64), sw_batch_size=2)
pred = inferer(inputs, model)
```

## Pretrained Models
```python
from monai.apps import download_model

model_path = download_model("whole_body_ct_segmentation_v0.1")
```

## Tool Registration

```json
{
  "name": "monai",
  "description": "MONAI medical imaging deep learning framework",
  "category": "ai_framework",
  "endpoints": ["transforms", "networks", "training", "inference", "pretrained"]
}
```
