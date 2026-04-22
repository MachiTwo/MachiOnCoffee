---
title: Gemini CLI
slug: gemini-cli
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - cli
  - concepts
  - config
  - gemini
  - integration
  - mcp
  - protocol
  - system
  - troubleshooting
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

Integre Vectora com a **Google Gemini CLI** para usar Vectora dentro de workflows do Gemini.

## Setup Rápido

## 1. Instale Gemini CLI

```bash
npm install -g @google/generative-ai-cli
```

## 2. Configure Vectora como MCP Server

No seu `.gemini/config.json`:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_NAMESPACE": "seu-projeto"
      }
    }
  }
}
```

## 3. Use em Prompts do Gemini

```bash
gemini chat --system "Você tem acesso a Vectora para buscar código"
```

## Casos de Uso

| Caso              | Descrição                                       |
| ----------------- | ----------------------------------------------- |
| **Code Search**   | Buscar arquivos relevantes via Gemini + Vectora |
| **Documentation** | Gerar docs a partir do código indexado          |
| **Analysis**      | Analisar padrões em codebase                    |

## Troubleshooting

**Gemini não vê Vectora?**

1. Verifique se `vectora mcp --stdio` roda localmente
2. Verifique permissões em `.gemini/config.json`
3. Reinicie o Gemini CLI

---

> Dúvidas? [GitHub Discussions](https://github.com/Kaffyn/Vectora/discussions)

## External Linking

| Concept        | Resource                             | Link                                                                                   |
| -------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **Gemini API** | Google AI Studio Documentation       | [ai.google.dev/docs](https://ai.google.dev/docs)                                       |
| **MCP**        | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
