# DICOM Conformance Statement Parser

Parse and validate DICOM implementations.

## Purpose

Extracts DICOM capabilities from vendor conformance statements to ensure interoperability.

## Key Fields Extracted

### Transfer Syntaxes
- Explicit VR Little Endian (1.2.840.10008.1.2.1)
- Implicit VR Little Endian (1.2.840.10008.1.2)
- JPEG Lossless (1.2.840.10008.1.2.4.70)
- JPEG 2000 Lossless (1.2.840.10008.1.2.4.90)

### SOP Classes Supported

| Class | UID | Description |
|-------|-----|-------------|
| CT Image Storage | 1.2.840.10008.5.1.4.1.1.2 | CT Images |
| MR Image Storage | 1.2.840.10008.5.1.4.1.1.4 | MR Images |
| Enhanced MR | 1.2.840.10008.5.1.4.1.1.4.1 | Enhanced MR |
| Print Management | 1.2.840.10008.5.1.1.14 | DICOM Print |

### Query/Retrieve
```yaml
query_models:
  - Patient Root Q/R
  - Study Root Q/R
  - Patient/Study Only Q/R

retrieval_levels:
  - Patient
  - Study
  - Series
  - Image
```

## Parser Implementation

```python
import re

def parse_conformance(text):
    """Extract capabilities from conformance statement."""
    capabilities = {
        'transfer_syntaxes': [],
        'sop_classes': [],
        'query_models': [],
        'retrieve_levels': []
    }
    
    # Extract transfer syntaxes
    syntax_pattern = r'(1\.2\.840\.\d+\.\d+\.\d+\.\d+\.\d+)'
    capabilities['transfer_syntaxes'] = re.findall(
        syntax_pattern, text)
    
    # Extract SOP classes
    sop_pattern = r'(?:Supported|SOP Class).*?([A-Z][^\n]+)'
    capabilities['sop_classes'] = re.findall(sop_pattern, text)
    
    return capabilities
```

## Validation Checks

1. **Required Transfer Syntax** - Explicit VR Little Endian required
2. **Lossless Support** - Should support at least one lossless format
3. **Query Model** - Must support Study Root or Patient Root
4. **SOP Classes** - Check for required imaging modalities

## Output Format

```json
{
  "vendor": "Vendor Name",
  "model": "Model Number",
  "version": "Software Version",
  "conformance_level": "Complete|Basic| Restricted",
  "transfer_syntaxes": [...],
  "sop_classes": [...],
  "query_retrieve": {...},
  "print": {...},
  "validation_results": {
    "is_interoperable": true,
    "warnings": [],
    "errors": []
  }
}
```

## Tool Registration

```json
{
  "name": "dicom_conformance",
  "description": "Parse and validate DICOM conformance statements",
  "category": "pacs",
  "endpoints": ["conformance_parse", "capability_extract", "interoperability_check"]
}
```
