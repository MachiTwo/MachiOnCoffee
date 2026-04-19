---
title: "Examples: Boss Patterns"
date: "2026-04-18T22:30:00-03:00"
slug: boss-patterns
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - example
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

Implementations of different boss types using the **Ability System**.

## Boss 1: Simple Melee Boss

```gdscript
extends CharacterBody3D
class_name SimpleMeleeBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 200.0
var target: Player = null
var attack_timer = 0.0
var phase = 1

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    attack_timer += delta

    ## Phase transition
    if health < 100 and phase == 1:
        enter_phase_2()

    ## Attack pattern
    if attack_timer >= 1.5:
        attack_pattern()
        attack_timer = 0.0

    ## Move to target
    if target:
        var distance = global_position.distance_to(target.global_position)
        if distance > 2.0:
            var dir = (target.global_position - global_position).normalized()
            velocity = dir * 4.0
            move_and_collide(velocity * delta)

func attack_pattern():
    if phase == 1:
        ## Simple: alternating slash and heavy
        if randf() < 0.5:
            asc.try_activate_ability_by_tag(&"boss.slash")
        else:
            asc.try_activate_ability_by_tag(&"boss.heavy_attack")
    else:
        ## Phase 2: more aggressive
        var attacks = [&"boss.slash", &"boss.heavy_attack", &"boss.roar"]
        var choice = attacks[randi() % attacks.size()]
        asc.try_activate_ability_by_tag(choice)

        ## Apply damage to player
        if choice in [&"boss.slash", &"boss.heavy_attack"]:
            target.asc.apply_effect_by_tag(&"effect.boss_damage", asc)

func enter_phase_2():
    phase = 2
    anim.play("phase_2_transition")
    asc.add_tag(&"boss.phase_2")
    print("Boss entered phase 2!")

func take_damage(amount: float):
    health -= amount
    health_changed.emit(health)
    anim.play("hit")

    if health <= 0:
        die()

func die():
    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()
```

## Boss 2: Caster Boss (AoE + Phases)

```gdscript
extends Node3D
class_name CasterBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 150.0
var target: Player = null
var spell_timer = 0.0
var phase = 1  ## 1=Normal, 2=Enraged
var minion_count = 0
var max_minions = 3

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)
    asc.ability_activated.connect(_on_ability_cast)

func _physics_process(delta):
    if health <= 0:
        return

    spell_timer += delta

    ## Phase check
    if health < 75 and phase == 1:
        enter_phase_2()

    ## Spell rotation
    if spell_timer >= 2.0:
        cast_spell()
        spell_timer = 0.0

func cast_spell():
    var spell = null

    match phase:
        1:
            ## Normal: fireball or heal
            if health < 50:
                spell = &"boss.heal"
            elif minion_count < max_minions:
                spell = &"boss.summon_minion"
            else:
                spell = &"boss.fireball"

        2:
            ## Enraged: cycling through spells
            var spells = [&"boss.fireball", &"boss.ice_storm", &"boss.summon_minion"]
            spell = spells[randi() % spells.size()]

    if spell:
        asc.try_activate_ability_by_tag(spell)

        if spell == &"boss.fireball":
            ## Create projectile
            var proj = preload("res://vfx/fireball_projectile.tscn").instantiate()
            get_parent().add_child(proj)
            proj.global_position = global_position
            proj.target = target
            proj.damage = 25.0

        elif spell == &"boss.heal":
            health = min(health + 30, 150)
            health_changed.emit(health)

        elif spell == &"boss.summon_minion":
            summon_minion()

func summon_minion():
    if minion_count >= max_minions:
        return

    var minion = preload("res://enemies/boss_minion.tscn").instantiate()
    get_parent().add_child(minion)
    minion.global_position = global_position + Vector3(randf_range(-3, 3), 0, randf_range(-3, 3))
    minion.target = target
    minion_count += 1

    ## Track minion death
    minion.defeated.connect(func():
        minion_count -= 1
    )

func enter_phase_2():
    phase = 2
    anim.play("enrage")
    asc.add_tag(&"boss.enraged")
    print("Boss enraged!")

func take_damage(amount: float):
    health -= amount
    health_changed.emit(health)
    anim.play("hit")

    if health <= 0:
        die()

func die():
    ## Kill remaining minions
    for child in get_parent().get_children():
        if child is BossMinion:
            child.queue_free()

    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()

func _on_ability_cast(spec):
    ## Sync animation
    var ability = spec.get_ability()
    if ability.ability_tag == &"boss.fireball":
        anim.play("cast_fireball")
    elif ability.ability_tag == &"boss.heal":
        anim.play("cast_heal")
```

