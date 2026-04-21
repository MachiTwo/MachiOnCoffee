---
title: Core Concepts
slug: concepts
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - concepts
  - embeddings
  - mcp
  - rag
  - reranker
  - trust-folder
  - vector-search
  - vectora
---

{{< lang-toggle >}}
Understand the technological pillars that underpin Vectora and how it solves the fragmented context problem in complex codebases.

## 5 Essential Pillars

| Pillar              | What it is                     | Why it matters                                            | Link                                      |
| ------------------- | ------------------------------ | --------------------------------------------------------- | ----------------------------------------- |
| **Context Engine**  | Semantic search for code       | Finds relevant snippets without exact keyword matches     | [→ Context Engine](./context-engine.md)   |
| **Embeddings**      | Vectors representing meaning   | Compares code by functional similarity, not lexical match | [→ Embeddings](./embeddings.md)           |
| **Reranker**        | Intelligent results refinement | Increases search precision for specific code blocks       | [→ Reranker](./reranker.md)               |
| **Harness Runtime** | Secure tools orchestration     | Validates, authorizes, and executes code operations       | [→ Harness Runtime](./harness-runtime.md) |
| **Trust Folder**    | Filesystem sandbox             | Protects against directory traversal and secrets leakage  | [→ Trust Folder](./trust-folder.md)       |

## Deep Technical Concepts

## Search & Retrieval

- [**Vector Search**](./vector-search.md) — How vector search works internally
- [**Embeddings & Models**](./embeddings.md) — Voyage 4, dimensionality, distance metrics
- [**Reranker**](./reranker.md) — Cross-encoder for top-k refinement
- [**Local Reranker**](./reranker-local.md) — Intelligent retrieval without VectorDB, ideal for mutable data

## Architecture & Runtime

- [**Harness Runtime**](./harness-runtime.md) — Guardian, Preconditions, Circuit Breaker, Workers
- [**Trust Folder**](./trust-folder.md) — Path isolation, symlink detection, BYOK
- [**Namespaces**](./namespaces.md) — Logical isolation between projects/teams

## Advanced Concepts

- [**RAG (Retrieval-Augmented Generation)**](./rag.md) — Context enrichment pattern
- [**Sub-Agents**](./sub-agents.md) — How Vectora coordinates sub-agents
- [**State Persistence**](./state-persistence.md) — MongoDB as unified backend

## Full Flow: Query → Response

```text
1. IDE makes a query via MCP ("How to validate tokens?")
   ↓
2. Context Engine → Converts to embedding via Voyage 4
   ↓
3. Vector Search → Searches for top-100 similar chunks in MongoDB
   ↓
4. Reranker → Refines to top-5 most relevant results
   ↓
5. Harness Runtime → Validates permissions (RBAC) + Guardian checks
   ↓
6. Tool Executor → Returns chunks to IDE for LLM processing
```

## For Beginners

1. Start with [**Context Engine**](./context-engine.md) — Understand the search
2. Then [**Vector Search**](./vector-search.md) — The technique behind it
3. Finally [**Harness Runtime**](./harness-runtime.md) — Security

## For Architects

1. [**Trust Folder**](./trust-folder.md) — Data isolation
2. [**Namespaces**](./namespaces.md) — Multi-tenant isolation
3. [**Harness Runtime**](./harness-runtime.md) — Governance

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
