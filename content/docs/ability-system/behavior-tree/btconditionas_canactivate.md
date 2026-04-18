---
title: "BTConditionAS_CanActivate"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `BTCondition` • `LimboAI`

## Descrição Breve

Condição de Behavior Tree que verifica se uma ability pode ser ativada.

## Descrição Completa

`BTConditionAS_CanActivate` chama `ASComponent.can_activate_ability_by_tag()` para validar pré-requisitos **sem
ativar**.

**Retorna:**

- **BT.SUCCESS** se todos requisitos atendidos (pode ativar)
- **BT.FAILURE** se qualquer requisito falha

Usado para guiar decisões da IA: "Se pode atacar, ataca. Senão, esquiva."

## Herança

````gdscript
BTTask
 └─ BTCondition
     └─ BTConditionAS_CanActivate
```gdscript

## Propriedades

| Propriedade     | Tipo       | Descrição                                         |
| --------------- | ---------- | ------------------------------------------------- |
| `ability_tag`   | StringName | Tag da ability a validar (ex: &"ability.slash")   |
| `asc_node_path` | NodePath   | Caminho explícito para ASComponent (auto-resolve) |

## Métodos

## Getters

## `get_ability_tag() → StringName` (const)

Retorna tag da ability.

## `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

## Setters

## `set_ability_tag(tag: StringName) → void`

Define tag da ability.

## `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Tick:**

1. Resolve ASComponent
2. Chama: `asc.can_activate_ability_by_tag(ability_tag)`
3. Retorna **BT.SUCCESS** ou **BT.FAILURE**

**Sem Side Effects:** Apenas verifica, não ativa.

## Validações Automáticas

Verifica TODOS os requisitos:

- ✅ Requisitos de tag (TODAS, QUALQUER)
- ✅ Bloqueios por tag (QUALQUER, TODAS)
- ✅ Custos afordáveis
- ✅ Cooldown não ativo
- ✅ Nível suficiente

Se **qualquer** validação falha → **BT.FAILURE**

## Casos de Uso

## Guard Clause

```gdscript
sequence: [
    condition: BTConditionAS_CanActivate
      ability_tag: &"ability.fireball"
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.fireball"
]

# Se não pode ativar fireball:
#   Sequence falha (não tenta ativar)
# Se pode ativar:
#   Ativa fireball, sequence continua
```gdscript

## Decision Logic

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.heavy_attack"
        action: use_heavy_attack
    ],
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.light_attack"
        action: use_light_attack
    ],
    action: move_towards_enemy
]

# Tenta heavy (se disponível) → Se não, light → Se não, move
```gdscript

## Priority Selection

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.ultimate"
        condition: check_enough_fury
        action: use_ultimate
    ],
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.special"
        action: use_special
    ],
    action: use_basic_attack
]

# Prioridade: Ultimate (se pode) > Special > Basic
```gdscript

## Multi-Ability Combos

```gdscript
sequence: [
    condition: BTConditionAS_CanActivate
      ability_tag: &"ability.combo_1"
    action: use_combo_1,

    condition: BTConditionAS_CanActivate
      ability_tag: &"ability.combo_2"
    action: use_combo_2,

    condition: BTConditionAS_CanActivate
      ability_tag: &"ability.combo_3"
    action: use_combo_3
]

# Combo inteiro só executa se TODAS habilidades disponíveis
```gdscript

## Resource-Limited Abilities

```gdscript
# Ability com cost:
# costs: { "mana": 100 }

selector: [
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.expensive_spell"
        action: cast_spell
    ],
    sequence: [
        condition: BTConditionAS_CanActivate
          ability_tag: &"ability.cheap_spell"
        action: cast_cheap_spell
    ],
    action: rest_restore_mana
]

# Se mana insuficiente: condição falha → próxima opção
```gdscript

## Comparação: Condition vs Action

**BTConditionAS_CanActivate:** Valida sem ativar

```gdscript
condition: BTConditionAS_CanActivate
  ability_tag: &"ability.fireball"
# Verifica requisitos
# Retorna true/false
# SEM side effects
```gdscript

**BTActionAS_ActivateAbility:** Ativa (com side effects)

```gdscript
action: BTActionAS_ActivateAbility
  ability_tag: &"ability.fireball"
# Ativa ability
# Consome resources
# Dispara events
# Retorna SUCCESS/FAILURE
```gdscript

**Pattern:** Condition → Action

```gdscript
sequence: [
    condition: can_activate  # Verifica
    action: activate         # Ativa (se condição passou)
]
```gdscript

## Requisitos Possíveis

Ability pode ter qualquer combinação:

```gdscript
# ASAbility requisitos:
activation_required_all_tags: [&"class.warrior"]
activation_required_any_tags: [&"state.empowered"]
activation_blocked_any_tags: [&"state.stunned"]
activation_blocked_all_tags: []

costs: {
  "mana": 50.0,
  "stamina": 25.0
}

cooldown_duration: 2.0
```gdscript

`BTConditionAS_CanActivate` valida tudo isso automaticamente.

## Resolução de ASComponent

Auto-discovery se `asc_node_path` vazio.

## Performance

**Muito Rápido:** Uma validação por tick.

O(1) operação—nenhuma busca ou iteração.

## Casos de Falha

## 1. Cooldown

```gdscript
# Ability disponível agora?
# Cooldown expirado?
# Condição retorna false se cooldown ativo
```gdscript

## 2. Custos Insuficientes

```gdscript
# Mana >= 100 necessário?
# Tem 50 mana?
# Condição falha
```gdscript

## 3. Tags Bloqueadas

```gdscript
# Ability bloqueada por "state.stunned"?
# Tem estado stunned?
# Condição falha
```gdscript

## 4. Tags Faltando

```gdscript
# Ability requer "class.warrior"?
# Não é warrior?
# Condição falha
```gdscript

## Debugging

```gdscript
class_name DebugCanActivateCondition
extends BTConditionAS_CanActivate

func _tick(agent, blackboard):
    var asc = AbilitySystem.resolve_component(agent)
    var can_activate = asc.can_activate_ability_by_tag(ability_tag)
    print("Can activate %s: %s" % [ability_tag, can_activate])

    if not can_activate:
        # Debug why it failed
        print("  Cooldown: %s" % asc.get_ability_cooldown(ability_tag))
        print("  Mana: %s (need 100)" % asc.get_attribute_current_value(&"mana"))
        print("  Has state.stunned: %s" % asc.has_tag(&"state.stunned"))

    return super._tick(agent, blackboard)
```gdscript

## Integração com ASComponent

`can_activate_ability_by_tag` é API pública:

```gdscript
if asc.can_activate_ability_by_tag(&"ability.fireball"):
    print("Pode ativar!")
```gdscript

`BTConditionAS_CanActivate` simplesmente chama isso via Behavior Tree.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Valida ability
- [ASAbility](../resources/asability.md) — Define requisitos
- [BTActionAS_ActivateAbility](btactionas_activateability.md) — Ativa ability
- [BTConditionAS_HasTag](btconditionas_hastag.md) — Valida tag

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
