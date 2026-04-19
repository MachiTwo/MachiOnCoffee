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

Entenda os pilares tecnológicos que sustentam o Vectora e como ele resolve o problema do contexto fragmentado em codebases complexos.

## 5 Pilares Essenciais

| Pilar               | O que é                               | Por que importa                                           | Link                                      |
| ------------------- | ------------------------------------- | --------------------------------------------------------- | ----------------------------------------- |
| **Context Engine**  | Busca semântica em código             | Encontra trechos relevantes sem palavras-chave exatas     | [→ Context Engine](./context-engine.md)   |
| **Embeddings**      | Vetores que representam significado   | Compara código por similaridade funcional, não lexical    | [→ Embeddings](./embeddings.md)           |
| **Reranker**        | Refinamento inteligente de resultados | Aumenta precisão de buscas para código específico         | [→ Reranker](./reranker.md)               |
| **Harness Runtime** | Orquestração segura de tools          | Valida, autoriza e executa operações no código            | [→ Harness Runtime](./harness-runtime.md) |
| **Trust Folder**    | Sandbox de filesystem                 | Protege contra directory traversal e vazamento de secrets | [→ Trust Folder](./trust-folder.md)       |

## Conceitos Técnicos Profundos

### Busca & Recuperação

- [**Vector Search**](./vector-search.md) — Como a busca vetorial funciona internamente
- [**Embeddings & Modelos**](./embeddings.md) — Voyage 4, dimensionalidade, métricas de distância
- [**Reranker**](./reranker.md) — Cross-encoder para refinamento de top-k

### Arquitetura & Runtime

- [**Harness Runtime**](./harness-runtime.md) — Guardian, Preconditions, Circuit Breaker, Workers
- [**Trust Folder**](./trust-folder.md) — Isolamento de path, symlink detection, BYOK
- [**Namespaces**](./namespaces.md) — Isolação lógica entre projetos/equipes

### Conceitos Avançados

- [**RAG (Retrieval-Augmented Generation)**](./rag.md) — Padrão de enriquecimento de contexto
- [**Sub-Agents**](./sub-agents.md) — Como Vectora coordena sub-agents
- [**State Persistence**](./state-persistence.md) — MongoDB como backend unificado

## Fluxo Completo: Query → Resposta

```text
1. IDE faz query via MCP ("Como validar tokens?")
   ↓
2. Context Engine → Converte em embedding via Voyage 4
   ↓
3. Vector Search → Busca top-100 chunks similares em MongoDB
   ↓
4. Reranker → Refina para top-5 resultados mais relevantes
   ↓
5. Harness Runtime → Valida permissões (RBAC) + Guardian checks
   ↓
6. Tool Executor → Retorna chunks ao IDE para LLM processar
```

## Para Iniciantes

1. Comece por [**Context Engine**](./context-engine.md) — Entenda a busca
2. Depois [**Vector Search**](./vector-search.md) — Técnica por trás
3. Por fim [**Harness Runtime**](./harness-runtime.md) — Segurança

## Para Arquitetos

1. [**Trust Folder**](./trust-folder.md) — Isolamento de dados
2. [**Namespaces**](./namespaces.md) — Isolação multi-tenant
3. [**Harness Runtime**](./harness-runtime.md) — Governança

---

> Dúvidas sobre um conceito? [GitHub Discussions](https://github.com/vectora/vectora/discussions)
