---
title: RBAC
slug: rbac
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - governance
  - mcp
  - rbac
  - security
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}
**RBAC** (Role-Based Access Control) é o sistema de permissões granulares do Vectora. Ele utiliza 5 roles hierárquicos e 15 permissões específicas para gerenciar o acesso em nível de usuário e namespace.

> [!IMPORTANT] RBAC é "allow by role". Um usuário só pode fazer o que sua role permite. Não há exceções por usuário.

## Arquitetura

```text
User
  ↓
Role (Owner|Admin|Editor|Viewer|Guest)
  ↓
15 Permissions
  ├─ search
  ├─ index
  ├─ delete
  ├─ configure
  ├─ manage_users
  └─ ... (12 mais)
  ↓
Resource (Namespace|File|Config)
  ↓
Action (read|write|delete)
  ↓
Grant/Deny Decision
```

## 5 Roles Hierárquicos

O Vectora define cinco níveis de acesso, organizados de forma que cada nível superior herda todas as capacidades dos níveis abaixo dele.

## 1. Owner (Topo)

Controle total.

```yaml
role: owner
permissions:
  - search
  - index
  - delete
  - configure
  - manage_users
  - manage_roles
  - audit_logs
  - billing
  - api_tokens
  - webhooks
  - sso_config
  - backup_restore
  - advanced_analytics
  - custom_integrations
  - support_priority

can_perform:
  - Criar/deletar namespaces
  - Gerenciar todos os usuários
  - Alterar qualquer configuração
  - Ver all logs
  - Manage billing

examples:
  - CTO, Tech Lead
  - Empresa inteira (free tier)
```

Cada nível de acesso é otimizado para uma responsabilidade específica dentro da organização, desde o controle total até a visualização restrita.

## 2. Admin

Gerenciamento, sem mudanças estruturais.

```yaml
role: admin
permissions:
  - search
  - index
  - delete
  - configure
  - manage_users # SEM manage_roles
  - audit_logs
  - api_tokens
  - webhooks
  - advanced_analytics

cannot_perform:
  - Deletar namespace
  - Mudar roles de usuários
  - Ver billing
  - Sso/ldap config
```

A separação entre administração e edição permite que a equipe técnica foque na produção de dados sem riscos de alterações estruturais acidentais.

## 3. Editor

Trabalho técnico: busca e indexação.

```yaml
role: editor
permissions:
  - search
  - index
  - delete
  - api_tokens

cannot_perform:
  - Alterar configuração
  - Gerenciar usuários
  - Ver logs
  - Criar webhooks
```

Os papéis de visualização são ideais para consumidores de dados que precisam acessar o conhecimento sem modificar o índice semântico.

## 4. Viewer

Somente leitura.

```yaml
role: viewer
permissions:
  - search
  - api_tokens # Para leitura

cannot_perform:
  - index
  - delete
  - configure
  - manage_anything
```

Para acessos temporários ou limitados, o Vectora oferece um perfil de convidado com restrições automáticas de volume de busca.

## 5. Guest

Read-only com rate limiting.

```yaml
role: guest
permissions:
  - search (limited) # 100 req/day

cannot_perform:
  - index
  - delete
  - api_tokens
  - anything else
```

## 15 Permissões Granulares

| Permissão             | Descrição                | Roles                               |
| --------------------- | ------------------------ | ----------------------------------- |
| `search`              | Buscar contexto          | Owner, Admin, Editor, Viewer, Guest |
| `index`               | Indexar arquivos         | Owner, Admin, Editor                |
| `delete`              | Deletar chunks/namespace | Owner, Admin, Editor                |
| `configure`           | Alterar config           | Owner, Admin                        |
| `manage_users`        | Criar/deletar users      | Owner, Admin                        |
| `manage_roles`        | Alterar roles de users   | Owner                               |
| `audit_logs`          | Ver logs completos       | Owner, Admin                        |
| `api_tokens`          | Criar/revogar tokens     | Owner, Admin, Editor, Viewer        |
| `webhooks`            | Criar/gerenciar webhooks | Owner, Admin                        |
| `sso_config`          | Configurar SSO/LDAP      | Owner                               |
| `backup_restore`      | Backup e restore         | Owner                               |
| `advanced_analytics`  | Dashboard avançado       | Owner, Admin                        |
| `custom_integrations` | Custom endpoints         | Owner                               |
| `support_priority`    | Suporte prioritário      | Owner                               |
| `billing`             | Ver/alterar billing      | Owner                               |

