---
title: "ASTagsPanel"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `VBoxContainer` • `EditorUI`

## Descrição Breve

Interface visual no editor para gerenciamento central de tags globais do Ability System.

## Descrição Completa

`ASTagsPanel` é um painel customizado exibido em Project Settings que fornece UI para:

1. **Adicionar Tags Globais:** Registrar novas tags com tipo (NAME, CONDITIONAL, EVENT)
2. **Remover Tags:** Deletar tags do registry global
3. **Visualizar Hierarquia:** Tags agrupadas por dotação (ability._, state._, event.\*)
4. **Validação em Tempo Real:** Previne duplicatas e tipos inválidos

Acessível via: **Project Settings → Ability System**

## Herança

````gdscript
VBoxContainer
 └─ ASTagsPanel
```gdscript

## Interface

**Estrutura:**

```gdscript
┌─────────────────────────────────────────┐
│ Ability System Tags                     │
├─────────────────────────────────────────┤
│                                         │
│ ┌─ Organização por Tipo ──────────────┐ │
│ │                                     │ │
│ │ ☐ NAME Tags (Identidade)           │ │
│ │   ☐ ability.fireball                │ │
│ │   ☐ ability.slash                   │ │
│ │   ☐ effect.burn                     │ │
│ │                                     │ │
│ │ ☐ CONDITIONAL Tags (Estados)       │ │
│ │   ☐ state.burning                   │ │
│ │   ☐ state.stunned                   │ │
│ │   ☐ immune.fire                     │ │
│ │                                     │ │
│ │ ☐ EVENT Tags (Eventos)             │ │
│ │   ☐ event.on_hit                    │ │
│ │   ☐ event.on_death                  │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [Add Tag] [Remove Selected] [Clear All] │
│                                         │
└─────────────────────────────────────────┘
```gdscript

## Funcionalidades

## Adicionar Tag

1. Click **[Add Tag]**
2. Dialog aparece:

```gdscript
┌──────────────────────────────┐
│ New Tag                      │
├──────────────────────────────┤
│ Tag Name: [ability._______]  │
│ Type:     [NAME        ↓]    │
│            └─ NAME           │
│              CONDITIONAL     │
│              EVENT           │
│                              │
│         [Add] [Cancel]       │
└──────────────────────────────┘
```gdscript

3. Insira nome (ex: `ability.fireball`)
4. Selecione tipo (NAME, CONDITIONAL, ou EVENT)
5. Click **[Add]**
6. Tag aparece na lista se válida

**Validação:**

- ❌ Nome vazio: Rejeita
- ❌ Tag duplicada: Aviso "Already exists"
- ✅ Nome único + tipo válido: Registra

## Remover Tag

1. Selecione tag na lista
2. Click **[Remove Selected]**
3. Confirmação:

```gdscript
Are you sure you want to remove "ability.fireball"?
[Remove] [Cancel]
```gdscript

4. Se confirm: Tag removida do registry
5. Se referenciada: Aviso "Tag still in use by X properties"

## Hierarquia Automática

Tags organizadas por raiz:

```gdscript
☐ ability           (COLLAPSE/EXPAND)
  ☐ ability.fireball
  ☐ ability.slash
  ☐ ability.shield

☐ state
  ☐ state.burning
  ☐ state.stunned

☐ event
  ☐ event.on_hit
```gdscript

Click arrow para expandir/colapsar grupo.

## Busca (Opcional)

Campo de filtro pode existir:

```gdscript
┌──────────────────────┐
│ Search: [ability____] │
│ ☐ ability.fireball    │
│ ☐ ability.slash       │
│ ☐ ability.shield      │
└──────────────────────┘
```gdscript

Filtra tags em tempo real por texto.

## Métodos

## Refresh

## `update_tags() → void`

Recarrega lista de tags do registry global (`AbilitySystem`).

Chamado automaticamente quando:

- Nova tag registrada
- Tag removida
- Projeto reloadado

Você pode chamar manualmente para force-refresh:

```gdscript
tags_panel.update_tags()
```gdscript

## Persistência

Tags são salvas em `project.godot`:

```ini
[ability_system]
tags = ["ability.fireball", "state.burning", "event.damage"]
tag_types = [0, 1, 2]  # NAME, CONDITIONAL, EVENT
```gdscript

Ao reabrir projeto: tags automaticamente restauradas.

## Integração com AbilitySystem

Panel sincroniza com `AbilitySystem` singleton:

```gdscript
# Ao adicionar tag no painel:
AbilitySystem.register_tag(&"ability.new", ASTagType.NAME)

# Ao remover:
AbilitySystem.unregister_tag(&"ability.old")

# Panel monitora sinais:
AbilitySystem.tags_changed.connect(_on_tags_changed)
```gdscript

## Casos de Uso

## Projeto Novo: Setup Inicial

1. Abra Project Settings → Ability System
2. Click **[Add Tag]**:
   - `ability.fireball` (NAME)
   - `ability.slash` (NAME)
   - `state.burning` (CONDITIONAL)
   - `state.stunned` (CONDITIONAL)
   - `event.on_hit` (EVENT)
3. Tags registradas globalmente para todo projeto

## Adicionar Feature: Novas Habilidades

1. Design nova ability (ex: "ice blast")
2. No painel, **[Add Tag]**:
   - `ability.ice_blast` (NAME)
   - `effect.freeze` (NAME)
   - `state.frozen` (CONDITIONAL)
3. Agora editor permite usar estas tags em dropdowns de ASAbility

## Audit: Verificar Tags Não Usadas

1. Abra painel
2. Visualize todas as tags registradas
3. Se tag aparece mas nunca referenciada em nenhuma ability/effect:
   - ⚠️ Potencial dead code
   - Remove se confirmar não-uso

## Melhor Prática

## Estrutura Recomendada

```gdscript
ability.*
  ├─ warrior.*
  ├─ mage.*
  └─ rogue.*

effect.*
  ├─ damage.*
  ├─ heal.*
  └─ debuff.*

state.*
  ├─ buff.*
  ├─ debuff.*
  └─ control.*

event.*
  ├─ damage.*
  ├─ heal.*
  └─ control.*
```gdscript

Hierarquia facilita navegação no painel.

## Criação em Bulk

Se projeto grande, considere criar tags via script em `_ready()`:

```gdscript
func _ready():
    if not AbilitySystem.is_tag_registered(&"ability.fireball"):
        AbilitySystem.register_tag(&"ability.fireball", ASTagType.NAME)
    # ... etc
```gdscript

Depois sincronize com painel:

```gdscript
func sync_tags_to_panel():
    tags_panel.update_tags()
```gdscript

## Referências Relacionadas

- [AbilitySystem](../singleton/ability-system.md) — Registry de tags
- [ASEditorPlugin](aseditorplugin.md) — Instancia painel
- [ASAbility](../resources/asability.md) — Usa tags
- [ASEffect](../resources/aseffect.md) — Usa tags

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
