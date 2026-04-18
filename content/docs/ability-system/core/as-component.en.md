---
title: "ASComponent: The Central Hub"
type: docs
weight: 1
---

{{< lang-toggle >}}

The **ASComponent** (ASC) is the brain of the ability system within your scene. It is the orchestrator that connects
Attributes, Tags, and Abilities to an Actor.

## 🧠 Role and Responsibility

The ASC does not contain the logic for "how" a sword cuts; it contains the list of "which" abilities this character can
use and manages their state.

- **Collection Manager**: Maintains the list of `active_specs` (active) and `unlocked_specs` (known).
- **State Owner**: The only one that can permanently add/remove tags.
- **Attribute Authority**: Contains the `ASAttributeSet` and processes all status modifications.

---

## 🛰️ Networking: Prediction and Rollback

The ASC was built from the ground up for authoritative multiplayer:

### ASStateCache

Maintains a lightweight circular buffer of the last **128 ticks**.

- **Prediction**: The client executes the ability locally and buffers the result.
- **Rollback**: If the server disagrees with a tick's result, the ASC reverts its entire state via `ASStateSnapshot` and
  re-simulates necessary frames.

---

## 🛠️ Main Methods

| Method                 | Intent              | Description                                                     |
| :--------------------- | :------------------ | :-------------------------------------------------------------- |
| `try_activate_ability` | **Safe Execution**  | Attempts to activate an ability by checking all costs and tags. |
| `apply_effect_to_self` | **Direct Mutation** | Injects an `ASEffect` directly into the component.              |
| `dispatch_event`       | **Reactivity**      | Emits a frame occurrence (EVENT type Tag).                      |
| `resolve_component`    | **Smart Search**    | Static method to locate an ASC in a complex scene tree.         |

---

## 🔒 Hard-Coded Security: Guardian

Located within the ASC, the **Guardian** is a middleware that prevents:

- Sensitive file reading by AI agents.
- Access to namespaces of other projects.
- State modifications in invalid ticks.

> [!IMPORTANT] The ASC should never be accessed directly for manual variable mutation. Always use the `try_` or
> `request_` API to ensure the integrity of the Governance Contract.
