---
title: Trust Folder
slug: trust-folder
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - concepts
  - config
  - errors
  - folder
  - guardian
  - integration
  - mcp
  - reference
  - security
  - system
  - troubleshooting
  - trust
  - trust-folder
  - vector-search
  - vectora
  - yaml
---

{{< lang-toggle >}}
The Trust Folder is the **security perimeter** that limits which files Vectora can index, read, and process. It acts as a "path sandbox" against reading sensitive files.

> [!IMPORTANT] The Trust Folder is not optional. Without it, Vectora could index .env files, private keys, and user data. With the Trust Folder, only files within the perimeter are accessible.

## The Problem

Without a Trust Folder:

- Vectora indexes everything on the disk: `/etc/passwd`, `~/.ssh/id_rsa`, `.env`
- It is vulnerable to directory traversal: `../../sensitive/file.txt`
- There is no audit of who accessed which file

With a Trust Folder:

- Indexing is confined to `./src`, `./docs` (configurable)
- Directory traversal is blocked: `../../../.env` is rejected
- Audit logs track all reading operations

## Configuration

The Trust Folder is configured in `vectora.config.yaml` and can use relative or absolute paths, with support for environment variable expansion.

## Default

```yaml
# vectora.config.yaml
project:
  trust_folder: "." # Default: project root
```

This means: "I trust everything within this directory and its subdirectories."

## Explicit (Recommended)

```yaml
project:
  trust_folder: "./src" # ONLY ./src

# Or multiple folders
project:
  trust_folders:
    - "./src"
    - "./docs"
    - "./packages"
    # NOT included: ./node_modules, ./build, ./.env
```

## Absolute vs. Relative Paths

```yaml
# Relative (recommended)
trust_folder: "./src"
# Resolved to: /current/working/dir/src

# Absolute (allowed)
trust_folder: "/home/user/myproject/src"

# Variable expansion
trust_folder: "${PROJECT_ROOT}/src"
# Resolved via environment variables
```

## Path Resolution

Vectora resolves paths securely, normalizing relative paths to absolute ones and blocking attempts to step out of the Trust Folder.

## Allow List

When indexing:

```text
Trust Folder: ./src
File Requested: ./src/auth/login.ts

Resolution:
1. ./src/auth/login.ts → /absolute/path/to/src/auth/login.ts
2. Is /absolute/path/to/src/auth/login.ts inside /absolute/path/to/src?
3. YES → Allowed
```

## Block List (Directory Traversal)

```text
Trust Folder: ./src
File Requested: ../../../.env

Resolution:
1. Normalize: ../../../.env → /absolute/path/.env
2. Is /absolute/path/.env inside /absolute/path/to/src?
3. NO → BLOCKED
text
Trust Folder: ./src
File Requested: ./src/../../.env

Resolution:
1. Normalize: ./src/../../.env → /absolute/path/.env
2. Is /absolute/path/.env inside /absolute/path/to/src?
3. NO → BLOCKED
```

## Use Cases

Below we present three real-world configuration patterns: monorepo with package isolation, documentation site with private sections, and a complete sandbox for maximum security.

## Case 1: Monorepo with Multiple Packages

```text
project/
├── packages/
│ ├── backend/
│ │ ├── src/
│ │ └── docs/
│ └── frontend/
│ ├── src/
│ └── docs/
├── shared/
└── .env (SENSITIVE)
```

Configuration:

```yaml
# For backend
project:
  trust_folders:
    - "./packages/backend/src"
    - "./packages/backend/docs"
    - "./shared"

# For frontend
project:
  trust_folders:
    - "./packages/frontend/src"
    - "./packages/frontend/docs"
    - "./shared"
```

Result:

- Backend cannot read frontend code
- Frontend cannot read backend code
- Both can access shared
- `.env` is blocked for BOTH

## Case 2: Documentation + Source Code

```text
docs-website/
├── content/ ← Public
│ ├── getting-started/
│ └── api-reference/
├── src/ ← Site code (config, templates)
├── private/ ← Private drafts (SENSITIVE)
└── .env
```

Configuration:

```yaml
project:
  trust_folders:
    - "./content"
    - "./src"
  # private/ and .env are inaccessible
```

## Case 3: Complete Sandbox

For maximum security (e.g., CI/CD):

```yaml
project:
  trust_folder: "./sanitized"
# Before running, copy ONLY what is allowed:
# mkdir sanitized
# cp -r src/ sanitized/
# cp -r docs/ sanitized/
# vectora init --trust-folder ./sanitized
```

## Guardian Integration

Guardian also validates paths:

```yaml
guardian:
  rules:
    - name: "block_env_files"
      pattern: "\.env.*"
      action: "block"

    - name: "block_secrets"
      pattern: "secrets/"
      action: "block"

    - name: "allow_only_src_docs"
      pattern: "^(src|docs)/.*"
      action: "allow"
```

**Order**: Trust Folder → Guardian → Indexing

- Trust Folder denies: file blocked immediately
- Trust Folder allows: Guardian validates pattern
- Both pass: file is indexed

## Auditing

## Logging

```bash
VECTORA_AUDIT_LOG=true
VECTORA_LOG_LEVEL=debug
```

