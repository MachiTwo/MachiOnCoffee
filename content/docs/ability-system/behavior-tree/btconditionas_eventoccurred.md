---
title: "BTConditionAS_EventOccurred"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# BTConditionAS_EventOccurred

**Badge:** `BTCondition` • `LimboAI`

## Descrição Breve

Condição de Behavior Tree que verifica se um evento ocorreu recentemente.

## Descrição Completa

`BTConditionAS_EventOccurred` consulta o histórico de eventos via `ASTagUtils.event_did_occur()` dentro de uma janela de
tempo.

**Retorna:**

- **BT.SUCCESS** se evento ocorreu nos últimos N segundos
- **BT.FAILURE** se evento não encontrado no histórico

Usado para reações baseadas em eventos: "Se tomou dano há pouco, retreate. Se venceu inimigo, comemora."

## Herança

```
BTTask
 └─ BTCondition
     └─ BTConditionAS_EventOccurred
```

## Propriedades

| Propriedade     | Tipo       | Descrição                                         |
| --------------- | ---------- | ------------------------------------------------- |
| `event_tag`     | StringName | Evento a verificar (ex: &"event.on_hit")          |
| `time_window`   | float      | Histórico a verificar em segundos (padrão: 1.0)   |
| `asc_node_path` | NodePath   | Caminho explícito para ASComponent (auto-resolve) |

## Métodos

### Getters

#### `get_event_tag() → StringName` (const)

Retorna tag do evento.

#### `get_time_window() → float` (const)

Retorna janela de tempo.

#### `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

### Setters

#### `set_event_tag(tag: StringName) → void`

Define tag do evento.

#### `set_time_window(seconds: float) → void`

Define janela (em segundos).

#### `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Tick:**

1. Resolve ASComponent
2. Verifica histórico: `ASTagUtils.event_did_occur(event_tag, asc, time_window)`
3. Retorna **BT.SUCCESS** ou **BT.FAILURE**

**Histórico:** Consulta buffer automático de últimos N segundos.

## Time Window

Representa quantos segundos olhar para trás:

```gdscript
time_window: 0.5   # Últimos 0.5 segundos
time_window: 2.0   # Últimos 2.0 segundos
time_window: 10.0  # Últimos 10.0 segundos
```

## Casos de Uso

### Reação a Dano

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_EventOccurred
          event_tag: &"event.take_damage"
          time_window: 0.5
        action: play_pain_animation
    ],
    action: idle
]

# Se tomou dano nos últimos 0.5s → pain anim
# Senão → idle
```

### Combate Responsivo

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_EventOccurred
          event_tag: &"event.parried"
          time_window: 0.2
        action: counter_attack
    ],
    action: continue_attacking
]

# Se parrou nos últimos 0.2s → contra-ataca
# Senão → continua
```

### Multi-Evento Logic

```gdscript
sequence: [
    condition: BTConditionAS_EventOccurred
      event_tag: &"event.took_damage"
      time_window: 1.0
    condition: BTConditionAS_EventOccurred
      event_tag: &"event.health_below_50"
      time_window: 0.5
    action: activate_emergency_heal
]

# Se tomou dano recente E saúde baixa → heal
```

### Boss Phase Transition

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_EventOccurred
          event_tag: &"event.player_hit_three_times"
          time_window: 2.0
        action: phase_2_attack
    ],
    action: phase_1_attack
]

# Após 3 hits em 2 segundos → mudar fase
```

### Chaining Events

```gdscript
sequence: [
    action: BTActionAS_DispatchEvent
      event_tag: &"event.trigger_combo",
    action: wait_0.1_seconds,
    condition: BTConditionAS_EventOccurred
      event_tag: &"event.trigger_combo"
      time_window: 0.2  # Verifica se ainda no histórico
    action: continue_combo
]

