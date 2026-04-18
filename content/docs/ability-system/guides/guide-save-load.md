---
title: "Guia: Sistema de Salvamento e Carregamento"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Sistema de Salvamento e Carregamento

Padrões para persistência de estado Ability System.

## Conceitos

**O que salvar:**

- Attributes (stats, health, mana)
- Tags (estado, imunidades)
- Abilities desbloqueadas
- Effects ativos
- Cooldowns
- Skill tree progress
- Equipment
- Inventory

**O que NÃO salvar:**

- Specs em tempo real (refaz-se ao carregar)
- Snapshots (128-tick buffer)
- Transient state (durante abilities)

## 1. Save Data Structure

```gdscript
class_name GameSaveData
extends Resource

## Metadados
@export var save_slot: int = 0
@export var save_timestamp: float = 0.0
@export var character_name: String = ""
@export var level: int = 1

## Atributos
@export var attributes: Dictionary = {}  # {"health": 100.0, "mana": 50.0}
@export var attribute_modifiers: Dictionary = {}  # Persistent modifiers

## Tags
@export var tags: PackedStringArray = []

## Abilities
@export var ability_tags: PackedStringArray = []
@export var ability_cooldowns: Dictionary = {}  # {"ability.slash": 0.5}

## Effects
@export var active_effects: Array = []  # Array de effect data

## Progression
@export var experience: float = 0.0
@export var skill_tree_unlocked: PackedStringArray = []
@export var skill_ranks: Dictionary = {}  # {"slash_mastery": 3}

## Equipment
@export var equipment_slots: Dictionary = {}  # {"head": item_data}
@export var inventory_items: Array = []

## Posição e Estado
@export var position: Vector3 = Vector3.ZERO
@export var rotation: Vector3 = Vector3.ZERO

func to_json() -> String:
    var dict = {
        "save_slot": save_slot,
        "save_timestamp": save_timestamp,
        "character_name": character_name,
        "level": level,
        "attributes": attributes,
        "tags": tags,
        "ability_tags": ability_tags,
        "ability_cooldowns": ability_cooldowns,
        "experience": experience,
        "skill_tree_unlocked": skill_tree_unlocked,
        "skill_ranks": skill_ranks,
        "position": var_to_str(position),
        "rotation": var_to_str(rotation)
    }
    return JSON.stringify(dict)

static func from_json(json: String) -> GameSaveData:
    var data = GameSaveData.new()
    var dict = JSON.parse_string(json)

    data.save_slot = dict.get("save_slot", 0)
    data.save_timestamp = dict.get("save_timestamp", 0.0)
    data.character_name = dict.get("character_name", "")
    data.level = dict.get("level", 1)
    data.attributes = dict.get("attributes", {})
    data.tags = PackedStringArray(dict.get("tags", []))
    data.ability_tags = PackedStringArray(dict.get("ability_tags", []))
    data.ability_cooldowns = dict.get("ability_cooldowns", {})
    data.experience = dict.get("experience", 0.0)
    data.skill_tree_unlocked = PackedStringArray(dict.get("skill_tree_unlocked", []))
    data.skill_ranks = dict.get("skill_ranks", {})
    data.position = str_to_var(dict.get("position", "Vector3(0, 0, 0)"))
    data.rotation = str_to_var(dict.get("rotation", "Vector3(0, 0, 0)"))

    return data
```

## 2. Capturar Estado

