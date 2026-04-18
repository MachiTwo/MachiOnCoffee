---
title: "Exemplo Completo: Sistema de Combate Funcional"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Exemplo Completo: Sistema de Combate Funcional

Código pronto para usar com player vs inimigo.

## Estrutura de Assets

Crie em `res://assets/ability-system/`:

```
player_attributes.tres
enemy_attributes.tres
player_container.tres
enemy_container.tres
ability_slash.tres
ability_heavy_attack.tres
ability_heal.tres
effect_slash_damage.tres
effect_heal.tres
effect_bleed.tres
```

## 1. Script do Player

```gdscript
extends CharacterBody3D
class_name Player

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer
@onready var ui = $UI

var target: Enemy = null
var is_in_combat = false
var health = 100.0

signal health_changed(new_health)

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)
    asc.ability_activated.connect(_on_ability_activated)
    asc.effect_applied.connect(_on_effect_applied)

func _physics_process(_delta):
    if not is_in_combat or not target:
        return

    # Input
    if Input.is_action_just_pressed("ability_1"):
        use_ability(&"ability.slash")
    elif Input.is_action_just_pressed("ability_2"):
        use_ability(&"ability.heavy_attack")
    elif Input.is_action_just_pressed("ability_3"):
        use_ability(&"ability.heal")

    # Direcionar para alvo
    var direction = (target.global_position - global_position).normalized()
    if direction.length() > 2.0:
        velocity = direction * 5.0
        move_and_collide(velocity * _delta)

func use_ability(ability_tag: StringName):
    if not asc.can_activate_ability_by_tag(ability_tag):
        ui.show_message("Não pode usar agora")
        return

    asc.try_activate_ability_by_tag(ability_tag)

    # Aplicar efeitos ao alvo
    match ability_tag:
        &"ability.slash":
            target.asc.apply_effect_by_tag(&"effect.slash_damage", asc)
        &"ability.heavy_attack":
            target.asc.apply_effect_by_tag(&"effect.slash_damage", asc)
            var damage = 35.0
            target.take_damage(damage)
        &"ability.heal":
            var heal_amount = 25.0
            heal(heal_amount)

func take_damage(amount: float):
    health -= amount
    asc.dispatch_event(&"event.damage", amount)
    health_changed.emit(health)
    ui.update_health(health)

    if health <= 0:
        die()

func heal(amount: float):
    health = min(health + amount, 100.0)
    health_changed.emit(health)
    ui.update_health(health)

func die():
    is_in_combat = false
    anim.play("death")
    ui.show_message("Você morreu!")

func _on_ability_activated(spec):
    anim.play("attack")

func _on_effect_applied(effect_spec):
    var damage = effect_spec.get_magnitude(&"health")
    if damage < 0:
        take_damage(-damage)
```

## 2. Script do Enemy

```gdscript
extends CharacterBody3D
class_name Enemy

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var target: Player = null
var health = 80.0
var is_alive = true
var attack_cooldown = 0.0

signal health_changed(new_health)
signal defeated

func _ready():
    asc.attribute_set.set_attribute_base_value(&"health", health)
    asc.ability_activated.connect(_on_ability_activated)

func _physics_process(delta):
    if not is_alive or not target:
        return

    attack_cooldown -= delta

    # Mover para alvo
    var distance = global_position.distance_to(target.global_position)
    if distance > 1.5:
        var direction = (target.global_position - global_position).normalized()
        velocity = direction * 3.0
        move_and_collide(velocity * delta)
    else:
        velocity = Vector3.ZERO

    # Atacar
    if attack_cooldown <= 0:
        attack_player()
        attack_cooldown = 2.0

func attack_player():
    if asc.can_activate_ability_by_tag(&"ability.slash"):
        asc.try_activate_ability_by_tag(&"ability.slash")
        asc.apply_effect_by_tag(&"effect.slash_damage", target.asc)

func take_damage(amount: float):
    health -= amount
    asc.dispatch_event(&"event.damage", amount)
    health_changed.emit(health)

    if health <= 0:
        die()

func die():
    is_alive = false
    anim.play("death")
    await anim.animation_finished
    defeated.emit()
    queue_free()

func _on_ability_activated(spec):
    anim.play("attack")
```

## 3. Manager de Combat

