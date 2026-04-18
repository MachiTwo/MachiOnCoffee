---
title: "ASStateCache & ASStateSnapshot"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `RefCounted` (Cache) | `Resource` (Snapshot)

## ASStateCache

## Descrição Breve

Buffer circular de alta performance (128 ticks) para rollback multiplayer.

## Descrição Completa

`ASStateCache` é um buffer interno automático que armazena snapshots de estado a cada `_physics_process` tick. Mantém os
últimos 128 ticks para permitir rollback instantâneo sem alocação de memória.

**Automaticamente gerenciado**—você não cria nem popula manualmente. O `ASComponent` cuida disso.

## Uso em Rollback

```gdscript
# Cliente detecta erro de predição
if server_state != predicted_state:
    # Restaurar para tick anterior e re-simular
    asc.apply_snapshot(server_tick_id)
```gdscript

## Estrutura Interna

```gdscript
Tick 0   → [Attrs, Tags, Effects]
Tick 1   → [Attrs, Tags, Effects]
...
Tick 127 → [Attrs, Tags, Effects] ← Buffer circular
         ↻ (volta para tick 0 ao overflow)
```gdscript

Cada entrada armazena:

- Todos os valores de atributo
- Tags ativas
- Effects ativos com duração
- Timestamp/tick_id

---

## ASStateSnapshot

## Descrição Breve

Resource para persistência de estado (saves e multiplayer).

## Descrição Completa

`ASStateSnapshot` é um Resource que armazena um snapshot completo e serializable do estado de um ator:

- **Atributos**: Todos os valores base e modificadores
- **Tags**: Lista de tags ativas
- **Effects**: Effects ativos com duração/stacks
- **Cooldowns**: Estado de abilities
- **Histórico**: Buffer de mudanças recentes

Permite:

- **Save/Load**: Persistência em disco
- **Multiplayer**: Sincronização de estado entre cliente/servidor
- **Rollback**: Restaurar a estado anterior

## ⚠️ Uso Restrito

**Regra Crítica**: Use apenas em **players/personagens controláveis**. NPCs massivos não devem usar snapshots (overhead
de performance).

```gdscript
# ✅ CORRETO: Player tem snapshot
player_asc.snapshot_state = player_snapshot_resource

# ❌ INCORRETO: 1000 inimigos com snapshots = lag
for enemy in enemy_list:
    enemy_asc.snapshot_state = snapshot_resource  # NÃO FAÇA ISTO!
```gdscript

## Métodos

## `capture_snapshot(asc: ASComponent) → void`

Congela estado atual em snapshot.

```gdscript
asc.capture_snapshot()  # Salva estado antes de ação preditiva
```gdscript

## `load_snapshot(asc: ASComponent) → void`

Restaura estado de snapshot.

```gdscript
asc.apply_snapshot(tick_id)  # Carrega de ASStateCache se disponível
# Ou carrega de snapshot_state se tick mais antigo
```gdscript

## Serialização

Snapshots são nativamente serializáveis:

```gdscript
# Salvar em disco
var save_data = {
    "player_snapshot": asc.snapshot_state.to_dict()
}
save_to_file(save_data)

# Carregar do disco
var load_data = load_from_file()
asc.snapshot_state = ASStateSnapshot.new()
asc.snapshot_state.from_dict(load_data["player_snapshot"])
asc.apply_snapshot(-1)  # -1 = use snapshot_state
```gdscript

## Casos de Uso

## Multiplayer Client Prediction + Rollback

```gdscript
func _physics_process(delta):
    if is_local_authority():
        # 1. Capture pre-prediction state
        asc.capture_snapshot()

        # 2. Local prediction
        if Input.is_action_just_pressed("fire"):
            asc.try_activate_ability_by_tag(&"ability.slash")

        # 3. Send to server
        asc.request_activate_ability.rpc_id(1, &"ability.slash")

@rpc("any_peer", "call_local")
func request_activate_ability(tag: StringName):
    if is_server():
        if asc.can_activate_ability_by_tag(tag):
            asc.try_activate_ability_by_tag(tag)
            asc.confirm_ability_activation.rpc(tag)
        else:
            # Predição falhou—cliente rollback
            asc.apply_snapshot(current_tick)  # ASStateCache
            asc.deny_ability_activation.rpc(tag)
```gdscript

## Game Save/Load

```gdscript
func save_game():
    var save_data = {
        "player_health": asc.get_attribute_current_value(&"health"),
        "player_mana": asc.get_attribute_current_value(&"mana"),
        "snapshot": asc.snapshot_state.to_dict() if asc.snapshot_state else null
    }
    save_to_disk(save_data)

func load_game():
    var save_data = load_from_disk()

    if save_data.get("snapshot"):
        asc.snapshot_state = ASStateSnapshot.new()
        asc.snapshot_state.from_dict(save_data["snapshot"])
        asc.apply_snapshot(-1)
    else:
        # Fallback: restaurar valores manualmente
        asc.set_attribute_base_value(&"health", save_data["player_health"])
        asc.set_attribute_base_value(&"mana", save_data["player_mana"])
```gdscript

## Nó de Checkpoint

```gdscript
class_name Checkpoint

var checkpoint_snapshot: ASStateSnapshot

func _ready():
    if checkpoint_snapshot == null:
        checkpoint_snapshot = ASStateSnapshot.new()

func save_checkpoint(asc: ASComponent):
    # Congelar estado atual
    checkpoint_snapshot.from_dict(asc.get_state_dict())
    print("Checkpoint salvo!")

func load_checkpoint(asc: ASComponent):
    if checkpoint_snapshot:
        asc.apply_snapshot_data(checkpoint_snapshot)
        print("Checkpoint restaurado!")
```gdscript

## Performance Considerations

| Operação     | ASStateCache                 | ASStateSnapshot        |
| ------------ | ---------------------------- | ---------------------- |
| **Storage**  | 128 ticks em buffer circular | Full state em Resource |
| **Speed**    | Muito rápido (alocação O(1)) | Moderado (I/O disk)    |
| **Use Case** | Rollback em frame            | Save/Load em disco     |
| **Overhead** | Minimal (automático)         | Significativo em NPCs  |

## Referências Relacionadas

- [ASComponent](../nodes/ascomponent.md) — Gerencia cache/snapshot
- [ASAttributeSet](../resources/asattributeset.md) — Serializado em snapshot
- [ASEffectSpec](aseffectspec.md) — Estado salvo

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
