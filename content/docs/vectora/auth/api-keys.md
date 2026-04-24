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

As API Keys do Vectora são usadas para autenticação programática e integração com ferramentas de terceiros que não suportam fluxos interativos de SSO.

## Visão Geral

Diferente do JWT, que é destinado a sessões de curta duração, as API Keys são persistentes e permitem o acesso controlado a namespaces específicos do Vectora.

## Segurança

O Vectora utiliza hashing unidirecional (SHA-256) para armazenar suas chaves. Isso significa que, mesmo se o banco de dados for comprometido, suas chaves originais não podem ser recuperadas.

## Como Usar

Para autenticar uma requisição REST usando uma API Key, envie o cabeçalho `X-API-Key`:

```bash
curl -X POST https://api.vectora.app/v1/search \
  -H "X-API-Key: vca_live_xxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "como funciona o auth?"}'
```

## Gestão de Chaves

Você pode gerenciar suas chaves através da CLI do Vectora:

```bash
# Criar uma nova chave
vectora auth keys create --name "GitHub Actions" --namespace "prod"

# Listar chaves ativas
vectora auth keys list

# Revogar uma chave
vectora auth keys revoke <key_id>
```

## External Linking

### Referência de Segurança e Gestão

| Conceito                   | Recurso           | Link                                                                                                   |
| :------------------------- | :---------------- | :----------------------------------------------------------------------------------------------------- |
| **API Key Best Practices** | Google Cloud Docs | [cloud.google.com/docs/authentication/api-keys](https://cloud.google.com/docs/authentication/api-keys) |
| **SHA-256**                | NIST Standard     | [csrc.nist.gov/projects/hash-functions](https://csrc.nist.gov/projects/hash-functions)                 |
| **RBAC**                   | Auth0 Blog        | [auth0.com/blog/role-based-access-control/](https://auth0.com/blog/role-based-access-control/)         |
