---
title: "ASEditorPropertySelector"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASEditorPropertySelector

**Badge:** `EditorProperty`

## Descrição Breve

Property editor customizado para seleção múltipla de tags do Ability System.

## Descrição Completa

`ASEditorPropertySelector` fornece uma interface dialog-based para selecionar múltiplas tags registradas. Usado em
propriedades de array de tags (ex: `activation_required_all_tags`, `granted_tags`, `removal_tags`).

**Comportamento:**

1. Botão "Select Tags..." no inspector
2. Ao clicar, abre dialog com checkboxes
3. Seleciona múltiplas tags (CTRL+Click ou checkbox)
4. Confirma seleção → Array atualiza no inspector

## Herança

```
EditorProperty
 └─ ASEditorPropertySelector
```

## Interface

**Inspector:**

```
[activation_required_all_tags: Array]
┌───────────────────────┐
│ [Select Tags...] [X]  │  ← Botão abre dialog
└───────────────────────┘
```

**Dialog:**

```
┌─────────────────────────┐
│ Select Tags             │
├─────────────────────────┤
│ ☐ ability.fireball      │
│ ☑ ability.slash         │  ← Selecionada
│ ☐ ability.shield        │
│ ☐ state.burning         │
│ ☑ state.empowered       │  ← Selecionada
│ ☐ event.on_hit          │
│                         │
│     [OK] [Cancel]       │
└─────────────────────────┘
```

## Funcionalidades

### Seleção Múltipla

- **Checkbox Individual:** Seleciona/deseleciona tag
- **CTRL+Click:** Adiciona/remove da seleção
- **Shift+Click:** Range selection

### Filtragem Opcional

Dialog pode incluir campo de busca:

```
┌──────────────────────┐
│ Search: [ability____] │  ← Filtra por texto
│ ☐ ability.fireball   │
│ ☐ ability.slash      │
│ ☐ ability.shield     │
└──────────────────────┘
```

### Agrupamento Hierárquico

Tags agrupadas por raiz:

```
☐ ability
  ☐ ability.fireball
  ☐ ability.slash
  ☐ ability.shield
☑ state
  ☑ state.burning
  ☐ state.frozen
☐ event
  ☐ event.on_hit
```

## Validação de Tipo

`ASEditorPropertySelector` valida tipos:

```
activation_required_all_tags: Array[StringName]
  Aceita: CONDITIONAL tags (states)
  Rejeita: NAME tags (abilities)
  Rejeita: EVENT tags (events)
```

Campo exibe apenas tags compatíveis.

## Casos de Uso

### Requisitos de Ability

```
# ASAbility.activation_required_all_tags
┌──────────────────────┐
│ Select Tags...       │
├──────────────────────┤
│ ☑ class.mage         │ ← Requer ser mago
│ ☑ state.not_silenced │ ← Requer não estar silenciado
│ ☐ state.empowered    │
└──────────────────────┘
```

### Tags Concedidas por Effect

```
# ASEffect.granted_tags
┌──────────────────────┐
│ Select Tags...       │
├──────────────────────┤
│ ☑ state.burning      │ ← Concede burning
│ ☑ immune.fire        │ ← Concede imunidade fogo
│ ☐ state.stunned      │
└──────────────────────┘
```

### Tags Removidas no Cancel

```
# ASAbility.activation_cancel_tags
┌──────────────────────┐
│ Select Tags...       │
├──────────────────────┤
│ ☑ ability.channel    │ ← Cancela ability em execução
│ ☑ state.charging     │ ← Remove state
│ ☐ state.burning      │
└──────────────────────┘
```

## Integração com ASInspectorPlugin

Registrado automaticamente:

```gdscript
# Dentro ASInspectorPlugin:
func _handles_type(type):
    if property in ["activation_required_all_tags", "granted_tags"]:
        return ASEditorPropertySelector.new()
```

## Filtragem por Tipo de Tag

`ASEditorPropertySelector` filtra por tipo de propriedade:

```gdscript
# Campo: "activation_required_all_tags"
# Tipo esperado: CONDITIONAL (states, conditions)
# Dialog exibe APENAS: state.*, immune.*, condition.* tags

# Campo: "granted_tags"
# Tipo esperado: CONDITIONAL
# Dialog exibe APENAS: state.*, immune.* tags

# Campo: "event_dispatch"
# Tipo esperado: EVENT
# Dialog exibe APENAS: event.* tags
```

## Melhor Prática

### Organizando Seleções

Agrupe tags semanticamente:

```
Requisitos para Ultimate:
☑ class.mage
☑ mana >= 100
☑ not_on_cooldown

Requisitos para Dodge:
☑ state.not_stunned
☑ stamina >= 20
```

### Validação no Projeto

Após selecionar tags, `AbilitySystem` valida:

```gdscript
# Se seleciona tag não-registrada:
# ⚠️ Aviso: "Tag 'unknown' não está registrada no AbilitySystem"
```

Registre todas as tags em `AbilitySystem` antes de usar no selector.

## Referências Relacionadas

- [ASEditorPropertyTagSelector](aseditorpropertytagselector.md) — Single tag selector
- [ASEditorPlugin](aseditorplugin.md) — Plugin principal
- [ASInspectorPlugin](asinspectorplugin.md) — Orquestra property editors
- [ASAbility](../resources/asability.md) — Usa seletor para requisitos
- [ASEffect](../resources/aseffect.md) — Usa seletor para tags

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