```gdscript
extends Node
class_name GameSaveSystem

var save_directory: String = "user://saves/"
var auto_save_interval: float = 300.0  # 5 minutos

func _ready():
    if not DirAccess.dir_exists_absolute(save_directory):
        DirAccess.make_absolute(save_directory)

    # Auto-save timer
    var timer = Timer.new()
    add_child(timer)
    timer.timeout.connect(_on_auto_save_timeout)
    timer.start(auto_save_interval)

func capture_player_state(player: Node) -> GameSaveData:
    var save_data = GameSaveData.new()

    save_data.save_timestamp = Time.get_ticks_msec() / 1000.0
    save_data.character_name = player.name
    save_data.position = player.global_position
    save_data.rotation = player.global_rotation

    # Capturar ASComponent
    var asc = player.asc

    # Atributos
    save_data.attributes = {}
    for attr in asc.get_all_attributes():
        save_data.attributes[attr] = asc.get_attribute_current_value(attr)

    # Tags
    save_data.tags = PackedStringArray(asc.get_all_tags())

    # Abilities e cooldowns
    save_data.ability_tags = PackedStringArray()
    save_data.ability_cooldowns = {}

    for ability_spec in asc.get_all_ability_specs():
        var ability = ability_spec.get_ability()
        save_data.ability_tags.append(ability.ability_tag)

        if ability_spec.is_on_cooldown():
            save_data.ability_cooldowns[ability.ability_tag] = ability_spec.get_cooldown_remaining()

    # Experiência e progressão
    var exp_system = player.get_node("ExperienceSystem")
    save_data.experience = exp_system.current_xp
    save_data.level = exp_system.current_level

    # Skill tree
    var skill_tree = player.get_node("SkillTree")
    save_data.skill_tree_unlocked = PackedStringArray(skill_tree.unlocked_skills)
    save_data.skill_ranks = {}

    for skill_id in skill_tree.skills:
        var skill = skill_tree.skills[skill_id]
        save_data.skill_ranks[skill_id] = skill.current_rank

    # Equipment
    var equipment_system = player.get_node("EquipmentSystem")
    save_data.equipment_slots = {}

    for slot_type in equipment_system.equipment_slots:
        var slot = equipment_system.equipment_slots[slot_type]
        if slot.current_item:
            save_data.equipment_slots[slot_type] = {
                "id": slot.current_item.id,
                "durability": slot.current_item.durability
            }

    # Inventory
    var inventory_system = player.get_node("InventorySystem")
    save_data.inventory_items = []

    for item in inventory_system.inventory:
        save_data.inventory_items.append({
            "id": item.id,
            "quantity": 1  # Se item stacking
        })

    return save_data

func save_game(player: Node, slot: int = 0) -> bool:
    var save_data = capture_player_state(player)
    save_data.save_slot = slot

    var file_path = save_directory + "save_%d.json" % slot

    var file = FileAccess.open(file_path, FileAccess.WRITE)
    if file == null:
        print("ERROR: Não conseguiu salvar em %s" % file_path)
        return false

    file.store_string(save_data.to_json())
    print("✅ Game saved to slot %d" % slot)
    return true

func _on_auto_save_timeout():
    var player = get_tree().root.get_child(0).find_child("Player", true, false)
    if player:
        save_game(player, 0)  # Auto-save no slot 0
```

## 3. Carregar Estado

```gdscript
func load_game(player: Node, slot: int = 0) -> bool:
    var file_path = save_directory + "save_%d.json" % slot

    if not FileAccess.file_exists(file_path):
        print("ERROR: Save file not found: %s" % file_path)
        return false

    var file = FileAccess.open(file_path, FileAccess.READ)
    var json_string = file.get_as_text()
    var save_data = GameSaveData.from_json(json_string)

    # Restaurar estado
    _restore_player_state(player, save_data)

    print("✅ Game loaded from slot %d" % slot)
    return true

func _restore_player_state(player: Node, save_data: GameSaveData):
    var asc = player.asc

    # 1. Restaurar atributos
    print("Restoring attributes...")
    for attr_name in save_data.attributes:
        var value = save_data.attributes[attr_name]
        asc.set_attribute_base_value(attr_name, value)

    # 2. Restaurar tags
    print("Restoring tags...")
    for tag in save_data.tags:
        asc.add_tag(tag)

    # 3. Restaurar abilities
    print("Restoring abilities...")
    for ability_tag in save_data.ability_tags:
        var ability = AbilitySystem.get_ability_resource(ability_tag)
        if ability:
            asc.add_ability(ability)

            # Restaurar cooldown
            if ability_tag in save_data.ability_cooldowns:
                var remaining = save_data.ability_cooldowns[ability_tag]
                var spec = asc.get_ability_spec_by_tag(ability_tag)
                if spec:
                    spec.apply_cooldown(remaining)

    # 4. Restaurar experiência
    print("Restoring progression...")
    var exp_system = player.get_node("ExperienceSystem")
    exp_system.current_xp = save_data.experience
    exp_system.current_level = save_data.level

    # 5. Restaurar skill tree
    print("Restoring skill tree...")
    var skill_tree = player.get_node("SkillTree")

    for skill_id in save_data.skill_tree_unlocked:
        skill_tree.unlocked_skills.append(skill_id)

        if skill_id in save_data.skill_ranks:
            var skill = skill_tree.skills[skill_id]
            skill.current_rank = save_data.skill_ranks[skill_id]

    # 6. Restaurar equipment
    print("Restoring equipment...")
    var equipment_system = player.get_node("EquipmentSystem")

    for slot_type in save_data.equipment_slots:
        var item_data = save_data.equipment_slots[slot_type]
        var item = _recreate_equipment_item(item_data)
        equipment_system.equip_item(item)

    # 7. Restaurar inventory
    print("Restoring inventory...")
    var inventory_system = player.get_node("InventorySystem")

    for item_data in save_data.inventory_items:
        var item = _recreate_inventory_item(item_data)
        inventory_system.add_item(item)

    # 8. Restaurar posição
    player.global_position = save_data.position
    player.global_rotation = save_data.rotation

    print("✅ All systems restored")

func _recreate_equipment_item(item_data: Dictionary):
    # Buscar item resource se necessário
    var item = load("res://assets/equipment/%s.tres" % item_data["id"])
    if item:
        item.durability = item_data.get("durability", item.max_durability)
    return item

func _recreate_inventory_item(item_data: Dictionary):
    return load("res://assets/items/%s.tres" % item_data["id"])
```

