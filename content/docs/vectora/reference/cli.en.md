---
title: CLI
slug: cli
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

Vectora offers a **complete CLI interface** for configuration, indexing, and debugging. Use it for automation, CI/CD, or local development.

> [!TIP]
> Use `vectora --help` to see all commands, or `vectora [command] --help` for specific details.

## General Structure

```bash
vectora [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

## Global Flags

```bash
--version, -v   # Show version
--help, -h      # Show help
--config PATH   # Custom path to vectora.yaml
--namespace NS  # Override default namespace (default: local)
--debug         # Enable debug mode (verbose logging)
--quiet, -q     # Suppress output (except errors)
--json          # JSON output for automation
```

Examples:

```bash
vectora --version
vectora --debug index
vectora --namespace staging init
vectora --config ./custom.yaml search "query"
```

## Commands

Vectora's command-line interface is organized into logical subcommands that facilitate management throughout the entire lifecycle of your project.

## vectora init

Initializes a new Vectora project.

```bash
vectora init [OPTIONS]

OPTIONS:
  --name NAME # Project name (default: directory name)
  --type TYPE # Type: codebase|docs|hybrid (default: codebase)
  --namespace NS # Customized namespace (default: org-project-env)
  --trust-folder PATH # Trust folder (default: .)
  --providers YAML # Provider config (see config docs)
```

**Examples**:

```bash
vectora init --name "My App" --type codebase
# Creates vectora.config.yaml + .vectora/

vectora init --namespace kaffyn-backend-prod --type codebase
# Creates with specific namespace
```

## vectora index

Indexes files in the namespace.

```bash
vectora index [OPTIONS]

OPTIONS:
  --force               # Reindex even if no changes are detected
  --incremental         # New/modified files only (default: true)
  --exclude PATTERN     # Exclude globs (e.g., bin/**, .git/**)
  --include PATTERN     # Include only specific globs (e.g., pkg/**, cmd/**)
  --dry-run             # Simulate indexing without persisting data
  --watch               # Watch for filesystem changes (dev mode)
```

**Examples**:

```bash
# Incremental indexing (default)
vectora index

# Reindex everything
vectora index --force

# Go files only
vectora index --include "**/*.go"

# Development mode (watch)
vectora index --watch

# Verify what would be indexed
vectora index --dry-run
```

## vectora search

Semantic search via CLI.

```bash
vectora search QUERY [OPTIONS]

OPTIONS:
  --strategy STRATEGY # semantic|structural|hybrid (default: semantic)
  --top-k NUM # Number of results (default: 10)
  --format FORMAT # text|json|markdown (default: text)
  --include-snippets # Include code snippet
  --compare-baseline # Compare with previous version
```

**Examples**:

```bash
# Simple search
vectora search "How to do login?"

# Structural search for code relationships
vectora search "Who calls getUserById?" --strategy structural

# JSON output
vectora search "validation" --format json

# Search with code snippets
vectora search "middleware" --include-snippets
```

## vectora analyze

Deep analysis with LLM (Gemini).

```bash
vectora analyze QUERY [OPTIONS]

OPTIONS:
  --model MODEL # LLM to use (default: gemini-3-flash)
  --context NUM # How many chunks to use (default: 10)
  --output FILE # Save to file (e.g., report.md)
  --compare-baseline # Compare with previous analysis
```

**Examples**:

```bash
# Simple analysis
vectora analyze "How does authentication work?"

# Deep analysis
vectora analyze "Review this code for security" --model gemini-pro --context 20

# Save to file
vectora analyze "Write API documentation" --output docs/api.md
```

## vectora config

Manages configuration.

```bash
vectora config [SUBCOMMAND]

SUBCOMMANDS:
  get KEY # Get value
  set KEY VALUE # Set value
  list # List all
  validate # Validate current config
  reset # Reset to default
  show-schema # Show YAML schema
```

**Examples**:

```bash
# View current configuration
vectora config list

# View specific key
vectora config get project.namespace

# Set key
vectora config set context_engine.strategy semantic

# Validate config
vectora config validate

# View available schema
vectora config show-schema
```

## vectora namespace

Manage namespaces.

```bash
vectora namespace [SUBCOMMAND]

