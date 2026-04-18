---
title: "ASEditorPropertyTagSelector"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASEditorPropertyTagSelector

**Badge:** `EditorProperty`

## Descrição Breve

Property editor customizado para seleção de **uma única tag** do Ability System.

## Descrição Completa

`ASEditorPropertyTagSelector` fornece um dropdown `OptionButton` para selecionar uma tag única. Usado em propriedades
tipo `StringName` que requerem uma tag específica (ex: `ability_tag`, `effect_tag`, `event_dispatch_tag`).

**Comportamento:**

1. Dropdown no inspector com "(None)" + todas as tags registradas
2. Clica para abrir lista
3. Seleciona tag
4. Valor atualiza imediatamente

## Herança

```
EditorProperty
 └─ ASEditorPropertyTagSelector
```

## Interface

**Inspector:**

```
┌──────────────────────────────┐
│ ability_tag: [ability.slash ↓] │
└──────────────────────────────┘
```

**Dropdown Aberto:**

```
┌──────────────────────┐
│ (None)               │
│ ability.fireball     │
│ ability.slash        │ ← Selecionada
│ ability.shield       │
│ state.burning        │
│ state.frozen         │
│ event.on_hit         │
│ event.on_damage      │
└──────────────────────┘
```

## Validação de Tipo

`ASEditorPropertyTagSelector` valida tipos por propriedade:

```gdscript
# Campo: "ability_tag"
# Tipo esperado: NAME (identidade)
# Dropdown exibe: ability.*, effect.*, state.* (NAME tags)

# Campo: "event_dispatch_tag"
# Tipo esperado: EVENT
# Dropdown exibe: event.* (EVENT tags APENAS)
```

Tipos inválidos aparecem desabilitados (greyed out).

## Casos de Uso

### Seleção de Ability Tag

```
# ASAbility.ability_tag
┌──────────────────────┐
│ (None)               │
│ ability.fireball     │ ← Identificador da ability
│ ability.slash        │
│ ability.shield       │
└──────────────────────┘
```

### Seleção de Effect Tag

```
# ASEffect.effect_tag
┌──────────────────────┐
│ (None)               │
│ effect.burn          │
│ effect.heal          │
│ effect.stun          │
└──────────────────────┘
```

### Seleção de Event Tag

```
# ASComponent.event_dispatch_tag
┌──────────────────────┐
│ (None)               │
│ event.on_hit         │
│ event.on_death       │
│ event.on_cast        │
└──────────────────────┘
```

### Seleção em Triggers

```
# ASAbility.triggers[].trigger_tag
# Quando seleciona qual evento ativa a ability
┌──────────────────────┐
│ (None)               │
│ event.on_damage      │ ← Dispara ao tomar dano
│ event.on_parry       │
│ event.on_crit        │
└──────────────────────┘
```

## Filtragem Dinâmica

Dropdown atualiza dinamicamente quando:

1. **Nova tag registrada:** Aparece no dropdown
2. **Tag removida:** Desaparece do dropdown
3. **Projeto reloadado:** Sincroniza com `AbilitySystem` registry

```gdscript
# Editor (AbilitySystem tags painel):
# Você registra: &"ability.new_ability"

# Dropdown imediatamente mostra:
# ☐ ability.new_ability
```

## Integração com ASInspectorPlugin

Registrado automaticamente:

```gdscript
# Dentro ASInspectorPlugin:
func _handles_type(type):
    if property == "ability_tag":
        return ASEditorPropertyTagSelector.new()
    if property == "effect_tag":
        return ASEditorPropertyTagSelector.new()
    # ... etc
```

## Sincronização com AbilitySystem

Selector lê sempre do registry global:

```gdscript
# Ao abrir dropdown:
var all_tags = AbilitySystem.get_all_registered_tags()
# Popula com todas as tags registradas
```

Se tag removida de registry mas ainda referenciada:

```
# Campo tem: &"ability.old_ability"
# Tag foi removida do registry
# Dropdown mostra: "(None) [ability.old_ability]"
# ⚠️ Aviso: "Tag não registrada"
```

## Validação de Seleção

Ao selecionar tag:

```gdscript
# Valida tipo:
var tag_type = AbilitySystem.get_tag_type(selected_tag)

if tag_type != expected_type:
    # ⚠️ Aviso: "Wrong tag type for this field"
    # Rejeita seleção, mantém valor anterior
```

## Melhor Prática

### Convenção de Nomes

Use hierarquia clara:

```
ability.wizard_*
ability.warrior_*
effect.damage_*
effect.heal_*
state.condition_*
event.trigger_*
```

Facilita encontrar tags no dropdown.

### Criar Tag Antes de Usar

Registre tag em `AbilitySystem` antes de atribuir em property:

```gdscript
# ✅ Correto
AbilitySystem.register_tag(&"ability.new_attack", ASTagType.NAME)
# Agora atribua em ASAbility.ability_tag

# ❌ Incorreto
# Tenta atribuir tag não registrada
# Dropdown não a exibe
```

## Referências Relacionadas

- [ASEditorPropertySelector](aseditorpropertyselector.md) — Multi-tag selector
- [ASEditorPlugin](aseditorplugin.md) — Plugin principal
- [ASInspectorPlugin](asinspectorplugin.md) — Orquestra property editors
- [AbilitySystem](../singleton/ability-system.md) — Registry de tags
- [ASAbility](../resources/asability.md) — Usa seletor

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