## 4. Versioning de Save

```gdscript
class_name SaveVersionManager

const SAVE_VERSION = 2

func save_with_version(save_data: GameSaveData) -> String:
    var wrapper = {
        "version": SAVE_VERSION,
        "timestamp": Time.get_ticks_msec(),
        "data": JSON.parse_string(save_data.to_json())
    }
    return JSON.stringify(wrapper)

func load_with_version(json: String) -> GameSaveData:
    var wrapper = JSON.parse_string(json)
    var version = wrapper.get("version", 1)
    var data = wrapper.get("data", {})

    # Migração de versão
    match version:
        1:
            data = _migrate_v1_to_v2(data)
        2:
            pass  # Versão atual

    return _dict_to_save_data(data)

func _migrate_v1_to_v2(old_data: Dictionary) -> Dictionary:
    # Exemplo: v1 tinha "mana_points", v2 tem "mana"
    if "mana_points" in old_data:
        old_data["mana"] = old_data["mana_points"]
        old_data.erase("mana_points")

    return old_data

func _dict_to_save_data(data: Dictionary) -> GameSaveData:
    var save_data = GameSaveData.new()
    # ... (preencher campos)
    return save_data
```

## 5. Cloud Save Integration

```gdscript
extends Node
class_name CloudSaveSystem

var cloud_enabled: bool = false
var cloud_service: String = "steam"  # ou "playfab", "gamesparks"

func upload_save(player: Node, slot: int = 0):
    var save_system = get_node("../GameSaveSystem")
    var save_data = save_system.capture_player_state(player)

    # 1. Salvar localmente
    save_system.save_game(player, slot)

    # 2. Fazer upload
    match cloud_service:
        "steam":
            _upload_steam(save_data, slot)
        "playfab":
            _upload_playfab(save_data, slot)

func _upload_steam(save_data: GameSaveData, slot: int):
    # Usar Steam Cloud API
    var file_path = "save_%d.json" % slot
    var content = save_data.to_json().to_utf8_buffer()

    # Steam.fileWrite(file_path, content)
    print("Uploaded to Steam Cloud: %s" % file_path)

func _upload_playfab(save_data: GameSaveData, slot: int):
    # Usar PlayFab API
    var url = "https://your-title.playfabapi.com/Client/UpdateUserData"

    var json = {
        "Data": {
            "GameSave_%d" % slot: save_data.to_json()
        },
        "Permission": "Public"
    }

    # var http = HTTPRequest.new()
    # http.request(url, ["X-Authorization: %s" % auth_token], HTTPClient.METHOD_POST, JSON.stringify(json))

func download_save(slot: int):
    match cloud_service:
        "steam":
            _download_steam(slot)
        "playfab":
            _download_playfab(slot)

func _download_steam(slot: int):
    var file_path = "save_%d.json" % slot
    # var content = Steam.fileRead(file_path)
    # var save_data = GameSaveData.from_json(content.get_string_from_utf8())
    print("Downloaded from Steam Cloud: %s" % file_path)
```

## 6. Validação de Save

```gdscript
extends Node
class_name SaveValidator

func validate_save(save_data: GameSaveData) -> bool:
    var errors: Array = []

    # 1. Verificar atributos
    if save_data.attributes.is_empty():
        errors.append("No attributes saved")

    for attr in save_data.attributes:
        var value = save_data.attributes[attr]
        if not (value is float or value is int):
            errors.append("Invalid attribute type: %s" % attr)

    # 2. Verificar tags válidas
    for tag in save_data.tags:
        if not AbilitySystem.is_tag_registered(tag):
            errors.append("Unknown tag: %s" % tag)

    # 3. Verificar abilities
    for ability_tag in save_data.ability_tags:
        if not AbilitySystem.get_ability_resource(ability_tag):
            errors.append("Unknown ability: %s" % ability_tag)

    # 4. Verificar cooldowns válidos
    for ability_tag in save_data.ability_cooldowns:
        var cooldown = save_data.ability_cooldowns[ability_tag]
        if cooldown < 0:
            errors.append("Invalid cooldown for %s" % ability_tag)

    # 5. Verificar level válido
    if save_data.level <= 0 or save_data.level > 100:
        errors.append("Invalid level: %d" % save_data.level)

    # 6. Reportar
    if not errors.is_empty():
        print("❌ Save validation failed:")
        for error in errors:
            print("  - %s" % error)
        return false

    print("✅ Save is valid")
    return true
```

