---
title: Reference
slug: reference
date: "2026-04-19T10:10:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - architecture
  - concepts
  - reference
  - system
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}
Vectora é uma **arquitetura modular** em camadas que combina embedding (Voyage), search (Qdrant), reranking (Voyage), e reasoning (Gemini) para fornecer contexto inteligente e governado.

```text
┌─────────────────────────────────────────────────────┐
│ IDEs (Claude Code, Cursor, VS Code) │
└────────────────────┬────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────┐
│ Vectora MCP Server │
│ (search_context, analyze_dependencies, etc) │
└────────┬──────────────────────────────────────────┬─┘
         │ │
         ▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ Context Engine │ │ Harness Runtime │
│ - Embedding (V4) │ │ - Pre-execution │
│ - Search (HNSW) │ │ - Validation │
│ - Reranking (V2.5) │ │ - Metrics │
└────────┬─────────────┘ └──────────┬───────────┘
         │ │
         ▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ Guardian Blocklist │ │ RBAC System │
│ - Path isolation │ │ - 5 roles │
│ - Trust folder │ │ - 15 permissions │
│ - Pattern matching │ │ - User management │
└────────┬─────────────┘ └──────────┬───────────┘
         │ │
         ▼──────────────┬───────────────────▼
                        │
                        ▼
            ┌──────────────────────┐
            │ Qdrant Vector DB │
            │ - Collections │
            │ - HNSW Index │
            │ - Namespaces │
            │ - Metadata Filters │
            └──────────────────────┘
                        │
                        ▼
            ┌──────────────────────┐
            │ File Storage │
            │ - Trust folder │
            │ - Vector index │
            │ - Cache (.vectora) │
            └──────────────────────┘
```

---

## Camadas

A arquitetura do Vectora é organizada em quatro camadas principais que garantem desde a interface com o usuário até a persistência segura dos dados.

## 1. Integration Layer (IDEs)

Onde o usuário interage com Vectora:

- **Claude Code**: MCP nativo
- **Cursor**: MCP nativo
- **VS Code**: Extension própria
- **ChatGPT**: Custom GPT Plugin
- **CLI**: Comandos diretos

## 2. MCP Server Layer

Esta camada atua como o cérebro da comunicação, seguindo o padrão aberto do Model Context Protocol para garantir interoperabilidade total.

```typescript
// Exemplo de tool MCP
tool: {
  name: "search_context",
  inputSchema: { /* JSON Schema */ }
}
```

Converte requisições em chamadas ao Context Engine.

## 3. Core Logic Layer

Aqui reside a inteligência do sistema, onde o contexto é processado, validado e governado antes de chegar ao executor de ferramentas.

## Context Engine

Orquestra busca inteligente:

1. **Embedding**: Texto → vetor (Voyage 4, 1536D)
2. **Search**: Busca HNSW em Qdrant (top-100)
3. **Reranking**: Refina top-100 → top-10 (Voyage Rerank 2.5)
4. **Compaction**: Reduz tamanho mantendo contexto (head/tail)
5. **Validation**: Harness valida output

## Harness Runtime

Proteção e validação:

- **Pre-execution**: Guardian checks, rate limit, preconditions
- **Execution**: Wrapped tool call com timeout/retry
- **Post-execution**: Validação, métricas, comparison mode

## Guardian Blocklist

Segurança hard-coded:

- **Trust Folder**: `/absolute/path/to/src` é o perímetro
- **Path Isolation**: Directory traversal bloqueado
- **Pattern Matching**: Regex rules para bloqueio
- **Audit Logging**: Todas as tentativas registradas

## RBAC (Role-Based Access Control)

5 níveis hierárquicos:

```text
Owner
  ├─ Edit namespace, manage users
  ├─ Admin
  │ ├─ Configure server, manage keys
  │ ├─ Editor
  │ │ ├─ Index, search, analyze
  │ │ ├─ Viewer
  │ │ │ └─ Search only
  │ │ └─ Guest
  │ │ └─ Limited search (rate limited)
```

15 permissões granulares: `search`, `index`, `delete`, `configure`, etc.

## 4. Storage Layer

A camada de armazenamento garante que os índices vetoriais e metadados sejam persistidos com segurança e eficiência em nível local ou distribuído.

## Qdrant (Vector Database)

- **Collections**: Um por namespace
- **HNSW**: Hierarchical Navigable Small World
- **Metadata Filtering**: Pre-filtering por namespace
- **Quantization**: Redução de dimensionalidade (4x mais rápido)

```yaml
collection: "seu-namespace"
vectors:
  size: 1536
  distance: cosine
  hnsw:
    m: 16
    ef_construct: 200
    ef_search: 150
```

