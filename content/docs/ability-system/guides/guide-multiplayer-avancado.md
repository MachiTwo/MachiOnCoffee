---
title: "Guia: Multiplayer Avançado"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Multiplayer Avançado

Padrões comprovados para sincronização de Ability System em multiplayer.

## Conceitos Fundamentais

**Client Prediction:** Cliente executa ação imediatamente, sincroniza com servidor **Server Authority:** Servidor valida
e confirma/nega ações **State Reconciliation:** Cliente rollback se servidor negar **128-Tick Buffer:** ASStateCache
mantém histórico de 128 ticks para rollback suave

## Arquitetura Base

```gdscript
# Server.gd
extends Node

class_name MultiplayerServer

var players: Dictionary = {}

func _ready():
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)

func _on_peer_connected(peer_id: int):
    players[peer_id] = load("res://scenes/player.tscn").instantiate()
    add_child(players[peer_id])
    print("Player %d connected" % peer_id)

func _on_peer_disconnected(peer_id: int):
    if peer_id in players:
        players[peer_id].queue_free()
        players.erase(peer_id)
    print("Player %d disconnected" % peer_id)
```

## 1. Client-Side Prediction

**Fluxo:**

```gdscript
# PlayerClient.gd
extends CharacterBody3D
class_name PlayerClient

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var target: Node3D = null
var is_local_player = false

func _physics_process(_delta):
    if not is_local_player:
        return

    # 1. Capturar snapshot PRÉ-ação
    asc.capture_snapshot()

    # 2. Input local
    if Input.is_action_just_pressed("ability_1"):
        try_use_ability(&"ability.slash")
    elif Input.is_action_just_pressed("ability_2"):
        try_use_ability(&"ability.heavy_attack")

func try_use_ability(ability_tag: StringName):
    # 3. Validar localmente
    if not asc.can_activate_ability_by_tag(ability_tag):
        print("Localmente indisponível: %s" % ability_tag)
        return

    # 4. Executar localmente (optimistic)
    asc.try_activate_ability_by_tag(ability_tag)

    # 5. Animar
    var ability = asc.get_ability_resource_by_tag(ability_tag)
    if ability:
        anim.play("ability_%s" % ability_tag.to_lower())

    # 6. Requisitar ao servidor
    request_ability_activation.rpc_id(1, ability_tag, Engine.get_physics_frames())
```

## 2. Server-Side Validation

**Validação Rigorosa:**

```gdscript
# PlayerServer.gd
extends CharacterBody3D
class_name PlayerServer

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

@rpc("any_peer", "call_local")
func request_ability_activation(ability_tag: StringName, client_frame: int):
    var peer_id = multiplayer.get_remote_sender_id()

    # 1. Validação servidor
    if not asc.can_activate_ability_by_tag(ability_tag):
        print("Server rejected %s for peer %d" % [ability_tag, peer_id])
        deny_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
        return

    # 2. Executar servidor
    asc.try_activate_ability_by_tag(ability_tag)

    # 3. Propagar a outros clientes
    var affected_players = get_affected_targets(ability_tag)
    for target_peer in affected_players:
        confirm_ability_activation.rpc_id(target_peer, ability_tag, peer_id)

    print("Server confirmed %s from peer %d" % [ability_tag, peer_id])

@rpc("authority", "call_local")
func deny_ability_activation(ability_tag: StringName, client_frame: int):
    # Cliente recebe negação
    if is_multiplayer_authority():
        return

    print("Ability denied: %s at frame %d" % [ability_tag, client_frame])
    asc.apply_snapshot(client_frame)  # Rollback

@rpc("authority", "call_local")
func confirm_ability_activation(ability_tag: StringName, peer_id: int):
    # Confirmar para outros clientes
    if is_multiplayer_authority():
        return

    var peer_asc = get_node("../Player%d/AbilityComponent" % peer_id)
    if peer_asc:
        peer_asc.try_activate_ability_by_tag(ability_tag)
```

## 3. Snapshot e Rollback

**ASStateCache - 128-Tick Circular Buffer:**

```gdscript
# Em ASComponent - já implementado
# Exemplo de uso:

func use_snapshot_system():
    var asc = $AbilityComponent

    # Snapshot atual
    asc.capture_snapshot()

    # Tentar ação
    asc.try_activate_ability_by_tag(&"ability.dash")

    # Se server nega, rollback
    if server_denied:
        var tick_to_restore = Engine.get_physics_frames() - 5
        asc.apply_snapshot(tick_to_restore)
        print("Rolledback to tick %d" % tick_to_restore)
```

**Estrutura Interna:**

```gdscript
# Circular buffer de 128 ticks
class_name ASStateCache

var ticks: Array[Dictionary] = []
var tick_index: int = 0
var current_tick: int = 0

func capture_snapshot():
    var state = {
        "frame": Engine.get_physics_frames(),
        "health": asc.get_attribute_current_value(&"health"),
        "mana": asc.get_attribute_current_value(&"mana"),
        "tags": asc.get_all_tags().duplicate(),
        "cooldowns": {}
    }

    # Snapshot ciclical
    ticks[tick_index % 128] = state
    tick_index += 1

func apply_snapshot(target_tick: int):
    # Encontra snapshot mais próximo
    var idx = target_tick % 128
    if idx < ticks.size():
        var state = ticks[idx]
        # Restaura atributos, tags, cooldowns
        print("Restored to frame %d" % state["frame"])
```