## 7. Exemplo Completo: Save/Load Menu

```gdscript
extends CanvasLayer
class_name SaveLoadUI

@onready var save_buttons = $VBox/SaveSlots
@onready var load_buttons = $VBox/LoadSlots
@onready var status_label = $StatusLabel

var save_system: GameSaveSystem
var current_player: Node

func _ready():
    save_system = get_tree().root.get_child(0).get_node("GameSaveSystem")
    current_player = get_tree().root.get_child(0).find_child("Player", true, false)

    _update_save_slots()

func _update_save_slots():
    # Limpar botões
    for child in save_buttons.get_children():
        child.queue_free()

    for child in load_buttons.get_children():
        child.queue_free()

    # Criar botões para cada slot
    for slot in range(5):
        # Save button
        var save_btn = Button.new()
        save_btn.text = "Save Slot %d" % slot
        save_btn.pressed.connect(_on_save_pressed.bind(slot))
        save_buttons.add_child(save_btn)

        # Load button
        var load_btn = Button.new()
        var save_path = save_system.save_directory + "save_%d.json" % slot

        if FileAccess.file_exists(save_path):
            load_btn.text = "Load Slot %d (exists)" % slot
            load_btn.pressed.connect(_on_load_pressed.bind(slot))
        else:
            load_btn.text = "Load Slot %d (empty)" % slot
            load_btn.disabled = true

        load_buttons.add_child(load_btn)

func _on_save_pressed(slot: int):
    if save_system.save_game(current_player, slot):
        status_label.text = "Saved to slot %d" % slot
        _update_save_slots()
    else:
        status_label.text = "Save failed!"

func _on_load_pressed(slot: int):
    if save_system.load_game(current_player, slot):
        status_label.text = "Loaded from slot %d" % slot
    else:
        status_label.text = "Load failed!"
```

## 8. Encryption (Opcional)

```gdscript
extends Node
class_name EncryptedSaveSystem

var encryption_key: String = "YOUR_SECRET_KEY_HERE"

func encrypt_save(save_data: GameSaveData) -> String:
    var json = save_data.to_json()
    var cipher = AESContext.new()

    # Usar Key derivation
    var key = _derive_key(encryption_key, 32)
    cipher.start(AESContext.MODE_CBC, key, _get_iv())

    var encrypted = cipher.update(json.to_utf8_buffer())
    encrypted += cipher.finish()

    return Marshalls.raw_to_base64(encrypted)

func decrypt_save(encrypted_data: String) -> GameSaveData:
    var cipher = AESContext.new()
    var key = _derive_key(encryption_key, 32)

    cipher.start(AESContext.MODE_CBC, key, _get_iv())
    var decrypted = cipher.update(Marshalls.base64_to_raw(encrypted_data))
    decrypted += cipher.finish()

    var json = decrypted.get_string_from_utf8()
    return GameSaveData.from_json(json)

func _derive_key(password: String, size: int) -> PackedByteArray:
    # Usar PBKDF2 or similar
    var hasher = HashingContext.new()
    hasher.start(HashingContext.HASH_SHA256)
    hasher.update(password.to_utf8_buffer())
    return hasher.finish().slice(0, size)

func _get_iv() -> PackedByteArray:
    # Usar IV fixo ou armazenar junto do save
    return PackedByteArray([0] * 16)
```

## Checklist Save/Load

```
Design:
[ ] Definir que dados salvar
[ ] Estrutura de save data
[ ] Estratégia de versioning
[ ] Validação de save

Implementation:
[ ] Capture state function
[ ] Save to disk
[ ] Load from disk
[ ] Restore all systems
[ ] Error handling
[ ] Encryption (if needed)

Testing:
[ ] Teste save/load básico
[ ] Teste corrupted save
[ ] Teste version migration
[ ] Teste cloud sync
[ ] Performance em saves grandes
[ ] Teste concorrência

Deployment:
[ ] Cleanup old saves
[ ] Backup system
[ ] Save location (user://)
[ ] Encryption em produção
```

---

Save/load é crítico para player retention.
