---
title: MCP Reference
slug: mcp
date: "2026-04-19T10:25:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - byok
  - concepts
  - errors
  - mcp
  - protocol
  - reference
  - tools
  - vectora
  - yaml
---

{{< lang-toggle >}}

Referência técnica completa da implementação MCP de Vectora: tools, autenticação, transporte, tratamento de erros e exemplos.

## Server Info

```json
{
  "name": "vectora",
  "version": "0.8.0",
  "protocolVersion": "2024-11-05",
  "capabilities": {
    "tools": {
      "listChanged": true
    }
  }
}
```

## Tools Disponíveis

Vectora oferece **12 tools** via MCP para busca, análise, indexação e monitoramento de código.

**Para referência completa de todas as tools com parâmetros e exemplos:**
→ [MCP Tools Reference](./mcp-tools.md)

## Autenticação

O Vectora suporta múltiplos métodos de autenticação para garantir que as ferramentas MCP sejam acessadas apenas por clientes autorizados.

## Método 1: Bearer Token (Recomendado)

```bash
Authorization: Bearer sk-proj-vectora-abc123...
```

Token gerado via:

```bash
vectora auth token create --name "Claude Code"
```

Token expira em 30 dias (configurável).

## Método 2: API Key

```bash
X-API-Key: sk-...
```

Menos recomendado (não expira automaticamente).

## Método 3: BYOK (Bring Your Own Key)

Para planos Free:

```bash
Authorization: Bearer {GEMINI_API_KEY}
```

Vectora não armazena, apenas forwarda.

## Transport

A comunicação entre o cliente MCP e o servidor Vectora pode ocorrer localmente via canais de entrada/saída padrão ou remotamente através de endpoints HTTP seguros.

## STDIO (Padrão para IDE)

```bash
# Em .claude/claude_desktop_config.json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_TOKEN": "sk-proj-..."
      }
    }
  }
}
```

Ideal para: Claude Code, Cursor, Zed (local, <10ms latência)

## HTTP (Para Remote)

```bash
POST https://api.vectora.app/mcp
Authorization: Bearer sk-proj-...

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_context",
    "arguments": {"query": "..."}
  }
}
```

Ideal para: Servidores remotos, CI/CD

## Error Handling

Erros retornam no padrão JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "error_code": "INVALID_QUERY",
      "detail": "Query deve ter 3-10000 chars"
    }
  }
}
```

## Códigos de Erro MCP

| Código | Significado      | HTTP |
| ------ | ---------------- | ---- |
| -32700 | Parse error      | 400  |
| -32600 | Invalid request  | 400  |
| -32602 | Invalid params   | 400  |
| -32601 | Method not found | 404  |
| -32603 | Internal error   | 500  |

Vectora retorna também `error_code` customizado (ex: `NAMESPACE_NOT_FOUND`).

## Streaming (Respostas Grandes)

Para queries que retornam muitos chunks:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Chunk 1...",
        "partial": true
      },
      {
        "type": "text",
        "text": "Chunk 2...",
        "partial": true
      },
      {
        "type": "text",
        "text": "Chunk 3...",
        "partial": false
      }
    ]
  }
}
```

Suporta streaming progressivo até 30s timeout.

## Caching

MCP suporta caching automático via `cache_control`:

```json
{
  "type": "text",
  "text": "resultado",
  "cache_control": { "type": "ephemeral" } // TTL 5min
}
```

Economiza latência em queries repetidas.

## Capabilities

```yaml
tools:
  listChanged: true # Avisar quando tools mudam
  implementation: 12 # Número de tools

logging:
  enabled: true # Log de todas calls
  level: info # info, debug, warn

performance:
  latency_p95: 250ms # 95th percentile
  timeout: 30000ms # 30s máximo
```

## Exemplo Completo: Fluxo MCP

```bash
# 1. IDE inicia Vectora MCP
vectora mcp --stdio

# 2. IDE envia initialize
> {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"claude-code"}}}

# 3. Vectora responde
< {"jsonrpc":"2.0","id":1,"result":{"serverInfo":{"name":"vectora"}}}

# 4. IDE lista tools
> {"jsonrpc":"2.0","id":2,"method":"tools/list"}

# 5. Vectora retorna
< {"jsonrpc":"2.0","id":2,"result":{"tools":[...]}}

# 6. IDE chama tool
> {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_context","arguments":{"query":"Como validar JWT?"}}}

# 7. Vectora retorna resultado
< {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Encontrei 5 chunks..."}]}}
```

## Debug

Habilitar logs detalhados:

```bash
VECTORA_DEBUG=true VECTORA_LOG_LEVEL=debug vectora mcp --stdio 2> ~/.vectora/mcp-debug.log
```

Logs mostram todos os messages JSON trocados.

---

> Especificação completa: [Model Context Protocol Spec](https://modelcontextprotocol.io)

## External Linking

| Concept              | Resource                                       | Link                                                                                   |
| -------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| **MCP**              | Model Context Protocol Specification           | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**       | Go SDK for MCP (mark3labs)                     | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude** | Claude Documentation                           | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **JWT**              | RFC 7519: JSON Web Token Standard              | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |
| **JSON-RPC**         | JSON-RPC 2.0 Specification                     | [www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)                 |
| **GitHub Actions**   | Automate your workflow from idea to production | [docs.github.com/en/actions](https://docs.github.com/en/actions)                       |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
