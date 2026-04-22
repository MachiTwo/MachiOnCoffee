---
title: Security FAQ
slug: security
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - byok
  - concepts
  - config
  - embeddings
  - faq
  - guardian
  - mongodb-atlas
  - privacy
  - rbac
  - reranker
  - security
  - sso
  - vector-search
  - vectora
  - voyage
---

{{< lang-toggle >}}
{{< section-toggle >}}

Perguntas frequentes sobre segurança, proteção de dados, criptografia, compliance e boas práticas.

## Dados & Privacidade

**P: Meus dados são seguros com Vectora?**
R: Sim. BYOK (suas chaves), criptografia AES-256-GCM, TLS 1.3, Guardian blocklist, RBAC, audit logging.

**P: Vectora vê meu código?**
R: Não. Código indexado fica em seu MongoDB Atlas. Embeddings passam apenas por APIs que você controla (Voyage). Vectora nunca acessa o código.

**P: Como vocês usam meus dados?**
R: Não usamos. Dados são isolados por namespace e usuário. Sem analytics, sem treinamento de modelos.

**P: Como funciona bloqueio de .env?**
R: Guardian bloqueia arquivos por padrão ANTES de ler:

- `.env*` (ambiente)
- `*secret*`, `*credential*` (secrets)
- `*.key`, `*.pem`, `*.pfx` (chaves)
- `package-lock.json`, `Gemfile.lock` (locks)
  Guardian é compilado no runtime, não pode ser bypassado.

**P: Como deleto dados sensíveis?**
R: Delete o arquivo, reindex: `vectora index --incremental`. Chunks são removidos imediatamente de búscas e backups.

## Acesso & Autenticação

**P: Posso usar SSO/LDAP?**
R: Sim, plano Team+. Suporta: Azure AD, Okta, Google Workspace, custom OIDC.

**P: Como resetar senha?**
R: `vectora user reset-password --email user@company.com`. Link por email, válido por 1h.

**P: É seguro usar token em CI/CD?**
R: Sim. Tokens são JWT, expiráveis (30 dias por default), com scopes granulares (read-only, search-only, etc).

**P: Há 2FA?**
R: Sim, habilitado por default. Suporta TOTP (Authy, Google Authenticator, Microsoft Authenticator).

**P: Como revogar acesso?**
R: Admin faz `vectora user revoke --email user@company.com --token-id token_123`. Imediato.

## Compliance & Certificações

**P: Vocês são GDPR compliant?**
R: Sim. Suportamos: direito ao esquecimento, portabilidade, export.
`vectora export --namespace seu-ns --format gdpr`

**P: Vocês têm SOC 2?**
R: Em progresso para 2026. Atualmente suportamos manual audits.

**P: É HIPAA compliant?**
R: Sim para dados (AES-256, TLS, audit). Requer contrato BAA (disponível no plano Team).

**P: Posso usar em governo/defesa?**
R: Sim. Plano Enterprise com: on-premise, air-gapped, custom SLA.

## Auditoria & Logs

**P: Como auditar acessos?**
R: `vectora audit --since 7d`

Exemplo de log:

```json
{
  "timestamp": "2026-04-19T10:30:00Z",
  "action": "search",
  "user": "bruno@empresa.com",
  "query": "autenticação",
  "namespace": "seu-projeto",
  "result": "success",
  "ip": "192.168.1.1"
}
```

**P: Por quanto tempo logs são retidos?**
R: Free: 30 dias. Pro: 90 dias. Team: 180 dias. Enterprise: customizado.

**P: Os logs são imutáveis?**
R: Sim. Armazenados em append-only log com hash chain (não pode alterar).

**P: Posso auditar atividade de um usuário?**
R: Sim. `vectora user activity --email user@company.com --since 7d`.

## Criptografia & Chaves

**P: Há criptografia?**
R: Sim, dupla camada:

- **At Rest**: AES-256-GCM (FIPS 140-2 compliant)
- **In Transit**: TLS 1.3 (obrigatório)

**P: Quem tem a chave?**
R: Você. BYOK significa suas chaves são:

- Geradas por você em Google AI Studio / Voyage AI
- Armazenadas localmente em `~/.vectora/config`
- Usadas apenas para suas chamadas de API
- Nunca salvas em servidores da Vectora

**P: Há rotação de chaves?**
R: Sim. Você controla: `vectora config rotate-key GEMINI_API_KEY`. Novo key é usado, antigo é descartado.

## Boas Práticas

**P: Há rate limiting?**
R: Sim.

- Free: 60 req/min (API)
- Pro: 2000 req/min
- Team: Custom
- Brute-force protection: 5 falhas = 15min block

**P: Posso usar em produção?**
R: Sim.

- Free: Zero SLA
- Pro: 99.9% SLA (8.7h downtime/year)
- Team: 99.99% SLA (52min downtime/year)
- Enterprise: Custom SLA até 99.999%

**P: Como protestar contra ataque de força bruta?**
R: Automático. Após 5 falhas de senha, IP é bloqueado por 15min.

**P: Há teste de segurança?**
R: Sim.

- Penetration testing: Anual (incluído em SOC 2)
- Code scanning: Automatizado em cada merge
- Dependency scanning: OWASP, npm audit
- Secret scanning: GitHub secret scanning ativo

**P: Como reporto vulnerabilidade?**
R: [GitHub Security Advisory](https://github.com/Kaffyn/Vectora/security)
Resposta em < 24h, coordinated disclosure.

---

> Mais dúvidas? [GitHub Security](https://github.com/Kaffyn/Vectora/security) ou [Email](mailto:security@vectora.app)

## External Linking

| Concept               | Resource                                | Link                                                                                                       |
| --------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **MongoDB Atlas**     | Atlas Vector Search Documentation       | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **Voyage Embeddings** | Voyage Embeddings Documentation         | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)                             |
| **Voyage Reranker**   | Voyage Reranker API                     | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)                                 |
| **RBAC**              | NIST Role-Based Access Control Standard | [csrc.nist.gov/projects/rbac](https://csrc.nist.gov/projects/rbac)                                         |
| **JWT**               | RFC 7519: JSON Web Token Standard       | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)                     |
| **OpenID Connect**    | OIDC Core 1.0 Specification             | [openid.net/specs/openid-connect-core-1_0.html](https://openid.net/specs/openid-connect-core-1_0.html)     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
