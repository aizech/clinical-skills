# Modality Detection Reference

## Modality Selection Guidelines

### When to Use Each Modality

| Clinical Question | Recommended Modality | Alternative |
|-------------------|---------------------|-------------|
| Acute stroke | CT Head, MRI DWI | CTA if thrombectomy considered |
| Pulmonary embolism | CTPA (CT Pulmonary Angiography) | V/Q scan if contrast contraindicated |
| Appendicitis | CT Abdomen/Pelvis | Ultrasound (especially in children) |
| Kidney stones | CT KUB (non-contrast) | Ultrasound |
| Spinal cord compression | MRI | CT |
| Lung nodules | CT | PET/CT for characterization |
| Breast cancer screening | Mammography | MRI for high risk |
| Abdominal aortic aneurysm | Ultrasound, CTA | MRA |
| Stroke hemorrhage | CT | MRI |

## DICOM Modalities Reference

Complete list of DICOM modality codes (Part 16 CID 29):

### Imaging Modalities
- AR - Autorefraction
- BDUS - Bone Densitometry (Ultrasound)
- BI - Biomagnetic Imaging
- BMG - Bone Densitometry (X-Ray)
- BT - Tomotherapy
- CardCT - Cardiac Computed Tomography
- CR - Computed Radiography
- CT - Computed Tomography
- DE - Dental Intra-oral X-ray
- DG - Dental Panoramic X-ray
- DM - Digital Microscopy
- DOC - Document Scanner
- DX - Digital Radiography
- EC - Electron Crystallography
- ECG - Electrocardiography
- EPS - Cardiac Electrophysiology
- ES - Endoscopy
- FA - Fluorescein Angiography
- FFA - Fundus Fluorescein Angiography
- FP - Fingerprint
- GM - General Microscopy
- HDS - Helical/Serial Tomosynthesis
- IO - Intra-oral X-ray
- IOL - Intraocular Lens Data
- IVUS - Intravascular Ultrasound
- KER - Keratometry
- KO - Corneal Topography
- LAS - Laser Scan
- LE - Lensometry
- LEN - Lensometry
- LS - Laser Scans
- MA - Magnetic Resonance Angiography
- MG - Mammography
- MR - Magnetic Resonance
- MS - MR Spectroscopy
- NM - Nuclear Medicine
- OAM - Ocular Anatomy Map
- OCT - Optical Coherence Tomography
- OP - Ophthalmic Photography
- OPM - Objective Perimetry
- OPT - Ophthalmic Tomography
- OPV - Ocular Phenotype Vision
- OT - Other
- OU - Ophthalmic Ultrasound
- PA - Photo CD Image - Mammography
- PALM - Papanicolaou Smear
- PAT - Patient Data
- PC - Photo CD Image - Other
- PET - Positron Emission Tomography
- PLAN - Plan
- PLM - Cardiac Plaque Map
- PMA - Posture Analysis
- PNM - Psychiatric Naming
- PR - Patient Presentation
- PT - PET (non-DICOM term, use PET modality)
- RF - Radio Fluoroscopy
- RG - Radiographic Imaging (Conventional Film)
| RH - Rhodopsin
| RTDOSE - Radiation Therapy Dose
| RTIMAGE - Radiation Therapy Image
| RTPLAN - Radiation Therapy Plan
| RTRECORD - RT Treatment Record
| RTSTRUCT - Radiation Therapy Structure Set
| SEG - Segmentation
| SMR - Stereometric Row
| SR - Structured Report
| SRF - Subjective Refraction
| ST - Single-Photon Emission Computed Tomography
| TEP - Thermography
| TH - Thermography
| TY - Typing
| UFF - Ultrasound Face and Neck
| UG - Urography
| UI - Ultrasound Imaging
| UL - Ultrasound
| UM - Ultrasound Microscopy
| UO - Ultrasound Ophthalmic
| UP - Urology
| UR - Urinary
| US - Ultrasound
| VA - Visual Acuity
| VF - Visual Field
- VF - Vital Signs
| XA - X-Ray Angiography
| XAng - X-Ray Angiography
| XA - X-Ray Angiography

## Contrast Agents Reference

### CT Contrast
| Agent Type | Iodine Concentration | Use |
|------------|---------------------|-----|
| Iso-osmolar | 320 mgI/mL | High-risk patients |
| Low-osmolar | 300-370 mgI/mL | Standard use |
| Oral | Varies | GI tract opacification |

### MRI Contrast
| Agent Type | Gadolinium Type | Use |
|------------|-----------------|-----|
| Extracellular | Gadopentetate, Gadoteridol | General imaging |
| Hepatobiliary | Gadoxetate (Eovist) | Liver |
| Blood Pool | Gadofosveset | Vascular |

## Multi-Modality Studies

When studies combine modalities:

| Combined Study | Primary Modality | Secondary |
|----------------|-----------------|-----------|
| PET/CT | PET | CT (for attenuation correction) |
| PET/MR | PET | MRI |
| SPECT/CT | NM (SPECT) | CT (for attenuation correction) |
| IVUS-OCT | IVUS | OCT |

## Quality Assurance Notes

### Common Errors in Modality Detection

1. **Confusing abbreviations**: CT vs CTA, MR vs MRA
2. **Body part in modality field**: "Chest CT" is CT, not Chest
3. **Legacy codes**: Film-based modalities vs digital
4. **Vendor-specific codes**: Non-standard extensions

### Verification Steps

1. Cross-reference modality with body part
2. Check if contrast indication matches modality capabilities
3. Verify protocol consistency with clinical indication
