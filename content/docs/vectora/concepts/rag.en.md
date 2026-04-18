---
title: "Connected RAG: Why isolated context kills your productivity"
date: 2026-04-17T21:00:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["rag", "infra", "ai", "vectora"]
---

Have you ever asked an AI agent about a function in your project, and it replied with something that looked right but
completely ignored how that function was used in the rest of the system? This is the classic symptom of **fragmented
RAG**.

## What is RAG?

**RAG (Retrieval-Augmented Generation)** is the technique of providing external data (like your code files) to an LLM at
the time of the query. Instead of the model "guessing" based on what it learned during training, it consults your
documents and answers based on them.

Sounds perfect, right? But for code, common RAG is dangerous.

## The Problem with Traditional RAG

Most vector databases focus on **semantic similarity of isolated chunks**.

If you search for `login`, it will give you code blocks containing the word `login`. But it might ignore the
authentication middleware, the database configuration file, or the dependency that manages JWT tokens.

For the LLM, it's like trying to build a puzzle while only receiving 5 random pieces and without the box to see the full
picture.

## The Solution: Connected RAG (Context Engine)

In [Vectora](/en/04/17/vectora/), RAG is not just "text search." It works through a **Context Engine** that understands
structure:

1. **Multimodal Search**: Combines vector search (semantic) with structural search (AST and Grep).
2. **Multi-hop Reasoning**: The context engine doesn't just do one search. If it finds a reference to an interface, it
   "jumps" to fetch the implementation of that interface.
3. **Structured Composition**: The context delivered to the primary Agent is not a list of texts, but an organized tree
   of files, dependencies, and metadata.

## Why does it matter?

When context is **connected**:

- Hallucinations drop drastically.
- The Agent stops suggesting changes that break other parts of the system.
- You spend fewer tokens, as the context sent is surgical, not a "dump" of files.

Traditional RAG gives you data. Vectora's Connected RAG gives you **knowledge**.

---

_This is a supporting post for the [Vectora](/en/docs/vectora/) project._
