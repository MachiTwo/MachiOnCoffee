---
title: "ASComponent"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `Node`

## Descrição Breve

Hub central para gerenciar abilities, efeitos, atributos e tags de um ator.

## Descrição Completa

`ASComponent` (ASC) é o coração do Ability System. Orquestra:

- **Ativação de Abilities**: Valida e executa abilities
- **Aplicação de Effects**: Gerencia efectos ativos com durações/stacks
- **Atributos**: Mantém stats do ator (HP, Mana, Força, etc)
- **Tags**: Adiciona/remove tags que representam estado do ator
- **Cues**: Dispara feedback audiovisual
- **Sinais**: Notifica sistema de mudanças
- **Multiplayer**: Buffer de estado para predição/rollback
- **Node Registry**: Conhece nós customizados para Cues

Deve ser **child de CharacterBody2D ou CharacterBody3D**.

## Herança

```gdscript
Node
 └─ ASComponent
```gdscript

## Propriedades

| Propriedade      | Tipo            | Padrão | Descrição                                               |
| ---------------- | --------------- | ------ | ------------------------------------------------------- |
| `container`      | ASContainer     | `null` | Arquétipo a carregar na inicialização                   |
| `snapshot_state` | ASStateSnapshot | `null` | Recurso para persistência de estado (multiplayer/saves) |

## Métodos Principais (Gameplay)

## Inicialização

## `apply_container(container: ASContainer, level: int = 1) → void`

Carrega container completo:

1. Deep-clona AttributeSet
2. Carrega abilities do catálogo
3. Aplica effects iniciais

**Parâmetros:**

- `container`: Arquétipo a aplicar
- `level`: Nível do ator (escala modificadores)

**Exemplo:**

```gdscript
asc.apply_container(warrior_container, level=5)
```gdscript

## Ativação de Abilities

## `try_activate_ability_by_tag(tag: StringName) → bool`

Ativação segura de ability por tag. **Método preferido para gameplay.**

Valida automaticamente:

- Tags requeridas/bloqueadas
- Custos (recursos suficientes)
- Cooldown (não em espera)

**Retorna:** `true` se sucesso, `false` se falha

**Emite:** `ability_activated` (sucesso) ou `ability_failed` (falha)

**Exemplo:**

```gdscript
if asc.try_activate_ability_by_tag(&"ability.fireball"):
    print("Fireball lançada!")
else:
    print("Falhou—faltam recursos/cooldown/requisitos")
```gdscript

## `try_activate_ability_by_resource(ability: ASAbility) → bool`

Ativação segura por referência direta (menos comum).

## `can_activate_ability_by_tag(tag: StringName) → bool` (const)

Pré-validação sem efeitos colaterais.

**Exemplo:**

```gdscript
if asc.can_activate_ability_by_tag(&"ability.slash"):
    # UI pode habilitar botão
```gdscript

## Aplicação de Effects

## `apply_effect_by_tag(tag: StringName, level: float = 1.0, target_node: Object = null) → void`

Aplica effect do container por tag. **Sem validações** (uso de infraestrutura).

## `apply_effect_by_resource(effect: ASEffect, level: float = 1.0, target_node: Object = null) → void`

Aplica effect por referência. **Sem validações.**

## `apply_package(package: ASPackage, level: float = 1.0, source_component: ASComponent = null) → void`

Aplica todos effects e cues de um package.

**Usado por:**

- ASDelivery (projectiles)
- Direct calls

**Exemplo:**

```gdscript
asc.apply_package(fireball_package)
```gdscript

## `apply_effect_spec_to_self(spec: ASEffectSpec) → void`

Aplica spec já-construído com validação de tags.

## `apply_effect_spec_to_target(spec: ASEffectSpec, target: ASComponent) → void`

Aplica effect a outro componente.

## Gerenciamento de Tags

## `add_tag(tag: StringName) → void`

Adiciona tag ao ator.

**Emite:** `tag_added` signal

**Exemplo:**

```gdscript
asc.add_tag(&"state.burning")
asc.add_tag(&"class.warrior")
```gdscript

## `remove_tag(tag: StringName) → void`

Remove tag.

**Emite:** `tag_removed` signal

## `has_tag(tag: StringName) → bool` (const)

Verifica se ator tem tag.

**Suporta hierarquia:**

```gdscript
asc.has_tag(&"state.stunned.freeze")  # true se tem
asc.has_tag(&"state.stunned")         # true se tem stunned.freeze
asc.has_tag(&"state")                 # true se tem qualquer state
```gdscript

## `get_all_tags() → StringName[]` (const)

Retorna todas as tags do ator.

## Atributos

## `set_attribute_base_value(attribute: StringName, value: float) → void`

Define valor base de atributo (antes de modificadores).

## `get_attribute_base_value(attribute: StringName) → float` (const)

Lê valor base.

## `get_attribute_current_value(attribute: StringName) → float` (const)

Lê valor atual (base + modificadores, clamped min/max).

**Exemplo:**

```gdscript
asc.set_attribute_base_value(&"health", 100.0)
asc.set_attribute_base_value(&"mana", 50.0)

var hp = asc.get_attribute_current_value(&"health")  # 100
var mana = asc.get_attribute_current_value(&"mana")  # 50
```gdscript

## Multiplayer (Predição/Rollback)

## `capture_snapshot() → void`

Congela estado atual para rollback.

**Chamado antes de ativação preditiva:**

