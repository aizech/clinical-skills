# Radiology Dataset Guide Skill

Guides researchers and developers through radiology dataset selection, access, and utilization for AI development.

## Triggers

- "radiology dataset"
- "medical imaging data"
- "RSNA challenge"
- "MIMIC data access"
- "CheXpert download"
- "dataset comparison"
- "training data preparation"
- "public dataset"

## Parameters

- `task_type` (required): ML/AI task being solved
  - `detection` - Abnormality/nodule/cancer detection
  - `segmentation` - Organ or lesion segmentation
  - `classification` - Disease or finding classification
  - `reconstruction` - Image reconstruction/enhancement
  - `quantification` - Measurement and feature extraction
- `anatomy` (optional): Body region or organ system
- `modality` (optional): Imaging modality preference
- `access_requirements` (optional): Data use restrictions
- `commercial_use` (optional): Boolean for commercial application intent

## Dataset Inventory

| Dataset | Modality | Primary Task | Access | Annotations |
|---------|----------|---------------|--------|-------------|
| RSNA Bone Age | X-ray | Regression | Public | Age, quality |
| RSNA Pneumonia | Chest X-ray | Detection | Public | Bounding boxes |
| RSNA Brain Hemorrhage | CT | Detection | Public | Bounding boxes, type |
| NIH ChestX-ray14 | Chest X-ray | Classification | Public | Labels |
| CheXpert | Chest X-ray | Classification | Institutional | Labels |
| MIMIC-CXR | Chest X-ray | Multi | PhysioNet | Labels, reports |
| CheXphoto | Chest X-ray | Classification | Public | Synth/real pairs |
| LUNA16 | CT | Detection | Public | Nodule centers |
| KiTS | CT | Segmentation | Public | Kidney/tumor |
| BraTS | MRI | Segmentation | Research | Multi-modal seg |
| PANDA | Histology | Classification | Public | Biopsy grades |
| OBJ-CXR | Chest X-ray | Detection | Public | Bounding boxes |

## Output Format

Returns structured JSON with:
- Relevant datasets ranked by suitability
- Annotation quality and completeness
- Access procedure and requirements
- Key publications and benchmarks
- Preprocessing recommendations
- Compliance and ethics considerations

## Usage Examples

```
task_type: detection
anatomy: lung
modality: CT

task_type: classification
anatomy: chest
commercial_use: true
```
