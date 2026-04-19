---
title: "Examples: Full RPG System"
date: "2026-04-18T22:30:00-03:00"
slug: rpg-system
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - example
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

In-depth implementation of RPG mechanics using the **Ability System**: leveling, skill trees, equipment, and attribute progression.

## 1. Experience and Leveling System

```gdscript
extends Node
class_name ExperienceSystem

signal level_up(new_level, stat_points)
signal experience_gained(amount, current_xp)

var player: Player = null
var current_xp: float = 0.0
var current_level: int = 1
var xp_thresholds: Array[float] = []
var stat_points: int = 0

func _ready():
    player = get_parent()
    _generate_xp_thresholds()

func _generate_xp_thresholds():
    ## Each level requires 20% more XP
    xp_thresholds.clear()
    var base_xp = 100.0

    for level in range(1, 100):
        var threshold = base_xp * pow(1.2, level - 1)
        xp_thresholds.append(threshold)

func gain_experience(amount: float):
    current_xp += amount
    experience_gained.emit(amount, current_xp)

    ## Level up check
    while current_xp >= xp_thresholds[current_level - 1]:
        current_xp -= xp_thresholds[current_level - 1]
        level_up_player()

func level_up_player():
    current_level += 1
    stat_points += 5 ## 5 points per level

    ## Automatic attribute bonus
    player.asc.apply_modifier(&"health", 10.0)
    player.asc.apply_modifier(&"mana", 5.0)
    player.asc.apply_modifier(&"strength", 1.0)

    level_up.emit(current_level, stat_points)
    print("Level Up! New level: %d" % current_level)

func get_xp_for_next_level() -> float:
    if current_level >= xp_thresholds.size():
        return xp_thresholds[-1]
    return xp_thresholds[current_level]

func get_xp_progress() -> float:
    var needed = get_xp_for_next_level()
    return current_xp / needed
```

## 2. Skill Tree

```gdscript
extends Node
class_name SkillTree

signal skill_unlocked(skill_id, skill_data)
signal skill_upgraded(skill_id, new_rank)

class SkillNode:
    var id: StringName
    var name: String
    var description: String
    var icon: Texture2D
    var max_rank: int = 5
    var current_rank: int = 0
    var required_level: int = 1
    var required_parent: StringName = &"" ## Parent in the tree
    var cost_per_rank: int = 1 ## Stat points
    var stat_bonus: Dictionary = {} ## {"strength": 2, "intelligence": 1}
    var ability_granted: StringName = &""

var player: Player = null
var skills: Dictionary[StringName, SkillNode] = {}
var unlocked_skills: Array[StringName] = []

func _ready():
    player = get_parent()
    _initialize_skill_tree()

func _initialize_skill_tree():
    ## Tier 1: Basic attacks
    add_skill(&"slash_mastery", SkillNode.new()).setup(
        "Slash Mastery",
        "Increases slash damage by 10% per rank",
        1, ## Level req
        &"", ## No parent
        1, ## 1 point per rank
        {"strength": 2}
    )

    add_skill(&"heavy_strike", SkillNode.new()).setup(
        "Heavy Strike",
        "Heavy attack with knockback",
        3, ## Level 3
        &"slash_mastery", ## Requires Slash Mastery
        2, ## 2 points per rank
        {"strength": 3, "constitution": 1},
        &"ability.heavy_strike"
    )

    ## Tier 2: Magic
    add_skill(&"fireball", SkillNode.new()).setup(
        "Fireball",
        "Throws a fireball",
        5,
        &"",
        2,
        {"intelligence": 3},
        &"ability.fireball"
    )

    add_skill(&"inferno", SkillNode.new()).setup(
        "Inferno",
        "Improves Fireball with AoE damage",
        10,
        &"fireball",
        3,
        {"intelligence": 5},
        &"ability.inferno"
    )

    ## Tier 3: Defense
    add_skill(&"iron_skin", SkillNode.new()).setup(
        "Iron Skin",
        "Increases defense by 5% per rank",
        2,
        &"",
        1,
        {"constitution": 2}
    )

func add_skill(skill_id: StringName, node: SkillNode) -> SkillNode:
    node.id = skill_id
    skills[skill_id] = node
    return node

func can_unlock_skill(skill_id: StringName) -> bool:
    var skill = skills[skill_id]

    ## 1. Level check
    var exp_system = player.get_node("ExperienceSystem")
    if exp_system.current_level < skill.required_level:
        return false

    ## 2. Parent check
    if skill.required_parent != &"" and skill.required_parent not in unlocked_skills:
        return false

    ## 3. Stat points check
    if player.get_node("ExperienceSystem").stat_points < skill.cost_per_rank:
        return false

    return true

func unlock_skill(skill_id: StringName) -> bool:
    if not can_unlock_skill(skill_id):
        return false

    var skill = skills[skill_id]
    var exp_system = player.get_node("ExperienceSystem")

    ## Spend points
    exp_system.stat_points -= skill.cost_per_rank
    skill.current_rank += 1

    ## Apply stat bonuses
    for stat in skill.stat_bonus:
        var bonus = skill.stat_bonus[stat]
        player.asc.apply_modifier(stat, bonus)

    ## If not unlocked, add to list
    if skill_id not in unlocked_skills:
        unlocked_skills.append(skill_id)
        skill_unlocked.emit(skill_id, skill)

        ## Grant ability if exists
        if skill.ability_granted != &"":
            player.asc.add_ability(AbilitySystem.get_ability_resource(skill.ability_granted))

    skill_upgraded.emit(skill_id, skill.current_rank)
    print("Skill unlocked: %s (Rank %d)" % [skill.name, skill.current_rank])

    return true

func get_skill_tree_paths() -> Dictionary:
    ## Returns visual tree paths {skill_id: [dependents]}
    var paths: Dictionary = {}

    for skill_id in skills:
        paths[skill_id] = []

        for other_id in skills:
            var other = skills[other_id]
            if other.required_parent == skill_id:
                paths[skill_id].append(other_id)

    return paths
```