```gdscript
asc.capture_snapshot()  # Salva estado atual
asc.try_activate_ability_by_tag(&"ability.attack")  # Local prediction
asc.request_activate_ability.rpc_id(1, &"ability.attack")  # Envia server
```gdscript

## `apply_snapshot(tick: int) → void`

Restaura estado de tick anterior.

Tenta recuperar de **ASStateCache** (128 ticks) primeiro. Se mais antigo, carrega de `snapshot_state` resource.

**Usado para rollback:**

```gdscript
asc.apply_snapshot(authoritative_tick_id)
```gdscript

## Cálculos

## `calculate_effect_duration(spec: ASEffectSpec) → float` (const)

Calcula duração final considerando customizações.

## `calculate_modifier_magnitude(index: int, spec: ASEffectSpec) → float` (const)

Calcula magnitude final de modificador.

## Callbacks Virtuais

## `_on_calculate_custom_magnitude(effect_spec: ASEffectSpec, modifier_index: int) → float` (virtual const)

Override para cálculo customizado de magnitude (ex: scaling com inteligência).

**Exemplo:**

```gdscript
func _on_calculate_custom_magnitude(effect_spec: ASEffectSpec, modifier_index: int) -> float:
    if modifier_index == 0:  # Primeiro modificador
        return get_attribute_current_value(&"intelligence") * 0.5
    return 0.0
```gdscript

## Sinais

| Sinal               | Parâmetros                                | Emitido por                               |
| ------------------- | ----------------------------------------- | ----------------------------------------- |
| `ability_activated` | `tag: StringName`                         | `try_activate_ability_by_tag()` (sucesso) |
| `ability_failed`    | `tag: StringName, reason: String`         | Validação falhou                          |
| `effect_applied`    | `tag: StringName`                         | `apply_effect_*()` sucesso                |
| `effect_removed`    | `tag: StringName`                         | Efeito expirou/removido                   |
| `tag_added`         | `tag: StringName`                         | `add_tag()`                               |
| `tag_removed`       | `tag: StringName`                         | `remove_tag()`                            |
| `attribute_changed` | `attribute: StringName, new_value: float` | Modificador aplicado                      |

**Exemplo:**

```gdscript
func _ready():
    asc.ability_activated.connect(_on_ability_activated)
    asc.tag_added.connect(_on_tag_added)
    asc.attribute_changed.connect(_on_attribute_changed)

func _on_ability_activated(tag: StringName):
    print("Ativou: ", tag)
    play_activation_animation(tag)

func _on_tag_added(tag: StringName):
    if tag == &"state.burning":
        $Sprite.modulate = Color.RED  # Visual feedback
```gdscript

## Casos de Uso

## Setup Inicial

```gdscript
@onready var asc = $ASComponent

func _ready():
    # Aplicar arquétipo
    asc.apply_container(warrior_container)

    # Conectar sinais
    asc.ability_activated.connect(_on_ability_activated)
    asc.tag_added.connect(_on_tag_added)
    asc.attribute_changed.connect(_on_attribute_changed)
```gdscript

## Input Handling

```gdscript
func _physics_process(delta):
    if Input.is_action_just_pressed("ability_fireball"):
        if asc.try_activate_ability_by_tag(&"ability.fireball"):
            velocity = Vector2.ZERO  # Freeze durante cast
        else:
            print_debug("Falhou—sem mana?")
```gdscript

## Efeito de Dano

```gdscript
func take_damage(amount: float):
    # Aplicar efeito de dano
    var damage_effect = create_damage_effect(amount)
    asc.apply_effect_by_resource(damage_effect)

    # Ou via package (projectile)
    asc.apply_package(projectile_package, source=projectile_owner)

    # Verificar morte
    if asc.get_attribute_current_value(&"health") <= 0:
        die()
```gdscript

## Multiplayer (Client Prediction)

```gdscript
func _physics_process(delta):
    if is_local_authority():
        asc.capture_snapshot()

        if Input.is_action_just_pressed("fire"):
            asc.try_activate_ability_by_tag(&"ability.slash")
            asc.request_activate_ability.rpc_id(1, &"ability.slash")
```gdscript

## Server Reconciliation

```gdscript
@rpc("any_peer", "call_local")
func request_activate_ability(tag: StringName):
    if is_server():
        if asc.can_activate_ability_by_tag(tag):
            asc.try_activate_ability_by_tag(tag)
            asc.confirm_ability_activation.rpc(tag)
        else:
            # Predição falhou
            asc.apply_snapshot(correct_tick_id)
            asc.deny_ability_activation.rpc(tag)
```gdscript

## Performance Tips

1. **Reuse Specs**: Não criar ASAbilitySpec novo a cada ativação
2. **Tag Hierarchy**: Use `has_tag(&"state")` em vez de múltiplas checks
3. **Snapshot**: Use ASStateSnapshot apenas em players, não em NPCs massivos
4. **Custom Magnitude**: Evitar cálculos complexos em callbacks (cache valores)

## Referências Relacionadas

- [AbilitySystem](../singleton/ability-system.md) — Registro global
- [ASContainer](../resources/ascontainer.md) — Arquétipo
- [ASAbility](../resources/asability.md) — Ability
- [ASEffect](../resources/aseffect.md) — Effect
- [ASDelivery](asdelivery.md) — Entrega física
- [ASStateCache](../refcounted/asstatecache.md) — Buffer rollback

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
