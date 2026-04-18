---
title: "ASCue"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASCue (Base Class)

**Badge:** `Resource`

## Descrição Breve

Resource base para sincronização de eventos audiovisuais.

## Descrição Completa

`ASCue` é a classe base para resources que lidam com ativação de eventos e sincronização, como tocar animações ou sons em resposta a effects e abilities.

Para a maioria dos casos, use:

- **[ASCueAnimation](ascueanimation.md)** — Sincronizar animações
- **[ASCueAudio](ascueaudio.md)** — Sincronizar áudio

Você pode estender a classe base em GDScript para comportamento completamente customizado:

```gdscript
extends ASCue

func _on_execute(spec: ASCueSpec):
    print("Custom cue triggered!")
```

## Herança

```
Resource
 └─ ASCue (Base)
     ├─ ASCueAnimation
     ├─ ASCueAudio
     └─ (Custom subclasses)
```

## Propriedades

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `cue_name` | String | `""` | Nome único |
| `cue_tag` | StringName | `&""` | Tag identificadora (tipo NAME) |
| `event_type` | int (enum) | `ON_EXECUTE` | Quando disparar (ON_EXECUTE / ON_ACTIVE / ON_REMOVE) |
| `node_name` | StringName | `&""` | Nome do node registrado em ASComponent (opcional) |
| `activation_required_all_tags` | StringName[] | `[]` | Owner DEVE ter TODAS (AND) |
| `activation_required_any_tags` | StringName[] | `[]` | Owner DEVE ter QUALQUER UMA (OR) |
| `activation_blocked_any_tags` | StringName[] | `[]` | Falha se tiver QUALQUER UMA |
| `activation_blocked_all_tags` | StringName[] | `[]` | Falha se tiver TODAS |

## Constantes (Enums)

### CueEventType

```gdscript
enum CueEventType {
    ON_EXECUTE = 0,  # Disparado para effects instant (hit, explosion)
    ON_ACTIVE = 1,   # Disparado quando effect/ability ativa
    ON_REMOVE = 2    # Disparado quando effect/ability termina
}
```

## Callbacks Virtuais

### `_on_execute(spec: ASCueSpec) → void` (virtual)

Chamado para effects instant. Use para hit impacts, explosões.

### `_on_active(spec: ASCueSpec) → void` (virtual)

Chamado quando effect/ability ativa. Use para buffs, auras.

### `_on_remove(spec: ASCueSpec) → void` (virtual)

Chamado quando effect/ability termina. Use para cleanup.

## Casos de Uso (Custom Subclass)

### Custom Particle Cue

```gdscript
extends ASCue

class_name CustomParticleCue

var particle_scene: PackedScene

func _on_execute(spec: ASCueSpec):
    var particles = particle_scene.instantiate()
    var target_node = get_target_node(spec)
    target_node.add_child(particles)
    particles.emitting = true

    await particles.tree_exiting
    particles.queue_free()

func get_target_node(spec: ASCueSpec) -> Node:
    var asc = spec.get_target_component()
    if node_name:
        return asc.get_node(node_name)
    return asc
```

### Custom Shockwave Cue

```gdscript
extends ASCue

func _on_execute(spec: ASCueSpec):
    var target = spec.get_target_component()
    var level = spec.get_level()

    # Criar shockwave visual
    var shockwave = create_shockwave_visual()
    target.add_child(shockwave)

    # Escalar com level
    shockwave.scale = Vector3.ONE * level

    await shockwave.finish()
    shockwave.queue_free()
```

## Referências Relacionadas

- [ASCueAnimation](ascueanimation.md) — Especialização para animações
- [ASCueAudio](ascueaudio.md) — Especialização para áudio
- [ASCueSpec](../refcounted/ascuespec.md) — Instância em execução
- [ASComponent](../nodes/ascomponent.md) — Dispara cues
- [ASAbility](asability.md) — Contém cues
- [ASEffect](aseffect.md) — Contém cues

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
