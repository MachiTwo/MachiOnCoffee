---
title: Configuration
slug: configuration
date: "2026-04-19T08:15:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - configuration
  - yaml
  - environment
  - vectora
  - setup
---

{{< lang-toggle >}}

## Overview

Vectora configuration is controlled by:

1. **`vectora.config.yaml`** — Project configuration (local).
2. **Environment Variables** — Keys and credentials (global).
3. **CLI Commands** — Dynamic configuration via terminal.

---

## The `vectora.config.yaml` File

Created automatically with `vectora init`, this file controls the agent's behavior.

### Full Structure

```yaml
# Project Metadata
project:
  name: "My Project"
  id: "proj_auth_service"
  type: "codebase" # or 'documentation', 'api'
  description: "Auth backend in Go"

# Namespace and Security Configuration
namespace:
  id: "backend" # Logical isolation
  trust_folder: "." # Allowed root for operations
  visibility: "private" # 'private', 'team', 'public'

# AI Providers (Curated Stack)
providers:
  embedding:
    provider: "voyage"
    model: "voyage-4" # or fallback: "gemini-embedding-2"
    dimension: 1024
    batch_size: 32

  reranker:
    enabled: true
    provider: "voyage" # or "cohere", "local-bge"
    model: "voyage-rerank-2.5"

  llm:
    primary:
      provider: "gemini"
      model: "gemini-3-flash"
      temperature: 0.1
      max_tokens: 4096
    fallback:
      - provider: "openai"
        model: "gpt-4o"

# Context Engine (Intelligent RAG)
context_engine:
  strategy: "auto" # or 'semantic', 'structural', 'hybrid'
  max_depth: 3 # For multi-hop searches
  compaction: true
  include_ast: true # AST metadata
  include_dependencies: true # Import graph

# Security (Guardian + RBAC)
security:
  guardian:
    hard_blocklist:
      - ".env*"
      - "*.key"
      - "*.pem"
      - "*.crt"
      - "node_modules/**"
      - ".git/**"
    sanitize_output: true

  rbac:
    enabled: true
    roles:
      - name: "reader"
        permissions: ["context_search", "file_read", "plan_mode"]
      - name: "contributor"
        permissions: ["context_search", "file_read", "file_write", "context_ingest"]
      - name: "admin"
        permissions: ["*"]

# Indexing (Qdrant)
indexing:
  auto_ingest: true # Monitors file changes
  watch_patterns:
    - "src/**/*.{ts,js,go,py}"
    - "docs/**/*.md"
  ignore_patterns:
    - "node_modules/**"
    - ".git/**"
    - "*.test.*"
  chunk_size: 512 # Tokens per chunk
  overlap: 50 # Overlap between chunks

# Harness (Validation + Metrics)
harness:
  enabled: true
  validate_retrieval: true
  min_retrieval_score: 0.65
  validate_tool_calls: true

# Logging
logging:
  level: "info" # 'debug', 'info', 'warn', 'error'
  format: "json" # or 'text'
  output: "console" # or "file", "both"
```

---

## Environment Variables

### Mandatory

```bash
GEMINI_API_KEY=sk-xxx... # Google AI Studio
VOYAGE_API_KEY=pa-xxx... # Voyage AI
```

### Optional

```bash
VECTORA_NAMESPACE=my-project # Overrides vectora.config.yaml
VECTORA_TRUST_FOLDER=/path # Overrides trust_folder
VECTORA_LOG_LEVEL=debug # 'debug', 'info', 'warn', 'error'
VECTORA_CACHE_DIR=~/.vectora # Cache directory
QDRANT_URL=http://localhost:6333 # If using local Qdrant
SUPABASE_URL=https://xxx.supabase.co # For custom auth
```

### `.env` File

```bash
# .env (never commit!)
GEMINI_API_KEY=sk-xxx
VOYAGE_API_KEY=pa-xxx
VECTORA_NAMESPACE=backend
VECTORA_LOG_LEVEL=debug
```

Loaded automatically when running Vectora.

---

## CLI Configuration

### List Configuration

```bash
vectora config list
# Output:
# GEMINI_API_KEY: ••••••••••
# VOYAGE_API_KEY: ••••••••••
# VECTORA_NAMESPACE: my-project
```

### Set Values

```bash
# Interactive
vectora config set GEMINI_API_KEY

# Direct
vectora config set --key GEMINI_API_KEY --value sk-xxx

# Multiple values
vectora config set \
  --key VOYAGE_API_KEY --value pa-xxx \
  --key VECTORA_NAMESPACE --value backend
```

### Reset Configuration

```bash
vectora config reset --confirm
# Removes all local keys (does not affect .env)
```

---

## Configuration Examples by Use Case

### Case 1: Backend Project (Go/Rust)

```yaml
project:
  name: "Auth Service"
  type: "codebase"

providers:
  embedding:
    model: "voyage-4" # Specialized for code
  reranker:
    enabled: true

context_engine:
  strategy: "hybrid" # Code + documentation
  include_dependencies: true # Important for Go imports

indexing:
  watch_patterns:
    - "src/**/*.go"
    - "internal/**/*.go"
    - "*.md"
```

### Case 2: Technical Documentation

```yaml
project:
  name: "Technical Docs"
  type: "documentation"

providers:
  embedding:
    model: "qwen3-embedding" # Good for text
  reranker:
    enabled: true

indexing:
  watch_patterns:
    - "docs/**/*.md"
    - "guides/**/*.md"
```

### Case 3: Local Development (CPU Limited)

```yaml
providers:
  embedding:
    provider: "voyage"
    fallback: "gemini" # Fast fallback

  llm:
    primary:
      provider: "local"
      model: "qwen3-1.7b-instruct" # Running via Ollama
    fallback:
      - provider: "gemini"
        model: "gemini-3-flash"

context_engine:
  compaction: true # Save memory
  max_depth: 2 # Fewer hops

harness:
  enabled: false # Disable metrics for speed gain
```

---

## Configuration Validation

```bash
# Verify YAML syntax
vectora config validate

# Expected output:
# vectora.config.yaml is valid
# All required keys present
# Environment variables loaded
# API keys accessible
```

---

## Troubleshooting

### Error: `Config validation failed`

**Cause**: Invalid YAML file.

**Solution**: Validate at [yamllint.com](https://yamllint.com) or use:

```bash
yamllint vectora.config.yaml
```

### Error: `API key not found in environment`

**Cause**: Environment variables not loaded.

**Solution**:

```bash
# Verify if .env is in the correct directory
ls -la .env

# Load manually
export $(cat .env | xargs)
```

### Error: `Trust folder does not exist`

**Cause**: `trust_folder` points to an invalid directory.

**Solution**: Update in `vectora.config.yaml`:

```yaml
namespace:
  trust_folder: "." # or a valid path
```

---

## FAQ

**Q: Can I have multiple configurations for different projects?**
A: Yes. Create a `vectora.config.yaml` in each project directory. Vectora reads the file closest to the project root.

**Q: How do I use local models instead of APIs?**
A: Configure `provider: "local"` and install Ollama:

```bash
ollama pull qwen3:1.7b-instruct
# Then configure in vectora.config.yaml
```

**Q: Can I share `vectora.config.yaml`?**
A: Yes, commit it to git. Never commit `.env` or sensitive keys (use `.env.example` without values).

**Q: How do I reset the configuration?**
A: Use `vectora config reset --confirm`, or delete `~/.vectora/config.json`.

---

> **Next**: Configure your IDE in [Quickstart MCP](./quickstart-mcp.md).

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
