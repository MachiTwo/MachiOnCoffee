---
title: SSO (Vectora Auth)
slug: sso
date: "2026-04-23T00:00:00-03:00"
type: docs
tags:
  - ai
  - auth
  - concepts
  - config
  - mcp
  - oidc
  - saml
  - security
  - sso
  - system
  - tools
  - vectora
---

{{< lang-toggle >}}

O **Vectora Auth** é o sistema de identidade independente do Vectora. Ele permite que organizações gerenciem o acesso à inteligência de código de forma soberana e isolada.

## Identidade Standalone

Diferente de versões anteriores, o Vectora agora opera seu próprio provedor de identidade ou permite a conexão com provedores externos (BYOI - Bring Your Own Identity).

## Opções de SSO

O Vectora suporta integração com os principais provedores do mercado via protocolos padrão:

1. **OAuth2 / OpenID Connect (OIDC)**: Conecte o Vectora diretamente ao Google Workspace, GitHub Enterprise, Okta ou Auth0.
2. **SAML 2.0**: Integração robusta com Microsoft Azure AD e outros provedores corporativos.

## Configuração do Provedor

Para configurar um provedor externo, adicione as credenciais no seu arquivo de configuração ou variáveis de ambiente:

```env
VECTORA_AUTH_METHOD=oidc
VECTORA_OIDC_ISSUER=https://accounts.google.com
VECTORA_OIDC_CLIENT_ID=seu_client_id
VECTORA_OIDC_CLIENT_SECRET=seu_client_secret
```

## Fluxo de Autenticação

1. O usuário solicita acesso via CLI ou Interface.
2. O Vectora redireciona para o provedor SSO configurado.
3. Após o login, o Vectora emite um **Vectora JWT** assinado localmente.
4. Este token é usado para todas as interações com o motor de busca e ferramentas MCP.

## External Linking

| Concept            | Resource                                        | Link                                                                                                   |
| ------------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **OpenID Connect** | OIDC Core 1.0 Specification                     | [openid.net/specs/openid-connect-core-1_0.html](https://openid.net/specs/openid-connect-core-1_0.html) |
| **JWT**            | RFC 7519: JSON Web Token Standard               | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)                 |
| **OAuth 2.0**      | RFC 6749: The OAuth 2.0 Authorization Framework | [datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749)                 |
| **MCP**            | Model Context Protocol Specification            | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                 |
| **MCP Go SDK**     | Go SDK for MCP (mark3labs)                      | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
