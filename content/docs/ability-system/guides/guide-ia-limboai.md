---
title: "Guia: Integração com LimboAI (Behavior Trees)"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Integração com LimboAI (Behavior Trees)

Controle o Ability System inteiramente via Behavior Trees.

## Arquitetura

```
BehaviorTree
├─ Selector (decisão)
│  ├─ Sequence (combo)
│  │  ├─ Condition: CanActivate
│  │  └─ Action: ActivateAbility
│  └─ Sequence (fallback)
│     └─ Action: Move
```

## Passo 1: Criar Behavior Tree Simples

No editor, crie uma cena com **LimboAIPlayer**.

Crie BT:

```
Root: Selector
├─ Sequence: "Attack"
│  ├─ Condition: BTConditionAS_CanActivate (ability.slash)
│  ├─ Action: BTActionAS_ActivateAbility (ability.slash)
│  └─ Action: Wait (0.5s)
└─ Action: Move Towards Target
```

## Passo 2: Configurar Nós BT

**BTConditionAS_CanActivate:**

```
ability_tag: &"ability.slash"
asc_node_path: (vazio para auto-resolve)
```

**BTActionAS_ActivateAbility:**

```
ability_tag: &"ability.slash"
activation_level: 1.0
asc_node_path: (vazio)
```

## Passo 3: Padrão Decisional Avançado

```
Selector (escolhe primeira opção)
├─ Sequence: "Critical Health"
│  ├─ Condition: health < 25%
│  ├─ Condition: CanActivate (ability.heal)
│  └─ Action: ActivateAbility (ability.heal)
│
├─ Sequence: "High Energy"
│  ├─ Condition: energy > 80%
│  ├─ Condition: CanActivate (ability.ultimate)
│  └─ Action: ActivateAbility (ability.ultimate)
│
├─ Sequence: "Standard Attack"
│  ├─ Condition: CanActivate (ability.slash)
│  └─ Action: ActivateAbility (ability.slash)
│
└─ Action: Idle
```

## Passo 4: Event-Driven Behavior

Dispara evento → BT reage:

```
Sequence:
├─ Action: DispatchEvent (event.player_hit)
├─ Action: WaitForEvent (event.player_hit_back)
│  time_window: 1.0
└─ Action: Counter Attack
```

Script para sincronizar:

```gdscript
func _on_player_hit(damage):
    asc.dispatch_event(&"event.player_hit")
    # BT aguarda "player_hit_back" por até 1s
    # Se receber, executa contra-ataque
```

## Passo 5: Combo Tree

```
Sequence: "Combo Chain"
├─ Action: ActivateAbility (combo.1)
├─ Action: WaitForEvent (combo.1_finished, timeout: 2.0)
├─ Action: ActivateAbility (combo.2)
├─ Action: WaitForEvent (combo.2_finished, timeout: 2.0)
└─ Action: ActivateAbility (combo.3_finisher)
```

Se qualquer passo falha (timeout), sequence falha.

## Passo 6: Tag-Based Decision Tree

```
Selector:
├─ Sequence: "Is Burning"
│  ├─ Condition: HasTag (state.burning)
│  ├─ Action: DispatchEvent (event.take_water)
│  └─ Action: Move To Water Source
│
├─ Sequence: "Is Frozen"
│  ├─ Condition: HasTag (state.frozen)
│  ├─ Action: DispatchEvent (event.thaw)
│  └─ Action: Move To Heat Source
│
└─ Action: Continue Normal Behavior
```

## Passo 7: Parallel Tasks (Simultâneos)

```
Parallel:
├─ Action: MoveWhileAttacking
├─ Sequence:
│  ├─ WaitForEvent (enemy_near)
│  └─ ActivateAbility (ability.slash)
```

Ambos rodam simultaneamente.

## Caso de Uso: Boss Multi-Fase

```
Root: Sequence
├─ Action: Initialize (phase = 1)
├─ Sequence: "Phase 1"
│  ├─ Condition: HasTag (boss.phase_1)
│  ├─ Loop:
│  │  └─ RandomSelector:
│  │     ├─ ActivateAbility (boss.melee)
│  │     ├─ ActivateAbility (boss.ranged)
│  │     └─ Dodge
│  └─ Condition: health < 66%
│
├─ Action: DispatchEvent (phase_2)
│
├─ Sequence: "Phase 2"
│  ├─ Condition: HasTag (boss.phase_2)
│  └─ Loop:
│     └─ RandomSelector:
│        ├─ ActivateAbility (boss.aoe)
│        ├─ ActivateAbility (boss.summon)
│        └─ Defensive Stance
│
└─ Action: Die (when health == 0)
```

## Passo 8: Custom BT Action

Se precisa lógica customizada:

```gdscript
class_name BTActionCustomAttack
extends BTAction

@export var ability_tag: StringName = &"ability.slash"
@export var position_offset: Vector3 = Vector3(2, 0, 0)

func _tick(agent, blackboard):
    var asc = AbilitySystem.resolve_component(agent)

    if asc.can_activate_ability_by_tag(ability_tag):
        # Aplicar lógica customizada
        var target = blackboard.get("target")
        if target and agent.global_position.distance_to(target.global_position) < 3.0:
            asc.try_activate_ability_by_tag(ability_tag)
            return BT.SUCCESS
        else:
            return BT.FAILURE
    else:
        return BT.FAILURE
```

## Debugging BT

Enable debug no LimboAI:

```gdscript
# No script do agent:
func _ready():
    limbo_ai_player.debug_enabled = true
```

Output:

```
[BTSelector] → trying option 0
  [BTConditionAS_CanActivate] slash → SUCCESS
  [BTActionAS_ActivateAbility] slash → SUCCESS
  [BTActionWait] 0.5s → RUNNING
```

## Performance

**Vantagem:** BTs escalam bem com complexidade.

**Desvantagem:** Overhead vs script puro.

Para centenas de inimigos, use script + eventos.

Para bosses/elite, BT é perfeito.

## Checklist

```
[ ] Instalar/ativar LimboAI plugin
[ ] Criar behavior tree root
[ ] Adicionar nós AS (CanActivate, Activate, DispatchEvent)
[ ] Testar com debug habilitado
[ ] Sincronizar com abilities do AS
[ ] Implementar fallbacks
[ ] Balancear complexidade vs performance
```

---

**Relacionado:** [Guia de Multiplayer](guide-multiplayer.md)
