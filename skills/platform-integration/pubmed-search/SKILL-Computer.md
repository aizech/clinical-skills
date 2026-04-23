---
name: pubmed-search
description: Evidence-based literature search for radiology. Also use when the user needs to find relevant studies, guidelines, clinical evidence, systematic reviews, or research papers for imaging findings. For guideline-specific searches, see guideline-integration.
---

# PubMed Search for Radiology

You are a medical literature search expert. Your role is to help users find relevant, high-quality research for radiology applications.

## PubMed API Overview

### NCBI Entrez API

| Service | Endpoint | Purpose |
|---------|----------|---------|
| ESearch | `/esearch.fcgi` | Search for article IDs |
| ESummary | `/esummary.fcgi` | Get article summaries |
| EFetch | `/efetch.fcgi` | Get full article details |
| ELink | `/elink.fcgi` | Find related articles |
| EGQuery | `/egquery.fcgi` | Global search |

### Base URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## Search Construction

### Basic Search

```python
import requests
from urllib.parse import urlencode

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def pubmed_search(query, max_results=20, date_filter=None):
    """
    Search PubMed for articles.
    
    Args:
        query: Search terms (use [MeSH] for controlled vocabulary)
        max_results: Maximum number of results
        date_filter: Optional date restriction (e.g., "2020:2026")
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }
    
    if date_filter:
        params["datetype"] = "pdat"
        params["reldate"] = date_filter
    
    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    return response.json()
```

### Search Query Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| AND | "lung nodule" AND "AI" | Both terms required |
| OR | "MRI" OR "CT" | Either term |
| NOT | "COVID" NOT "pneumonia" | Exclude term |
| [MeSH] | "Neoplasm"[MeSH] | MeSH controlled vocabulary |
| [tiab] | "cancer"[tiab] | Title/abstract only |
| [ti] | "lung cancer"[ti] | Title only |
| [au] | "Smith J"[au] | Author search |

## Radiology-Specific Searches

### Imaging Modality Studies

```python
# CT Studies
def search_ct_studies(topic, years=5):
    return pubmed_search(
        f"({topic}) AND (CT[tiab] OR 'computed tomography'[tiab])",
        date_filter=f"{years}[dp]"
    )

# MRI Studies  
def search_mri_studies(topic, years=5):
    return pubmed_search(
        f"({topic}) AND (MRI[tiab] OR 'magnetic resonance'[tiab])",
        date_filter=f"{years}[dp]"
    )

# X-ray Studies
def search_xray_studies(topic, years=5):
    return pubmed_search(
        f"({topic}) AND (X-ray[tiab] OR 'radiograph'[tiab])",
        date_filter=f"{years}[dp]"
    )

# Ultrasound
def search_ultrasound_studies(topic, years=5):
    return pubmed_search(
        f"({topic}) AND (ultrasound[tiab] OR 'sonography'[tiab])",
        date_filter=f"{years}[dp]"
    )
```

### AI/ML in Radiology

```python
def search_ai_radiology(max_results=50):
    """Search for AI/ML papers in radiology."""
    query = """
    (deep learning[tiab] OR machine learning[tiab] OR 
     artificial intelligence[tiab] OR neural network[tiab] OR
     convolutional[tiab] OR CNN[tiab] OR AI[tiab])
    AND (radiology[tiab] OR radiologist[tiab] OR 
         imaging[tiab] OR diagnostic imaging[tiab])
    """
    return pubmed_search(query, max_results=max_results)
```

### Guideline Searches

```python
def search_guidelines(condition, modality=None):
    """Search for clinical guidelines."""
    query = f"({condition})"
    
    if modality:
        query += f" AND ({modality})"
    
    query += """ AND 
    (guideline[pt] OR practice guideline[pt] OR 
     recommendation[tiab] OR consensus[tiab])"""
    
    return pubmed_search(query)
```

### Systematic Reviews

```python
def search_systematic_review(topic):
    """Find systematic reviews."""
    query = f"({topic}) AND (systematic[pt] OR 'systematic review'[tiab])"
    return pubmed_search(query)
```

## Get Article Details

```python
def get_article_details(pmids):
    """Get detailed article information."""
    if isinstance(pmids, str):
        pmids = [pmids]
    
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    
    response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params)
    return response.text  # Parse XML as needed
```

### Extract Key Information

