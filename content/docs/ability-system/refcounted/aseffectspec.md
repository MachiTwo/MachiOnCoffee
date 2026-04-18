---
title: "ASEffectSpec"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASEffectSpec

**Badge:** `RefCounted`

## Descrição Breve

Instância runtime de um effect ativo.

## Descrição Completa

`ASEffectSpec` representa um effect ativo no ator. Armazena e gerencia:

- **Duração Restante**: Tempo até terminus
- **Stacks**: Quantas vezes o effect foi aplicado (stacking policy)
- **Magnitude Calculada**: Valores finais dos modificadores
- **Período**: Timer para DoT/HoT
- **Nível**: Power level para scaling
- **Source/Target**: Referências a componentes

## Herança

```
RefCounted
 └─ ASEffectSpec
```

## Métodos Públicos

### Inicialização

#### `init(effect: ASEffect, level: float = 1.0) → void`

Inicializa o spec com effect e nível.

### Duração

#### `get_duration_remaining() → float` (const)

Tempo restante até terminus.

#### `get_total_duration() → float` (const)

Duração total inicial calculada.

#### `set_duration_remaining(value: float) → void`

Define tempo restante (para testes/debug).

### Nível e Magnitude

#### `get_level() → float` (const)

Power level da instância.

#### `set_level(level: float) → void`

Muda nível (recalcula magnitudes).

#### `get_magnitude(attribute: StringName) → float` (const)

Magnitude calculada de um modificador.

**Exemplo:**

```gdscript
var health_mod = spec.get_magnitude(&"health")  # -30.0 (ADD)
```

### Stacking

#### `get_stack_count() → int` (const)

Quantas vezes foi aplicado (stacking).

### Período (DoT/HoT)

#### `get_period_timer() → float` (const)

Tempo até próximo tick periódico.

### Componentes

#### `get_effect() → ASEffect` (const)

Resource definition.

#### `get_source_component() → ASComponent` (const)

Quem aplicou o effect (pode ser null).

#### `get_target_component() → ASComponent` (const)

Quem recebe o effect.

#### `get_source_attribute_value(attribute: StringName) → float` (const)

Valor de atributo no source.

#### `get_target_attribute_value(attribute: StringName) → float` (const)

Valor de atributo no target.

## Casos de Uso

### Verificar Duration no \_process

```gdscript
func _process(_delta):
    for spec in active_effect_specs:
        var remaining = spec.get_duration_remaining()

        if remaining < 0.5:
            print("Effect quase terminando")
            play_end_animation(spec.get_effect())
```

### DoT com Período

```gdscript
func _process(delta):
    var period_timer = dot_spec.get_period_timer()

    if period_timer <= 0:
        # Próximo tick!
        var damage = dot_spec.get_magnitude(&"health")
        target.take_damage(-damage)

        # Resetar período
        # (ASComponent cuida disso automaticamente)
```

### Stacking Visual Feedback

```gdscript
func _on_effect_applied(effect_spec: ASEffectSpec):
    var stacks = effect_spec.get_stack_count()

    # Mostrar número de stacks
    ui.update_stack_counter(effect_spec.get_effect().effect_tag, stacks)

    # Escala visual com stacks
    var scale = 1.0 + (stacks * 0.1)
    vfx_node.scale = Vector3.ONE * scale
```

### Scaling com Source Attribute

```gdscript
func calculate_custom_magnitude(effect_spec: ASEffectSpec) -> float:
    # Dano baseado em inteligência do atacante
    var source_intelligence = effect_spec.get_source_attribute_value(&"intelligence")
    var level = effect_spec.get_level()

    return source_intelligence * 0.5 * level
```

## Referências Relacionadas

- [ASEffect](../resources/aseffect.md) — Definição imutável
- [ASComponent](../nodes/ascomponent.md) — Gerencia specs
- [ASAbilitySpec](asabilityspec.md) — Spec de ability

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
