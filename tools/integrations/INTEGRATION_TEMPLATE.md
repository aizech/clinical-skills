# {Integration Name} Integration

{Brief 1-2 sentence description of what this integration provides.}

## Overview

{Detailed description of the integration, including:
- What the tool/platform/service does
- Why it's relevant to radiology workflows
- Key use cases and scenarios
}

## Connection

### Configuration

```yaml
# Required fields
host: example.com
port: 443
api_key: ${API_KEY_ENV_VAR}

# Optional fields
timeout: 30
verify_ssl: true
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `{INTEGRATION}_API_KEY` | Yes | API key for authentication |
| `{INTEGRATION}_HOST` | No | Override default host |
| `{INTEGRATION}_PORT` | No | Override default port |

## Authentication

{Describe authentication method - Basic Auth, Bearer Token, OAuth, etc.}

```bash
# Example authentication
curl -H "Authorization: Bearer ${API_KEY}" https://api.example.com/endpoint
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/studies` | GET | List all studies |
| `/studies/{id}` | GET | Get study details |
| `/series` | POST | Create new series |

## Common Operations

### Operation 1

{Description of what the operation does}

```bash
# Example command
curl -X GET https://api.example.com/endpoint
```

**Parameters:**
- `param1`: Description
- `param2`: Description

**Response:**
```json
{
  "status": "success",
  "data": {}
}
```

### Operation 2

{Description of what the operation does}

```bash
# Example command
curl -X POST https://api.example.com/endpoint
```

## Rate Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Requests/minute | 100 | Per API key |
| Burst | 200 | Short-term spikes |

## Error Handling

| Status Code | Meaning | Resolution |
|-------------|---------|------------|
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Verify API key |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry with exponential backoff |

## Tool Registration

```json
{
  "name": "{integration_name}",
  "description": "{Brief description for tool registry}",
  "category": "{category: pacs, dicomweb, ai, dataset, etc.}",
  "endpoints": ["endpoint1", "endpoint2", "endpoint3"],
  "auth_method": "{bearer, basic, oauth, none}",
  "rate_limit": 100
}
```

## Troubleshooting

### Issue 1

**Symptom:** {Description of the problem}

**Solution:** {Steps to resolve}

### Issue 2

**Symptom:** {Description of the problem}

**Solution:** {Steps to resolve}

## References

- [Official Documentation](https://example.com/docs)
- [API Reference](https://example.com/api)
- [Community Forum](https://example.com/community)

## Examples

### Example 1: Use Case Title

{Step-by-step walkthrough of a common workflow}

```bash
# Step 1
command_1

# Step 2
command_2

# Step 3
command_3
```

### Example 2: Use Case Title

{Another workflow example}

```bash
# Complete workflow
workflow_command
```

## Notes

- {Important note 1}
- {Important note 2}
