---
title: Pro
slug: pro
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

## Overview

The **Pro** plan is for scaling teams. We offer two modes: **BYOK** (priority support and increased limits) or **Plus** (with included AI credits and managed storage).

**$29/month** per workspace (up to 50 users) - _Plus Plan includes base credits_

---

## What's Included

### Everything in Free, PLUS

| Feature                    | Free       | Pro          |
| -------------------------- | ---------- | ------------ |
| **Unlimited Namespaces**   |            |              |
| **Searches/month**         | 30K        | Unlimited    |
| **Embedding Tokens/month** | 1.5M       | Unlimited    |
| **LLM Tokens/month**       | 1.5M       | Unlimited    |
| **Concurrent Users**       | 1          | 50           |
| **Rate Limiting**          | 60 req/min | 2000 req/min |
| **Webhooks**               | -          |              |
| **Custom Domain**          | -          |              |
| **API Tokens**             | -          |              |
| **Advanced Metrics**       | -          |              |
| **Priority Support**       | -          |              |
| **99.9% SLA**              | -          |              |
| **Custom Reranker**        | -          |              |

### Premium Models

Access to more models (BYOK or Managed Plus):

| Component     | Free              | Pro                     |
| ------------- | ----------------- | ----------------------- |
| **Embedding** | Voyage 4          | Voyage 4 + Claude 3     |
| **Reranking** | Voyage Rerank 2.5 | + Custom (Cohere, etc.) |
| **LLM**       | Gemini Flash      | + Claude, GPT-4         |

---

## Pro Limits

```yaml
pro_tier_limits:
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

---

## Webhooks

Automate workflows with webhooks:

```bash
# Example: Index on Git push
POST https://your-domain.vectora.app/webhooks/index
Authorization: Bearer sk-...
Content-Type: application/json

{
  "event": "repository.push",
  "branch": "main",
  "files_changed": 12
}

# Vectora will automatically reindex
```

### Available Events

| Event                 | Trigger                  |
| --------------------- | ------------------------ |
| `index.completed`     | After indexing completes |
| `search.high_latency` | Search > 1s              |
| `quota.warning`       | 80% quota reached        |
| `error.security`      | Guardian blocked access  |
| `user.login`          | New user login           |

---

## Custom Domain

Access your server via a custom domain:

```bash
# Default (free)
https://api.vectora.app/project-abc123

# Custom (pro)
https://vectora.your-domain.com
# Or
https://code-search.your-domain.com
```

### CNAME Setup

```bash
# Your domain:
code-search.your-domain.com CNAME vectora-pro.cloud.app
```

---

## API Tokens

Create tokens for automation and CI/CD:

```bash
# Create token
vectora auth token create \
  --name "CI/CD Pipeline" \
  --ttl 365d \
  --scopes "search,index"

# Output: sk-proj-abc123xyz...

# Use in pipeline
curl -H "Authorization: Bearer sk-proj-abc123xyz..." \
  https://your-domain.vectora.com/search
```

### Available Scopes

```text
- search # Searches
- index # Indexing
- configure # Change configuration
- user # Manage users
- billing # View invoices
```

---

## Advanced Metrics

Dashboard with detailed metrics:

```text
Pro Users Dashboard
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

Export to CSV, JSON, or Prometheus.

---

## Priority Support

- **Email support**: <4h response time
- **Direct Slack channel**: For critical issues
- **Monthly office hours**: With the Vectora team
- **Custom onboarding**: Setup + training

---

## Transparent Pricing

### Calculation

- **Base**: $29/month
- **Excess users**: $0.50/month per user (above 50)
- **Excess storage**: $0.10/GB/month (above 5GB)

```text
Example:
- 12 users: $29 (included up to 50)
- 120 users: $29 + (70 × $0.50) = $64
```

### No Surprises

- No setup fee
- Cancel anytime
- No long-term contract
- Automatic billing

---

## Upgrading from Free

```bash
# Via CLI
vectora upgrade --plan pro --stripe-token sk_...

# Via dashboard
# https://console.vectora.app/settings/billing
```

### Automatic Migration

- All data preserved
- No downtime
- Namespaces maintained
- Configuration intact

---

## Comparison: Free vs Pro

| Feature              | Free       | Pro          | Team      |
| -------------------- | ---------- | ------------ | --------- |
| **Price**            | Free       | $29/month    | Custom    |
| **Users**            | 1          | 50           | Unlimited |
| **Rate Limit**       | 60 req/min | 2000 req/min | Custom    |
| **Tokens/month**     | 1.5M       | Unlimited    | Unlimited |
| **Webhooks**         | -          |              |           |
| **Custom Domain**    | -          |              |           |
| **SLA**              | -          | 99.9%        | 99.99%    |
| **Priority Support** | -          |              |           |
| **SSO/LDAP**         | -          | -            |           |
| **On-Premise**       | -          | -            |           |

---

## Ideal Use Cases for Pro

- **Growing startups**: 5-50 devs, multiple projects
- **Agencies**: Manage different client projects
- **Remote teams**: Needs 24/7 reliability
- **CI/CD Automation**: Webhooks for pipelines
- **Custom domain**: Custom branding

---

## Pro FAQ

**Q: Can I downgrade to Free later?**
A: Yes, anytime. Your data is preserved.

**Q: How much does it cost with 100 users?**
A: $29 + (50 × $0.50) = $54/month.

**Q: Does it include technical support?**
A: Yes, email response < 4h + priority Slack.

**Q: Can I use it in production?**
A: Yes, with 99.9% SLA (guaranteed uptime).

---

> **Next**: [Team Plan](./team.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
