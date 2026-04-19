---
title: "Exemplos: Padrões de Boss"
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

Implementações de diferentes tipos de boss utilizando o **Ability System**.

## Boss 1: Simple Melee Boss (Boss Corpo a Corpo)

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

    ## Transição de fase
    if health < 100 and phase == 1:
        enter_phase_2()

    ## Padrão de ataque
    if attack_timer >= 1.5:
        attack_pattern()
        attack_timer = 0.0

    ## Mover para o alvo
    if target:
        var distance = global_position.distance_to(target.global_position)
        if distance > 2.0:
            var dir = (target.global_position - global_position).normalized()
            velocity = dir * 4.0
            move_and_collide(velocity * delta)

func attack_pattern():
    if phase == 1:
        ## Simples: alternando entre slash e heavy
        if randf() < 0.5:
            asc.try_activate_ability_by_tag(&"boss.slash")
        else:
            asc.try_activate_ability_by_tag(&"boss.heavy_attack")
    else:
        ## Fase 2: mais agressivo
        var attacks = [&"boss.slash", &"boss.heavy_attack", &"boss.roar"]
        var choice = attacks[randi() % attacks.size()]
        asc.try_activate_ability_by_tag(choice)

        ## Aplicar dano ao jogador
        if choice in [&"boss.slash", &"boss.heavy_attack"]:
            target.asc.apply_effect_by_tag(&"effect.boss_damage", asc)

func enter_phase_2():
    phase = 2
    anim.play("phase_2_transition")
    asc.add_tag(&"boss.phase_2")
    print("Boss entrou na fase 2!")

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

## Boss 2: Caster Boss (Mago AoE + Fases)

```gdscript
extends Node3D
class_name CasterBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 150.0
var target: Player = null
var spell_timer = 0.0
var phase = 1 ## 1=Normal, 2=Enraged
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

    ## Checagem de fase
    if health < 75 and phase == 1:
        enter_phase_2()

    ## Rotação de feitiços
    if spell_timer >= 2.0:
        cast_spell()
        spell_timer = 0.0

func cast_spell():
    var spell = null

    match phase:
        1:
            ## Normal: fireball ou heal
            if health < 50:
                spell = &"boss.heal"
            elif minion_count < max_minions:
                spell = &"boss.summon_minion"
            else:
                spell = &"boss.fireball"

        2:
            ## Enraged: rotacionando feitiços
            var spells = [&"boss.fireball", &"boss.ice_storm", &"boss.summon_minion"]
            spell = spells[randi() % spells.size()]

    if spell:
        asc.try_activate_ability_by_tag(spell)

        if spell == &"boss.fireball":
            ## Criar projétil
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

    ## Monitorar morte do minion
    minion.defeated.connect(func():
        minion_count -= 1
    )

func enter_phase_2():
    phase = 2
    anim.play("enrage")
    asc.add_tag(&"boss.enraged")
    print("Boss em fúria!")

func take_damage(amount: float):
    health -= amount
    health_changed.emit(health)
    anim.play("hit")

    if health <= 0:
        die()

func die():
    ## Matar minions restantes
    for child in get_parent().get_children():
        if child is BossMinion:
            child.queue_free()

    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()

func _on_ability_cast(spec):
    ## Sincronizar animação
    var ability = spec.get_ability()
    if ability.ability_tag == &"boss.fireball":
        anim.play("cast_fireball")
    elif ability.ability_tag == &"boss.heal":
        anim.play("cast_heal")
```

## Boss 3: Reactive Boss (Boss que se Adapta)

