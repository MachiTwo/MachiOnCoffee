---
title: Config YAML
slug: config-yaml
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - config
  - mcp
  - vectora
  - yaml
---

{{< lang-toggle >}}

Referência completa de configuração: esquema YAML, variáveis de ambiente, validação e exemplos.

### Full Schema

```yaml
# Project metadata
project:
  name: "Project Name"
  namespace: "org-project-env"
  trust_folder: "./src"
  description: "Optional"

# Indexing
indexing:
  paths:
    - "./src/**/*.ts"
    - "./docs/**/*.md"
  exclude:
    - "node_modules/**"
    - ".git/**"
    - "*.test.ts"
  auto_index: true
  on_save: true

# Providers
providers:
  embedding:
    name: "voyage"
    model: "voyage-4"
    api_key: "${VOYAGE_API_KEY}"
    fallback: "local"
  
  reranker:
    name: "voyage"
    model: "voyage-rerank-2.5"
    api_key: "${VOYAGE_API_KEY}"
  
  llm:
    name: "gemini"
    model: "gemini-3-flash"
    api_key: "${GEMINI_API_KEY}"
    fallback_model: "gemini-pro"

# Context Engine
context_engine:
  strategy: "semantic"  # semantic|structural|hybrid
  max_depth: 3
  max_tokens: 4096
  timeout_ms: 2000
  compaction: true
  include_ast: true

# Harness Runtime
harness:
  enabled: true
  pre_execution:
    validate_guardian: true
    validate_preconditions: true
    rate_limit_per_minute: 60
  execution:
    timeout_ms: 30000
    retry_attempts: 3
    circuit_breaker_threshold: 5
  post_execution:
    validate_output: true
    capture_metrics: true

# Guardian Security
guardian:
  enabled: true
  rules:
    - name: "block_env"
      pattern: "\.env.*"
      action: "deny"
    - name: "block_secrets"
      pattern: "secrets/.*"
      action: "deny"
    - name: "allow_src"
      pattern: "^src/"
      action: "allow"

# RBAC
rbac:
  enabled: true
  default_role: "viewer"

# Qdrant Vector DB
qdrant:
  url: "http://localhost:6333"
  api_key: "${QDRANT_API_KEY}"
  timeout_ms: 5000

# Logging
logging:
  level: "info"  # debug|info|warn|error
  format: "text"  # text|json
  file: ".vectora/logs/vectora.log"
  retention_days: 30

# Advanced
cache:
  enabled: true
  ttl_seconds: 3600
  max_size_mb: 500

metrics:
  enabled: true
  export_prometheus: false
  export_interval_seconds: 60
```

### Environment Variable Reference

```bash
GEMINI_API_KEY          # Google Gemini API key
VOYAGE_API_KEY          # Voyage AI API key
QDRANT_URL              # Qdrant cluster URL
QDRANT_API_KEY          # Qdrant API key (if auth)
VECTORA_NAMESPACE       # Override default namespace
VECTORA_TRUST_FOLDER    # Override trust folder
VECTORA_LOG_LEVEL       # Override log level
```

### Validation

```bash
vectora config validate
# ✅ All required fields present
# ✅ API keys configured
# ✅ Paths exist
```

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
