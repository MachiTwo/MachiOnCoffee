---
title: "BTActionAS_ActivateAbility"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `BTAction` • `LimboAI`

## Descrição Breve

Ação de Behavior Tree que ativa uma ability via Ability System.

## Descrição Completa

`BTActionAS_ActivateAbility` é um nó de ação que chama `ASComponent.try_activate_ability_by_tag()` com validação
automática de requisitos.

**Retorna:**

- **BT.SUCCESS** se ability ativada com sucesso
- **BT.FAILURE** se requisitos não atendidos (cooldown, custos, tags bloqueadas)

Respeita todos os requisitos: tags de ativação, cooldowns, custos, nível.

## Herança

````gdscript
BTTask
 └─ BTAction
     └─ BTActionAS_ActivateAbility
```gdscript

## Propriedades

| Propriedade        | Tipo       | Descrição                                         |
| ------------------ | ---------- | ------------------------------------------------- |
| `ability_tag`      | StringName | Tag da ability a ativar (ex: &"ability.fireball") |
| `activation_level` | float      | Power level da ativação (padrão: 1.0)             |
| `asc_node_path`    | NodePath   | Caminho explícito para ASComponent (auto-resolve) |

## Métodos

## Getters

## `get_ability_tag() → StringName` (const)

Retorna tag da ability.

## `get_activation_level() → float` (const)

Retorna power level.

## `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

## Setters

## `set_ability_tag(tag: StringName) → void`

Define tag da ability.

## `set_activation_level(level: float) → void`

Define power level para scaling.

## `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Tick (enter):**

1. Resolve ASComponent
2. Valida se pode ativar: `asc.can_activate_ability_by_tag(ability_tag)`
3. Se válido: Ativa `asc.try_activate_ability_by_tag(ability_tag, activation_level)`
4. Retorna **BT.SUCCESS** ou **BT.FAILURE**

**Validações Automáticas:**

- ❌ Requisitos não atendidos (tags, attributes)
- ❌ Cooldown ativo
- ❌ Custos não afordáveis
- ❌ Bloqueado por tags

Se qualquer validação falhar → **BT.FAILURE**

## Casos de Uso

## Sequência Simples

```gdscript
behavior_tree = [
    sequence: [
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.slash",
        action: play_animation(&"slash")
    ]
]

# Ativa "slash" → Se sucesso, anima
# Se falhar (cooldown?), sequence inteira falha
```gdscript

## Selector com Fallback

```gdscript
selector: [
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.fireball"  # Primary
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.fire_bolt" # Secondary
    action: move_towards_enemy           # Fallback
]

# Tenta fireball → Se falhar, fire_bolt → Se falhar, move
```gdscript

## Ativação com Level Scale

```gdscript
behavior_tree = [
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.explosive_strike"
      activation_level: 2.0  # Double damage
]

# Ativa com level 2.0 (damage scaling, duration scaling, etc)
```gdscript

## Boss Ability Rotation

```gdscript
selector: [
    sequence: [
        condition: has_high_health,
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.heal_self"
    ],
    sequence: [
        condition: player_in_range,
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.aoe_blast"
    ],
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.basic_attack"
]

# Boss escolhe ability baseado em condições
```gdscript

## Validação de Requisitos

Ability define próprios requisitos:

```gdscript
# ASAbility:
activation_required_all_tags: [&"class.warrior"]
activation_required_any_tags: []
activation_blocked_any_tags: [&"state.stunned"]
activation_blocked_all_tags: []

costs: {
  "mana": 20.0
}

cooldown_duration: 2.0
```gdscript

`BTActionAS_ActivateAbility` valida TUDO automaticamente.

## Resolução de ASComponent

**Auto-discovery:** Se `asc_node_path` vazio:

1. Usa agent do behavior tree
2. `AbilitySystem.resolve_component(agent)`
3. Busca em order: self → children → parent → owner

**Explicit Path:** Se `asc_node_path` fornecido:

```gdscript
asc_node_path: NodePath("Subnode/AbilityComponent")
# Busca caminho específico relativo ao agent
```gdscript

## Integração com ASComponent

Chamadas internas:

```gdscript
# Valida:
if asc.can_activate_ability_by_tag(ability_tag):
    # Ativa:
    asc.try_activate_ability_by_tag(ability_tag, activation_level)
    return BT.SUCCESS
else:
    return BT.FAILURE
```gdscript

Sinais de `ASComponent` emitidos:

```gdscript
asc.ability_activated.emit(spec)  # Se sucesso
asc.ability_failed.emit(ability_tag)  # Se falha
```gdscript

## Debugging

```gdscript
class_name DebugActivateAbilityAction
extends BTActionAS_ActivateAbility

func _tick(agent, blackboard):
    var asc = AbilitySystem.resolve_component(agent)
    var can_activate = asc.can_activate_ability_by_tag(ability_tag)
    print("Attempting ability: %s - Can activate: %s" % [ability_tag, can_activate])

    var result = super._tick(agent, blackboard)
    print("Result: %s" % BT.status_to_string(result))
    return result
```gdscript

## Performance

**Muito Rápido:** Uma validação + uma ativação por tick.

O(1) operação—nenhuma busca ou iteração.

## Comparação: Action vs Condition

**BTActionAS_ActivateAbility:** Ativa (side effects)

```gdscript
action: BTActionAS_ActivateAbility
  ability_tag: &"ability.fireball"
# Ativa fireball IMEDIATAMENTE, consumindo recursos
# Retorna SUCCESS/FAILURE baseado validação
```gdscript

**BTConditionAS_CanActivate:** Valida apenas

```gdscript
condition: BTConditionAS_CanActivate
  ability_tag: &"ability.fireball"
# Verifica se PODE ativar (sem efeitos colaterais)
# Retorna true/false—NÃO ativa
```gdscript

## Casos de Falha Comum

## 1. Ability Não Registrada

```gdscript
ability_tag: &"ability.unknown_attack"
# AbilitySystem não tem recurso
# Resultado: BT.FAILURE
```gdscript

**Fix:** Registre ability em ASContainer ou globalmente.

## 2. Cooldown Ativo

```gdscript
# Ability tem cooldown_duration: 2.0
# Apenas ativada 0.5 segundos atrás
# Resultado: BT.FAILURE
```gdscript

**Fix:** Aguarde com `BTActionAS_WaitForEvent` ou verifique com `BTConditionAS_CanActivate`.

## 3. Custos Insuficientes

```gdscript
# Ability custa 100 mana
# Personagem tem 50 mana
# Resultado: BT.FAILURE
```gdscript

**Fix:** Verifique atributos antes com condição customizada.

## 4. Bloqueado por Tag

```gdscript
# Ability tem activation_blocked_any_tags: [&"state.stunned"]
# Personagem tem estado "stunned"
# Resultado: BT.FAILURE
```gdscript

**Fix:** Remova estado bloqueador antes.

## Integração em Sequências

```gdscript
# Padrão: Checar → Ativar → Animar
sequence: [
    condition: BTConditionAS_CanActivate
      ability_tag: &"ability.special"
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.special"
    action: play_animation
]

# Se condição falha, sequence inteira pula
# Se ativação falha, sequence falha
```gdscript

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Ativa ability
- [ASAbility](../resources/asability.md) — Definição
- [BTConditionAS_CanActivate](btconditionas_canactivate.md) — Valida sem ativar
- [BTActionAS_WaitForEvent](btactionas_waitforevent.md) — Aguarda conclusão
- [BTActionAS_DispatchEvent](btactionas_dispatchevent.md) — Dispara evento

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
