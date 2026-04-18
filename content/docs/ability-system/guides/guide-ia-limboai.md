---
title: "Guia: Integração com LimboAI (Behavior Trees)"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

Controle o Ability System inteiramente via Behavior Trees.

## Arquitetura

```gdscript
BehaviorTree
├─ Selector (decisão)
│  ├─ Sequence (combo)
│  │  ├─ Condition: CanActivate
│  │  └─ Action: ActivateAbility
│  └─ Sequence (fallback)
│     └─ Action: Move
```gdscript

## Passo 1: Criar Behavior Tree Simples

No editor, crie uma cena com **LimboAIPlayer**.

Crie BT:

```gdscript
Root: Selector
├─ Sequence: "Attack"
│  ├─ Condition: BTConditionAS_CanActivate (ability.slash)
│  ├─ Action: BTActionAS_ActivateAbility (ability.slash)
│  └─ Action: Wait (0.5s)
└─ Action: Move Towards Target
```gdscript

## Passo 2: Configurar Nós BT

**BTConditionAS_CanActivate:**

```gdscript
ability_tag: &"ability.slash"
asc_node_path: (vazio para auto-resolve)
```gdscript

**BTActionAS_ActivateAbility:**

```gdscript
ability_tag: &"ability.slash"
activation_level: 1.0
asc_node_path: (vazio)
```gdscript

## Passo 3: Padrão Decisional Avançado

```gdscript
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
```gdscript

## Passo 4: Event-Driven Behavior

Dispara evento → BT reage:

```gdscript
Sequence:
├─ Action: DispatchEvent (event.player_hit)
├─ Action: WaitForEvent (event.player_hit_back)
│  time_window: 1.0
└─ Action: Counter Attack
```gdscript

Script para sincronizar:

```gdscript
func _on_player_hit(damage):
    asc.dispatch_event(&"event.player_hit")
    # BT aguarda "player_hit_back" por até 1s
    # Se receber, executa contra-ataque
```gdscript

## Passo 5: Combo Tree

```gdscript
Sequence: "Combo Chain"
├─ Action: ActivateAbility (combo.1)
├─ Action: WaitForEvent (combo.1_finished, timeout: 2.0)
├─ Action: ActivateAbility (combo.2)
├─ Action: WaitForEvent (combo.2_finished, timeout: 2.0)
└─ Action: ActivateAbility (combo.3_finisher)
```gdscript

Se qualquer passo falha (timeout), sequence falha.

## Passo 6: Tag-Based Decision Tree

```gdscript
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
```gdscript

## Passo 7: Parallel Tasks (Simultâneos)

```gdscript
Parallel:
├─ Action: MoveWhileAttacking
├─ Sequence:
│  ├─ WaitForEvent (enemy_near)
│  └─ ActivateAbility (ability.slash)
```gdscript

Ambos rodam simultaneamente.

## Caso de Uso: Boss Multi-Fase

```gdscript
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
```gdscript

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
```gdscript

## Debugging BT

Enable debug no LimboAI:

```gdscript
# No script do agent:
func _ready():
    limbo_ai_player.debug_enabled = true
```gdscript

Output:

```gdscript
[BTSelector] → trying option 0
  [BTConditionAS_CanActivate] slash → SUCCESS
  [BTActionAS_ActivateAbility] slash → SUCCESS
  [BTActionWait] 0.5s → RUNNING
```gdscript

## Performance

**Vantagem:** BTs escalam bem com complexidade.

**Desvantagem:** Overhead vs script puro.

Para centenas de inimigos, use script + eventos.

Para bosses/elite, BT é perfeito.

## Checklist

```gdscript
[ ] Instalar/ativar LimboAI plugin
[ ] Criar behavior tree root
[ ] Adicionar nós AS (CanActivate, Activate, DispatchEvent)
[ ] Testar com debug habilitado
[ ] Sincronizar com abilities do AS
[ ] Implementar fallbacks
[ ] Balancear complexidade vs performance
```gdscript

---

**Relacionado:** [Guia de Multiplayer](guide-multiplayer.md)
