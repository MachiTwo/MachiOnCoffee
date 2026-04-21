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
**RBAC** (Role-Based Access Control) is the granular permission system of Vectora. It uses 5 hierarchical roles and 15 specific permissions to manage access at both the user and namespace levels.

> [!IMPORTANT]
> RBAC is "allow by role". A user can only do what their role allows. There are no per-user exceptions.

## Architecture

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
  └─ ... (12 more)
  ↓
Resource (Namespace|File|Config)
  ↓
Action (read|write|delete)
  ↓
Grant/Deny Decision
```

## 5 Hierarchical Roles

Vectora defines five levels of access, organized so that each higher level inherits all the capabilities of the levels below it.

## 1. Owner (Top)

Full control.

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
  - Create/delete namespaces
  - Manage all users
  - Change any configuration
  - View all logs
  - Manage billing

examples:
  - CTO, Tech Lead
  - Entire company (free tier)
```

Each access level is optimized for a specific responsibility within the organization, ranging from full control to restricted viewing.

## 2. Admin

Management, without structural changes.

```yaml
role: admin
permissions:
  - search
  - index
  - delete
  - configure
  - manage_users # WITHOUT manage_roles
  - audit_logs
  - api_tokens
  - webhooks
  - advanced_analytics

cannot_perform:
  - Delete namespace
  - Change user roles
  - View billing
  - Sso/ldap config
```

The separation between administration and editing allows the technical team to focus on data production without risks of accidental structural changes.

## 3. Editor

Technical work: search and indexing.

```yaml
role: editor
permissions:
  - search
  - index
  - delete
  - api_tokens

cannot_perform:
  - Change configuration
  - Manage users
  - View logs
  - Create webhooks
```

Viewing roles are ideal for data consumers who need to access knowledge without modifying the semantic index.

## 4. Viewer

Read-only.

```yaml
role: viewer
permissions:
  - search
  - api_tokens # For reading

cannot_perform:
  - index
  - delete
  - configure
  - manage_anything
```

For temporary or limited access, Vectora offers a guest profile with automatic search volume restrictions.

## 5. Guest

Read-only with rate limiting.

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

## 15 Granular Permissions

| Permission            | Description             | Roles                               |
| --------------------- | ----------------------- | ----------------------------------- |
| `search`              | Search context          | Owner, Admin, Editor, Viewer, Guest |
| `index`               | Index files             | Owner, Admin, Editor                |
| `delete`              | Delete chunks/namespace | Owner, Admin, Editor                |
| `configure`           | Change config           | Owner, Admin                        |
| `manage_users`        | Create/delete users     | Owner, Admin                        |
| `manage_roles`        | Change user roles       | Owner                               |
| `audit_logs`          | View complete logs      | Owner, Admin                        |
| `api_tokens`          | Create/revoke tokens    | Owner, Admin, Editor, Viewer        |
| `webhooks`            | Create/manage webhooks  | Owner, Admin                        |
| `sso_config`          | Configure SSO/LDAP      | Owner                               |
| `backup_restore`      | Backup and restore      | Owner                               |
| `advanced_analytics`  | Advanced dashboard      | Owner, Admin                        |
| `custom_integrations` | Custom endpoints        | Owner                               |
| `support_priority`    | Priority support        | Owner                               |
| `billing`             | View/change billing     | Owner                               |

## Configuration

RBAC implementation can be performed dynamically via the command line or through static definitions in configuration files.

## Create User with Role

```bash
# Via CLI
vectora user create \
  --email dev@company.com \
  --name "João Developer" \
  --role editor \
  --namespace your-namespace

# Via API
POST /api/users
{
  "email": "dev@company.com",
  "role": "editor",
  "namespaces": ["your-namespace"],
  "expires_at": "2027-04-19"
}
```

## Update Role

