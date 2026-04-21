---
title: MCP
slug: mcp
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - mcp-protocol
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

**Vectora works exclusively via MCP (Model Context Protocol).** This document describes how Vectora implements MCP, its architecture, and how IDEs (Claude Code, Cursor, Zed) integrate.

## What is MCP?

**MCP** is an open protocol that allows LLMs (Large Language Models) to call "tools" on a computer. Unlike generic REST APIs, MCP is optimized for:

- **Tool Discovery**: The IDE discovers which tools are available.
- **Structured I/O**: JSON schemas to ensure validation.
- **Error Handling**: Structured responses with automatic retry.
- **Capability Negotiation**: Client and server agree on features.

```text
┌─────────────┐
│     IDE     │ (Claude Code, Cursor, etc)
│ (MCP Client)│
└──────┬──────┘
       │ {"jsonrpc": "2.0", "method": "resources/list"}
       ▼
┌──────────────────────────┐
│   Vectora MCP Server     │
│ (mcp service running)    │
│                          │
│ • Tool: search_context   │
│ • Tool: analyze_file     │
│ • Tool: find_references  │
└──────────────────────────┘
       ▲
       │ {"result": [...], "tools": [...]}
       │
```

## Why Does Vectora Use MCP?

| Alternative               | Problem                                | How MCP Resolves                    |
| ------------------------- | -------------------------------------- | ----------------------------------- |
| **REST API**              | SDK in each IDE, complex configuration | MCP is native in Claude Code/Cursor |
| **CLI Tool**              | No shared context between IDE and tool | MCP maintains state between calls   |
| **Subprocess**            | Slow, no structured output             | MCP is efficient + native JSON      |
| **LSP (Language Server)** | Designed for autocomplete, not AI      | MCP is generic for any tool         |

**Result**: One IDE (Claude Code) ↔ Multiple MCPs (Vectora, pytest, git, file-system).

## Vectora MCP Architecture

Vectora implements MCP with a clear stack: the MCP client in the IDE connects to the Vectora server via STDIO, which orchestrates the Harness Runtime, Context Engine, and Tool Executor.

## Components

```text
IDE (Claude Code)
    │
    └─→ MCP Client (built-in)
         │
         ├─→ STDIO Transport (pipe)
         │
         └─→ Vectora MCP Server
              │
              ├─→ Harness Runtime (validation)
              │    ├─→ Guardian (security)
              │    └─→ Preconditions (verification)
              │
              ├─→ Context Engine (search)
              │    ├─→ Embeddings (Voyage 4)
              │    ├─→ Search (HNSW + Qdrant)
              │    └─→ Reranking (Voyage 2.5)
              │
              └─→ Tool Executor
                   ├─→ search_context
                   ├─→ analyze_file
                   ├─→ find_references
                   └─→ ... (12 tools total)
```

## Transport

Vectora MCP uses **STDIO** (stdin/stdout pipes):

```bash
# In Claude Code's settings.json
"mcp": {
  "vectora": {
    "command": "vectora",
    "args": ["mcp", "--stdio"]
  }
}

# Vectora starts with:
# STDIN ← JSON messages from the IDE
# STDOUT → JSON responses from Vectora
```

## Protocol Flow

The MCP flow in Vectora goes through three phases: initialization where the IDE and server negotiate capabilities, discovery of available tools, and tool execution with error handling.

## 1. Initialization

```json
// IDE sends
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "claude-code",
      "version": "1.0.0"
    }
  }
}

// Vectora responds
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {} // Available tools
    },
    "serverInfo": {
      "name": "vectora",
      "version": "0.8.0"
    }
  }
}
```

## 2. Tool Discovery

```json
// IDE requests tools list
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}

// Vectora lists (simplified example)
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "search_context",
        "description": "Semantic search across codebase",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {"type": "string"},
            "top_k": {"type": "integer", "default": 10}
          }
        }
      }
    ]
  }
}
```

## 3. Tool Execution

```json
// IDE calls tool
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_context",
    "arguments": {
      "query": "How to validate JWT tokens?",
      "top_k": 5
    }
  }
}

// Vectora executes (passes through Harness + Guardian)
// Returns result
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 5 relevant chunks..."
      },
      {
        "type": "text",
        "text": "[JSON with chunks, metadata, precision]"
      }
    ]
  }
}
```

## Vectora MCP Tools (12 Total)

