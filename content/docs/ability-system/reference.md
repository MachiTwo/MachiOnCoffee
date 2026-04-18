---
title: "Referência Rápida"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

Índice compilado de todas as classes, métodos e constantes.

## 🔐 Singleton

## [AbilitySystem](singleton/ability-system.md)

**Registro global central de tags e componentes**

```gdscript
# Tags
AbilitySystem.register_tag(&"ability.fireball", ASTagType.NAME)
AbilitySystem.is_tag_registered(&"state.stunned")
AbilitySystem.get_tag_type(&"state.burning")
AbilitySystem.get_all_registered_tags()
AbilitySystem.get_registered_tags_of_type(ASTagType.CONDITIONAL)
AbilitySystem.rename_tag(&"old", &"new")
AbilitySystem.remove_tag_branch(&"state")

# Comparação
AbilitySystem.tag_matches(&"state.stunned.freeze", &"state")  # true

# Componentes
AbilitySystem.get_component_from_node(node)
AbilitySystem.resolve_component(agent, path)

# Nomes
AbilitySystem.register_resource_name("MyAbility", id)
AbilitySystem.get_resource_name_owner("MyAbility")

# Testes
AbilitySystem.run_tests()

# Sinais
AbilitySystem.tags_changed
```gdscript

---

## 📦 Resources (Blueprints Imutáveis)

## [ASAbility](resources/asability.md)

**Define lógica de uma ação**

| Propriedade                    | Tipo         | Descrição                      |
| ------------------------------ | ------------ | ------------------------------ |
| `ability_tag`                  | StringName   | Identificador (NAME)           |
| `ability_duration_policy`      | int          | INSTANT / DURATION / INFINITE  |
| `cooldown_duration`            | float        | Segundos                       |
| `costs`                        | Dict[]       | Custos de atributo             |
| `requirements`                 | Dict[]       | Requisitos de atributo         |
| `activation_required_all_tags` | StringName[] | Deve ter TODAS (AND)           |
| `activation_required_any_tags` | StringName[] | Deve ter QUALQUER UMA (OR)     |
| `activation_blocked_any_tags`  | StringName[] | Falha se tiver QUALQUER UMA    |
| `activation_blocked_all_tags`  | StringName[] | Falha se tiver TODAS           |
| `activation_owned_tags`        | StringName[] | Tags concedidas                |
| `activation_cancel_tags`       | StringName[] | Abilities canceladas ao ativar |
| `effects`                      | ASEffect[]   | Effects aplicados              |
| `phases`                       | ASAbility[]  | Fases da ability               |
| `triggers`                     | Dict[]       | Ativação automática            |

```gdscript
# Métodos principais
ability.try_activate_ability(owner, spec)
ability.can_activate_ability(owner)
ability.add_cost(&"mana", 30.0)
ability.add_requirement(&"intelligence", 50.0)
ability.can_afford_costs(owner)
ability.add_trigger(&"state.on_fire", TRIGGER_ON_TAG_ADDED)
```gdscript

**Constantes:**

```gdscript
enum DurationPolicy { INSTANT=0, DURATION=1, INFINITE=2 }
enum TriggerType { ON_TAG_ADDED=0, ON_TAG_REMOVED=1, ON_EVENT=2 }
```gdscript

---

## [ASEffect](resources/aseffect.md)

**Define modificadores e state changes**

| Propriedade                            | Tipo         | Descrição                                      |
| -------------------------------------- | ------------ | ---------------------------------------------- |
| `effect_tag`                           | StringName   | Identificador (NAME)                           |
| `duration_policy`                      | int          | INSTANT / DURATION / INFINITE                  |
| `duration_magnitude`                   | float        | Duração base                                   |
| `stacking_policy`                      | int          | NEW_INSTANCE / OVERRIDE / INTENSITY / DURATION |
| `period`                               | float        | Intervalo periódico (DoT/HoT)                  |
| `execute_periodic_tick_on_application` | bool         | Executa tick imediatamente                     |
| `target_type`                          | int          | SELF / OTHERS                                  |
| `granted_tags`                         | StringName[] | Tags concedidas                                |
| `removed_tags`                         | StringName[] | Tags removidas                                 |
| `activation_required_all_tags`         | StringName[] | Requer TODAS                                   |
| `activation_required_any_tags`         | StringName[] | Requer QUALQUER UMA                            |
| `activation_blocked_any_tags`          | StringName[] | Bloqueado por QUALQUER UMA                     |
| `activation_blocked_all_tags`          | StringName[] | Bloqueado por TODAS                            |

```gdscript
# Métodos
effect.add_modifier(&"health", OP_ADD, -30.0)
effect.add_modifier(&"health", OP_MULTIPLY, 0.5)
effect.get_modifier_count()
effect.get_modifier_attribute(0)
effect.get_modifier_operation(0)
effect.get_modifier_magnitude(0)
```gdscript

**Constantes:**

