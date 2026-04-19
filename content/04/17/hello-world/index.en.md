---
title: "Hello World!"
date: "2026-04-17T15:00:00-03:00"
slug: hello-world
tags:
  - introduction
  - personal
  - journey
draft: false
---

{{< lang-toggle >}}

Hello world! I'm Bruno, and I decided this blog would be more than just a diary; it would be the safe harbor for the
documentation and evolution of the systems I've been building. My journey started in 2020 with Java, moved through
GameMaker, and consolidated in the Godot Engine, but today my focus lies at the intersection of **Engine Engineering**
and **AI Agents**.

Below, I detail the three pillars that define my current work:

### 1. Zyris Engine: The Next Level of Godot

**Zyris** is not just a fork; it's an **opinionated** vision of what professional game development should be. While
Godot prizes absolute freedom, Zyris focuses on **stability and convention**.

- **Core Architecture**: We implemented a native C++ **Save Server** that uses **ZSTD** compression and **AES-256**
  encryption on dedicated threads, ensuring gameplay never suffers from stutter during data persistence.
- **Input System**: **Virtual Input Devices** abstracts the complexity of multi-platform mapping directly in the core,
  offering a deterministic translation layer for Joysticks and D-Pads.
- [**Read more about Zyris Engine here**](../zyris-engine/)

### 2. Ability System: Data-Driven Gameplay

Born as a module for Zyris, the **Ability System (AS)** is a high-performance gameplay framework that scales from
micro-projects to massive RPGs.

- **Dual Build**: Available both natively in Zyris and via **GDExtension** for the official Godot 4.x.
- **Hierarchical Tags**: We use a rigorous Tag system (`NAME`, `CONDITIONAL`, `EVENT`) to orchestrate combat states
  without "spaghetti" code.
- **Phase Logic**: Native support for ability phases (Windup, Execution, Recovery) and circular buffers ready for
  **Multiplayer with Rollback**.
- [**Explore the Ability System in detail**](docs/ability-system/)

### 3. Vectora: The Contextual Knowledge Engine

**Vectora** is my most ambitious project in the AI field. It's not a generic "chat"; it's a **Specialist Sub-Agent
(Tier 2)** designed to connect your code's context to primary agents (like Claude Code or Gemini CLI).

- **Runtime**: Built in **TypeScript/Node.js 20+**, integrating **MCP** and **ACP** protocols.
- **Context Engine**: Unlike traditional RAG, Vectora performs **multi-hop reasoning** and structural analysis (via
  **Tree-sitter**) to understand how functions and dependencies connect globally.
- **Harness Validation**: We created **Vectora Harness**, an objective metrics system that proves (through precision
  scores and token efficiency) how the delivered context improves AI performance.
- **Security**: The **Hard-Coded Guardian** protects secrets (.env, .keys) directly in the runtime, ensuring sensitive
  data never leaves your environment.
- [**Understand Vectora's architecture**](docs/vectora/)

---

All of this happens while I balance development with my reality outside the screens. I've been a shop clerk, a waiter,
and today I work in a bakery. This duality between "dough and code" is what keeps my feet on the ground and my head
focused on creating tools that truly solve real engineering problems.

This blog is the start of this new phase of technical publication. Welcome to MachiOnCoffee.
