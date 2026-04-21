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
{{< section-toggle >}}

Vectora's **Free** plan is fully **open source and time-unlimited**. Use it locally on any codebase without paying anything. Perfect for:

- Individual developers
- Small teams (< 10 people)
- Educational projects
- Prototyping and testing

## What's Included

## Core Features

| Feature                     | Free |
| --------------------------- | ---- |
| **Semantic Search**         | [x]  |
| **Dependency Analysis**     | [x]  |
| **Full Indexing**           | [x]  |
| **Unlimited Namespaces**    | [x]  |
| **Trust Folder + Guardian** | [x]  |
| **RBAC (5 roles)**          | [x]  |
| **Full CLI**                | [x]  |
| **Harness Runtime**         | [x]  |
| **Webhooks**                | [x]  |
| **SSO/LDAP**                | [x]  |
| **SLA Uptime**              | -    |

## Integrations

| Platform               | Free          |
| ---------------------- | ------------- |
| **Claude Code (MCP)**  | [x]           |
| **Cursor (MCP)**       | [x]           |
| **VS Code Extension**  | [x]           |
| **CLI**                | [x]           |
| **ChatGPT Custom GPT** | (self-hosted) |
| **Gemini Integration** | (BYOK)        |

## AI Models (BYOK)

Use your own:

| Component     | Option              | Cost   |
| ------------- | ------------------- | ------ |
| **Embedding** | Voyage 4            | Free\* |
| **Reranking** | Voyage Rerank 2.5   | Free\* |
| **LLM**       | Gemini 3 Flash      | Free\* |
| **Local**     | Ollama (all-MiniLM) | Free   |

\*Free tier with limits: 60 req/min (Gemini), 50 req/min (Voyage)

---

## Limits

## Rate Limiting

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

## Storage

- **Vector Index**: Unlimited (local disk)
- **Embeddings Cache**: 500MB
- **Logs**: 30 days retention

## Performance

- **Search Latency**: <2s
- **Concurrent Requests**: 1
- **Max File Size**: 100MB per file
- **Max Chunks per Search**: 20

---

## How to Start

## Installation

```bash
# Install globally
npm install -g @kaffyn/vectora

# Verify
vectora --version
```

## First Run

```bash
# 1. Initialize project
cd ~/your-project
vectora init --name "My Project"

# 2. Obtain free keys
# → Gemini: https://aistudio.google.com/app/apikey
# → Voyage: https://dash.voyageai.com/api-keys

# 3. Configure
vectora config set --key GEMINI_API_KEY
vectora config set --key VOYAGE_API_KEY

# 4. Index
vectora index

# 5. Search!
vectora search "How does login work?"
```

## With IDE (Claude Code, Cursor)

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
        "VECTORA_NAMESPACE": "your-namespace"
      }
    }
  }
}
```

---

## Recommended Use Cases

## Best in Free

- **Codebase < 100K lines**: Indexing in minutes
- **1 project**: 1 namespace, isolated Trust Folder
- **Teams < 10 people**: RBAC available
- **Local development**: No infrastructure needed
- **Education/research**: Open source (MIT)

## Consider Upgrade

- **Multiple large projects**: > 5 projects
- **Teams > 10 people**: Needs LDAP/SSO
- **High frequency**: > 1000 searches/day
- **24/7 uptime**: Needs SLA
- **Webhooks**: For automated CI/CD

---

## Troubleshooting

## "Quota exceeded"

You have reached the monthly API limit (Gemini or Voyage).

**Solutions**:

1. Wait for reset on the 1st of the next month
2. Upgrade to Pro (unlimited)

## "Rate limit exceeded"

You made too many requests in 1 minute.

**Solution**: Wait or use spacing:

```bash
# Wait between searches
for query in "login" "auth" "token"; do
  vectora search "$query"
  sleep 1
done
```

## "Concurrent users exceeded"

Only 1 user at a time in the free tier (1 IDE).

**Solutions**:

1. Close other instances
2. Upgrade to Pro (up to 100 users)

---

## Roadmap to Pro

When you grow:

```text
Free (Your Project)
    ↓
Pro (Multiple projects + webhooks)
    ↓
Team (LDAP + SLA + support)
    ↓
Enterprise (On-premise + support)
```

No migration required - upgrade is automatic.

---

## Support & Community

**You're not alone!**

- **Docs**: [vectora.app/docs](https://vectora.app/docs)
- **GitHub**: [github.com/kaffyn/vectora](https://github.com/kaffyn/vectora)
- **Discussions**: [GitHub Discussions](https://github.com/kaffyn/vectora/discussions)
- **Issues**: [Report bugs](https://github.com/kaffyn/vectora/issues)

---

> **Next**: [Pro Plan](./pro.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
