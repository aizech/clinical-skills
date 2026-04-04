# Troubleshooting Guide

Common issues and solutions for clinical-skills users and contributors.

## Installation Issues

### Skill Installation Fails

**Symptom:** `npx skills add aizech/clinical-skills` fails

**Possible Causes:**
1. Network connectivity issues
2. npm not installed or outdated
3. Permission issues

**Solutions:**
```bash
# Check npm version
npm --version  # Should be 7+

# Update npm
npm install -g npm@latest

# Try with verbose output
npx skills add aizech/clinical-skills --verbose

# Alternative: Clone manually
git clone https://github.com/aizech/clinical-skills.git
cp -r clinical-skills/skills/* .agents/skills/
```

### Claude Code Plugin Not Loading

**Symptom:** Skills don't appear in Claude Code

**Possible Causes:**
1. Incorrect installation path
2. Plugin marketplace not configured
3. Claude Code version incompatibility

**Solutions:**
```bash
# Check skills directory
ls .agents/skills/
ls .claude/skills/

# Verify symlink (if using npx skills)
ls -la .claude/skills/

# Reinstall plugin
/plugin marketplace remove clinical-skills
/plugin marketplace add aizech/clinical-skills
/plugin install clinical-skills
```

## Validation Issues

### Frontmatter Validation Fails

**Symptom:** `Missing YAML frontmatter` or `Invalid frontmatter`

**Common Issues:**

1. **Missing `---` delimiters**
   ```yaml
   # Wrong
   name: skill-name
   description: description

   # Correct
   ---
   name: skill-name
   description: description
   ---
   ```

2. **Extra spaces in delimiters**
   ```yaml
   # Wrong
   --- 
   name: skill-name
   ---

   # Correct
   ---
   name: skill-name
   ---
   ```

3. **Indentation errors**
   ```yaml
   # Wrong
   ---
   name: skill-name
     description: description  # Extra indentation
   ---

   # Correct
   ---
   name: skill-name
   description: description
   ---
   ```

### Name Mismatch Error

**Symptom:** `Name mismatch: directory='x' but frontmatter='y'`

**Solution:** Ensure the `name` field in frontmatter exactly matches the directory name:

```bash
# Directory: skills/core/radiology-context
# Frontmatter must be:
---
name: radiology-context
description: ...
---
```

### Description Length Error

**Symptom:** `Description length invalid: X chars (must be 1-1024)`

**Solution:** Shorten description or move details to skill body:

```yaml
# Too long
---
name: my-skill
description: This is a very long description that exceeds 1024 characters and needs to be shortened...
---

# Better
---
name: my-skill
description: Brief description with trigger phrases. See skill body for details.
---
```

### SKILL.md Line Count Warning

**Symptom:** `SKILL.md is X lines (should be <500)`

**Solution:** Move detailed content to `references/`:

```bash
# Create references directory
mkdir -p skills/{category}/{skill-name}/references

# Move detailed sections to separate files
mv skills/{category}/{skill-name}/SKILL.md detailed-section.md references/
```

## Security Check Issues

### False Positive: Environment Variable References

**Symptom:** Security report shows warnings for `password: "env:ORTHANC_PASSWORD"`

**Status:** **Fixed** - This is a legitimate pattern and should not be flagged.

**Solution:** If you still see this warning, ensure you're using the latest security-baseline.js:

```bash
# Pull latest changes
git pull origin main

# Re-run security check
node .github/scripts/security-baseline.js security-report.json
```

### Bearer Token Warning

**Symptom:** Security report shows `Bearer Token` warning

**Cause:** Documentation examples showing `Authorization: Bearer <token>`

**Solution:** This is expected in documentation. Use placeholder format:

```markdown
# Instead of:
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# Use:
Authorization: Bearer ${API_TOKEN}
# or
Authorization: Bearer <your-token-here>
```

### External Link Warnings

**Symptom:** Security report lists external links

**Status:** This is informational, not an error.

**Solution:** Review links to ensure they're:
- Publicly accessible
- Not pointing to internal resources
- Using HTTPS when possible

## CLI Tool Issues

### Import Error: Module Not Found

**Symptom:** `ModuleNotFoundError: No module named 'requests'`

**Solution:** Install required dependencies:

```bash
# Install requests
pip install requests

# Or install all dependencies if requirements.txt exists
pip install -r requirements.txt
```

### CLI Tool Permission Denied

**Symptom:** `bash: ./tools/clis/dicom_qido.py: Permission denied`

**Solution:** Make the script executable:

```bash
chmod +x tools/clis/*.py
```

### DICOMweb Connection Timeout

**Symptom:** `requests.exceptions.Timeout` or `requests.exceptions.ConnectionError`

**Possible Causes:**
1. PACS server is down
2. Network connectivity issues
3. Incorrect URL or port
4. Firewall blocking connection

