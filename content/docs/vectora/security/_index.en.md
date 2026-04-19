---
title: Security
slug: security
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - governance
  - mcp
  - security
  - vectora
---

{{< lang-toggle >}}

Security in Vectora is implemented in 3 layers: application (Guardian blocklist), isolation (Trust Folder), and access control (RBAC). Data is yours - Vectora is BYOK (Bring Your Own Key).

## Security Pillars

| Layer           | Component         | Function                                         | Docs                                          |
| --------------- | ----------------- | ------------------------------------------------ | --------------------------------------------- |
| **Application** | Guardian          | Hard-coded blocklist for .env, secrets, binaries | [→ Guardian](./guardian.md)                   |
| **Filesystem**  | Trust Folder      | Path isolation against directory traversal       | [→ Trust Folder](../concepts/trust-folder.md) |
| **Access**      | RBAC              | 5 roles (Owner→Guest) with 15 permissions        | [→ RBAC](./rbac.md)                           |
| **Data**        | BYOK + Encryption | User keys, AES-256-GCM encryption                | [→ BYOK & Privacy](./byok-privacy.md)         |

## Compliance & Certifications

Supports compliance frameworks:

- **GDPR** — Right to be forgotten, data portability
- **HIPAA** — Encryption, audit, controlled access
- **SOC 2 Type II** — In progress for 2026
- **PCI-DSS** — If credit card data is not indexed

## Shared Responsibility Security

| Responsibility      | Vectora | You        |
| ------------------- | ------- | ---------- |
| Guardian blocklist  |         | -          |
| Trust Folder config | -       | Configure  |
| API keys            | -       | Protect    |
| Password            | -       | Use 2FA    |
| Network (firewall)  | -       | (optional) |

## Next Steps

1. **Understand**: Read [Guardian](./guardian.md) for hard-coded protections
2. **Configure**: Define [Trust Folder](../concepts/trust-folder.md) appropriately
3. **Manage**: Configure [RBAC](./rbac.md) for your team
4. **Data**: Review [BYOK & Privacy](./byok-privacy.md) for compliance

---

> Security vulnerability? [Report here](https://github.com/vectora/vectora/security)
