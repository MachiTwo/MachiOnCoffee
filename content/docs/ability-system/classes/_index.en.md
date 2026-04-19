---
title: "Classes"
date: "2026-04-18T22:30:00-03:00"
slug: classes
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

Welcome to the **Ability System** technical reference. This section contains detailed information about all classes, structures, and utilities available in the framework.

## Technical Categories

### [Singleton](singleton/)

The global entry point for the system. Manages tag registration and runtime component resolution.

### [Resources](resources/)

Blueprints and Data Definitions. Here you define the "DNA" of abilities, effects, and attributes (Godot Resources).

### [Nodes](nodes/)

Scene components. The building blocks you attach to your characters and objects in the editor.

### [RefCounted](refcounted/)

Lightweight runtime instances. Objects that manage mutable state during gameplay (Specs and Utilities).

### [Behavior Tree](behavior-tree/)

Integrated AI nodes. Tasks and conditions for LimboAI that allow agents to use the system naturally.

### [Editor](editor/)

Godot editor extensions. Tools that facilitate the designer's daily life.

---

To get started, we recommend reading the main class: [**AbilitySystem (Singleton)**](singleton/ability-system).
