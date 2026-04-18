---
title: "Identity Matrix: Tags"
type: docs
weight: 1
---

{{< lang-toggle >}}

In the Zyris Ability System, **Tags** are not just labels; they are the absolute truth about your game's state. They
form an Actor's **Identity Matrix**.

## 🏷️ What Are Tags?

Tags are hierarchical identifiers based on `StringName` (e.g., `state.stunned`, `ability.warrior.powerhit`). They allow
for high-performance queries and automatic visual tree organization.

## The 3 Canonical Types

To ensure governance, tags are divided into mandatory types:

| Type          | Semantic Role     | Usage Restriction                                                   |
| :------------ | :---------------- | :------------------------------------------------------------------ |
| `NAME`        | **Who I Am**      | Used exclusively to identify Resources (`ASAbility`/`ASEffect`).    |
| `CONDITIONAL` | **How I Am**      | Used for Logical Gates (`Required`/`Blocked`). Persist in RefCount. |
| `EVENT`       | **What Happened** | Instantaneous occurrences (1 tick). Used for event dispatch.        |

---

## 🏛️ Hierarchy and Groups

Tags use dots (`.`) to define ancestors. If an actor has the `state.stunned.frozen` tag, they technically also have
`state.stunned` and `state`. This allows for broad checks:

````gdscript
# Returns true if the target is stunned in any way
ASTagUtils.has_tag(target, "state.stunned")
```gdscript

---

## 🕒 Temporal Memory (History)

The `ASComponent` maintains circular buffers of **128 entries** to track the recent past:

- **NAME History**: When identities were added/removed.
- **CONDITIONAL History**: Changes in permissions and immunities.
- **EVENT History**: What happened in recent frames (magnitude, instigator).

## Reactivity Example

Counter-attack abilities can ask: _"Did a block event occur in the last 0.4 seconds?"_

```cpp
ASTagUtils::event_did_occur("event.damage.block", target, 0.4f);
```gdscript

---

## ⚖️ Golden Rules (Security)

1. **Never use NAME tags for logic**: Attempting to block an ability using a `NAME` tag is a security violation. Logic
   must only depend on `CONDITIONAL` tags.
2. **Singleton Registration**: All tags (except event payloads) must be registered in the global singleton to ensure
   autocomplete and prevent typos.
3. **Event Dispatch**: Never dispatch an event whose name is not registered with the `EVENT` type.
````
