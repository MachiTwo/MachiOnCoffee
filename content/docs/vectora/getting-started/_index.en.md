---
title: Getting Started
slug: getting-started
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - getting
  - mcp
  - setup
  - started
  - vectora
---

{{< lang-toggle >}}

Everything you need to get started with Vectora in 5 minutes: installation, key configuration, and your first search.

## Recommended Sequence

| Step | Description                             | Time      |
| ---- | --------------------------------------- | --------- |
| 1⃣   | [Installation](./installation.md)       | 2 min     |
| 2⃣   | [Configuration](./configuration.md)     | 2 min     |
| 3⃣   | [Quickstart MCP](./quickstart-mcp.md)   | 3 min     |
| 4⃣   | [Troubleshooting](./troubleshooting.md) | On demand |

## What You Will Do

### Step 1: Install Vectora

```bash
npm install -g @vectora/cli
vectora --version
```

**Prerequisites**: Node.js 18+, npm or yarn.

### Step 2: Configure API Keys

Vectora uses BYOK (Bring Your Own Key). You provide:

- `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com)
- `VOYAGE_API_KEY` from [Voyage AI](https://www.voyageai.com)

```bash
vectora config set GEMINI_API_KEY "your-key-here"
vectora config set VOYAGE_API_KEY "your-key-here"
```

### Step 3: Connect to IDE

- **Claude Code**: 1 line in `claude_desktop_config.json`
- **Cursor**: 1 line in `.cursor/settings.json`
- **Zed**: 1 line in `.zed/settings.json`

See [Quickstart MCP](./quickstart-mcp.md) for copy/paste instructions.

### Step 4: Make Your First Search

```bash
vectora search "How to authenticate users?"
```

Or directly in the IDE using MCP tool autocomplete.

## Need Help?

- **Installation error?** → [Troubleshooting](./troubleshooting.md)
- **MCP not connecting?** → [Quickstart MCP](./quickstart-mcp.md)
- **Config not working?** → [Configuration](./configuration.md)
- **Other questions?** → [FAQ](../faq/)

## Next Readings

After setup:

1. [Concepts](../concepts/) — Understand how it works
2. [Integrations](../integrations/) — Configure your IDE
3. [Security](../security/) — Protect your data

---

> Total time: ~5-10 minutes. Let's go!
