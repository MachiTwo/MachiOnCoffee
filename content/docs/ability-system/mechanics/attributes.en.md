---
title: "Attributes: The Status System"
type: docs
weight: 3
---

**Attributes** are the numerical values that define an actor's capabilities (HP, Mana, Strength, Speed).

## 📊 ASAttributeSet

Unlike loose variables in a script, attributes are grouped in a **Set**. This allows for:

- **Centralization**: All "Damage" or "Defense" logic stays in one place.
- **Security**: Values are protected against clamping (Min/Max).
- **Simulation**: The system knows exactly how to recalculate the current value based on active modifiers.

---

## 🚗 Attribute Drivers (Derivation)

One of the most potent features is the ability for one attribute to "drive" another.

**Example: Strength increases Attack.**

- Attribute: `Strength`
- Attribute: `AttackPower`
- Driver: `AttackPower = Strength * 2.0`

Whenever your `Strength` changes, `AttackPower` will be automatically recalculated by the engine in the next tick.

---

## 📈 Calculation Order

To ensure determinism (vital for multiplayer), attributes follow this order:

1. **Base Value**: The actor's "pure" value.
2. **Drivers**: Application of calculations derived from other attributes.
3. **Flat Modifiers**: Direct additions (e.g., +5 shield from an item).
4. **Percentage Modifiers**: Final multipliers (e.g., +10% fury).

> [!NOTE] Changes to the `Base Value` are permanent. Changes to `Modifiers` are temporary and linked to `ASEffects`.
