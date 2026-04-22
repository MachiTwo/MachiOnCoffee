---
title: ACP
slug: acp
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - acp
  - ai
  - auth
  - concepts
  - mcp
  - protocol
  - state
  - sub-agents
  - system
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

**ACP** (Agent Communication Protocol) is a communication protocol between Vectora and custom agents or other systems. It is currently in **Beta** for early adopters.

## What is ACP?

ACP allows:

- **Vectora to be a sub-agent** of a larger system (e.g., a multi-agent orchestrator AI)
- **Multiple agents to work together** sharing context
- **Distributed architectures** with Vectora in multiple instances

Unlike MCP (IDE ↔ Vectora), ACP is for **agent ↔ agent** communication.

## Use Cases

| Case                   | Description                                         |
| ---------------------- | --------------------------------------------------- |
| **Multi-agent system** | Vectora + Code Agent + Test Agent coordinated       |
| **Distributed search** | Vectora across multiple namespaces/datacenters      |
| **Custom workflows**   | Orchestrator agent calls Vectora dynamically        |
| **Hybrid systems**     | Vectora + GenAI + Traditional APIs working together |

## Status

**Beta** - Specification in evolution. Accepting early adopters and feedback.

- Protocol: JSON-based RPC (similar to MCP)
- Auth: JWT with refresh tokens
- Transport: HTTP/2 or WebSocket for streaming

## Get Started

ACP does not yet have full public documentation. For early access:

1. Open a [GitHub Discussion](https://github.com/Kaffyn/Vectora/discussions)
2. Mention "ACP interest"
3. Describe your use case
4. You will receive access to the beta spec + support

## Comparison: MCP vs ACP

| Aspect        | MCP                  | ACP                     |
| ------------- | -------------------- | ----------------------- |
| **Use Case**  | Local IDE            | Inter-agent distributed |
| **Transport** | STDIO (IPC)          | HTTP/2 or WebSocket     |
| **Latency**   | <10ms                | 50-100ms                |
| **State**     | Persistent (session) | Shared between agents   |
| **Status**    | Stable               | Beta                    |

---

> Interested in ACP? [Open a Discussion](https://github.com/Kaffyn/Vectora/discussions)

## External Linking

| Concept        | Resource                             | Link                                                                                   |
| -------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **JWT**        | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
