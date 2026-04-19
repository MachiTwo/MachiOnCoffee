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

Segurança no Vectora é implementada em 3 camadas: aplicação (Guardian blocklist), isolamento (Trust Folder), e controle de acesso (RBAC). Dados são seus - Vectora é BYOK (Bring Your Own Key).

## 🔒 Pilares de Segurança

| Camada | Componente | Função | Docs |
|--------|-----------|--------|------|
| **Aplicação** | Guardian | Blocklist hard-coded para .env, secrets, binários | [→ Guardian](./guardian.md) |
| **Filesystem** | Trust Folder | Isolamento de path contra directory traversal | [→ Trust Folder](../concepts/trust-folder.md) |
| **Acesso** | RBAC | 5 roles (Owner→Guest) com 15 permissões | [→ RBAC](./rbac.md) |
| **Dados** | BYOK + Encryption | Chaves do usuário, criptografia AES-256-GCM | [→ BYOK & Privacy](./byok-privacy.md) |

## Compliance & Certificações

Suporta frameworks de conformidade:

- ✅ **GDPR** — Direito ao esquecimento, portabilidade de dados
- ✅ **HIPAA** — Criptografia, auditoria, acesso controlado
- ✅ **SOC 2 Type II** — Em progresso para 2026
- ✅ **PCI-DSS** — Se não indexar dados de cartão

## Segurança Shared Responsibility

| Responsabilidade | Vectora | Você |
|-----------------|---------|------|
| Guardian blocklist | ✅ | - |
| Trust Folder config | - | ✅ Configurar |
| API keys | - | ✅ Proteger |
| Senha | - | ✅ Usar 2FA |
| Rede (firewall) | - | ✅ (opcional) |

## Próximos Passos

1. **Entender**: Leia [Guardian](./guardian.md) para proteções hard-coded
2. **Configurar**: Defina [Trust Folder](../concepts/trust-folder.md) apropriadamente
3. **Gerenciar**: Configure [RBAC](./rbac.md) para seu time
4. **Dados**: Revise [BYOK & Privacy](./byok-privacy.md) para conformidade

---

> 🔐 Vulnerabilidade de segurança? [Reporte aqui](https://github.com/vectora/vectora/security)