```gdscript
extends CharacterBody3D
class_name ReactiveBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 250.0
var target: Player = null
var adaptation_timer = 0.0
var player_damage_taken = 0.0
var weakness: StringName = &"" ## Adapta-se à estratégia do jogador

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    adaptation_timer += delta

    ## Analisar jogador a cada 5 segundos
    if adaptation_timer >= 5.0:
        analyze_player()
        adaptation_timer = 0.0

    ## Atacar baseando-se na fraqueza detectada
    attack_intelligently()

func analyze_player():
    ## Checar o que o jogador está fazendo
    var player_tags = target.asc.get_all_tags()

    ## Se o jogador usa muito melee, atacar à distância
    if target.asc.has_tag(&"state.attacking"):
        weakness = &"melee"
    ## Se o jogador usa muita magia, ganhar resistência
    elif ASTagUtils.event_did_occur(&"event.magic_damage", target.asc, 5.0):
        weakness = &"magic"
    ## Se o jogador se cura muito, dar dispel
    elif ASTagUtils.event_did_occur(&"event.healed", target.asc, 5.0):
        weakness = &"healer"

    print("Boss adaptado à fraqueza: ", weakness)

func attack_intelligently():
    match weakness:
        &"melee":
            ## Atacar de longe
            asc.try_activate_ability_by_tag(&"boss.fireball")

        &"magic":
            ## Ataque físico + buff de resistência mágica
            asc.try_activate_ability_by_tag(&"boss.heavy_attack")
            if not asc.has_tag(&"state.magic_resistance"):
                asc.add_tag(&"state.magic_resistance")

        &"healer":
            ## Remover cura + silenciar
            asc.try_activate_ability_by_tag(&"boss.dispel")
            asc.try_activate_ability_by_tag(&"boss.silence")

        _:
            ## Padrão: rotacionar ataques
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
var phase = 1 ## 1, 2, 3

signal defeated
signal health_changed(new_health)
signal phase_changed(new_phase)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    ## Checagem contínua de fase
    if health < 375 and phase == 1:
        change_phase(2)
    elif health < 250 and phase == 2:
        change_phase(3)

    ## Comportamento por fase
    match phase:
        1:
            phase_1_behavior()
        2:
            phase_2_behavior()
        3:
            phase_3_behavior()

func phase_1_behavior():
    ## Dificuldade moderada
    var attacks = [&"boss.slash", &"boss.fireball"]
    asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])

func phase_2_behavior():
    ## Dificuldade alta - invoca ajudantes
    var attacks = [&"boss.heavy_attack", &"boss.fireball", &"boss.summon_minion"]
    asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])

    ## Aplicar debuff de vulnerabilidade no jogador
    target.asc.apply_effect_by_tag(&"effect.vulnerability", asc)

func phase_3_behavior():
    ## Extremo - habilidade ultimate + poder total
    if health > 100:
        var attacks = [&"boss.ultimate_attack", &"boss.meteor_storm", &"boss.summon_minion"]
        asc.try_activate_ability_by_tag(attacks[randi() % attacks.size()])
    else:
        ## Último suspiro - lento mas poderoso
        asc.try_activate_ability_by_tag(&"boss.last_stand")

func change_phase(new_phase: int):
    phase = new_phase
    phase_changed.emit(new_phase)
    anim.play("phase_%d_transition" % new_phase)
    asc.add_tag(&"boss.phase_%d" % new_phase)

    match new_phase:
        2:
            print("Boss: Fase 2 - Ficando sério!")
            health += 50 ## Curar na troca de fase
        3:
            print("Boss: Fase 3 - PODER ABSOLUTO!")
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
    ## Sequência de morte épica
    anim.play("death")
    asc.dispatch_event(&"event.boss_defeated")

    ## Drop de loot
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

## Boss 5: Puzzle Boss (Focado em Mecânicas)

```gdscript
extends Node3D
class_name PuzzleBoss

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 100.0
var target: Player = null
var puzzle_phase = 0 ## 0=esperando, 1=vulnerável, 2=escudo
var shield_active = false
var shield_durability = 30.0

signal defeated
signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _physics_process(delta):
    if health <= 0:
        return

    ## Mecânicas do puzzle
    match puzzle_phase:
        0:
            waiting_phase()
        1:
            vulnerable_phase()
        2:
            shield_phase()

func waiting_phase():
    ## Boss está dormindo, jogador deve ativar
    print("Boss esperando ativação...")

func vulnerable_phase():
    ## Boss vulnerável - janela de 30 segundos
    if not asc.has_tag(&"boss.vulnerable"):
        asc.add_tag(&"boss.vulnerable")
        anim.play("vulnerable")

    ## Jogador deve atacar agora
    target.asc.effect_applied.connect(_on_player_damage)

    await get_tree().create_timer(30.0).timeout
    if puzzle_phase == 1:
        shield_phase() ## Fecha a janela

func shield_phase():
    if shield_active:
        return

    shield_active = true
    asc.add_tag(&"boss.shielded")
    puzzle_phase = 2

    ## Boss cria escudo que deve ser quebrado
    print("Escudo ativado! Durabilidade: ", shield_durability)

    ## Esperar o escudo quebrar
    while shield_durability > 0:
        await get_tree().create_timer(0.5).timeout

    ## Escudo quebrado
    shield_active = false
    asc.remove_tag(&"boss.shielded")
    puzzle_phase = 1
    vulnerable_phase()

func trigger_boss():
    if puzzle_phase != 0:
        return

    print("Boss desperta!")
    anim.play("awaken")
    vulnerable_phase()

func break_shield(amount: float):
    if not shield_active:
        return

    shield_durability -= amount
    print("Durabilidade do escudo: ", shield_durability)

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
        ## Jogador está causando dano na janela vulnerável
        var damage = -effect_spec.get_magnitude(&"health")
        take_damage(damage)
```

## Integração na Cena

```gdscript
## Em BossScene.gd
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
    ui.show_message("Fase %d!" % phase)

func _on_boss_defeated():
    ui.show_message("Vitória! Boss derrotado!")
    await get_tree().create_timer(3.0).timeout
    get_tree().reload_current_scene()
```

---

Cada padrão pode ser customizado e combinado para criar encontros épicos!
