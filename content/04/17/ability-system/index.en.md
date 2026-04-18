---
title: "Ability System: The Heart of Gameplay Mechanics in Zyris"
date: "2026-04-17T17:00:00-03:00"
slug: ability-system
tags:
  - gamedev
  - gameplay-system
  - zyris
draft: false
---

The **Ability System (AS)** is the backbone of combat gameplay. More than just managing abilities, it offers a data-driven framework to orchestrate complex states with **high C++ performance**.

## Data-Driven Paradigm

The great revolution of AS is moving gameplay logic from source code into the **Godot Editor**. Using resources (`.tres`), designers can configure complex behaviors without recompilation.
- **ASAbitilies**: Define the "action"—costs, cooldowns, and requirements.
- **ASEffects**: Manage attribute modification over time (Damage over time, Attribute buffs).
- **ASContainers**: Function as archetypes that connect multiple effects and abilities to a character.

## Tag Hierarchy: The Language of State

The system uses a strict vocabulary of **Hierarchical Tags** for communication between decoupled systems:
- **$NAME**: Defines the unique identity of a gameplay element.
- **$CONDITIONAL**: Represents persistent and logical states (e.g., `IsStunned`, `IsReloading`).
- **$EVENT**: Instant triggers that fire reactions (e.g., `OnDamageTaken`, `OnJump`).

## Phase Logic and Gameplay Flow

An ability in AS is not just a "trigger." It is divided into native stages that allow fine-tuned control of the experience:
1. **Windup**: Preparation time (telegraphy).
2. **Execution**: When the main logic and *hitbox* are activated.
3. **Recovery**: The necessary action cooldown after use.

## Network Engineering: Native Rollback

Developed with multiplayer in mind, the **Ability System** utilizes **circular state buffers**. This allows the system to support **Rollback Networking**, where the client can predict the game state and the server can reconcile prediction errors by going back in time and re-executing logic deterministically.

## Dual Build Integration

To ensure no one is left behind, we maintain two ways of usage:
- **Zyris Native**: Maximum integration with the engine's core tools.
- **GDExtension**: Stable plugin for any official Godot 4.x project, bringing the power of C++ to GDScript developers.

---
*Developed with ❤️ by **MachiTwo**.*