**Solutions:**
```bash
# Test connectivity
ping pacs.example.com
curl -I https://pacs.example.com/dicomweb

# Check with verbose output
python tools/clis/dicom_qido.py https://pacs.example.com/dicomweb --verbose

# Increase timeout (if tool supports it)
python tools/clis/dicom_qido.py https://pacs.example.com/dicomweb --timeout 60
```

### PubMed API Rate Limit

**Symptom:** HTTP 429 error from PubMed

**Cause:** Exceeded NCBI API rate limit (3 requests/second without API key)

**Solution:**
1. Get NCBI API key: https://www.ncbi.nlm.nih.gov/account/
2. Use API key in requests:

```bash
python tools/clis/pubmed_search.py "query" --api-key YOUR_API_KEY
```

## Agent Integration Issues

### Skill Not Triggering

**Symptom:** Agent doesn't use skill when expected

**Possible Causes:**
1. Description lacks trigger phrases
2. Skill not installed correctly
3. Agent context mismatch

**Solutions:**

1. **Check description includes trigger phrases:**
   ```yaml
   ---
   name: my-skill
   description: Use when user mentions X, asks about Y, or needs Z
   ---
   ```

2. **Verify skill is installed:**
   ```bash
   ls .agents/skills/
   ls .claude/skills/
   ```

3. **Test with explicit invocation:**
   ```
   /my-skill
   ```

### Context Not Persisting

**Symptom:** Radiology context not available across sessions

**Possible Causes:**
1. Context file not created
2. Wrong context file location
3. Permission issues

**Solutions:**

```bash
# Check context file exists
ls .agents/radiology-context.json
ls .claude/radiology-context.json
ls ./radiology-context.json

# Recreate context
# Ask agent: "Initialize radiology context with PACS at localhost:8042"
```

### Skill Returns Wrong Output

**Symptom:** Skill provides incorrect or incomplete information

**Possible Causes:**
1. Skill logic error
2. Missing related context
3. Outdated documentation

**Solutions:**

1. **Check related skills are loaded:**
   - Always load `radiology-context` first
   - Check skill's "Related Skills" section

2. **Verify skill version:**
   ```bash
   git log --oneline skills/{category}/{skill-name}/SKILL.md
   ```

3. **Report issue:**
   - Open GitHub issue with details
   - Include: skill name, input, expected output, actual output

## GitHub Actions Issues

### Validation Workflow Fails

**Symptom:** GitHub Actions validate-skill workflow fails

**Common Causes:**
1. Frontmatter validation error
2. Line count exceeded
3. Missing required fields

**Solutions:**

1. **Run validation locally first:**
   ```bash
   ./scripts/validate-skills.sh
   ```

2. **Check workflow logs in GitHub Actions tab**
3. **Fix issues locally, push fix**

### Security Workflow Fails

**Symptom:** GitHub Actions security-baseline workflow fails

**Common Causes:**
1. Actual secrets detected (not false positives)
2. PHI patterns found
3. Frontmatter errors

**Solutions:**

1. **Run security check locally:**
   ```bash
   node .github/scripts/security-baseline.js security-report.json
   cat security-report.json | jq '.skills[] | select(.securityStatus != "verified")'
   ```

2. **Review flagged items:**
   - If legitimate: Update patterns to exclude
   - If actual issue: Remove or redact

3. **Re-run workflow:**
   - Push fix to trigger workflow
   - Or manually re-run from GitHub Actions tab

## Performance Issues

### Validation Script Slow

**Symptom:** `./scripts/validate-skills.sh` takes >30 seconds

**Possible Causes:**
1. Large number of skills
2. Disk I/O bottleneck
3. Sequential processing

**Solutions:**

1. **Validate specific skill only:**
   ```bash
   ./scripts/validate-skills.sh skills/{category}/{skill-name}
   ```

2. **Optimization planned in Phase 2** (parallel processing)

### Security Check Slow

**Symptom:** Security baseline takes >2 minutes

**Status:** Optimization planned in Phase 2 (parallel analysis)

**Workaround:** Run on specific skills only (modify script)

## Getting Help

### Still Stuck?

1. **Check existing issues:** https://github.com/aizech/clinical-skills/issues
2. **Search documentation:**
   - [README.md](../README.md)
   - [DEVELOPMENT.md](DEVELOPMENT.md)
   - [CLAUDE.md](../CLAUDE.md)
3. **Open new issue:**
   - Include: OS, tool versions, error messages, steps to reproduce
4. **Ask in discussions:** https://github.com/aizech/clinical-skills/discussions

### Reporting Bugs

When reporting bugs, include:

- **Environment:** OS, Python/Node version
- **Steps to reproduce:** Exact commands or inputs
- **Expected behavior:** What should happen
- **Actual behavior:** What actually happened
- **Error messages:** Full error output
- **Logs:** Relevant logs if available

### Feature Requests

For feature requests:
1. Check existing issues first
2. Describe use case clearly
3. Explain why it's important
4. Suggest implementation approach if known
