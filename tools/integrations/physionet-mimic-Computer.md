# PhysioNet MIMIC Integration

Access MIMIC medical imaging datasets via PhysioNet.

## Connection

```yaml
physionet_url: https://physionet.org
mimic_path: mimic-cxr/
```

## Authentication

PhysioNet credentials + data use agreement:
```bash
# Login
physiotools login --username {user}

# Credentialed access
export PhysioNetToken={credential_token}
```

## Datasets Available

### MIMIC-CXR
- **Description**: Chest X-rays with radiologist reports
- **Size**: ~377,000 images, ~227,000 studies
- **Reports**: NLP-parsed + manual validation
- **Access**: Credentialed (CITI training required)

### MIMIC-Note
- **Description**: Clinical notes (radiology reports)
- **Size**: ~331,000 reports
- **Format**: MIMIC-IV Notes

### MIMIC-Image
- **Description**: CT, MRI, ultrasound (limited)
- **Access**: Research only, additional application

## Key Operations

### Dataset Access
```bash
# List files
aws s3 ls s3://physionet-mimic-cxr-ego-data/

# Download with wget
wget -r -np -nH --cut-dirs=4 \
  --user={user} --ask-password \
  https://physionet.org/files/mimic-cxr/2.0.0/

# Download with wfdb
python -m wfdb download mimic-cxr
```

### Database Access
```bash
# Connect to MIMIC
psql "postgresql://user:pass@host:5432/mimic"

# Query studies
SELECT subject_id, study_id, study_date, modality
FROM mimiccxr.study
WHERE modality = 'SR';
```

## Data Schema

```sql
-- Study metadata
CREATE TABLE mimiccxr.study (
  subject_id INT,
  study_id INT,
  study_datetime TIMESTAMP,
  study_date DATE,
  modality VARCHAR(10),
  study_id_gcp VARCHAR(50),
  dicom_id VARCHAR(100)
);

-- Report metadata
CREATE TABLE mimiccxr.report (
  subject_id INT,
  study_id INT,
  report_text TEXT,
  report_status VARCHAR(20),
  report_datetime TIMESTAMP
);
```

## Compliance

- Requires CITI Data or Specimens Only Research
- Data use agreement signature required
- IRB approval recommended
- No commercial use without separate agreement

## Rate Limits

- Download: 10 GB/day free tier
- Cloud access: Via AWS Public Dataset (no charge)

## Tool Registration

```json
{
  "name": "physionet_mimic",
  "description": "MIMIC-CXR and MIMIC-IV datasets via PhysioNet",
  "category": "dataset",
  "endpoints": ["dataset_access", "metadata_query", "image_download", "report_retrieval"]
}
```
