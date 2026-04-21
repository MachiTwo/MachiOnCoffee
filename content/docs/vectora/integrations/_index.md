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
{{< section-toggle >}}

Conecte Vectora com suas ferramentas e IDEs preferidas. Escolha entre integração genérica (MCP Protocol) ou apps proprietários com UX customizada.

## Qual Integração Escolher?

| IDE/App          | Recomendação        | Tempo Setup | Docs                                                          |
| ---------------- | ------------------- | ----------- | ------------------------------------------------------------- |
| **Claude Code**  | MCP Nativo          | 1 min       | [MCP Protocol](./mcp-protocol.md)                             |
| **Cursor**       | MCP Nativo          | 1 min       | [MCP Protocol](./mcp-protocol.md)                             |
| **Zed**          | MCP Nativo          | 2 min       | [MCP Protocol](./mcp-protocol.md)                             |
| **VS Code**      | Extension Native UI | 2 min       | [VS Code Extension](./vscode-extension.md)                    |
| **ChatGPT**      | Plugin Custom GPT   | 5 min       | [ChatGPT Plugin](./chatgpt-plugin.md)                         |
| **Gemini**       | API REST ou CLI     | 3 min       | [Gemini API](./gemini-api.md) / [Gemini CLI](./gemini-cli.md) |
| **Agent Custom** | REST API (beta)     | 5 min       | [Custom Agents](./custom-agents.md)                           |

## Integração Genérica

## MCP (Model Context Protocol)

**Melhor para**: IDEs modernas (Claude Code, Cursor, Zed)

Protocolo padrão aberto que permite que IDEs chamem tools do computador. Vectora oferece 12 tools via MCP.

- Setup: 1-2 linhas no config da IDE
- Latência: <10ms (IPC local)
- Descoberta: Automática de tools

[→ MCP Protocol](./mcp-protocol.md)

## Integrações com UI Customizada

## VS Code Extension

**Melhor para**: Desenvolvedores VS Code

UI nativa com sidebar, comandos integrados, syntax highlighting de código encontrado.

[→ VS Code Extension](./vscode-extension.md)

## ChatGPT Plugin

**Melhor para**: Usar Vectora dentro do ChatGPT

Custom GPT Plugin com suporte a análise, documentação, code review via ChatGPT.

[→ ChatGPT Plugin](./chatgpt-plugin.md)

## Gemini API Integration

**Melhor para**: Workflows com Google Gemini

Integração REST + CLI para análise de código, revisão, geração com contexto Vectora.

[→ Gemini API](./gemini-api.md)

## Integrações Avançadas

## Custom Agents & REST API

Construa agents em Python, Node.js, Go ou qualquer linguagem. Chame Vectora via REST API (beta).

[→ Custom Agents](./custom-agents.md)

## Quick Start por Caso de Uso

**"Quero usar em Claude Code"**
→ [MCP Protocol Quickstart](../getting-started/quickstart-mcp.md)

**"Quero usar em VS Code"**
→ [VS Code Extension](./vscode-extension.md)

**"Quero integrar em meu app"**
→ [Custom Agents](./custom-agents.md)

**"Quero usar com ChatGPT"**
→ [ChatGPT Plugin](./chatgpt-plugin.md)

---

> Não achou sua IDE? [Abra uma Issue](https://github.com/Kaffyn/Vectora/issues)
