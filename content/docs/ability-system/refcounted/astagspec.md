---
title: "ASTagSpec"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `RefCounted`

## Descrição Breve

Coleção gerenciada de tags com suporte a hierarquia e reference counting.

## Descrição Completa

`ASTagSpec` é um container que mantém um conjunto de tags únicas com reference counting automático. Cada tag pode
existir múltiplas vezes (stacking), e é removida apenas quando refcount atinge zero.

Usado internamente por `ASComponent` para gerenciar tags ativas. Suporta matching hierárquico (ex: `state.stunned`
combina com `state`).

## Herança

````gdscript
RefCounted
 └─ ASTagSpec
```gdscript

## Métodos Públicos

## Adição e Remoção

## `add_tag(tag: StringName) → bool`

Adiciona tag ao container.

**Retorna:** `true` se primeira referência, `false` se já existia (refcount incrementado).

**Comportamento:**

- Cada adicional incrementa refcount
- Reference counting automático permite múltiplas origens concederem mesma tag
- Exemplo: Se "state.stunned" adicionada 3 vezes, precisa de 3 remoções

```gdscript
tag_spec.add_tag(&"state.stunned")  # refcount = 1
tag_spec.add_tag(&"state.stunned")  # refcount = 2
tag_spec.remove_tag(&"state.stunned")  # refcount = 1
tag_spec.remove_tag(&"state.stunned")  # refcount = 0, removida
```gdscript

## `remove_tag(tag: StringName) → bool`

Remove tag (decrementa refcount).

**Retorna:** `true` se refcount atingiu zero (tag realmente removida), `false` se ainda referenciada.

```gdscript
var was_removed = tag_spec.remove_tag(&"state.burning")
if was_removed:
    print("State burning foi realmente removido")
else:
    print("Ainda há referências a state.burning")
```gdscript

## Consultas

## `has_tag(tag: StringName, exact: bool = false) → bool` (const)

Verifica se container possui tag.

**Parâmetros:**

- `tag`: Tag a buscar
- `exact`: Se `true`, match exato; se `false`, match hierárquico

**Match Hierárquico (exact=false):**

```gdscript
tag_spec.add_tag(&"state.stunned.freeze")

tag_spec.has_tag(&"state.stunned.freeze")  # true (exato)
tag_spec.has_tag(&"state.stunned")         # true (parent)
tag_spec.has_tag(&"state")                 # true (raiz)
tag_spec.has_tag(&"other")                 # false
```gdscript

**Match Exato (exact=true):**

```gdscript
tag_spec.add_tag(&"state.stunned.freeze")

tag_spec.has_tag(&"state.stunned.freeze", true)  # true
tag_spec.has_tag(&"state.stunned", true)         # false
tag_spec.has_tag(&"state", true)                 # false
```gdscript

## `has_any_tags(tags: StringName[], exact: bool = false) → bool` (const)

Verifica se container possui QUALQUER UM das tags.

```gdscript
var blocking_tags = [&"state.stunned", &"state.silenced"]
if tag_spec.has_any_tags(blocking_tags):
    print("Pode atacar? Não—está stunned ou silenced")
```gdscript

## `has_all_tags(tags: StringName[], exact: bool = false) → bool` (const)

Verifica se container possui TODAS as tags.

```gdscript
var required_tags = [&"state.empowered", &"state.focused"]
if tag_spec.has_all_tags(required_tags):
    print("Todos os buffs ativos—pode usar ultimate")
```gdscript

## Iteração

## `get_all_tags() → StringName[]` (const)

Retorna array de todas as tags no container.

```gdscript
for tag in tag_spec.get_all_tags():
    print("Tag ativa: ", tag)
```gdscript

## Limpeza

## `clear() → void`

Remove todas as tags (reseta refcounts para zero).

```gdscript
tag_spec.clear()
# Útil para reset de estado ou respawn
```gdscript

## Comportamento de Reference Counting

**Padrão Padrão:**

Múltiplas fontes podem conceder a mesma tag. Tag permanece até que todas as fontes a removam.

```gdscript
var tags = ASTagSpec.new()

