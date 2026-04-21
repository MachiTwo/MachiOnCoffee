---
title: Context Engine
slug: context-engine
date: "2026-04-19T09:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - concepts
  - context
  - context-engine
  - mcp
  - vectora
---

{{< lang-toggle >}}
The Context Engine is the heart of Vectora's orchestration. It decides **what, how, and when** to fetch context from your codebase, avoiding noise and overfetch.

> [!IMPORTANT] Context Engine is not just search. It is an intelligent pipeline: **Embed → Search → Rerank → Compose → Validate**.

## The Problem

Generic agents return 50 irrelevant files for a simple query. The Context Engine filters by relevance, reducing this to 5-10 highly useful chunks.

## Search Strategies

The Context Engine offers three search strategies, either independent or combined, depending on the query type and desired precision.

## Semantic

Uses embeddings to find functional similarity. Ideal for queries like "How to validate tokens?"

## Structural

Uses AST parsing for code relationships. Ideal for "Which functions call X?"

## Hybrid

Combines semantic + structural search. Ideal for module refactoring.

## Pipeline

1. **Embedding**: Query → 1024D vector (Voyage 4)
2. **Search**: Qdrant with filters by namespace
3. **Reranking**: Voyage Rerank 2.5 refines top-50 to top-10
4. **Compaction**: head/tail reduction without losing context
5. **Validation**: Guardian + Harness validate the output

## Configuration

```yaml
context_engine:
  strategy: "auto"
  max_depth: 3
  compaction: true
  include_ast: true
  include_dependencies: true
```

## Practical Examples

Below are two detailed examples showing how the Context Engine processes queries and returns structured context.

## Example 1: Semantic Search

**Query**: "How to validate tokens?"

```text
Input:
  - Query: "How to validate tokens?"
  - Strategy: semantic
  - Namespace: your-project
  - Top-k: 10

Processing:
  1. Embed: Query → 1536D vector via Voyage 4
  2. Search: HNSW searches for 100 closest candidates
  3. Rerank: Voyage Rerank 2.5 refines to top-10
  4. Compaction: Reduces size from 15KB → 4KB while maintaining context
  5. Validate: Harness validates output, captures metrics

Output:
  chunks: [
    {file: "src/auth/jwt.ts", precision: 0.89, content: "...validateToken..."},
    {file: "src/auth/guards.ts", precision: 0.78, content: "...middleware..."},
    ...
  ]
  metadata: {
    retrieval_precision: 0.87,
    latency_ms: 234,
    total_searched: 3159,
    compaction_ratio: 0.27
  }
```

## Example 2: Structural Search

**Query**: "Who calls getUserById?"

```text
Input:
  - Symbol: getUserById
  - Strategy: structural
  - Include indirect: true

Processing:
  1. AST Parse: Analyzes file where getUserById is defined
  2. Call Graph: Finds all references (direct + indirect)
  3. Context: Extracts context lines for each call

Output:
  direct_calls: 47
  indirect_calls: 12
  callers: [
    {file: "src/middleware/auth.ts", line: 34, type: "direct"},
    {file: "src/routes/profile.ts", line: 12, type: "indirect via getUserData"},
    ...
  ]
```

---

> **Next**: [Harness Runtime](./harness-runtime.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
