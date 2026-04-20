---
title: Custom Agents
slug: custom-agents
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - agents
  - ai
  - custom
  - integration
  - mcp
  - vectora
---

{{< lang-toggle >}}

Integrar Vectora com agents customizados em Python, Node.js, Go ou qualquer linguagem que suporte HTTP.

## Opções de Integração

| Método         | Caso de Uso                           | Complexidade |
| -------------- | ------------------------------------- | ------------ |
| **MCP**        | Agent roda localmente em Go/Rust      |              |
| **REST API**   | Agent remoto em Python/Node/Go        |              |
| **ACP (Beta)** | Inter-agent communication distribuída |              |

## REST API (Recomendado para Começar)

Vectora expõe uma REST API (beta) que qualquer agent pode chamar:

```bash
curl -X POST https://vectora.app/api/search \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Como validar tokens JWT?",
    "namespace": "seu-projeto",
    "top_k": 5
  }'
```

## MCP para Agents Customizados

Se seu agent é escrito em Go/Rust, pode usar MCP diretamente:

```text
Seu Agent (Python/Node) ↔ MCP Client ↔ Vectora MCP Server
```

Veja [MCP Integration](./mcp-protocol.md) para detalhes.

## Começar

1. Obtenha um **token de API** em console.vectora.app
2. Configure seu agent para chamar `/api/search`
3. Teste localmente com `curl`
4. Integre em seu workflow

## Referência Completa

- REST API Reference (beta): `/api/docs`
- MCP Spec: [Model Context Protocol](https://modelcontextprotocol.io)
- ACP (Beta): [GitHub Discussions](https://github.com/Kaffyn/Vectora/discussions)

---

> Precisa de uma integração específica? [Abra uma Issue](https://github.com/Kaffyn/Vectora/issues)
