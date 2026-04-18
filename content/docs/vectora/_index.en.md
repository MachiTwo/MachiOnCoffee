---
title: "Vectora"
date: "2026-04-17T18:00:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

## The Problem

Traditional AI agents **hallucinate** because they operate in fragmented contexts, without structured understanding of
the codebase. A search for "authentication function" returns 50 disconnected results. The delivered context is shallow,
without understanding of flow, dependencies, or architectural patterns.

## The Solution: Vectora

**Vectora** solves this not by being "just another chat," but by being a **Contextual Knowledge Engine** that functions
as a **Tier 2 Sub-Agent**. It doesn't just retrieve code — it **understands structure, semantics, and relationships**
through:

- **AST-Aware Parsing**: Structural analysis using Tree-sitter, not text search
- **Connected RAG**: Retrieval that weaves fragments into coherent context
- **Context Engine**: Intelligent decider of _what_, _how_, and _when_ to fetch
- **Smart Reranking**: Ranks results by semantic relevance, not frequency

Vectora was born to be the intelligence layer that **connects the dots**, delivering what we call **Connected
Knowledge** — structured, multi-hop context, ready for the LLM to produce high-quality code.

## 📦 Official Stack

Vectora is built on these **officially curated and supported** technologies:

| Component            | Solution                    | Why                                                                 |
| -------------------- | --------------------------- | ------------------------------------------------------------------- |
| **LLM**              | Google Gemini 3 Flash       | 30ms latency, 90% cheaper, sufficient performance for code          |
| **Embeddings**       | Voyage AI 4                 | 1,536 dimensions, multimodal support (code + text), 98.5% precision |
| **Reranking**        | Voyage Rerank 2.5           | Cross-encoder precision, trained on code, <100ms latency            |
| **Vector DB**        | Qdrant Cloud                | HNSW with TurboQuant, payload filters, <50ms performance            |
| **Metadata & Auth**  | Supabase (PostgreSQL + RLS) | Namespace isolation, scalable, serverless                           |
| **API & Serverless** | Vercel Functions            | Global deploy, <100ms cold start, auto-scaling                      |

**Important note**: Vectora uses **ONLY** this stack. We don't support fallbacks to Voyage 3-large, Gemini Embedding
2.0, or alternative models. The choice was rigorous after months of benchmarking.

## 🏗️ Philosophy and Design

Vectora is more than a script — it's an **ecosystem** designed for low latency, high precision, and total security:

- **MCP & ACP Protocols**: Ultra-fast communication with IDEs (VS Code, JetBrains) and autonomous agents
- **Context Engine**: The "brain" that dynamically decides what to fetch, in what order, and at what depth
- **Guardian (Hard-Coded)**: Immutable blocklist at TypeScript binary level — never accesses `.env`, `.key`, `.pem`, or
  binaries
- **Harness (Validation)**: Quality assessment system with judge engine + vector comparison
- **Namespace Isolation**: Secure multi-tenant via Supabase RLS + Qdrant payload filtering

---

## 🚀 Where to Start?

- 📖 [**Getting Started**](getting-started/) — Set up Vectora in minutes, obtain your API keys
- 🏗️ [**Foundational Concepts**](concepts/) — Understand Connected RAG, embeddings, reranking, and the Context Engine
- 📚 [**Deep Architecture**](architecture/) — Deep dive into each system component
- 🛠️ [**API Reference**](api/) — Complete endpoint and payload documentation
- ❓ [**FAQ & Troubleshooting**](faq/) — Common questions and problem resolution
