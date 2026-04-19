---
title: "Tutorial: Primeiro Ataque"
date: "2026-04-18T22:30:00-03:00"
slug: first-attack
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

Passo a passo para criar sua primeira habilidade de combate funcional no **Ability System**.

**Tempo:** ~15 minutos | **Nível:** Iniciante

## Passo 1: Criar o Resource da Habilidade

1. Crie uma pasta `res://combat/abilities/`.
2. Clique com o botão direito → **New Resource → ASAbility**.
3. Salve como `basic_attack.tres`.

## Passo 2: Configurar Tags de Ativação

No inspetor do seu novo resource, procure pela seção **Tags**:

- **Ability Tag:** `&"ability.basic_attack"`
- **Activation Owned Tags:** `[&"state.attacking"]` (Isso impede que outras habilidades usem o personagem enquanto ataca).

## Passo 3: Criar o Efeito de Dano

Habilidades no **Ability System** geralmente causam efeitos (`ASEffect`).

1. Crie um novo **ASEffect** em `res://combat/effects/damage_basic.tres`.
2. Configure os **Modifiers**:
   - **Attribute:** `&"health"`
   - **Operation:** `0 (ADD)`
   - **Magnitude:** `-10.0`

## Passo 4: Vincular o Efeito à Habilidade

Volte ao resource `basic_attack.tres`:

1. Adicione um item ao array **Application Effects**.
2. Arraste o arquivo `damage_basic.tres` para lá.

## Passo 5: Chamar via Código

No seu script do Personagem:

```gdscript
func _input(event):
    if event.is_action_pressed("attack"):
        if asc.try_activate_ability_by_tag(&"ability.basic_attack"):
            print("Ataque iniciado!")
```

## Conclusão

Você acaba de criar o fluxo completo: Entrada → Ativação de Habilidade → Aplicação de Efeito.

---

**Explorar mais:** [Tutorial: Buffs e Debuffs](buffs)
