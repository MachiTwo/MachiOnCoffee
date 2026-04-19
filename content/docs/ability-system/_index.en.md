---
title: "Ability System"
date: "2026-04-18T22:30:00-03:00"
slug: ability-system
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - gameplay-framework
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

The **Ability System (AS)** is a powerful and modular framework for creating combat, abilities, and attributes in Godot 4.x. Designed to scale from simple mechanics to complex RPG systems — all with high performance in C++ and data-driven architecture (v0.1.0 Stable).

## Architectural Principles

- **SSOT (Single Source of Truth)**: Actor state = its **Tags** (hierarchical identifier)
- **Total Decoupling**: ASComponent orchestrates without knowing internal logic of Specs
- **Type-Safety**: Globally registered tags prevent typos (editor autocomplete)
- **Determinism**: Native multiplayer with client prediction and automatic rollback
- **Performance**: Flyweight pattern—actors share immutable blueprints

## 3 Architectural Pillars

### 1. **Tags** — The Matrix of Identity

Hierarchical identifiers (`StringName`) representing the absolute truth of state.

### 2. **Blueprints** — The Immutable "DNA"

Static resources (`.tres`) shared across instances (ASAbility, ASEffect, etc).

### 3. **Specs** — Runtime Instances

Lightweight, dynamic, maintaining mutable state (Cooldowns, Stacks, Duration).

---

## Class Reference (API)

Explore the complete technical documentation organized by category:

- [**Singleton**](classes/singleton/) — Global registry and central resolver.
- [**Resources**](classes/resources/) — Abilities, Effects, and Immutable Blueprints.
- [**Nodes**](classes/nodes/) — Scene components (ASComponent, ASDelivery).
- [**RefCounted**](classes/refcounted/) — Runtime executors and state utilities.
- [**Behavior Tree**](classes/behavior-tree/) — Native integration with LimboAI.
- [**Editor**](classes/editor/) — Tag panels and custom inspectors.

---

## Tutorials and Examples

Learn in practice how to implement the system:

- [**Tutorials**](tutorials/) — Step-by-step for common mechanics.
- [**Examples**](examples/) — Reference projects and design patterns.

---

## Project Status

v0.1.0 Stable | Godot 4.6+ | Dual-Build (GDExtension/Module) | Developed with by MachiTwo
