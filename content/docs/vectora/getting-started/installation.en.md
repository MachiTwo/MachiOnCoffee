---
title: Installation
slug: installation
date: "2026-04-19T08:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - installation
  - setup
  - npm
  - vectora
  - byok
  - api-keys
---

{{< lang-toggle >}}
Vectora is distributed as a high-performance native binary for Windows, macOS, and Linux. On Windows, installation is standardized via **Winget** and resides in your local programs directory, requiring no Node.js or administrator privileges.

> [!IMPORTANT] > **BYOK (Bring Your Own Key)**: In the Free plan, Vectora requires API keys from Gemini and Voyage. In **Pro** and **Team (Plus)** plans, you can opt for **Managed** mode, where AI credits are already included.

## Prerequisites

## Operating System

- **macOS** 12.0+
- **Linux** (Ubuntu 20.04+, Fedora 35+, Debian 11+)
- **Windows 11** (WSL2 recommended)

## Software

- **64-bit Systems** (x64 or ARM64)
- **Internet Connection** for key activation

## Verify Winget Version (Windows)

```powershell
winget --version # Should return v1.4 or higher
```

## Step 1: Install Vectora

## Windows (Recommended)

Open your terminal (PowerShell or CMD) and run:

```powershell
winget install kaffyn.vectora
```

The binary will be installed in `%LOCALAPPDATA%\Programs\Vectora` and automatically added to your PATH.

## macOS / Linux

Use our quick installation script:

```bash
curl -sSf https://vectora.sh/install.sh | sh
```

## Manual Download

You can also download the binary directly from our [GitHub Releases page](https://github.com/kaffyn/vectora/releases).

## Step 2: Obtain Free API Keys

## Gemini API (Google)

1. Access [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the generated key

**Free limit**: 60 requests per minute, 1.5M tokens/month.

## Voyage API (VoyageAI)

1. Access [Voyage AI Dashboard](https://dash.voyageai.com/api-keys)
2. Click **"Create API Key"**
3. Copy the generated key

**Free limit**: 50 requests per minute, 100M tokens/month.

## Step 3: Configure via Systray

After installation, look for the Vectora icon in your system tray (near the clock).

1. Click the icon and select **"Login"**.
2. This will open your browser for SSO authentication.
3. Once authenticated, Vectora will automatically configure your keys.

## Step 4: Verify Configuration (CLI)

If you prefer the terminal, verify the status:

```bash
vectora auth status
```

## Step 5: Initialize a Project

```bash
# Create a directory for your first project
mkdir my-vectora-project
cd my-vectora-project

# Initialize Vectora
vectora init --name "My Project" --type codebase
```

This creates:

- `vectora.config.yaml` — Project configuration.
- `.vectora/` — Internal directory (cache, local indices).
- `AGENTS.md` — Agent memory file.

## Next Steps

## For Claude Desktop Users

Go to [Claude Code Integration](../integrations/claude-code.md) and configure MCP.

## For Cursor Users

Go to [Cursor Integration](../integrations/cursor.md).

## For VS Code Users

Go to [VS Code Extension](../integrations/vscode.md).

## To Learn Configuration

Go to [Configuration](./configuration.md).

## Troubleshooting

### Error: `command not found: vectora`

**Cause**: The binary is not in your PATH.

**Solution**: Ensure installation was completed and restart your terminal.

### Error: `Error: API key not found`

**Cause**: Environment variables not set or login failed.

**Solution**: Re-run `vectora auth login` or check status with `vectora auth status`.

### Error: `403 Quota Exceeded` (Gemini)

**Cause**: Request limit exceeded (60/min on free tier).

**Solution**: Wait or upgrade to the [Pro plan](../plans/pro.md).

### Error: `EACCES: permission denied`

**Cause**: The binary does not have execution permission.

**Solution**:

```bash
# macOS / Linux
chmod +x $(which vectora)
```

## FAQ

**Q: Do I need internet to use Vectora?**
A: Yes, you need a connection for Gemini and Voyage APIs. For local mode (experimental), you can use local models via Ollama, but this requires additional configuration.

**Q: Are my API keys secure?**
A: Yes. Keys are stored locally in `~/.vectora/credentials.enc` (encrypted) or in your `.env`. Kaffyn never accesses your keys.

**Q: Can I use multiple projects with a single installation?**
A: Yes. Use `vectora init` for each project in different directories.

**Q: How do I update Vectora?**
R: On Windows, use `winget upgrade kaffyn.vectora`. On other systems, re-run the installation script or use `vectora update`.

---

> **Next**: You are all set! Now configure your IDE in [Configuration](./configuration.md).

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
