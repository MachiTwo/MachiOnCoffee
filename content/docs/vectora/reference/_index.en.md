---
title: Reference
slug: reference
date: "2026-04-19T10:10:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - architecture
  - concepts
  - reference
  - system
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}
Vectora is a **modular layered architecture** that combines embedding (Voyage), search (Qdrant), reranking (Voyage), and reasoning (Gemini) to provide intelligent and governed context.

```text
┌─────────────────────────────────────────────────────┐
│ IDEs (Claude Code, Cursor, VS Code) │
└────────────────────┬────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────┐
│ Vectora MCP Server │
│ (search_context, analyze_dependencies, etc) │
└────────┬──────────────────────────────────────────┬─┘
         │ │
         ▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ Context Engine │ │ Harness Runtime │
│ - Embedding (V4) │ │ - Pre-execution │
│ - Search (HNSW) │ │ - Validation │
│ - Reranking (V2.5) │ │ - Metrics │
└────────┬─────────────┘ └──────────┬───────────┘
         │ │
         ▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ Guardian Blocklist │ │ RBAC System │
│ - Path isolation │ │ - 5 roles │
│ - Trust folder │ │ - 15 permissions │
│ - Pattern matching │ │ - User management │
└────────┬─────────────┘ └──────────┬───────────┘
         │ │
         ▼──────────────┬───────────────────▼
                        │
                        ▼
            ┌──────────────────────┐
            │ Qdrant Vector DB │
            │ - Collections │
            │ - HNSW Index │
            │ - Namespaces │
            │ - Metadata Filters │
            └──────────────────────┘
                        │
                        ▼
            ┌──────────────────────┐
            │ File Storage │
            │ - Trust folder │
            │ - Vector index │
            │ - Cache (.vectora) │
            └──────────────────────┘
```

## Layers

Vectora's architecture is organized into four main layers that ensure everything from the user interface to secure data persistence.

## 1. Integration Layer (IDEs)

Where the user interacts with Vectora:

- **Claude Code**: Native MCP
- **Cursor**: Native MCP
- **VS Code**: Own extension
- **ChatGPT**: Custom GPT Plugin
- **CLI**: Direct commands

## 2. MCP Server Layer

This layer acts as the communication brain, following the Model Context Protocol open standard to ensure full interoperability.

```typescript
// MCP Tool example
tool: {
  name: "search_context",
  inputSchema: { /* JSON Schema */ }
}
```

Converts requests into Context Engine calls.

## 3. Core Logic Layer

Here resides the system's intelligence, where context is processed, validated, and governed before reaching the tool executor.

## Context Engine

Orchestrates intelligent search:

1. **Embedding**: Text → vector (Voyage 4, 1536D)
2. **Search**: HNSW search in Qdrant (top-100)
3. **Reranking**: Refines top-100 → top-10 (Voyage Rerank 2.5)
4. **Compaction**: Reduces size while maintaining context (head/tail)
5. **Validation**: Harness validates output

## Harness Runtime

Protection and validation:

- **Pre-execution**: Guardian checks, rate limit, preconditions
- **Execution**: Wrapped tool call with timeout/retry
- **Post-execution**: Validation, metrics, comparison mode

## Guardian Blocklist

Hard-coded security:

- **Trust Folder**: `/absolute/path/to/src` is the perimeter
- **Path Isolation**: Directory traversal blocked
- **Pattern Matching**: Regex rules for blocking
- **Audit Logging**: All attempts recorded

## RBAC (Role-Based Access Control)

5 hierarchical levels:

```text
Owner
  ├─ Edit namespace, manage users
  ├─ Admin
  │ ├─ Configure server, manage keys
  │ ├─ Editor
  │ │ ├─ Index, search, analyze
  │ │ ├─ Viewer
  │ │ │ └─ Search only
  │ │ └─ Guest
  │ │ └─ Limited search (rate limited)
```

15 granular permissions: `search`, `index`, `delete`, `configure`, etc.

## 4. Storage Layer

The storage layer ensures that vector indices and metadata are persisted securely and efficiently at a local or distributed level.

## Qdrant (Vector Database)

- **Collections**: One per namespace
- **HNSW**: Hierarchical Navigable Small World
- **Metadata Filtering**: Pre-filtering by namespace
- **Quantization**: Dimensionality reduction (4x faster)

