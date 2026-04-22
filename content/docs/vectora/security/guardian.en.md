---
title: Guardian
slug: guardian
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - byok
  - concepts
  - config
  - errors
  - governance
  - guardian
  - mcp
  - privacy
  - rbac
  - reference
  - security
  - system
  - tools
  - troubleshooting
  - trust-folder
  - vectora
  - yaml
---

{{< lang-toggle >}}
{{< section-toggle >}}
The **Guardian** is Vectora's governance engine, compiled directly into the Go binary. It acts as an application firewall, inspecting every command and path before execution.

> [!IMPORTANT] Guardian is not a firewall - it's a gatekeeper. A Guardian violation is BLOCKED before reaching the filesystem, with no exceptions.

## Architecture

```text
Request to read file
    ↓
┌─────────────────┐
│ Trust Folder │ Is it within the perimeter?
│ Check │
└────────┬────────┘
         │ YES
         ↓
┌─────────────────────┐
│ Guardian Rules │ Matches allow/deny pattern?
│ Pattern Matching │
└────────┬────────────┘
         │ ALLOW (or NO MATCH)
         ↓
┌──────────────────┐
│ RBAC Check │ Does user have permission?
│ │
└────────┬─────────┘
         │ YES
         ↓
┌──────────────────────┐
│ File Access │ File can be read
│ Permitted │
└──────────────────────┘

If any check FAILS → Request is BLOCKED + Audit Log
```

## Configuration

The Guardian configuration is divided into logical layers, allowing for a balance between strict restriction and operational flexibility.

## Trust Folder (Layer 1)

Defines the security perimeter:

```yaml
# vectora.config.yaml
project:
  trust_folder: "./src"
  # Only files in ./src/* can be accessed
```

Any attempt to read outside this directory is blocked:

```text
Request: ../../../.env
Trust Folder: ./src
Result: BLOCKED (outside perimeter)
```

## Guardian Rules (Layer 2)

Regex patterns for allow/deny:

```yaml
# vectora.config.yaml
guardian:
  rules:
    # DENY has priority
    - name: "block_env"
      pattern: "\.env.*" # .env, .env.local, .env.production
      action: "deny"

    - name: "block_secrets"
      pattern: "secrets/.*"
      action: "deny"

    - name: "block_credentials"
      pattern: ".*credentials.*" # Any file with "credentials"
      action: "deny"

    # ALLOW (optional, more specific)
    - name: "allow_src_docs"
      pattern: "^(src|docs)/.*"
      action: "allow"
```

Order matters: rules are evaluated top→bottom, first match wins.

## RBAC (Layer 3)

Additionally, Vectora respects user permissions:

```yaml
# Defined in RBAC config
roles:
  owner:
    permissions:
      - search
      - index
      - configure
      - manage_users
  editor:
    permissions:
      - search
      - index
  viewer:
    permissions:
      - search
```

## Pre-Configured Patterns

Guardian comes with pre-set security patterns:

```yaml
# Defaults (always active)
defaults:
  block_patterns:
    - "\.env.*"
    - ".*\.key$"
    - ".*\.pem$"
    - ".*secret.*"
    - "\.git/.*"
    - "\.ssh/.*"
    - "bin/.*"
    - "vendor/.*"
    - "\.git/.*"
```

To customize, override in config:

```yaml
guardian:
  override_defaults: true
  rules:
    - name: "my_rule"
      pattern: "custom.*"
      action: "deny"
```

## Audit Logging

Every access attempt (blocked or permitted) is logged:

```bash
VECTORA_AUDIT_LOG=true vectora search "query"
```

Log output:

```json
{
  "timestamp": "2026-04-19T10:30:00Z",
  "event": "guardian_check",
  "action": "file_access",
  "requested_file": ".env",
  "trust_folder": "/home/user/project/src",
  "status": "BLOCKED",
  "reason": "matches_deny_pattern",
  "pattern": ".env.*",
  "user": "dev@company.com",
  "user_role": "editor",
  "ip": "192.168.1.100"
}
```

Inspect logs:

```bash
# Last 24h
vectora audit --action file_access --since 24h

# Blocked only
vectora audit --filter "BLOCKED"

# By pattern
vectora audit --filter "pattern:\.env"
```

## Use Cases

Below are practical examples of how to configure the Guardian for common security scenarios in development and production.

## Case 1: Protect .env

```yaml
guardian:
  rules:
    - name: "block_dotenv"
      pattern: "\.env.*"
      action: "deny"
```

Result: `.env`, `.env.local`, `.env.production` are all blocked.

## Case 2: Protect private data

```yaml
guardian:
  rules:
    - name: "block_private"
      pattern: "private/.*"
      action: "deny"

    - name: "block_test_data"
      pattern: "test_data/.*\.csv"
      action: "deny"
```

## Case 3: Specific allow-list

```yaml
project:
  trust_folder: "." # I trust everything

guardian:
  rules:
    # Explicitly allow only src/ and docs/
    - name: "allow_src_docs"
      pattern: "^(src|docs)/"
      action: "allow"

    # Everything else is blocked
    - name: "deny_everything_else"
      pattern: ".*"
      action: "deny"
```

## Known Violations

The Guardian is trained to identify and mitigate common attack vectors based on path and reference manipulation.

## Directory Traversal Attempts

