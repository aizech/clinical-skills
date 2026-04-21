---
name: modality-detection
description: Auto-detect imaging modality (CT, MRI, X-ray, US, etc.) from user input, DICOM file headers, or file analysis. Also use when the user mentions "what modality", "detect from file", "identify imaging type", or needs to classify imaging studies. For PACS queries, see pacs-workflow.
---

# Modality Detection

You are a radiology modality detection expert. Your role is to accurately identify the imaging modality from various input formats.

## Modality Categories

### Primary Modalities

| Modality | Code | Description |
|----------|------|-------------|
| Computed Tomography | CT, CT-A | X-ray cross-sections, often with contrast |
| Magnetic Resonance Imaging | MR, MR-A | Magnetic field imaging, no radiation |
| Plain Radiography | CR, DX | Projectional X-ray images |
| Ultrasound | US | Sound wave imaging, no radiation |
| Mammography | MG | Breast imaging, specialized X-ray |
| Nuclear Medicine | NM, PT, PET | Radioactive tracer imaging |
| Fluoroscopy | RF | Real-time X-ray video |

### Hybrid/Advanced Modalities

| Modality | Code | Description |
|----------|------|-------------|
| PET/CT | PT/CT | Combined PET and CT |
| PET/MR | PT/MR | Combined PET and MRI |
| SPECT/CT | NM/CT | Combined SPECT and CT |
| CT Angiography | CTA | CT with arterial contrast timing |
| MR Angiography | MRA | MRI for vessel imaging |

### DICOM Modality Codes

Standard DICOM modality values:
- **CT**: Computed Tomography
- **MR**: Magnetic Resonance
- **DX**: Digital Radiography
- **CR**: Computed Radiography
- **US**: Ultrasound
- **MG**: Mammography
- **NM**: Nuclear Medicine
- **PT**: PET
- **RF**: Radio Fluoroscopy
- **XA**: X-Ray Angiography
- **OP**: Ophthalmic Photography
- **ES**: Endoscopy

## Detection Patterns

### From Text Input

Extract modality from clinical text using these patterns:

```python
def detect_modality(text):
    text_upper = text.upper()
    
    # Exact matches first
    if "PET/CT" in text_upper:
        return "PET/CT"
    if "CT ANGIOGRAPHY" in text_upper or "CTA" in text_upper:
        return "CTA"
    if "MR ANGIOGRAPHY" in text_upper or "MRA" in text_upper:
        return "MRA"
    if "DIGITAL MAMMOGRAPHY" in text_upper or "SCREENING MAMMO" in text_upper:
        return "Mammography"
    
    # Pattern matching
    if "CT " in text_upper or text_upper.startswith("CT"):
        return "CT"
    if "MRI " in text_upper or text_upper.startswith("MR ") or "MAGNETIC RESONANCE" in text_upper:
        return "MRI"
    if "X-RAY" in text_upper or "CHEST X" in text_upper or "DX " in text_upper:
        return "X-ray"
    if "ULTRASOUND" in text_upper or "SONOGRAPHY" in text_upper or "US " in text_upper:
        return "Ultrasound"
    if "MAMMO" in text_upper or "BREAST" in text_upper:
        return "Mammography"
    if "PET " in text_upper or "PET-" in text_upper:
        return "PET/CT"
    
    return None  # Unknown
```

### From DICOM Headers

Extract modality from DICOM file metadata:

```python
def detect_from_dicom(dicom_file):
    # Using pydicom
    import pydicom
    
    ds = pydicom.dcmread(dicom_file)
    
    modality = getattr(ds, 'Modality', None)
    body_part = getattr(ds, 'BodyPartExamined', None)
    series_desc = getattr(ds, 'SeriesDescription', None)
    
    return {
        'modality': modality,
        'body_part': body_part,
        'series_description': series_desc
    }
```

### Modality Mapping

Map DICOM codes to human-readable names:

| DICOM Code | Display Name | Category |
|------------|--------------|----------|
| CT | CT Scan | Tomography |
| MR | MRI | Tomography |
| DX | X-ray | Projection |
| CR | X-ray | Projection |
| US | Ultrasound | Ultrasound |
| MG | Mammography | Projection |
| PT | PET | Nuclear |
| NM | Nuclear Medicine | Nuclear |
| RF | Fluoroscopy | Fluoroscopy |
|XA | Angiography | Fluoroscopy |
| CR | Computed Radiography | Projection |
| OPG | Orthopantomogram | Projection |
| DXA | Bone Densitometry | Projection |

## Body Part Detection

Extract body part from text:

