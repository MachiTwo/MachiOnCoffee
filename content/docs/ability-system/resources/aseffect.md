---
title: "ASEffect"
date: "2026-04-18T12:00:00-03:00"
type: docs
---


**Badge:** `Resource`

## Descrição Breve

Resource que define modificações de atributos e concessão de tags.

## Descrição Completa

`ASEffect` é um "pacote de mudança" que encapsula:

- **Modificadores de Atributo**: Add, Multiply, Divide, Override em stats
- **Concessão de Tags**: Tags adicionadas enquanto efeito está ativo
- **Remoção de Tags**: Tags removidas ao aplicar
- **Duração**: Instant, Duration, ou Infinite
- **Empilhamento**: New Instance, Override, Intensity, ou Duration
- **Requisitos de Ativação**: Quais tags/atributos são necessários para aplicar
- **Período**: Para efeitos que repetem (DoT, HoT)
- **Cues**: Feedback audiovisual (animação, som)

Um efeito pode ser aplicado por:

- Uma **ASAbility** (directly)
- Um **ASPackage** (via ASDelivery)
- Efeito inicial de um **ASContainer**

## Herança

```gdscript
Resource
 └─ ASEffect
```gdscript

## Propriedades

## Identidade

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `effect_name` | String | `""` | Nome único do effect |
| `effect_tag` | StringName | `&""` | Tag identificadora (tipo NAME) |

## Duração

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `duration_policy` | int (enum) | `POLICY_INSTANT` | `POLICY_INSTANT` (0), `POLICY_DURATION` (1), `POLICY_INFINITE` (2) |
| `duration_magnitude` | float | `0.0` | Duração base quando não INSTANT |
| `use_custom_duration` | bool | `false` | Se `true`, trigger callback para cálculo customizado (índice -1) |

## Empilhamento

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `stacking_policy` | int (enum) | `STACK_NEW_INSTANCE` | Como novas aplicações interagem com existentes |

## Período (DoT/HoT)

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `period` | float | `0.0` | Segundos entre aplicações periódicas |
| `execute_periodic_tick_on_application` | bool | `false` | Se `true`, executa tick imediatamente ao aplicar |

## Modificadores

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `modifiers` | int | `0` | Número de modificadores de atributo |

Modificadores são adicionados via `add_modifier()` e consultados via getters.

## Requisitos

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `requirements` | int | `0` | Número de requisitos |

## Validação de Ativação (Tags)

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `activation_required_all_tags` | StringName[] | `[]` | Alvo DEVE ter TODAS (AND) |
| `activation_required_any_tags` | StringName[] | `[]` | Alvo DEVE ter PELO MENOS UMA (OR) |
| `activation_blocked_any_tags` | StringName[] | `[]` | Falha se tiver QUALQUER UMA (OR) |
| `activation_blocked_all_tags` | StringName[] | `[]` | Falha se tiver TODAS SIMULTANEAMENTE (AND) |

## Estado Enquanto Ativo

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `granted_tags` | StringName[] | `[]` | Tags concedidas enquanto efeito ativo |
| `removed_tags` | StringName[] | `[]` | Tags removidas ao aplicar efeito |
| `blocked_tags` | StringName[] | `[]` | Tags que ditam bloqueio de efeito |

## Tipo de Alvo

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `target_type` | int (enum) | `TARGET_SELF` | `TARGET_SELF` (aplicar ao owner) ou `TARGET_OTHERS` (aplicar via ASDelivery) |

## Conteúdo

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `cues` | ASCue[] | `[]` | Feedback audiovisual |

## Eventos

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `events_on_apply` | StringName[] | `[]` | Events disparados ao aplicar com sucesso |
| `events_on_remove` | StringName[] | `[]` | Events disparados ao remover |

## Constantes (Enums)

## DurationPolicy

```gdscript
enum DurationPolicy {
    POLICY_INSTANT = 0,    # Aplicado uma vez, removido imediatamente
    POLICY_DURATION = 1,   # Dura tempo especificado
    POLICY_INFINITE = 2    # Permanece indefinidamente
}
```gdscript

