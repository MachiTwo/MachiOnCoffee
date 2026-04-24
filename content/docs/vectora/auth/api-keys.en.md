---
title: API Keys
slug: api-keys
date: "2026-04-23T00:00:00-03:00"
type: docs
tags:
  - auth
  - api-keys
  - security
  - integration
---

{{< lang-toggle >}}

Vectora API Keys are used for programmatic authentication and integration with third-party tools that do not support interactive SSO flows.

## Overview

Unlike JWT, which is intended for short-lived sessions, API Keys are persistent and allow controlled access to specific Vectora namespaces.

## Security

Vectora uses one-way hashing (SHA-256) to store your keys. This means that even if the database is compromised, your original keys cannot be recovered.

## How to Use

To authenticate a REST request using an API Key, send the `X-API-Key` header:

```bash
curl -X POST https://api.vectora.app/v1/search \
  -H "X-API-Key: vca_live_xxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "how does auth work?"}'
```

## Key Management

You can manage your keys through the Vectora CLI:

```bash
# Create a new key
vectora auth keys create --name "GitHub Actions" --namespace "prod"

# List active keys
vectora auth keys list

# Revoke a key
vectora auth keys revoke <key_id>
```

## External Linking

### Security & Management Reference

| Concept                    | Resource          | Link                                                                                                   |
| :------------------------- | :---------------- | :----------------------------------------------------------------------------------------------------- |
| **API Key Best Practices** | Google Cloud Docs | [cloud.google.com/docs/authentication/api-keys](https://cloud.google.com/docs/authentication/api-keys) |
| **SHA-256**                | NIST Standard     | [csrc.nist.gov/projects/hash-functions](https://csrc.nist.gov/projects/hash-functions)                 |
| **RBAC**                   | Auth0 Blog        | [auth0.com/blog/role-based-access-control/](https://auth0.com/blog/role-based-access-control/)         |
