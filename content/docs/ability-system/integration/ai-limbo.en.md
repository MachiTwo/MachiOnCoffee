---
title: "AI: Integration with LimboAI"
type: docs
weight: 1
---

{{< lang-toggle >}}

Artificial Intelligence in the Zyris Engine does not operate in a vacuum. It interacts with the **Ability System**
through a logical layer called **ASBridge**.

## 🌉 What is the ASBridge Layer?

Status v0.2.0 decommissioned the `ASBridge` Singleton in favor of native and atomic integration. Now, "Bridge" strictly
refers to the collection of:

- **BT Actions**: Behavior Tree tasks (LimboAI).
- **BT Conditions**: Logical conditions for tree branches.
- **LimboState**: States for hierarchical state machines (HSM).

---

## 🚦 The Resolution Authority

The main **AbilitySystem** Singleton now acts as the reference judge. Behavior trees use the `resolve_component()`
method to find the agent's ASC, without needing to know where it is physically in the scene tree.

```cpp
// Internal example of Bridge tasks
AbilitySystem::get_singleton()->resolve_component(agent);
```

---

## 🤖 Common Tasks (BTNodes)

| Node                         | Description                                                                |
| :--------------------------- | :------------------------------------------------------------------------- |
| `BTActionAS_ActivateAbility` | Sends the activation command to the ASC.                                   |
| `BTConditionAS_HasTag`       | Checks if the target has a specific tag to decide the next branch.         |
| `BTConditionAS_CanActivate`  | Pre-checks if the ability has costs and tags to be used.                   |
| `BTActionAS_DispatchEvent`   | Dispatches an event (e.g., `event.ai.spotted`) that can trigger reactions. |

## 🔄 HSM Synergy (State Machines)

The `ASComponent` interacts closely with **LimboHSM**. The state of the character's state machine can be driven
reactively through **Events** and **Tags**.

This means your AI can change state simply because the Ability System detected that the `state.stunned` tag was added,
without you having to write manual verification code in every frame.

> [!CAUTION] > **Rigorous Decoupling**: Never let your AI manipulate attributes directly. It should always "ask" through
> abilities or effects, respecting the Governance Contract.
