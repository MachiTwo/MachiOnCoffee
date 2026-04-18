---
title: "Ability System"
date: "2026-04-17T18:00:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

The **Zyris Ability System** is a robust gameplay framework designed to manage abilities, attributes, and states (Tags)
in a professional and scalable way. Inspired by Unreal's _Gameplay Ability System (GAS)_ but optimized for the **Zyris
Engine** and **Godot**, it rejects "Vibe-Coding" in favor of rigorous engineering contracts.

## 🛡️ The Governance Contract

Unlike ability systems based on loose scripts, our framework operates under an **Iron Law**:

- **SSOT (Single Source of Truth)**: The actor's state is defined exclusively by its **Tags**.
- **Total Decoupling**: The Component (ASC) does not know the internal logic of abilities (Specs); it only orchestrates
  their execution.
- **Technical Rigor**: No business logic exists without a test that justifies it (TDD Protocol).

## 🏗️ System Structure

Documentation is divided into fundamental pillars:

- [**Core (The Heart)**](./core/) - Components, Containers, and the Singleton.
- [**Mechanics (The Logic)**](./mechanics/) - How to create Abilities, Effects, and Attributes.
- [**Infrastructure (The Network)**](./infrastructure/) - System of Tags, Cues, and Business Rules.
- [**Integration (AI)**](./integration/) - How to connect with LimboAI via ASBridge.

---

### Where to start?

If you are new to the system, we recommend reading about the [**Identity Matrix: Tags**](./infrastructure/tags/) first,
which is the foundation of all game logic flow.