## Boss 3: Reactive Boss (Adapts to Player)

```gdscript
extends CharacterBody3D
class_name ReactiveBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 250.0
var target: Player = null
var adaptation_timer = 0.0
var player_damage_taken = 0.0
var weakness: StringName = &""  ## Adapt to player's strategy

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    adaptation_timer += delta

    ## Analyze player every 5 seconds
    if adaptation_timer >= 5.0:
        analyze_player()
        adaptation_timer = 0.0

    ## Attack based on weakness
    attack_intelligently()

func analyze_player():
    ## Check what player is doing
    var player_tags = target.asc.get_all_tags()

    ## If player keeps using melee, cast ranged
    if target.asc.has_tag(&"state.attacking"):
        weakness = &"melee"
    ## If player keeps using magic, build resistance
    elif ASTagUtils.event_did_occur(&"event.magic_damage", target.asc, 5.0):
        weakness = &"magic"
    ## If player heals a lot, dispel
    elif ASTagUtils.event_did_occur(&"event.healed", target.asc, 5.0):
        weakness = &"healer"

    print("Boss adapted to weakness: ", weakness)

func attack_intelligently():
    match weakness:
        &"melee":
            ## Cast ranged spell
            asc.try_activate_ability_by_tag(&"boss.fireball")

        &"magic":
            ## Physical attack + magic resistance buff
            asc.try_activate_ability_by_tag(&"boss.heavy_attack")
            if not asc.has_tag(&"state.magic_resistance"):
                asc.add_tag(&"state.magic_resistance")

        &"healer":
            ## Dispel healing + silence
            asc.try_activate_ability_by_tag(&"boss.dispel")
            asc.try_activate_ability_by_tag(&"boss.silence")

        _:
            ## Default: rotate attacks
            var attacks = [&"boss.slash", &"boss.heavy_attack", &"boss.fireball"]
            asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])

func take_damage(amount: float):
    health -= amount
    player_damage_taken += amount
    health_changed.emit(health)

    if health <= 0:
        die()

func die():
    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()
```

## Boss 4: Multi-Phase Mega Boss

```gdscript
extends CharacterBody3D
class_name MegaBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 500.0
var target: Player = null
var phase = 1  ## 1, 2, 3

signal defeated
signal health_changed(new_health)
signal phase_changed(new_phase)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    ## Continuous phase checks
    if health < 375 and phase == 1:
        change_phase(2)
    elif health < 250 and phase == 2:
        change_phase(3)

    ## Phase-specific behavior
    match phase:
        1:
            phase_1_behavior()
        2:
            phase_2_behavior()
        3:
            phase_3_behavior()

func phase_1_behavior():
    ## Moderate difficulty
    var attacks = [&"boss.slash", &"boss.fireball"]
    asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])

func phase_2_behavior():
    ## Hard difficulty - summon adds
    var attacks = [&"boss.heavy_attack", &"boss.fireball", &"boss.summon_minion"]
    asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])

    ## Apply vulnerability debuff to player
    target.asc.apply_effect_by_tag(&"effect.vulnerability", asc)

func phase_3_behavior():
    ## Extreme - ultimate ability + full power
    if health > 100:
        var attacks = [&"boss.ultimate_attack", &"boss.meteor_storm", &"boss.summon_minion"]
        asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])
    else:
        ## Final stand - slow but powerful
        asc.try_activate_ability_by_tag(&"boss.last_stand")

func change_phase(new_phase: int):
    phase = new_phase
    phase_changed.emit(new_phase)
    anim.play("phase_%d_transition" % new_phase)
    asc.add_tag(&"boss.phase_%d" % new_phase)

    match new_phase:
        2:
            print("Boss: Phase 2 - Geting serious!")
            health += 50  ## Heal on phase change
        3:
            print("Boss: Phase 3 - ULTIMATE POWER!")
            asc.add_tag(&"state.invulnerable")
            await get_tree().create_timer(1.0).timeout
            asc.remove_tag(&"state.invulnerable")

    health_changed.emit(health)

func take_damage(amount: float):
    if asc.has_tag(&"state.invulnerable"):
        return

    health -= amount
    health_changed.emit(health)
    anim.play("hit")

    if health <= 0:
        die()

func die():
    ## Epic death sequence
    anim.play("death")
    asc.dispatch_event(&"event.boss_defeated")

    ## Drop loot
    var loot = [&"item.legendary_sword", &"item.boss_ring", &"item.gold_chest"]
    for item_tag in loot:
        spawn_loot(item_tag)

    await anim.animation_finished
    defeated.emit()
    queue_free()

func spawn_loot(item_tag: StringName):
    var loot = preload("res://items/loot.tscn").instantiate()
    get_parent().add_child(loot)
    loot.global_position = global_position + Vector3(randf_range(-2, 2), 1, randf_range(-2, 2))
    loot.item_tag = item_tag
```

