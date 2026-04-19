# Vectora

> [!TIP]
> Read this file in another language | Leia esse arquivo em outro idioma.
> [English](README.md) | [Português](README.pt.md)

> [!NOTE]
>
> **Correct context + reliable execution for developers.**
> The specialist sub-agent that empowers any primary agent in real-world codebases.

---

**Traditional agents operate in fragmented context.
Vectora delivers connected context.**

- semantic search via Qdrant (HNSW + quantization)
- code structure (files, functions, dependencies)
- isolated namespaces with RBAC via Supabase
- multi-hop reasoning with Context Engine

Result: agents that understand how your system really works — not just isolated snippets.

---

## ✨ Highlights

- **Specialist Sub-Agent**: Integrates via MCP/ACP with Claude Code, Gemini CLI, Cursor, and IDEs — without competing, only empowering.
- **Intelligent Context Engine**: Decides *what*, *how*, and *when* to fetch — avoids noise, reduces tokens, delivers structured context.
- **Namespaces with RBAC**: Real isolation between projects; shared public namespaces (Godot, TypeScript, Rust) as ready-to-use "skills".
- **Hard-Coded Guardian**: Immutable blocklist (.env, .key, .pem, binaries) — security through code, not just prompts.
- **Provider-Agnostic**: OpenAI, Gemini, Claude, OpenRouter, or local llama.cpp — choose your stack, keep the same interface.
- **Validation Harness**: Objective proof of quality with `vectora harness run --compare vectora:on,off`.
- **Cloud-First, Local-Optional**: Managed Qdrant + Supabase + Vercel; local inference option via llama.cpp for extreme privacy.
- **Zero Infra for the User**: `npm install -g vectora-agent` — no Kubernetes, no database management.

---

## 🎯 Who is Vectora for?

| Profile                       | Why use it                                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Individual Developer** | Understand legacy codebases, refactor with confidence, generate contextualized tests — without wasting time manually navigating.                        |
| **Engineering Teams**    | Shared namespaces with RBAC: internal documentation, architecture patterns, and technical decisions available as context for the whole team. |
| **Agent Integrators**   | Add precise RAG and reliable execution to your Tier-1 agent via MCP — without rebuilding the context engine.                                     |
| **Privacy-First Users**      | Optional local mode with llama.cpp: 100% offline inference, data never leaves your machine.                                                     |

> 💡 **Vectora is not an autonomous agent.**  
> It is the layer that makes any agent work better on code.

---

## 🏗️ EndGame Architecture

```text
[IDE / Primary Agent]
         ↓ MCP / ACP (stdio)
[Vectora Agent - TypeScript Runtime]
         ├── Protocol Layer: @modelcontextprotocol/server + JSON-RPC
         ├── Tool Router + Guardian Middleware (security first)
         ├── Context Engine: decides what/how/when to fetch
         ├── Provider Adapter: OpenAI/Gemini/Claude/OpenRouter/llama.cpp
         │
         ├── Qdrant Cloud → Vector Search (payload filtering by namespace)
         └── Supabase → Auth, Projects, Metadata, RLS policies
```

### Official Stack

| Layer              | Technology                              | Why we chose it                                                                   |
| ------------------- | --------------------------------------- | ------------------------------------------------------------------------------------ |
| **Runtime**         | TypeScript + Node.js 20+                | Mature ecosystem for MCP/ACP, Vercel's AI SDK ready for streaming/tool calling |
| **Vector DB**       | Qdrant Cloud (multi-tenant)             | Native HNSW, payload filtering, quantization, scales without operation                    |
| **Metadata/Auth**   | Supabase (Postgres + Auth + RLS)        | Native Row Level Security, realtime, simple integration with Next.js                  |
| **API/Edge**        | Vercel Functions + AI Gateway           | Serverless, edge-ready, integrated billing, zero infra to manage                 |
| **Dashboard**       | Next.js 14 + Tailwind                   | Landing + configuration + billing in a single app, automatic deploy                  |
| **Local Inference** | llama.cpp via `@vectora/llama-provider` | Optional total privacy, without depending on external APIs                            |

