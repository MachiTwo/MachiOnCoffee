---
title: VS Code Extension
slug: vscode-extension
date: "2026-04-19T09:45:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - extension
  - integration
  - mcp
  - vscode
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

**OWN APP**: Vectora offers a native VS Code extension with integrated UI (sidebar panel, commands, inline hover) — no MCP required. Fully customized development for VS Code.

> [!IMPORTANT] VS Code Extension (own app) vs MCP Protocol (generic for multiple IDEs). Use the extension if you are using VS Code.

## Installation

## Via VS Code Marketplace

1. Open VS Code.
2. Go to **Extensions** (Cmd/Ctrl + Shift + X).
3. Search for: `Vectora`.
4. Click **Install**.

## Alternative: Manual Install

```bash
# Clone the repository
git clone https://github.com/kaffyn/vectora-vscode.git

# Install in ~/.vscode/extensions
ln -s $(pwd)/vectora-vscode ~/.vscode/extensions/
```

## Initial Setup

## Step 1: Configure Vectora in the Project

```bash
cd ~/your-project
vectora init --name "My Project" --type codebase
```

## Step 2: Open Project in VS Code

```bash
code ~/your-project
```

## Step 3: Configure Keys

VS Code will prompt for API keys on the first run. You can:

- **Option A**: Paste keys directly (stored in encrypted settings.json).
- **Option B**: Use local `.env` (`.env` will be read automatically).
- **Option C**: Use system environment variables (PATH, HOME, etc.).

```bash
# Via .env (recommended)
cat > .env << 'EOF'
GEMINI_API_KEY=sk-...
VOYAGE_API_KEY=sk-...
VECTORA_NAMESPACE=your-namespace
EOF
```

## Interface & Features

## Sidebar Panel

VS Code displays a "Vectora" panel in the sidebar:

```text
┌─────────────────────────┐
│ Vectora │
├─────────────────────────┤
│ Indexed Files │
│ • src/ (2847 chunks) │
│ • docs/ (312 chunks) │
│ │
│ Search │
│ [Search box] │
│ │
│ Stats │
│ Precision: 0.72 │
│ Latency: 120ms │
│ Indexed: 3159 chunks │
└─────────────────────────┘
```

## Command Palette

Access commands via `Cmd/Ctrl + Shift + P`:

```text
Vectora: Search Context
Vectora: Analyze Dependencies
Vectora: Find Tests
Vectora: Index Status
Vectora: Show Metrics
```

## Inline Hover

Hover over an identifier to see context:

```typescript
function getUserById(|id: string) { ← Hover here
  // Shows:
  // - Type: function
  // - Defined in: src/user-service.ts:45
  // - Similar context: findUserById, getUser, etc.
}
```

## Step-by-Step Workflows

The workflows below demonstrate the typical experience of using the Vectora extension in VS Code, with a detailed interface and clear steps.

## Workflow 1: Quick Search (5s setup)

**Scenario**: You want to understand how JWT tokens are validated in the project.

```text
1. Press Cmd/Ctrl + Shift + P (Command Palette)
   → Shows: empty input box with ">" at the top

2. Type: "Vectora: Search Context"
   → Autocomplete shows Vectora option

3. Press Enter
   → Opens search panel (right of the sidebar)

4. Type: "How to validate tokens?"
   → In real-time: shows results as you type

5. Results appear in 120-250ms
   ┌─────────────────────────────────┐
   │ Vectora Results (8 chunks) │
   ├─────────────────────────────────┤
   │ src/auth/jwt.ts:45 │ ← Click to go
   │ validateToken() { ... │
   │ precision: 0.92 | latency 240ms│
   │ │
   │ src/auth/guards.ts:12 │
   │ VerifyJWT middleware { ... │
   │ precision: 0.88 | latency 240ms│
   │ │
   │ src/auth/types.ts:3 │
   │ interface JWTPayload { ... │
   │ precision: 0.76 │
   │ │
   │ [Show more] │
   └─────────────────────────────────┘
```

Click any result → editor jumps to the file.

## Workflow 2: Intelligent Function Analysis

**Scenario**: You clicked on a function and want to see EVERYTHING related to it.

```text
1. Position cursor on: getUserById
2. Press Cmd/Ctrl + Shift + H (Find References)
3. VS Code shows "Find All References" panel:

   ┌─────────────────────────────────┐
   │ 62 References to getUserById │
   ├─────────────────────────────────┤
   │ DIRECT CALLS (47) │
   │ • src/routes/user.ts:23 │
   │ • src/middleware/auth.ts:34 │
   │ • src/services/profile.ts:12 │
   │ │
   │ INDIRECT via getUserData (12) │
   │ • src/handlers/index.ts:5 │
   │ • src/cache/service.ts:99 │
   │ │
   │ TESTS (3) │
   │ • src/__tests__/user.test.ts:45 │
   │ │
   │ [Expand with Vectora] ← New │
   └─────────────────────────────────┘
```

Click "Expand with Vectora" → shows semantic context:

```text
Similar references not found via AST:
• getUserByEmail() [85% similar]
• fetchUser() [72% similar]
• getActiveUser() [68% similar]
```

