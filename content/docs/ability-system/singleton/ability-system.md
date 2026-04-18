---
title: "AbilitySystem"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# AbilitySystem

**Badge:** `Singleton` • `Object`

## Descrição Breve

Central authority para gerenciamento global de Tags e registro de componentes.

## Descrição Completa

`AbilitySystem` é um singleton que gerencia o registro global de tags para todo o projeto. Atua como:

1. **Registro Central de Tags**: Armazena e valida todas as tags (NAME, CONDITIONAL, EVENT)
2. **Resolutor de Componentes**: Localiza `ASComponent` em árvores de cena com segurança
3. **Autoridade de Type-Safety**: Impede em tempo de edição que tags do tipo errado sejam usadas em campos restritos
4. **Integração Project Settings**: Salva e carrega tags nas configurações do projeto (`project.godot`)

Nenhuma tag deve ser usada sem estar registrada aqui. O sistema valida tipos e oferece autocomplete automático no
editor.

## Herança

```
Object
 └─ AbilitySystem (Singleton)
```

Acesso via `AbilitySystem.get_singleton()` ou `AbilitySystem`.

## Constantes (ASTagType)

| Constante     | Valor | Significado                                                                  |
| ------------- | ----- | ---------------------------------------------------------------------------- |
| `NAME`        | 0     | Identidade estática — usado para identificar resources (ASAbility, ASEffect) |
| `CONDITIONAL` | 1     | Estado persistente — usado em requisitos/bloqueios de abilities/effects      |
| `EVENT`       | 2     | Ocorrência instantânea — dispatched transitori via ASTagUtils                |

## Métodos

### Registro de Tags

#### `register_tag(tag: StringName, type: int = NAME, owner_id: int = 0) → void`

Registra uma nova tag globalmente com tipo específico.

**Parâmetros:**

- `tag`: Identificador da tag (ex: `&"ability.fireball"`)
- `type`: Tipo da tag (`ASTagType.NAME`, `CONDITIONAL`, ou `EVENT`)
- `owner_id`: ID da instância owner (opcional)

**Exemplo:**

```gdscript
AbilitySystem.register_tag(&"ability.fireball", AbilitySystem.ASTagType.NAME)
AbilitySystem.register_tag(&"state.burning", AbilitySystem.ASTagType.CONDITIONAL)
AbilitySystem.register_tag(&"event.damage", AbilitySystem.ASTagType.EVENT)
```

#### `unregister_tag(tag: StringName) → void`

Remove uma tag do registro global.

#### `remove_tag_branch(tag: StringName) → void`

Remove uma tag e todas suas sub-tags hierárquicas. Exemplo: remover `"state"` também remove `"state.stunned"` e
`"state.burning"`.

#### `rename_tag(old_tag: StringName, new_tag: StringName) → void`

Renomeia uma tag e atualiza automaticamente todas as sub-tags. Exemplo: `"state"` → `"condition"` atualiza
`"state.stunned"` para `"condition.stunned"`.

### Consultas de Tags

#### `is_tag_registered(tag: StringName) → bool` (const)

Verifica se uma tag está registrada no sistema.

**Exemplo:**

```gdscript
if AbilitySystem.is_tag_registered(&"ability.fireball"):
    print("Tag é válida!")
```

#### `get_tag_type(tag: StringName) → int` (const)

Retorna o tipo de uma tag registrada.

**Retorna:** `ASTagType.NAME`, `CONDITIONAL`, ou `EVENT`

**Exemplo:**

```gdscript
var tag_type = AbilitySystem.get_tag_type(&"state.stunned")
if tag_type == AbilitySystem.ASTagType.CONDITIONAL:
    print("É um estado condicional")
```

#### `get_all_registered_tags() → StringName[]` (const)

Retorna array de todas as tags registradas (NAME, CONDITIONAL, EVENT).

#### `get_registered_tags_of_type(type: int) → StringName[]` (const)

Retorna tags registradas apenas do tipo especificado.

**Parâmetros:**

- `type`: `ASTagType.NAME`, `CONDITIONAL`, ou `EVENT`

**Exemplo:**

```gdscript
var conditional_tags = AbilitySystem.get_registered_tags_of_type(
    AbilitySystem.ASTagType.CONDITIONAL
)
```

### Comparação Hierárquica de Tags

#### `tag_matches(tag: StringName, match_against: StringName, exact: bool = false) → bool` (static)

Comparação hierárquica de tags com suporte a wildcards.

**Parâmetros:**

- `tag`: Tag a verificar
- `match_against`: Pattern para comparação
- `exact`: Se `true`, faz match exato (string)

**Exemplo:**

```gdscript
# Hierárquico (padrão)
AbilitySystem.tag_matches(&"state.stunned.freeze", &"state.stunned")  # true
AbilitySystem.tag_matches(&"state.stunned.freeze", &"state")          # true

# Exato
AbilitySystem.tag_matches(&"state.stunned", &"state.stunned", true)   # true
AbilitySystem.tag_matches(&"state.stunned", &"state", true)           # false
```

### Resolução de Componentes

#### `get_component_from_node(node: Node) → ASComponent` (static)

Localiza um `ASComponent` a partir de um node.

**Lógica:**

1. Se `node` é um `ASComponent`, retorna ele
2. Se `node` tem `ASComponent` como child, retorna child
3. Caso contrário, retorna `null`

**Exemplo:**

```gdscript
var asc = AbilitySystem.get_component_from_node(player_node)
if asc:
    asc.try_activate_ability_by_tag(&"ability.slash")
```

#### `resolve_component(agent: Node, path: NodePath = NodePath("")) → ASComponent` (static)

Advanced utility para localizar `ASComponent` com múltiplos pontos de fallback.

**Ordem de Resolução:**

