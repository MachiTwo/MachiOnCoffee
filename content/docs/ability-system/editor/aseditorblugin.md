---
title: "ASEditorPlugin"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASEditorPlugin

**Badge:** `EditorPlugin`

## Descrição Breve

Plugin principal do editor para integração do Ability System.

## Descrição Completa

`ASEditorPlugin` é o ponto de entrada da integração do Ability System no editor Godot. Responsável por:

1. **Registro de Tipos:** Registra classes customizadas (ASAbility, ASEffect, etc.) como tipos do projeto
2. **Ícones:** Associa ícones customizados a cada tipo para visual consistency no FileSystem
3. **Inspector Extensions:** Registra `ASInspectorPlugin` para property editores customizados
4. **Tags Panel:** Instancia `ASTagsPanel` no editor para gerenciamento visual de tags
5. **Type Safety:** Habilita validação de tipo em tempo de design

Carregado automaticamente quando projeto abre (via plugin.cfg).

## Herança

```
EditorPlugin
 └─ ASEditorPlugin
```

## Inicialização Automática

**Via `plugin.cfg`:**

```ini
[plugin]
name = "Ability System"
description = "Framework modular para combate e habilidades"
author = "MachiTwo"
version = "0.1.0"
script = "ASEditorPlugin.gd"
```

Quando `godot` abre projeto com plugin.cfg válido, carrega automaticamente `ASEditorPlugin._enter_tree()`.

## Responsabilidades

### 1. Registro de Tipos

Ao carregar, `ASEditorPlugin` registra todos os recursos do Ability System:

```
ASAbility → Resource icon
ASEffect → Resource icon
ASAttributeSet → Resource icon
ASContainer → Resource icon
ASPackage → Resource icon
ASCue → Feedback icon
ASAbilityPhase → Fase icon
ASAbilitySpec → Spec icon
... (todos os tipos expostos)
```

Permite no FileSystem: New Resource → AS\* Types aparecem como opções.

### 2. Ícones Customizados

Cada tipo tem ícone visual:

- **ASAbility**: Ícone de skill/magia
- **ASEffect**: Ícone de modificador/buff
- **ASContainer**: Ícone de arquétipo
- **ASPackage**: Ícone de envelope/entrega
- **ASCue**: Ícone de feedback

Melhor UX—visual identification no editor.

### 3. Inspector Extensions (ASInspectorPlugin)

Registra properties customizadas para type-safety:

```gdscript
# Campo "activation_required_all_tags" recusa tags NAME
# Campo "ability_name" recusa tags EVENT
# Campo "event_dispatch" recusa tudo exceto EVENT
```

Ocorre via `ASInspectorPlugin`—validação automática ao editar.

### 4. Tags Panel (ASTagsPanel)

Instancia interface visual para tag management:

```
Project Settings → Ability System (Painel customizado)
├─ NAME Tags (identidade)
├─ CONDITIONAL Tags (estados)
└─ EVENT Tags (eventos)
```

Permite add/remove tags globais sem editar código.

### 5. Validação de Projeto

Ao carregar, pode validar:

- Todas as tags estão registradas
- Tipos customizados carregam sem erro
- Recursos teem IDs únicos (naming convention)

## Ciclo de Vida

```
_enter_tree()
  ├─ Register tipos AS* no editor
  ├─ Instancia ícones customizados
  ├─ Registra ASInspectorPlugin
  └─ Instancia ASTagsPanel

... (projeto rodando) ...

_exit_tree()
  ├─ Remove inspector plugin
  ├─ Limpa ícones
  └─ Fecha tags panel
```

## Configuração do Projeto

Plugin é configurável via `project.godot`:

```ini
[ability_system]
enabled = true
tags = ["ability.fireball", "state.burning", "event.damage"]
tag_types = [0, 1, 2]  # NAME, CONDITIONAL, EVENT
```

## Uso (Automático)

Plugin funciona transparentemente. Desenvolvedores não precisam chamar direto. Apenas:

1. Crie novo Resource (FileSystem → New Resource → ASAbility)
2. Configure properties
3. Inspector plugin valida tipos automaticamente
4. Project Settings → Ability System para gerenciar tags globais

## Integração com AbilitySystem (Singleton)

`ASEditorPlugin` sincroniza com `AbilitySystem` singleton:

```gdscript
# Dentro de _enter_tree():
AbilitySystem.register_tag(&"ability.fireball", ASTagType.NAME)
AbilitySystem.register_tag(&"state.burning", ASTagType.CONDITIONAL)
# ... (todas as tags do projeto)
```

Carrega tags persistidas em `project.godot` ao iniciar.

## Melhor Prática

**Não sobrescreva métodos internos**—plugin é automático. Se customizar:

1. Faça subclass de `ASEditorPlugin`
2. Chame `super._enter_tree()` e `super._exit_tree()`
3. Adicione lógica customizada (ex: validação extra)

```gdscript
class_name CustomAbilityEditorPlugin
extends ASEditorPlugin

func _enter_tree():
    super._enter_tree()
    # Custom initialization
    validate_all_resources()

func _exit_tree():
    super._exit_tree()
    # Custom cleanup
```

## Debugging

Para verificar se plugin carregou:

```gdscript
# No console do editor
print(AbilitySystem)  # Deve ser singleton válido
print(AbilitySystem.get_all_registered_tags())  # Deve listar tags
```

Se plugin não carrega:

1. Verifique `plugin.cfg` sintaxe
2. Verifique caminho `script` em `plugin.cfg`
3. Abra Project Settings → Plugins, ative "Ability System"

## Referências Relacionadas

- [ASInspectorPlugin](asinspectorplugin.md) — Property editores customizados
- [ASTagsPanel](astagspanel.md) — Interface de tags
- [AbilitySystem](../singleton/ability-system.md) — Singleton registrado

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
