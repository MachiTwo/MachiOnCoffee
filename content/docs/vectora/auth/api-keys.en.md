---
title: API Keys
slug: api-keys
date: "2026-04-18T22:30:00-03:00"
weight: 67
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

## 🔑 Vectora API Keys

API Keys are programmatic credentials that enable secure, scoped access to the Vectora backend without interactive authentication. They are designed for machine-to-machine communication, CI/CD pipelines, custom agent integrations, and direct HTTP/REST access to your indexed namespaces.

> [!IMPORTANT]
> API Keys are **only available on Pro, Team, and Enterprise plans**. Free/Local users authenticate via `vectora auth login` (interactive JWT).

---

### 🧩 Key Capabilities

| Feature                | Description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| **Granular Scopes**    | `read`, `write`, `search`, `admin` — assign minimum privilege required   |
| **Rate Limiting**      | Configurable requests/minute per key to prevent quota exhaustion         |
| **Auto-Rotation**      | Seamless key rollover with overlap period (zero downtime during updates) |
| **Instant Revocation** | Immediate invalidation across all Vectora nodes via dashboard or CLI     |
| **Secure Storage**     | Keys are stored as cryptographic hashes (bcrypt) — never in plaintext    |

---

### 📋 Available Scopes & Permissions

| Scope    | Allowed Operations                                         | Typical Use Case                                             |
| -------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `search` | `context_search`, `context_build`, namespace read-only     | RAG agents, documentation bots, read-only analytics          |
| `read`   | `file_read`, `file_list`, `file_find`, `context_search`    | Code navigation tools, static analysis, audit scripts        |
| `write`  | `file_write`, `file_edit`, `context_ingest`, `memory_save` | CI/CD indexing bots, automated refactoring agents            |
| `admin`  | Full namespace management, key rotation, quota override    | Platform automation, team management, infrastructure scripts |

> [!WARNING]
> API Keys operate **outside the interactive SSO session**. They are bound to a specific namespace and plan quota. Exceeding quota triggers fallback to your configured [BYOK credentials](/providers/gemini/) or returns `429 Too Many Requests`.

---

### 🔌 Integration Examples

#### 1. MCP Server Configuration

Pass the API key via environment variables when starting the Vectora MCP server:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "npx",
      "args": ["@kaffyn/vectora", "mcp-serve"],
      "env": {
        "VECTORA_API_KEY": "vca_live_xxxxxxxxxxxxxxxxxxxxxxxx",
        "VECTORA_NAMESPACE": "my-team-auth-service",
        "VECTORA_SCOPE": "search"
      }
    }
  }
}
```

#### 2. Direct HTTP/REST Access

Authenticate via `Authorization` header for custom tooling:

```bash
curl -X POST "https://api.vectora.dev/v1/search" \
  -H "Authorization: Bearer vca_live_xxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "JWT validation middleware", "namespace": "my-project", "top_k": 5}'
```

#### 3. Programmatic Usage (TypeScript)

```ts
import { VectoraClient } from "@vectora/sdk";

const client = new VectoraClient({
  apiKey: process.env.VECTORA_API_KEY!,
  namespace: "ci-pipeline-indexer",
  scope: "write",
});

// Ingest codebase on push
await client.context.ingest("./src");
```

---

### 🛡️ Security Best Practices

✅ **Principle of Least Privilege**: Use `search` for read-only agents, `write` only for automated indexing pipelines.  
✅ **Environment Injection**: Never hardcode keys. Use `.env`, CI/CD secrets, or cloud KMS.  
✅ **Rotation Policy**: Rotate keys every 90 days or immediately after a security incident.  
✅ **Audit Logging**: All API key usage is logged in your [Audit Trail](/security/rbac/) with timestamp, IP, and executed tool.  
✅ **Scope Validation**: Vectora enforces scope at the [Guardian](/security/guardian/) layer — keys cannot bypass hard-coded blocklists.

> [!TIP]
> Combine API Keys with [SSO](/auth/sso/) for human users and [Trust Folders](/security/trust-folder/) for filesystem isolation. API Keys grant logical access; security policies enforce runtime boundaries.

---

### 🔄 Key Management Lifecycle

| Action     | Dashboard                         | CLI                                                     |
| ---------- | --------------------------------- | ------------------------------------------------------- | --- |
| Create Key | `Settings → API Keys → New`       | `vectora api-key create --scope search --name "ci-bot"` |
| Revoke Key | `Revoke` button (immediate)       | `vectora api-key revoke --id vca_live_...`              |
| Rotate Key | `Rotate` (creates overlap window) | `vectora api-key rotate --id vca_live_...`              |
| View Usage | Quota usage meter + history       | `vectora api-key usage --id vca_live_...`               |     |

**Overlap Period Explained**: When rotating, the old key remains valid for a configurable window (default: 2h). Both keys count against your quota. This prevents downtime during CI/CD or agent deployments.

---

### ❓ Frequently Asked Questions

**Q: Can I share an API Key across multiple namespaces?**  
A: No. Each key is strictly bound to a single namespace at creation. Cross-namespace access requires multiple keys or [Team/Enterprise RBAC](/plans/team/).

**Q: What happens if my key is compromised?**  
A: Revoke it immediately via dashboard or CLI. All active sessions using that key are terminated within seconds. Audit logs capture the last usage for forensic analysis.

**Q: Do API Keys bypass the Guardian blocklist?**  
A: Absolutely not. [Guardian](/security/guardian/) validation runs at the application layer before any tool execution, regardless of authentication method. `.env`, `.key`, and `node_modules/` remain inaccessible.

**Q: Can I use API Keys with my own LLM provider?**  
A: Yes. API Keys authenticate you to the Vectora backend. LLM/embedding quotas are managed separately via [BYOK configuration](/providers/gemini/) or managed plan limits.

**Q: Is there a rate limit?**  
A: Default: 100 req/min for `search`, 20 req/min for `write`. Custom limits available on Team/Enterprise plans.

---

> 💡 **Phrase to remember**:  
> _"API Keys open the door. Scopes define the room. Guardian locks the vault."_

_Part of Vectora Auth · Available on Pro, Team & Enterprise_  
_Security: Hashed storage, scope enforcement, instant revocation_  
_Next: [SSO & Identity](/auth/sso/) · Previous: [Trust Folder](/security/trust-folder/)_
