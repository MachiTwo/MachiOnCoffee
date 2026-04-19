---
title: Backend
slug: backend
date: "2026-04-18T22:30:00-03:00"
weight: 35
type: docs
sidebar:
  open: true
tags:
  - ai
  - backend
  - mcp
  - vectora
---

{{< lang-toggle >}}

## 🏗️ The Engine Behind Context

Vectora's backend infrastructure is designed to solve the biggest bottleneck for modern AI agents: **state management at scale**. While the Vectora runtime processes intelligence, the backend ensures that this intelligence is grounded in persistent, secure, and searchable data.

Vectora uses a unified architecture based on **MongoDB Atlas**, allowing vectors, metadata, and operational memory to coexist within the same ecosystem.

---

### 📋 Topics in this Section

| Page                                                   | Description                                                                             |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| [MongoDB Atlas](/backend/mongodb-atlas/)               | Why we chose Atlas and how it serves as our data foundation.                            |
| [Vector Search](/concepts/vector-search/)              | Technical deep dive into embeddings, cosine similarity, and the HNSW algorithm.         |
| [Persistence and Memory](/concepts/state-persistence/) | How Vectora maintains state between sessions and builds long-term memory (`AGENTS.md`). |

---

### 🧭 Architecture Overview

Vectora's backend is not just a storage location; it is an extension of the **Harness Runtime**.

```mermaid
graph TD
    A[Vectora Runtime] --> B{Service Layer}
    B --> C[Vector Service]
    B --> D[Session Service]
    B --> E[Audit Service]

    subgraph "MongoDB Atlas (Managed by Kaffyn)"
        C --> F[(Documents & Vectors)]
        D --> G[(Operational State)]
        E --> H[(Audit Logs)]
    end
```

---

### 🛡️ Backend Principles

1. **Namespace Isolation (RBAC)**: The backend enforces strict boundaries. Data from one project never mixes with others, ensuring multi-tenant privacy.
2. **Atomicity**: Code vectors and metadata are stored together. If a file is updated, the vector index and the document are updated simultaneously.
3. **Transparent Scalability**: Using MongoDB Atlas, Vectora scales from small individual projects to enterprise codebases with millions of lines of code without performance loss.
4. **Active Governance**: Every interaction is persisted and auditable, allowing full transparency over AI actions.

---

### 🔄 Backend Modes

| Mode                    | Description                                                                           | Ideal Use                                  |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| **Managed (SaaS)**      | MongoDB Atlas backend provisioned by Kaffyn. Zero configuration.                      | Free, Pro, and Team plans.                 |
| **Hybrid (BYOK)**       | You provide [Voyage](/concepts/embeddings/) API keys, but Atlas is managed by Kaffyn. | API cost control with easy infrastructure. |
| **Enterprise / Custom** | Connection to your own MongoDB Atlas cluster or on-premise infrastructure.            | Strict data sovereignty requirements.      |

---

### ❓ Frequently Asked Questions

**Q: Where are my vectors physically stored?**  
R: In MongoDB Atlas clusters managed by Kaffyn, typically located in low-latency AWS or Google Cloud regions.

**Q: Is my backend data used to train Kaffyn's models?**  
R: **No.** We follow a strict privacy policy. Your vectors and metadata are your exclusive property and used only to provide context to your agent.

**Q: Is the backend required for offline mode?**  
R: Vectora allows local caching of some metadata, but full semantic vector search and long-term persistent memory depend on backend connectivity.

---

> 💡 **Phrase to remember**:  
> _"The runtime is the brain; the backend is the library. Without an organized library, the brain has nowhere to look for answers."_
