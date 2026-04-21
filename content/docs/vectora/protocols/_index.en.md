---
title: Protocols
slug: protocols
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - protocols
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

Vectora implements two communication protocols: MCP (Model Context Protocol) for integration with IDEs, and ACP (Agent Communication Protocol) for communication between sub-agents.

## Supported Protocols

| Protocol | Use Case                            | Status | Docs              |
| -------- | ----------------------------------- | ------ | ----------------- |
| **MCP**  | Connection with Claude Code, Cursor | Stable | [→ MCP](./mcp.md) |
| **ACP**  | Communication between sub-agents    | Beta   | [→ ACP](./acp.md) |

## MCP (Model Context Protocol)

**The standard protocol for modern IDEs.**

MCP is an open protocol developed by Anthropic that allows LLMs to call tools on a computer in a structured way. Vectora offers 12 tools via MCP.

**Advantages:**

- Native in Claude Code and Cursor (zero extra config)
- Dynamic tool discovery
- Schema validation (ZOD)
- Automatic result caching
- Latency <10ms (local IPC)

## ACP (Agent Communication Protocol)

**For communication between Vectora and custom agents.**

ACP allows multiple agents to work together, sharing context and state. Ideal for distributed architectures where Vectora is a sub-agent of a larger system.

**Status:** Beta - Available for early adopters

## Which Protocol to Use?

- **Using Claude Code / Cursor / Zed?** → **MCP**
- **Integrating with custom agent in Python/Node/Go?** → **MCP** or REST API (beta)
- **Agent-to-agent communication?** → **ACP** (beta)

See [MCP](./mcp.md) for full implementation details.

---

> Next: [MCP Specification](./mcp.md)