## StackingPolicy

```gdscript
enum StackingPolicy {
    STACK_NEW_INSTANCE = 0,  # Cada aplicação é independente
    STACK_OVERRIDE = 1,      # Nova substitui antiga (reseta timer)
    STACK_INTENSITY = 2,     # Aumenta magnitude (add stack count)
    STACK_DURATION = 3       # Estende duração restante
}
```gdscript

## TargetType

```gdscript
enum TargetType {
    TARGET_SELF = 0,    # Aplicado ao componente que originou
    TARGET_OTHERS = 1   # Aplicado via ASDelivery/projétil
}
```gdscript

## ModifierOp (Operações de Modificador)

```gdscript
enum ModifierOp {
    OP_ADD = 0,        # Add(magnitude) → value += magnitude
    OP_MULTIPLY = 1,   # Multiply(magnitude) → value *= magnitude
    OP_DIVIDE = 2,     # Divide(magnitude) → value /= magnitude
    OP_OVERRIDE = 3    # Override(magnitude) → value = magnitude
}
```gdscript

## Métodos Públicos

## Modificadores

## `add_modifier(attribute: StringName, operation: int, magnitude: float, use_custom_magnitude: bool = false) → void`

Adiciona modificador de atributo.

**Parâmetros:**

- `attribute`: Atributo a modificar (ex: `&"health"`)
- `operation`: `OP_ADD`, `OP_MULTIPLY`, `OP_DIVIDE`, `OP_OVERRIDE`
- `magnitude`: Valor para operação (ex: 20.0 para Add, 0.5 para Multiply)
- `use_custom_magnitude`: Se `true`, trigger callback para cálculo customizado

**Exemplo:**

```gdscript
var burn_effect = ASEffect.new()

# Reduz health 5 por tick
burn_effect.add_modifier(&"health", ASEffect.OP_ADD, -5.0)

# Reduz fire_resistance à metade
burn_effect.add_modifier(&"fire_resistance", ASEffect.OP_MULTIPLY, 0.5)
```gdscript

## `get_modifier_count() → int` (const)

Total de modificadores.

## `get_modifier_attribute(index: int) → StringName` (const)

Atributo do modificador em índice.

## `get_modifier_operation(index: int) → int` (const)

Operação do modificador em índice.

## `get_modifier_magnitude(index: int) → float` (const)

Magnitude base do modificador.

## `is_modifier_custom(index: int) → bool` (const)

Se modificador usa cálculo customizado.

## Requisitos

## `add_requirement(attribute: StringName, amount: float) → void`

Adiciona requisito de atributo mínimo.

## `get_requirement_attribute(index: int) → StringName` (const)

Atributo do requisito.

## `get_requirement_amount(index: int) → float` (const)

Valor mínimo requerido.

## Casos de Uso

## Efeito Simples de Dano

```gdscript
var impact_damage = ASEffect.new()
impact_damage.effect_name = "Impact Damage"
impact_damage.effect_tag = &"effect.impact_damage"

# Instant—aplica uma vez
impact_damage.duration_policy = ASEffect.POLICY_INSTANT

# -30 health
impact_damage.add_modifier(&"health", ASEffect.OP_ADD, -30.0)

# Dispara evento ao remover
impact_damage.events_on_apply.append(&"event.damage_taken")
```gdscript

## Buff com Duração

```gdscript
var strength_buff = ASEffect.new()
strength_buff.effect_name = "Strength Buff"
strength_buff.effect_tag = &"effect.strength_buff"

# Dura 10s
strength_buff.duration_policy = ASEffect.POLICY_DURATION
strength_buff.duration_magnitude = 10.0

# +20% damage
strength_buff.add_modifier(&"damage", ASEffect.OP_MULTIPLY, 1.2)

# Concede tag de buff
strength_buff.granted_tags.append(&"state.buffed")
```gdscript

## DoT (Dano Contínuo)

