---
title: "BTActionAS_DispatchEvent"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# BTActionAS_DispatchEvent

**Badge:** `BTAction` • `LimboAI`

## Descrição Breve

Ação de Behavior Tree que dispara um evento do Ability System.

## Descrição Completa

`BTActionAS_DispatchEvent` chama `ASComponent.dispatch_event()` com tag, magnitude e payload customizado.

**Retorna:** **BT.SUCCESS** imediatamente após dispatch (sincronizado).

Usado para comunicação entre sistemas: habilidades dispararem eventos que triggerm outras reações.

## Herança

```
BTTask
 └─ BTAction
     └─ BTActionAS_DispatchEvent
```

## Propriedades

| Propriedade      | Tipo       | Descrição                                         |
| ---------------- | ---------- | ------------------------------------------------- |
| `event_tag`      | StringName | Evento a disparar (ex: &"event.on_damaged")       |
| `magnitude`      | float      | Valor associado (ex: 30.0 dano)                   |
| `custom_payload` | Dictionary | Dados adicionais como key-value                   |
| `asc_node_path`  | NodePath   | Caminho explícito para ASComponent (auto-resolve) |

## Métodos

### Getters

#### `get_event_tag() → StringName` (const)

Retorna tag do evento.

#### `get_magnitude() → float` (const)

Retorna magnitude.

#### `get_custom_payload() → Dictionary` (const)

Retorna payload customizado.

#### `get_asc_node_path() → NodePath` (const)

Retorna caminho customizado.

### Setters

#### `set_event_tag(tag: StringName) → void`

Define tag do evento.

#### `set_magnitude(mag: float) → void`

Define magnitude.

#### `set_custom_payload(payload: Dictionary) → void`

Define payload customizado.

#### `set_asc_node_path(path: NodePath) → void`

Define caminho para ASComponent.

## Comportamento de Execução

**Tick (enter):**

1. Resolve ASComponent
2. Dispara evento: `asc.dispatch_event(event_tag, magnitude, custom_payload)`
3. Evento registrado no histórico do ASComponent
4. Retorna **BT.SUCCESS** imediatamente

**Síncronamente Executado:** Não aguarda listeners responderem.

## Casos de Uso

### Sinalizar Conclusão de Ability

```gdscript
sequence: [
    action: BTActionAS_ActivateAbility
      ability_tag: &"ability.fireball_cast"
    action: BTActionAS_DispatchEvent
      event_tag: &"event.ability_completed"
      magnitude: 1.0
    action: play_cooldown_animation
]

# Dispara evento que outros systems podem escutar
# Ex: Triggers damage application, visual feedback, etc
```

### Sinalizar Dano Tomado

```gdscript
action: BTActionAS_DispatchEvent
  event_tag: &"event.take_damage"
  magnitude: 25.0  # Dano em HP

# AI behaviors podem escutar:
# "Se receber dano > 50 → retreater"
```

### Sinalizar Estado Crítico

```gdscript
sequence: [
    condition: health_below_25_percent,
    action: BTActionAS_DispatchEvent
      event_tag: &"event.critical_health"
      magnitude: 0.2  # 20% HP
]

# Triggers: Música mudar, inimigos agressivos, etc
```

### Disparo com Payload Customizado

```gdscript
action: BTActionAS_DispatchEvent
  event_tag: &"event.boss_phase_change"
  magnitude: 2.0
  custom_payload: {
    "phase_name": "Enraged",
    "new_attack_pattern": "aggressive",
    "shield_active": true
  }

# Listeners recebem dados estruturados
```

### Coordenar Múltiplos NPCs

```gdscript
# Boss dispara:
action: BTActionAS_DispatchEvent
  event_tag: &"event.boss_summon_minions"
  magnitude: 5.0  # 5 minions

# Outros NPCs escutam e respondem:
# listener: on_event_boss_summon_minions(magnitude=5.0)
#   spawn 5 minions
#   coordinate attack formation
```

## Magnitude vs Payload

**Magnitude:** Número simples (damage, healing, count, intensity)

```gdscript
magnitude: 30.0  # 30 damage
magnitude: 0.5   # 50% slow
magnitude: 3.0   # 3 stuns
```

**Payload:** Dados estruturados complexos

```gdscript
custom_payload: {
  "source": "fire_trap",
  "location": Vector3(10, 0, 20),
  "damage_type": "fire",
  "crit_chance": 0.25
}
```

Use magnitude para valores simples, payload para estruturas.

## Histórico de Eventos

Após dispatch, evento registrado no `ASComponent.event_history`:

```gdscript
# Dentro ASComponent:
event_history[event_tag] = {
  "magnitude": magnitude,
  "payload": custom_payload,
  "timestamp": get_ticks_msec()
}

# Consultável via ASTagUtils:
ASTagUtils.event_did_occur(&"event.on_damaged", asc, 1.0)
ASTagUtils.event_get_last_magnitude(&"event.on_damaged", asc)
```

## Resolução de ASComponent

Auto-discovery se `asc_node_path` vazio.

## Casos de Uso Avançado

### Trigger Chain

```gdscript
sequence: [
    action: BTActionAS_DispatchEvent
      event_tag: &"event.trigger_1",
    action: wait_one_frame,
    action: BTActionAS_DispatchEvent
      event_tag: &"event.trigger_2",
    action: wait_one_frame,
    action: BTActionAS_DispatchEvent
      event_tag: &"event.trigger_3"
]

# Cadeia de eventos sequenciais
```

### Conditional Dispatch

```gdscript
selector: [
    sequence: [
        condition: health_above_50_percent,
        action: BTActionAS_DispatchEvent
          event_tag: &"event.idle_chatter"
    ],
    sequence: [
        condition: health_below_20_percent,
        action: BTActionAS_DispatchEvent
          event_tag: &"event.death_cry"
    ]
]

# Dispara diferentes eventos baseado em contexto
```

### Synchronizing with Animations

```gdscript
sequence: [
    action: play_attack_animation,
    action: wait_for_animation_frame(15),  # Frame 15
    action: BTActionAS_DispatchEvent
      event_tag: &"event.attack_hit"
      magnitude: current_damage
]

# Garante dano aplicado no frame visual correto
```

## Performance

**Instantâneo:** O(1) dispatch + O(1) histórico registration.

Nenhuma busca ou iteração.

## Debugging

```gdscript
class_name DebugDispatchAction
extends BTActionAS_DispatchEvent

func _tick(agent, blackboard):
    print("Dispatching event: %s (magnitude: %.2f)" % [event_tag, magnitude])
    var result = super._tick(agent, blackboard)
    print("Dispatch complete")
    return result
```

## Listeners

Você pode escutar eventos via `ASComponent` ou `ASTagUtils`:

```gdscript
# Via ASComponent sinais:
asc.event_occurred.connect(_on_event)

# Via ASTagUtils query:
if ASTagUtils.event_did_occur(&"event.on_hit", asc, 0.5):
    # Evento ocorreu nos últimos 0.5 segundos
```

## Integração com ASComponent

`dispatch_event` é API pública:

```gdscript
asc.dispatch_event(
    &"event.custom",
    50.0,
    {"extra": "data"}
)
```

`BTActionAS_DispatchEvent` simplesmente chama isso via Behavior Tree.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Dispara evento
- [ASTagUtils](../refcounted/astagutils.md) — Histórico de eventos
- [BTActionAS_WaitForEvent](btactionas_waitforevent.md) — Aguarda evento
- [BTConditionAS_EventOccurred](btconditionas_eventoccurred.md) — Verifica evento

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