1. Se `path` fornecido, tenta resolver aquele caminho relativo ao `agent`
2. Se `agent` é um `ASComponent`, retorna ele
3. Busca children imediatos do `agent`
4. Busca parent do `agent` e seus children
5. Busca owner do `agent` e seus children

**Parâmetros:**

- `agent`: Node de origem
- `path`: Caminho específico (opcional)

**Exemplo:**

```gdscript
# Resolução automática
var asc = AbilitySystem.resolve_component(character_body)

# Com caminho específico
var asc = AbilitySystem.resolve_component(character_body, ^"AbilityComponent")
```

### Nomes de Recursos

#### `register_resource_name(name: String, owner_id: int) → bool`

Registra um nome único para um resource.

**Retorna:** `true` se registrado com sucesso, `false` se nome já existe

#### `unregister_resource_name(name: String) → void`

Remove registro de nome de resource.

#### `get_resource_name_owner(name: String) → int` (const)

Retorna o instance ID do resource que possui o nome.

### Testes Internos

#### `run_tests() → int`

Executa suite completa de testes unitários internos. Usado para validação CI/CD.

**Retorna:** `0` se todos os testes passarem, ou número de testes que falharam

**Exemplo:**

```gdscript
if AbilitySystem.run_tests() != 0:
    push_error("Testes do Ability System falharam!")
```

## Sinais

#### `tags_changed` → void

Emitido quando o registro global de tags foi modificado (tag adicionada/removida/renomeada).

**Emitido por:**

- `register_tag()`
- `unregister_tag()`
- `remove_tag_branch()`
- `rename_tag()`

**Exemplo:**

```gdscript
func _ready():
    AbilitySystem.tags_changed.connect(_on_tags_changed)

func _on_tags_changed():
    print("Tags foram atualizadas")
    refresh_ui()
```

## Regras de Utilização

### SSOT (Single Source of Truth)

`AbilitySystem` é a ÚNICA fonte confiável para:

- Lista global de tags
- Tipos de tags
- Validação em tempo de design

Sempre registrar tags aqui antes de usar em qualquer lugar.

### Type-Safety: TAG types não são intercambiáveis

```gdscript
# ❌ ERRADO: Tag NAME usada para bloquear (deve ser CONDITIONAL)
ability.activation_blocked_any_tags.append(&"ability.other_attack")

# ✅ CERTO: Tag CONDITIONAL para bloquear
ability.activation_blocked_any_tags.append(&"state.silenced")
```

O **ASInspectorPlugin** valida isso no editor (campos de requisito/bloqueio recusam tipos inválidos).

### Hierarquia Automática

Pontos (`.`) criam ramos visualmente no **ASTagsPanel**:

```
state
  ├─ stunned
  ├─ burning
  └─ frozen

ability
  ├─ warrior
  │   ├─ slash
  │   └─ shield
  └─ mage
      └─ fireball
```

Registrar apenas a raiz:

```gdscript
AbilitySystem.register_tag(&"state.stunned")      # Raiz "state" criada automaticamente
AbilitySystem.register_tag(&"state.burning")      # Mesmo grupo
```

### Integração Project Settings

Tags são persistidas em `project.godot` via `project_settings`. Ao carregar o projeto:

```
[ability_system]
tags = ["ability.fireball", "state.stunned", "event.damage"]
tag_types = [0, 1, 2]  # NAME, CONDITIONAL, EVENT
```

## Casos de Uso

### Configurar Vocabulário do Projeto

```gdscript
func _ready():
    # Abilities
    AbilitySystem.register_tag(&"ability.fireball", AbilitySystem.ASTagType.NAME)
    AbilitySystem.register_tag(&"ability.ice_blast", AbilitySystem.ASTagType.NAME)

    # States
    AbilitySystem.register_tag(&"state.burning", AbilitySystem.ASTagType.CONDITIONAL)
    AbilitySystem.register_tag(&"state.frozen", AbilitySystem.ASTagType.CONDITIONAL)
    AbilitySystem.register_tag(&"state.stunned", AbilitySystem.ASTagType.CONDITIONAL)

    # Events
    AbilitySystem.register_tag(&"event.damage", AbilitySystem.ASTagType.EVENT)
    AbilitySystem.register_tag(&"event.heal", AbilitySystem.ASTagType.EVENT)
```

### Encontrar Componente de NPC

```gdscript
var npc = get_tree().get_first_node_in_group("npcs")
var asc = AbilitySystem.resolve_component(npc)

if asc and asc.can_activate_ability_by_tag(&"ability.talk"):
    asc.try_activate_ability_by_tag(&"ability.talk")
```

### Validar Tag Antes de Usar

```gdscript
func apply_burning_effect(target: ASComponent):
    if not AbilitySystem.is_tag_registered(&"state.burning"):
        push_error("Tag 'state.burning' não está registrada!")
        return

    var tag_type = AbilitySystem.get_tag_type(&"state.burning")
    if tag_type != AbilitySystem.ASTagType.CONDITIONAL:
        push_error("'state.burning' deve ser CONDITIONAL!")
        return

    # Agora é seguro usar
    target.apply_effect_by_tag(&"state.burning")
```

### Listar Todas as Abilities

```gdscript
var ability_tags = AbilitySystem.get_registered_tags_of_type(
    AbilitySystem.ASTagType.NAME
).filter(func(tag): return tag.begins_with("ability."))

for ability_tag in ability_tags:
    print("Ability disponível: ", ability_tag)
```

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Hub que usa estas tags
- [ASAbility](../resources/asability.md) — Define requisitos/bloqueios
- [ASEffect](../resources/aseffect.md) — Define requisitos/bloqueios
- [ASTagUtils](../refcounted/astagutils.md) — Utilidades de manipulação histórica

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
