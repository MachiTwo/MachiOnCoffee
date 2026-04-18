---
title: "ASContainer"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASContainer

**Badge:** `Resource`

## Descrição Breve

Arquétipo completo (blueprint) para um ator.

## Descrição Completa

`ASContainer` é um "molde" (template/archetype) que define toda a configuração inicial de um ator. Armazena:

- **AttributeSet**: Esquema de stats (HP, Mana, Força, etc)
- **Abilities Catalog**: Lista de todas as abilities que o ator pode ter
- **Initial Effects**: Effects aplicados ao spawn (buffs iniciais, auras passivas)
- **Cues Catalog**: Feedback audiovisual disponível
- **Events**: Lista de eventos que o ator pode disparar/ouvir

Quando um `ASComponent` chama `apply_container(container)`, ele:

1. Deep-clona o `AttributeSet` para instância única
2. Carrega todas as abilities no catálogo
3. Aplica effects iniciais

## Herança

```
Resource
 └─ ASContainer
```

## Propriedades

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `attribute_set` | ASAttributeSet | `null` | Esquema de stats para este ator |
| `abilities` | ASAbility[] | `[]` | Catálogo de abilities |
| `cues` | ASCue[] | `[]` | Catálogo de cues disponíveis |
| `effects` | ASEffect[] | `[]` | Effects aplicados ao inicializar |
| `events` | StringName[] | `[]` | Eventos associados com este container |

## Métodos Públicos

### Gerenciamento de Abilities

#### `add_ability(ability: ASAbility) → void`

Adiciona ability ao catálogo do container.

#### `has_ability(ability: ASAbility) → bool` (const)

Verifica se ability está no catálogo.

**Exemplo:**

```gdscript
if container.has_ability(fireball_ability):
    print("Container tem fireball!")
```

### Gerenciamento de Effects

#### `add_effect(effect: ASEffect) → void`

Adiciona effect à lista de effects iniciais.

**Exemplo:**

```gdscript
container.add_effect(passive_aura_effect)  # Aplicado ao spawn
```

#### `has_effect(effect: ASEffect) → bool` (const)

Verifica se effect está na lista inicial.

### Gerenciamento de Cues

#### `add_cue(cue: ASCue) → void`

Adiciona cue ao catálogo.

#### `has_cue(tag: StringName) → bool` (const)

Verifica se cue com tag existe.

#### `has_cue_resource(cue: ASCue) → bool` (const)

Verifica se recurso específico existe.

**Exemplo:**

```gdscript
if container.has_cue(&"cue.hit_animation"):
    # Pode usar este cue
```

## Casos de Uso

### Arquétipo de Guerreiro

```gdscript
var warrior_container = ASContainer.new()
warrior_container.attribute_set = warrior_attribute_set

# Catálogo de abilities
warrior_container.add_ability(ability_slash)
warrior_container.add_ability(ability_shield_bash)
warrior_container.add_ability(ability_whirlwind)

# Effects iniciais (passivos)
warrior_container.add_effect(effect_warrior_passive)

# Cues (feedback)
warrior_container.add_cue(cue_slash_animation)
warrior_container.add_cue(cue_shield_block_sound)

# Eventos
warrior_container.events.append(&"event.warrior.combat")
warrior_container.events.append(&"event.warrior.shield_active")
```

### Arquétipo de NPC Inimigo

```gdscript
var enemy_container = ASContainer.new()
enemy_container.attribute_set = enemy_attribute_set

# Abilities limitadas
enemy_container.add_ability(ability_basic_attack)
enemy_container.add_ability(ability_charge_attack)

# Buff inicial
enemy_container.add_effect(effect_enemy_armor_buff)

# Sem cues complexas (simples)
enemy_container.add_cue(cue_basic_hit)
```

### Uso em ASComponent

```gdscript
@onready var asc = $ASComponent

func _ready():
    # Aplica container (carrega abilities, effects, attribute set)
    asc.apply_container(warrior_container)

    # Agora guerreiro tem seus atributos e abilities
    if asc.can_activate_ability_by_tag(&"ability.slash"):
        asc.try_activate_ability_by_tag(&"ability.slash")
```

### Instanciar Múltiplos Atores de Mesmo Tipo

```gdscript
func spawn_warrior(position: Vector2) -> Node:
    var warrior = character_scene.instantiate()
    var asc = AbilitySystem.resolve_component(warrior)

    # Cada instância carrega do container
    asc.apply_container(warrior_container)

    warrior.position = position
    add_child(warrior)

    return warrior

# Spawn 5 guerreiros—cada um com AttributeSet único, abilities compartilhadas
for i in range(5):
    spawn_warrior(Vector2(i * 100, 0))
```

### Deep Clone Safety

Importante: Quando `apply_container()` é chamado, o `AttributeSet` é **deep-cloned**:

```gdscript
asc.apply_container(container)

# Agora asc tem seu próprio AttributeSet
var health_1 = asc.get_attribute_current_value(&"health")

# Container pode ser aplicado a outro ASC
asc2.apply_container(container)

# asc2 tem seu próprio AttributeSet (não compartilhado com asc)
asc.set_attribute_base_value(&"health", 50.0)  # Afeta apenas asc
asc2.get_attribute_current_value(&"health")    # Ainda é 100
```

## Referências Relacionadas

- [ASAttributeSet](asattributeset.md) — Esquema de stats
- [ASAbility](asability.md) — Abilities no catálogo
- [ASEffect](aseffect.md) — Effects iniciais
- [ASCue](ascue.md) — Cues de feedback
- [ASComponent](../nodes/ascomponent.md) — Node que carrega container

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
