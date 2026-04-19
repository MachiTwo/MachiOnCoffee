---
title: MCP Reference
slug: mcp
date: "2026-04-19T10:25:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - protocol
  - reference
  - vectora
---

{{< lang-toggle >}}

Complete technical reference for Vectora's MCP implementation: tools, authentication, transport, error handling, and examples.

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

## Available Tools

Vectora offers **12 tools** via MCP for search, analysis, indexing, and code monitoring.

**For complete reference of all tools with parameters and examples:**
→ [MCP Tools Reference](./mcp-tools.md)

## Authentication

### Method 1: Bearer Token (Recommended)

```bash
Authorization: Bearer sk-proj-vectora-abc123...
```

Generate token via:
```bash
vectora auth token create --name "Claude Code"
```

Token expires in 30 days (configurable).

### Method 2: API Key

```bash
X-API-Key: sk-...
```

Less recommended (doesn't auto-expire).

### Method 3: BYOK (Bring Your Own Key)

For Free plans:

```bash
Authorization: Bearer {GEMINI_API_KEY}
```

Vectora doesn't store, only forwards.

## Transport

### STDIO (Default for IDE)

```bash
# In .claude/claude_desktop_config.json
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

Ideal for: Claude Code, Cursor, Zed (local, <10ms latency)

### HTTP (For Remote)

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

Ideal for: Remote servers, CI/CD

## Error Handling

Errors return in JSON-RPC 2.0 format:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "error_code": "INVALID_QUERY",
      "detail": "Query must be 3-10000 chars"
    }
  }
}
```

### MCP Error Codes

| Code | Meaning | HTTP |
|------|---------|------|
| -32700 | Parse error | 400 |
| -32600 | Invalid request | 400 |
| -32602 | Invalid params | 400 |
| -32601 | Method not found | 404 |
| -32603 | Internal error | 500 |

Vectora also returns custom `error_code` (e.g., `NAMESPACE_NOT_FOUND`).

## Streaming (Large Responses)

For queries returning many chunks:

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

Supports progressive streaming up to 30s timeout.

## Caching

MCP supports automatic caching via `cache_control`:

```json
{
  "type": "text",
  "text": "result",
  "cache_control": {"type": "ephemeral"}  // TTL 5min
}
```

Saves latency on repeated queries.

## Capabilities

```yaml
tools:
  listChanged: true      # Notify when tools change
  implementation: 12     # Number of tools

logging:
  enabled: true          # Log all calls
  level: info            # info, debug, warn

performance:
  latency_p95: 250ms     # 95th percentile
  timeout: 30000ms       # 30s maximum
```

## Complete Example: MCP Flow

```bash
# 1. IDE starts Vectora MCP
vectora mcp --stdio

# 2. IDE sends initialize
> {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"claude-code"}}}

# 3. Vectora responds
< {"jsonrpc":"2.0","id":1,"result":{"serverInfo":{"name":"vectora"}}}

# 4. IDE lists tools
> {"jsonrpc":"2.0","id":2,"method":"tools/list"}

# 5. Vectora returns
< {"jsonrpc":"2.0","id":2,"result":{"tools":[...]}}

# 6. IDE calls tool
> {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_context","arguments":{"query":"How to validate JWT?"}}}

# 7. Vectora returns result
< {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Found 5 chunks..."}]}}
```

## Debug

Enable detailed logging:

```bash
VECTORA_DEBUG=true VECTORA_LOG_LEVEL=debug vectora mcp --stdio 2> ~/.vectora/mcp-debug.log
```

Logs show all JSON messages exchanged.

---

> 📖 Complete spec: [Model Context Protocol Spec](https://modelcontextprotocol.io)
