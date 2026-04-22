---
title: Namespaces
slug: namespaces
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - auth
  - concepts
  - config
  - mcp
  - namespaces
  - security
  - system
  - vectora
  - yaml
---

{{< lang-toggle >}}
Namespaces are **logical isolators** of vector indices within a single cluster. Each project, environment, or context runs in its own namespace, preventing results contamination.

> [!IMPORTANT] A namespace is like a "virtual database" within the system. Searches in one namespace NEVER return chunks from another namespace.

## The Problem

Without namespaces:

- Searching for "login" returns chunks from 50 different projects
- Easy to "leak" context between teams
- Impossible to manage indices by project or environment

With namespaces:

- Search is isolated: "login" returns ONLY from project X
- Multiple teams can share an instance without contamination
- Scalability: adding a new project = new namespace

## Naming & Conventions

Standardizing namespace names is essential for organization and automation in multi-tenant clusters.

## Recommended Pattern

```text
<org>-<project>-<environment>
```

Examples:

```yaml
kaffyn-vectora-prod # Org-Project-Env
kaffyn-vectora-dev # Same project, different environment
acme-backend-staging # Another project
```

## Validation

Namespaces must:

- Have 3-63 characters
- Use only `[a-z0-9-]` (lowercase, numbers, hyphens)
- Start with a letter
- NOT include underscores or spaces

## Lifecycle

Namespace management covers everything from technical initialization to secure disposal of indexed data.

## Creation

```bash
# Via CLI
vectora namespace create --name kaffyn-vectora-prod

# Via config
vectora.config.yaml:
  project:
    namespace: kaffyn-vectora-prod
```

## Indexing

Once created, the namespace accepts chunks:

```yaml
# indexing.yaml
namespace: kaffyn-vectora-prod
```

## Search

Every search specifies a namespace:

```typescript
// Search is filtered by namespace
const results = await vectoraClient.search({
  query: "How to validate tokens?",
  namespace: "kaffyn-vectora-prod",
  top_k: 10,
});
```

## Multi-Tenancy Patterns

Using namespaces allows for the implementation of different isolation patterns depending on the needs of the project or organization.

## Pattern 1: One Namespace per Project

```yaml
# Team A
namespace: acme-backend-prod

# Team B
namespace: acme-frontend-prod
```

Use when: Completely separate teams, rigorous compliance/security.

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
