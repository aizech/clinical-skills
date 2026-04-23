# Radiopaedia Reference Integration

Radiology case database and educational resource.

## Connection

```yaml
base_url: https://radiopaedia.org
api_url: https://api.radiopaedia.org
```

## Authentication

API key for programmatic access:
```bash
curl -H "X-API-Key: {api_key}" \
  https://api.radiopaedia.org/v1/search?q=lung+nodule
```

## Key Operations

### Case Search
```bash
# Search by keyword
GET /v1/search?keyword={term}&modality=CT&body_part=chest

# Featured cases
GET /v1/cases/featured

# Recent cases
GET /v1/cases/recent?modality=CT&limit=20
```

### Case Details
```bash
# Get case
GET /v1/cases/{case_id}

# Get case images
GET /v1/cases/{case_id}/images

# Get associated articles
GET /v1/articles?topic={condition}
```

## Content Structure

### Case Components
- **Clinical presentation**: Patient history and symptoms
- **Imaging findings**: Detailed description of imaging
- **Differential diagnosis**: Possible diagnoses
- **Discussion**: Educational discussion
- **References**: Related literature

### Article Types
- **Articles**: Condition overviews (e.g., "Pulmonary embolism")
- **Case reports**: Individual patient cases
- **Case series**: Multiple related cases

## Web Scraping (Alternative)

For non-API access:
```python
import requests
from bs4 import BeautifulSoup

def search_radiopaedia(query):
    """Search Radiopaedia via web scraping."""
    url = f"https://radiopaedia.org/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    for article in soup.select(".search-result"):
        results.append({
            "title": article.select_one("h2").text,
            "url": article.select_one("a")["href"],
            "type": article.select_one(".type").text
        })
    
    return results
```

## Rate Limits

- API: Requires registration and approval
- Web scraping: Respect robots.txt, rate limit requests

## Use Cases

1. **Case Lookup**: Find similar cases for differential diagnosis
2. **Educational Reference**: View classic presentations
3. **Imaging Findings**: See examples of specific findings
4. **Teaching Points**: Review educational discussions

## Tool Registration

```json
{
  "name": "radiopaedia",
  "description": "Radiopaedia case database and educational articles",
  "category": "reference",
  "endpoints": ["case_search", "case_details", "article_lookup"]
}
```

## Best Practices

- Use for educational and reference purposes
- Cite Radiopaedia in educational materials
- Respect copyright for images
- Link to original cases when referencing
