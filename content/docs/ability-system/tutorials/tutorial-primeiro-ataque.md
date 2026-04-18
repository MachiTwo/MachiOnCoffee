---
title: "Tutorial: Criar Seu Primeiro Ataque"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

Neste tutorial, você criará uma habilidade simples de ataque (slash) do zero até executá-la.

**Tempo:** ~10 minutos | **Nível:** Iniciante

## Passo 1: Registrar Tags Globais

Abra **Project Settings → Ability System** (painel do editor).

Click **[Add Tag]** e crie:

````gdscript
1. ability.slash (tipo: NAME)
2. state.attacking (tipo: CONDITIONAL)
3. event.hit (tipo: EVENT)
```gdscript

## Passo 2: Criar AttributeSet

No FileSystem, clique direito → **New Resource → ASAttributeSet**

Salve como `res://assets/attributes/base_attributes.tres`

No Inspector:

```gdscript
attributes: (clique "New Dictionary")
  health: 100.0
  mana: 50.0
  strength: 10.0
```gdscript

## Passo 3: Criar ASAbility

New Resource → **ASAbility**

Salve como `res://assets/abilities/slash.tres`

Configure:

```gdscript
ability_tag: &"ability.slash"
ability_duration_policy: 0 (INSTANT)
cooldown_duration: 0.5
costs: []
requirements: []
activation_required_all_tags: []
activation_owned_tags: [&"state.attacking"]
effects: []
```gdscript

## Passo 4: Criar ASEffect

New Resource → **ASEffect**

Salve como `res://assets/effects/slash_damage.tres`

Configure:

```gdscript
effect_tag: &"effect.slash_damage"
duration_policy: 0 (INSTANT)
target_type: 1 (OTHERS)
granted_tags: []
removed_tags: []
modifiers: (clique "New Array Element")
  modifier[0]:
    attribute: &"health"
    operation: 0 (ADD)
    magnitude: -20.0
```gdscript

## Passo 5: Criar ASContainer

New Resource → **ASContainer**

Salve como `res://assets/archetypes/player.tres`

Configure:

```gdscript
attribute_set: (drag base_attributes.tres)
initial_abilities:
  - (drag slash.tres)
initial_effects: []
initial_cues: []
```gdscript

## Passo 6: Criar Cena do Player

Nova Scene:

```gdscript
Player (CharacterBody3D)
├─ AbilityComponent (ASComponent)
└─ MeshInstance3D
```gdscript

No **AbilityComponent**:

```gdscript
container: (drag player.tres)
```gdscript

## Passo 7: Script do Player

```gdscript
extends CharacterBody3D

@onready var ability_component = $AbilityComponent

func _physics_process(_delta):
    if Input.is_action_just_pressed("ui_accept"):
        # Ativar ataque
        if ability_component.try_activate_ability_by_tag(&"ability.slash"):
            print("Ataque ativado!")
        else:
            print("Não pode atacar agora (cooldown?)")
```gdscript

## Passo 8: Testar

Play a cena. Pressione SPACE.

Você verá "Ataque ativado!" no console.

Aguarde 0.5s (cooldown), pressione novamente.

## Próximas Adições

## Adicionar Dano Real

Modifique o script:

```gdscript
func _physics_process(_delta):
    if Input.is_action_just_pressed("ui_accept"):
        if ability_component.try_activate_ability_by_tag(&"ability.slash"):
            # Aplicar dano ao inimigo
            if has_node("../Enemy"):
                var enemy = get_node("../Enemy")
                var enemy_asc = AbilitySystem.resolve_component(enemy)
                ability_component.apply_effect_by_tag(&"effect.slash_damage", enemy_asc)
                print("Dano aplicado!")
```gdscript

## Adicionar Animação

Crie AnimationPlayer no player:

```gdscript
@onready var anim = $AnimationPlayer

func _physics_process(_delta):
    if Input.is_action_just_pressed("ui_accept"):
        if ability_component.try_activate_ability_by_tag(&"ability.slash"):
            anim.play("slash")
```gdscript

## Adicionar Cooldown Visual

```gdscript
@onready var label = $CooldownLabel

func _process(_delta):
    var spec = ability_component.get_ability_spec_by_tag(&"ability.slash")
    if spec and spec.is_on_cooldown():
        var remaining = spec.get_cooldown_remaining()
        label.text = "%.1f" % remaining
    else:
        label.text = ""
```gdscript

## Troubleshooting

**Erro: "ability.slash" não registrada**

- Verifique se você registrou a tag no painel do editor
- Caminho: Project Settings → Ability System

**Ability não ativa**

- Verifique cooldown: `spec.get_cooldown_remaining() > 0`
- Verifique custos: `asc.get_attribute_current_value(&"mana") >= 20`

**Dano não aplicado**

- Confirm que o enemy tem ASComponent
- Verifique que enemy_asc não é null

## Conceitos Aprendidos

✅ Criar e registrar tags ✅ Criar ASAbility, ASEffect, ASContainer ✅ Montar cena com ASComponent ✅ Ativar ability via
script ✅ Aplicar efeitos ✅ Verificar cooldown

---

**Próximo Tutorial:** [Combate Avançado com Fases](tutorial-fases.md)
````
