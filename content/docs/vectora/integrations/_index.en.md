---
title: Integrations
slug: integrations
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - integration
  - integrations
  - mcp
  - vectora
---

{{< lang-toggle >}}

Connect Vectora with your favorite tools and IDEs. Choose between generic integration (MCP Protocol) or proprietary apps with customized UX.

## Which Integration to Choose?

| IDE/App          | Recommendation      | Setup Time | Docs                                                          |
| ---------------- | ------------------- | ---------- | ------------------------------------------------------------- |
| **Claude Code**  | Native MCP          | 1 min      | [MCP Protocol](./mcp-protocol.md)                             |
| **Cursor**       | Native MCP          | 1 min      | [MCP Protocol](./mcp-protocol.md)                             |
| **Zed**          | Native MCP          | 2 min      | [MCP Protocol](./mcp-protocol.md)                             |
| **VS Code**      | Extension Native UI | 2 min      | [VS Code Extension](./vscode-extension.md)                    |
| **ChatGPT**      | Custom GPT Plugin   | 5 min      | [ChatGPT Plugin](./chatgpt-plugin.md)                         |
| **Gemini**       | REST API or CLI     | 3 min      | [Gemini API](./gemini-api.md) / [Gemini CLI](./gemini-cli.md) |
| **Custom Agent** | REST API (beta)     | 5 min      | [Custom Agents](./custom-agents.md)                           |

## Generic Integration

### MCP (Model Context Protocol)

**Best for**: Modern IDEs (Claude Code, Cursor, Zed)

Open standard protocol that allows IDEs to call tools on your computer. Vectora offers 12 tools via MCP.

- **Setup**: 1-2 lines in your IDE config
- **Latency**: <10ms (local IPC)
- **Discovery**: Automatic tool discovery

[→ MCP Protocol](./mcp-protocol.md)

## Customized UI Integrations

### VS Code Extension

**Best for**: VS Code developers

Native UI with sidebar, integrated commands, and syntax highlighting for retrieved code.

[→ VS Code Extension](./vscode-extension.md)

### ChatGPT Plugin

**Best for**: Using Vectora inside ChatGPT

Custom GPT Plugin with analysis, documentation, and code review support via ChatGPT.

[→ ChatGPT Plugin](./chatgpt-plugin.md)

### Gemini API Integration

**Best for**: Workflows using Google Gemini

REST + CLI integration for code analysis, review, and generation with Vectora context.

[→ Gemini API](./gemini-api.md)

## Advanced Integrations

### Custom Agents & REST API

Build agents in Python, Node.js, Go, or any language. Call Vectora via REST API (beta).

[→ Custom Agents](./custom-agents.md)

## Quick Start by Use Case

**"I want to use it in Claude Code"**
→ [MCP Protocol Quickstart](../getting-started/quickstart-mcp.md)

**"I want to use it in VS Code"**
→ [VS Code Extension](./vscode-extension.md)

**"I want to integrate it into my app"**
→ [Custom Agents](./custom-agents.md)

**"I want to use it with ChatGPT"**
→ [ChatGPT Plugin](./chatgpt-plugin.md)

---

> Didn't find your IDE? [Open an Issue](https://github.com/Kaffyn/Vectora/issues)
