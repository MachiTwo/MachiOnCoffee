---
title: "State Persistence and Memory"
weight: 78
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}

## The Problem: Stateless Agents

Most AI tools operate on a _stateless_ model: every question is a new blank slate. For code applications, this is disastrous. If the agent forgets that you've already explained that the database port has changed, or that it shouldn't touch the `src/legacy` folder, it will commit the same errors repeatedly.

Vectora solves this through a system of **State Persistence and Operational Memory**.

---

## Short-Term vs. Long-Term Memory

In Vectora, persistence is divided into layers to optimize performance and token costs:

### 1. Operational Memory (Short-Term)

Resides in the `sessions` collection of MongoDB Atlas.

- **Duration**: Current MCP session (active while the principal agent is running).
- **Content**: History of tool calls, temporary execution plans, and recent tool outputs.
- **Usage**: Ensures that if the agent listed files in one step, it doesn't need to list them again in the next step of the same task.

### 2. Persistent Memory (Long-Term/AGENTS)

Resides in the `memory` collection and can be mirrored in an `AGENTS.md` file (optional).

- **Duration**: Lifetime for the namespace.
- **Content**: Learned facts ("The project uses Clean Architecture"), security rules ("Never edit .pem files"), and user preferences ("Prefer using `async/await` over callbacks").
- **Usage**: Provides the project "DNA" to the agent as soon as it is initialized.

---

## How Persistence Works

### Operation via MongoDB Atlas

When the principal agent sends a request via MCP, Vectora:

1. **Retrieves State**: Reads the active session from Atlas.
2. **Injects Memory Context**: Loads relevant rules from the persisted `AGENTS.md`.
3. **Updates in Real-Time**: Every decision made by the [Context Engine](/concepts/context-engine/) is recorded in the database.

---

## Audit and Governance

Backend persistence isn't just for the AI; it's for the developer.

### Audit Logs (`audit_logs` Collection)

Vectora records immutable metadata for every operation:

- **Timestamp**: Exact millisecond.
- **Identity**: Which API Key or user executed the operation.
- **Tool**: `file_edit`, `context_search`, etc.
- **Status**: Success or Error (including Harness error logs).

This allows security teams and technical leads to audit **exactly** what agents are doing in the codebase.

---

## Isolation and Encryption (RBAC)

State persistence is strictly isolated by **Namespace**.

- An agent running in `namespace: front-end` will never see the memory or session state of `namespace: back-end`.
- Sensitive data in the state (such as code snippets in memory) are encrypted at rest in MongoDB Atlas (AES-256).

---

## Optimization: Session Compaction

Agent sessions can become immense, exceeding the LLM's context limit. Vectora applies **Compaction** on the backend:

- **Pruning**: Removes details of tools that failed or were overwritten by successful actions.
- **Summarization**: Summarizes intermediate thought blocks, keeping only conclusions and critical facts.
- **Head/Tail management**: Maintains the beginning (objective) and current state (tail) in detail, compacting the middle.

---

## Persistence FAQ

**Q: Where is the `AGENTS.md` file saved?**
A: It is stored persistently in MongoDB Atlas. You can also enable synchronization to a physical file in your project root so it can be versioned in Git.

**Q: Can I clear the agent's memory?**
A: Yes. You can reset a specific session via `vectora session reset --id <session_id>` or clear the namespace's persistent memory via the dashboard.

**Q: How does Vectora prevent the agent's memory from being "polluted" with wrong information?**
A: Through the **Verification Hooks** of the [Harness](/concepts/harness/). If an operation fails or the output is considered irrelevant, the Harness prevents that fact from being consolidated in persistent memory.

---

> **Phrase to remember**:
> _"Intelligence without memory is just a calculation. With Vectora's persistence, your agent gains experience."_
