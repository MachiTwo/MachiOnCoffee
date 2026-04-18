---
title: "Sub-Agents vs MCP: Ferramentas passivas vs Governança ativa"
date: 2026-04-17T21:15:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["mcp", "acp", "infra", "vectora"]
---

Você já ouviu falar do **Model Context Protocol (MCP)**? É um padrão aberto que permite que IAs (como o Claude) usem
ferramentas externas. Mas ser "apenas uma ferramenta MCP" não é o suficiente para o Vectora.

## O Que São Ferramentas MCP?

Imagine que o MCP é um canivete suíço. Cada ferramenta (como `read_file` ou `google_search`) é uma lâmina. O Agente
principal (Claude) abre a lâmina que ele acha que precisa e a usa.

O problema? O Agente principal não é um especialista na sua infraestrutura. Ele pode tentar ler um arquivo gigante e
travar o contexto, ou ignorar uma regra de segurança importante.

## A Diferença do Sub-Agent (Vectora)

O [Vectora](/04/17/vectora/) não é apenas o canivete; ele é um **Sub-Agent Especialista**. Quando o Claude o chama, ele
não está apenas pedindo um arquivo, ele está delegando uma missão de contexto.

| Recurso        | MCP Tool Comum                 | Vectora Sub-Agent                  |
| :------------- | :----------------------------- | :--------------------------------- |
| **Segurança**  | Depende do prompt (frágil)     | **Guardian** Hard-coded (lei)      |
| **Embeddings** | Geralmente não possui          | Pipeline nativo integrado          |
| **Validação**  | Nenhuma                        | **Harness** (Métricas de precisão) |
| **Namespaces** | Acesso direto ao disco         | Isolamento via RBAC                |
| **Decisão**    | O Agente principal decide tudo | O **Context Engine** filtra antes  |

## Protocolos: MCP e ACP

O Vectora fala as duas línguas:

- **MCP**: Para se conectar a qualquer agente Tier 1 moderno (Claude Code, Gemini CLI, etc.).
- **ACP (Agent Client Protocol)**: Um protocolo próprio de ultra-baixa latência para integração profunda com a sua IDE
  (VS Code, Cursor).

## Conclusão

Ferramentas passivas dão **funções**. O Sub-Agent Vectora dá **governança**. Ele garante que o seu Agente principal
receba o melhor contexto possível, da forma mais segura e barata, sem que você precise configurar cada detalhe.

---

_Este é um post de apoio ao projeto [Vectora](/04/17/vectora/)._
