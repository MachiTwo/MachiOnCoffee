---
title: Retenção de Dados
slug: retention
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - byok
  - concepts
  - embeddings
  - mcp
  - privacy
  - protocol
  - retention
  - security
  - vectora
---

{{< lang-toggle >}}

Esta página detalha as políticas de retenção de dados para diferentes planos e tipos de informação no Vectora.

## Políticas por Tipo de Dado

| Tipo de Dado           | Free               | Pro                      | Team                     |
| :--------------------- | :----------------- | :----------------------- | :----------------------- |
| **Embeddings**         | Vitalício (local)  | Enquanto ativo + 30 dias | Enquanto ativo + 90 dias |
| **Logs de Auditoria**  | 30 dias            | 90 dias                  | 7 anos (Compliance)      |
| **Sessões MCP**        | 24h de inatividade | 14 dias                  | Customizado              |
| **Arquivos de Backup** | Manual             | Automático (30 dias)     | Automático (Customizado) |

## Cancelamento e Expiração

Se você cancelar sua assinatura ou sua conta expirar:

1. **Conta Suspensa**: Você tem 5 dias para exportar seus dados.
2. **Purga Intermediária**: Logs e metadados de sessão são deletados após 15 dias.
3. **Purga Final**: Todos os embeddings e configurações são removidos permanentemente após 30 dias (Pro) ou 90 dias (Team).

---

> Para exercer seus direitos de privacidade, consulte nossa [Política de Privacidade](../security/byok-privacy.md).

## External Linking

| Concept        | Resource                             | Link                                                                                   |
| -------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
