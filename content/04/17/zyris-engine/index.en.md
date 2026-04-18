---
title: "Zyris Engine: Control, Performance, and Opinionated by Design"
date: "2026-04-17T16:00:00-03:00"
slug: zyris-engine
tags:
  - engine
  - gamedev
  - zyris
draft: false
---

Hello world! Today I want to introduce the **Zyris Engine**, a project born from the need for **structural control, predictability, and scalability** in professional game development.

## What is Zyris?

**Zyris** is a **fork of the Godot Engine**. This means it maintains full compatibility with the Godot base—your projects, your GDScript knowledge, and your workflow remain familiar.

However, Zyris has its own **governance and roadmap**. We do not blindly apply Godot updates; every change from the "upstream" is analyzed, filtered, and integrated in a controlled manner to ensure long-term stability.

## An Opinionated Philosophy

Unlike engines that offer absolute freedom and can eventually lead to chaotic codebases, Zyris is **intentionally opinionated**. We believe that clear conventions reduce the need to reinvent fundamental solutions in every project.

You still have total freedom, but by default, Zyris offers:
- **Predictable structures** for complex systems.
- **Deterministic state management**.
- **Consistent architectural foundation** for AI and gameplay.

## Features Already Implemented

Currently, the engine already features robust systems integrated into its core:

- **Virtual Input Devices**: A multi-platform input abstraction layer (Joysticks, D-Pads) integrated directly into the core.
- **Save Server**: A high-performance persistence orchestrator with **ZSTD** compression and **AES-256** encryption, running on dedicated threads to ensure fluid *autosaves*.

## The Future: Ability System and Beyond

We are working on the native integration of the [**Ability System**](../ability-system/), a data-driven gameplay framework for scaling combat mechanics.

Our development roadmap also includes:
- **Behavior Tree**: Modular and reactive node-based AI.
- **Inventory System**: Authoritative item and equipment management.
- **Camera System (vCam)**: Cinematic arbitration for smooth transitions.
- **AOT Export System**: Native binary generation for maximum performance without VM overhead.

Zyris is focused on those seeking **technical maturity** and longevity for their projects.

---
*Follow official development on [Machi](https://www.youtube.com/@machiatodev) and [Alen](https://www.youtube.com/@yatsuragames)'s channels.*
