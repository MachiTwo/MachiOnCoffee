---
title: "Sub-Agents vs MCP: Passive tools vs Active governance"
slug: sub-agents
date: "2026-04-18T22:30:00-03:00"
draft: false
categories:
  - Deep Dive
tags:
  - active
  - agents
  - ai
  - architecture
  - concepts
  - context-engine
  - embeddings
  - gemini
  - governance
  - guardian
  - harness-runtime
  - integration
  - mcp
  - mcp-protocol
  - passive
  - protocol
  - rag
  - rbac
  - security
  - sub-agents
  - tools
  - vector-search
  - vectora
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}
Have you heard of the **Model Context Protocol (MCP)**? It's an open standard that allows AIs (like Claude) to use
external tools. But being "just an MCP tool" is not enough for Vectora.

## What are MCP Tools?

Imagine MCP is a Swiss Army knife. Each tool (like `read_file` or `google_search`) is a blade. The primary Agent
(Claude) opens the blade it thinks it needs and uses it.

The problem? The primary Agent is not an expert in your infrastructure. It might try to read a giant file and crash the
context, or ignore an important security rule.

## The Sub-Agent Difference (Vectora)

[Vectora](04/17/vectora/) is not just the knife; it is a **Specialist Sub-Agent**. When Claude calls it, it's not
just asking for a file, it's delegating a context mission.

| Feature        | Common MCP Tool                  | Vectora Sub-Agent                |
| :------------- | :------------------------------- | :------------------------------- |
| **Security**   | Prompt-dependent (fragile)       | Hard-coded **Guardian** (law)    |
| **Embeddings** | Usually none                     | Integrated native pipeline       |
| **Validation** | None                             | **Harness** (Precision metrics)  |
| **Namespaces** | Direct disk access               | Isolation via RBAC               |
| **Decision**   | Primary Agent decides everything | **Context Engine** filters first |

## Protocols: MCP and ACP

Vectora speaks both languages:

- **MCP**: To connect to any modern Tier 1 agent (Claude Code, Gemini CLI, etc.).
- **ACP (Agent Client Protocol)**: A proprietary ultra-low latency protocol for deep integration with your IDE (VS Code,
  Cursor).

## Conclusion

Passive tools give **functions**. The Vectora Sub-Agent gives **governance**. It ensures your primary Agent receives the
best possible context, in the safest and cheapest way, without you needing to configure every detail.

---

_This is a supporting post for the [Vectora](docs/vectora/) project._

## External Linking

| Concept              | Resource                                                   | Link                                                                                   |
| -------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **MCP**              | Model Context Protocol Specification                       | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**       | Go SDK for MCP (mark3labs)                                 | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude** | Claude Documentation                                       | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **RBAC**             | NIST Role-Based Access Control Standard                    | [csrc.nist.gov/projects/rbac](https://csrc.nist.gov/projects/rbac)                     |
| **Gemini API**       | Google AI Studio Documentation                             | [ai.google.dev/docs](https://ai.google.dev/docs)                                       |
| **RAG**              | Retrieval-Augmented Generation for Knowledge-Intensive NLP | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)                           |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