## 4. Sincronização de Efeitos

**Broadcast de Efeitos:**

```gdscript
# PlayerServer.gd
func apply_effect_networked(effect_tag: StringName, target_peer: int):
    var target_asc = get_node("../Player%d/AbilityComponent" % target_peer)

    # Servidor aplica
    asc.apply_effect_by_tag(effect_tag, target_asc)

    # Broadcast a todos
    broadcast_effect_applied.rpc(effect_tag, target_peer, multiplayer.get_unique_id())

@rpc("authority", "call_local")
func broadcast_effect_applied(effect_tag: StringName, target_peer: int, caster_peer: int):
    # Clientes sincronizam efeito
    if is_multiplayer_authority():
        return

    var target = get_node("../Player%d" % target_peer)
    if target:
        var target_asc = target.get_node("AbilityComponent")
        var caster_asc = get_node("../Player%d/AbilityComponent" % caster_peer)
        target_asc.apply_effect_by_tag(effect_tag, caster_asc)
```

## 5. Atributos Replicados

**Sincronização Automática:**

```gdscript
# PlayerServer.gd
func _physics_process(delta):
    # Server valida atributos
    if asc.get_attribute_current_value(&"health") <= 0:
        die()

    # Sync a cada mudança significativa
    if asc.has_tag(&"attribute.dirty"):
        sync_attributes()
        asc.remove_tag(&"attribute.dirty")

func sync_attributes():
    var attrs = {
        "health": asc.get_attribute_current_value(&"health"),
        "mana": asc.get_attribute_current_value(&"mana"),
        "stamina": asc.get_attribute_current_value(&"stamina")
    }
    broadcast_attributes.rpc(attrs)

@rpc("authority")
func broadcast_attributes(attrs: Dictionary):
    # Clientes atualizam
    for attr_name in attrs:
        var value = attrs[attr_name]
        asc.set_attribute_current_value(attr_name, value)
```

## 6. Lag Compensation

**Dead Reckoning:**

```gdscript
# PlayerClient.gd
var last_server_position: Vector3 = Vector3.ZERO
var last_server_velocity: Vector3 = Vector3.ZERO
var last_update_time: float = 0.0

func _physics_process(delta):
    # Extrapolação local enquanto aguarda update
    if Time.get_ticks_msec() - last_update_time > 50:
        global_position += last_server_velocity * delta

func receive_server_update(new_pos: Vector3, new_vel: Vector3):
    last_server_position = new_pos
    last_server_velocity = new_vel
    last_update_time = Time.get_ticks_msec()

    # Smooth correction
    var correction = new_pos - global_position
    if correction.length() > 0.5:
        # Teleport se desvio muito grande (hack/desync)
        global_position = new_pos
    else:
        # Smooth blend
        global_position = global_position.lerp(new_pos, 0.2)
```

## 7. Transição de Autoridade

**Quando Player Muda de Host:**

```gdscript
# HostMigration.gd
func _on_peer_disconnected(peer_id: int):
    # Se autoridade desconectou
    if multiplayer.server_peer == peer_id:
        # Eleger novo servidor
        var new_server = players.keys()[0]
        multiplayer.multiplayer_peer.remove_peer(peer_id)

        # Transferir autoridade de players
        for player in players:
            player.asc.set_multiplayer_authority(new_server)

        print("New server elected: %d" % new_server)
```

## 8. Cheat Prevention

**Validações Servidor:**

```gdscript
# PlayerServer.gd
func request_ability_activation(ability_tag: StringName, client_frame: int):
    var peer_id = multiplayer.get_remote_sender_id()

    # 1. Rate limit (máx 10 abilities/seg)
    if ability_request_count >= 10:
        deny_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
        return

    # 2. Verificar cooldown (servidor tem autoridade)
    var spec = asc.get_ability_spec_by_tag(ability_tag)
    if spec and spec.is_on_cooldown():
        deny_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
        return

    # 3. Verificar recurso (mana, stamina)
    var ability = asc.get_ability_resource_by_tag(ability_tag)
    if not asc.can_afford_costs(ability):
        deny_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
        return

    # 4. Validar distância (se AoE)
    if ability.target_type == ASAbility.TARGET_TYPE.OTHERS:
        var distance = global_position.distance_to(target.global_position)
        if distance > ability.max_range:
            deny_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
            return

    # Aprovado
    asc.try_activate_ability_by_tag(ability_tag)
    confirm_ability_activation.rpc_id(peer_id, ability_tag, client_frame)
```

## 9. Sincronização de Tags

**Tag Replication:**

