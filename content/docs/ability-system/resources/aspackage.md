---
title: "ASPackage"
date: "2026-04-18T12:00:00-03:00"
type: docs
---


**Badge:** `Resource`

## Descrição Breve

Container reutilizável para effects e cues que pode ser entregue.

## Descrição Completa

`ASPackage` é um "envelope de dados" que agrupa múltiplos `ASEffect`s e `ASCue`s para transporte e entrega. Usado primariamente pelo `ASDelivery` (projéteis, AoEs) para aplicar um payload complexo (ex: explosão de fireball = dano + queimadura + visual).

Permite:

- **Efeitos diretos**: `add_effect(effect_resource)`
- **Efeitos por tag**: `add_effect_tag(tag)` — resolvidos no alvo
- **Cues diretos**: `add_cue(cue_resource)`
- **Cues por tag**: `add_cue_tag(tag)` — resolvidas no alvo
- **Eventos**: Eventos disparados ao entregar

## Herança

```gdscript
Resource
 └─ ASPackage
```gdscript

## Propriedades

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `package_tag` | StringName | `&""` | Tag identificadora (tipo NAME) |
| `effects_resources` | ASEffect[] | `[]` | Effects diretos no package |
| `effects_tags` | StringName[] | `[]` | Tags de effects (resolvidos no alvo) |
| `cues_resources` | ASCue[] | `[]` | Cues diretos no package |
| `cues_tags` | StringName[] | `[]` | Tags de cues (resolvidas no alvo) |
| `events_on_deliver` | StringName[] | `[]` | Eventos disparados ao entregar |

## Métodos Públicos

## Gerenciamento de Effects Diretos

## `add_effect(effect: ASEffect) → void`

Adiciona effect direto (resource) ao package.

## `remove_effect(effect: ASEffect) → void`

Remove effect direto.

## `clear_effects() → void`

Remove todos os effects diretos.

## Gerenciamento de Tags de Effects

## `add_effect_tag(tag: StringName) → void`

Adiciona tag de effect (será resolvido pelo alvo).

## `remove_effect_tag(tag: StringName) → void`

Remove tag de effect.

## Gerenciamento de Cues Diretos

## `add_cue(cue: ASCue) → void`

Adiciona cue direto (resource) ao package.

## `remove_cue(cue: ASCue) → void`

Remove cue direto.

## Gerenciamento de Tags de Cues

## `add_cue_tag(tag: StringName) → void`

Adiciona tag de cue (será resolvida pelo alvo).

## `remove_cue_tag(tag: StringName) → void`

Remove tag de cue.

## `clear_cues() → void`

Remove todas as cues.

## Casos de Uso

## Payload de Fireball (Explosão)

```gdscript
var fireball_package = ASPackage.new()
fireball_package.package_tag = &"package.fireball"

# Effects diretos
fireball_package.add_effect(fire_damage_effect)      # -50 health
fireball_package.add_effect(fire_dot_effect)         # Burning DoT
fireball_package.add_effect(knockback_effect)        # Impacto

# Cues diretos
fireball_package.add_cue(explosion_animation_cue)
fireball_package.add_cue(fire_sound_cue)
fireball_package.add_cue(particles_cue)

# Evento ao entregar
fireball_package.events_on_deliver.append(&"event.fireball_hit")
```gdscript

## Entrega via Projectile

```gdscript
func _on_fireball_cast():
    var projectile = fireball_projectile_scene.instantiate()
    var delivery = projectile.get_node("ASDelivery")

    # Atribuir package
    delivery.package = fireball_package

    # Configurar source (quem lançou)
    delivery.set_source_component(asc)

    # Ativar entrega (colisão aplicará o package)
    delivery.activate()

    add_child(projectile)
```gdscript

## Payload Mixto (Effects + Tags)

```gdscript
var poison_trap_package = ASPackage.new()
poison_trap_package.package_tag = &"package.poison_trap"

# Effect direto
poison_trap_package.add_effect(poison_effect)  # DoT específico

# Efeitos por tag (resolvidos no alvo)
poison_trap_package.add_effect_tag(&"effect.poison_resistance_down")

# Cue por tag (o alvo fornece)
poison_trap_package.add_cue_tag(&"cue.poison_particle")

# Evento
poison_trap_package.events_on_deliver.append(&"event.poison_applied")
```gdscript

## Aura Passiva (Area2D + Delivery)

```gdscript
# Uma aura aplicada a aliados dentro de um círculo
var aura_package = ASPackage.new()
aura_package.package_tag = &"package.healing_aura"

# Cura contínua
aura_package.add_effect(healing_over_time_effect)

# Tag que alvo deve ter (validação)
aura_package.effects_tags.append(&"effect.ally_only")

# Cue
aura_package.add_cue(aura_glow_cue)

# ASDelivery na aura respawna a cada 0.5s:
func _on_aura_tick():
    var targets = aura_area.get_overlapping_bodies()
    for target in targets:
        var asc = AbilitySystem.resolve_component(target)
        if asc:
            asc.apply_package(aura_package)
```gdscript

## Payload Condicional (Múltiplos Effects)

```gdscript
# Magia que muda baseado no alvo
var spell_package = ASPackage.new()
spell_package.package_tag = &"package.adaptive_spell"

# Dano base
spell_package.add_effect(base_damage_effect)

# Se alvo é inimigo, aplicar débuff
spell_package.add_effect_tag(&"effect.enemy_debuff")

# Se alvo é aliado, aplicar buff
spell_package.add_effect_tag(&"effect.ally_buff")

# Efeito visual genérico
spell_package.add_cue(spell_visual_cue)

# Evento genérico
spell_package.events_on_deliver.append(&"event.spell_cast")
```gdscript

## Integração com ASComponent.apply_package()

```gdscript
# Direct application (não via projectile)
var target_asc = target.get_node("ASComponent")
target_asc.apply_package(fireball_package, level=2.0)

# apply_package valida tags do package:
# - Confere activation_required_all_tags / blocked_any_tags
# - Emite sinais: "effect_applied", "effect_failed"
# - Retorna void (sempre tenta aplicar)
```gdscript

## Diferença: Apply vs Delivery

## `apply_package()` (Direct)

```gdscript
asc.apply_package(package)  # Aplica direto, sem física/delay
```gdscript

Usado para:

- Effects imediatos
- Habilidades de self-cast
- AoE instantânea

## `ASDelivery` (Via Projectile/Trigger)

```gdscript
delivery.package = package  # Atribuir
delivery.activate()         # Disparar quando colidir
```gdscript

Usado para:

- Projéteis com viagem
- AoE com rastreamento
- Armadilhas passivas

## Referências Relacionadas

- [ASEffect](aseffect.md) — Effects no package
- [ASCue](ascue.md) — Cues no package
- [ASDelivery](../nodes/asdelivery.md) — Entrega física
- [ASComponent](../nodes/ascomponent.md) — Aplicação direta

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