---

## 🔌 Integration Protocols

### MCP (Model Context Protocol)

For integration with Tier-1 agents: Claude Code, Gemini CLI, Antigravity, etc.

```bash
# In your Claude Desktop config.json:
{
  "mcpServers": {
    "vectora": {
      "command": "npx",
      "args": ["vectora-agent", "mcp-serve"],
      "env": {
        "VECTORA_API_KEY": "your_key_here"
      }
    }
  }
}
```

- **Focus on Context**: Vectora exposes RAG, filesystem, and code analysis tools.
- **Stable Tool Calling**: AI SDK + adapter layer normalizes responses across providers.
- **Native Streaming**: Tokens arrive in real-time, without artificial buffering.

### ACP (Agent Client Protocol)

For direct integration with IDEs via JSON-RPC 2.0 over stdio/Unix Sockets.

- **Low Latency**: Target <100ms from IDE event to context response.
- **Restricted Scope**: All operations validate Trust Folder + namespace before execution.
- **Transparent Fallback**: If the primary provider fails, it automatically routes to the configured fallback.

---

## 🤖 AI Agnostic: Choose Your Provider

Vectora doesn't lock you into any provider. Configure via CLI or dashboard:

```bash
# Example: OpenRouter as a unified gateway
vectora config --provider openrouter --key $OPENROUTER_KEY

# Example: Gemini for multimodality
vectora config --provider gemini --key $GEMINI_KEY

# Example: Local mode with llama.cpp
vectora config --provider local --model ~/.vectora/models/qwen3-1.7b-instruct.Q4_K_M.gguf
```

### Supported Providers

| Provider       | SDK                       | Models                                 | Mode         |
| -------------- | ------------------------- | --------------------------------------- | ------------ |
| **OpenRouter** | `ai` + OpenAI compat.     | Any model on the gateway              | Cloud        |
| **Google**     | `@google/genai`           | Gemini 2.0 Flash/Pro, Embedding 2.0     | Cloud        |
| **Anthropic**  | `@anthropic-ai/sdk`       | Claude 3.5/3.7 Sonnet/Opus              | Cloud        |
| **Alibaba**    | `openai` compat.          | Qwen3.5, Qwen3-Embedding                | Cloud        |
| **Local**      | `@vectora/llama-provider` | Qwen3-1.7B, Gemma3, Phi-4 via llama.cpp | 100% Offline |

> [!TIP]
> **Gateway Support**: Point to OpenRouter or any OpenAI-compatible gateway to load balance between models without changing configuration.

---

## 🧩 Agentic Toolkit (Core Tools)

All tools are exposed via JSON schema, validated by Zod before execution:

### Filesystem & Code

| Tool          | Description                                           | Scope                   |
| ------------- | --------------------------------------------------- | ------------------------ |
| `file_read`   | Paged file reading (supports large files)      | Trust Folder + namespace |
| `file_write`  | Controlled writing with automatic Git snapshot      | Trust Folder + namespace |
| `file_edit`   | Surgical patching without rewriting the entire file | Trust Folder + namespace |
| `file_list`   | Recursive listing with structural metadata       | Trust Folder + namespace |
| `file_find`   | Search by glob patterns (`**/*.ts`, `src/**/*.tsx`) | Trust Folder + namespace |
| `grep_search` | Regex search via ripgrep with filters and limit        | Trust Folder + namespace |

### Context & RAG

| Tool             | Description                                     | Key Advantage                             |
| ---------------- | --------------------------------------------- | --------------------------------------- |
| `context_search` | Semantic + structural search in the codebase      | Context Engine decides what to search      |
| `context_ingest` | On-demand indexing of files/directories  | Multi-modal: text, PDF, image, audio  |
| `context_build`  | Structured context composition for the LLM | Avoids overfetch, delivers only what's relevant |

### Web & External

