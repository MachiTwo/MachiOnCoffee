---
title: General
slug: general
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - general
  - mcp
  - vectora
---

{{< lang-toggle >}}

Quick answers to the most common questions about Vectora — functionality, cost, production use, security, and more.

## What is Vectora?

**Vectora** is a **semantic search engine** for code that indexes your entire codebase and allows you to search by semantic meaning, not just keywords. It integrates with IDEs (Claude Code, Cursor, VS Code) via MCP to provide intelligent and governed context to your AI agent.

**How it works:**

1. You index your code (`npm install -g vectora && vectora index`).
2. Code is split into chunks and embedded via Voyage 4 (1,536D vectors).
3. Vectors are stored in Qdrant with metadata (file, lines, namespace).
4. When you make a query ("How to validate tokens?"), Vectora:
   - Transforms the query into a vector.
   - Searches for similar chunks via HNSW (fast nearest neighbors).
   - Re-ranks the top 100 → top 10 via Voyage Rerank 2.5.
   - Returns chunks with structured context.

**Practical example:**

- **Query**: "How to validate JWT tokens?"
- **Without Vectora**: Searching for "JWT" returns 5 files, none of which are useful.
- **With Vectora**: Finds `validateToken()` in auth.ts, middleware in guards.ts, types in jwt.types.ts — all relevant.

**Result**: Your AI agent receives governed + validated context, not hallucinations.

---

## How It Works

```text
1. Index your code (once)
   - Splits into chunks
   - Generates embeddings (Voyage 4)
   - Stores in Qdrant

2. Semantic Search
   - Your question → embedding
   - HNSW searches for similar chunks
   - Re-ranking (Voyage Rerank 2.5)
   - Returns top 10

3. IDE Integration
   - Claude Code / Cursor / VS Code
   - Shows contextual chunks
   - You stay in your flow
```

---

## What is the Cost?

**Free Tier** (forever):

- Unlimited local searches.
- Unlimited indexing.
- 60 req/min API limits (Gemini, Voyage).
- BYOK (Bring Your Own Key).

**Pro** ($29/month):

- Unlimited API requests.
- 50 concurrent users.
- Webhooks + custom domain.
- 99.9% SLA.

**Team** (Custom):

- On-premise + SSO/LDAP.
- 99.99% SLA.
- Dedicated support.

---

## How Long Does It Take to Index?

**First time**:

- 10K lines: < 1 minute.
- 100K lines: 5-10 minutes.
- 1M lines: 30-60 minutes.

**Incremental** (changes only):

- Generally < 30 seconds.

---

## How Much Disk Space?

The ratio is approximately **1:10**.

If your code is 50MB:

- Qdrant Index: ~5MB.
- Cache: 100MB.

**Total**: ~105MB.

---

## Can I Use It in Production?

**Free Tier**: No (1 concurrent user, no SLA).

**Pro Tier**: Yes (99.9% SLA, up to 50 users).

**Team Tier**: Yes (99.99% SLA, on-premise option).

---

## Is My Data Secure?

**YES.**

- BYOK — you control the keys.
- Encrypted on disk (AES-256).
- Encrypted in transit (TLS 1.3).
- Guardian blocklist (protects .env, secrets).
- RBAC (user control).
- Audit logging (tracks everything).

---

## Which Languages are Supported?

**All of them:**

- TypeScript / JavaScript
- Python
- Go
- Java / Kotlin
- C# / .NET
- Rust
- C++ / C
- Ruby
- PHP
- SQL
- YAML / JSON
- Markdown

Voyage 4 (embedding model) understands semantic structures in any language.

---

## Can I Use It Offline?

**Not completely, but almost.**

```text
Embedding: Requires Voyage API
Re-ranking: Requires Voyage Rerank API
LLM: Requires Gemini API
Local Search: 100% offline (local Qdrant)
```

**100% Offline Alternative**:
Use Ollama for local embeddings:

```bash
docker run ollama/ollama
vectora config set EMBEDDING_PROVIDER ollama
```

---

## How Much Does It Cost to Scale?