```text
Attempt: ../../.env
Resolution: Normalized to /absolute/path/.env
Trust Folder: /absolute/path/src
Result: BLOCKED (outside perimeter)
```

## Symlink Attacks

```text
File: ./src/link-to-secret → ../../secret.key
Resolution: Resolved to /absolute/path/secret.key
Trust Folder: /absolute/path/src
Result: BLOCKED (symlink outside perimeter)
```

To allow specific symlinks:

```yaml
guardian:
  symlink_handling: "follow" # or "deny"
  symlink_whitelist:
    - "./src/allowed-link"
```

## Case Sensitivity (Windows)

Windows is case-insensitive, patterns are case-sensitive by default:

```yaml
guardian:
  case_sensitive: false # Match .ENV, .Env, .env
```

## Testing & Validation

Before applying rules in production, it is essential to validate Guardian's behavior using simulation and pattern testing tools.

## Dry-Run Mode

Test rules without blocking:

```bash
vectora guardian validate --dry-run
```

Output:

```text
Guardian Validation Report
├─ Trust Folder: ./src
├─ Default Deny Patterns: 9
├─ Custom Rules: 3
└─ Test Cases:
   ├─ .env → BLOCKED (pattern: \.env.*)
   ├─ src/main.ts → ALLOWED
   └─ secrets/key.pem → BLOCKED (pattern: secrets/.*)
```

## Rule Testing

```bash
# Test specific pattern
vectora guardian test-pattern "\.env.*" ".env.local"
# Output: MATCH

vectora guardian test-pattern "\.env.*" "src/index.ts"
# Output: NO MATCH
```

## Monitoring & Alerts

Maintain visibility into your server's security status through detailed metrics and real-time alerts.

## Metrics

Guardian captures security metrics:

```bash
vectora metrics --filter guardian
```

Output:

```yaml
guardian_metrics:
  period: "24h"
  total_checks: 12543
  allowed: 12500
  blocked: 43

  blocked_by_reason:
    deny_pattern: 35
    outside_trust_folder: 8
    rbac_violation: 0

  top_blocked_patterns:
    - "\.env.*": 15
    - "\.key$": 12
    - "secret": 8
```

### Alerts

Configure alerts for violations:

```yaml
guardian:
  alerts:
    enabled: true
    notify_on_violations: true
    threshold_per_hour: 10 # Alert if > 10 blocks/h
    webhook: "https://your-slack.com/webhook"
```

## Best Practices

Follow these recommendations to ensure that the Guardian acts with maximum efficiency without hindering developer productivity.

## 1. Minimum Trust Folder

Don't trust `./` - be specific:

```yaml
# Unsafe
project:
  trust_folder: "."

# Safe
project:
  trust_folder: "./src"
```

### 2. Deny-by-Default

When possible, use "deny all, allow specific" pattern:

```yaml
guardian:
  rules:
    - name: "allow_src_docs"
      pattern: "^(src|docs)/"
      action: "allow"

    - name: "deny_everything"
      pattern: ".*"
      action: "deny"
```

### 3. Audit Regularly

```bash
# Weekly review
vectora audit --since 7d --filter "BLOCKED" | wc -l
```

### 4. Avoid Exceptions

Don't create "exception rules" for .env - use default values:

```yaml
# Bad - exception
guardian:
  rules:
    - name: "allow_local_env"
      pattern: "\.env\.local" # Exception!
      action: "allow"

# Better - use variables
guardian:
  rules:
    - name: "block_env"
      pattern: "\.env"
      action: "deny"

# Use .env via environment variables instead
export GEMINI_API_KEY="..."
```

## Troubleshooting

If you encounter access problems or unexpected messages, use these procedures to diagnose and resolve conflicts with the Guardian.

## Legitimate file blocked

```text
Error: ./src/config.secrets.ts is blocked by pattern
```

**Diagnostic**:

```bash
vectora guardian explain "./src/config.secrets.ts"
# Output: Matches deny_pattern ".*secret.*"
```

**Solution 1**: Rename file

```bash
mv src/config.secrets.ts src/config.secure.ts
```

**Solution 2**: Adjust pattern (less recommended)

```yaml
guardian:
  rules:
    - name: "block_secrets"
      pattern: "secret_keys/.*" # More specific
      action: "deny"
```

### "Guardian disabled" messages

If Guardian is disabled (dev mode):

```bash
# Check status
vectora config get guardian.enabled

# Re-enable
vectora config set guardian.enabled true
```

## Compliance & Regulations

Guardian helps comply with:

- **GDPR**: Protected personal data
- **HIPAA**: Medical records not indexed
- **PCI-DSS**: Credit card numbers blocked
- **SOC 2**: Complete audit trail

Configure specific rules:

```yaml
# HIPAA
guardian:
  rules:
    - pattern: "patient_data/.*"
      action: "deny"
    - pattern: ".*\.phi\..*" # Protected Health Info
      action: "deny"
```

## Next Steps

1. **Understand**: Read [Guardian](./guardian.md) for hard-coded protections
2. **Configure**: Define [Trust Folder](../concepts/trust-folder.md) appropriately
3. **Manage**: Configure [RBAC](./rbac.md) for your team
4. **Data**: Review [BYOK & Privacy](./byok-privacy.md) for compliance

---

> **Next**: [RBAC System](./rbac.md)

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
