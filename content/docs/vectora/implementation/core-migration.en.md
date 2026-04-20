---
title: Core Migration
slug: core-migration
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - engineering
  - golang
  - migration
  - performance
---

{{< lang-toggle >}}
{{< section-toggle >}}

## Core Migration (TS to Go)

The transition of Vectora from **TypeScript (Node.js)** to **Golang** was not just a language swap, but a complete re-engineering to meet performance and native distribution requirements. This document details the technical motivations and structural changes.

### Why Golang?

| Factor           | TypeScript (Node.js)                | Golang                       | Impact on Vectora                         |
| :--------------- | :---------------------------------- | :--------------------------- | :---------------------------------------- |
| **Distribution** | Requires Node.js installed (+100MB) | Single Static Binary (~20MB) | Winget installation without dependencies. |
| **Concurrency**  | Event Loop (Single-threaded)        | Goroutines (Native/Parallel) | RAG processing 3x faster.                 |
| **Memory Usage** | High (V8 Garbage Collector)         | Low (Efficient Management)   | Smaller footprint on developer machines.  |
| **Security**     | Design-time typing                  | Compiled strong typing       | Fewer runtime errors in production.       |

### Core Structural Changes

#### 1. From Zod to Struct Tags

In the legacy version, we used **Zod** to validate schemas in real-time. In Go, we use native `structs` with validation tags (`validate:"required"`), which reduces parsing overhead and ensures the binary rejects malformed inputs before logical execution.

#### 2. Native Harness Runtime

The **Harness Runtime**, which previously relied on asynchronous bridges in Node, now operates directly on the OS file system and network. This allows [Guardian](../security-engine.md) interceptions to be performed at a simulated kernel-space level, increasing sandbox reliability.

#### 3. Concurrency in the Context Engine

The `Embed → Search → Rerank` pipeline is now orchestrated via Go's `Channels` and `Contexts`. While Node processed one chunk at a time, the Go engine fires multiple parallel requests to MongoDB Atlas and Voyage AI, reducing total MCP response latency.

### Migration Challenges

- **MCP Interoperability**: Maintaining compliance with the MCP protocol (JSON-RPC) while migrating from Node libraries to native Go implementations.
- **Binary Distribution**: Configuring the multi-platform build pipeline (Windows/macOS/Linux) to ensure identical sub-agent behavior across all OSs.

---

_Part of the Vectora ecosystem_ · Internal Engineering
