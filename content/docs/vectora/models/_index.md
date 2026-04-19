---
title: Models
slug: models
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - embeddings
  - gemini
  - models
  - voyage
  - vectora
---

{{< lang-toggle >}}

Vectora funciona com modelos de AI plugáveis para embeddings, reranking e LLM. Este guia cobre os modelos suportados e como customizar.

## Stack Padrão de Vectora

| Componente     | Modelo            | Provedor  | Docs                    |
| -------------- | ----------------- | --------- | ----------------------- |
| **LLM**        | Gemini 3 Flash    | Google AI | [→ Gemini](./gemini.md) |
| **Embeddings** | Voyage 4          | Voyage AI | [→ Voyage](./voyage.md) |
| **Reranker**   | Voyage Rerank 2.5 | Voyage AI | [→ Voyage](./voyage.md) |

## Comparação: Vectora vs Alternativas

| Aspecto        | Vectora (Gemini + Voyage) | OpenAI            | Anthropic            | Cohere            |
| -------------- | ------------------------- | ----------------- | -------------------- | ----------------- |
| **LLM**        | Gemini 3 Flash            | GPT-4             | Claude 3.5           | Command R+        |
| **Embeddings** | Voyage 4                  | text-embedding-3  | Claude embeddings    | Embed-3           |
| **Reranker**   | Voyage Rerank 2.5         | Nenhum            | Nenhum               | Rerank 3          |
| **BYOK**       | Obrigatório               | Chaves via OpenAI | Chaves via Anthropic | Chaves via Cohere |
| **Latência**   | <300ms                    | ~500ms            | ~600ms               | ~400ms            |

## Customização: Usar Outros Modelos

Vectora suporta qualquer embedding via **Ollama**, **LM Studio**, ou **Hugging Face**:

```yaml
# .vectora/config.yaml
embeddings:
  provider: ollama
  model: nomic-embed-text
  endpoint: http://localhost:11434
```

Recomendações por caso:

| Caso              | Modelo Recomendado          |
| ----------------- | --------------------------- |
| **Code** (Padrão) | Voyage 4 (treino em código) |
| **Português**     | Multilingual-e5-large       |
| **Edge/Local**    | nomic-embed-text (Ollama)   |
| **Speed**         | bge-small-en-v1.5           |

## Próximas Leituras

- [Gemini Configuration](./gemini.md) — Setup Google AI
- [Voyage Configuration](./voyage.md) — Setup Voyage AI
- [Conceitos](../concepts/embeddings.md) — Como embeddings funcionam

---

> Quer usar outro modelo? [Abra uma Issue](https://github.com/vectora/vectora/issues)
