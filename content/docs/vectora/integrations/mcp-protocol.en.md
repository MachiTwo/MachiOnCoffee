---
title: MCP Protocol Integration
slug: mcp-protocol
date: "2026-04-19T10:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - chatgpt
  - claude
  - concepts
  - config
  - cursor
  - embeddings
  - gemini
  - ide
  - integration
  - mcp
  - mcp-protocol
  - plugins
  - protocol
  - reranker
  - tools
  - troubleshooting
  - vectora
  - voyage
---

{{< lang-toggle >}}
{{< section-toggle >}}

Vectora implements **Model Context Protocol (MCP)**, a standardized protocol that allows any IDE with MCP support to connect and use Vectora as a context server. Works natively in Claude Code and Cursor.

## What is MCP?

**MCP** is a standardized protocol for connecting AI models to external tools. Vectora exposes its functions (search, analysis) as MCP tools that any compatible IDE can use.

```text
IDE (Claude Code / Cursor / other with MCP)
    ↓
  MCP Protocol (JSON-RPC)
    ↓
Vectora Server (localhost:9090 or remote)
    ↓
  12 Available Tools
```

## Quick Start

## Prerequisites

- Node.js 18+
- Vectora installed: `npm install -g @kaffyn/vectora`
- API keys (Gemini, Voyage)
- IDE with MCP support (Claude Code, Cursor, etc)

## Step 1: Initialize Project

```bash
cd ~/your-project
vectora init --name "Your Project"
```

## Step 2: Configure MCP in Your IDE

**Config file** (location varies by IDE):

- Claude Code: `~/.claude/claude_desktop_config.json`
- Cursor: `~/.cursor/cursor_config.json`
- Other IDEs: See MCP documentation

**Add Vectora:**

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "GEMINI_API_KEY": "your-value",
        "VOYAGE_API_KEY": "your-value",
        "VECTORA_NAMESPACE": "your-namespace"
      }
    }
  }
}
```

## Step 3: Test

1. Restart your IDE
2. Look for `search_context` tool in MCP menu
3. Test: `@vectora search_context "How to validate tokens?"`

## 12 Available Tools

| Tool                   | Function                   |
| ---------------------- | -------------------------- |
| `search_context`       | Semantic search for chunks |
| `search_tests`         | Find related tests         |
| `analyze_dependencies` | Find function callers      |
| `find_similar_code`    | Find similar code patterns |
| `get_file_structure`   | Summarize file structure   |
| `list_files`           | List indexed files         |
| `list_namespaces`      | List namespaces            |
| `get_namespace_stats`  | Namespace statistics       |
| `index_status`         | Index status               |
| `reindex`              | Force re-indexing          |
| `get_config`           | Get current config         |
| `get_metrics`          | Execution metrics          |

## Practical Workflows

## Workflow 1: Understand Feature

```text
You: "Explain how authentication works"
IDE: @vectora search_context "authentication"
Vectora: Returns relevant chunks
IDE: Shows chunks in context
```

## Workflow 2: Debugging

```text
You: "Why does this test fail?"
IDE: @vectora search_context "test X"
IDE: @vectora analyze_dependencies "tested function"
Vectora: Returns relevant context
```

## Workflow 3: Code Review

```text
You: "Review this function"
IDE: @vectora find_similar_code "your code"
Vectora: Finds similar patterns
IDE: Compares with existing code
```

## Advanced Configuration

## Custom Namespace

```json
{
  "mcpServers": {
    "vectora": {
      "env": {
        "VECTORA_NAMESPACE": "staging" // Use different namespace
      }
    }
  }
}
```

## Multiple Synchronized IDEs

If using multiple IDEs, both point to same config and namespace:

```json
// Claude Code
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "VECTORA_NAMESPACE": "your-namespace"
      }
    }
  }
}

// Cursor - same config
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "VECTORA_NAMESPACE": "your-namespace"
      }
    }
  }
}
```

Both see the same chunks, indices, namespaces.

## Troubleshooting

## "Vectora command not found"

```bash
# Check installation
npm list -g @kaffyn/vectora

# Reinstall if needed
npm install -g @kaffyn/vectora --force
```

## "Connection refused"

Vectora is not running as server:

```bash
# Start manually
vectora mcp

# Or via config with custom port
{
  "env": {
    "VECTORA_MCP_PORT": "9091"
  }
}
```

## "API key not found"

Check environment variables:

```bash
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# If empty, configure in .env or config JSON
```

## Performance

- **Expected latency**: ~300-500ms (network + APIs)
- **Local search**: ~100ms (no APIs)
- **Cache**: Results cached in `.vectora/`
- **Concurrent**: Supports multiple IDEs pointing to same server

## Compatible IDEs

| IDE             | Support        | Status            |
| --------------- | -------------- | ----------------- |
| **Claude Code** | Native MCP     | Tested            |
| **Cursor**      | Native MCP     | Tested            |
| **VS Code**     | No native MCP  | Use own extension |
| **Zed**         | MCP supported  | Not tested        |
| **Neovim**      | MCP via plugin | Not tested        |

For VS Code, use [VS Code Extension](./vscode-extension.md).

## Next Steps

- **VS Code?** → [VS Code Extension](./vscode-extension.md)
- **ChatGPT?** → [ChatGPT Plugin](./chatgpt-plugin.md)
- **Gemini?** → [Gemini API](./gemini-api.md)

---

## External Linking

| Concept               | Resource                             | Link                                                                                   |
| --------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**               | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude**  | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **Gemini API**        | Google AI Studio Documentation       | [ai.google.dev/docs](https://ai.google.dev/docs)                                       |
| **Voyage Embeddings** | Voyage Embeddings Documentation      | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)         |
| **Voyage Reranker**   | Voyage Reranker API                  | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)             |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
