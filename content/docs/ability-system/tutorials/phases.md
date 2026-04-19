---
title: "Tutorial: Fases de Habilidade"
date: "2026-04-18T22:30:00-03:00"
slug: phases
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - tutorial
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

Aprenda a criar habilidades complexas com múltiplas fases (Casting, Active, Recovery) no **Ability System**.

**Tempo:** ~15 minutos | **Nível:** Avançado

## O que são Fases?

Fases permitem dividir uma habilidade em etapas temporais, cada uma com seu próprio comportamento:

1. **Casting:** Tempo de preparação (pode ser interrompido).
2. **Active:** O momento em que o efeito principal ocorre.
3. **Recovery:** Tempo de "recuperação" após o uso.

## Passo 1: Definir as Fases no Resource

No seu `ASAbility`, você pode configurar o array `phases`.

```gdscript
# Exemplo de configuração de fases para um 'Super Ataque'
phases = [
    {
        "name": &"prepare",
        "duration": 1.0,
        "is_interruptible": true,
        "tags_granted": [&"state.casting"]
    },
    {
        "name": &"execute",
        "duration": 0.5,
        "is_interruptible": false,
        "tags_granted": [&"state.immune"]
    },
    {
        "name": &"recover",
        "duration": 0.8,
        "is_interruptible": true,
        "tags_granted": [&"state.vulnerable"]
    }
]
```

## Passo 2: Escutar Sinais de Mudança de Fase

No seu script de personagem ou no script da habilidade, você pode reagir às mudanças:

```gdscript
func _ready():
    asc.ability_phase_changed.connect(_on_ability_phase_changed)

func _on_ability_phase_changed(ability_spec, old_phase, new_phase):
    print("Habilidade %s mudou de %s para %s" % [ability_spec.get_ability().resource_name, old_phase, new_phase])

    match new_phase:
        &"prepare":
            play_animation("cast_start")
            spawn_particles("charge_up")
        &"execute":
            play_animation("attack_swing")
            apply_damage_area()
        &"recover":
            play_animation("cast_end")
```

## Passo 3: Interrupção de Fases

Se uma fase for marcada como `is_interruptible`, ela pode ser cancelada por efeitos externos ou chamadas manuais:

```gdscript
func take_hit():
    # Se estiver no meio de um 'cast' interrompível, cancela a habilidade
    if asc.is_any_ability_in_phase(&"prepare"):
        asc.cancel_all_abilities_with_tag(&"state.casting")
        play_animation("stagger")
```

## Passo 4: Transições Visuais (Cues)

Você pode vincular `ASCue` a fases específicas para automação visual:

```gdscript
# No inspetor do ASAbility
# phase_cues = {
# "prepare": [res://vfx/charge.tres],
# "execute": [res://vfx/explosion.tres]
# }
```

## Conclusão

O sistema de fases é a base para criar mecânicas de "commit" e risco/recompensa em jogos de ação e RPG.

---

**Próximo:** [Tutorial: Primeiro Ataque](first-attack)
