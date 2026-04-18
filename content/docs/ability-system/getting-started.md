---
title: "Getting Started"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Getting Started com Ability System

Guia passo-a-passo para começar a usar o framework.

## 1️⃣ Registre suas Tags

Todas as tags devem ser registradas globalmente no `AbilitySystem` singleton.

### Abra o Painel de Tags

- **GDExtension**: Procure pela aba **Ability System Tags** no **Painel Inferior** (ao lado de Output)
- **Ou**: Acesse `AbilitySystem` singleton → método `register_tag()`

### Registre o Vocabulário

```gdscript
func _ready():
    # Abilities (tipo NAME)
    AbilitySystem.register_tag(&"ability.slash", AbilitySystem.ASTagType.NAME)
    AbilitySystem.register_tag(&"ability.fireball", AbilitySystem.ASTagType.NAME)

    # States (tipo CONDITIONAL)
    AbilitySystem.register_tag(&"state.stunned", AbilitySystem.ASTagType.CONDITIONAL)
    AbilitySystem.register_tag(&"state.burning", AbilitySystem.ASTagType.CONDITIONAL)

    # Events (tipo EVENT)
    AbilitySystem.register_tag(&"event.damage", AbilitySystem.ASTagType.EVENT)
    AbilitySystem.register_tag(&"event.hit", AbilitySystem.ASTagType.EVENT)
```

## 2️⃣ Crie um AttributeSet

Define os stats do seu ator (HP, Mana, Força, etc).

```gdscript
# Arquivo: WarriorAttributeSet.tres (no editor ou código)
var attribute_set = ASAttributeSet.new()

# Health (0–100, começa 100)
var health = ASAttribute.new()
health.attribute_name = "Health"
health.min_value = 0.0
health.max_value = 100.0
health.base_value = 100.0
attribute_set.add_attribute(health)

# Mana (0–50)
var mana = ASAttribute.new()
mana.attribute_name = "Mana"
mana.min_value = 0.0
mana.max_value = 50.0
mana.base_value = 50.0
attribute_set.add_attribute(mana)

# Strength (0–100)
var strength = ASAttribute.new()
strength.attribute_name = "Strength"
strength.min_value = 0.0
strength.max_value = 100.0
strength.base_value = 10.0
attribute_set.add_attribute(strength)
```

## 3️⃣ Crie uma Ability

Define uma ação (com custos, cooldown, efeitos).

```gdscript
# Arquivo: AbilitySlash.tres
var slash = ASAbility.new()
slash.ability_name = "Slash"
slash.ability_tag = &"ability.slash"

# Instant—executa uma vez
slash.ability_duration_policy = ASAbility.POLICY_INSTANT

# Cooldown 1s
slash.cooldown_duration = 1.0

# Sem custo (melee)

# Não pode atacar se atordoado
slash.activation_blocked_any_tags.append(&"state.stunned")

# Tag de "atacando" enquanto ativa
slash.activation_owned_tags.append(&"state.attacking")

# Aplica efeito de dano
slash.effects.append(damage_effect)
```

## 4️⃣ Crie um Effect

Define modificações de atributo e tags.

```gdscript
# Arquivo: EffectSlashDamage.tres
var damage_effect = ASEffect.new()
damage_effect.effect_name = "Slash Damage"
damage_effect.effect_tag = &"effect.slash_damage"

# Instant
damage_effect.duration_policy = ASEffect.POLICY_INSTANT

# -30 health
damage_effect.add_modifier(&"health", ASEffect.OP_ADD, -30.0)
```

## 5️⃣ Crie um Container (Archetype)

Agrupa AttributeSet, Abilities, e Effects iniciais.

```gdscript
# Arquivo: WarriorContainer.tres
var container = ASContainer.new()

# Assign attribute set
container.attribute_set = warrior_attribute_set

# Add abilities to catalog
container.add_ability(ability_slash)
container.add_ability(ability_fireball)

# Add initial effects (passive auras)
# container.add_effect(passive_effect)
```

## 6️⃣ Adicione ASComponent ao Character

Adicione o Node `ASComponent` como child do seu `CharacterBody2D`/`CharacterBody3D`.

```gdscript
# Cena do personagem
Player (CharacterBody2D)
  └─ ASComponent
```

## 7️⃣ Carregue o Container na Inicialização

```gdscript
@onready var asc = $ASComponent

func _ready():
    # Aplica container—carrega abilities, effects, attribute set
    asc.apply_container(warrior_container)

    # Conecta sinais
    asc.ability_activated.connect(_on_ability_activated)
    asc.tag_added.connect(_on_tag_added)
```

## 8️⃣ Ative Abilities via Input

```gdscript
func _physics_process(delta):
    # Movimentação
    var direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = direction * speed

    # Input de ability
    if Input.is_action_just_pressed("ability_slash"):
        if asc.try_activate_ability_by_tag(&"ability.slash"):
            print("Slash ativado!")
        else:
            print("Falhou—em cooldown?")

    move_and_slide()
```

## 9️⃣ Reaja a Mudanças de Estado

```gdscript
func _on_ability_activated(tag: StringName):
    print("Ability ativada: ", tag)
    play_animation_for_ability(tag)

func _on_tag_added(tag: StringName):
    if tag == &"state.burning":
        $Sprite.modulate = Color.RED
    elif tag == &"state.frozen":
        $Sprite.modulate = Color.CYAN

func _on_attribute_changed(attribute: StringName, new_value: float):
    if attribute == &"health":
        update_health_bar(new_value)
```

---

## 📋 Checklist de Setup Completo

- [ ] Tags registradas no `AbilitySystem`
- [ ] `AttributeSet` criado (`.tres` ou código)
- [ ] `ASAbility` criado com custos/cooldown
- [ ] `ASEffect` criado com modificadores
- [ ] `ASContainer` criado e tudo conectado
- [ ] `ASComponent` adicionado ao Character
- [ ] `apply_container()` chamado em `_ready()`
- [ ] Sinais conectados para feedback
- [ ] Input handling implementado
- [ ] Testado—consegue ativar abilities?

---

## ⚡ Referência Rápida de Métodos

### Ativação (Gameplay)

```gdscript
asc.try_activate_ability_by_tag(&"ability.slash")    # Seguro
asc.can_activate_ability_by_tag(&"ability.fireball")  # Verificar
```

### Estado

```gdscript
asc.has_tag(&"state.stunned")
asc.add_tag(&"state.burning")
asc.remove_tag(&"state.burning")
```

### Atributos

```gdscript
asc.set_attribute_base_value(&"health", 100.0)
asc.get_attribute_current_value(&"health")
```

### Effects

```gdscript
asc.apply_effect_by_tag(&"effect.burn")
asc.apply_package(fireball_package)
```

---

## 🎬 Próximos Passos

1. **[Documentação Completa](./reference.md)** — API detalhada
2. **[ASAbility](resources/asability.md)** — Custos, triggers, fases
3. **[ASEffect](resources/aseffect.md)** — DoT, buffs, debuffs
4. **[ASDelivery](nodes/asdelivery.md)** — Projéteis e AoEs
5. **[Multiplayer](refcounted/asstatecache.md)** — Predição e rollback

---

**v0.1.0 | Godot 4.6+ | Desenvolvido com ❤️ por MachiTwo**
