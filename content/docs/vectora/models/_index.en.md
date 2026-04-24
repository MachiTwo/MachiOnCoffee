---
title: Models
slug: models
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - byok
  - concepts
  - config
  - embeddings
  - gemini
  - models
  - privacy
  - reranker
  - vectora
  - voyage
---

{{< lang-toggle >}}

Vectora works with pluggable AI models for embeddings, reranking, and LLMs. This guide covers supported models and how to customize them.

## Vectora's Standard Stack

| Component      | Model             | Provider  | Docs                    |
| -------------- | ----------------- | --------- | ----------------------- |
| **LLM**        | Gemini 3 Flash    | Google AI | [→ Gemini](./gemini.md) |
| **Embeddings** | Voyage 4          | Voyage AI | [→ Voyage](./voyage.md) |
| **Reranker**   | Voyage Rerank 2.5 | Voyage AI | [→ Voyage](./voyage.md) |

## Operation Modes

| Feature             | BYOK Mode (Free)                | Managed Mode (Plus)      |
| :------------------ | :------------------------------ | :----------------------- |
| **Standard Models** | Gemini + Voyage                 | Gemini + Voyage          |
| **Key Management**  | You provide (BYOK)              | Managed by Vectora       |
| **AI Cost**         | Paid to provider (or Free tier) | Included in Vectora plan |
| **Setup**           | Manual (`vectora config`)       | Automatic (Zero Config)  |
| **Privacy**         | Local keys                      | Managed keys             |

## Next Readings

- [Gemini Configuration](./gemini.md) — Setup Google AI
- [Voyage Configuration](./voyage.md) — Setup Voyage AI
- [Concepts](../concepts/embeddings.md) — How embeddings work

---

> Want to use another model? [Open an Issue](https://github.com/Kaffyn/Vectora/issues)

## External Linking

| Concept               | Resource                        | Link                                                                           |
| --------------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| **Voyage Embeddings** | Voyage Embeddings Documentation | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings) |
| **Voyage Reranker**   | Voyage Reranker API             | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)     |
| **Gemini API**        | Google AI Studio Documentation  | [ai.google.dev/docs](https://ai.google.dev/docs)                               |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