## Configuração

A implementação do RBAC pode ser realizada de forma dinâmica via linha de comando ou através de definições estáticas em arquivos de configuração.

## Criar Usuário com Role

```bash
# Via CLI
vectora user create \
  --email dev@company.com \
  --name "João Developer" \
  --role editor \
  --namespace seu-namespace

# Via API
POST /api/users
{
  "email": "dev@company.com",
  "role": "editor",
  "namespaces": ["seu-namespace"],
  "expires_at": "2027-04-19"
}
```

## Atualizar Role

```bash
# Promover
vectora user update \
  --email dev@company.com \
  --role admin

# Revogar específica permissão (advanced)
vectora user revoke-permission \
  --email dev@company.com \
  --permission manage_users
```

## YAML Config

```yaml
# vectora.config.yaml
rbac:
  enabled: true
  roles:
    owner:
      max_users: 1
      can_create_namespaces: true
      can_delete_namespaces: true

    admin:
      max_users: 5
      can_create_namespaces: false

    editor:
      max_users: unlimited
      can_index: true

    viewer:
      max_users: unlimited
      can_search: true

    guest:
      max_users: unlimited
      rate_limit: 100/day
```

## User Management

O gerenciamento de usuários abrange desde o provisionamento inicial até a auditoria de atividades e a revogação de acessos quando necessário.

## Lifecycle

```text
Criar User (Owner)
    ↓
User recebe convite via email
    ↓
User clica link, set password
    ↓
User faz login
    ↓
User pode usar Vectora conforme role
    ↓
Admin pode revocar acesso
    ↓
User deletion (logs preservados)
```

## Criar Usuário

```bash
vectora user create \
  --email alice@company.com \
  --name "Alice Engineer" \
  --role editor \
  --namespace kaffyn-vectora-prod \
  --send-invite true

# Saída:
# User created: alice@company.com
# Role: editor
# Invitation sent to alice@company.com
# Invite expires in: 7 days
```

## Listar Usuários

```bash
vectora user list [--namespace <ns>]

# Output:
# Email | Role | Joined | Last Active
# ─────────────────────────┼───────────┼────────────┼─────────────
# owner@company.com | owner | 2026-01-10 | 5 min ago
# admin@company.com | admin | 2026-02-15 | 2 hours ago
# dev@company.com | editor | 2026-03-20 | offline
```

## Revogar Acesso

```bash
vectora user delete --email dev@company.com

# Saída:
# User revoked: dev@company.com
# - Todos os tokens revogados
# - Acesso imediato removido
# - Audit log criado
```

## Namespace-Level Permissions

Granularidade por namespace:

```yaml
# User pode ter roles diferentes por namespace
users:
  - email: dev@company.com
    namespaces:
      kaffyn-vectora-prod:
        role: viewer # Só lê em prod
      kaffyn-vectora-staging:
        role: editor # Edita em staging
      kaffyn-vectora-dev:
        role: owner # Controla em dev
```

Setup:

```bash
vectora user assign-namespace \
  --email dev@company.com \
  --namespace kaffyn-vectora-prod \
  --role viewer

vectora user assign-namespace \
  --email dev@company.com \
  --namespace kaffyn-vectora-staging \
  --role editor
```

## Integration with Guardian & Harness

O RBAC opera em conjunto com o Guardian e o Harness para formar uma defesa em profundidade, validando permissões antes de qualquer inspeção de segurança.

