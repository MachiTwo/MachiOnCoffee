---
title: "Tutorial: Buff/Debuff System"
date: "2026-04-18T22:30:00-03:00"
slug: buffs
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

Learn how to create temporary modifiers that affect characters in the **Ability System**.

**Time:** ~10 minutes | **Level:** Intermediate

## Concept

**Buff:** Temporary positive effect (e.g., increases damage)
**Debuff:** Temporary negative effect (e.g., reduces speed)

Both are `ASEffect` with a duration.

## Step 1: Create Status Tags

Open **Project Settings → Ability System** and create:

```gdscript
state.empowered (CONDITIONAL)
state.slowed (CONDITIONAL)
state.burning (CONDITIONAL)
state.frozen (CONDITIONAL)
effect.empower (NAME)
effect.slow (NAME)
effect.burn (NAME)
effect.freeze (NAME)
```

## Step 2: Create Buff ASEffect

New Resource → **ASEffect**

Save as `res://assets/effects/empower.tres`

```gdscript
effect_tag: &"effect.empower"
duration_policy: 1 (DURATION)
duration_magnitude: 5.0
target_type: 0 (SELF)
granted_tags: [&"state.empowered"]
removed_tags: []
modifiers: (1 element)
  [0]:
    attribute: &"damage"
    operation: 1 (MULTIPLY)
    magnitude: 1.5
```

**Result:** Increases damage by 50% for 5 seconds.

## Step 3: Create Debuff ASEffect

New Resource → **ASEffect**

Save as `res://assets/effects/slow.tres`

```gdscript
effect_tag: &"effect.slow"
duration_policy: 1 (DURATION)
duration_magnitude: 3.0
target_type: 1 (OTHERS)
granted_tags: [&"state.slowed"]
removed_tags: []
modifiers: (1 element)
  [0]:
    attribute: &"movement_speed"
    operation: 0 (ADD)
    magnitude: -3.0
```

**Result:** Reduces speed by 3.0 for 3 seconds.

## Step 4: Apply Buff

```gdscript
# In Player.gd
func use_empower():
    asc.apply_effect_by_tag(&"effect.empower")
    print("Empowered!")

func _process(_delta):
    if asc.has_tag(&"state.empowered"):
        var remaining_duration = # calculate
        print("Empowered for another %.1f seconds" % remaining_duration)
```

## Step 5: Apply Debuff to Enemy

```gdscript
# When player attacks enemy
func use_ability(ability_tag: StringName):
    if asc.try_activate_ability_by_tag(ability_tag):
        # Apply slow to enemy
        if ability_tag == &"ability.ice_bolt":
            var enemy_asc = AbilitySystem.resolve_component(enemy)
            asc.apply_effect_by_tag(&"effect.slow", enemy_asc)
```

## Step 6: Continuous Debuff (DoT)

New Resource → **ASEffect**

Save as `res://assets/effects/burning.tres`

```gdscript
effect_tag: &"effect.burning"
duration_policy: 1 (DURATION)
duration_magnitude: 5.0
period: 1.0
execute_periodic_tick_on_application: true
target_type: 1 (OTHERS)
granted_tags: [&"state.burning"]
modifiers: (1 element)
  [0]:
    attribute: &"health"
    operation: 0 (ADD)
    magnitude: -10.0
```

**Result:** -10 HP every 1 second for 5 seconds (total -50 HP).

## Step 7: Visualize Buffs

```gdscript
func update_buff_ui():
    var all_effects = asc.get_all_effect_specs()

    for effect_spec in all_effects:
        var effect = effect_spec.get_effect()
        var remaining = effect_spec.get_duration_remaining()

        var label = Label.new()
        label.text = "%s (%.1f)" % [effect.effect_tag, remaining]

        if effect.effect_tag.begins_with("effect.empower"):
            label.modulate = Color.YELLOW
        elif effect.effect_tag.begins_with("effect.slow"):
            label.modulate = Color.BLUE

        buff_container.add_child(label)
```

## Step 8: Immunity

Prevents effects from being applied:

```gdscript
# In ASAbility or ASEffect:
activation_blocked_any_tags: [&"immune.fire"]

# When applying effect:
func apply_effect_to_target(effect, target_asc):
    if target_asc.has_tag(&"immune.fire"):
        if effect.effect_tag.begins_with("effect.burn"):
            print("Target is immune to burning!")
            return false

    target_asc.apply_effect_by_tag(effect.effect_tag)
    return true
```

## Step 9: Automatic Cleanup

ASComponent takes care of removing buffs when they expire:

```gdscript
func _process(_delta):
    # ASComponent automatically removes expired effects
    # You can listen for:
    asc.effect_removed.connect(_on_effect_removed)

func _on_effect_removed(effect_spec):
    var effect_tag = effect_spec.get_effect().effect_tag
    print("Effect removed: ", effect_tag)

    if effect_tag == &"effect.empower":
        print("Empowered finished!")
```

## Advanced Use Cases

### 1. Buff Stacking

```gdscript
# Apply empower 3 times = 1.5x * 1.5x * 1.5x = 3.375x damage
for i in range(3):
    asc.apply_effect_by_tag(&"effect.empower")
```

### 2. Conflicting Effects

```gdscript
# Freeze removes burning
func apply_freeze(target_asc):
    target_asc.apply_effect_by_tag(&"effect.freeze")

# In freeze ASEffect:
removed_tags: [&"state.burning"]
```

### 3. Buff Granting Ability

```gdscript
# Effect grants new ability temporarily
effect.granted_tags: [&"ability.enhanced_strike"]

# When buff expires, ability disappears
```

### 4. Buff Scaling by Level

```gdscript
func apply_buff_scaled(level: float):
    var damage_boost = 1.0 + (level * 0.1) # +10% per level
    asc.apply_effect_by_tag(&"effect.empower", level)
```

## Checklist

- [ ] Create status tags
- [ ] Create 1-2 basic buffs
- [ ] Create 1-2 basic debuffs
- [ ] Apply to player
- [ ] Apply to enemy
- [ ] Implement DoT
- [ ] Active status UI
- [ ] Remove on expiration
- [ ] Debug duration

---

**Next:** [Multiplayer Guide](../guides/guide-multiplayer)
