---
title: Harness Runtime
slug: harness-runtime
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - auth
  - concepts
  - config
  - embeddings
  - errors
  - guardian
  - harness
  - harness-runtime
  - mcp
  - persistence
  - protocol
  - reranker
  - runtime
  - security
  - tools
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}
Harness Runtime é o módulo de **validação e proteção** que roda imediatamente antes e depois da execução de ferramentas. Ele captura falhas silenciosas, verifica segurança e mede qualidade.

> [!IMPORTANT] Harness não tolera erros silenciosos. Se uma ferramenta falha, Harness para e reporta. Se um Guardian check falha, a execução é bloqueada.

## O Problema

Agentes genéricos executam ferramentas "cegamente":

- Sem validar se a saída é relevante
- Sem checar se houve violação de segurança
- Sem medir latência ou qualidade

Resultado: respostas confiantes sobre dados inválidos, brechas de segurança, e token waste.

## Arquitetura

O Harness Runtime implementa três fases de proteção: validação antes da execução, execução envolvida com resiliência, e validação pós-execução com métricas.

## Pre-Execution

Antes de rodar qualquer ferramenta:

1. **Guardian Check**: Valida permissões contra blocklist
2. **Preconditions**: Verifica variáveis de ambiente, API keys, namespaces
3. **Rate Limit**: Verifica quota de requisições por minuto
4. **Input Validation**: Sanitiza strings, arrays e estruturas

## Tool Execution (Wrapped)

A ferramenta roda com:

- **Timeout**: Máximo de 30s por padrão (configurável)
- **Retry Logic**: Até 3 tentativas em falhas transitórias
- **Streaming**: Output é buffered em chunks de 4KB
- **Circuit Breaker**: Falhas repetidas disparam fallback

## Post-Execution

Depois da ferramenta retornar:

1. **Output Validation**: Verifica schema, tipos, limites de tamanho
2. **Metrics Capture**: Latência, tokens, erros, segurança
3. **Comparison Mode**: Compara resultado vs baseline (opcional)
4. **Persistence**: Salva execução em AGENTS.md ou logs

## Métricas & SLA

Harness captura 5 métricas-chave de cada execução e define limites para degradação automática quando as métricas caem abaixo dos SLAs.

## Core Metrics

```yaml
retrieval_precision: >= 0.65 # Relevância da busca
tool_accuracy: >= 0.95 # Taxa de sucesso
security_events: 0 # Zero violações
latency_p95: < 2000ms # 95º percentil em ms
token_efficiency: >= 0.85 # Úteis / totais

# Exemplo de execução bem-sucedida
execution:
  tool_name: search_context
  latency_ms: 1240
  tokens_used: 2100
  tokens_useful: 1850
  precision: 0.72
  security_events: 0
  status: success
```

## Degradation Paths

Se métricas caem abaixo do SLA:

| Métrica                      | Ação                         |
| ---------------------------- | ---------------------------- |
| `retrieval_precision < 0.65` | Rerank com model mais pesado |
| `tool_accuracy < 0.95`       | Retry até 3x                 |
| `security_events > 0`        | Bloqueia execução + Alert    |
| `latency_p95 > 3000ms`       | Ativa compaction + timeout   |

## Comparação: Com vs Sem Harness

A diferença fundamental é que Harness adiciona validação, observabilidade e resiliência a cada chamada de tool. O comparativo abaixo mostra os impactos práticos.

## Sem Harness (MCP genérico)

```text
Agent → Tool → Output (confiar que é bom) → Response
```

- Sem validação pré-execução
- Sem captura de métricas
- Sem verificação de segurança inline
- Falhas silenciosas possíveis

## Com Harness

```text
Agent → Guardian → Preconditions → Tool (Wrapped) →
Output Validation → Metrics → Decision (use/retry/fail)
```

- Guardian blocklist enforcement
- Métricas por execução
- Retry automático em falhas transitórias
- Reranking se precision cai
- Circuit breaker em cascata

## Validação & Debug

Para validar que mudanças de performance foram positivas, Harness oferece um modo de comparação que testa antes/depois automaticamente.

## Mode de Comparação (--compare)

Use comparison mode para validar mudanças de performance após alterar reranker, embeddings ou índice:

## Caso 1: Testar novo reranker

```bash
vectora execute search_context \
  --query "Como validar tokens JWT em middleware?" \
  --compare baseline \
  --reranker voyage-rerank-2.5 # Novo reranker vs anterior
```

Output detalhado:

```yaml
execution_id: "harness_20260419_abc123"
tool: search_context
query: "Como validar tokens JWT em middleware?"

baseline: # Versão anterior (voyage-rerank-2.4 ou BM25)
  precision: 0.68
  latency_ms: 1520
  chunks_returned: 8
  top_chunk: { file: "src/auth/jwt.ts", relevance: 0.64 }
  top_chunk_2: { file: "src/utils/crypto.ts", relevance: 0.52 } # Ruído
  token_efficiency: 0.71

current: # Nova config (voyage-rerank-2.5)
  precision: 0.87
  latency_ms: 1240
  chunks_returned: 8
  top_chunk: { file: "src/auth/guards.ts", relevance: 0.92 }
  top_chunk_2: { file: "src/auth/jwt.ts", relevance: 0.84 } # Relevante
  token_efficiency: 0.89

delta:
  precision: +0.19 (28% improvement)
  latency: -280ms (faster)
  token_efficiency: +0.18
  verdict: "APPROVE - Reranker upgrade recommended"
```

## Caso 2: Validar reindex após schema change

```bash
# Reindexar com novo schema
vectora index --namespace "meu-projeto" --force

# Comparar contra versão anterior (backup automático)
vectora execute search_context \
  --query "handlers de autenticação" \
  --compare backup-20260418 # Compara vs índice anterior
```

## Caso 3: Monitorar degradação de performance

```bash
# Runbook: detectar problemas antes do SLA cair
vectora execute search_context \
  --query "rate limiting" \
  --compare last-1h \
  --fail-if-precision-drops 0.10 # Falha se cair >10%
```

Se `precision < 0.55` (abaixo do SLA 0.65):

```yaml
status: FAILED
reason: "precision degradation detected"
action: "Ativando recompression + rerank pesado"
fallback: true
```

## Logs de Validação

Ativa logging estruturado:

```yaml
# .env
VECTORA_HARNESS_DEBUG=true
VECTORA_LOG_LEVEL=debug
VECTORA_LOG_FORMAT=json
```

Logs incluem:

- Pre-execution: Guardian checks, preconditions
- Execution: Timeouts, retries, chunks
- Post-execution: Validation, metrics, decisions

## Configuração

```yaml
context_engine:
  harness:
    enabled: true
    pre_execution:
      validate_guardian: true
      validate_preconditions: true
      rate_limit_per_minute: 60
    execution:
      timeout_ms: 30000
      retry_attempts: 3
      circuit_breaker_threshold: 5
    post_execution:
      validate_output: true
      capture_metrics: true
      comparison_mode: false # true para --compare
    thresholds:
      min_retrieval_precision: 0.65
      min_tool_accuracy: 0.95
      max_security_events: 0
      max_latency_p95_ms: 3000

    # Fallbacks automáticos
    degradation:
      rerank_on_low_precision: true
      retry_on_timeout: true
      circuit_break_on_failures: true
```

---

> **Próximo**: [Namespaces](./namespaces.md)

---

## External Linking

| Concept               | Resource                             | Link                                                                                   |
| --------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**               | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Voyage Embeddings** | Voyage Embeddings Documentation      | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)         |
| **Voyage Reranker**   | Voyage Reranker API                  | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)             |
| **JWT**               | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
