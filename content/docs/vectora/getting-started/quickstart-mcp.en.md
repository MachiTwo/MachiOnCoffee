---
title: Quickstart MCP
slug: quickstart-mcp
date: "2026-04-19T08:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - mcp
  - quickstart
  - claude-desktop
  - integration
  - vectora
---

{{< lang-toggle >}}
This guide allows you to integrate Vectora with Claude Desktop via MCP in less than 5 minutes.

> [!IMPORTANT] Prerequisites: Vectora installed globally (`vectora --version`) and Claude Desktop installed ([download](https://claude.ai/download)).

## Step 1: Locate the Configuration File

## macOS / Linux

```bash
# Claude Desktop configuration file
open ~/.claude/claude_desktop_config.json

# If it does not exist, create it with:
mkdir -p ~/.claude
touch ~/.claude/claude_desktop_config.json
```

## Windows

```powershell
# Configuration file (WSL2 or Windows)
"$env:APPDATA\Claude\claude_desktop_config.json"

# If it does not exist, create it with:
New-Item -Path "$env:APPDATA\Claude" -ItemType Directory -Force
```

## Step 2: Add Vectora as an MCP Server

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp-serve"],
      "env": {
        "GEMINI_API_KEY": "sk-xxx...",
        "VOYAGE_API_KEY": "pa-xxx...",
        "VECTORA_NAMESPACE": "my-project"
      }
    }
  }
}
```

## Alternative: Use System Environment Variables

If you already have `GEMINI_API_KEY` and `VOYAGE_API_KEY` defined:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp-serve"]
    }
  }
}
```

## Step 3: Restart Claude Desktop

```bash
# Completely close Claude Desktop and open it again
# This loads the new MCP configuration
```

## Step 4: Test the Connection

## Via Claude Desktop Chat

Open Claude Desktop and test:

```text
Show me the available files using Vectora
```

Claude should respond with something like:

```text
I have access to Vectora, a code context engine. Let me check what files are available in your project.

[Vectora is now searching your codebase...]

Available files in namespace 'my-project':
- src/auth/jwt.ts (authentication)
- src/services/database.ts (database layer)
- docs/README.md (documentation)
...
```

## Verify MCP Status

If you receive an error:

1. **Open MCP Inspector** (in Claude Desktop: Menu → Settings → Developer Tools).
2. **Search for "vectora"** in the server list.
3. **Status should be "Connected"**.

If it is not connected:

- Verify that `vectora --version` works in the terminal.
- Check the `claude_desktop_config.json` file (JSON syntax).
- Restart Claude Desktop.

## Step 5: Your First Vectora Command

## Explore the Codebase

```text
What is the structure of this project? List the main directories.
```

Claude uses `file_list` via Vectora.

## Search Context

```text
How does JWT authentication work in this project? Find the implementation.
```

Claude uses `context_search` for semantic search.

## Analyze a File

```text
Read and explain the src/main.ts file
```

Claude uses `file_read` to read the file.

## Project Structure

After running `vectora init`, you will have:

```text
my-project/
├── vectora.config.yaml # Project configuration
├── AGENTS.md # Agent memory (auto-generated)
├── .vectora/ # Cache and local indices
│ ├── embeddings/ # Embedding cache
│ └── index.json # Index metadata
├── src/ # Your code
└── .env # Environment variables (never commit!)
```

## Available MCP Commands

| Command          | What it does                | Example              |
| ---------------- | --------------------------- | -------------------- |
| `context_search` | Semantic search in codebase | "JWT authentication" |
| `file_read`      | Reads a file                | `src/main.ts`        |
| `file_list`      | Lists files recursively     | `src/`               |
| `file_write`     | Writes or modifies a file   | Creating a new file  |
| `file_edit`      | Edits part of a file        | Changing a function  |
| `grep_search`    | Search via regex            | Specific patterns    |

## Troubleshooting

### Error: `Vectora MCP server not found`

**Cause**: `vectora` is not in your PATH.

**Solution**:

```bash
# Check where vectora is installed
which vectora # macOS/Linux
where.exe vectora # Windows

# If not found, reinstall:
npm install -g @kaffyn/vectora
```

### Error: `Connection refused`

**Cause**: Vectora cannot connect to the Gemini/Voyage API.

**Solution**:

```bash
# Verify API keys
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# If empty, configure:
export GEMINI_API_KEY="sk-xxx"
export VOYAGE_API_KEY="pa-xxx"
```

### Error: `Project not found`

**Cause**: Namespace does not exist.

**Solution**:

```bash
# Initialize the project
vectora init --name "My Project"

# Or specify in claude_desktop_config.json:
"VECTORA_NAMESPACE": "my-project"
```

### Claude does not use Vectora automatically

**Cause**: Claude doesn't detect that the tool is relevant.

**Solution**: Be explicit:

```text
Use Vectora to search for information about authentication in this project.
```

## Next Steps

- **Deep Dive**: Read [Context Engine](../concepts/context-engine.md).
- **Integrate with Cursor**: [Cursor Integration](../integrations/cursor.md).
- **Understand Security**: [Guardian & RBAC](../security/guardian.md).

## FAQ

**Q: Can I use Vectora with other agents besides Claude?**
A: Yes! See [Gemini Integration](../integrations/gemini-integration.md) and [Custom Agents](../integrations/custom-agents.md).

**Q: Does Vectora work offline?**
A: Partially. Context search requires internet (Voyage API). File operations work offline.

**Q: How to debug MCP connections?**
A: Use the MCP Inspector in Claude Desktop (Menu → Developer Tools → MCP Inspector).

---

> **Next**: Learn about [Troubleshooting](./troubleshooting.md).

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