# Verifica se próprio evento ainda está em histórico
```

## Window Time Importante

**Muito Pequena:** Pode perder eventos

```gdscript
time_window: 0.1  # Apenas 100ms
# Evento ocorreu 150ms atrás?
# Já fora do histórico → falha
```

**Muito Grande:** Muitos falsos positivos

```gdscript
time_window: 60.0  # 1 minuto inteiro
# Dano tomado há 50s atrás?
# Ainda conta como recente → pode ser indesejado
```

**Bom:** Baseado em use case

```gdscript
# Para reações imediatas: 0.2s - 0.5s
# Para combate normal: 1.0s - 2.0s
# Para eventos duráveis: 5.0s+
```

## Histórico Automático

`ASComponent` mantém histórico:

```gdscript
# Interno:
event_history = {
    &"event.on_hit": { timestamp, magnitude, payload },
    &"event.on_damage": { timestamp, magnitude, payload },
    # ...
}

# TTL automático: remove eventos após 60s (configurável)
```

## Resolução de ASComponent

Auto-discovery se `asc_node_path` vazio.

## Magnitudes

Se quiser verificar por valor:

```gdscript
# Conseguir magnitude do evento:
var last_magnitude = ASTagUtils.event_get_last_magnitude(&"event.damage", asc)
if last_magnitude > 50:
    # Dano > 50: retreate
    action_retreat()
```

Mas `BTConditionAS_EventOccurred` apenas verifica **ocorrência**, não magnitude.

## Debugging

```gdscript
class_name DebugEventOccurredCondition
extends BTConditionAS_EventOccurred

func _tick(agent, blackboard):
    var asc = AbilitySystem.resolve_component(agent)
    var occurred = ASTagUtils.event_did_occur(event_tag, asc, time_window)
    print("Event %s occurred in last %.2fs: %s" % [event_tag, time_window, occurred])

    if occurred:
        var magnitude = ASTagUtils.event_get_last_magnitude(event_tag, asc)
        print("  Last magnitude: %.2f" % magnitude)

    return super._tick(agent, blackboard)
```

## Comparação: Condition vs Action

**BTConditionAS_EventOccurred:** Verifica histórico

```gdscript
condition: BTConditionAS_EventOccurred
  event_tag: &"event.parried"
  time_window: 0.5
# Apenas verifica se evento já ocorreu
# Retorna true/false
```

**BTActionAS_WaitForEvent:** Aguarda evento

```gdscript
action: BTActionAS_WaitForEvent
  event_tag: &"event.parried"
  time_window: 0.5
# Entra em RUNNING até evento ocorrer
# Bloqueia execução
```

## Casos de Uso Avançado

### Reactive Chain

```gdscript
selector: [
    sequence: [
        condition: BTConditionAS_EventOccurred
          event_tag: &"event.hit_by_fire"
          time_window: 1.0
        action: take_water,
    ],
    action: continue_fight
]

# Se foi atingido por fogo recente → toma água
```

### Stateful Logic

```gdscript
sequence: [
    action: attack_enemy,
    action: BTActionAS_DispatchEvent
      event_tag: &"event.attack_completed",
    action: wait_0.5s,
    condition: BTConditionAS_EventOccurred
      event_tag: &"event.counter_detected"
      time_window: 1.0
    action: dodge_counter
]

# Verifica se inimigo contra-atacou durante espera
```

## Integração com ASComponent

`event_did_occur` é API pública:

```gdscript
if ASTagUtils.event_did_occur(&"event.damage", asc, 1.0):
    print("Tomou dano recentemente")
```

`BTConditionAS_EventOccurred` simplesmente chama isso via Behavior Tree.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Mantém histórico
- [ASTagUtils](../refcounted/astagutils.md) — Consulta histórico
- [BTActionAS_DispatchEvent](btactionas_dispatchevent.md) — Dispara evento
- [BTActionAS_WaitForEvent](btactionas_waitforevent.md) — Aguarda evento

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