| Tool         | Description                                       | Security                                             |
| ------------ | ----------------------------------------------- | ----------------------------------------------------- |
| `web_fetch`  | URL fetch with relevant content extraction | Output sanitization, malicious domain blocking |
| `web_search` | Web search for updated external context      | Results filtered by relevance and freshness         |

### System & Memory

| Tool           | Description                                                  | Usage                                             |
| -------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| `terminal_run` | Command execution with real-time stdout/stderr       | Configurable timeout, optional approval         |
| `memory_save`  | Fact/preference persistence (global or per-project) | Isolated by namespace, encrypted at rest |
| `plan_mode`    | Structured mode to validate plan before execution      | UX for human review of complex actions       |

> [!IMPORTANT]
> **Hard-Coded Guardian**: All tools validate paths against an immutable blocklist (.env, .key, .pem, binaries, lockfiles). Blocked files are never read, embedded, or sent to the LLM — regardless of provider or prompt.

---

## 🔐 Security by Design

### Hard-Coded Guardian (TypeScript Middleware)

```ts
// packages/core/src/security/guardian.ts
export const HARD_BLOCKLIST = [
  /\.env(\..+)?$/,
  /\.key$/,
  /\.pem$/,
  /\.crt$/,
  /\.p12$/,
  /(^|\/)\.git\//,
  /(^|\/)node_modules\//,
  /(^|\/)\.venv\//,
  /\.(bin|exe|dll|so|dylib|pyc|pyo)$/,
  /^(package-lock\.json|pnpm-lock\.yaml|yarn\.lock)$/,
];

export class Guardian {
  static isBlocked(path: string): boolean {
    return HARD_BLOCKLIST.some((pattern) => pattern.test(path));
  }

  static sanitizeOutput(content: string): string {
    return content
      .replace(
        /(?:aws_access_key_id|aws_secret_access_key)\s*[:=]\s*['"]?[\w+/]{20,}['"]?/gi,
        "[REDACTED_AWS]",
      )
      .replace(/ghp_[\w]{36}/g, "[REDACTED_GITHUB]")
      .replace(/sk-[a-zA-Z0-9]{48}/g, "[REDACTED_OPENAI]");
  }
}
```

### Namespaces with RBAC (Supabase + Qdrant)

```yaml
# Example: public namespace godot-4.6-api
namespace:
  id: "godot-4.6-api"
  visibility: "public" # public | team | private
  owner: "kaffyn"
  rbac:
    read: ["*"] # any authenticated user can read
    write: ["org:kaffyn"] # only the owner organization can update
    delete: ["org:kaffyn"]
```

- **Supabase RLS**: Row Level Security in Postgres for metadata and permission control.
- **Qdrant Payload Filtering**: All vector queries include a mandatory filter by `namespace_id` + `visibility`.
- **Real Isolation**: Contexts never leak between namespaces; you control which ones are "mounted" in the session.

### Trust Folder + Symlink Protection

```ts
// Scope validation before any operation
export function validateTrustFolder(
  requestedPath: string,
  trustFolder: string,
): boolean {
  const resolved = fs.realpathSync(requestedPath);
  const normalizedTrust = path.resolve(trustFolder);
  return resolved.startsWith(normalizedTrust);
}
```

---

## 🧪 Vectora Harness: Objective Validation

> [!NOTE]
> The Harness does NOT validate "general intelligence". It validates **operational consistency + correct context usage + execution security**.

### Objective

Ensure that any agent using Vectora → behaves better, safer, and more predictably.

### Key Feature: Objective Comparison

```bash
# Runs test suite with and without Vectora, generates structured diff
vectora harness run ./tests --compare vectora:on,vectora:off
```

Result:

```json
{
  "suite_score_delta": "+22%",
  "retrieval_precision_delta": "+31%",
  "token_usage_delta": "-18%",
  "security_violations": { "with_vectora": 0, "without_vectora": 3 },
  "failures": { "with_vectora": 1, "without_vectora": 7 }
}
```

### Test Types

