---
title: Gemini CLI
slug: gemini-cli
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - gemini
  - integration
  - mcp
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

Integrate Vectora with the **Google Gemini CLI** to use Vectora within Gemini workflows.

## Quick Setup

## 1. Install Gemini CLI

```bash
npm install -g @google/generative-ai-cli
```

## 2. Configure Vectora as an MCP Server

In your `.gemini/config.json`:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_NAMESPACE": "your-project"
      }
    }
  }
}
```

## 3. Use in Gemini Prompts

```bash
gemini chat --system "You have access to Vectora to search for code"
```

## Use Cases

| Case              | Description                                    |
| ----------------- | ---------------------------------------------- |
| **Code Search**   | Search for relevant files via Gemini + Vectora |
| **Documentation** | Generate documentation from indexed code       |
| **Analysis**      | Analyze codebase patterns                      |

## Troubleshooting

**Gemini not seeing Vectora?**

1. Verify that `vectora mcp --stdio` runs locally.
2. Check permissions in `.gemini/config.json`.
3. Restart the Gemini CLI.

---

> Questions? [GitHub Discussions](https://github.com/Kaffyn/Vectora/discussions)
