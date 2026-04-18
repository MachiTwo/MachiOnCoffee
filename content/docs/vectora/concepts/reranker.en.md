---
title: "Reranker: Why similarity isn't enough for code"
date: 2026-04-17T21:10:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["reranker", "rag", "ai", "vectora"]
---

Often, a vector search (Embedding) returns 50 files that "look" relevant, but only 3 are actually useful for fixing the
bug. Sending all 50 to the LLM is a waste of tokens and can confuse the AI. This is where the **Reranker** comes in.

## The Precision Filter

While Embedding is excellent at quickly finding candidates in a giant database, it often brings a lot of noise (like
test files or boilerplates that use the same words).

The **Reranker** is a slower, "deeper" AI model that analyzes only those 50 candidates and your original question. It
performs a direct cross-match (cross-attention) to reorder the list, putting what is **crucial** at the top.

## Why does Vectora require a Reranker?

In code, precision is prefix. A context error can lead to a disastrous refactor. The [Vectora](/en/04/17/vectora/)
pipeline uses models like **Cohere Rerank v3.5** or **Voyage Rerank 2** to:

1. **Eliminate Noise**: Ignores files that are semantically close but functionally irrelevant.
2. **Prioritize Dependencies**: If you ask about an error, the Reranker understands that the log file and the error
   handling logic should come before a `README` file.
3. **Token Efficiency**: By filtering only the truly relevant "Top N," Vectora saves up to 40% in API costs.

## The Context Trinity

[Vectora](/en/04/17/vectora/) orchestrates the perfect trinity:

1. **Embedding**: Finds the candidates.
2. **Reranker**: Filters the relevant ones.
3. **LLM**: Acts on the refined context.

---

_This is a supporting post for the [Vectora](/en/docs/vectora/) project._