| Type           | Validates                                        | YAML Example                                                        |
| -------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| **Tooling**    | Correct tool sequence, valid args      | `strict_sequence: [{tool: "file_read", args: {path: "auth.go"}}]`   |
| **Retrieval**  | Found the right files, ignored noise       | `must_include: ["auth.go"], must_exclude: ["unrelated/logger.go"]`  |
| **Reasoning**  | Correct answer, valid conclusion            | `semantic_checks: [{pattern: "expiration", case_sensitive: false}]` |
| **Safety**     | No secret leaks, no .env access            | `blocked_tools: ["terminal_run"], blocked_paths: [".env"]`          |
| **Resilience** | Recovers from failures (timeout, partial error) | `fault_injection: [{type: "timeout", tool: "file_read"}]`           |

> 💡 **This is a product weapon**: Objective proof that Vectora improves quality, reduces costs, and increases security.

---

## 🌐 Shared Namespaces: Asset Library

**Vectora Assets** is a catalog of shared namespaces with RBAC — not a traditional marketplace.

### Public Namespaces (Curated)

Available for instant mounting in any workspace:

| Namespace         | Content                                    | Usage                                               |
| ----------------- | ------------------------------------------- | ------------------------------------------------- |
| `godot-4.6-api`   | Official documentation + GDScript examples | "How to implement a state machine in Godot?"    |
| `typescript-docs` | Language specs + typing patterns     | "What is the difference between `unknown` and `any`?"       |
| `rust-patterns`   | Idioms, traits, and concurrency patterns   | "How to share state between threads in Rust?" |
| `web-security`    | OWASP Top 10, headers, CSP, authentication    | "Which security headers should I configure?"     |

### How to Use

```bash
# List available public namespaces
vectora assets list

# Mount a public namespace in the current workspace
vectora assets mount godot-4.6-api

# Unmount
vectora assets unmount godot-4.6-api

# Publish a namespace as public (requires approval)
vectora assets publish ./my-docs --namespace my-lib --visibility public
```

> [!IMPORTANT]
> **Privacy Policy**: `private` and `team` namespaces remain exclusively in your Qdrant/Supabase instance. **Not even Kaffyn has access to data contained in private or team workspaces.**

---

## 🚀 Quick Start

### Installation

```bash
# Install globally via npm
npm install -g vectora-agent

# Verify installation
vectora-agent --version
```

### Initial Configuration

```bash
# Configure provider (e.g., OpenRouter)
vectora-agent config --provider openrouter --key $OPENROUTER_KEY

# Configure cloud backend (optional, default comes pre-configured)
vectora-agent config --qdrant-url $QDRANT_URL --supabase-url $SUPABASE_URL

# Or activate local mode with llama.cpp
vectora-agent setup-local --model qwen3-1.7b-instruct
```

### Execution

```bash
# Start as MCP server (for Claude Code, Gemini CLI, etc)
vectora-agent mcp-serve

# Or start as ACP client for a specific project
vectora-agent acp-start --workspace ./my-project

# Use basic CLI for quick tasks
vectora-agent ask "Which functions depend on the authentication module?"
vectora-agent embed --path ./docs/
vectora-agent search "repository pattern"
```

### VS Code Integration

1. Install the **Vectora** extension from the marketplace
2. The extension already includes the Agent binary — no additional setup
3. Use the dedicated panel for interactive chat or invoke as a sub-agent via command

---

## 💰 Usage Models

### 🟢 Free (BYOK - Bring Your Own Keys)

- All tools and Context Engine included
- You provide your own API keys (OpenRouter, Gemini, etc.)
- Qdrant + Supabase: use your own instances or Kaffyn's free tier
- Full Harness for local validation
- **Cost**: $0 + your APIs

### 🔵 Pro (~$20/month)

- Managed Qdrant + Supabase by Kaffyn (multi-tenant, auto-scaling)
- Limited embeddings included (e.g., 100k tokens/month)
- Dashboard with usage tracking, billing, and API key management
- Priority support and early access to features
- **Ideal for**: Professional developers who want zero configuration

### 🟣 Team (Custom)