## 3. Class System

```gdscript
extends Resource
class_name CharacterClass

enum CLASS_TYPE { WARRIOR, MAGE, ROGUE, PALADIN }

@export var class_type: CLASS_TYPE = CLASS_TYPE.WARRIOR
@export var base_health: float = 100.0
@export var base_mana: float = 50.0
@export var base_strength: float = 10.0
@export var base_intelligence: float = 5.0
@export var base_constitution: float = 10.0
@export var base_dexterity: float = 8.0
@export var starting_abilities: Array[StringName] = []

func apply_to_player(player: Player):
    var asc = player.asc

    ## Apply base stats
    asc.set_attribute_base_value(&"health", base_health)
    asc.set_attribute_base_value(&"mana", base_mana)
    asc.set_attribute_base_value(&"strength", base_strength)
    asc.set_attribute_base_value(&"intelligence", base_intelligence)
    asc.set_attribute_base_value(&"constitution", base_constitution)
    asc.set_attribute_base_value(&"dexterity", base_dexterity)

    ## Add starting abilities
    for ability_tag in starting_abilities:
        var ability = AbilitySystem.get_ability_resource(ability_tag)
        asc.add_ability(ability)

    ## Class-specifics
    match class_type:
        CLASS_TYPE.WARRIOR:
            asc.add_tag(&"class.warrior")
            asc.apply_modifier(&"damage", 1.2)

        CLASS_TYPE.MAGE:
            asc.add_tag(&"class.mage")
            asc.apply_modifier(&"mana_regeneration", 0.5)

        CLASS_TYPE.ROGUE:
            asc.add_tag(&"class.rogue")
            asc.apply_modifier(&"attack_speed", 1.3)
```

## 4. Equipment System

```gdscript
extends Node
class_name EquipmentSystem

signal equipment_changed(slot, old_item, new_item)
signal stat_changed(stat_name, old_value, new_value)

class EquipmentSlot:
    enum SLOT_TYPE { HEAD, CHEST, LEGS, FEET, HANDS, BACK, MAIN_HAND, OFF_HAND }
    var type: SLOT_TYPE
    var current_item: EquipmentItem = null

class EquipmentItem:
    var id: StringName
    var name: String
    var slot: EquipmentSlot.SLOT_TYPE
    var rarity: String ## "common", "uncommon", "rare", "legendary"
    var level_requirement: int
    var stat_modifiers: Dictionary ## {"strength": 5, "health": 20}
    var ability_granted: StringName = &""
    var durability: float = 100.0
    var max_durability: float = 100.0

var player: Player = null
var equipment_slots: Dictionary[int, EquipmentSlot] = {}
var inventory: Array[EquipmentItem] = []

func _ready():
    player = get_parent()
    _initialize_slots()

func _initialize_slots():
    for slot_type in EquipmentSlot.SLOT_TYPE.values():
        equipment_slots[slot_type] = EquipmentSlot.new()
        equipment_slots[slot_type].type = slot_type

func equip_item(item: EquipmentItem) -> bool:
    ## Level requirement check
    var exp_system = player.get_node("ExperienceSystem")
    if exp_system.current_level < item.level_requirement:
        return false

    ## Remove previous item
    var slot = equipment_slots[item.slot]
    var old_item = slot.current_item

    if old_item:
        _remove_item_bonuses(old_item)

    ## Equip new item
    slot.current_item = item
    _apply_item_bonuses(item)

    equipment_changed.emit(item.slot, old_item, item)
    print("Equipped: %s" % item.name)

    return true

func _apply_item_bonuses(item: EquipmentItem):
    for stat in item.stat_modifiers:
        var bonus = item.stat_modifiers[stat]
        player.asc.apply_modifier(stat, bonus)

    if item.ability_granted != &"":
        var ability = AbilitySystem.get_ability_resource(item.ability_granted)
        player.asc.add_ability(ability)

func _remove_item_bonuses(item: EquipmentItem):
    for stat in item.stat_modifiers:
        var bonus = item.stat_modifiers[stat]
        player.asc.apply_modifier(stat, -bonus)

    if item.ability_granted != &"":
        var ability = AbilitySystem.get_ability_resource(item.ability_granted)
        player.asc.remove_ability(ability)

func take_durability_damage(amount: float):
    for slot_type in equipment_slots:
        var slot = equipment_slots[slot_type]
        if slot.current_item:
            slot.current_item.durability -= amount

            if slot.current_item.durability <= 0:
                unequip_item(slot.current_item.slot)
                print("Item broke: %s" % slot.current_item.name)

func unequip_item(slot_type: int):
    var slot = equipment_slots[slot_type]
    if slot.current_item:
        _remove_item_bonuses(slot.current_item)
        slot.current_item = null
```