## Local Storage

- **Indexing State**: `.vectora/` (cache)
- **Configuration**: `vectora.config.yaml`
- **Credentials**: `~/.vectora/credentials.enc` (criptografado)
- **AGENTS.md**: Agent memory (json-in-frontmatter)

---

## Data Flow

O fluxo de dados no Vectora é otimizado para latência ultra-baixa, garantindo que o contexto seja recuperado e validado em milissegundos.

## Busca Semântica

```text
1. User Query
   "Como fazer autenticação?"
        ▼
2. Embedding (Voyage 4)
   [0.12, 0.45, ..., 0.67] (1536D)
        ▼
3. Vector Search (HNSW/Qdrant)
   Top-100 chunks by cosine similarity
        ▼
4. Reranking (Voyage Rerank 2.5)
   Refina para top-10 (semantic relevance)
        ▼
5. Compaction
   Head (primeiras linhas) + Tail (últimas)
   Mantém contexto, reduz tokens
        ▼
6. Validation (Harness)
   - Output schema
   - Security checks
   - Metrics captured
        ▼
7. Response
   {chunks: [...], precision: 0.87}
        ▼
8. To IDE
   Claude/Cursor/VS Code recebem chunks
```

## Rate Limiting & SLA

```text
Request → Guardian (check blocklist) →
Rate Limiter (60 req/min free tier) →
Timeout (30s default) →
Retry (3 tentativas) →
Circuit Breaker (fail-open depois de 5 erros)
```

---

## Componentes-Chave

| Componente       | Função                   | Provider           |
| ---------------- | ------------------------ | ------------------ |
| **Embedding**    | Converter texto→vetor    | Voyage 4           |
| **Vector Store** | Armazenar/buscar vetores | Qdrant             |
| **Reranking**    | Refinar relevância       | Voyage Rerank 2.5  |
| **LLM**          | Reasoning + análise      | Gemini 3 Flash     |
| **Auth**         | Validação de tokens      | JWT + RBAC         |
| **Namespace**    | Isolamento lógico        | Qdrant collections |
| **Trust Folder** | Path isolation           | Guardian           |

---

## Configuração do Sistema

```yaml
# vectora.config.yaml
project:
  name: "Seu Projeto"
  namespace: "seu-namespace"
  trust_folder: "./src"

providers:
  embedding:
    name: "voyage"
    model: "voyage-4"
  reranker:
    name: "voyage"
    model: "voyage-rerank-2.5"
  llm:
    name: "gemini"
    model: "gemini-3-flash"

context_engine:
  strategy: "semantic"
  max_depth: 3
  timeout_ms: 2000

harness:
  enabled: true
  pre_execution:
    validate_guardian: true
    rate_limit_per_minute: 60
  post_execution:
    validate_output: true
    capture_metrics: true

guardian:
  rules:
    - pattern: "^(src|docs)/"
      action: "allow"
    - pattern: "\.env.*"
      action: "block"

rbac:
  roles:
    - owner
    - admin
    - editor
    - viewer
    - guest
```

---

## Performance Targets

| Métrica                 | Target | Típico |
| ----------------------- | ------ | ------ |
| **Search Latency**      | <500ms | ~234ms |
| **Embedding**           | <200ms | ~120ms |
| **Reranking**           | <100ms | ~50ms  |
| **Retrieval Precision** | ≥ 0.65 | ~0.78  |
| **Tool Accuracy**       | ≥ 0.95 | ~0.98  |
| **Security Events**     | 0      | 0      |
| **Availability**        | 99.9%  | 99.95% |

---

## Escalabilidade

## Horizontal

- **Múltiplos clusters Qdrant**: Para isolamento físico
- **Load balancing**: Entre servidores MCP
- **Read replicas**: Para busca em larga escala

## Vertical

- **Quantização**: Reduz tamanho em 4x
- **Compaction**: Reduz output em 50%
- **Caching**: Resultado local em `.vectora/`

---

## Segurança

## Defense in Depth

```text
1. Trust Folder (path isolation)
2. Guardian Blocklist (pattern matching)
3. RBAC (user-level permissions)
4. Harness (pre/post execution validation)
5. Audit Logging (quem fez o quê)
6. Encryption (API keys, tokens)
```

## Data Privacy

- BYOK (Bring Your Own Key): Você controla as chaves
- Local processing: Embeddings são calculados local
- No data sync: Código nunca deixa seu servidor
- Audit trail: Completo e imutável

---

> **Próximo**: [Plans - Free](../plans/free.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