## Flow Completo

```text
User Request
    ↓
┌──────────────────────────┐
│ RBAC Check │ Role permite?
│ - User role: editor? │
│ - Permission: search? │
└────────┬─────────────────┘
         │ SIM
         ↓
┌──────────────────────────┐
│ Guardian Check │ Trust folder + patterns
│ - Trust folder violation?│
│ - Pattern match? │
└────────┬─────────────────┘
         │ ALLOW
         ↓
┌──────────────────────────┐
│ Harness Validation │ Pre/post execution
│ - Metrics captured │
│ - Audit logged │
└────────┬─────────────────┘
         │ SUCCESS
         ↓
┌──────────────────────────┐
│ Response to User │
│ - Chunks returned │
│ - Metrics included │
└──────────────────────────┘

Se qualquer check falha → Deny + Log
```

## Audit & Compliance

Todas as alterações de permissões e atribuições de usuários são registradas para garantir a conformidade com auditorias de segurança e requisitos regulatórios.

## RBAC Audit Trail

```bash
vectora audit --filter "rbac" --since 7d

# Output:
# Timestamp | Action | User | Details
# ─────────────────────┼─────────────────────┼──────────────────────┼─────────────
# 2026-04-19 10:30:00 | user_created | owner@company.com | role=editor
# 2026-04-19 11:15:00 | role_changed | owner@company.com | dev@co → admin
# 2026-04-19 14:22:00 | access_denied | dev@company.com | permission=configure
# 2026-04-19 16:45:00 | user_deleted | admin@company.com | alice@company.com
```

## Compliance Reports

```bash
vectora report rbac --format pdf --output rbac-report.pdf

# Inclui:
# - Todos os usuários e roles
# - Mudanças de role (últimos 90 dias)
# - Access denied attempts
# - Usuários inativos (> 30 dias)
```

## Best Practices

## 1. Principle of Least Privilege

Sempre comece com role mais restritivo:

```bash
# Crie como viewer
vectora user create ... --role viewer

# Depois promova conforme necessário
vectora user update ... --role editor
```

## 2. Separate Namespaces per Env

```yaml
prod:
  owner: 1 person
  roles: owner, viewer

staging:
  owner: 2 people
  roles: owner, editor

dev:
  owner: team
  roles: owner, admin, editor
```

## 3. Review Regularly

```bash
# Mensal review
vectora audit --since 30d --filter "user_created|role_changed|user_deleted"

# Desabilitar usuários inativos
vectora user list --inactive 60d
```

## 4. No Shared Accounts

Cada pessoa = 1 conta. Nunca compartilhe:

```bash
# Ruim
export VECTORA_TOKEN="shared-token-for-team"

# Bem
# Cada dev tem seu próprio:
export VECTORA_TOKEN="sk-proj-$(whoami)-..."
```

## Troubleshooting

## "Permission denied: search"

User role não inclui `search`:

```bash
vectora user list-permissions --email dev@company.com
# Output: [index, delete]

# Solução: Promover role
vectora user update --email dev@company.com --role editor
```

## "Unauthorized in namespace"

User não tem acesso ao namespace específico:

```bash
vectora user list-namespaces --email dev@company.com
# Output: [kaffyn-staging, kaffyn-dev]
# Missing: kaffyn-prod

# Solução: Assign namespace
vectora user assign-namespace --email dev@company.com --namespace kaffyn-prod --role viewer
```

## Migration from No-RBAC

Se estava usando Vectora sem RBAC:

```bash
# 1. Enable RBAC
vectora config set rbac.enabled true

# 2. Create users based on existing tokens
vectora user create --email dev@company.com --role editor

# 3. Migrate tokens
vectora migrate-tokens --from v1 --to v2

# 4. Revoke old tokens
vectora token revoke-all-old
```

---

> **Próximo**: [BYOK & Privacy](./byok-privacy.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
