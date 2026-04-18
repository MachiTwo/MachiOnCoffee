---
title: "ASCueAnimation"
date: "2026-04-18T12:00:00-03:00"
type: docs
---


**Badge:** `Resource` • `ASCue`

## Descrição Breve

Cue especializado para reproduzir animações durante execução de abilities.

## Descrição Completa

`ASCueAnimation` é um feedback visual que executa uma animação em resposta a eventos do Ability System. Integra-se automaticamente com `AnimationPlayer`, `AnimatedSprite2D` e `AnimatedSprite3D` registrados no `ASComponent`.

Crie um resource `.tres` do tipo `ASCueAnimation`, configure a propriedade `animation_name`, e adicione à lista `cues` de qualquer `ASAbility` ou `ASEffect`. Quando a ability é ativada ou o effect aplicado, a animação toca automaticamente no nó alvo.

**Fluxo de Execução:**

1. Ability/Effect ativa cue trigger (ON_EXECUTE, ON_ACTIVE, etc.)
2. ASComponent cria `ASCueSpec` com contexto
3. ASCueAnimation procura nó com alias `node_name` no registry
4. AnimationPlayer.play() dispara com a `animation_name` configurada

## Herança

```gdscript
Resource
 └─ ASCue
     └─ ASCueAnimation
```gdscript

## Propriedades

| Propriedade       | Tipo    | Descrição                                                                          |
| --------------- | ------- | ---------------------------------------------------------------------------------- |
| `animation_name` | String  | Nome da animação a reproduzir no AnimationPlayer                                  |
| `cue_tag`        | StringName | Identificador da cue (herdado de ASCue) — deve ser NAME type                      |
| `node_name`      | StringName | Alias do nó alvo no registry do ASComponent (herdado de ASCue)                     |
| `event_type`     | int      | Trigger: ON_EXECUTE (0), ON_ACTIVE (1), ON_REMOVE (2) (herdado de ASCue)          |

## Métodos

## Getters

## `get_animation_name() → String` (const)

Retorna nome da animação configurada.

## Setters

## `set_animation_name(name: String) → void`

Define a animação a ser tocada. Deve corresponder a uma animação existente no AnimationPlayer alvo.

## Comportamento Automático

**Resolução de Nó Alvo:**

Se `node_name` vazio, ASCueAnimation tenta nesta ordem:

1. AnimationPlayer direto no owner
2. Primeiro child AnimationPlayer
3. Primeiro AnimatedSprite2D/3D

**Segurança:**

- Se nó não encontrado: nenhum erro (falha silenciosa)
- Se animação não existe: Godot loga aviso mas continua
- Se AnimationPlayer já tocando: interrompe e começa nova

## Casos de Uso

## Ability com Animação de Ataque

```gdscript
# attack_animation.tres (ASCueAnimation)
# cue_tag: "cue.attack_animation"
# animation_name: "attack"
# event_type: ON_EXECUTE

# Na ASAbility:
ability.cues.append(attack_animation_resource)
# Quando ativa ability → toca "attack" automaticamente
```gdscript

## Multi-Fase com Animações Diferentes

```gdscript
# Fase 1: Windup (charging animation)
phase1.effects.append(charging_cue)  # toca "charge" no ON_ACTIVE

# Fase 2: Execution (impact animation)
phase2.effects.append(impact_cue)  # toca "impact" no ON_EXECUTE

# Fase 3: Recovery (recovery animation)
phase3.effects.append(recovery_cue)  # toca "recover" no ON_ACTIVE
```gdscript

## Cue Condicional por Node Path

```gdscript
# Para NPC com AnimationPlayer em caminho específico
cue_anim.node_name = &"Skeleton3D/AnimationPlayer"
cue_anim.animation_name = "death"
cue_anim.event_type = ASCue.ON_REMOVE  # Toca ao morrer
```gdscript

## Cue Trigger no Effect

```gdscript
# Efeito que concede animação de estado
var burn_effect = ASEffect.new()
burn_effect.granted_tags.append(&"state.burning")
burn_effect.cues.append(burn_loop_animation)
# Enquanto "state.burning" ativo → animação loop reproduz

# Quando state removido → ON_REMOVE dispara cleanup animation
```gdscript

## Performance

**Leve:** Cues são altamente otimizadas—nenhuma alocação por frame. AnimationPlayer cuida do blending nativo.

**Melhor Prática:** Reuse a mesma `ASCueAnimation` resource em múltiplas abilities se a animação for idêntica.

```gdscript
# ✅ Compartilhado
var punch_animation = ASCueAnimation.new()
punch_animation.animation_name = "punch"
ability1.cues.append(punch_animation)
ability2.cues.append(punch_animation)  # Mesmo resource

# ❌ Overhead desnecessário
ability1.cues.append(punch_animation.duplicate())
ability2.cues.append(punch_animation.duplicate())
```gdscript

## Integração com ASComponent

```gdscript
# ASComponent resolve automaticamente
asc.try_activate_ability_by_tag(&"ability.slash")
# → Ability dispara cue trigger
# → ASCueAnimation busca AnimationPlayer automaticamente
# → Toca "slash_animation"
```gdscript

Sinais relacionados:

```gdscript
asc.ability_activated.connect(func(spec):
    # Cues já foram disparadas internamente
    print("Ability ativada - animação tocando agora")
)
```gdscript

## Referências Relacionadas

- [ASCue](ascue.md) — Classe base de feedback
- [ASComponent](../nodes/ascomponent.md) — Orquestra cues
- [ASAbility](asability.md) — Define cues na ability
- [ASEffect](aseffect.md) — Effects podem disparar cues

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