```gdscript
enum DurationPolicy { INSTANT=0, DURATION=1, INFINITE=2 }
enum StackingPolicy { NEW_INSTANCE=0, OVERRIDE=1, INTENSITY=2, DURATION=3 }
enum TargetType { SELF=0, OTHERS=1 }
enum ModifierOp { ADD=0, MULTIPLY=1, DIVIDE=2, OVERRIDE=3 }
```gdscript

---

## [ASAttribute & ASAttributeSet](resources/asattributeset.md)

**Sistema de atributos e stats**

```gdscript
attribute_set.add_attribute(&"health", 0.0, 100.0, 100.0)
attribute_set.add_driver(&"damage", &"strength", DRIVER_MULTIPLY, 2.0)
attribute_set.get_attribute_base_value(&"health")
attribute_set.get_attribute_current_value(&"mana")  # Base + mods
```gdscript

---

## [ASContainer](resources/ascontainer.md)

**Arquétipo (template) de ator**

```gdscript
container.add_ability(ability)
container.add_effect(initial_effect)
container.add_cue(cue)
container.has_ability(ability)
```gdscript

---

## [ASPackage](resources/aspackage.md)

**Envelope de entrega (effects + cues)**

```gdscript
package.add_effect(effect)
package.add_effect_tag(&"effect.burn")
package.add_cue(cue)
package.add_cue_tag(&"cue.visual")
package.events_on_deliver.append(&"event.hit")
```gdscript

---

## [ASCue (& variants)](resources/ascue.md)

**Feedback audiovisual**

- **ASCue**: Base
- **ASCueAnimation**: Toca AnimationPlayer
- **ASCueAudio**: Toca som
- **ASCueParticles**: Emite partículas

---

## [ASAbilityPhase](resources/asabilityphase.md)

**Fases de execução granular**

```gdscript
phase.phase_duration = 0.2
phase.granted_tags.append(&"state.charging")
phase.effects.append(phase_effect)
phase.transition_trigger = &"animation.hit_frame"
```gdscript

---

## 🎬 Nodes (Componentes de Cena)

## [ASComponent](nodes/ascomponent.md)

**Hub orquestrador do ator**

```gdscript
# Inicialização
asc.apply_container(container)

# Abilities
asc.try_activate_ability_by_tag(&"ability.slash")  # Seguro
asc.can_activate_ability_by_tag(&"ability.fireball")

# Effects
asc.apply_effect_by_tag(&"effect.burn")
asc.apply_package(package)

# Tags
asc.add_tag(&"state.burning")
asc.has_tag(&"state")
asc.get_all_tags()

# Atributos
asc.set_attribute_base_value(&"health", 100.0)
asc.get_attribute_current_value(&"health")

# Multiplayer
asc.capture_snapshot()
asc.apply_snapshot(tick_id)

# Sinais
asc.ability_activated.connect(_on_ability_activated)
asc.tag_added.connect(_on_tag_added)
asc.attribute_changed.connect(_on_attribute_changed)
```gdscript

---

## [ASDelivery](nodes/asdelivery.md)

**Entrega física de payload (projéteis, AoEs)**

```gdscript
delivery.package = package
delivery.set_source_component(asc)
delivery.activate()

# Automático:
# - Colisão → apply_package()
# - Emite evento
```gdscript

---

## ⚙️ RefCounted (Specs e Utils)

## [ASAbilitySpec](refcounted/asabilityspec.md)

**Instância de ability em execução**

```gdscript
spec.get_cooldown_remaining()
spec.is_active()
spec.get_current_phase_index()
```gdscript

---

## [ASEffectSpec](refcounted/aseffectspec.md)

**Instância de effect ativo**

```gdscript
spec.get_duration_remaining()
spec.get_stack_count()
spec.add_stack()
```gdscript

---

## [ASStateCache](refcounted/asstatecache.md)

**Buffer circular (128 ticks) para rollback multiplayer**

Automático—não chamado direto.

---

## [ASStateSnapshot](refcounted/asstatecache.md)

**Persistência de estado (saves/multiplayer)**

```gdscript
asc.snapshot_state = snapshot_resource
asc.capture_snapshot()
asc.apply_snapshot(tick)
```gdscript

---

## [ASTagUtils](refcounted/astagutils.md)

**Utilitários de manipulação histórica de tags**

```gdscript
ASTagUtils.was_tag_added(&"state.stunned", target, 2.0)
ASTagUtils.was_tag_removed(&"ability.attack", target, 1.0)
ASTagUtils.tag_had_count(&"state.burning", target, 5.0)

# Event history
ASTagUtils.event_did_occur(&"event.damage", target, 1.0)
ASTagUtils.event_get_last_magnitude(&"event.damage", target)
ASTagUtils.event_get_last_instigator(&"event.damage", target)
```gdscript

---

## [ASStateUtils](refcounted/asstatecache.md)

**Utilitários de estado**

(Funcionalidades de suporte)

---

## 🎮 Behavior Tree Integration

## BTActionAS_ActivateAbility

```gdscript
# Propriedades no editor
ability_tag: StringName
resolve_mode: BY_TAG / BY_RESOURCE
```gdscript

