---
title: Plus
slug: plus
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

O plano **Plus** é para equipes que escalam. Oferecemos dois modos: **BYOK** (suporte prioritário e limites aumentados) ou **Plus** (com créditos de IA e armazenamento gerenciado inclusos).

**$29/mês** por workspace (até 50 usuários) - _Plano Plus inclui créditos base_

## O Que Está Incluído

## Tudo do Free, PLUS

| Feature                   | Free       | Plus         |
| ------------------------- | ---------- | ------------ |
| **Namespaces Ilimitados** | [x]        | [x]          |
| **Buscas/mês**            | 30K        | Unlimited    |
| **Tokens Embedding/mês**  | 1.5M       | Unlimited    |
| **Tokens LLM/mês**        | 1.5M       | Unlimited    |
| **Usuários Simultâneos**  | 1          | 50           |
| **Rate Limiting**         | 60 req/min | 2000 req/min |
| **Webhooks**              | -          | [x]          |
| **Custom Domain**         | -          | [x]          |
| **API Tokens**            | -          | [x]          |
| **Advanced Metrics**      | -          | [x]          |
| **Priority Support**      | -          | [x]          |
| **99.9% SLA**             | -          | [x]          |
| **Custom Reranker**       | -          | [x]          |

## Modelos Premium

Acesso a mais modelos (BYOK ou Managed Plus):

| Componente    | Free              | Plus                   |
| ------------- | ----------------- | ---------------------- |
| **Embedding** | Voyage 4          | Voyage 4 + Claude 3    |
| **Reranking** | Voyage Rerank 2.5 | + Custom (Cohere, etc) |
| **LLM**       | Gemini Flash      | + Claude, GPT-4        |

## Limites Plus

```yaml
plus_tier_limits:
  rate_limiting:
    requests_per_minute: 2000
    concurrent_users: 50

  storage:
    vector_index: unlimited
    embeddings_cache: 5GB
    logs_retention: 90 days

  performance:
    search_latency: <500ms (p99)
    max_file_size: 500MB
    max_chunks_per_query: 100
```

## Webhooks

Automatize workflows com webhooks:

```bash
# Exemplo: Indexar ao fazer push no Git
POST https://seu-domain.vectora.app/webhooks/index
Authorization: Bearer sk-...
Content-Type: application/json

{
  "event": "repository.push",
  "branch": "main",
  "files_changed": 12
}

# Vectora reindexará automaticamente
```

## Eventos Disponíveis

| Evento                | Trigger                  |
| --------------------- | ------------------------ |
| `index.completed`     | Após indexação finalizar |
| `search.high_latency` | Busca > 1s               |
| `quota.warning`       | 80% da quota atingida    |
| `error.security`      | Guardian bloqueou acesso |
| `user.login`          | Novo user login          |

## Custom Domain

Acesse seu servidor via domínio customizado:

```bash
# Default (free)
https://api.vectora.app/project-abc123

# Custom (plus)
https://vectora.seu-dominio.com
# Ou
https://code-search.seu-dominio.com
```

## Setup CNAME

```bash
# Seu domínio:
code-search.seu-dominio.com CNAME vectora-plus.cloud.app
```

## API Tokens

Crie tokens para automação e CI/CD:

```bash
# Criar token
vectora auth token create \
  --name "CI/CD Pipeline" \
  --ttl 365d \
  --scopes "search,index"

# Output: sk-proj-abc123xyz...

# Usar em pipeline
curl -H "Authorization: Bearer sk-proj-abc123xyz..." \
  https://seu-dominio.vectora.com/search
```

## Scopes Disponíveis

```text
- search # Buscas
- index # Indexação
- configure # Alterar config
- user # Gerenciar users
- billing # Ver faturas
```

## Advanced Metrics

Dashboard com métricas detalhadas:

```text
Plus Users Dashboard
├─ Search Performance
│ ├─ p50 latency: 120ms
│ ├─ p95 latency: 280ms
│ ├─ p99 latency: 450ms
│ └─ Error rate: 0.1%
├─ Indexing Performance
│ ├─ Files indexed: 2,847
│ ├─ Chunks: 45,231
│ ├─ Index size: 150MB
│ └─ Last index: 2h ago
├─ User Activity
│ ├─ Active users: 23
│ ├─ Searches (24h): 1,234
│ ├─ Top queries: [...]
│ └─ Most used files: [...]
└─ Billing
   ├─ Current usage: $24.32
   ├─ Monthly limit: $100
   └─ Next billing: 2026-05-19
```

Exportar em CSV, JSON, ou Prometheus.

## Priority Support

- **Email support**: <4h response time
- **Direct Slack channel**: Para issues críticas
- **Monthly office hours**: Com time Vectora
- **Custom onboarding**: Setup + treinamento

## Pricing Transparente

## Cálculo

- **Base**: $29/mês
- **Usuários excedentes**: $0.50/mês por user (acima de 50)
- **Armazenamento excedente**: $0.10/GB/mês (acima de 5GB)

```text
Exemplo:
- 12 usuários: $29 (incluso até 50)
- 120 usuários: $29 + (70 × $0.50) = $64
```

## Sem Surpresas

- Sem setup fee
- Cancelamento anytime
- Sem contrato longo
- Faturamento automático

## Upgrade do Free

```bash
# Via CLI
vectora upgrade --plan plus --stripe-token sk_...

# Via dashboard
# https://console.vectora.app/settings/billing
```

## Migração Automática

- Todos os dados preservados
- Sem downtime
- Namespaces mantidos
- Configurações intactas

## Comparação: Free vs Pro

| Feature              | Free       | Plus         | Team      |
| -------------------- | ---------- | ------------ | --------- |
| **Price**            | Grátis     | $29/mês      | Custom    |
| **Users**            | 1          | 50           | Unlimited |
| **Rate Limit**       | 60 req/min | 2000 req/min | Custom    |
| **Tokens/mês**       | 1.5M       | Unlimited    | Unlimited |
| **Webhooks**         |            |              |           |
| **Custom Domain**    |            |              |           |
| **SLA**              |            | 99.9%        | 99.99%    |
| **Priority Support** |            |              |           |
| **SSO/LDAP**         |            |              |           |
| **On-Premise**       |            |              |           |

## Use Cases Ideais para Plus

- **Startups em crescimento**: 5-50 devs, múltiplos projetos
- **Agências**: Gerenciar projects de clientes diferentes
- **Teams remotos**: Precisa de 24/7 reliability
- **CI/CD Automation**: Webhooks para pipelines
- **Custom domain**: Branding próprio

## FAQ Plus

**P: Posso downgrade para Free depois?**
R: Sim, anytime. Seus dados são preservados.

**P: Quanto custa com 100 usuários?**
R: $29 + (50 × $0.50) = $54/mês

**P: Inclui suporte técnico?**
R: Sim, email <4h + Slack prioritário.

**P: Posso usar em produção?**
R: Sim, com 99.9% SLA (uptime garantido).

---

> **Próximo**: [Team Plan](./team.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