| Tool               | Input              | Output                      | Latency SLA |
| ------------------ | ------------------ | --------------------------- | ----------- |
| `search_context`   | query, top_k       | chunks, precision           | <300ms      |
| `analyze_file`     | file_path          | structure, imports, exports | <200ms      |
| `find_references`  | symbol_name        | call sites, types           | <250ms      |
| `file_summary`     | file_path          | summary, key functions      | <150ms      |
| `list_workspace`   | filter (opt)       | files, structure            | <100ms      |
| `get_dependencies` | file_path          | direct, indirect deps       | <200ms      |
| `analyze_changes`  | file_paths[]       | impact analysis             | <400ms      |
| `validate_imports` | file_paths[]       | validation results          | <300ms      |
| `search_by_type`   | type_name          | usages of type              | <250ms      |
| `get_config`       | key (opt)          | config value                | <50ms       |
| `index_status`     | none               | status, size, chunks        | <100ms      |
| `execute_query`    | query_type, params | generic query               | <500ms      |

See [MCP Tools Reference](../reference/mcp-tools.md) for full details.

## IDE Configuration

Each IDE has a different process for configuring MCP servers. Below are examples for the most used platforms.

## Claude Code (Recommended)

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"]
    }
  }
}
```

## Cursor

```json
// .cursor/settings.json
{
  "mcp": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_NAMESPACE": "my-project"
      }
    }
  }
}
```

## Zed

```json
// .zed/settings.json
{
  "language_servers": {
    "vectora": {
      "binary": {
        "path": "vectora"
      },
      "initialization_options": {
        "namespace": "my-project"
      }
    }
  }
}
```

## Error Handling

MCP defines structured errors:

```json
// Tool fails with error
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "error_code": "NAMESPACE_NOT_FOUND",
      "detail": "Namespace 'invalid' does not exist"
    }
  }
}
```

Vectora error codes:

- `NAMESPACE_NOT_FOUND` (404)
- `AUTHENTICATION_FAILED` (401)
- `RATE_LIMIT_EXCEEDED` (429)
- `INVALID_SCHEMA` (400)
- `TIMEOUT` (504)
- `INTERNAL_ERROR` (500)

## Performance & Optimizations

Vectora implements various techniques to maintain low latency and high scalability: streaming for large responses, caching frequent results, and batch processing.

## Streaming (For large responses)

MCP supports streaming of tool results:

```json
// Chunked response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      { "type": "text", "text": "Chunk 1...", "partial": true },
      { "type": "text", "text": "Chunk 2...", "partial": true },
      { "type": "text", "text": "Chunk 3...", "partial": false } // end
    ]
  }
}
```

## Caching

Vectora caches search results:

```text
Client: search_context("How to validate tokens?")
  ↓ (first time)
Server: Processes + Returns + **Caches with 5min TTL**
  ↓ (second time, same query within 5min)
Server: Returns from cache (0ms vs 230ms)
```

## Batch Calls

IDEs can make multiple parallel calls:

```json
[
  {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_context", "arguments": {...}}},
  {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "analyze_file", "arguments": {...}}},
  {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "find_references", "arguments": {...}}}
]
```

## Debug & Logging

To understand what is happening between the IDE and Vectora, use the MCP Inspector or activate structured logging. Both help diagnose integration issues.

## MCP Inspector

```bash
# View MCP messages in real-time
# (IDE + Vectora)
vectora mcp --debug

# Output:
# [MCP] Client → Server: {"jsonrpc": "2.0", "method": "initialize", ...}
# [MCP] Server → Client: {"jsonrpc": "2.0", "result": {...}, ...}
# [MCP] Tool call: search_context | Query: "..." | Time: 234ms
```

## Logging Structure

```yaml
# logs/mcp.log (JSON)
{
  "timestamp": "2026-04-19T10:30:45Z",
  "level": "INFO",
  "event": "tool_executed",
  "tool_name": "search_context",
  "tool_duration_ms": 234,
  "error_code": null,
  "precision": 0.87,
  "chunks_returned": 5,
}
```

## Comparison: MCP vs Alternatives

| Aspect          | MCP                      | REST API             | LSP           |
| --------------- | ------------------------ | -------------------- | ------------- |
| **Setup**       | Automatic in IDE         | Manual config        | Manual config |
| **Discovery**   | Dynamic (tools/list)     | Static documentation | Static        |
| **State**       | Persistent (session)     | Stateless            | Stateless     |
| **Latency**     | <10ms IPC                | >100ms network       | <50ms IPC     |
| **IDE Support** | Claude Code, Cursor, Zed | All                  | Some          |

**Conclusion**: MCP is ideal for tools that need persistent context + discovery.

## Full Specification

MCP is defined by Anthropic. See:

- [MCP Specification](https://modelcontextprotocol.io/docs)
- [GitHub: anthropics/mcp](https://github.com/anthropics/mcp)

Vectora follows specification v2024-11-05 (latest).
