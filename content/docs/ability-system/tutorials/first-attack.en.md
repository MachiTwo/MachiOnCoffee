---
title: "Tutorial: First Attack"
date: "2026-04-18T22:30:00-03:00"
slug: first-attack
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - tutorial
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

Step-by-step guide to creating your first functional combat ability in the **Ability System**.

**Time:** ~15 minutes | **Level:** Beginner

## Step 1: Create the Ability Resource

1.  Create a folder `res://combat/abilities/`.
2.  Right-click → **New Resource → ASAbility**.
3.  Save it as `basic_attack.tres`.

## Step 2: Configure Activation Tags

In the inspector of your new resource, look for the **Tags** section:

-   **Ability Tag:** `&"ability.basic_attack"`
-   **Activation Owned Tags:** `[&"state.attacking"]` (This prevents other abilities from using the character while attacking).

## Step 3: Create the Damage Effect

Abilities in the **Ability System** usually cause effects (`ASEffect`).

1.  Create a new **ASEffect** in `res://combat/effects/damage_basic.tres`.
2.  Configure the **Modifiers**:
    -   **Attribute:** `&"health"`
    -   **Operation:** `0 (ADD)`
    -   **Magnitude:** `-10.0`

## Step 4: Link the Effect to the Ability

Go back to the `basic_attack.tres` resource:

1.  Add an item to the **Application Effects** array.
2.  Drag the `damage_basic.tres` file there.

## Step 5: Call via Code

In your Character script:

```gdscript
func _input(event):
    if event.is_action_pressed("attack"):
        if asc.try_activate_ability_by_tag(&"ability.basic_attack"):
            print("Attack started!")
```

## Conclusion

You have just created the full flow: Input → Ability Activation → Effect Application.

---

**Explore more:** [Tutorial: Buffs and Debuffs](buffs)
