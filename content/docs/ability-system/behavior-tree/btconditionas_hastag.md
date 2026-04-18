---
title: "BTConditionAS_HasTag"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `BTCondition` • `LimboAI`

## Descrição Breve

Condição de Behavior Tree que verifica se um ator possui uma tag específica.

## Descrição Completa

`BTConditionAS_HasTag` chama `ASComponent.has_tag()` para validar possessão de tag.

**Retorna:**

- **BT.SUCCESS** se ator possui a tag
- **BT.FAILURE** se não possui

Usado para gating de comportamento: "Se está queimando, não pode congelar. Se está voando, não pode usar ground moves."

## Herança

````gdscript
BTTask
 └─ BTCondition
     └─ BTConditionAS_HasTag
```gdscript

## Propriedades

| Propriedade     | Tipo       | Descrição                                                   |
| --------------- | ---------- | ----------------------------------------------------------- |
| `tag`           | StringName | Tag a verificar (ex: &"state.burning")                      |
| `exact_match`   | bool       | Se true, match exato; se false, hierárquico (padrão: false) |
| `asc_node_path` | NodePath   | Caminho explícito para ASComponent (auto-resolve)           |

## Métodos

## Getters

## `get_tag() → StringName` (const)

Retorna tag.

## `get_exact_match() → bool` (const)

Retorna modo de match.

## `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

## Setters

## `set_tag(tag: StringName) → void`

Define tag.

## `set_exact_match(exact: bool) → void`

Define modo de match.

## `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Tick:**

1. Resolve ASComponent
2. Verifica: `asc.has_tag(tag, exact_match)`
3. Retorna **BT.SUCCESS** ou **BT.FAILURE**

## Matching Modes

## Hierárquico (exact_match = false)

```gdscript
# Ator tem: &"state.stunned.freeze"

asc.has_tag(&"state.stunned.freeze")  # true (exato)
asc.has_tag(&"state.stunned")         # true (parent)
asc.has_tag(&"state")                 # true (raiz)
asc.has_tag(&"other")                 # false
```gdscript

**Use:** Comportamentos amplos que se aplicam a categorias.

## Exato (exact_match = true)

```gdscript
# Ator tem: &"state.stunned.freeze"

asc.has_tag(&"state.stunned.freeze", true)  # true
asc.has_tag(&"state.stunned", true)         # false
asc.has_tag(&"state", true)                 # false
```gdscript

**Use:** Comportamentos específicos para estado exato.

## Casos de Uso

## Guard Clause: Impedir Ação

```gdscript
sequence: [
    condition: NOT BTConditionAS_HasTag
      tag: &"state.stunned"
    action: attack_enemy
]

# Se está stunned → sequence falha, não ataca
# Se não stunned → ataca
```gdscript

## Categoria Gating

```gdscript
sequence: [
    condition: BTConditionAS_HasTag
      tag: &"state"  # Qualquer estado
      exact_match: false
    action: play_status_animation
]

# Se tem qualquer "state.*" → animar status
```gdscript

## Class/Type Check

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"class.warrior"
        action: use_warrior_ability
    ],
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"class.mage"
        action: use_mage_ability
    ],
    action: basic_attack
]

# Baseia ação na classe do ator
```gdscript

## Buff/Debuff Response

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"state.burning"
        action: search_for_water
    ],
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"state.frozen"
        action: search_for_heat_source
    ],
    action: continue_normal_behavior
]

# Comportamento muda com debuffs
```gdscript

## Multi-Tag Requirements

```gdscript
sequence: [
    condition: BTConditionAS_HasTag
      tag: &"state.empowered"
    condition: BTConditionAS_HasTag
      tag: &"ability.unlocked_ultimate"
    action: use_ultimate
]

# Ultimate requer 2 tags
```gdscript

## Inverted Logic

```gdscript
# NÃO tem tag:
sequence: [
    condition: NOT BTConditionAS_HasTag
      tag: &"state.silenced"
    action: cast_spell
]

# Se está silenciado → não casteia
# Se não silenciado → casteia
```gdscript

## Resolução de ASComponent

Auto-discovery se `asc_node_path` vazio.

## Performance

**Muito Rápido:** O(1) lookup em hashtable interna.

## Casos de Uso Avançado

## Stat-Based Behavior

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"state.low_health"
        action: flee
    ],
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"state.high_health"
        action: aggressive_attack
    ],
    action: balanced_behavior
]
```gdscript

## Phase Transitions

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"boss.phase_3"
        action: use_enraged_attacks
    ],
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"boss.phase_2"
        action: use_special_attacks
    ],
    action: use_basic_attacks
]
```gdscript

## Environmental Awareness

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"environment.underwater"
        action: swim_behavior
    ],
    sequence: [
        condition: BTConditionAS_HasTag
          tag: &"environment.airborne"
        action: flying_behavior
    ],
    action: ground_behavior
]
```gdscript

## Immunities and Resistances

```gdscript
sequence: [
    condition: BTConditionAS_HasTag
      tag: &"immune.fire"
      exact_match: true
    action: skip_fire_damage
]

# Apenas "immune.fire", não "immune" genérico
```gdscript

## Debugging

```gdscript
class_name DebugHasTagCondition
extends BTConditionAS_HasTag

func _tick(agent, blackboard):
    var asc = AbilitySystem.resolve_component(agent)
    var has = asc.has_tag(tag, exact_match)
    print("Has tag '%s' (exact=%s): %s" % [tag, exact_match, has])

    if has:
        print("  All tags on actor: %s" % asc.get_all_tags())

    return super._tick(agent, blackboard)
```gdscript

## Comparação: Exact vs Hierarchical

**Hierarchical (exact_match = false):**

```gdscript
# Ator: state.stunned.freeze
condition: BTConditionAS_HasTag
  tag: &"state"
  exact_match: false
# Resultado: SUCCESS (combina parent)
```gdscript

**Exact (exact_match = true):**

```gdscript
# Ator: state.stunned.freeze
condition: BTConditionAS_HasTag
  tag: &"state"
  exact_match: true
# Resultado: FAILURE (não é match exato)
```gdscript

**Regra:** Usar hierárquico para categorias, exato para específicos.

## Integração com ASComponent

`has_tag` é API pública:

```gdscript
if asc.has_tag(&"state.burning"):
    print("Está queimando!")

if asc.has_tag(&"state", false):  # Qualquer state
    print("Tem algum estado")
```gdscript

`BTConditionAS_HasTag` simplesmente chama isso via Behavior Tree.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Verifica tag
- [AbilitySystem](../singleton/ability-system.md) — Registry de tags
- [ASTagSpec](../refcounted/astagspec.md) — Container de tags
- [BTConditionAS_CanActivate](btconditionas_canactivate.md) — Verifica ability (usa tags internamente)

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