```gdscript
# PlayerServer.gd
func _physics_process(_delta):
    # Monitorar mudanças de tag
    asc.tag_added.connect(_on_tag_added)
    asc.tag_removed.connect(_on_tag_removed)

func _on_tag_added(tag: StringName):
    # Propagate
    broadcast_tag_changed.rpc("add", tag)

func _on_tag_removed(tag: StringName):
    # Propagate
    broadcast_tag_changed.rpc("remove", tag)

@rpc("authority")
func broadcast_tag_changed(operation: String, tag: StringName):
    if is_multiplayer_authority():
        return

    if operation == "add":
        asc.add_tag(tag)
    elif operation == "remove":
        asc.remove_tag(tag)
```

## 10. Exemplo Completo: Batalha 1v1

```gdscript
# MultiplayerBattle.gd
extends Node3D
class_name MultiplayerBattle

@onready var player_1 = $Player1
@onready var player_2 = $Player2
@onready var ui = $UI

var battle_active = false

func _ready():
    # Setup autoridade
    if multiplayer.is_server():
        player_1.asc.set_multiplayer_authority(1)
        player_2.asc.set_multiplayer_authority(2)

    # Conectar eventos
    player_1.asc.effect_applied.connect(_on_effect_applied.bind(1))
    player_2.asc.effect_applied.connect(_on_effect_applied.bind(2))

    battle_active = true

func _physics_process(_delta):
    if not battle_active:
        return

    # Apenas servidor valida states
    if not multiplayer.is_server():
        return

    # Verificar vitória
    if player_1.health <= 0:
        end_battle(2)
    elif player_2.health <= 0:
        end_battle(1)

func _on_effect_applied(effect_spec, player_num: int):
    var attacker = player_1 if player_num == 1 else player_2
    var defender = player_2 if player_num == 1 else player_1

    # Dano
    var damage = effect_spec.get_magnitude(&"health")
    if damage < 0:
        defender.asc.apply_modifier(&"health", damage)
        broadcast_damage.rpc(player_num, -damage)

func broadcast_damage(attacker_num: int, damage: float):
    var attacker = player_1 if attacker_num == 1 else player_2
    var defender = player_2 if attacker_num == 1 else player_1

    ui.show_damage(defender, damage)
    print("%s took %.0f damage!" % [defender.name, damage])

func end_battle(winner_num: int):
    battle_active = false
    broadcast_battle_end.rpc(winner_num)

@rpc("authority")
func broadcast_battle_end(winner_num: int):
    ui.show_winner(winner_num)
```

## 11. Performance em Multiplayer

**Otimizações:**

```gdscript
# Reduzir frequência de sync
var sync_timer = 0.0
var sync_interval = 0.1  # 10 Hz

func _physics_process(delta):
    sync_timer += delta
    if sync_timer >= sync_interval:
        sync_state()
        sync_timer = 0.0

# Caching de queries
var cached_abilities: Dictionary = {}

func get_ability_cached(tag: StringName):
    if not tag in cached_abilities:
        cached_abilities[tag] = asc.get_ability_resource_by_tag(tag)
    return cached_abilities[tag]

# Batch updates
var pending_updates: Array = []

func queue_update(update_type: String, data):
    pending_updates.append({"type": update_type, "data": data})

func flush_updates():
    if pending_updates.is_empty():
        return

    broadcast_batch_updates.rpc(pending_updates)
    pending_updates.clear()
```

## 12. Debugging Multiplayer

```gdscript
# MultiplayerDebug.gd
extends Node

static var debug_enabled = true

static func log_action(peer_id: int, action: String, data: Variant = null):
    if not debug_enabled:
        return

    var timestamp = Time.get_ticks_msec()
    print("[%d] [P%d] %s: %s" % [timestamp, peer_id, action, data])

static func log_sync(peer_id: int, tick: int, data: Variant):
    if not debug_enabled:
        return

    print("[SYNC] P%d Tick=%d Data=%s" % [peer_id, tick, data])

static func log_rollback(peer_id: int, from_tick: int, to_tick: int):
    if not debug_enabled:
        return

    print("[ROLLBACK] P%d %d->%d" % [peer_id, from_tick, to_tick])

# Uso:
MultiplayerDebug.log_action(1, "ability_used", &"ability.slash")
MultiplayerDebug.log_sync(1, frame_count, {"health": 100})
MultiplayerDebug.log_rollback(2, 150, 140)
```

## Checklist Multiplayer

```
Design:
[ ] Identificar client vs server actions
[ ] Definir taxa de sync (10-20 Hz típico)
[ ] Planejar lag compensation
[ ] Validações servidor

Implementation:
[ ] Snapshot system
[ ] Rollback logic
[ ] RPC handlers
[ ] Error handling
[ ] Timeout management

Testing:
[ ] Simular lag (AddressSanitizer)
[ ] Teste disconnect/reconnect
[ ] Teste 100+ jogadores
[ ] Performance profiling

Deployment:
[ ] Rate limiting
[ ] Cheat detection
[ ] Logging centralizado
[ ] Monitoring
```

---

Padrões robustos para multiplayer escalável.