```bash
# Promote
vectora user update \
  --email dev@company.com \
  --role admin

# Revoke specific permission (advanced)
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

User management covers everything from initial provisioning to activity auditing and revoking access when necessary.

## Lifecycle

```text
Create User (Owner)
    ↓
User receives invitation via email
    ↓
User clicks link, sets password
    ↓
User logs in
    ↓
User can use Vectora according to role
    ↓
Admin can revoke access
    ↓
User deletion (logs preserved)
```

## Create User

```bash
vectora user create \
  --email alice@company.com \
  --name "Alice Engineer" \
  --role editor \
  --namespace kaffyn-vectora-prod \
  --send-invite true

# Output:
# User created: alice@company.com
# Role: editor
# Invitation sent to alice@company.com
# Invite expires in: 7 days
```

## List Users

```bash
vectora user list [--namespace <ns>]

# Output:
# Email | Role | Joined | Last Active
# ─────────────────────────┼───────────┼────────────┼─────────────
# owner@company.com | owner | 2026-01-10 | 5 min ago
# admin@company.com | admin | 2026-02-15 | 2 hours ago
# dev@company.com | editor | 2026-03-20 | offline
```

## Revoke Access

```bash
vectora user delete --email dev@company.com

# Output:
# User revoked: dev@company.com
# - All tokens revoked
# - Immediate access removed
# - Audit log created
```

## Namespace-Level Permissions

Granularity per namespace:

```yaml
# User can have different roles per namespace
users:
  - email: dev@company.com
    namespaces:
      kaffyn-vectora-prod:
        role: viewer # Only reads in prod
      kaffyn-vectora-staging:
        role: editor # Edits in staging
      kaffyn-vectora-dev:
        role: owner # Controls in dev
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

RBAC operates in conjunction with the Guardian and Harness to form a defense-in-depth, validating permissions before any security inspection.

## Full Flow

```text
User Request
    ↓
┌──────────────────────────┐
│ RBAC Check │ Role allows?
│ - User role: editor? │
│ - Permission: search? │
└────────┬─────────────────┘
         │ YES
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

If any check fails → Deny + Log
```

## Audit & Compliance

All permission changes and user assignments are recorded to ensure compliance with security audits and regulatory requirements.

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

# Includes:
# - All users and roles
# - Role changes (last 90 days)
# - Access denied attempts
# - Inactive users (> 30 days)
```

## Best Practices

## 1. Principle of Least Privilege

Always start with the most restrictive role:

```bash
# Create as viewer
vectora user create ... --role viewer

# Then promote as needed
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
# Monthly review
vectora audit --since 30d --filter "user_created|role_changed|user_deleted"

# Disable inactive users
vectora user list --inactive 60d
```

## 4. No Shared Accounts

Each person = 1 account. Never share:

```bash
# Bad
export VECTORA_TOKEN="shared-token-for-team"

# Good
# Each dev has their own:
export VECTORA_TOKEN="sk-proj-$(whoami)-..."
```

## Troubleshooting

## "Permission denied: search"

User role does not include `search`:

```bash
vectora user list-permissions --email dev@company.com
# Output: [index, delete]

# Solution: Promote role
vectora user update --email dev@company.com --role editor
```

## "Unauthorized in namespace"

User does not have access to the specific namespace:

```bash
vectora user list-namespaces --email dev@company.com
# Output: [kaffyn-staging, kaffyn-dev]
# Missing: kaffyn-prod

# Solution: Assign namespace
vectora user assign-namespace --email dev@company.com --namespace kaffyn-prod --role viewer
```

## Migration from No-RBAC

If you were using Vectora without RBAC:

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

## Next Steps

1. **Understand**: Read [Guardian](./guardian.md) for hard-coded protections
2. **Configure**: Define [Trust Folder](../concepts/trust-folder.md) appropriately
3. **Manage**: Configure [RBAC](./rbac.md) for your team
4. **Data**: Review [BYOK & Privacy](./byok-privacy.md) for compliance

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
