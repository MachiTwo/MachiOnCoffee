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

Welcome to the **Zyris Engine**. This project is not just a fork of Godot; it is a statement of intent on how to maintain a professional, stable, and scalable game architecture in the long term.

## An Opinionated Philosophy (Convention over Configuration)

While the Godot Engine prizes maximum flexibility—often allowing projects to grow chaotically—Zyris adopts an **"opinionated"** philosophy. We believe that developer time should be spent creating gameplay, not reinventing fundamental systems.

In Zyris, we establish clear architectural standards. If you are building a professional project, the engine expects certain structures, which facilitates teamwork and the maintenance of legacy codebases.

## Core Engineering (Core Features)

Unlike conventional plugins, Zyris integrates critical functionality directly into its C++ core:

### Deterministic Save Server
We implemented a high-performance persistence subsystem that operates on dedicated threads.
- **Performance**: Zero blocking of the main gameplay loop.
- **Compression**: Uses state-of-the-art **ZSTD** algorithms to drastically reduce file sizes.
- **Security**: Native **AES-256** encryption integrated into the write flow.

### Virtual Input Devices
An abstraction layer that allows treating physical inputs from any platform (Joysticks, D-Pads, Touch) as consistent virtual events. This removes the need for repetitive, complex mappings in every new project.

### AOT Export System
We are developing an **Ahead-of-Time (AOT)** export system that generates native binaries optimized for each target platform, removing virtual machine overhead and ensuring maximum performance on hardware-limited devices.

## The Maturity Roadmap

Zyris evolves with a focus on production tools:
- **Integrated Behavior Tree**: Reactive AI flows via native node graphs.
- **Camera System (vCam)**: Cinematic camera arbitration inspired by industry standards (Cinemachine).
- **Authoritative Inventory System**: Item management integrated into the core with native network support.

Zyris is the choice for developers who understand that **freedom without structure is just technical debt.**

---
*Stay informed about development on [Machi](https://www.youtube.com/@machiatodev) and [Alen](https://www.youtube.com/@yatsuragames)'s channels.*