## Workflow 3: Context-Aware Code Review (Understanding complex PR)

**Scenario**: Reviewing a PR that touches authentication; need to understand the impact.

```text
1. Open modified file: auth/jwt.ts
2. Cmd/Ctrl + Alt + F (Find Changes in Context)
3. Panel shows:

   ┌────────────────────────────────────┐
   │ Vectora: Changes & Impact │
   ├────────────────────────────────────┤
   │ MODIFIED LINES │
   │ L45: function validateToken │
   │ L52: if (!token.verified) │
   │ │
   │ FILES USING THESE FUNCTIONS │
   │ • src/guards/auth.guard.ts (5) │
   │ • src/routes/api.ts (3) │
   │ • src/middleware/verify.ts (8) │
   │ │
   │ RELATED TESTS │
   │ • auth.guard.test.ts │
   │ • jwt.validation.test.ts │
   │ │
   │ ALERT: 16 dependencies │
   │ Recommend running full tests │
   └────────────────────────────────────┘
```

4. Click "Run Related Tests"
   → VS Code executes only relevant tests (10s vs 2min full suite)

## Configuration

## settings.json

```json
{
  "vectora.enabled": true,
  "vectora.namespace": "your-namespace",
  "vectora.trustFolder": "./src",
  "vectora.autoIndex": true,
  "vectora.indexOnSave": true,
  "vectora.maxTokens": 4096,
  "vectora.searchStrategy": "semantic",
  "vectora.showMetrics": true,
  "vectora.debugMode": false
}
```

## Advanced Config

```yaml
# .vscode/vectora.yaml (alternative)
vectora:
  namespace: your-namespace
  context_engine:
    strategy: "semantic"
    max_depth: 3
    timeout_ms: 2000

  ui:
    show_metrics: true
    position: "right" # or "left"
    width_percent: 30

  indexing:
    auto_index: true
    on_save: true
    exclude:
      - node_modules/**
      - .git/**
```

## Complementary Extensions

For the best experience, install:

1. **ES7+ React/Redux/React-Native snippets** — Smart autocomplete.
2. **Prettier** — Consistent formatting.
3. **GitLens** — Blame + history (combines well with Vectora).

## Troubleshooting

## Extension doesn't appear in the sidebar

**Cause**: It is not enabled.

**Solution**:

```text
Cmd/Ctrl + Shift + X → Search "Vectora" → Click "Enable"
```

## "Vectora command not found" in integrated terminal

**Cause**: VS Code uses a different PATH.

**Solution**:

```bash
# In the integrated terminal
which vectora
# If not found:
npm install -g @kaffyn/vectora

# Or add to PATH in settings.json
"vectora.commandPath": "/usr/local/bin/vectora"
```

## "API key not configured"

**Solution**:

1. Cmd/Ctrl + Shift + P → "Vectora: Configure"
2. Paste your keys.
3. Or use `.env` in the project root.

## Extension is very slow

**Reduce scope**:

```json
{
  "vectora.trustFolder": "./src",
  "vectora.searchStrategy": "structural"
}
```

**Disable auto-index**:

```json
{
  "vectora.autoIndex": false,
  "vectora.indexOnSave": false
}
```

## Performance Tips

1. **Incremental Index**: Only changed files are re-indexed.

   ```bash
   # In VS Code terminal
   vectora index --incremental
   ```

2. **Filter by Extension**:

   ```json
   {
     "vectora.includePatterns": ["**/*.ts", "**/*.tsx"],
     "vectora.excludePatterns": ["**/*.test.ts"]
   }
   ```

3. **Local Embedding**: For maximum privacy + performance:

   ```json
   {
     "vectora.embeddingProvider": "local",
     "vectora.embeddingModel": "all-MiniLM-L6-v2"
   }
   ```

## Hotkeys

| Shortcut               | Action               |
| ---------------------- | -------------------- |
| `Cmd/Ctrl + Shift + P` | Open Vectora command |
| `Cmd/Ctrl + Shift + V` | Open Vectora sidebar |
| `Cmd/Ctrl + Alt + F`   | Find via Vectora     |
| `Cmd/Ctrl + Alt + D`   | Analyze dependencies |

Customize in: **Code** → **Preferences** → **Keyboard Shortcuts**

## Comparison: Extension vs MCP

| Feature     | VS Code Extension       | MCP (Cursor/Claude) |
| ----------- | ----------------------- | ------------------- |
| Install     | Marketplace             | Config JSON         |
| UI Panel    | Native                  | Chat-based          |
| Hotkeys     | Customizable            | Fixed               |
| Performance | Local                   | Network             |
| Privacy     | Full (local embeddings) | APIs                |

**Recommendation**: Use VS Code Extension for best UX. Use MCP for Cursor/Claude.

## Limitations

| Resource            | Limit                       |
| ------------------- | --------------------------- |
| Simultaneous search | 1                           |
| Context window      | 4K-8K tokens (configurable) |
| Index size          | Unlimited (disk)            |
| Latency target      | < 300ms                     |

---

> **Next**: [ChatGPT Plugin](./chatgpt-plugin.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
