---
title: "Guia: Sistema de Combate Completo"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Sistema de Combate Completo

Aprenda a montar um sistema de combate funcional com player vs inimigo.

## Arquitetura

```
Player               Inimigo
├─ ASComponent      ├─ ASComponent
├─ AnimationPlayer  ├─ AnimationPlayer
├─ Ability A        ├─ Ability B (IA)
└─ Input            └─ Behavior Tree
```

## Passo 1: Setup Base

Crie ASContainer para ambos (Player e Enemy):

**player.tres:**

```
attribute_set: player_attributes
initial_abilities:
  - ability.slash
  - ability.heavy_attack
  - ability.dodge
```

**enemy.tres:**

```
attribute_set: enemy_attributes
initial_abilities:
  - ability.claw_swipe
  - ability.roar
```

## Passo 2: Script do Player (Combate Manual)

```gdscript
extends CharacterBody3D
class_name Player

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer
@onready var enemy: Enemy = get_tree().get_first_node_in_group("enemies")

var is_in_combat = false

func _ready():
    asc.ability_activated.connect(_on_ability_activated)
    asc.effect_applied.connect(_on_effect_applied)

func _physics_process(_delta):
    if not is_in_combat:
        return

    # Controles
    if Input.is_action_just_pressed("attack1"):
        use_ability(&"ability.slash")
    elif Input.is_action_just_pressed("attack2"):
        use_ability(&"ability.heavy_attack")
    elif Input.is_action_just_pressed("dodge"):
        use_ability(&"ability.dodge")

func use_ability(ability_tag: StringName):
    if asc.can_activate_ability_by_tag(ability_tag):
        asc.try_activate_ability_by_tag(ability_tag)
        _apply_to_enemy(ability_tag)

func _apply_to_enemy(ability_tag: StringName):
    if ability_tag == &"ability.slash":
        enemy.asc.apply_effect_by_tag(&"effect.slash_damage", asc)
        enemy.take_damage(20.0)
    elif ability_tag == &"ability.heavy_attack":
        enemy.take_damage(35.0)

func _on_ability_activated(spec):
    print("Ativou: ", spec.get_ability().ability_tag)
    anim.play("attack")

func _on_effect_applied(effect_spec):
    var damage = effect_spec.get_magnitude(&"health")
    print("Dano: ", damage)
```

## Passo 3: Script do Inimigo (IA Simples)

```gdscript
extends CharacterBody3D
class_name Enemy

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var health = 100.0
var is_alive = true
var attack_timer = 0.0

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)

func _process(delta):
    if not is_alive:
        return

    attack_timer += delta

    # IA: Ataca a cada 2 segundos
    if attack_timer >= 2.0:
        attack_player()
        attack_timer = 0.0

func attack_player():
    if asc.can_activate_ability_by_tag(&"ability.claw_swipe"):
        asc.try_activate_ability_by_tag(&"ability.claw_swipe")
        anim.play("attack")

func take_damage(amount: float):
    health -= amount
    asc.dispatch_event(&"event.damage", amount)

    print("Inimigo HP: %.1f" % health)

    if health <= 0:
        die()

func die():
    is_alive = false
    anim.play("death")
    await anim.animation_finished
    queue_free()
```

## Passo 4: Estado de Combate

```gdscript
# Em Player.gd
func _on_combat_started():
    is_in_combat = true
    print("Combat started!")

func _on_combat_ended():
    is_in_combat = false
    print("Combat ended!")

# No _ready():
enemy.health_changed.connect(_on_enemy_health_changed)

func _on_enemy_health_changed(new_health):
    if new_health <= 0:
        _on_combat_ended()
```

## Passo 5: Sistema de Recompensa

```gdscript
# Em Enemy.gd
signal defeated

func die():
    is_alive = false
    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()

# Em Player.gd
func _ready():
    enemy.defeated.connect(_on_enemy_defeated)

func _on_enemy_defeated():
    print("Victory! Gained 100 XP")
    get_tree().reload_current_scene()
```

## Casos de Uso Avançados

### 1. Sistema de Bloqueio

```gdscript
func use_ability(ability_tag: StringName):
    if asc.has_tag(&"state.blocking"):
        print("Não pode atacar enquanto bloqueia!")
        return

    if asc.can_activate_ability_by_tag(ability_tag):
        asc.try_activate_ability_by_tag(ability_tag)
```

### 2. Direcionamento

```gdscript
func _apply_to_enemy(ability_tag: StringName):
    # Verificar alcance
    var distance = global_position.distance_to(enemy.global_position)
    if distance > 2.0:
        print("Fora de alcance!")
        return

    # Aplicar efeito
    enemy.asc.apply_effect_by_tag(&"effect.slash_damage", asc)
```

### 3. Sistema de Resistência

```gdscript
# Em Enemy.gd
func take_damage(amount: float, damage_type: StringName = &"physical"):
    var resistance = asc.get_attribute_current_value(&"resistance." + damage_type)
    var final_damage = amount * (1.0 - resistance * 0.01)

    health -= final_damage
```

### 4. Combo System

```gdscript
var combo_counter = 0
var combo_timer = 0.0
const COMBO_TIMEOUT = 1.0

func _process(delta):
    combo_timer -= delta
    if combo_timer <= 0:
        combo_counter = 0

func use_ability(ability_tag: StringName):
    combo_counter += 1
    combo_timer = COMBO_TIMEOUT

    var damage_multiplier = 1.0 + (combo_counter * 0.1)

    _apply_to_enemy(ability_tag, damage_multiplier)

    if combo_counter >= 3:
        print("Combo x3! Dano crítico!")
        combo_counter = 0
```

## Checklist de Implementação

```
[ ] Setup ASComponent para player e inimigo
[ ] Criar abilities básicas
[ ] Implementar input do player
[ ] Implementar IA do inimigo
[ ] Sistema de aplicação de efeitos
[ ] Sistema de HP e morte
[ ] Animações sincronizadas
[ ] Sistema de recompensa
[ ] Feedback visual/sonoro
[ ] Balanceamento de dano
```

---

**Relacionado:** [Guia de Multiplayer](guide-multiplayer.md)
