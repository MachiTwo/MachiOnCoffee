---
title: Error Codes Reference
slug: errors
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - concepts
  - config
  - embeddings
  - errors
  - gemini
  - mcp
  - mongodb-atlas
  - protocol
  - rbac
  - reference
  - reranker
  - system
  - troubleshooting
  - vector-search
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}

Referência completa de códigos de erro: códigos HTTP, mensagens, causas raízes e soluções.

## 400 - Bad Request

Seu request está malformado ou com parâmetros inválidos.

| Erro                     | Causa                                        | Solução                                                     |
| ------------------------ | -------------------------------------------- | ----------------------------------------------------------- |
| `INVALID_QUERY`          | Query muito curta (<3 chars) ou longa (>10K) | Reformule: "Como validar tokens?" (5-100 chars recomendado) |
| `INVALID_NAMESPACE`      | Namespace não existe                         | Crie com `vectora namespace create seu-ns`                  |
| `INVALID_PARAMS`         | top_k não é número, filter inválido          | Verifique tipos: `{"top_k": 10, "namespace": "proj"}`       |
| `MISSING_REQUIRED_FIELD` | Faltam campos obrigatórios                   | Query e namespace são obrigatórios                          |

**Debug**: Use `vectora search --debug` para ver payload exato.

## 401 - Unauthorized

Falha de autenticação ou permissão.

| Erro                  | Causa                      | Solução                                                  |
| --------------------- | -------------------------- | -------------------------------------------------------- |
| `INVALID_TOKEN`       | Token expirado ou inválido | Gere novo: `vectora auth token create`                   |
| `MISSING_CREDENTIALS` | API key não configurada    | `vectora config set GEMINI_API_KEY "sua-chave"`          |
| `PERMISSION_DENIED`   | Seu role não tem permissão | Contate admin para upgrade (Owner/Admin pode mudar RBAC) |
| `SESSION_EXPIRED`     | Sessão > 7 dias            | Reautentique: `vectora auth login`                       |

**Debug**: `vectora auth status` mostra token atual e expiration.

## 404 - Not Found

Recurso não existe.

| Erro                  | Causa                                   | Solução                            |
| --------------------- | --------------------------------------- | ---------------------------------- |
| `NAMESPACE_NOT_FOUND` | Namespace deletado ou não compartilhado | Liste com `vectora namespace list` |
| `FILE_NOT_FOUND`      | Arquivo não está indexado               | Reindex: `vectora index --force`   |
| `CHUNK_NOT_FOUND`     | Chunk foi deletado                      | Não há solução, chunk foi removido |

## 429 - Rate Limited

Você excedeu quotas de rate limit ou API.

| Erro                  | Limite                          | Solução                                             |
| --------------------- | ------------------------------- | --------------------------------------------------- |
| `RATE_LIMIT_EXCEEDED` | 60 req/min                      | Aguarde 1 min ou implemente backoff exponencial     |
| `QUOTA_EXCEEDED`      | Atingiu limite mensal de tokens | Upgrade para Pro (500k tokens/mês) ou aguarde reset |
| `CONCURRENT_LIMIT`    | Muitas requests simultâneas     | Use connection pooling, máximo 10 concurrent        |

**Debug**: Headers de resposta mostram `X-RateLimit-Remaining`.

## 500 - Server Error

Erro interno do Vectora ou dependências.

| Erro               | Causa                      | Solução                                                 |
| ------------------ | -------------------------- | ------------------------------------------------------- |
| `EMBEDDING_FAILED` | Voyage API indisponível    | Verifique `VOYAGE_API_KEY` e status da Voyage           |
| `SEARCH_FAILED`    | MongoDB Atlas indisponível | Verifique conexão de rede, status do cluster            |
| `RERANK_FAILED`    | Reranker offline           | Aguarde recovery automático (3s retry)                  |
| `LLM_ERROR`        | Gemini API erro            | Verifique `GEMINI_API_KEY` e quota na Google AI Console |
| `TIMEOUT`          | Request > 30s              | Query muito complexa, simplifique                       |

**Debug**: Stack trace completo em `~/.vectora/logs/error.log`.

## CLI Exit Codes

```text
0 Sucesso
1 Erro genérico
2 Config erro (arquivo YAML inválido)
3 API erro (500, timeout)
4 Auth falhou (401, invalid token)
5 Namespace não encontrado (404)
127 Comando não encontrado
```

## Habilitar Debug Mode

Para problemas complexos, o modo de depuração fornece uma visão detalhada das entranhas do sistema, incluindo logs de rede e payloads brutos de API.

## Exemplo: Troubleshoot Erro Comum

```bash
# Debug mode mostra stack traces e verbose logging
VECTORA_DEBUG=true vectora search "query"

# Ou com flag
vectora --debug search "query"

# Ou globalmente
vectora config set DEBUG true
```

Para facilitar a resolução, mantenha seu ambiente atualizado e verifique as configurações de rede antes de realizar procedimentos manuais de troca de tokens.

## Relatando Bugs

**Cenário**: `INVALID_TOKEN` ao usar MCP em Claude Code

```bash
# 1. Verifique se token existe
vectora auth status
# Output: Token: exp_...abc | Expires: 2026-05-19

# 2. Se expirado, regenere
vectora auth token create
# Output: New token: exp_...xyz | Valid until: 2026-06-19

# 3. Atualize Claude Code config
# ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_TOKEN": "exp_...xyz" # Token novo aqui
      }
    }
  }
}

# 4. Reinicie Claude Code
```

## Reportar um Bug Não Documentado

Se vê um erro não documentado:

1. Colete logs: `vectora logs --since 1h`
2. Habilite debug: `VECTORA_DEBUG=true vectora ...`
3. Abra issue: <https://github.com/Kaffyn/Vectora/issues>
4. Inclua: erro, stack trace, comando usado

---

> Encontrou um erro não documentado aqui? [Reporte](https://github.com/Kaffyn/Vectora/issues)

## External Linking

| Concept               | Resource                             | Link                                                                                                       |
| --------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **MongoDB Atlas**     | Atlas Vector Search Documentation    | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **MCP**               | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                     |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                                         |
| **Anthropic Claude**  | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                                         |
| **Voyage Embeddings** | Voyage Embeddings Documentation      | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)                             |
| **Voyage Reranker**   | Voyage Reranker API                  | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)                                 |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
