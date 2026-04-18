---
title: "Effects: State Modifiers"
type: docs
weight: 2
---

{{< lang-toggle >}}

**Effects** (`ASEffect`) are the agents of change. Anything that alters an attribute or adds a tag for a specific
duration is an effect.

## 🕒 Duration Policies

- **INSTANT**: Applied in one frame and disappears (e.g., Direct Damage, Healing).
- **DURATION**: Lasts for a fixed time (e.g., Strength Buff for 5s).
- **INFINITE**: Persists until manually removed or via other logic (e.g., Poison Aura).

---

## 🥞 Stacking

How does the system handle applying the same "Poison" twice?

1. **STACK_NEW_INSTANCE**: Each application is independent (two timers running).
2. **STACK_OVERRIDE**: The new application resets the old one's timer.
3. **STACK_INTENSITY**: Increases the "level" or magnitude (e.g., Poison x1 -> Poison x2).
4. **STACK_DURATION**: Adds the new duration to the remaining time of the old one.

---

## 💓 Modifiers and Operations

An effect can contain multiple modifiers acting on different attributes:

| Operation       | Description                                                           |
| :-------------- | :-------------------------------------------------------------------- |
| **OP_ADD**      | Adds the value to the base (e.g., +10 HP).                            |
| **OP_MULTIPLY** | Multiplies the value (e.g., x1.5 Damage).                             |
| **OP_OVERRIDE** | Ignores the base and sets a fixed value (e.g., Morphed -> Speed = 0). |

### Periodicity (Ticking)

Duration effects can have a `period`. This allows creating DoT (Damage over Time) or HoT (Heal over Time) effects that
"tick" every X seconds.

---

## 🎨 Granted Tags

Effects are the primary means of applying **CONDITIONAL Tags**. If you are under the "Frozen" effect, the effect grants
you the `state.frozen` tag. As soon as the effect expires, the tag is automatically removed by the **RefCount** system.