## Boss 5: Puzzle Boss (Mechanics-Heavy)

```gdscript
extends Node3D
class_name PuzzleBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 100.0
var target: Player = null
var puzzle_phase = 0  ## 0=waiting, 1=vulnerable, 2=shield
var shield_active = false
var shield_durability = 30.0

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    ## Puzzle mechanics
    match puzzle_phase:
        0:
            waiting_phase()
        1:
            vulnerable_phase()
        2:
            shield_phase()

func waiting_phase():
    ## Boss is dormant, player must trigger
    print("Boss waiting for input...")

func vulnerable_phase():
    ## Boss is vulnerable - 30 seconds window
    if not asc.has_tag(&"boss.vulnerable"):
        asc.add_tag(&"boss.vulnerable")
        anim.play("vulnerable")

    ## Player should attack now
    target.asc.effect_applied.connect(_on_player_damage)

    await get_tree().create_timer(30.0).timeout
    if puzzle_phase == 1:
        shield_phase()  ## Close window

func shield_phase():
    if shield_active:
        return

    shield_active = true
    asc.add_tag(&"boss.shielded")
    puzzle_phase = 2

    ## Boss creates shield that must be broken
    print("Boss shield activated! Durability: ", shield_durability)

    ## Wait for shield to break
    while shield_durability > 0:
        await get_tree().create_timer(0.5).timeout

    ## Shield broken
    shield_active = false
    asc.remove_tag(&"boss.shielded")
    puzzle_phase = 1
    vulnerable_phase()

func trigger_boss():
    if puzzle_phase != 0:
        return

    print("Boss awakens!")
    anim.play("awaken")
    vulnerable_phase()

func break_shield(amount: float):
    if not shield_active:
        return

    shield_durability -= amount
    print("Shield durability: ", shield_durability)

    if shield_durability <= 0:
        shield_durability = 30.0

func take_damage(amount: float):
    if shield_active:
        break_shield(amount)
        return

    health -= amount
    health_changed.emit(health)

    if health <= 0:
        die()

func die():
    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()

func _on_player_damage(effect_spec):
    if puzzle_phase == 1:
        ## Player is damaging in vulnerable window
        var damage = -effect_spec.get_magnitude(&"health")
        take_damage(damage)
```

## Scene Integration

```gdscript
## In BossScene.gd
extends Node3D

@onready var boss = $MegaBoss
@onready var player = $Player
@onready var ui = $UI

func _ready():
    boss.target = player
    player.target = boss

    boss.health_changed.connect(_on_boss_health_changed)
    boss.phase_changed.connect(_on_boss_phase_changed)
    boss.defeated.connect(_on_boss_defeated)

func _on_boss_health_changed(health):
    ui.update_boss_health(health)

func _on_boss_phase_changed(phase):
    ui.show_message("Phase %d!" % phase)

func _on_boss_defeated():
    ui.show_message("Victory! Boss defeated!")
    await get_tree().create_timer(3.0).timeout
    get_tree().reload_current_scene()
```

---

Each pattern can be customized and combined to create epic encounters!
