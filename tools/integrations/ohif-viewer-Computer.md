# OHIF Viewer Integration

Web-based DICOM viewer with DICOMweb support.

## Connection

```yaml
host: viewer.example.com
wado_uri_base: https://viewer.example.com/dicomweb
qido_base_url: https://viewer.example.com/dicomweb
wado_rs_base_url: https://viewer.example.com/dicomweb
```

## DICOMweb Endpoints

### QIDO-RS (Query)
```bash
# Search studies
GET /studies?PatientName=SMITH&ModalitiesInStudy=CT

# Search series
GET /series?StudyInstanceUID={uid}&Modality=MR

# Search instances
GET /instances?SeriesInstanceUID={uid}
```

### WADO-RS (Retrieve)
```bash
# Retrieve metadata
GET /studies/{uid}/metadata

# Retrieve frames
GET /studies/{uid}/series/{uid}/instances/{uid}/frames/1

# Retrieve rendered image
GET /studies/{uid}/series/{uid}/instances/{uid}/rendered
```

### WADO-URI (Legacy)
```bash
GET /wado?studyUID={uid}&seriesUID={uid}&objectUID={iid}&contentType=application/dicom
```

## Authentication

JWT token in Authorization header or cookie-based session.

## Rate Limits

Usually 1000 requests/minute per client.

## Tool Registration

```json
{
  "name": "ohif_viewer",
  "description": "DICOMweb REST operations via OHIF Viewer",
  "category": "dicomweb",
  "endpoints": ["qido_search", "wado_retrieve", "wado_render"]
}
```
