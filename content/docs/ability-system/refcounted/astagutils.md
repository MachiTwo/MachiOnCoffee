---
title: "ASTagUtils"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASTagUtils

**Badge:** `RefCounted` (Namespace/Utilities)

## Descrição Breve

Utilitários de manipulação histórica e consultaa de tags.

## Descrição Completa

`ASTagUtils` fornece métodos estáticos otimizados para consultar o histórico de mudanças de tags em um ator. Permite
verificar:

- Se uma tag foi adicionada/removida recentemente
- Se um evento ocorreu nos últimos N segundos
- Magnitudes e instigadores de eventos
- Histórico completo de mudanças

O `ASComponent` mantém buffers circulares separados para cada tipo de tag (NAME, CONDITIONAL, EVENT), com até 128
entradas cada.

## Métodos Estáticos

### Consultas de Tag NAME

#### `name_was_tag_added(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag NAME foi adicionada nos últimos N segundos.

```gdscript
if ASTagUtils.name_was_tag_added(&"state.stunned", target, 1.0):
    print("Ficou atordoado recentemente")
```

#### `name_was_tag_removed(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag NAME foi removida recentemente.

#### `name_had_tag(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag NAME existia em qualquer ponto do intervalo.

#### `name_get_recent_additions(target: ASComponent, lookback_seconds: float) → StringName[]`

Lista todas as tags NAME adicionadas recentemente.

#### `name_count_additions(tag: StringName, target: ASComponent, lookback_seconds: float) → int`

Conta quantas vezes tag NAME foi adicionada.

### Consultas de Tag CONDITIONAL

#### `cond_was_tag_added(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag CONDITIONAL foi adicionada.

#### `cond_was_tag_removed(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag CONDITIONAL foi removida.

#### `cond_had_tag(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se tag CONDITIONAL existia.

### Consultas de Tag EVENT

#### `event_did_occur(event_tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Verifica se evento ocorreu recentemente.

```gdscript
if ASTagUtils.event_did_occur(&"event.hit", target, 0.5):
    print("Tomou hit nos últimos 500ms")
```

#### `event_get_recent_events(event_tag: StringName, target: ASComponent, lookback_seconds: float) → Dictionary[]`

Lista todos os eventos recentes com payload completo.

#### `event_get_all_recent_events(target: ASComponent, lookback_seconds: float) → Dictionary[]`

Lista TODOS os eventos que ocorreram.

#### `event_get_last_data(event_tag: StringName, target: ASComponent) → Dictionary`

Recupera dados completos do último evento.

```gdscript
var hit_data = ASTagUtils.event_get_last_data(&"event.damage", target)
var damage_amount = hit_data.get("magnitude", 0.0)
var attacker = hit_data.get("instigator")
```

#### `event_get_last_magnitude(event_tag: StringName, target: ASComponent) → float`

Magnitude do último evento (ex: dano).

#### `event_get_last_instigator(event_tag: StringName, target: ASComponent) → Object`

Quem causou o último evento (ex: atacante).

#### `event_count_occurrences(event_tag: StringName, target: ASComponent, lookback_seconds: float) → int`

Quantas vezes evento ocorreu.

### Consultas Unificadas

#### `history_was_tag_present(tag: StringName, target: ASComponent, lookback_seconds: float) → bool`

Funciona com qualquer tipo de tag (detecção automática).

#### `history_get_tag_history(tag: StringName, target: ASComponent, lookback_seconds: float) → Dictionary[]`

Retorna histórico completo de mudanças de tag.

#### `history_get_all_changes(target: ASComponent, lookback_seconds: float) → Dictionary[]`

Retorna TODAS as mudanças (tags + eventos).

#### `history_dump(target: ASComponent, lookback_seconds: float) → String`

Debug: retorna dump legível do histórico.

## Casos de Uso

### Counter-Attack Reativo

```gdscript
# Parry ativa se foi atacado nos últimos 500ms
var parry = ASAbility.new()

func can_activate_parry(asc: ASComponent) -> bool:
    return ASTagUtils.event_did_occur(&"event.incoming_damage", asc, 0.5)

func _process(_delta):
    if can_activate_parry(asc):
        asc.try_activate_ability_by_tag(&"ability.parry")
```

### Elemental Chain Reaction

```gdscript
# Spell que funciona só se alvo foi queimado recentemente
func cast_cold_explosion(target: ASComponent):
    if ASTagUtils.name_was_tag_added(&"state.burning", target, 2.0):
        # Queimado recentemente—aplica damage extra
        apply_effect(target, intense_cold_effect)
    else:
        # Sem burn—damage normal
        apply_effect(target, normal_cold_effect)
```

### Consecutive Hit Bonus

```gdscript
# Damage sobe se acertou múltiplos hits seguidos
func calculate_damage(target: ASComponent) -> float:
    var hit_count = ASTagUtils.event_count_occurrences(&"event.hit", target, 1.0)
    var base_damage = 30.0
    return base_damage * (1.0 + hit_count * 0.1)  # +10% per hit
```

### Disarm on Stun

```gdscript
# Se foi atordoado, remove a ability de atacar
func _on_stunned(target: ASComponent):
    if not ASTagUtils.cond_was_tag_added(&"state.stunned", target, 0.1):
        return

    # Certeza de que foi AGORA que ficou atordoado
    target.add_tag(&"state.disarmed")
```

### Retaliation Trigger

```gdscript
# Trigger automático: retaliar se sofreu damage
var retaliate = ASAbility.new()

func check_trigger_retaliate(target: ASComponent):
    if ASTagUtils.event_get_last_instigator(&"event.damage", target):
        var attacker = ASTagUtils.event_get_last_instigator(&"event.damage", target)

        # Contra-atacar o atacante
        target.try_activate_ability_by_tag(&"ability.retaliate")
```

### Combo Reset Timer

```gdscript
# Combo reseta se não acertou nada nos últimos 2 segundos
func check_combo_reset():
    if not ASTagUtils.event_did_occur(&"event.hit", asc, 2.0):
        combo_counter = 0
        play_combo_reset_animation()
```

## Buffers Históricos Internos

Cada `ASComponent` mantém automaticamente:

```
NAME History Buffer (128 entradas)
  ├─ tag_added: &"class.warrior", timestamp: 1000
  ├─ tag_removed: &"state.stunned", timestamp: 1050
  └─ ...

CONDITIONAL History Buffer (128 entradas)
  ├─ tag_added: &"state.burning", timestamp: 1100
  └─ ...

EVENT History Buffer (128 entradas)
  ├─ event: &"event.damage", magnitude: 30, instigator: enemy, timestamp: 1200
  ├─ event: &"event.hit", magnitude: 0, instigator: enemy, timestamp: 1210
  └─ ...
```

## Performance

- **Lookup O(log n)**: Busca binária no buffer circular
- **Amortizado O(1)**: Adição de nova entrada
- **Memory**: ~64KB por ator (128 \* 3 buffers)

Eficiente mesmo para centenas de atores.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Mantém buffers
- [AbilitySystem](../singleton/ability-system.md) — Registro de tags
- [ASAbility](../resources/asability.md) — Pode usar em triggers

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
