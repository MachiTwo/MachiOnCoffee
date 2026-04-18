---
title: "BTActionAS_WaitForEvent"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `BTAction` • `LimboAI`

## Descrição Breve

Ação de Behavior Tree que aguarda um evento do Ability System com timeout.

## Descrição Completa

`BTActionAS_WaitForEvent` é um nó de ação que entra em estado **RUNNING** enquanto aguarda um `ASEventTag`. Monitora via
histórico de eventos (`ASTagUtils`) dentro de uma janela de tempo.

**Retorna:**

- **BT.RUNNING** enquanto aguarda
- **BT.SUCCESS** quando evento ocorre
- **BT.FAILURE** após timeout expirado

Usado para sequências sincronizadas: "Ativar ability → aguardar conclusão → próxima ação".

## Herança

```gdscript
BTTask
 └─ BTAction
     └─ BTActionAS_WaitForEvent
```gdscript

## Propriedades

| Propriedade     | Tipo       | Descrição                                                |
| --------------- | ---------- | -------------------------------------------------------- |
| `event_tag`     | StringName | Tag do evento a aguardar (ex: &"event.ability_finished") |
| `time_window`   | float      | Segundos para aguardar antes timeout (padrão: 0.5)       |
| `asc_node_path` | NodePath   | Caminho explícito para ASComponent (auto-resolve)        |

## Métodos

## Getters

## `get_event_tag() → StringName` (const)

Retorna tag do evento.

## `get_time_window() → float` (const)

Retorna timeout em segundos.

## `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

## Setters

## `set_event_tag(tag: StringName) → void`

Define tag do evento.

## `set_time_window(seconds: float) → void`

Define timeout.

## `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Primeira Tick (enter):**

1. Resolve ASComponent
2. Registra timestamp inicial
3. Retorna **BT.RUNNING**

**Ticks Subsequentes:**

1. Verifica histórico de eventos: `ASTagUtils.event_did_occur(event_tag, asc, time_window)`
2. Se evento ocorreu: Retorna **BT.SUCCESS**
3. Se timeout expirado: Retorna **BT.FAILURE**
4. Senão: Retorna **BT.RUNNING**

**Window Time:** Observa histórico nos últimos N segundos (padrão: 0.5s).

## Casos de Uso

## Sincronizar Ativações

```gdscript
behavior_tree = [
    sequence: [
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.charged_attack"
        action: BTActionAS_WaitForEvent
          event_tag: &"event.ability_finished"
          time_window: 3.0  # Espera até 3 segundos
        action: play_victory_animation
    ]
]

# Fluxo:
# 1. Ativa "charged_attack"
# 2. Aguarda até 3s por "ability_finished"
# 3. Se recebe evento dentro 3s → play_victory_animation
# 4. Se timeout → sequence falha
```gdscript

## Combo com Timing

```gdscript
behavior_tree = [
    sequence: [
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.combo_1"
        action: BTActionAS_WaitForEvent
          event_tag: &"event.combo_1_finished"
          time_window: 0.5  # Tight window para combo
        action: BTActionAS_ActivateAbility
          ability_tag: &"ability.combo_2"
        action: BTActionAS_WaitForEvent
          event_tag: &"event.combo_2_finished"
          time_window: 0.5
    ]
]
```gdscript

## Casting com Delay

```gdscript
sequence = [
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.fireball_cast"
    action: BTActionAS_WaitForEvent
      event_tag: &"event.casting_finished"
      time_window: 2.0
    action: apply_damage_to_target
]

# Cast leva até 2s para completar
```gdscript

## Reaction Chain

```gdscript
# Após levar dano, retaliar com timing
sequence = [
    action: BTActionAS_DispatchEvent
      event_tag: &"event.on_damaged"
      magnitude: 50.0
    action: BTActionAS_WaitForEvent
      event_tag: &"event.damage_applied"
      time_window: 1.0
    action: play_stun_animation
]
```gdscript

## Window Time vs Timeout

**`time_window`:** Janela de histórico para verificar evento.

```gdscript
# Espera até 2 segundos
time_window: 2.0

# ASTagUtils verifica se evento ocorreu nos últimos 2 segundos
ASTagUtils.event_did_occur(&"event.damage", asc, 2.0)
```gdscript

**Evento Ocorrido Antes?** Se evento ocorreu ANTES desta ação iniciar:

```gdscript
# Tick 0: ativou ability (dispara event)
# Tick 5: começa wait (5 segundos depois)
# time_window: 0.5

# Verifica últimos 0.5 segundos → evento FORA da window
# Retorna FAILURE (evento já passou)
```gdscript

Use `time_window` suficiente para sua use case.

## Timeout Behavior

Se timeout expirado:

```gdscript
time_window: 1.0
# 1.0 segundo passa sem evento

# Retorna BT.FAILURE
# Sequência interrompida
```gdscript

Para recuperar falha:

```gdscript
selector: [
    sequence: [
        action: ativar_ability,
        action: BTActionAS_WaitForEvent
          time_window: 1.0
    ],
    action: fallback_action  # Se timeout
]
```gdscript

## Performance

**Leve:** Uma chamada ao histórico de eventos por tick (durante RUNNING).

**Histórico Automático:** `ASComponent` mantém buffer circular—sem alocação.

## Resolução de ASComponent

Auto-discovery se `asc_node_path` vazio.

## Sinais

Você pode monitorar conclusão:

```gdscript
# Custom subclass:
class_name OnEventWaitCompleted
extends BTActionAS_WaitForEvent

func _tick(agent, blackboard):
    var result = super._tick(agent, blackboard)
    if result == BT.SUCCESS:
        print("Evento aguardado recebido!")
    elif result == BT.FAILURE:
        print("Timeout—evento não ocorreu")
    return result
```gdscript

## Debugging

```gdscript
class_name DebugWaitForEvent
extends BTActionAS_WaitForEvent

func _tick(agent, blackboard):
    var elapsed = get_elapsed_time()  # Aproximado
    var did_occur = ASTagUtils.event_did_occur(
        event_tag,
        AbilitySystem.resolve_component(agent),
        time_window
    )
    print("Waiting for %s - did_occur: %s, elapsed: %.2f / %.2f" %
          [event_tag, did_occur, elapsed, time_window])
    return super._tick(agent, blackboard)
```gdscript

## Comparação: Wait vs Condition

**BTActionAS_WaitForEvent:** Aguarda em RUNNING

```gdscript
action: BTActionAS_WaitForEvent
  event_tag: &"event.finished"
  time_window: 2.0
# Bloqueia execução até evento ou timeout
```gdscript

**BTConditionAS_EventOccurred:** Verifica instantaneamente

```gdscript
condition: BTConditionAS_EventOccurred
  event_tag: &"event.finished"
# Retorna true/false imediatamente (não aguarda)
```gdscript

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Dispara evento
- [ASTagUtils](../refcounted/astagutils.md) — Histórico de eventos
- [BTActionAS_DispatchEvent](btactionas_dispatchevent.md) — Dispara evento
- [BTConditionAS_EventOccurred](btconditionas_eventoccurred.md) — Verifica evento
- [BTActionAS_ActivateAbility](btactionas_activateability.md) — Ativa ability

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
