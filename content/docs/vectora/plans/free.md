---
title: Free
slug: free
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - free
  - mcp
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

O plano **Free** de Vectora é totalmente **open source e sem limite de tempo**. Use localmente, em qualquer codebase, sem pagar nada. Perfeito para:

- ‍ Desenvolvedores individuais
- Pequenos times (< 10 pessoas)
- Projetos educacionais
- Prototipagem e testes

---

## O Que Está Incluído

### Core Features

| Feature                     | Free |
| --------------------------- | ---- |
| **Search Semântica**        |      |
| **Análise de Dependências** |      |
| **Indexação Completa**      |      |
| **Namespaces Ilimitados**   |      |
| **Trust Folder + Guardian** |      |
| **RBAC (5 roles)**          |      |
| **CLI Completo**            |      |
| **Harness Runtime**         |      |
| **Webhooks**                |      |
| **SSO/LDAP**                |      |
| **SLA Uptime**              |      |

### Integrações

| Plataforma             | Free          |
| ---------------------- | ------------- |
| **Claude Code (MCP)**  |               |
| **Cursor (MCP)**       |               |
| **VS Code Extension**  |               |
| **CLI**                |               |
| **ChatGPT Custom GPT** | (self-hosted) |
| **Gemini Integration** | (BYOK)        |

### Modelos de IA (BYOK)

Use seus próprios:

| Componente    | Opção               | Custo    |
| ------------- | ------------------- | -------- |
| **Embedding** | Voyage 4            | Grátis\* |
| **Reranking** | Voyage Rerank 2.5   | Grátis\* |
| **LLM**       | Gemini 3 Flash      | Grátis\* |
| **Local**     | Ollama (all-MiniLM) | Grátis   |

\*Free tier com limites: 60 req/min (Gemini), 50 req/min (Voyage)

---

## Limites

### Rate Limiting

```yaml
free_tier_limits:
  gemini_api:
    requests_per_minute: 60
    tokens_per_month: 1.5M

  voyage_api:
    requests_per_minute: 50
    tokens_per_month: 100M

  vectora_server:
    concurrent_users: 1
    searches_per_day: 1000
```

### Storage

- **Vector Index**: Unlimited (local disk)
- **Embeddings Cache**: 500MB
- **Logs**: 30 dias retidos

### Performance

- **Search Latency**: <2s
- **Concurrent Requests**: 1
- **Max File Size**: 100MB per file
- **Max Chunks per Search**: 20

---

## Como Começar

### Instalação

```bash
# Install globally
npm install -g @kaffyn/vectora

# Verify
vectora --version
```

### Primeira Execução

```bash
# 1. Inicializar projeto
cd ~/seu-projeto
vectora init --name "Meu Projeto"

# 2. Obter chaves gratuitas
# → Gemini: https://aistudio.google.com/app/apikey
# → Voyage: https://dash.voyageai.com/api-keys

# 3. Configurar
vectora config set --key GEMINI_API_KEY
vectora config set --key VOYAGE_API_KEY

# 4. Indexar
vectora index

# 5. Buscar!
vectora search "Como funciona login?"
```

### Com IDE (Claude Code, Cursor)

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "GEMINI_API_KEY": "sk-...",
        "VOYAGE_API_KEY": "sk-...",
        "VECTORA_NAMESPACE": "seu-namespace"
      }
    }
  }
}
```

---

## Casos de Uso Recomendados

### Melhor em Free

- **Codebase < 100K linhas**: Indexação em minutos
- **1 projeto**: 1 namespace, Trust Folder isolado
- **Equipes < 10 pessoas**: RBAC disponível
- **Desenvolvimento local**: Sem infraestrutura
- **Educação/pesquisa**: Open source MIT

### Considere Upgrade

- **Múltiplos projetos grandes**: > 5 projetos
- **Equipes > 10 pessoas**: Precisa LDAP/SSO
- **Alta frequência**: > 1000 buscas/dia
- **24/7 uptime**: Precisa SLA
- **Webhooks**: Para CI/CD automático

---

## Troubleshooting

### "Quota exceeded"

Você atingiu o limite mensal de API (Gemini ou Voyage).

**Soluções**:

1. Aguarde reset no 1º do próximo mês
2. Upgrade para Pro (unlimited)

### "Rate limit exceeded"

Você fez muitas requisições em 1 minuto.

**Solução**: Aguarde ou use espacing:

```bash
# Esperar entre buscas
for query in "login" "auth" "token"; do
  vectora search "$query"
  sleep 1
done
```

### "Concurrent users exceeded"

Apenas 1 usuário por vez no free tier (1 IDE).

**Soluções**:

1. Fechar outras instâncias
2. Upgrade para Pro (até 100 usuários)

---

## Roadmap para Pro

Quando crescer:

```text
Free (Seu Projeto)
    ↓
Pro (múltiplos projetos + webhooks)
    ↓
Team (LDAP + SLA + suporte)
    ↓
Enterprise (On-premise + support)
```

Nenhuma migração necessária - upgrade é automático.

---

## Support & Community

**Você não está sozinho!**

- **Docs**: [vectora.app/docs](https://vectora.app/docs)
- **GitHub**: [github.com/kaffyn/vectora](https://github.com/kaffyn/vectora)
- **Discussions**: [GitHub Discussions](https://github.com/kaffyn/vectora/discussions)
- **Issues**: [Report bugs](https://github.com/kaffyn/vectora/issues)

---

> **Próximo**: [Pro Plan](./pro.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