# Fonte A: ativa state.burning (duração 5s)
tags.add_tag(&"state.burning")

# Fonte B: ativa estado.burning (duração 10s)
tags.add_tag(&"state.burning")

# Após 5s, Fonte A remove:
tags.remove_tag(&"state.burning")  # refcount = 1, tag PERMANECE

# Após 10s, Fonte B remove:
tags.remove_tag(&"state.burning")  # refcount = 0, tag REMOVIDA
```gdscript

**Aplicação Prática:**

```gdscript
# Efeito 1: Concede "state.vulnerable" por 3s
ability1.effects.append(create_effect_with_tag(&"state.vulnerable", 3.0))

# Efeito 2: Concede "state.vulnerable" por 5s
ability2.effects.append(create_effect_with_tag(&"state.vulnerable", 5.0))

# Se ambos aplicados simultaneamente:
# - ASComponent.add_tag(&"state.vulnerable") chamado 2 vezes
# - ASTagSpec refcount = 2
# - Após 3s (efeito 1 expira): remove chamado, refcount = 1
# - Tag PERMANECE (efeito 2 ainda ativo)
# - Após 5s (efeito 2 expira): remove chamado, refcount = 0
# - Tag REMOVIDA
```gdscript

## Casos de Uso

## Verificar Requisito de Ability

```gdscript
func can_perform_ultimate(tag_spec: ASTagSpec) -> bool:
    # Ultimate requer todos estes estados
    return tag_spec.has_all_tags([
        &"state.empowered",
        &"state.focused",
        &"class.mage"
    ])
```gdscript

## Aplicar Effect Condicional

```gdscript
func apply_defensive_effect(tag_spec: ASTagSpec):
    if tag_spec.has_tag(&"state.burning"):
        # Se queimando, água extingue
        apply_effect(&"effect.extinguish_fire")
    elif tag_spec.has_tag(&"state.frozen"):
        # Se congelado, fogo descongela
        apply_effect(&"effect.unfreeze")
```gdscript

## Gerenciar Buffs Mutualmente Exclusivos

```gdscript
func apply_buff(tag_spec: ASTagSpec, buff_tag: StringName):
    # Buffs de estância mutualmente exclusivos
    var stance_tags = [&"stance.aggressive", &"stance.defensive", &"stance.balanced"]

    # Remove antigas estâncias
    for old_stance in stance_tags:
        if tag_spec.has_tag(old_stance):
            tag_spec.remove_tag(old_stance)

    # Adiciona nova
    tag_spec.add_tag(buff_tag)
```gdscript

## Implementar Imunidade Condicional

```gdscript
func can_apply_effect(tag_spec: ASTagSpec, effect: ASEffect) -> bool:
    # Verificar imunidades
    for tag in effect.requires_all_tags:
        if not tag_spec.has_tag(tag):
            return false

    for tag in effect.blocks_on_any_tags:
        if tag_spec.has_tag(tag):
            return false  # Bloqueado por tag

    return true
```gdscript

## Debug: Listar Todos os Estados Ativos

```gdscript
func debug_print_active_tags(tag_spec: ASTagSpec):
    print("Estados ativos:")
    for tag in tag_spec.get_all_tags():
        print("  - ", tag)
```gdscript

## Integração com ASComponent

`ASComponent` usa `ASTagSpec` internamente:

```gdscript
# ASComponent.add_tag chama internamente:
# tag_container.add_tag(tag)

# ASComponent.remove_tag chama:
# tag_container.remove_tag(tag)

# ASComponent.has_tag chama:
# tag_container.has_tag(tag, exact_match)
```gdscript

Você não interage diretamente—use API pública de `ASComponent`.

## Performance

**Muito Eficiente:**

- O(1) add/remove (hashtable interna)
- O(n) para has_any_tags/has_all_tags (n = número de tags verificadas, não total no container)
- Nenhuma alocação em operações críticas

**Uso Automático:** `ASComponent` gerencia—nenhuma criação manual necessária.

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Usa ASTagSpec internamente
- [AbilitySystem](../singleton/ability-system.md) — Registro global de tags
- [ASTagUtils](astagutils.md) — Utilitários de histórico de tags

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