---

## BTConditionAS_CanActivate

```gdscript
ability_tag: StringName
expect_true: bool  # Esperar true ou false?
```gdscript

---

## BTConditionAS_HasTag

```gdscript
tag: StringName
expect_true: bool
```gdscript

---

## BTConditionAS_EventOccurred

```gdscript
event_tag: StringName
lookback_seconds: float
expect_true: bool
```gdscript

---

## BTActionAS_DispatchEvent

```gdscript
event_tag: StringName
magnitude: float  # Payload
```gdscript

---

## BTActionAS_WaitForEvent

```gdscript
event_tag: StringName
timeout_seconds: float
```gdscript

---

## ✏️ Editor Tools

## ASEditorPlugin

Bootloader (registro de tipos, ícones)

## ASInspectorPlugin

Seletores inteligentes (dropdowns de tags, busca)

## ASTagsPanel

Interface visual para gerenciar tags globais

---

## 📚 Padrões de API

## Nomenclatura Gameplay (Público)

```gdscript
try_activate_ability_by_tag()      # Ativação segura
try_activate_ability_by_resource()
can_activate_ability_by_tag()      # Pré-autorização
is_active()                         # Status boolean
has_tag()                           # Consulta posse
get_attribute_current_value()      # Leitura
request_activate_ability.rpc()     # Intenção rede
cancel_ability()                    # Interrupção
```gdscript

## Nomenclatura Infraestrutura (Privado)

```gdscript
apply_effect_by_resource()          # Força aplicação
add_tag()                           # Mutação baixo nível
unlock_ability()                    # Gestão inventário
set_attribute_base_value()          # Mutação direta
capture_snapshot()                  # Persistência
```gdscript

---

## 🏷️ Tag Types (Constantes)

```gdscript
AbilitySystem.ASTagType.NAME        # 0—Identidade
AbilitySystem.ASTagType.CONDITIONAL # 1—Estado
AbilitySystem.ASTagType.EVENT       # 2—Ocorrência
```gdscript

---

## 🔍 Conversão Rápida: Por Tarefa

## Quero ativar uma ability

```gdscript
# Seguro (recomendado)
asc.try_activate_ability_by_tag(&"ability.fireball")

# Ou verificar antes
if asc.can_activate_ability_by_tag(&"ability.slash"):
    asc.try_activate_ability_by_tag(&"ability.slash")
```gdscript

## Quero aplicar um effect

```gdscript
# Direto (sem validação)
asc.apply_effect_by_tag(&"effect.burn")

# Via package (com entrega)
asc.apply_package(fireball_package)

# Com spec customizado
asc.apply_effect_spec_to_self(custom_spec)
```gdscript

## Quero verificar estado

```gdscript
# Tag
if asc.has_tag(&"state.stunned"):
    cannot_attack()

# Atributo
var hp = asc.get_attribute_current_value(&"health")
if hp <= 0:
    die()
```gdscript

## Quero adicionar tag

```gdscript
asc.add_tag(&"state.burning")
asc.add_tag(&"class.warrior")
```gdscript

## Quero dano contínuo (DoT)

```gdscript
var effect = ASEffect.new()
effect.duration_policy = ASEffect.POLICY_DURATION
effect.duration_magnitude = 5.0
effect.period = 1.0
effect.add_modifier(&"health", ASEffect.OP_ADD, -5.0)
asc.apply_effect_by_resource(effect)
```gdscript

## Quero trigger automático

```gdscript
var ability = ASAbility.new()
ability.add_trigger(&"event.parry_success", ASAbility.TRIGGER_ON_EVENT)
# Ativa automaticamente quando evento dispara
```gdscript

## Quero multiplayer (predição)

```gdscript
# Client
asc.capture_snapshot()
asc.try_activate_ability_by_tag(&"ability.slash")
asc.request_activate_ability.rpc_id(1, &"ability.slash")

# Server
if asc.can_activate_ability_by_tag(tag):
    asc.try_activate_ability_by_tag(tag)
    asc.confirm_ability_activation.rpc(tag)
else:
    asc.apply_snapshot(correct_tick)  # Rollback
```gdscript

---

## 📖 Ordem de Leitura Recomendada

1. **[AbilitySystem](singleton/ability-system.md)** — Começar com registro global
2. **[ASComponent](nodes/ascomponent.md)** — Entender o hub
3. **[ASAbility](resources/asability.md)** → **[ASEffect](resources/aseffect.md)** →
   **[ASContainer](resources/ascontainer.md)** — Montar arquétipos
4. **[ASPackage](resources/aspackage.md)** → **[ASDelivery](nodes/asdelivery.md)** — Entrega física
5. **[ASStateCache](refcounted/asstatecache.md)** → **[ASStateSnapshot](refcounted/asstatecache.md)** — Multiplayer
6. **[Behavior Tree](behavior-tree/)** — Integração IA

---

**v0.1.0 | Godot 4.6+ | Desenvolvido com ❤️ por MachiTwo**