```gdscript
var fire_dot = ASEffect.new()
fire_dot.effect_name = "Burning"
fire_dot.effect_tag = &"effect.burning"

# Dura 5s, repete a cada 1s
fire_dot.duration_policy = ASEffect.POLICY_DURATION
fire_dot.duration_magnitude = 5.0
fire_dot.period = 1.0

# -5 health por tick
fire_dot.add_modifier(&"health", ASEffect.OP_ADD, -5.0)

# Adiciona tag "state.burning"
fire_dot.granted_tags.append(&"state.burning")

# Imediatamente aplica primeiro tick
fire_dot.execute_periodic_tick_on_application = true
```gdscript

## Debuff Infinito com Override

```gdscript
var frozen = ASEffect.new()
frozen.effect_name = "Frozen"
frozen.effect_tag = &"effect.frozen"

# Infinito—até ser removido
frozen.duration_policy = ASEffect.POLICY_INFINITE

# Reduz speed à metade
frozen.add_modifier(&"speed", ASEffect.OP_MULTIPLY, 0.5)

# Bloqueia ataque
frozen.granted_tags.append(&"state.frozen")
frozen.activation_blocked_any_tags.append(&"ability.attack")

# Nova aplicação substitui (reseta)
frozen.stacking_policy = ASEffect.STACK_OVERRIDE
```gdscript

## Efeito com Requisito de Alvo

```gdscript
var holy_blessing = ASEffect.new()
holy_blessing.effect_name = "Holy Blessing"
holy_blessing.effect_tag = &"effect.holy_blessing"

# Requer que alvo tenha "class.paladin"
holy_blessing.activation_required_all_tags.append(&"class.paladin")

# Duration 30s
holy_blessing.duration_policy = ASEffect.POLICY_DURATION
holy_blessing.duration_magnitude = 30.0

# +15 health per second (HoT) → +15 every 1s for 30s = 450 total
holy_blessing.add_modifier(&"health", ASEffect.OP_ADD, 15.0)
holy_blessing.period = 1.0

# Tag para visual
holy_blessing.granted_tags.append(&"state.blessed")
```gdscript

## Efeito com Stacking Intensity

```gdscript
var poison_stack = ASEffect.new()
poison_stack.effect_name = "Poison Stack"
poison_stack.effect_tag = &"effect.poison"

poison_stack.duration_policy = ASEffect.POLICY_DURATION
poison_stack.duration_magnitude = 8.0
poison_stack.period = 2.0

# -3 health por tick
poison_stack.add_modifier(&"health", ASEffect.OP_ADD, -3.0)

# Cada nova aplicação aumenta intensidade (não timer)
poison_stack.stacking_policy = ASEffect.STACK_INTENSITY

# Visual feedback
poison_stack.granted_tags.append(&"state.poisoned")
poison_stack.events_on_apply.append(&"event.poison_applied")
```gdscript

## Integração com Abilities e Delivery

## Via Ability (Self-Target)

```gdscript
var self_heal = ASAbility.new()
self_heal.ability_tag = &"ability.self_heal"
self_heal.effects.append(healing_effect)  # Aplicado automaticamente

# Ativar
asc.try_activate_ability_by_tag(&"ability.self_heal")
```gdscript

## Via Package (Projectile Delivery)

```gdscript
var package = ASPackage.new()
package.package_tag = &"package.fireball"
package.effects_resources.append(fire_damage_effect)
package.effects_resources.append(fire_dot_effect)
package.cues_resources.append(fire_visual_cue)

var delivery = delivery_node  # ASDelivery
delivery.package = package

# Ao colidir, ASDelivery aplica effects via:
# target_asc.apply_package(package)
```gdscript

## Referências Relacionadas

- [ASEffectSpec](../refcounted/aseffectspec.md) — Instância em execução
- [ASAbility](asability.md) — Ability que aplica effects
- [ASPackage](aspackage.md) — Container de entrega
- [ASComponent](../nodes/ascomponent.md) — Alvo que recebe

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
