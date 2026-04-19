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

## Overview

Vectora is installed globally via npm as an MCP (Model Context Protocol) agent. Installation takes less than 5 minutes and requires only Node.js 18+ and free API keys.

> [!IMPORTANT] > **BYOK (Bring Your Own Key)**: In the Free plan, Vectora requires API keys from Gemini and Voyage. In **Pro** and **Team (Plus)** plans, you can opt for **Managed** mode, where AI credits are already included.

---

## Prerequisites

### Operating System

- **macOS** 12.0+
- **Linux** (Ubuntu 20.04+, Fedora 35+, Debian 11+)
- **Windows 11** (WSL2 recommended)

### Software

- **Node.js** 18.0.0 or higher ([download](https://nodejs.org))
- **npm** 9.0.0+ (included with Node.js)
- **git** 2.30+ (optional, for cloning repositories)

### Verify Prerequisites

```bash
node --version # Should return v18.0.0 or higher
npm --version # Should return 9.0.0 or higher
```

---

## Step 1: Install Vectora Globally

```bash
npm install -g @kaffyn/vectora
```

**Expected time**: 2-3 minutes (first installation)

### Verify Installation

```bash
vectora --version
# Expected output: vectora/1.x.x
```

If the command is not found, you may need to update your `PATH`:

```bash
# macOS / Linux
export PATH="$PATH:$(npm config get prefix)/bin"

# Add the line above to your ~/.bashrc or ~/.zshrc for persistence
```

---

## Step 2: Obtain Free API Keys

### Gemini API (Google)

1. Access [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the generated key

**Free limit**: 60 requests per minute, 1.5M tokens/month.

### Voyage API (VoyageAI)

1. Access [Voyage AI Dashboard](https://dash.voyageai.com/api-keys)
2. Click **"Create API Key"**
3. Copy the generated key

**Free limit**: 50 requests per minute, 100M tokens/month.

---

## Step 3: Configure Environment Variables

### Option A: Local `.env` File (Recommended)

Create a `.env` file in your project root:

```bash
cat > .env << 'EOF'
GEMINI_API_KEY=your_gemini_key_here
VOYAGE_API_KEY=your_voyage_key_here
VECTORA_NAMESPACE=my-project
VECTORA_TRUST_FOLDER=.
EOF
```

Replace `your_gemini_key_here` and `your_voyage_key_here` with your actual keys.

### Option B: System Environment Variables

```bash
# macOS / Linux
export GEMINI_API_KEY="your_gemini_api_key"
export VOYAGE_API_KEY="your_voyage_api_key"

# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_gemini_api_key"
$env:VOYAGE_API_KEY = "your_voyage_api_key"
```

### Option C: Use `vectora config` (Interactive)

```bash
vectora config set --key GEMINI_API_KEY
# You will be prompted for interactive input
# Then:
vectora config set --key VOYAGE_API_KEY
```

---

## Step 4: Verify Configuration

```bash
vectora config list
# Should show:
# GEMINI_API_KEY: ••••••••••
# VOYAGE_API_KEY: ••••••••••
# VECTORA_NAMESPACE: my-project
```

---

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

---

## Next Steps

### For Claude Desktop Users

Go to [Claude Code Integration](../integrations/claude-code.md) and configure MCP.

### For Cursor Users

Go to [Cursor Integration](../integrations/cursor.md).

### For VS Code Users

Go to [VS Code Extension](../integrations/vscode.md).

### To Learn Configuration

Go to [Configuration](./configuration.md).

---

## Troubleshooting

### Error: `command not found: vectora`

**Cause**: Node.js is not in your PATH.

**Solution**:

```bash
# Reinstall Node.js: https://nodejs.org
node --version # Must work first
npm install -g @kaffyn/vectora # Reinstall
```

### Error: `Error: API key not found`

**Cause**: Environment variables not configured.

**Solution**: Verify that `GEMINI_API_KEY` and `VOYAGE_API_KEY` are defined:

```bash
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY
```

### Error: `403 Quota Exceeded` (Gemini)

**Cause**: Request limit exceeded (60/min on free tier).

**Solution**: Wait or upgrade to the [Pro plan](../plans/pro.md).

### Error: `EACCES: permission denied`

**Cause**: Insufficient permission for global installation.

**Solution**:

```bash
# Option 1: Use sudo (not recommended)
sudo npm install -g @kaffyn/vectora

# Option 2: Configure npm for home directory installation (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g @kaffyn/vectora
```

---

## FAQ

**Q: Do I need internet to use Vectora?**
A: Yes, you need a connection for Gemini and Voyage APIs. For local mode (experimental), you can use local models via Ollama, but this requires additional configuration.

**Q: Are my API keys secure?**
A: Yes. Keys are stored locally in `~/.vectora/credentials.enc` (encrypted) or in your `.env`. Kaffyn never accesses your keys.

**Q: Can I use multiple projects with a single installation?**
A: Yes. Use `vectora init` for each project in different directories.

**Q: How do I update Vectora?**
A: Use `npm update -g @kaffyn/vectora` or install a specific version: `npm install -g @kaffyn/vectora@latest`.

---

> **Next**: You are all set! Now configure your IDE in [Configuration](./configuration.md).

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
