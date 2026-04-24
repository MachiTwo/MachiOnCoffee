---
title: MCP Server Test Suite
slug: mcp-server-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - testing
  - mcp
  - json-rpc
  - protocol
  - integration
---

{{< lang-toggle >}}

O servidor MCP deve ser robusto, rápido, confiável e 100% conforme à especificação JSON-RPC 2.0, suportando requisições concorrentes, grandes payloads e recuperação graceful de erros. Esta suite valida a implementação completa do protocolo MCP. Cobertura: **80+ testes** | **Prioridade**: ALTA

## Test Segments

---

## Segmentos de Testes

### 1. JSON-RPC 2.0 Compliance (20 testes)

#### Test: Valid Request Format

```text
Given: Request com formato correto:
  {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {...},
    "id": 1
  }
When: Enviado ao servidor
Then:
  - Parseado corretamente
  - Response com id correspondente
  - Sem erros de parsing
```

#### Test: Invalid Request Rejection

```text
Given: Request malformado:
  - Faltando "jsonrpc": "2.0"
  - ID inválido
  - Method não string
When: Enviado
Then:
  - Error response retornado
  - Code: -32600 (Invalid Request)
  - Mensagem clara
```

#### Test: Notification Handling

```text
Given: Notification (sem id):
  {
    "jsonrpc": "2.0",
    "method": "initialized",
    "params": {}
  }
When: Enviado
Then:
  - Processado
  - Sem response esperada
  - Operação completa
```

#### Test: Batch Requests

```text
Given: Multiple requests no mesmo payload:
  [req1, req2, req3]
When: Enviado
Then:
  - Todos processados
  - Array de responses
  - Ordem preservada (por id)
```

---

### 2. Tool Operations (25 testes)

#### Test: Tool Discovery

```text
Given: Server ativo
When: tools/list enviado
Then:
  - Lista de tools retornada
  - Schema para cada tool
  - Nomes, descrições
  - Parâmetros documentados
```

#### Test: Tool Invocation

```text
Given: Tool "search_context" disponível
When: tools/call executado com:
  {
    "name": "search_context",
    "arguments": {"query": "auth", "top_k": 5}
  }
Then:
  - Ferramenta invocada
  - Resultado retornado
  - Content no formato correto
```

#### Test: Parameter Validation

```text
Given: Tool espera top_k: integer
When: Enviado top_k: "string"
Then:
  - Error retornado
  - Code: -32602 (Invalid params)
  - Mensagem sobre tipo esperado
```

#### Test: Missing Required Parameters

```text
Given: Tool requer "query" obrigatório
When: Enviado sem "query"
Then:
  - Error de parâmetro obrigatório
  - Descrição clara
  - Sugestão de correção
```

---

### 3. Performance (15 testes)

#### Test: Low Latency Response

```text
Given: Simple request
When: Enviado
Then:
  - Response em < 100ms
  - Sem overhead desnecessário
  - Rápido parsing e serialização
```

#### Test: Concurrent Requests

```text
Given: 10 requests simultâneos
When: Todos enviados
Then:
  - Todos processados
  - Response para cada um
  - Latência p95 < 200ms
```

#### Test: Large Payload Handling

```text
Given: Request com payload de 10MB
When: Enviado
Then:
  - Aceito (se sob limite)
  - Processado corretamente
  - Sem memory leak
```

---

### 4. Reliability (20 testes)

#### Test: Connection Resilience

```text
Given: Connection ativa
When: Network intermittent
Then:
  - Detecta desconexão
  - Reconnect automático
  - Estado preservado (se possível)
```

#### Test: Error Recovery

```text
Given: Tool falha durante execução
When: Exception lançada
Then:
  - Error response gerado
  - Cliente avisado
  - Server continua operacional
```

#### Test: Graceful Degradation

```text
Given: Tool indisponível
When: Chamado
Then:
  - Error específico retornado
  - Server não crashes
  - Outras tools funcionam
```

---

## Performance SLAs

| Métrica             | Alvo    |
| ------------------- | ------- |
| Latência p50        | < 50ms  |
| Latência p95        | < 200ms |
| Latência p99        | < 500ms |
| Concurrent requests | 100+    |
| Success rate        | 99.9%   |

---

## Como Executar

```bash
# Testes MCP
go test -v ./tests/mcp-server/...

# Com JSON-RPC conformance
go test -v -run JSONRPCCompliance ./tests/mcp-server/...

# Load test
go test -v -bench=. ./tests/mcp-server/bench_test.go

# Com race detection
go test -v -race ./tests/mcp-server/...
```

---

## External Linking

| Conceito                  | Recurso        | Link                                                                                                                                                                         |
| ------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MCP Specification**     | Official Spec  | [modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)                                                                 |
| **JSON-RPC 2.0**          | Spec Document  | [www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)                                                                                                       |
| **MCP Development Guide** | Server Dev     | [github.com/cyanheads/model-context-protocol-resources](https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-server-development-guide.md)      |
| **MCP Message Types**     | Deep Dive      | [portkey.ai/blog/mcp-message-types](https://portkey.ai/blog/mcp-message-types-complete-json-rpc-reference-guide)                                                             |
| **MCP Implementation**    | Hands-on Guide | [abvijaykumar.medium.com/model-context-protocol-deep-dive](https://abvijaykumar.medium.com/model-context-protocol-deep-dive-part-3-1-3-hands-on-implementation-522ecd702b0d) |
| **MCP Transports**        | Reference      | [modelcontextprotocol.info/docs/concepts/transports](https://modelcontextprotocol.info/docs/concepts/transports/)                                                            |
| **MCP Introduction**      | Overview       | [stytch.com/blog/model-context-protocol-introduction](https://stytch.com/blog/model-context-protocol-introduction/)                                                          |
| **Why MCP Uses JSON-RPC** | Article        | [medium.com/@dan.avila7/why-model-context-protocol-uses-json-rpc](https://medium.com/@dan.avila7/why-model-context-protocol-uses-json-rpc-64d466112338)                      |
