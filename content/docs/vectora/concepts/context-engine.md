---
title: Context Engine
slug: context-engine
date: "2026-04-19T09:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - concepts
  - context-engine
  - rag
  - search
  - semantic
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

O Context Engine é o coração da orquestração do Vectora. Ele decide **o quê, como e quando** buscar contexto em seu codebase, evitando ruído e overfetch.

> [!IMPORTANT]
> Context Engine não é apenas busca. É um pipeline inteligente: **Embed → Search → Rerank → Compose → Validate**.

---

## O Problema

Agents genéricos retornam 50 arquivos irrelevantes para uma query simples. O Context Engine filtra por relevância, reduzindo para 5-10 chunks altamente úteis.

---

## Estratégias de Busca

O Context Engine oferece três estratégias de busca independentes ou combinadas, dependendo do tipo de consulta e precisão desejada.

### Semântica

Usa embeddings para encontrar similaridade funcional. Ideal para "Como validar tokens?"

### Estrutural

Usa AST parsing para relações de código. Ideal para "Que funções chamam X?"

### Híbrida

Combina semântica + estrutura. Ideal para refatoração de módulos.

---

## Pipeline

1. **Embedding**: Query → vetor 1024D (Voyage 4)
2. **Search**: Qdrant com filters por namespace
3. **Reranking**: Voyage Rerank 2.5 refina top-50 para top-10
4. **Compaction**: head/tail reduz tamanho sem perder contexto
5. **Validação**: Guardian + Harness validam saída

---

## Configuração

```yaml
context_engine:
  strategy: "auto"
  max_depth: 3
  compaction: true
  include_ast: true
  include_dependencies: true
```

---

## Exemplos Práticos

Abaixo estão dois exemplos detalhados mostrando como o Context Engine processa queries e retorna contexto estruturado.

### Exemplo 1: Busca Semântica

**Query**: "Como validar tokens?"

```text
Input:
  - Query: "Como validar tokens?"
  - Strategy: semantic
  - Namespace: seu-projeto
  - Top-k: 10

Processamento:
  1. Embed: Query → vetor 1536D via Voyage 4
  2. Search: HNSW busca 100 candidatos mais próximos
  3. Rerank: Voyage Rerank 2.5 refina para top-10
  4. Compaction: Reduz tamanho de 15KB → 4KB mantendo contexto
  5. Validate: Harness valida output, captura métricas

Output:
  chunks: [
    {file: "src/auth/jwt.ts", precision: 0.89, content: "...validateToken..."},
    {file: "src/auth/guards.ts", precision: 0.78, content: "...middleware..."},
    ...
  ]
  metadata: {
    retrieval_precision: 0.87,
    latency_ms: 234,
    total_searched: 3159,
    compaction_ratio: 0.27
  }
```

### Exemplo 2: Busca Estrutural

**Query**: "Quem chama getUserById?"

```text
Input:
  - Symbol: getUserById
  - Strategy: structural
  - Include indirect: true

Processamento:
  1. AST Parse: Analisa arquivo onde getUserById é definido
  2. Call Graph: Encontra todas as referências (diretas + indiretas)
  3. Context: Extrai linhas de contexto de cada chamada

Output:
  direct_calls: 47
  indirect_calls: 12
  callers: [
    {file: "src/middleware/auth.ts", line: 34, type: "direct"},
    {file: "src/routes/profile.ts", line: 12, type: "indirect via getUserData"},
    ...
  ]
```

---

> **Próximo**: [Harness Runtime](./harness-runtime.md)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
