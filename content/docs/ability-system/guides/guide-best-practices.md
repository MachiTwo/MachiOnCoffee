---
title: "Guia: Best Practices e Padrões"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Best Practices e Padrões

Aprenda padrões verificados para o Ability System.

## 1. Organização de Assets

**Estrutura de Pastas:**

```
res://assets/ability-system/
├─ attributes/
│  ├─ player_attributes.tres
│  ├─ enemy_attributes.tres
│  └─ boss_attributes.tres
├─ abilities/
│  ├─ player/
│  │  ├─ slash.tres
│  │  ├─ fireball.tres
│  │  └─ heal.tres
│  ├─ enemy/
│  │  └─ claw_swipe.tres
│  └─ boss/
│      └─ ultimate.tres
├─ effects/
│  ├─ damage/
│  │  ├─ slash_damage.tres
│  │  ├─ fire_damage.tres
│  │  └─ burning.tres
│  ├─ buff/
│  │  ├─ empower.tres
│  │  └─ shield.tres
│  └─ debuff/
│      ├─ slow.tres
│      └─ stun.tres
├─ containers/
│  ├─ player_archetype.tres
│  ├─ goblin_archetype.tres
│  └─ boss_archetype.tres
├─ phases/
│  └─ (ASAbilityPhase resources)
└─ cues/
   ├─ animations/
   ├─ sounds/
   └─ particles/
```

## 2. Naming Conventions

**Tags:**

```gdscript
# Abilities
ability.warrior.slash
ability.warrior.charge
ability.mage.fireball
ability.rogue.backstab

# States
state.physical
state.physical.stunned
state.physical.slowed
state.magical
state.magical.burning
state.magical.frozen

# Events
event.damage.physical
event.damage.magical
event.heal
event.death

# Immunities
immune.fire
immune.cold
immune.magic
```

**Resources:**

```
✅ slash_damage_effect.tres
✅ fire_burst_ability.tres
✅ warrior_equipment_container.tres

❌ ability.tres  # Vago
❌ e1.tres       # Sem contexto
```

## 3. Container Patterns

**Base Player:**

```gdscript
# res://assets/containers/player_base.tres
attribute_set: base_attributes
initial_abilities: []  # Vazio, abilities adicionadas via items
initial_effects: []
initial_cues: []
```

**Entity Templates:**

```gdscript
# res://assets/containers/goblin.tres
attribute_set: goblin_attributes
initial_abilities: [claw_swipe, roar]
initial_effects: []

# res://assets/containers/goblin_mage.tres
attribute_set: goblin_mage_attributes
initial_abilities: [claw_swipe, fireball, heal]
initial_effects: [burn_aura]  # Sempre ativo
```

## 4. Ability Design Pattern

**Small Ability (Instant):**

```gdscript
ability_tag: &"ability.slash"
ability_duration_policy: INSTANT
cooldown_duration: 0.5
costs: [{"mana": 0}]
requirements: []
activation_required_all_tags: []
activation_owned_tags: []
effects: [slash_damage]
```

**Medium Ability (Channeled):**

```gdscript
ability_tag: &"ability.heal"
ability_duration_policy: DURATION
cooldown_duration: 3.0
costs: [{"mana": 30}]
requirements: [{"health": 1}]  # Precisa estar vivo
activation_owned_tags: [&"state.channeling"]
effects: [heal_effect]
```

**Complex Ability (Phased):**

```gdscript
ability_tag: &"ability.ultimate"
ability_duration_policy: DURATION
phases: [windup, execution, recovery]
cooldown_duration: 10.0
costs: [{"rage": 100}]
requirements: [{"health": 50}]  # Min 50 HP
```

## 5. Effect Stacking Strategy

**Não Stackable:**

```gdscript
stacking_policy: OVERRIDE  # Apenas 1 ativa por vez
duration_magnitude: 5.0
```

**Stackable com Límite:**

```gdscript
stacking_policy: INTENSITY  # Múltiplas instâncias
max_stacks: 5
```

**DoT Customizado:**

```gdscript
stacking_policy: NEW_INSTANCE
period: 1.0
duration_magnitude: 3.0
# Cada aplicação = novo tick a cada 1s por 3s
```

## 6. Attribute System Pattern

**Básico:**

```gdscript
# Player attributes
health: 100 → 1000 (escala com nível)
mana: 50 → 300
stamina: 100 → 200
strength: 10 → 50
```

