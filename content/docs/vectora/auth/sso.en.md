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
  - integration
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

**Vectora Auth** is Vectora's independent identity system. It allows organizations to manage access to code intelligence sovereignly and in isolation.

## Standalone Identity

Unlike previous versions, Vectora now operates its own identity provider or allows connection with external providers (BYOI - Bring Your Own Identity).

## SSO Options

Vectora supports integration with leading market providers via standard protocols:

1. **OAuth2 / OpenID Connect (OIDC)**: Connect Vectora directly to Google Workspace, GitHub Enterprise, Okta, or Auth0.
2. **SAML 2.0**: Robust integration with Microsoft Azure AD and other enterprise providers.

## Provider Configuration

To configure an external provider, add the credentials to your configuration file or environment variables:

```env
VECTORA_AUTH_METHOD=oidc
VECTORA_OIDC_ISSUER=https://accounts.google.com
VECTORA_OIDC_CLIENT_ID=your_client_id
VECTORA_OIDC_CLIENT_SECRET=your_client_secret
```

## Authentication Flow

1. The user requests access via CLI or Interface.
2. Vectora redirects to the configured SSO provider.
3. After login, Vectora issues a locally signed **Vectora JWT**.
4. This token is used for all interactions with the search engine and MCP tools.

## External Linking

| Concept            | Resource                                        | Link                                                                                                   |
| ------------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **OpenID Connect** | OIDC Core 1.0 Specification                     | [openid.net/specs/openid-connect-core-1_0.html](https://openid.net/specs/openid-connect-core-1_0.html) |
| **JWT**            | RFC 7519: JSON Web Token Standard               | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)                 |
| **OAuth 2.0**      | RFC 6749: The OAuth 2.0 Authorization Framework | [datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749)                 |
| **MCP**            | Model Context Protocol Specification            | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                 |
| **MCP Go SDK**     | Go SDK for MCP (mark3labs)                      | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                                     |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
