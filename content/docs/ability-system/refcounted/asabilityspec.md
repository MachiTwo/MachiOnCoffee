---
title: "ASAbilitySpec"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `RefCounted`

## Descrição Breve

Instância runtime de uma ability em execução.

## Descrição Completa

`ASAbilitySpec` é uma instância leve que representa uma ability ativa. Mantém:

- **Estado de Ativação**: Se está ativa, em cooldown, ou disponível
- **Duração**: Tempo restante até término
- **Cooldown**: Tempo restante até poder ativar novamente
- **Fase Atual**: Índice da fase em execução (se multi-fase)
- **Level**: Nível da ability (para scaling de modificadores)

O Resource `ASAbility` é imutável e compartilhado. O Spec é a instância mutável individual.

## Herança

```gdscript
RefCounted
 └─ ASAbilitySpec
```gdscript

## Métodos Públicos

## Status

## `is_active() → bool` (const)

Retorna se ability está em execução.

```gdscript
if spec.is_active():
    print("Ability está acontecendo agora")
```gdscript

## `is_on_cooldown() → bool` (const)

Retorna se ability está em cooldown (não pode ativar).

## Duração

## `get_duration_remaining() → float` (const)

Tempo restante até término da ability.

**Exemplo:**

```gdscript
var remaining = spec.get_duration_remaining()
if remaining < 0.5:
    print("Ability terminando em breve")
```gdscript

## Cooldown

## `get_cooldown_remaining() → float` (const)

Tempo restante antes de poder ativar novamente.

**Exemplo:**

```gdscript
var cooldown = spec.get_cooldown_remaining()
if cooldown > 0:
    ui.show_cooldown_timer(cooldown)
```gdscript

## Fases (Multi-Phase Abilities)

## `get_current_phase_index() → int` (const)

Índice da fase atual (0-based).

**Exemplo:**

```gdscript
var phase_idx = spec.get_current_phase_index()
if phase_idx == 0:
    print("Fase de windup")
elif phase_idx == 1:
    print("Fase de execução")
```gdscript

## `get_current_phase() → ASAbilityPhase` (const)

Resource da fase atual.

## `get_phase_duration_remaining() → float` (const)

Tempo restante na fase atual.

---

## Casos de Uso

## Verificar Cooldown na UI

```gdscript
func _process(_delta):
    if not asc.has_unlocked_ability(&"ability.slash"):
        return

    var spec = asc.get_ability_spec(&"ability.slash")
    if spec.is_on_cooldown():
        var cd = spec.get_cooldown_remaining()
        ui.update_cooldown_display(&"ability.slash", cd)
    else:
        ui.clear_cooldown_display(&"ability.slash")
```gdscript

## Multi-Phase Ability Animation

```gdscript
func _process(_delta):
    var spec = asc.get_active_ability_spec()
    if not spec:
        return

    var phase_idx = spec.get_current_phase_index()

    if phase_idx == 0:
        # Windup: play charging animation
        animation.play("charge")
    elif phase_idx == 1:
        # Execution: play impact
        animation.play("impact")
    elif phase_idx == 2:
        # Recovery: return to idle
        animation.play("idle")
```gdscript

## Interrupt on Cooldown Start

```gdscript
func _on_ability_activated(tag: StringName):
    var spec = asc.get_ability_spec(tag)
    if spec:
        var cooldown = spec.get_cooldown_remaining()
        if cooldown > 0:
            start_ability_cooldown_feedback(tag, cooldown)
```gdscript

---

## Referências Relacionadas

- [ASAbility](../resources/asability.md) — Resource imutável
- [ASAbilityPhase](../resources/asabilityphase.md) — Fase em execução
- [ASComponent](../nodes/ascomponent.md) — Gerencia specs
- [ASEffectSpec](aseffectspec.md) — Instância de effect

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
