---
title: "Tutorial: Sistema de Buff/Debuff"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Tutorial: Sistema de Buff/Debuff

Aprenda a criar modificadores temporários que afetam personagens.

**Tempo:** ~10 minutos | **Nível:** Intermediário

## Conceito

**Buff:** Efeito positivo temporário (ex: aumenta dano) **Debuff:** Efeito negativo temporário (ex: reduz velocidade)

Ambos são `ASEffect` com duração.

## Passo 1: Criar Tags de Status

Abra **Project Settings → Ability System** e crie:

```
state.empowered (CONDITIONAL)
state.slowed (CONDITIONAL)
state.burning (CONDITIONAL)
state.frozen (CONDITIONAL)
effect.empower (NAME)
effect.slow (NAME)
effect.burn (NAME)
effect.freeze (NAME)
```

## Passo 2: Criar ASEffect de Buff

New Resource → **ASEffect**

Salve como `res://assets/effects/empower.tres`

```
effect_tag: &"effect.empower"
duration_policy: 1 (DURATION)
duration_magnitude: 5.0
target_type: 0 (SELF)
granted_tags: [&"state.empowered"]
removed_tags: []
modifiers: (1 elemento)
  [0]:
    attribute: &"damage"
    operation: 1 (MULTIPLY)
    magnitude: 1.5
```

**Resultado:** Aumenta dano em 50% por 5 segundos.

## Passo 3: Criar ASEffect de Debuff

New Resource → **ASEffect**

Salve como `res://assets/effects/slow.tres`

```
effect_tag: &"effect.slow"
duration_policy: 1 (DURATION)
duration_magnitude: 3.0
target_type: 1 (OTHERS)
granted_tags: [&"state.slowed"]
removed_tags: []
modifiers: (1 elemento)
  [0]:
    attribute: &"movement_speed"
    operation: 0 (ADD)
    magnitude: -3.0
```

**Resultado:** Reduz velocidade em 3.0 por 3 segundos.

## Passo 4: Aplicar Buff

```gdscript
# Em Player.gd
func use_empower():
    asc.apply_effect_by_tag(&"effect.empower")
    print("Empowered!")

func _process(_delta):
    if asc.has_tag(&"state.empowered"):
        var remaining_duration = # calcular
        print("Empowered para mais %.1f segundos" % remaining_duration)
```

## Passo 5: Aplicar Debuff a Inimigo

```gdscript
# Quando player ataca inimigo
func use_ability(ability_tag: StringName):
    if asc.try_activate_ability_by_tag(ability_tag):
        # Aplicar slow ao inimigo
        if ability_tag == &"ability.ice_bolt":
            var enemy_asc = AbilitySystem.resolve_component(enemy)
            asc.apply_effect_by_tag(&"effect.slow", enemy_asc)
```

## Passo 6: Debuff Contínuo (DoT)

New Resource → **ASEffect**

Salve como `res://assets/effects/burning.tres`

```
effect_tag: &"effect.burning"
duration_policy: 1 (DURATION)
duration_magnitude: 5.0
period: 1.0
execute_periodic_tick_on_application: true
target_type: 1 (OTHERS)
granted_tags: [&"state.burning"]
modifiers: (1 elemento)
  [0]:
    attribute: &"health"
    operation: 0 (ADD)
    magnitude: -10.0
```

**Resultado:** -10 HP a cada 1 segundo por 5 segundos (total -50 HP).

## Passo 7: Visualizar Buffs

```gdscript
func update_buff_ui():
    var all_effects = asc.get_all_effect_specs()

    for effect_spec in all_effects:
        var effect = effect_spec.get_effect()
        var remaining = effect_spec.get_duration_remaining()

        var label = Label.new()
        label.text = "%s (%.1f)" % [effect.effect_tag, remaining]

        if effect.effect_tag.begins_with("effect.empower"):
            label.modulate = Color.YELLOW
        elif effect.effect_tag.begins_with("effect.slow"):
            label.modulate = Color.BLUE

        buff_container.add_child(label)
```

## Passo 8: Immunidade

Previne que efeitos sejam aplicados:

```gdscript
# Em ASAbility ou ASEffect:
activation_blocked_any_tags: [&"immune.fire"]

# Quando aplicar efeito:
func apply_effect_to_target(effect, target_asc):
    if target_asc.has_tag(&"immune.fire"):
        if effect.effect_tag.begins_with("effect.burn"):
            print("Target é imune a burning!")
            return false

    target_asc.apply_effect_by_tag(effect.effect_tag)
    return true
```

## Passo 9: Cleanup Automático

ASComponent cuida de remover buffs quando expiram:

```gdscript
func _process(_delta):
    # ASComponent remove automaticamente efeitos expirados
    # Você pode escutar:
    asc.effect_removed.connect(_on_effect_removed)

func _on_effect_removed(effect_spec):
    var effect_tag = effect_spec.get_effect().effect_tag
    print("Efeito removido: ", effect_tag)

    if effect_tag == &"effect.empower":
        print("Empowered finalizou!")
```

## Casos de Uso Avançados

### 1. Buff Stacking

```gdscript
# Aplicar empower 3 vezes = 1.5x * 1.5x * 1.5x = 3.375x damage
for i in range(3):
    asc.apply_effect_by_tag(&"effect.empower")
```

### 2. Conflicting Effects

```gdscript
# Congelamento remove burning
func apply_freeze(target_asc):
    target_asc.apply_effect_by_tag(&"effect.freeze")

# Em ASEffect de freeze:
removed_tags: [&"state.burning"]
```

### 3. Buff que Concede Ability

```gdscript
# Effect concede nova ability temporariamente
effect.granted_tags: [&"ability.enhanced_strike"]

# Quando buff expira, ability desaparece
```

### 4. Escalonamento de Buff por Nível

```gdscript
func apply_buff_scaled(level: float):
    var damage_boost = 1.0 + (level * 0.1)  # +10% por nível
    asc.apply_effect_by_tag(&"effect.empower", level)
```

## Checklist

```
[ ] Criar tags de status
[ ] Criar 1-2 buffs básicos
[ ] Criar 1-2 debuffs básicos
[ ] Aplicar a jogador
[ ] Aplicar a inimigo
[ ] Implementar DoT
[ ] UI de status ativo
[ ] Remover ao expirar
[ ] Debugar duração
```

---

**Próximo:** [Guia de Multiplayer](../guides/guide-multiplayer.md)