## 5. Inventory System

```gdscript
extends Node
class_name InventorySystem

signal item_added(item)
signal item_removed(item)
signal inventory_full

const MAX_SLOTS = 20
var inventory: Array = []

func add_item(item: Variant) -> bool:
    if inventory.size() >= MAX_SLOTS:
        inventory_full.emit()
        return false

    inventory.append(item)
    item_added.emit(item)
    return true

func use_consumable(item_id: StringName):
    var item = get_item_by_id(item_id)
    if not item: return

    ## Apply effect
    match item_id:
        &"potion.health":
            var player = get_parent()
            player.heal(50.0)
        &"potion.buff_strength":
            var player = get_parent()
            player.asc.apply_effect_by_tag(&"effect.strength_buff")

    inventory.erase(item)
    item_removed.emit(item)
```

## 6. Character Setup

```gdscript
extends CharacterBody3D
class_name PlayerRPG

@onready var asc = $AbilityComponent
@onready var anim = $AnimationPlayer

var experience_system: ExperienceSystem
var skill_tree: SkillTree
var equipment_system: EquipmentSystem
var inventory_system: InventorySystem

var health: float = 100.0
var is_in_combat = false

signal health_changed(new_health)
signal died

func _ready():
    experience_system = ExperienceSystem.new()
    add_child(experience_system)

    skill_tree = SkillTree.new()
    add_child(skill_tree)

    equipment_system = EquipmentSystem.new()
    add_child(equipment_system)

    inventory_system = InventorySystem.new()
    add_child(inventory_system)

    ## Select class
    var warrior_class = preload("res://assets/classes/warrior.tres")
    warrior_class.apply_to_player(self)

func take_damage(amount: float):
    health -= amount
    asc.dispatch_event(&"event.damage", amount)
    health_changed.emit(health)

    ## Damage equipment durability
    equipment_system.take_durability_damage(amount * 0.01)

    if health <= 0:
        die()

func heal(amount: float):
    health = min(health + amount, get_max_health())
    health_changed.emit(health)

func get_max_health() -> float:
    return asc.get_attribute_current_value(&"health")

func die():
    is_in_combat = false
    anim.play("death")
    died.emit()
```

## 7. RPG UI

```gdscript
extends CanvasLayer
class_name RPG_UI

@onready var level_label = $VBox/LevelLabel
@onready var xp_bar = $VBox/XPBar
@onready var health_bar = $VBox/HealthBar

var player: PlayerRPG

func _ready():
    player = get_parent()
    player.experience_system.level_up.connect(_on_level_up)
    player.experience_system.experience_gained.connect(_on_experience_gained)
    player.health_changed.connect(_on_health_changed)

func _on_level_up(new_level: int, stat_points: int):
    level_label.text = "Level: %d" % new_level

func _on_experience_gained(amount: float, current_xp: float):
    var progress = player.experience_system.get_xp_progress()
    xp_bar.value = progress * 100

func _on_health_changed(new_health: float):
    var max_health = player.get_max_health()
    health_bar.value = (new_health / max_health) * 100
```

---

The **Ability System** provides the necessary hooks for all these systems to talk harmoniously through Tags and Attributes.