Log output:

```json
{
  "timestamp": "2026-04-19T14:32:00Z",
  "event": "file_access_attempt",
  "path": "../../../.env",
  "normalized_path": "/home/user/.env",
  "trust_folder": "/home/user/project/src",
  "result": "DENIED",
  "reason": "outside_trust_folder"
}
```

## Inspection

```bash
vectora audit --since 24h --filter "DENIED"
# Shows all blocked attempts

vectora audit --filter "file_access" | jq '.[] | {path, result}'
```

## Security Scenarios (What Trust Folder Prevents)

Below we show 4 potential attacks and how the Trust Folder prevents each of them, demonstrating the importance of a secure configuration.

## Attack 1: Simple Path Traversal

**Without Trust Folder:**

```bash
# LLM asks (or user injects)
vectora search --file "../../.env"
# Result: .env is read VULNERABILITY
```

**With Trust Folder (`./src`):**

```bash
vectora search --file "../../.env"
# Resolution: /project/.env (outside of /project/src)
# Result: BLOCKED SAFE
```

## Attack 2: Symlink Escape

**Scenario:**

```text
project/src/link → ../../sensitive/secrets.yml
```

**Without resolution:**
Vectora sees `src/link` (looks safe) and indexes it.

**With resolution (default):**
Vectora resolves: `src/link` → `../../sensitive/secrets.yml` → `/project/sensitive/secrets.yml`
Detects: outside trust folder → BLOCKED

## Attack 3: Injection via LLM Context

**Scenario:**

```text
User: "My code imports from 'os.system'.
         Search in ../../../../etc/passwd"

LLM (without Trust Folder):
"I found this in /etc/passwd: root:x:0:0:..."

LLM (with Trust Folder):
"I cannot access /etc/passwd - outside the trust folder"
```

## Attack 4: CI/CD Exposure

**Without Trust Folder:**

```text
CI/CD runner executes: vectora index
Indices: /home/runner/secrets.json (with API keys!)
Vectora Cloud sync: secrets.json is sent
Result: Keys exposed
```

**With Trust Folder `./src`:**

```text
CI/CD runner executes: vectora index --trust-folder ./src
Indices: ONLY ./src/
Result: secrets.json ignored
```

## Testing & Verification

To validate that the Trust Folder is working correctly, use the commands below. A complete security audit ensures that no sensitive files are accessible.

## Verify Trust Folder is Active

```bash
# 1. Config
vectora config get trust_folder
# Output: ./src

# 2. List indexed files
vectora index --list-files | head -20
# Verify: do all start with ./src?

# 3. Path denied dry-run
vectora index --try-path "../.env" --dry-run
# Output: ERROR: outside_trust_folder
```

## Complete Security Audit

```bash
#!/bin/bash
# audit-trust-folder.sh

echo "=== Trust Folder Security Audit ==="

# 1. Check config
TRUST=$(vectora config get trust_folder)
echo "Trust Folder: $TRUST"

# 2. List all indexed files
INDEXED=$(vectora index --list-files)
OUTSIDE=$(echo "$INDEXED" | grep -v "^${TRUST}" | wc -l)

if [ "$OUTSIDE" -gt 0 ]; then
  echo " FAIL: $OUTSIDE files outside trust folder"
  exit 1
fi

# 3. Try to access sensitive files
SENSITIVE=(".env" ".secrets" "*.pem" "*.key")
for pattern in "${SENSITIVE[@]}"; do
  FOUND=$(vectora search --file "*/$pattern" 2>&1 | grep "outside_trust_folder" | wc -l)
  if [ "$FOUND" -eq 0 ]; then
    echo " WARNING: Pattern $pattern may be exposed"
  fi
done

echo " PASS: Trust Folder is properly configured"
```

## Troubleshooting

Common issues when using the Trust Folder and how to solve them, including solutions for symlinks and path resolution.

## Valid File Blocked

```text
Error: ./src/utils/helpers.ts is outside trust folder
```

**Diagnosis**:

```bash
# Check paths
pwd # Your CWD
cat vectora.config.yaml | grep trust_folder

# Verify with --dry-run
vectora index --dry-run
```

**Solution**: Verify if `trust_folder` is relative to the CWD.

## Symlinks

By default, symlinks are **resolved**:

```text
Trust Folder: ./src
File: ./src/link-to-config.ts (symlink → ../../../.env)

Resolution:
1. Resolve symlink: /home/user/.env
2. Is /home/user/.env inside /home/user/project/src?
3. NO → BLOCKED
```

To allow specific symlinks:

```yaml
project:
  trust_folder: "./src"
  symlink_mode: "follow" # default: "deny"
  symlink_whitelist:
    - "./src/link-to-shared" # Explicit exception
```

## Advanced Configuration

```yaml
# vectora.config.yaml
project:
  trust_folder: "./src"

  # Path resolution behavior
  path_resolution:
    normalize_case: false # Windows: case-insensitive?
    resolve_symlinks: true
    follow_mountpoints: false

  # Auditing
  audit:
    enabled: true
    log_all_accesses: false # true = very verbose
    log_denied_accesses: true
    retention_days: 30
```

---

> **Next**: [Vector Search](./vector-search.md)

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
