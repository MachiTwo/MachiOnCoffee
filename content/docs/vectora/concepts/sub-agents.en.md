---
title: "Sub-Agents vs MCP: Passive tools vs Active governance"
date: 2026-04-17T21:15:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["mcp", "acp", "infra", "vectora"]
---

Have you heard of the **Model Context Protocol (MCP)**? It's an open standard that allows AIs (like Claude) to use
external tools. But being "just an MCP tool" is not enough for Vectora.

## What are MCP Tools?

Imagine MCP is a Swiss Army knife. Each tool (like `read_file` or `google_search`) is a blade. The primary Agent
(Claude) opens the blade it thinks it needs and uses it.

The problem? The primary Agent is not an expert in your infrastructure. It might try to read a giant file and crash the
context, or ignore an important security rule.

## The Sub-Agent Difference (Vectora)

[Vectora](/en/04/17/vectora/) is not just the knife; it is a **Specialist Sub-Agent**. When Claude calls it, it's not
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

_This is a supporting post for the [Vectora](/en/docs/vectora/) project._
