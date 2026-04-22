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
{{< section-toggle >}}

Vectora funciona com modelos de AI plugáveis para embeddings, reranking e LLM. Este guia cobre os modelos suportados e como customizar.

## Stack Padrão de Vectora

| Componente     | Modelo            | Provedor  | Docs                    |
| -------------- | ----------------- | --------- | ----------------------- |
| **LLM**        | Gemini 3 Flash    | Google AI | [→ Gemini](./gemini.md) |
| **Embeddings** | Voyage 4          | Voyage AI | [→ Voyage](./voyage.md) |
| **Reranker**   | Voyage Rerank 2.5 | Voyage AI | [→ Voyage](./voyage.md) |

## Modos de Operação

| Recurso              | Modo BYOK (Free)                | Modo Managed (Plus)      |
| :------------------- | :------------------------------ | :----------------------- |
| **Modelos Padrão**   | Gemini + Voyage                 | Gemini + Voyage          |
| **Gestão de Chaves** | Você fornece (BYOK)             | Gerenciado pela Vectora  |
| **Custo de IA**      | Pago ao provedor (ou Free tier) | Incluso no plano Vectora |
| **Configuração**     | Manual (`vectora config`)       | Automática (Zero Config) |
| **Privacidade**      | Chaves locais                   | Chaves gerenciadas       |

## Próximas Leituras

- [Gemini Configuration](./gemini.md) — Setup Google AI
- [Voyage Configuration](./voyage.md) — Setup Voyage AI
- [Conceitos](../concepts/embeddings.md) — Como embeddings funcionam

---

> Quer usar outro modelo? [Abra uma Issue](https://github.com/Kaffyn/Vectora/issues)

## External Linking

| Concept               | Resource                        | Link                                                                           |
| --------------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| **Voyage Embeddings** | Voyage Embeddings Documentation | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings) |
| **Voyage Reranker**   | Voyage Reranker API             | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)     |
| **Gemini API**        | Google AI Studio Documentation  | [ai.google.dev/docs](https://ai.google.dev/docs)                               |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
