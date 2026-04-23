# Amazon HealthLake Integration

AWS HIPAA-eligible healthcare data analytics.

## Connection

```yaml
region: us-east-1
datastore_id: ${HEALTHLAKE_DATASTORE_ID}
role_arn: arn:aws:iam::123456789:role/HealthLakeRole
```

## Authentication

```bash
# AWS credentials
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

## Key Operations

### ImagingStudy FHIR Resource
```bash
# Create ImagingStudy
aws healthlake create-imaging-study \
  --datastore-id $DATSTORE_ID \
  --imaging-study '{"resourceType": "ImagingStudy", ...}'

# Get ImagingStudy
aws healthlake get-imaging-study \
  --datastore-id $DATASTORE_ID \
  --imaging-study-id $STUDY_ID
```

### Patient Search
```bash
aws healthlake search \
  --datastore-id $DATASTORE_ID \
  --search-type Patient \
  --filter '{"filters": [{"operator": "DATE_GE", "values": ["2024-01-01"]}]}'
```

### Analytics with Athena
```bash
# Query imaging data
aws athena start-query-execution \
  --query-string "SELECT * FROM healthlake_imaging WHERE modality = 'CT'" \
  --result-configuration "{\"outputLocation\": \"s3://bucket/results/\"}"
```

## S3 for DICOM Storage
```bash
# List DICOM files
aws s3 ls s3://radiology-dicom-bucket/studies/

# Upload DICOM
aws s3 cp image.dcm s3://radiology-dicom-bucket/incoming/
```

## SageMaker for ML
```bash
# Deploy inference endpoint
aws sagemaker create-endpoint \
  --endpoint-name radiology-ai \
  --production-variants file://variants.json
```

## Compliance

- HIPAA eligible
- SOC 2 Type II
- HITRUST CSF certified

## Rate Limits

Varies by AWS service. Standard AWS limits apply.

## Tool Registration

```json
{
  "name": "amazon_healthlake",
  "description": "AWS HIPAA-compliant healthcare data and imaging analytics",
  "category": "ai_platform",
  "endpoints": ["fhir", "s3_storage", "athena", "sagemaker"]
}
```