**Derived (Drivers):**

```gdscript
# Set quando criar:
attribute_set.add_driver(&"damage", &"strength", MULTIPLY, 2.0)
# Dano = Força * 2.0 (auto-recalcula)

attribute_set.add_driver(&"health", &"constitution", MULTIPLY, 10.0)
# Saúde = Constituição * 10
```

## 7. Multiplayer Pattern

**Client:**

```gdscript
func _physics_process(_delta):
    asc.capture_snapshot()  # Salvar pre-state

    if Input.is_action_just_pressed("attack"):
        asc.try_activate_ability_by_tag(&"ability.slash")
        request_ability.rpc_id(1, &"ability.slash")

@rpc("any_peer")
func request_ability(tag: StringName):
    # Server valida
    pass

@rpc("reliable")
func confirm_ability(tag: StringName):
    # Client confirma
    pass

@rpc("reliable")
func deny_ability(tag: StringName):
    # Client rollback
    var tick = get_tick_count()
    asc.apply_snapshot(tick)
```

## 8. Event Patterns

**Request-Response:**

```gdscript
# Player dispara:
asc.dispatch_event(&"event.request_heal", 50.0)

# Server responde:
asc.dispatch_event(&"event.heal_applied", actual_heal)
```

**State Change:**

```gdscript
# Entrar em burning:
asc.dispatch_event(&"event.status_change", {
    "status": "burning",
    "duration": 5.0
})

# Listeners reagem:
if ASTagUtils.event_did_occur(&"event.status_change", asc, 0.1):
    update_ui()
```

## 9. Combat Flow

**Padrão Recomendado:**

```gdscript
# 1. Check
if asc.can_activate_ability_by_tag(ability_tag):
    # 2. Activate
    asc.try_activate_ability_by_tag(ability_tag)

    # 3. Apply Effects
    var target_asc = get_target()
    asc.apply_effect_by_tag(&"effect.damage", target_asc)

    # 4. Emit Events
    asc.dispatch_event(&"event.ability_used", {
        "ability": ability_tag,
        "target": target_asc
    })
```

## 10. Performance Optimization

**Use Caching:**

```gdscript
var cached_specs = {}

func get_ability_spec_cached(tag: StringName):
    if not cached_specs.has(tag):
        cached_specs[tag] = asc.get_ability_spec_by_tag(tag)
    return cached_specs[tag]

# Invalidar quando ability muda:
asc.ability_activated.connect(func(spec):
    cached_specs.clear()
)
```

**Batch Queries:**

```gdscript
# ❌ Ruim: 100 queries
for enemy in enemies:
    if enemy.asc.has_tag(&"state.burning"):
        pass

# ✅ Bom: 1 query + loop
var burning_enemies = enemies.filter(func(e):
    return e.asc.has_tag(&"state.burning")
)
```

**Use Tags Cleverly:**

```gdscript
# ❌ Ruim: Query atributo frequente
if asc.get_attribute_current_value(&"health") <= 0:
    die()

# ✅ Bom: Tag-based
if asc.has_tag(&"state.dead"):
    die()

# Quando health <= 0, aplicar effect que concede state.dead
```

## 11. Testing Pattern

```gdscript
# test_ability_system.gd
extends GdUnitTestSuite

func test_ability_activates():
    var asc = ASComponent.new()
    var ability = ASAbility.new()
    ability.ability_tag = &"test.ability"

    assert_true(asc.try_activate_ability_by_tag(&"test.ability"))

func test_effect_applies():
    var effect = ASEffect.new()
    effect.effect_tag = &"test.effect"

    asc.apply_effect_by_tag(&"test.effect")
    var spec = asc.get_effect_spec_by_tag(&"test.effect")

    assert_not_null(spec)
```

## 12. Checklist de Projeto

```
Design Phase:
[ ] Listar todas as abilities
[ ] Definir stats base
[ ] Design tag taxonomy
[ ] Planejador de fases

Implementation:
[ ] Folder structure
[ ] Tag registry
[ ] Base containers
[ ] Ability templates
[ ] Effect templates

Testing:
[ ] Unidade abilities
[ ] Integração efeitos
[ ] Multiplayer sync
[ ] Performance

Polish:
[ ] Animações
[ ] Feedback audio
[ ] Partículas
[ ] UI elementos
```

---

**Relacionado:** [Troubleshooting](guide-troubleshooting.md)
