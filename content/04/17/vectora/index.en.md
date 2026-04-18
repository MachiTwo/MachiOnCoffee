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

Traditional AI agents often hallucinate because they operate in fragmented contexts. **Vectora** solves this not by being "just another chat," but as a **Contextual Knowledge Engine** that functions as a **Sub-Agent Tier 2**.

![Vectora Logo](/images/vectora.svg)

## Positioning: From RAG to Connected Knowledge

Unlike traditional RAG (Retrieval-Augmented Generation) that only searches for isolated text fragments, Vectora understands the **systemic structure** of your code.

It doesn't compete with agents like Claude Code, Gemini CLI, or Cursor; it **empowers** them. Vectora acts as an intermediate intelligence layer that delivers structured context via open protocols (**MCP** and **ACP**).

## Technical Architecture: Reliability in TypeScript

The Vectora runtime was developed in **TypeScript (Node.js 20+)**, utilizing **Vercel's AI SDK** to ensure stable and provider-agnostic model routing (OpenRouter, Google, Anthropic, OpenAI).

### Core Components:
- **Context Engine**: Performs **multi-hop reasoning** and structural analysis via **AST (Tree-sitter)**. It doesn't just search for words; it follows dependencies, imports, and execution flows to build a graph of your codebase.
- **Cloud & Local Native**: Integration with **Qdrant Cloud** for scalable vector search (using HNSW and scalar quantization) and optional support for 100% local inference via **llama.cpp**.
- **Infrastructure**: Metadata and authentication backend via **Supabase**, with API layers running on **Vercel Edge Functions**.

## Objective Validation: Vectora Harness

How do you know if the AI actually improved? We created **Vectora Harness**, the "central nervous system" of our agent. It allows for:
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
*Vectora is part of the Kaffyn ecosystem · Open Source · TypeScript · Provider-Agnostic.*