SUBCOMMANDS:
  create --name NS # Create new namespace
  delete --name NS # Delete namespace (PERMANENT)
  list # List all namespaces
  info --name NS # Details of a namespace
  reset --name NS # Clear chunks of a namespace
```

**Examples**:

```bash
# List namespaces
vectora namespace list

# Create new
vectora namespace create --name kaffyn-new-project

# View details
vectora namespace info --name kaffyn-vectora-prod

# Clear namespace
vectora namespace reset --name kaffyn-old-project
```

## vectora mcp

Starts MCP server for Claude Code, Cursor, etc.

```bash
vectora mcp [OPTIONS]

OPTIONS:
  --port PORT # Port (default: 9090)
  --host HOST # Host (default: localhost)
  --namespace NS # Default namespace
  --no-auth # Disable authentication (dev only)
```

**Examples**:

```bash
# Start server
vectora mcp

# With custom port
vectora mcp --port 9091

# Public server
vectora mcp --host 0.0.0.0 --port 9090
```

## vectora server

Starts full HTTP server (with UI, webhooks).

```bash
vectora server [OPTIONS]

OPTIONS:
  --port PORT # Port (default: 3000)
  --host HOST # Host (default: localhost)
  --ui # Enable web dashboard
  --webhooks # Enable webhooks support
  --cert FILE # SSL/TLS certificate
  --key FILE # SSL/TLS key
```

**Examples**:

```bash
# Basic server
vectora server

# With web UI
vectora server --ui

# HTTPS with certificate
vectora server --cert cert.pem --key key.pem
```

## vectora auth

Manage SSO authentication and access tokens.

```bash
vectora auth [COMMAND]

COMMANDS:
  login     # Start browser-based SSO flow
  logout    # End local session
  status    # Show logged-in user and token validity
  token     # Manage personal access tokens (PAT)
```

**Examples**:

```bash
# Interactive Login (opens Systray and Browser)
vectora auth login

# Check account status
vectora auth status
```

## vectora logs

View execution logs.

```bash
vectora logs [OPTIONS]

OPTIONS:
  --level LEVEL # debug|info|warn|error (default: info)
  --service SERVICE # Filter by service
  --since DURATION # Last N hours (e.g., 24h)
  --follow, -f # Stream logs in real-time
  --format FORMAT # text|json (default: text)
```

**Examples**:

```bash
# View recent logs
vectora logs --since 1h

# Debug logs in real-time
vectora logs --level debug --follow

# Search logs only
vectora logs --service search --since 24h

# JSON for parsing
vectora logs --format json | jq '.[]'
```

## vectora metrics

View operation metrics.

```bash
vectora metrics [OPTIONS]

OPTIONS:
  --period PERIOD # 24h|7d|30d (default: 24h)
  --export FORMAT # csv|json|prometheus (default: text)
  --output FILE # Save to file
```

**Examples**:

```bash
# Metrics of the last day
vectora metrics --period 24h

# Export as CSV
vectora metrics --period 7d --export csv --output metrics.csv

# Prometheus format
vectora metrics --export prometheus
```

## vectora audit

View audit log (who did what).

```bash
vectora audit [OPTIONS]

OPTIONS:
  --action ACTION # Filter by action (search|index|delete)
  --user USER # Filter by user
  --since DURATION # Since when (e.g., 7d)
  --limit NUM # Line limit (default: 100)
```

**Examples**:

```bash
# Full audit
vectora audit

# Searches of the last 7 days
vectora audit --action search --since 7d

# Deletions by user
vectora audit --action delete --user "your-email@company.com"
```

## vectora health

Check system health.

```bash
vectora health [OPTIONS]

OPTIONS:
  --detailed # Show details of each component
  --fix # Attempt to fix problems
```

**Examples**:

```bash
# Fast health
vectora health

# With details
vectora health --detailed

# Attempt to fix
vectora health --fix
```

## Exit Codes

```text
0 # Success
1 # Generic error
2 # Configuration error
3 # API error
4 # Authentication failed
5 # Namespace not found
```

## Environment Variables

Override CLI options:

```bash
VECTORA_NAMESPACE=staging vectora search "..."
VECTORA_LOG_LEVEL=debug vectora index
VECTORA_CONFIG=./custom.yaml vectora init
VECTORA_TRUST_FOLDER=./src vectora index
```

---

> **Next**: [Architecture Overview](./overview.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