| Aspect         | Free      | Pro        | Team       |
| -------------- | --------- | ---------- | ---------- |
| **Code**       | Unlimited | Unlimited  | Unlimited  |
| **Users**      | 1         | 50         | Unlimited  |
| **API calls**  | 60/min    | Unlimited  | Custom     |
| **Extra cost** | Free      | $0.50/user | Contact us |

**Scaling example:**

- 1 person: Free.
- 5 people: Pro ($29).
- 50+ people: Team ($X).

---

## How Does It Work with Multiple Projects?

Each project has its own namespace:

```bash
# Project A
vectora init --namespace "company-projectA"

# Project B
vectora init --namespace "company-projectB"

# They are completely isolated
# Searching in A will not find chunks from B
```

---

## Can I Use Vectora with Git?

**Yes.**

```bash
# Ignore the index
echo ".vectora/" >> .gitignore

# Rebuild on new clone
git clone ...
vectora index
```

**Suggestion**: Commit `vectora.config.yaml`, ignore `.vectora/`.

---

## Which IDE is Best?

| IDE         | Vectora    | Advantage              |
| ----------- | ---------- | ---------------------- |
| Claude Code | Native MCP | Perfect integration    |
| Cursor      | Native MCP | Similar to Claude Code |
| VS Code     | Extension  | Native editor UI       |
| ChatGPT     | Custom GPT | Stay inside ChatGPT    |

**Recommendation**: Use the one you already use. Vectora works equally well on all.

---

## Can I Delete a File?

Do you still want it to be indexed?

**Yes**: Reorganize (move file).

```bash
mv src/old-api.ts src/deprecated/old-api.ts
vectora index --incremental
# New path is indexed, old one is removed
```

**No**: Delete completely.

```bash
rm src/old-api.ts
vectora index --incremental
# Related chunks are removed
```

---

## How Long Does a Search Take?

Generally:

- **Embedding**: ~100ms
- **Search (HNSW)**: ~80ms
- **Re-ranking**: ~50ms
- **Total**: **~230ms**

With network latency (APIs):

- **Total with latency**: ~300-500ms

---

## Is There a Project Size Limit?

**Local (Free)**: No (limited by disk space).

**Pro**: No (AWS managed).

**Team**: Tested up to 10M chunks.

---

## Can I Share a Project?

**Yes:**

```bash
# Invite user
vectora user create \
  --email colleague@company.com \
  --namespace your-project \
  --role editor

# Colleague can now search and index
```

---

## How Do I Perform a Backup?

```bash
# Export everything
vectora export --namespace your-project --output backup.tar.gz

# Then:
# Store in S3, Azure, or locally
```

To restore:

```bash
vectora import --from backup.tar.gz --namespace your-project
```

---

## Can I Use My Own LLM?

**Yes, via API.**

```yaml
# vectora.config.yaml
providers:
  llm:
    name: "openai" # or "anthropic", "custom"
    model: "gpt-4"
    api_key: "${OPENAI_API_KEY}"
```

Or locally (Ollama):

```bash
docker run ollama/ollama
vectora config set LLM_PROVIDER ollama
```

---

## Does It Support Multiple Languages?

**Code**: Yes, all languages.

**Interface**: Yes.

- Portuguese
- English
- Spanish (coming soon)
- French (coming soon)

---

## Is There a REST API?

**Yes, in Pro and Team plans.**

```bash
curl -X POST https://your-domain.vectora.app/search \
  -H "Authorization: Bearer sk-proj-..." \
  -d '{"query": "login", "top_k": 10}'
```

---

## Can I Use It in a Monorepo?

**Yes.**

```yaml
# vectora.config.yaml
indexing:
  paths:
    - packages/backend/src
    - packages/frontend/src
    - packages/shared/src
  exclude:
    - node_modules
    - build
    - dist
```

---

## What is the Community?

### Open Source (MIT License)

- GitHub: [github.com/kaffyn/vectora](https://github.com/kaffyn/vectora)
- Discussions: [GitHub Discussions](https://github.com/kaffyn/vectora/discussions)
- Issues: [Bug reports](https://github.com/kaffyn/vectora/issues)
- Docs: [vectora.app/docs](https://vectora.app/docs)

---

> **Next**: [FAQ - Billing](./billing.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