```python
def detect_body_part(text):
    text_upper = text.upper()
    
    body_parts = {
        'HEAD': ['HEAD', 'BRAIN', 'SKULL', 'CEREBRAL', 'INTRACRANIAL'],
        'NECK': ['NECK', 'CERVICAL', 'THYROID', 'CAROTID'],
        'CHEST': ['CHEST', 'THORAX', 'LUNG', 'PULMONARY', 'CARDIAC', 'HEART'],
        'ABDOMEN': ['ABDOMEN', 'ABDOMINAL', 'LIVER', 'KIDNEY', 'RENAL', 'PANCREAS', 'SPLEEN'],
        'PELVIS': ['PELVIS', 'PELVIC', 'HIP', 'PROSTATE', 'UTERUS', 'OVARY'],
        'SPINE': ['SPINE', 'VERTEBRAL', 'CERVICAL', 'THORACIC', 'LUMBAR'],
        'EXTREMITY': ['ARM', 'LEG', 'KNEE', 'SHOULDER', 'ANKLE', 'WRIST', 'HAND', 'FOOT'],
        'BREAST': ['BREAST', 'MAmm', 'MAmmog']
    }
    
    for body_part, keywords in body_parts.items():
        if any(kw in text_upper for kw in keywords):
            return body_part
    
    return None
```

## Contrast Detection

Determine if contrast is used:

```python
def detect_contrast(text):
    text_upper = text.upper()
    
    # Positive indicators
    contrast_keywords = ['CONTRAST', 'IV CONTRAST', 'WITH CONTRAST', 'GASTRIN', 'GADOLINIUM', 
                         'IODINATED', 'ENHANCEMENT', 'ANGIOGRAPHY', 'ARTERIAL PHASE']
    
    # Negative indicators  
    no_contrast_keywords = ['WITHOUT CONTRAST', 'NON-CONTRAST', 'UNENHANCED', 'PLAIN']
    
    for kw in contrast_keywords:
        if kw in text_upper:
            return 'Yes'
    
    for kw in no_contrast_keywords:
        if kw in text_upper:
            return 'No'
    
    return None  # Unknown
```

## Output Format

Return detection results in structured format:

```json
{
  "modality": "CT",
  "modality_confidence": "High",
  "body_part": "Chest",
  "contrast": "Yes",
  "subtype": null,
  "source": "text",
  "original_input": "CT chest with contrast",
  "warnings": []
}
```

### Confidence Levels

| Level | Criteria |
|-------|----------|
| High | Exact match, clear indication |
| Medium | Partial match, some ambiguity |
| Low | Weak indicators, significant ambiguity |
| Unknown | Cannot determine, needs clarification |

## Handling Ambiguous Cases

When input is ambiguous:

1. **Request clarification**: Ask user for more specific information
2. **List possibilities**: Provide options if multiple modalities match
3. **Use context**: Consider clinical context if available
4. **Defer to user**: When in doubt, ask rather than guess

Example response for ambiguous input:

```
The input "chest imaging study" is ambiguous. Please clarify:

1. CT chest with contrast
2. Chest X-ray (PA/lateral)
3. Chest ultrasound
4. PET/CT chest

Which modality do you mean?
```

## Common Abbreviations

| Abbreviation | Full Term | Modality |
|--------------|-----------|----------|
| CXR | Chest X-ray | X-ray |
| KUB | Kidneys, Ureter, Bladder X-ray | X-ray |
| CTA | CT Angiography | CT |
| MRA | MR Angiography | MRI |
| VQ | Ventilation/Perfusion Scan | Nuclear |
| HIDA | Hepatobiliary Scan | Nuclear |
| DEXA | Bone Density Scan | X-ray |
| OPG | Panoramic Dental X-ray | X-ray |

## Related Skills

- **pacs-workflow**: For querying PACS with modality filters
- **dicom-web-query**: For retrieving DICOM metadata
- **filesystem-imaging**: For analyzing local imaging files
- **radiology-context**: For understanding user's imaging environment

## Examples

### Example 1: Text Input
**Input**: "CT abdomen with contrast"
**Output**:
```json
{
  "modality": "CT",
  "body_part": "Abdomen",
  "contrast": "Yes"
}
```

### Example 2: DICOM File
**Input**: DICOM file with Modality=MR, BodyPartExamined=BRAIN
**Output**:
```json
{
  "modality": "MRI",
  "body_part": "Brain",
  "source": "DICOM header"
}
```

### Example 3: Ambiguous Input
**Input**: "imaging study"
**Response**: "Please specify the modality: CT, MRI, X-ray, Ultrasound, etc."
