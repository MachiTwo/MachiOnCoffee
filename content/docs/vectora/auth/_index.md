---
title: Auth
slug: auth
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - guardian
  - mcp
  - mcp-protocol
  - vectora
---

{{< lang-toggle >}}
A camada de autenticação do Vectora garante que apenas usuários e serviços autorizados acessem recursos, namespaces e operações sensíveis. Esta seção documenta os mecanismos de identidade, gestão de chaves de API e controle de acesso que protegem sua infraestrutura de contexto.

## Autenticação e Autorização no Vectora

> [!IMPORTANT] > **Segurança na aplicação, não no banco**: O Vectora implementa RBAC, validação de namespace e sanitização na camada de aplicação (`Guardian`, `RBAC Logic`). O backend (MongoDB Atlas) armazena dados; a aplicação decide quem pode acessar o quê.

---

## Tópicos desta seção

| Página                                   | Descrição                                                                                                |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [SSO / Identidade Unificada](/auth/sso/) | Autenticação centralizada, gestão de sessões e integração com provedores externos (GitHub, Google, SAML) |
| [API Keys](/auth/api-keys/)              | Criação, rotação e escopos de chaves de API para integração programática com o Vectora                   |

---

## Fluxo de Autenticação Típico

```mermaid
graph LR
    A[Usuário / Serviço] --> B{Tipo de Acesso}
    B -->|Humano| C[Login via SSO]
    B -->|Máquina| D[API Key com escopo]

    C --> E[JWT com claims: userId, roles, namespaces]
    D --> F[Validação de chave + rate limiting]

    E --> G[Middleware RBAC]
    F --> G

    G --> H{Permissão concedida?}
    H -->|Sim| I[Executa operação]
    H -->|Não| J[Retorna 403 Forbidden]
```

---

## Conceitos Fundamentais

| Termo            | Definição                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| **Namespace**    | Isolamento lógico de dados e operações; cada projeto/time tem seu namespace                      |
| **RBAC**         | Role-Based Access Control: roles como `reader`, `contributor`, `admin` definem permissões        |
| **API Key**      | Token de acesso para integração programática, com escopos granulares (`read`, `write`, `search`) |
| **JWT**          | JSON Web Token assinado que carrega claims de identidade e permissões                            |
| **Trust Folder** | Escopo de filesystem permitido para operações; validado antes de qualquer tool call              |

---

## Boas Práticas de Segurança

**Use API Keys com escopo mínimo**: Conceda apenas `read` se a integração não precisa escrever
**Rotação periódica de chaves**: Renove API Keys a cada 90 dias ou após incidentes
**Valide namespaces em cada chamada**: Não confie apenas no token; revalide escopo no runtime
**Monitore logs de auditoria**: Use `audit_logs` para detectar acessos anômalos
**Nunca exponha chaves no client**: API Keys pertencem ao backend ou ao agent principal, nunca ao browser

> [!WARNING] > **Blocklist hard-coded**: Arquivos como `.env`, `.key`, `.pem` são bloqueados pelo `Guardian` antes de qualquer processamento — independente de autenticação. Segurança por código, não por configuração.

---

## Integração com Seu Sistema

#### Exemplo: Validação de JWT no seu backend

```ts
// Exemplo: middleware de validação de JWT
import { verifyJWT } from "@vectora/auth";

export async function authMiddleware(req: Request, next: Handler) {
  const token = req.headers.get("Authorization")?.replace("Bearer ", "");
  if (!token) return next({ status: 401, error: "Missing token" });

  try {
    const claims = await verifyJWT(token, { audience: "vectora-api" });
    req.context = { userId: claims.sub, roles: claims.roles, namespaces: claims.namespaces };
    return next();
  } catch {
    return next({ status: 403, error: "Invalid token" });
  }
}
```

#### Exemplo: Uso de API Key em chamada MCP

```json
{
  "mcpServers": {
    "vectora": {
      "command": "npx",
      "args": ["vectora-agent", "mcp-serve"],
      "env": {
        "VECTORA_API_KEY": "vca_live_...",
        "VECTORA_NAMESPACE": "my-project"
      }
    }
  }
}
```

---

## Perguntas Frequentes

**P: Preciso de SSO para usar o Vectora?**
R: Não. O plano Free usa autenticação local via `vectora auth login`. SSO é disponível nos planos Pro/Team para integração com provedores corporativos.

**P: Posso usar minha própria infraestrutura de auth?**
R: Sim. O Vectora aceita qualquer JWT válido configurado via `auth.jwt.publicKey`. Consulte [SSO](/auth/sso/) para detalhes de integração customizada.

**P: Como revogo uma API Key comprometida?**
R: Via dashboard (`/settings/api-keys`) ou CLI: `vectora api-key revoke --id <key_id>`. A revogação é imediata em todos os nós.

**P: O Vectora armazena minhas credenciais?**
R: Não. Chaves de API são armazenadas como hash (bcrypt). Tokens JWT são validados, não persistidos. Credenciais de providers (Gemini, Voyage) são fornecidas via BYOK e nunca tocadas pela Kaffyn.

---

> **Frase para guardar**:
> _"Autenticação verifica quem você é. Autorização define o que você pode fazer. Vectora aplica ambas em cada tool call — não apenas no login."_
