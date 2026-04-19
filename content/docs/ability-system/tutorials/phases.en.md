---
title: "Tutorial: Ability Phases"
date: "2026-04-18T22:30:00-03:00"
slug: phases
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

Learn how to create complex abilities with multiple phases (Casting, Active, Recovery) in the **Ability System**.

**Time:** ~15 minutes | **Level:** Advanced

## What are Phases?

Phases allow you to split an ability into temporal stages, each with its own behavior:

1.  **Casting:** Preparation time (can be interrupted).
2.  **Active:** The moment the main effect occurs.
3.  **Recovery:** "Recover" time after use.

## Step 1: Define Phases in the Resource

In your `ASAbility`, you can configure the `phases` array.

```gdscript
# Example phase configuration for a 'Super Attack'
phases = [
    {
        "name": &"prepare",
        "duration": 1.0,
        "is_interruptible": true,
        "tags_granted": [&"state.casting"]
    },
    {
        "name": &"execute",
        "duration": 0.5,
        "is_interruptible": false,
        "tags_granted": [&"state.immune"]
    },
    {
        "name": &"recover",
        "duration": 0.8,
        "is_interruptible": true,
        "tags_granted": [&"state.vulnerable"]
    }
]
```

## Step 2: Listen for Phase Change Signals

In your character script or ability script, you can react to changes:

```gdscript
func _ready():
    asc.ability_phase_changed.connect(_on_ability_phase_changed)

func _on_ability_phase_changed(ability_spec, old_phase, new_phase):
    print("Ability %s changed from %s to %s" % [ability_spec.get_ability().resource_name, old_phase, new_phase])
    
    match new_phase:
        &"prepare":
            play_animation("cast_start")
            spawn_particles("charge_up")
        &"execute":
            play_animation("attack_swing")
            apply_damage_area()
        &"recover":
            play_animation("cast_end")
```

## Step 3: Interrupting Phases

If a phase is marked as `is_interruptible`, it can be canceled by external effects or manual calls:

```gdscript
func take_hit():
    # If in the middle of an interruptible 'cast', cancel the ability
    if asc.is_any_ability_in_phase(&"prepare"):
        asc.cancel_all_abilities_with_tag(&"state.casting")
        play_animation("stagger")
```

## Step 4: Visual Transitions (Cues)

You can link `ASCue` to specific phases for visual automation:

```gdscript
# In the ASAbility inspector
# phase_cues = {
#     "prepare": [res://vfx/charge.tres],
#     "execute": [res://vfx/explosion.tres]
# }
```

## Conclusion

The phase system is the foundation for creating "commit" and risk/reward mechanics in action games and RPGs.

---

**Next:** [Tutorial: First Attack](first-attack)
