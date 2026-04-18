---
title: "Vectora: The Sub-Agent Connecting Your Code's Context"
date: "2026-04-17T18:00:00-03:00"
slug: vectora
tags:
  - ai
  - productivity
  - tools
draft: false
---

<div class="hx:flex hx:justify-center hx:my-8">
  <img src="/images/vectora.svg" alt="Vectora Logo" class="hx:max-w-md hx:w-full hx:rounded-2xl hx:shadow-2xl hx:border hx:border-gray-200 hx:dark:border-gray-800">
</div>

## The Problem: Fragmented Context

Most agents today (Claude Code, Cursor, GitHub Copilot) suffer from the same issue: they view code as isolated snippets
of text. They don't understand the **dependency tree**, past architectural decisions (ADRs), or the intent behind a
module.

Vectora was born to be the intelligence layer that connects these dots, delivering what we call **Connected Knowledge**.

## 🏗️ EndGame Architecture

Vectora is not just a script; it's an ecosystem designed for low latency and high precision:

- **MCP & ACP Protocols**: Integration via [Model Context Protocol (MCP)](/en/04/17/sub-agents-mcp/) for agents like
  Claude and Antigravity, and ACP for ultra-fast communication with IDEs.
- **Context Engine**: The "brain" that decides _what_, _how_, and _when_ to fetch information, avoiding the noise that
  consumes your tokens.
- **Vector DB (Qdrant Cloud)**: Uses vector search with [HNSW and Quantization](/en/04/17/embeddings-vector-db/) to find
  functional similarities in milliseconds.
- **Proven Reranker**: A [Reranking](/en/04/17/reranker-contexto/) layer that reorders results to ensure the most
  relevant code is at the top.

## 🔐 Security by Design: The Guardian

Security in AI agents cannot just be "system prompts" (which are easily bypassed). In Vectora, security is
**hard-coded**:

1. **Hard-Coded Guardian**: An immutable blocklist compiled into the binary that prevents access to sensitive files
   (`.env`, `.key`, `.pem`, binaries) regardless of what the user or agent asks for.
2. **Namespaces with RBAC**: Real isolation between projects. Your data from one project never leaks to another, and
   public namespaces can be mounted as ready-to-use "skills".
3. **Trust Folder**: The agent only operates within directories explicitly authorized by you.

## 🧪 Vectora Harness: Objective Proof

How do you know if the agent is actually improving? The **Vectora Harness** is our objective validation system. It
allows you to run comparative tests: `vectora harness run --compare vectora:on,off`

This generates real metrics for precision gain, token reduction, and prevention of security violations. It's not
intuition; it's quantitative evidence.

---

### Want to dive deeper into the tech?

Explore our core technical guides:

- [What is RAG and why does connected context matter?](/en/04/17/rag-conectado/)
- [Embeddings and Vector DBs: The heart of semantic search](/en/04/17/embeddings-vector-db/)
- [Reranker: Why similarity isn't enough for code](/en/04/17/reranker-contexto/)
- [Sub-Agents vs MCP: Passive tools vs Active governance](/en/04/17/sub-agents-mcp/)

The Vectora runtime was developed in **TypeScript (Node.js 20+)**, utilizing **Vercel's AI SDK** to ensure stable and
provider-agnostic model routing (OpenRouter, Google, Anthropic, OpenAI).

### Core Components

- **Context Engine**: Performs **multi-hop reasoning** and structural analysis via **AST (Tree-sitter)**. It doesn't
  just search for words; it follows dependencies, imports, and execution flows to build a graph of your codebase.
- **Cloud & Local Native**: Integration with **Qdrant Cloud** for scalable vector search (using HNSW and scalar
  quantization) and optional support for 100% local inference via **llama.cpp**.
- **Infrastructure**: Metadata and authentication backend via **Supabase**, with API layers running on **Vercel Edge
  Functions**.

## Objective Validation: Vectora Harness

How do you know if the AI actually improved? We created **Vectora Harness**, the "central nervous system" of our agent.
It allows for:

1. **Measuring Accuracy**: Objectively compares AI output with `vectora:on` vs `vectora:off`.
2. **Token Efficiency**: Optimizes retrieval to avoid context "overfetch," reducing costs and latency.
3. **Auditability**: Generates structured reports on how the agent used each tool to reach an answer.

## Security: Hard-Coded Guardian

AI security cannot rely solely on prompts. Vectora implements the **Guardian**, an immutable code-level middleware that:

- **Blocks Sensitive Paths**: Files like `.env`, `.key`, `.pem`, and lockfiles are never read or embedded.
- **Output Sanitization**: Native regex masks secrets and PATs before they leave your environment.
- **Git Snapshots**: Automatic atomic commits before any write operation, ensuring total reversibility.

Vectora is the trust layer that was missing to make AI-assisted development professional, secure, and measurable.

---

_Vectora is part of the Kaffyn ecosystem · Open Source · TypeScript · Provider-Agnostic._