```gdscript
extends Node
class_name CombatManager

@onready var player = $Player
@onready var enemy = $Enemy
@onready var ui = $UI

func _ready():
    player.target = enemy
    enemy.target = player

    player.is_in_combat = true
    enemy.target = player

    player.health_changed.connect(_on_player_health_changed)
    enemy.health_changed.connect(_on_enemy_health_changed)
    enemy.defeated.connect(_on_enemy_defeated)

func _on_player_health_changed(new_health):
    ui.update_player_health(new_health)

func _on_enemy_health_changed(new_health):
    ui.update_enemy_health(new_health)

func _on_enemy_defeated():
    ui.show_message("Vitória! +100 XP")
    await get_tree().create_timer(2.0).timeout
    get_tree().reload_current_scene()
```

## 4. Script de UI

```gdscript
extends CanvasLayer
class_name CombatUI

@onready var player_hp_label = $VBox/PlayerHP
@onready var enemy_hp_label = $VBox/EnemyHP
@onready var message_label = $VBox/Message
@onready var ability_buttons = [
    $VBox/HBox/Button1,
    $VBox/HBox/Button2,
    $VBox/HBox/Button3
]

func _ready():
    for i in range(ability_buttons.size()):
        var button = ability_buttons[i]
        button.pressed.connect(_on_ability_button_pressed.bind(i))

func update_player_health(health: float):
    player_hp_label.text = "Player: %.0f / 100" % health

func update_enemy_health(health: float):
    enemy_hp_label.text = "Enemy: %.0f / 80" % health

func show_message(msg: String):
    message_label.text = msg
    message_label.show()
    await get_tree().create_timer(3.0).timeout
    message_label.hide()

func update_cooldowns():
    var player = get_tree().root.get_child(0).player
    var abilities = [&"ability.slash", &"ability.heavy_attack", &"ability.heal"]

    for i in range(abilities.size()):
        var button = ability_buttons[i]
        var spec = player.asc.get_ability_spec_by_tag(abilities[i])

        if spec and spec.is_on_cooldown():
            var remaining = spec.get_cooldown_remaining()
            button.text = "%.1f" % remaining
            button.disabled = true
        else:
            button.disabled = false

func _process(_delta):
    update_cooldowns()

func _on_ability_button_pressed(index: int):
    var player = get_tree().root.get_child(0).player
    var abilities = [&"ability.slash", &"ability.heavy_attack", &"ability.heal"]
    player.use_ability(abilities[index])
```

## 5. Scene Structure

Crie a scene no editor:

```
CombatScene (Node)
├─ Player (CharacterBody3D)
│  ├─ CollisionShape3D
│  ├─ MeshInstance3D
│  ├─ AnimationPlayer
│  └─ AbilityComponent
│
├─ Enemy (CharacterBody3D)
│  ├─ CollisionShape3D
│  ├─ MeshInstance3D
│  ├─ AnimationPlayer
│  └─ AbilityComponent
│
├─ UI (CanvasLayer)
│  └─ VBox
│     ├─ Label (PlayerHP)
│     ├─ Label (EnemyHP)
│     ├─ Label (Message)
│     └─ HBox
│        ├─ Button1 (Slash)
│        ├─ Button2 (Heavy)
│        └─ Button3 (Heal)
│
└─ CombatManager (Node)
```

## 6. Input Map

No Project Settings → Input Map, adicione:

```
ability_1: [Space]
ability_2: [Q]
ability_3: [E]
ui_accept: [Enter]
```

## 7. Executar

1. Save scene como `res://scenes/combat.tscn`
2. Attach scripts aos nodes
3. Configure container do ASComponent
4. Play

## Expandir

**Adicionar Mais Abilities:**

```gdscript
# Em ability_charging_strike.tres (phased)
phases: [windup, execution, recovery]

# Em Player.use_ability()
&"ability.charging_strike":
    await anim.animation_finished
    target.asc.apply_effect_by_tag(&"effect.heavy_damage", asc)
```

**Sistema de Loot:**

```gdscript
func die():
    is_alive = false
    anim.play("death")
    await anim.animation_finished

    # Drop loot
    var loot = preload("res://items/healing_potion.tscn").instantiate()
    get_parent().add_child(loot)
    loot.global_position = global_position

    defeated.emit()
    queue_free()
```

**Skill Tree:**

```gdscript
# Adicionar abilities ao player dinamicamente
func unlock_ability(ability_tag: StringName):
    var ability = AbilitySystem.get_ability_resource(ability_tag)
    asc.add_ability(ability)
```

---

**Próximo:** Customizar e expandir conforme sua necessidade!
