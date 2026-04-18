---
title: "Abilities: Gameplay Logic"
type: docs
weight: 1
---

{{< lang-toggle >}}

**Abilities** (`ASAbility`) are the building blocks of action. They define what a character does, how much it costs, and
how they are prevented from doing it.

## 🧬 Anatomy of an Ability

An ability in the Zyris System is divided between the **Resource** (immutable DNA) and the **Spec** (runtime instance).

- **Costs**: Attribute modifiers consumed at the start.
- **Requirements**: Tags (CONDITIONAL) that must or must not be present.
- **Cooldown**: Waiting time marked by specific Tags.

---

## 🎭 Ability Phases (Complex Cycles)

One of the most powerful features for designers is the **Phases** system. If a standard ability is a "click", an ability
with Phases is a "ritual".

Example of a Heavy Attack:

1. **Windup (0.5s)**: The character prepares the strike. Applies `state.vulnerable` tag.
2. **Execution**: The strike occurs. Dispatches `event.damage`.
3. **Recovery (0.3s)**: The character recovers.

## Transitions

Phases can transition via **Time** (fixed duration) or **Event** (e.g., the animation master sends the `.Hit` signal).

---

## ⚡ Triggers: Reactive Automation

Abilities don't just have to be activated by buttons. They can be **Reactive**:

- `TRIGGER_ON_TAG_ADDED`: Automatically activates when the character receives a tag (e.g., "Shield Activated" when
  entering combat).
- `TRIGGER_ON_EVENT`: Activates in response to an occurrence (e.g., "Counter-attack" upon taking damage).

---

## 💻 Implementation Example (Virtuals)

Designers define data in the Inspector, and the programmer implements the logic:

````cpp
void _on_activate_ability(Object* owner, RefCounted* spec) {
    // Pure gameplay logic here
    // Costs and cooldowns are already handled by the engine!
}
```gdscript

> [!TIP] Use **Sub-Abilities** to create composed abilities that are unlocked together, keeping the hierarchy clean.
````
