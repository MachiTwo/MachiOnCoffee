---
title: "Voyage AI: The Precision Behind Vectora"
slug: voyage
date: "2026-04-18T22:30:00-03:00"
draft: false
categories:
  - Deep Dive
tags:
  - ai
  - embeddings
  - flash
  - gemini
  - guardian
  - intelligence
  - mcp
  - rag
  - reranker
  - vector-search
  - vectora
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}

## The Heart of Vectora Retrieval: Voyage 4 & Rerank 2.5

While **Gemini 3 Flash** provides the reasoning, the precision of Vectora's search relies on **Voyage AI**. Specifically, we use **Voyage 4** for embeddings and **Voyage Rerank 2.5** to ensure that only the most relevant code snippets reach the LLM.

## Why Voyage AI?

We tested leading embedding models. Here is the reality for code retrieval:

### Embedding Model Comparison (Code Retrieval)

| Aspect                 | Voyage 4 | text-embedding-3-large | Cohere Embed-3 |
| ---------------------- | -------- | ---------------------- | -------------- |
| **Code Benchmarks**    | Top-1    | Top-3                  | Top-2          |
| **Dimensions**         | 1,536    | 3,072                  | 1,024          |
| **Max Tokens**         | 32K      | 8K                     | 8K             |
| **Latency**            | <50ms    | ~200ms                 | ~150ms         |
| **Cost per 1M tokens** | $0.02    | $0.13                  | $0.10          |

### Why Voyage Wins for Developers

1. **Code-Specific Tuning**: Voyage 4 is trained specifically on vast repositories of source code (Python, TS, Go, Rust), understanding complex syntax better than general-purpose models.
2. **Efficiency**: 1,536 dimensions provide the perfect balance between retrieval precision and storage cost.
3. **Large Window**: 32K token support allows for much larger "chunks" or files to be processed without losing context.
4. **Reranking Integration**: Voyage Rerank 2.5 works seamlessly with Voyage 4, reducing noise and increasing the "precision at 1" (P@1).

## Architecture: The Vector Pipeline

Vectora uses a two-stage retrieval pipeline:

### 1. Vector Search (Coarse Retrieval)

1. **Chunking**: Your code is split into optimized chunks with Tree-sitter awareness.
2. **Embedding**: Voyage 4 converts these chunks into high-dimensional vectors.
3. **Indexing**: Vectors are stored in a Qdrant HNSW index.
4. **Query**: When you search, your question is embedded, and Qdrant finds the top 50-100 nearest neighbors.

### 2. Reranking (Fine Filtering)

Vector search alone can return chunks that are semantically similar but technically irrelevant. Voyage Rerank 2.5 re-evaluates the top results:

- **Semantic Match**: Does this code actually solve the user's problem?
- **Contextual Relevance**: Is this the right file or just a similar syntax pattern?
- **Result**: The top 5 highest-scoring chunks are sent to Gemini.

## Benefits of Reranking

Without a reranker, the LLM often gets "confused" by similar-looking but incorrect code. Reranking provides:

- **Higher Quality**: Reduces hallucination by providing only true positives.
- **Lower Cost**: Reduces the tokens sent to the LLM by filtering out fluff.
- **Better UX**: Answers feel more "aware" of your specific project structure.

## Configuration

To use Voyage AI, ensure your `vectora.config.yaml` is configured:

```yaml
providers:
  embedding:
    name: "voyage"
    model: "voyage-4"
    api_key: "${VOYAGE_API_KEY}"

  reranker:
    name: "voyage"
    model: "voyage-rerank-2.5"
    api_key: "${VOYAGE_API_KEY}"
```

## Pricing & Quotas

Voyage AI is extremely cost-effective:

| Model             | Cost (per 1M tokens) |
| ----------------- | -------------------- |
| Voyage 4          | $0.02                |
| Voyage Rerank 2.5 | $2.00                |

Most small to medium projects cost less than **$1/month** in Voyage API fees on the Free plan (BYOK).

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