```python
def extract_article_info(xml_text):
    """Extract key fields from PubMed XML."""
    import xml.etree.ElementTree as ET
    
    root = ET.fromstring(xml_text)
    articles = []
    
    for article in root.findall(".//PubmedArticle"):
        info = {
            "pmid": article.findtext(".//PMID"),
            "title": article.findtext(".//ArticleTitle"),
            "abstract": article.findtext(".//AbstractText"),
            "authors": [
                auth.findtext("LastName") + ", " + auth.findtext("ForeName")
                for auth in article.findall(".//Author")
            ],
            "journal": article.findtext(".//Journal/Title"),
            "pub_date": article.findtext(".//PubDate/Year"),
            "doi": article.findtext(".//ArticleIdList/ArticleId[@IdType='doi']")
        }
        articles.append(info)
    
    return articles
```

## Citation Analysis

```python
def find_related_articles(pmid):
    """Find articles related to a specific paper."""
    params = {
        "dbfrom": "pubmed",
        "id": pmid,
        "linkname": "pubmed_pubmed"
    }
    
    response = requests.get(f"{BASE_URL}/elink.fcgi", params=params)
    return response.json()

def get_citation_count(pmid):
    """Get citation count for an article."""
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "json"
    }
    
    response = requests.get(f"{BASE_URL}/esummary.fcgi", params=params)
    data = response.json()
    
    return data.get("result", {}).get(pmid, {}).get("citationcount", 0)
```

## Clinical Trials

```python
def search_clinical_trials(condition):
    """Search ClinicalTrials.gov for relevant trials."""
    base_url = "https://clinicaltrials.gov/api/v2"
    
    params = {
        "query.term": condition,
        "filter.advanced": "radiology[AreaOfResearch]",
        "pageSize": 20
    }
    
    response = requests.get(f"{base_url}/studies", params=params)
    return response.json()
```

## ACR Guidelines

### Common ACR Search Terms

| Topic | Search Terms |
|-------|-------------|
| Incidental Findings | "incidental"[tiab] AND ("ACR"[tiab] OR "American College"[tiab]) |
| Lung Nodules | "pulmonary nodule"[tiab] AND "ACR"[tiab] |
| TI-RADS | "TI-RADS"[tiab] OR "thyroid imaging"[tiab] |
| LI-RADS | "LI-RADS"[tiab] OR "liver imaging"[tiab] |
| PI-RADS | "PI-RADS"[tiab] OR "prostate imaging"[tiab] |
| BI-RADS | "BI-RADS"[tiab] OR "breast imaging"[tiab] |

## Search Result Formatting

### Structured Output

```json
{
  "query": "lung nodule AI detection",
  "total_results": 156,
  "returned": 20,
  "articles": [
    {
      "pmid": "12345678",
      "title": "Deep learning for lung nodule detection...",
      "authors": ["Smith J", "Doe A"],
      "journal": "Radiology",
      "year": 2025,
      "abstract": "...",
      "citation_count": 45,
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }
  ]
}
```

### Summary Format

```
LITERATURE SEARCH RESULTS
=========================

Query: Lung Nodule AI Detection
Date: 2026-04-03
Results: 156 studies (showing top 10)

1. Deep Learning for Lung Nodule Detection in CT
   PMID: 12345678 | Radiology 2025
   Smith J, et al. | Citations: 45
   https://pubmed.ncbi.nlm.nih.gov/12345678/

2. Comparison of AI vs Radiologist Performance...
   PMID: 12345679 | Lancet Digital Health 2025
   ...
```

## Quality Indicators

### Assess Article Quality

| Indicator | Good | Poor |
|-----------|------|------|
| Journal Impact Factor | >5 | <2 |
| Sample Size | >100 | <30 |
| Study Design | RCT, prospective | Case report |
| Peer Review | Yes | Preprint |
| Citations | >20 | <5 |

### Study Types

| Type | Description | Evidence Level |
|------|-------------|---------------|
| Systematic Review | Comprehensive literature review | 1 |
| RCT | Randomized controlled trial | 1-2 |
| Cohort | Prospective follow-up | 2-3 |
| Case-Control | Retrospective comparison | 3 |
| Case Report | Single patient description | 4 |

## Related Skills

- **guideline-integration**: For ACR/ESR guidelines
- **radiology-research**: For research study design
- **cross-reference-linking**: For linking to related literature

## Examples

### Example 1: Find Recent AI Mammography Studies

```python
results = pubmed_search(
    "(mammography OR breast cancer) AND "
    "(deep learning OR AI OR machine learning) AND "
    "(detection OR diagnosis) AND "
    "2024:2026[dp]",
    max_results=30
)
```

### Example 2: Find ACR Lung Nodule Guidelines

```python
results = search_guidelines(
    condition="pulmonary nodule",
    modality="CT"
)
```

### Example 3: Systematic Review on AI in Radiology

```python
results = search_systematic_review(
    "deep learning radiology"
)
```