- Shared namespaces with granular RBAC
- Multiple users, isolation by project/team
- Audit logs, optional SSO, guaranteed SLA
- **Ideal for**: Engineering teams that need secure shared knowledge

---

## 📦 Project Structure (Monorepo)

```text
vectora/
├── packages/
│   ├── core/          # Agent runtime: protocols, tools, security, context engine
│   ├── llm/           # Providers: openai, gemini, claude, openrouter, llama.cpp
│   ├── context/       # Context Engine + multi-namespace + multi-hop RAG
│   ├── harness/       # Validation system: runner, judge, schema (Zod)
│   └── shared/        # Types, utils, config, logger, constants
│
├── apps/
│   ├── agent/         # Entry point: MCP/ACP server, CLI commands
│   └── web/           # Next.js: landing + dashboard + billing + auth
│
├── infra/
│   ├── qdrant/        # Collections config, quantization, payload indexes
│   ├── supabase/      # Migrations, RLS policies, auth/projects schema
│   └── vercel/        # Functions config, AI Gateway, edge settings
│
├── assets/            # Shared namespaces definitions (YAML)
│   ├── public/
│   │   ├── godot-4.6-api.yaml
│   │   ├── typescript-docs.yaml
│   │   └── rust-patterns.yaml
│   └── README.md      # How to publish a public namespace
│
├── tests/
│   ├── e2e/           # MCP/ACP integration tests
│   ├── harness-suites/# YAML test cases (security, retrieval, resilience)
│   └── fixtures/      # Small codebases for testing
│
├── package.json       # pnpm workspace + turbo
├── tsconfig.json      # Base config + paths aliases
└── README.md          # You are here
```

---

## 🤝 Contributing

Vectora is open source and built by the community. Contributions are welcome!

### Getting Started

```bash
# Clone the repo
git clone https://github.com/Kaffyn/Vectora.git
cd Vectora

# Install dependencies (pnpm + turbo)
pnpm install

# Run the agent in development mode
pnpm --filter agent dev

# Run Harness tests
pnpm --filter harness test
```

### Guidelines

- **Strict TypeScript**: No `any`, explicit types, Zod for validation boundaries
- **Tests first**: New tool? Write the Harness test before implementation
- **Security by default**: No features that bypass the Guardian or Trust Folder
- **Updated docs**: Changed the API? Update the schema and examples

### Public Roadmap

- [ ] Harness: LLM-as-a-Judge with judgment caching
- [ ] Context Engine: Multi-hop with hybrid ranking (semantic + structural)
- [ ] Assets: Community curation system for public namespaces
- [ ] IDEs: Native support for JetBrains via strict ACP
- [ ] Local: Otimizações para llama.cpp em Apple Silicon / NVIDIA CUDA

---

## ❓ FAQ

**Q: Is Vectora an autonomous agent?**  
A: No. Vectora is a specialist sub-agent for code context. You trigger it via MCP/ACP during development — it doesn't run 24/7 or make decisions without your command.

**Q: Do I need a Kaffyn account?**  
A: For Free mode (BYOK), no. For Pro/Team or to use public namespaces, yes — authentication via Supabase Auth.

**Q: Does my data go to the cloud?**  
A: Only if you configure the cloud backend. In local mode, everything runs on your machine. `private` namespaces never leave your instance, even in the cloud.

**Q: Can I use Vectora with Cursor / Copilot / Antigravity?**  
A: Yes! Via MCP, any compatible client can use Vectora as a sub-agent. For IDEs with native ACP (VS Code), the integration is even deeper.

**Q: What if the AI provider goes down?**  
A: The Agent has automatic failover. Configure a secondary provider and, in case of an error (429, timeout, outage), the request is transparently routed — your IDE won't notice the switch.

---

## 📄 License

Vectora is distributed under the **MIT** license. See [LICENSE](LICENSE) for details.

> 💡 **Quote to remember**:  
> _"Vectora doesn't compete with the agent. It makes any agent competent in code."_

---

_Part of the Kaffyn ecosystem · Open Source · TypeScript · Provider-Agnostic_
