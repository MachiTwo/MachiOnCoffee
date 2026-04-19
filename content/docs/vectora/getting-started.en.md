---
title: "Getting Started"
weight: 1
type: docs
---

{{< lang-toggle >}}

## Starting with Vectora

Vectora is designed to be plug-and-play yet extremely customizable.

### Installation

The Vectora runtime is developed in **TypeScript (Node.js 20+)**, using the **Vercel AI SDK**.

```bash
npx @kaffyn/vectora init
```

### Core Configuration

- **Context Engine**: Performs multi-hop reasoning and structural analysis via **AST (Tree-sitter)**.
- **Vector DB**: Native integration with **Qdrant Cloud** for scalable vector search.
- **Provider Router**: Stable and provider-agnostic support (OpenRouter, Google, Anthropic, OpenAI).

## Validation: Vectora Harness

How do you know if the AI has actually improved? Use the **Vectora Harness**:

1. **Measure Accuracy**: Objectively compares AI output with `vectora:on` vs `vectora:off`.
2. **Token Efficiency**: Optimizes retrieval to avoid "overfetch".
3. **Auditability**: Structured reports on how the agent used each tool.
