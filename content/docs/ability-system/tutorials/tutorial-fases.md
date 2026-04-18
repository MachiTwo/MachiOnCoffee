---
title: "Tutorial: Habilidades com Fases (Windup → Execution → Recovery)"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Tutorial: Habilidades com Fases

Aprenda a criar habilidades complexas divididas em fases de execução granular.

**Tempo:** ~15 minutos | **Nível:** Intermediário

## Conceito: Fases

```
Ataque de Espada com 3 Fases:

[Windup]      [Execution]    [Recovery]
[0.3s]        [0.1s]         [0.2s]
Slow tag      Apply damage   Back to normal
```

## Passo 1: Criar ASAbilityPhase

Crie 3 resources de fase:

### Phase 1: Windup

New Resource → **ASAbilityPhase**

Salve como `res://assets/phases/slash_windup.tres`

```
phase_duration: 0.3
granted_tags: [&"state.attacking"]
effects: []
transition_trigger: &"animation.slash_frame_15"
```

### Phase 2: Execution

New Resource → **ASAbilityPhase**

Salve como `res://assets/phases/slash_execution.tres`

```
phase_duration: 0.1
granted_tags: []
effects: (array com 1 elemento)
  [0]: (drag slash_damage.tres)
transition_trigger: &"animation.slash_finished"
```

### Phase 3: Recovery

New Resource → **ASAbilityPhase**

Salve como `res://assets/phases/slash_recovery.tres`

```
phase_duration: 0.2
granted_tags: []
effects: []
transition_trigger: ""
```

## Passo 2: Criar ASAbility com Fases

Modifique `slash.tres`:

```
ability_tag: &"ability.slash"
ability_duration_policy: 1 (DURATION)
cooldown_duration: 1.0
phases: (array com 3 elementos)
  [0]: (drag slash_windup.tres)
  [1]: (drag slash_execution.tres)
  [2]: (drag slash_recovery.tres)
```

## Passo 3: Script para Sincronizar com Animação

```gdscript
extends CharacterBody3D

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

func _ready():
    anim.animation_finished.connect(_on_animation_finished)

func _physics_process(_delta):
    if Input.is_action_just_pressed("ui_accept"):
        if asc.try_activate_ability_by_tag(&"ability.slash"):
            anim.play("slash_attack")
            print("Fase 1: Windup")

func _on_animation_finished(anim_name):
    if anim_name == "slash_attack":
        var spec = asc.get_ability_spec_by_tag(&"ability.slash")
        if spec:
            var phase = spec.get_current_phase_index()
            print("Finalizou fase: %d" % phase)
```

## Passo 4: Entender Transições

Cada fase avança baseado em `transition_trigger`:

```gdscript
# Phase 1 (Windup):
transition_trigger: &"animation.slash_frame_15"
# Avança quando animação atinge frame 15

# Phase 2 (Execution):
transition_trigger: &"animation.slash_finished"
# Avança quando animação termina

# Phase 3 (Recovery):
transition_trigger: ""
# Usa duração (0.2s)
```

Para disparar triggers customizados:

```gdscript
# Na animation callback (frame 15):
func _on_animation_frame_changed():
    if anim.current_animation == "slash_attack":
        if anim.current_animation_position >= 0.15:  # Frame 15
            asc.dispatch_event(&"animation.slash_frame_15")
```

## Passo 5: Testar Fluxo Completo

Script de debug:

```gdscript
func _process(_delta):
    var spec = asc.get_ability_spec_by_tag(&"ability.slash")
    if spec and spec.is_active():
        var phase = spec.get_current_phase_index()
        var duration = spec.get_duration_remaining()
        print("Fase: %d, Duração: %.2f" % [phase, duration])
```

Output esperado:

```
Fase 0, Duração: 0.29  # Windup (0.3s)
Fase 0, Duração: 0.05
Fase 1, Duração: 0.09  # Execution (0.1s)
Fase 2, Duração: 0.18  # Recovery (0.2s)
```

## Caso de Uso: Habilidade Canalizável

Crie spell que cancela se player se mover:

```gdscript
var current_ability_spec = null

func _physics_process(_delta):
    if Input.is_action_just_pressed("ui_accept"):
        if asc.try_activate_ability_by_tag(&"ability.fireball_cast"):
            current_ability_spec = asc.get_ability_spec_by_tag(&"ability.fireball_cast")

    # Se player se mover, cancela casting
    if Input.is_action_pressed("ui_right") or Input.is_action_pressed("ui_left"):
        if current_ability_spec and current_ability_spec.is_active():
            asc.cancel_ability_by_spec(current_ability_spec)
            print("Casting cancelado!")
            current_ability_spec = null
```

## Caso de Uso: Combo Multi-Fase

Crie 3 fases de combo consecutivas:

```gdscript
func _process(_delta):
    var spec = asc.get_ability_spec_by_tag(&"ability.combo")
    if spec and spec.is_active():
        var phase = spec.get_current_phase_index()

        if Input.is_action_just_pressed("ui_accept"):
            # Player pressionou no tempo certo
            # Avanças para próxima fase
            if phase == 0:
                asc.dispatch_event(&"combo.confirmed_phase_1")
            elif phase == 1:
                asc.dispatch_event(&"combo.confirmed_phase_2")
```

## Debugging Fases

```gdscript
func debug_phase_info():
    var spec = asc.get_ability_spec_by_tag(&"ability.slash")
    if spec:
        var phase_idx = spec.get_current_phase_index()
        var phase_resource = spec.get_phase(phase_idx)
        print("Fase: ", phase_resource.granted_tags)
        print("Duração: ", phase_resource.phase_duration)
        print("Trigger: ", phase_resource.transition_trigger)
```

## Conceitos Aprendidos

✅ Criar ASAbilityPhase ✅ Sequenciar múltiplas fases ✅ Sincronizar com animação ✅ Disparar triggers customizados ✅
Debugar transições

---

**Próximo Tutorial:** [Sistema de Buff/Debuff](tutorial-buffs.md)
