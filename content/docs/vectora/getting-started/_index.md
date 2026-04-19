---
title: Getting Started
slug: getting-started
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - getting
  - mcp
  - setup
  - started
  - vectora
---

{{< lang-toggle >}}

Tudo que você precisa para começar com Vectora em 5 minutos: instalação, configuração de chaves, e primeira busca.

## Sequência Recomendada

| Passo | Descrição                               | Tempo       |
| ----- | --------------------------------------- | ----------- |
| 1⃣    | [Installation](./installation.md)       | 2 min       |
| 2⃣    | [Configuration](./configuration.md)     | 2 min       |
| 3⃣    | [Quickstart MCP](./quickstart-mcp.md)   | 3 min       |
| 4⃣    | [Troubleshooting](./troubleshooting.md) | Sob demanda |

## O Que Você Vai Fazer

### Passo 1: Instalar Vectora

```bash
npm install -g @vectora/cli
vectora --version
```

Pré-requisitos: Node.js 18+, npm ou yarn

### Passo 2: Configurar Chaves de API

Vectora usa BYOK (Bring Your Own Key). Você fornece:

- `GEMINI_API_KEY` de [Google AI Studio](https://aistudio.google.com)
- `VOYAGE_API_KEY` de [Voyage AI](https://www.voyageai.com)

```bash
vectora config set GEMINI_API_KEY "sua-chave-aqui"
vectora config set VOYAGE_API_KEY "sua-chave-aqui"
```

### Passo 3: Conectar ao IDE

- **Claude Code**: 1 linha no `claude_desktop_config.json`
- **Cursor**: 1 linha no `.cursor/settings.json`
- **Zed**: 1 linha no `.zed/settings.json`

Veja [Quickstart MCP](./quickstart-mcp.md) para copiar/colar.

### Passo 4: Fazer sua Primeira Busca

```bash
vectora search "Como authenticar usuários?"
```

Ou direto no IDE com autocomplete de MCP tools.

## Precisa de Ajuda?

- **Erro de instalação?** → [Troubleshooting](./troubleshooting.md)
- **MCP não conecta?** → [Quickstart MCP](./quickstart-mcp.md)
- **Config não funciona?** → [Configuration](./configuration.md)
- **Outra dúvida?** → [FAQ](../faq/)

## Próximas Leituras

Após configurar:

1. [Conceitos](../concepts/) — Entenda como funciona
2. [Integrações](../integrations/) — Configure seu IDE
3. [Segurança](../security/) — Proteja seus dados

---

> Tempo total: ~5-10 minutos. Vamos lá!
