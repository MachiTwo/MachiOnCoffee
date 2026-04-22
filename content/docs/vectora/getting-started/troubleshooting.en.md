---
title: Troubleshooting
slug: troubleshooting
date: "2026-04-19T08:45:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - config
  - debug
  - embeddings
  - errors
  - gemini
  - getting-started
  - guardian
  - help
  - integration
  - mcp
  - rag
  - security
  - tools
  - troubleshooting
  - trust-folder
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}
Guide to solving the most frequent problems during installation, configuration, and use of Vectora.

## Installation

## Error: `npm: command not found`

**Cause**: Node.js is not installed or not in your PATH.

**Solution**:

```bash
# Install Node.js: https://nodejs.org (LTS recommended)
node --version # Should return v18+
npm --version # Should return 9+
```

## Error: `EACCES: permission denied`

**Cause**: Insufficient permission to install globally.

**Solution**:

```bash
# Configure npm for local installation
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Add the line above to your ~/.bashrc or ~/.zshrc
npm install -g @kaffyn/vectora
```

## Error: `vectora: command not found`

**Cause**: Vectora is installed but not in your PATH.

**Solution**:

```bash
# Verify installation
npm list -g @kaffyn/vectora

# Reinstall
npm install -g @kaffyn/vectora

# Test
vectora --version
```

## Configuration

## Error: `API key not found`

**Cause**: Environment variables not configured.

**Solution**:

```bash
# Verify if keys are defined
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# If empty, configure
export GEMINI_API_KEY="your_key_here"
export VOYAGE_API_KEY="your_key_here"

# Or create a .env file
cat > .env << 'EOF'
GEMINI_API_KEY=sk-xxx
VOYAGE_API_KEY=pa-xxx
EOF
```

## Error: `Config validation failed`

**Cause**: Invalid YAML syntax in `vectora.config.yaml`.

**Solution**:

```bash
# Validate YAML
yamllint vectora.config.yaml

# Or use online: https://yamllint.com

# Common errors:
# - Inconsistent indentation (use 2 spaces)
# - Missing quotes around values
# - Unescaped special symbols
```

## Error: `Trust folder does not exist`

**Cause**: The path in `trust_folder` does not exist.

**Solution**:

```yaml
# Update vectora.config.yaml
namespace:
  trust_folder: "." # or a valid path
```

## MCP Integration

## Error: `Vectora MCP server not found`

**Cause**: `claude_desktop_config.json` is poorly formatted.

**Solution**:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp-serve"]
    }
  }
}
```

Verify:

- JSON is valid (use [jsonlint.com](https://jsonlint.com))
- File is in correct location: `~/.claude/claude_desktop_config.json`
- Restart Claude Desktop after saving

## Error: `Connection refused`

**Cause**: Vectora cannot connect to the API.

**Solution**:

```bash
# Verify API keys
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# Test connectivity
curl https://generativelanguage.googleapis.com/v1beta/models

# If it fails, your key might be invalid
# Generate a new key at https://aistudio.google.com/app/apikey
```

## Claude does not use Vectora automatically

**Cause**: Claude does not detect that the tool is relevant.

**Solution**: Be explicit in your request:

```text
Use Vectora to search for context about authentication.
Search the codebase for JWT implementations.
```

## API & Providers

## Error: `403 Quota Exceeded (Gemini)`

**Cause**: Request limit exceeded (60/min on free tier).

**Solution**:

```bash
# Wait for quota reset (next minute)
# Or upgrade to Plus plan at https://vectora.dev/plans

# For debug: verify usage
vectora stats --provider gemini
```

## Error: `401 Unauthorized (Voyage)`

**Cause**: API key invalid or expired.

**Solution**:

```bash
# Generate new key at https://dash.voyageai.com/api-keys
vectora config set --key VOYAGE_API_KEY --value "new_key"

# Test
vectora test --provider voyage
```

## Error: `Network timeout`

**Cause**: Slow connection or API unavailable.

**Solution**:

```bash
# Increase timeout (default: 30s)
export VECTORA_TIMEOUT_MS=60000

# Test connectivity
ping generativelanguage.googleapis.com

# If using VPN/proxy:
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=https://proxy:port
```

## Indexing & RAG

## Error: `Project not found`

**Cause**: Namespace does not exist.

**Solution**:

```bash
# Initialize project
vectora init --name "My Project"

# Or specify in claude_desktop_config.json
"VECTORA_NAMESPACE": "my-project"
```

## Error: `No results found`

**Cause**: Codebase not indexed or irrelevant query.

**Solution**:

```bash
# Force reindexing
vectora ingest --project . --force

# Verify status
vectora status --project .

# Try a different or more specific query
# Example: instead of "auth", try "JWT validation in middleware"
```

## Very slow embedding

**Cause**: Large codebase or slow connection.

**Solution**:

```bash
# Use batch processing
vectora ingest --batch-size 16 # default: 32

# Or configure in vectora.config.yaml
indexing:
  batch_size: 16

# For local development, use fallback
providers:
  embedding:
    fallback: "local" # local embedding via ollama
```

## Performance

## Claude Desktop is slow

**Cause**: Too many simultaneous requests or large codebase.

**Solution**:

```bash
# Limit automatic indexing
vectora config set VECTORA_AUTO_INGEST=false

# Or schedule indexing for off-peak times
vectora schedule ingest --time 02:00 --recurring daily
```

## High memory usage

**Cause**: Large local cache or uncleaned indices.

**Solution**:

```bash
# Clear cache
vectora cache clear

# Reduce cache size
vectora config set VECTORA_CACHE_SIZE=100MB

# Verify consumption
vectora stats --memory
```

## Debug & Logging

## Activate debug mode

```bash
# Via CLI
vectora --log-level debug

# Via variable
export VECTORA_LOG_LEVEL=debug

# Save logs to file
vectora mcp-serve --log-file debug.log
```

## Get more information

```bash
# General status
vectora status

# Configuration details
vectora config list

# Usage statistics
vectora stats

# Verify indexing
vectora index --list --verbose
```

## Where to Seek Help

1. **Specific FAQs**:

   - [General FAQ](../faq/general.md)
   - [Security FAQ](../faq/security.md)
   - [Billing FAQ](../faq/billing.md)

2. **Documentation**:

   - [Configuration Guide](./configuration.md)
   - [MCP Integration](../integrations/claude-code.md)
   - [Security & Guardian](../security/guardian.md)

3. **Community**:

   - GitHub Issues: [vectora/issues](https://github.com/kaffyn/vectora/issues)
   - Discussions: [vectora/discussions](https://github.com/kaffyn/vectora/discussions)
   - Discord: [Vectora Community](https://discord.gg/vectora)

4. **Report Bug**:

   ```bash
   vectora bug-report --include-logs --include-config
   # Generates file with sanitized information to send
   ```

## FAQ

**Q: Where is my data?**
A: Locally in `.vectora/` (cache) and Qdrant (indexed embeddings). Kaffyn never accesses your raw code.

**Q: How to reset everything?**
A: Use `vectora reset --full --confirm`. This removes cache, indices, and local config.

**Q: Can I use Vectora without internet?**
A: Partially. Semantic search needs an API. File operations work offline.

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
