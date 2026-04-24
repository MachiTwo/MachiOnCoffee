---
title: Protocols
slug: protocols
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - concepts
  - config
  - mcp
  - protocol
  - protocols
  - state
  - sub-agents
  - system
  - tools
  - vectora
---

{{< lang-toggle >}}

Vectora implementa dois protocolos de comunicação: MCP (Model Context Protocol) para integração com IDEs, e ACP (Agent Communication Protocol) para comunicação entre sub-agents.

## Protocolos Suportados

| Protocolo | Caso de Uso                          | Status | Docs              |
| --------- | ------------------------------------ | ------ | ----------------- |
| **MCP**   | Conexão com Claude Code, Cursor, Zed | Stable | [→ MCP](./mcp.md) |
| **ACP**   | Comunicação entre Vectora e agents   | Beta   | [→ ACP](./acp.md) |

## MCP (Model Context Protocol)

**O protocolo padrão para IDEs modernas.**

O MCP é um protocolo aberto desenvolvido pela Anthropic que permite que LLMs chamem ferramentas de um computador de forma estruturada. Vectora oferece 12 tools via MCP.

**Vantagens:**

- Nativo em Claude Code e Cursor (zero config a mais)
- Descoberta dinâmica de tools
- Schema validation (ZOD)
- Caching automático de resultados
- Latência <10ms (IPC local)

## ACP (Agent Communication Protocol)

**Para comunicação entre Vectora e agents customizados.**

ACP permite que múltiplos agents trabalhem juntos, compartilhando contexto e estado. Ideal para arquiteturas distribuídas onde Vectora é sub-agent de um sistema maior.

**Status:** Beta - Disponível para early adopters

## Qual Protocolo Usar?

- **Usando Claude Code / Cursor / Zed?** → **MCP**
- **Integrando com agent custom em Python/Node/Go?** → **MCP** ou REST API (beta)
- **Agent-to-agent communication?** → **ACP** (beta)

Veja [MCP](./mcp.md) para detalhes completos de implementação.

---

> Próximo: [MCP Specification](./mcp.md)

## External Linking

| Concept              | Resource                             | Link                                                                                   |
| -------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**              | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**       | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude** | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **Zod**              | TypeScript-first schema validation   | [zod.dev/](https://zod.dev/)                                                           |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
