---
title: "ASAbilityPhase"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASAbilityPhase

**Badge:** `Resource` (herda de ASAbility)

## Descrição Breve

Define uma fase granular de execução de uma ability.

## Descrição Completa

`ASAbilityPhase` é uma especialização de `ASAbility` que representa um estágio específico de execução. Abilities complexas podem ser divididas em múltiplas fases sequenciais, cada uma com:

- **Duração**: Tempo da fase em segundos
- **Effects Transitórios**: Aplicados apenas durante esta fase
- **Triggers de Avanço**: Avança por tempo ou por evento (ex: animation frame)

**Exemplo de Charged Strike:**

```
Windup (200ms)
  ├─ Aplica: state.charging
  └─ Avança por tempo

Execution (50ms)
  ├─ Aplica: Damage effect
  └─ Avança por tempo

Recovery (250ms)
  ├─ Sem effects transitórios
  └─ Retorna a normal
```

## Herança

```
Resource
 └─ ASAbility
     └─ ASAbilityPhase
```

## Propriedades (Fase-Específicas)

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `phase_duration` | float | `0.0` | Duração desta fase em segundos |
| `granted_tags` | StringName[] | `[]` | Tags aplicadas durante fase |
| `transition_trigger` | StringName | `&""` | Event que dispara avanço (opcional) |
| `effects` | ASEffect[] | `[]` | Effects aplicados apenas nesta fase |

Herda de `ASAbility`, então também tem:

- `ability_tag`, `ability_name`
- `activation_required_all_tags`, etc
- `costs`, `requirements`

## Métodos

Herdados de `ASAbility`. Nenhum método específico de fase.

## Casos de Uso

### Charged Attack (3 Phases)

```gdscript
var charged_strike = ASAbility.new()
charged_strike.ability_tag = &"ability.charged_strike"
charged_strike.ability_duration_policy = ASAbility.POLICY_DURATION
charged_strike.ability_duration = 0.5  # Total 500ms

# Fase 1: Windup (200ms)
var windup = ASAbilityPhase.new()
windup.phase_duration = 0.2
windup.granted_tags.append(&"state.charging")
windup.granted_tags.append(&"state.immobile")
charged_strike.phases.append(windup)

# Fase 2: Execution (50ms—hit frame)
var execution = ASAbilityPhase.new()
execution.phase_duration = 0.05
execution.effects.append(heavy_damage_effect)
execution.effects.append(knockback_effect)
charged_strike.phases.append(execution)

# Fase 3: Recovery (250ms)
var recovery = ASAbilityPhase.new()
recovery.phase_duration = 0.25
# Sem effects—retorna a normal
charged_strike.phases.append(recovery)
```

### Channeled Spell (2 Phases)

```gdscript
var channel_spell = ASAbility.new()
channel_spell.ability_tag = &"ability.channel_spell"

# Fase 1: Charging (1.5s)
var charging = ASAbilityPhase.new()
charging.phase_duration = 1.5
charging.granted_tags.append(&"state.channeling")
charging.effects.append(mana_drain_effect)  # Perde mana por segundo
channel_spell.phases.append(charging)

# Fase 2: Cast (0.5s—release)
var cast = ASAbilityPhase.new()
cast.phase_duration = 0.5
cast.effects.append(massive_damage_effect)
cast.effects.append(stun_effect)
cast.transition_trigger = &"animation.cast_finished"
channel_spell.phases.append(cast)
```

### Multi-Hit Combo (4 Phases)

```gdscript
var combo = ASAbility.new()
combo.ability_tag = &"ability.combo"

var damages = [light_damage, light_damage, medium_damage, heavy_damage]
var durations = [0.3, 0.3, 0.3, 0.4]
var tags = [
    &"state.attacking.hit1",
    &"state.attacking.hit2",
    &"state.attacking.hit3",
    &"state.attacking.hit4"
]

for i in range(4):
    var phase = ASAbilityPhase.new()
    phase.phase_duration = durations[i]
    phase.granted_tags.append(tags[i])
    phase.effects.append(damages[i])
    phase.transition_trigger = &"animation.hit_frame_%d" % (i + 1)
    combo.phases.append(phase)
```

## Integração com ASComponent

```gdscript
# ASComponent gerencia phases automaticamente
# Avança por:
# 1. Tempo (phase_duration expirado)
# 2. Evento (transition_trigger recebido)

func _on_ability_activated(tag: StringName):
    print("Ability %s ativada (fase 0)" % tag)

func _on_tag_added(tag: StringName):
    # Tag de fase foi adicionada
    if tag == &"state.charging":
        play_charging_animation()
    elif tag == &"state.attacking.hit1":
        play_first_hit_animation()
```

## Lifecycle da Fase

```
Ativa (fase 0)
  ├─ Aplicar effects da fase
  ├─ Aplicar granted_tags
  │
  └─ Aguardar avanço
      ├─ Opção 1: Timer (phase_duration)
      └─ Opção 2: Event (transition_trigger)

Avança para próxima fase
  ├─ Remove effects/tags da fase anterior
  ├─ Aplica novo effects/tags
  └─ Repete...

Termina (última fase)
  ├─ Remove effects/tags finais
  ├─ Emite ability_ended signal
  └─ Cooldown inicia
```

## Referências Relacionadas

- [ASAbility](asability.md) — Classe base
- [ASAbilitySpec](../refcounted/asabilityspec.md) — Rastreia fase atual
- [ASEffect](aseffect.md) — Effects da fase
- [ASComponent](../nodes/ascomponent.md) — Orquestra phases

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
