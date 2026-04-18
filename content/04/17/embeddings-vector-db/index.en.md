---
title: "Embeddings and Vector DBs: The heart of semantic search"
date: 2026-04-17T21:05:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["embeddings", "qdrant", "ai", "vectora"]
---

If you want a computer to understand that `create_user` and `signUp` have similar meanings, you need **Embeddings**.

## What are Embeddings?

Embeddings are lists of numbers (vectors) that represent the meaning of a text in a multidimensional space.

Imagine a map where words with similar meanings are "close" to each other. In the world of 2026 AI models (like
[Voyage-3 or Qwen3-Embedding](/en/04/17/vectora/)), this map has thousands of dimensions, allowing it to capture subtle
nuances of programming logic.

## Vector Databases (Vector DBs)

A standard database (SQL) is great for searching by exact match (`WHERE id = 10`). A **Vector DB** is specialized in
searching by **proximity**.

In Vectora, we use **Qdrant Cloud**, which stands out for:

- **HNSW (Hierarchical Navigable Small World)**: An ultra-fast search algorithm that organizes vectors into layers,
  allowing it to find the "nearest neighbor" in milliseconds, even in databases with millions of files.
- **Quantization (TurboQuant)**: A technique that reduces vector size to save memory and speed up searches without
  losing precision.

## Why is this vital for Vectora?

Without a vector database, your AI agent would have to read all your project files every time it received a question.
This would be slow and absurdly expensive.

With Embeddings + Qdrant, [Vectora](/en/04/17/vectora/) can:

1. "Remember" your entire codebase instantly.
2. Find code based on **intent**, not just keywords.
3. Isolate contexts through **Namespaces**, ensuring search is fast and secure.

---

_This is a supporting post for the [Vectora](/en/04/17/vectora/) project._
