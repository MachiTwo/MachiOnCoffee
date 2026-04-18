---
title: "ASAttributeSet"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASAttributeSet

**Badge:** `Resource`

## Descrição Breve

Container de estatísticas (stats) de um ator.

## Descrição Completa

`ASAttributeSet` define o esquema de atributos (stats) de um ator. Cada ator tem sua própria **deep-clone** única do set, garantindo que modificadores não afetem outros atores.

Suporta:

- **Limites**: Min/Max para cada atributo
- **Drivers**: Derivar valor de outro atributo (ex: Health = 2 * Strength)
- **Modificadores**: Flat add, multiply, divide, override
- **Clamping**: Valores automaticamente restringidos ao intervalo

## Herança

```
Resource
 └─ ASAttributeSet
```

## Propriedades

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `attributes` | ASAttribute[] | `[]` | Array de atributos definidos |

## Métodos Públicos

### Gerenciamento de Atributos

#### `add_attribute(attribute: ASAttribute) → void`

Adiciona atributo ao set.

#### `get_attribute(name: StringName) → ASAttribute` (const)

Recupera definição de atributo.

#### `has_attribute(name: StringName) → bool` (const)

Verifica se atributo existe.

#### `remove_attribute(name: StringName) → bool`

Remove atributo. Retorna `true` se existia.

### Valores

#### `set_attribute_base_value(attribute: StringName, value: float) → void`

Define valor base (antes de modificadores).

#### `get_attribute_base_value(attribute: StringName) → float` (const)

Lê valor base.

#### `get_attribute_current_value(attribute: StringName) → float` (const)

Lê valor final (base + modificadores, clamped).

**Exemplo:**

```gdscript
# Base é 100
attribute_set.set_attribute_base_value(&"health", 100.0)

# Aplicar modificador: -20%
# Current = 100 * 0.8 = 80
attribute_set.apply_modifier(&"health", ASEffect.OP_MULTIPLY, 0.8)

var hp = attribute_set.get_attribute_current_value(&"health")  # 80
```

### Drivers (Attribute Derivation)

#### `add_driver(attribute: StringName, source_attribute: StringName, operation: int, magnitude: float) → void`

Deriva valor base de outro atributo.

**Parâmetros:**

- `attribute`: Atributo a derivar (ex: `&"damage"`)
- `source_attribute`: Atributo fonte (ex: `&"strength"`)
- `operation`: `DRIVER_ADD`, `DRIVER_MULTIPLY`, `DRIVER_DIVIDE`, `DRIVER_OVERRIDE`
- `magnitude`: Fator (ex: 2.0 para dobro)

**Exemplo:**

```gdscript
# Damage base = Strength * 2
attribute_set.add_driver(&"damage", &"strength", ASAttributeSet.DRIVER_MULTIPLY, 2.0)

# Se Strength mudar, Damage base recalcula automaticamente
attribute_set.set_attribute_base_value(&"strength", 50.0)
var damage_base = attribute_set.get_attribute_base_value(&"damage")  # 100
```

**Ordem de Cálculo:**

1. Drivers executam (recalcam base values derivados)
2. Modificadores aplicados
3. Valor clamped ao intervalo [min, max]

#### `get_drivers(attribute: StringName) → Dictionary[]` (const)

Lista todos drivers de um atributo.

#### `remove_driver(attribute: StringName, source_attribute: StringName) → bool`

Remove driver específico. Retorna `true` se existia.

### Modificadores

#### `apply_modifier(attribute: StringName, operation: int, magnitude: float) → void`

Aplica modificador temporário (não persistido).

**Parâmetros:**

- `operation`: `OP_ADD`, `OP_MULTIPLY`, `OP_DIVIDE`, `OP_OVERRIDE`
- `magnitude`: Valor para operação

**Nota:** Modificadores são mantidos apenas durante lifetime de `ASEffectSpec`. Para persistência, usar Effects.

---

## Constantes (Enums)

### DriverOp

```gdscript
enum DriverOp {
    DRIVER_ADD = 0,        # base = source + magnitude
    DRIVER_MULTIPLY = 1,   # base = source * magnitude
    DRIVER_DIVIDE = 2,     # base = source / magnitude
    DRIVER_OVERRIDE = 3    # base = magnitude
}
```

### ModifierOp

```gdscript
enum ModifierOp {
    OP_ADD = 0,        # current = base + magnitude
    OP_MULTIPLY = 1,   # current = base * magnitude
    OP_DIVIDE = 2,     # current = base / magnitude
    OP_OVERRIDE = 3    # current = magnitude
}
```

## Casos de Uso

### Setup Básico

```gdscript
var attribute_set = ASAttributeSet.new()

# Adicionar stats
var health = ASAttribute.new()
health.attribute_name = "Health"
health.min_value = 0.0
health.max_value = 100.0
health.base_value = 100.0
attribute_set.add_attribute(health)

var mana = ASAttribute.new()
mana.attribute_name = "Mana"
mana.min_value = 0.0
mana.max_value = 50.0
mana.base_value = 50.0
attribute_set.add_attribute(mana)

var strength = ASAttribute.new()
strength.attribute_name = "Strength"
strength.min_value = 0.0
strength.max_value = 200.0
strength.base_value = 10.0
attribute_set.add_attribute(strength)
```

### Drivers (Attribute Scaling)

```gdscript
# Damage base é baseado em Strength
attribute_set.add_driver(&"damage", &"strength", ASAttributeSet.DRIVER_MULTIPLY, 2.0)

# Health base é baseado em Constitution
attribute_set.add_driver(&"health", &"constitution", ASAttributeSet.DRIVER_MULTIPLY, 10.0)

# Mana base = (Intelligence * 5) + 25
attribute_set.add_driver(&"mana", &"intelligence", ASAttributeSet.DRIVER_MULTIPLY, 5.0)
attribute_set.add_driver(&"mana", &"base_mana", ASAttributeSet.DRIVER_ADD, 25.0)
```

### Modificadores Temporários

```gdscript
# Buff: +20% Health
attribute_set.apply_modifier(&"health", ASAttributeSet.OP_MULTIPLY, 1.2)
var buffed_hp = attribute_set.get_attribute_current_value(&"health")

# Debuff: -30 damage
attribute_set.apply_modifier(&"damage", ASAttributeSet.OP_ADD, -30.0)

# Effect override: Set mana to 0
attribute_set.apply_modifier(&"mana", ASAttributeSet.OP_OVERRIDE, 0.0)
```

### Deep Clone Safety (ASComponent)

```gdscript
var container = ASContainer.new()
container.attribute_set = attribute_set

# Aplicar a múltiplos atores
asc1.apply_container(container)  # asc1 = deep-clone
asc2.apply_container(container)  # asc2 = deep-clone diferente

# Modificações não se afetam
asc1.set_attribute_base_value(&"health", 50.0)  # Apenas asc1
var asc2_health = asc2.get_attribute_current_value(&"health")  # Ainda 100
```

## Relacionadas

- [ASAttribute](asattribute.md) — Definição de um atributo
- [ASComponent](../nodes/ascomponent.md) — Gerencia AttributeSet
- [ASContainer](ascontainer.md) — Armazena AttributeSet
- [ASEffect](aseffect.md) — Aplica modificadores

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