```yaml
collection: "your-namespace"
vectors:
  size: 1536
  distance: cosine
  hnsw:
    m: 16
    ef_construct: 200
    ef_search: 150
```

## Local Storage

- **Indexing State**: `.vectora/` (cache)
- **Configuration**: `vectora.config.yaml`
- **Credentials**: `~/.vectora/credentials.enc` (encrypted)
- **AGENTS.md**: Agent memory (json-in-frontmatter)

## Data Flow

Data flow in Vectora is optimized for ultra-low latency, ensuring that context is retrieved and validated in milliseconds.

## Semantic Search

```text
1. User Query
   "How to do authentication?"
        ▼
2. Embedding (Voyage 4)
   [0.12, 0.45, ..., 0.67] (1536D)
        ▼
3. Vector Search (HNSW/Qdrant)
   Top-100 chunks by cosine similarity
        ▼
4. Reranking (Voyage Rerank 2.5)
   Refines to top-10 (semantic relevance)
        ▼
5. Compaction
   Head (first lines) + Tail (last lines)
   Maintains context, reduces tokens
        ▼
6. Validation (Harness)
   - Output schema
   - Security checks
   - Metrics captured
        ▼
7. Response
   {chunks: [...], precision: 0.87}
        ▼
8. To IDE
   Claude/Cursor/VS Code receive chunks
```

## Rate Limiting & SLA

```text
Request → Guardian (check blocklist) →
Rate Limiter (60 req/min free tier) →
Timeout (30s default) →
Retry (3 attempts) →
Circuit Breaker (fail-open after 5 errors)
```

## Key Components

| Component        | Function             | Provider           |
| ---------------- | -------------------- | ------------------ |
| **Embedding**    | Convert text→vector  | Voyage 4           |
| **Vector Store** | Store/search vectors | Qdrant             |
| **Reranking**    | Refine relevance     | Voyage Rerank 2.5  |
| **LLM**          | Reasoning + analysis | Gemini 3 Flash     |
| **Auth**         | Token validation     | JWT + RBAC         |
| **Namespace**    | Logical isolation    | Qdrant collections |
| **Trust Folder** | Path isolation       | Guardian           |

## System Configuration

```yaml
# vectora.config.yaml
project:
  name: "Your Project"
  namespace: "your-namespace"
  trust_folder: "./src"

providers:
  embedding:
    name: "voyage"
    model: "voyage-4"
  reranker:
    name: "voyage"
    model: "voyage-rerank-2.5"
  llm:
    name: "gemini"
    model: "gemini-3-flash"

context_engine:
  strategy: "semantic"
  max_depth: 3
  timeout_ms: 2000

harness:
  enabled: true
  pre_execution:
    validate_guardian: true
    rate_limit_per_minute: 60
  post_execution:
    validate_output: true
    capture_metrics: true

guardian:
  rules:
    - pattern: "^(src|docs)/"
      action: "allow"
    - pattern: "\.env.*"
      action: "block"

rbac:
  roles:
    - owner
    - admin
    - editor
    - viewer
    - guest
```

## Performance Targets

| Metric                  | Target | Typical |
| ----------------------- | ------ | ------- |
| **Search Latency**      | <500ms | ~234ms  |
| **Embedding**           | <200ms | ~120ms  |
| **Reranking**           | <100ms | ~50ms   |
| **Retrieval Precision** | ≥ 0.65 | ~0.78   |
| **Tool Accuracy**       | ≥ 0.95 | ~0.98   |
| **Security Events**     | 0      | 0       |
| **Availability**        | 99.9%  | 99.95%  |

## Scalability

## Horizontal

- **Multiple Qdrant clusters**: For physical isolation
- **Load balancing**: Between MCP servers
- **Read replicas**: For large-scale search

## Vertical

- **Quantization**: Reduces size by 4x
- **Compaction**: Reduces output by 50%
- **Caching**: Local result in `.vectora/`

## Security

## Defense in Depth

```text
1. Trust Folder (path isolation)
2. Guardian Blocklist (pattern matching)
3. RBAC (user-level permissions)
4. Harness (pre/post execution validation)
5. Audit Logging (who did what)
6. Encryption (API keys, tokens)
```

## Data Privacy

- BYOK (Bring Your Own Key): You control the keys
- Local processing: Embeddings are calculated locally
- No data sync: Code never leaves your server
- Audit trail: Complete and immutable

---

> **Next**: [Plans - Free](../plans/free.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
