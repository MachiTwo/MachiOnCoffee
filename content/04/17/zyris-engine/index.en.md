---
title: "Zyris Engine: Control, Performance, and Opinionated by Design"
date: "2026-04-17T19:00:00-03:00"
slug: zyris-engine
tags:
  - engine
  - gamedev
  - zyris
draft: false
---

Welcome to the **Zyris Engine**. This project is not just a fork of Godot; it is a statement of intent on how to
maintain a professional, stable, and scalable game architecture in the long run.

## An Opinionated Philosophy (Convention over Configuration)

While Godot Engine prizes maximum flexibility—often allowing projects to grow chaotically—Zyris adopts an
**"opinionated"** philosophy. We believe that developer time should be spent creating gameplay, not reinventing
fundamental systems.

In Zyris, we establish clear architectural standards. If you are building a professional project, the engine offers
predictable structures that facilitate teamwork and the maintenance of complex codebases.

## Core Engineering Features

Unlike conventional plugins, Zyris integrates critical functionalities directly into its C++ core:

### Save Server: Persistence Orchestrator

A robust and asynchronous persistence system integrated into the core.

- **Declarative Protocol**: Automation via `@persistent` in GDScript.
- **Threaded Architecture**: ZSTD compression and AES-256 encryption running on dedicated threads.
- **Incremental System**: Tracks modifications and applies surgical patches, reducing disk writing by up to 95%.

### Virtual Input Devices

Total input abstraction. The system automatically detects whether the player is on Touch, Keyboard, or Gamepad and
adapts the UI dynamically. Includes native nodes like `VirtualJoystick` and `VirtualDPad` integrated into Godot's
InputMap.

### Ability System (GAS)

A high-performance gameplay framework for RPGs and combat games. Based on `Resources` to be data-driven, it allows
designers to create complex abilities (Costs, Cooldowns, Effects) without touching code, with full processing in C++.

## The Production Ecosystem

Zyris expands the horizons of the base engine with systems designed for the "EndGame" of development:

### Inventory & Equipment System

Authoritative item management with an **Equipment Bridge** that automatically injects GAS abilities when equipping
items. Includes smart UI nodes and server-side validation to prevent cheating.

### Camera System (vCam)

Cinematic arbitration inspired by the Cinemachine standard. The `vCamServer` manages priorities between virtual cameras
and performs smooth transitions (blends), in addition to having a shake system (Procedural Shake) based on Perlin noise.

### Audio System Pro

Expansion of the native audio system with support for event-based and contextual audio. Introduces DSP per stream and
reactive mixing, where the game state directly influences the sound environment.

## Maturity Roadmap

Zyris continues to evolve with a focus on robustness:

- **Native Behavior Tree**: Modular and reactive AI with a dedicated visual editor and live debugging.
- **Multiplayer Update**: Layered replication (Network LOD) and native authoritative prediction.
- **Cloud Providers**: Polymorphic abstraction for Steam, Epic Online Services (EOS), and PlayFab.

Zyris is the choice for developers who understand that **freedom without structure is just technical debt.**

---

_Keep up with development on [Machi's](https://www.youtube.com/@machiatodev) and
[Alen's](https://www.youtube.com/@yatsuragames) channels._
