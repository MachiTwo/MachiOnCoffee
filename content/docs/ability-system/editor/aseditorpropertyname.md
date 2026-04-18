---
title: "ASEditorPropertyName"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASEditorPropertyName

**Badge:** `EditorProperty`

## Descrição Breve

Property editor customizado para nomes de resources com validação de unicidade.

## Descrição Completa

`ASEditorPropertyName` é uma extensão do inspector que fornece um campo de texto para nomear resources com **validação
automática de duplicidade**.

Usado em propriedades tipo `StringName` marcadas para nomes únicos (ex: `ability_tag`, `effect_tag`, `resource_name`).

**Comportamento:**

1. Campo de texto para entrada de nome
2. Validação em tempo real contra registry global
3. Aviso visual se nome duplicado
4. Integração com `AbilitySystem.register_resource_name()`

## Herança

```
EditorProperty
 └─ ASEditorPropertyName
```

## Validação em Tempo Real

**Durante digitação:**

- ✅ Nome único: Sem aviso, aceita
- ⚠️ Nome duplicado: Exibe aviso "Name already in use by resource X"
- ⚠️ Nome reservado: Exibe aviso se nome é palavra-chave Godot

**Ao confirmar (Enter):**

- Se válido: `AbilitySystem.register_resource_name(name, instance_id)` chamado
- Se inválido: Rejeita mudança, mantém valor anterior

## Casos de Uso

### Nomear ASAbility

```gdscript
# No inspector:
# ability_tag (ASEditorPropertyName)
# Campo: "ability.fireball"

# Editor valida em tempo real:
# ✅ "ability.fireball" → Novo? Aceita
# ⚠️ "ability.fireball" → Já existe? Aviso
```

### Nomear ASEffect

```gdscript
# No inspector:
# effect_tag (ASEditorPropertyName)
# Campo: "effect.burn"

# Validação automática
```

### Nomear ASContainer (Arquétipos)

```gdscript
# No inspector:
# container_name (ASEditorPropertyName)
# Campo: "archetype.warrior"

# Se tentar duplicar: Aviso
```

## Integração com ASEditorPlugin

`ASEditorPropertyName` é registrado automaticamente via `ASInspectorPlugin`:

```gdscript
# Dentro de ASInspectorPlugin._handles_type():
if property == "ability_tag":
    return ASEditorPropertyName.new()
if property == "effect_tag":
    return ASEditorPropertyName.new()
# ... (todas as propriedades de naming)
```

## Melhor Prática

**Convenção de Nomes:**

```
ability.wizard_fireball
ability.warrior_slash
effect.burn_damage
effect.heal_overtime
state.stunned
state.empowered
event.on_hit
event.on_death
```

Usar dotação hierárquica facilita organização:

```
ability
  ├─ wizard.*
  ├─ warrior.*
  └─ rogue.*

effect
  ├─ damage.*
  ├─ heal.*
  └─ debuff.*
```

## Validação Customizada

Se precisar de regras adicionais de validação:

1. Subclass `ASEditorPropertyName`
2. Override `_validate_name()`
3. Adicione lógica customizada

```gdscript
class_name CustomNameValidator
extends ASEditorPropertyName

func _validate_name(name: StringName) -> String:
    # Validação base
    var base_msg = super._validate_name(name)
    if base_msg:
        return base_msg

    # Validação customizada
    if not name.begins_with("custom_"):
        return "Nome deve começar com 'custom_'"

    if name.length() > 50:
        return "Nome muito longo (máx 50 chars)"

    return ""  # Válido
```

## Referências Relacionadas

- [ASEditorPlugin](aseditorplugin.md) — Registra property editors
- [ASInspectorPlugin](asinspectorplugin.md) — Orquestra property editors
- [AbilitySystem](../singleton/ability-system.md) — Registry de resource names

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
