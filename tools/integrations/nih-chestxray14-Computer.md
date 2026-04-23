# NIH ChestX-ray14 Integration

NIH Clinical Center chest X-ray dataset.

## Connection

```yaml
base_url: https://nihcc气囊.cloud.google.com
bucket: nlm-nihcc-chest
```

## Authentication

```bash
# GCP authentication
gcloud auth application-default login

# Or service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
```

## Dataset Details

- **Images**: 112,120 frontal/lateral views
- **Patients**: 30,805 unique
- **Resolution**: 1024x1024 pixels
- **Labels**: 14 disease patterns (NLP-extracted)
- **Labels**: Atelectasis, Cardiomegaly, Consolidation, Edema, Effusion, Emphysema, Fibrosis, Hernia, Infiltration, Mass, Nodule, Pleural_Thickening, Pneumonia, Pneumothorax

## Key Operations

### List Images
```bash
# List all image files
gsutil ls gs://nlm-nihcc-chest/

# List specific patient
gsutil ls gs://nlm-nihcc-chest/patient00001/

# Count files
gsutil ls gs://nlm-nihcc-chest/ | wc -l
```

### Download
```bash
# Download single image
gsutil cp gs://nlm-nihcc-chest/patient00001/study1/view1_frontal.jpg .

# Download batch
gsutil -m cp -r gs://nlm-nihcc-chest/patient00001 ./local_dir/

# Sync to local
gsutil rsync -r gs://nlm-nihcc-chest local_backup/
```

### Metadata Access
```bash
# Download labels CSV
gsutil cp gs://nlm-nihcc-chest/data_labels.csv .

# Download bounding boxes
gsutil cp gs://nlm-nihcc-chest/bbox_labels.csv .
```

## Label Format

```csv
Image,Atelectasis,Cardiomegaly,Consolidation,Edema,Effusion,Emphysema,Fibrosis,Hernia,Infiltration,Mass,Nodule,Pleural_Thickening,Pneumonia,Pneumothorax,No_Finding
00000123_000.png,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0
```

## Limitations

- Labels extracted via NLP (not radiologist-verified)
- Only frontal/lateral chest views
- De-identification: Verified (NSCLC removed)
- No follow-up outcome data

## Rate Limits

- Free via Google Cloud Public Datasets
- Standard egress charges apply

## Tool Registration

```json
{
  "name": "nih_chestxray",
  "description": "NIH ChestX-ray14 dataset access",
  "category": "dataset",
  "endpoints": ["image_list", "image_download", "labels_access", "metadata_query"]
}
```
