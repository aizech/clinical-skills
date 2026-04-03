# PubMed/NCBI Literature Integration

Search and retrieve medical literature via NCBI APIs.

## Connection

```yaml
base_url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
api_key: ${NCBI_API_KEY}
email: ${NCBI_EMAIL}
```

## Authentication

API key for increased limits (free):
```
?api_key={NCBI_API_KEY}
```

## Key Endpoints

### ESearch (Search)
```bash
# Search for articles
GET /esearch.fcgi?db=pubmed&term=lung+nodule+AI&retmax=20

# With filters
GET /esearch.fcgi?db=pubmed&term=radiology[MeSH]&
  filter=clinical-trial[pt]&retmax=50
```

### EFetch (Retrieve)
```bash
# Get article details
GET /efetch.fcgi?db=pubmed&id=12345678&rettype=xml

# Multiple articles
GET /efetch.fcgi?db=pubmed&id=123,234,345&rettype=medline
```

### ELink (Links)
```bash
# Related articles
GET /elink.fcgi?dbfrom=pubmed&id=12345678&linkname=pubmed_pubmed

# Cited by
GET /elink.fcgi?dbfrom=pubmed&id=12345678&linkname=citedby
```

### ESummary (Summary)
```bash
# Quick summary
GET /esummary.fcgi?db=pubmed&id=12345678
```

## Search Syntax

### MeSH Terms
```bash
# Radiological AI
"artificial intelligence"[MeSH Terms] AND "radiology"[MeSH Terms]

# Clinical trials
"deep learning"[All Fields] AND ("computed tomography"[MeSH] OR "CT scan"[All Fields])
```

### Filters
| Filter | Parameter |
|--------|-----------|
| Article Type | `clinical-trial[pt]` |
| Date Range | `2020:2024[PDAT]` |
| Language | `eng[la]` |
| Humans | `humans[MeSH]` |
| Free Full Text | `free fulltext[filter]` |

## Response Format

```xml
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <Title>...</Title>
        <Abstract>...</Abstract>
        <AuthorList>...</AuthorList>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
```

## Rate Limits

| Type | Without Key | With Key |
|------|-------------|----------|
| Requests/sec | 3 | 10 |
| Requests/day | 10,000 | 100,000 |
| Results/request | 100 | 10,000 |

## Tool Registration

```json
{
  "name": "pubmed_literature",
  "description": "PubMed literature search and retrieval",
  "category": "literature",
  "endpoints": ["article_search", "article_fetch", "related_articles", "cited_by"]
}
```
