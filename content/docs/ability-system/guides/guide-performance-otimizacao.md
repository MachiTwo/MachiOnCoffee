---
title: "Guia: Performance e Otimização"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

Técnicas comprovadas para otimizar Ability System em produção.

## Profiling Baseline

Antes de otimizar, medir:

````gdscript
# Criar baseline
class_name PerformanceMonitor
extends Node

var perf_data: Dictionary = {}

func measure_operation(name: String, callable: Callable) -> Variant:
    var start = Time.get_ticks_usec()
    var result = callable.call()
    var elapsed_us = Time.get_ticks_usec() - start

    if name not in perf_data:
        perf_data[name] = []

    perf_data[name].append(elapsed_us)
    return result

func get_stats(operation_name: String) -> Dictionary:
    var measurements = perf_data.get(operation_name, [])
    if measurements.is_empty():
        return {}

    var avg = measurements.reduce(func(a, b): return a + b) / measurements.size()
    var max_val = measurements.max()
    var min_val = measurements.min()

    return {
        "avg_us": avg,
        "max_us": max_val,
        "min_us": min_val,
        "count": measurements.size()
    }

func print_report():
    print("\n=== PERFORMANCE REPORT ===")
    for op_name in perf_data:
        var stats = get_stats(op_name)
        print("%s: avg=%.2fµs max=%.2fµs (n=%d)" % [
            op_name, stats["avg_us"], stats["max_us"], stats["count"]
        ])

# Uso:
var monitor = PerformanceMonitor.new()
monitor.measure_operation("tag_query", func():
    return asc.has_tag(&"state.burning")
)
monitor.print_report()
```gdscript

## 1. Tag System Optimization

**Problema:** Queries frequentes de tags são O(n)

**Solução:** Caching + batch queries

```gdscript
# ❌ Ruim: 1000 queries por frame
func _physics_process(_delta):
    for enemy in enemies:
        if enemy.asc.has_tag(&"state.burning"):
            handle_burning(enemy)

# ✅ Bom: 1 query de batch
func _physics_process(_delta):
    var burning_enemies = enemies.filter(func(e):
        return e.asc.has_tag(&"state.burning")
    )
    for enemy in burning_enemies:
        handle_burning(enemy)

# ✅✅ Melhor: Cache com invalidação
class TagCache:
    var cache: Dictionary = {}
    var dirty: bool = true

    func get_enemies_with_tag(enemies: Array, tag: StringName) -> Array:
        var cache_key = "%s_%d" % [tag, enemies.size()]

        if not dirty and cache_key in cache:
            return cache[cache_key]

        var result = enemies.filter(func(e):
            return e.asc.has_tag(tag)
        )

        cache[cache_key] = result
        dirty = false
        return result

    func invalidate():
        dirty = true
```gdscript

## 2. Ability Activation Optimization

**Problema:** Try-activate em muitos actors

```gdscript
# ❌ Ruim: Validação completa em cada chamada
func _physics_process(_delta):
    for npc in npcs:
        if npc.asc.can_activate_ability_by_tag(&"ability.attack"):
            npc.asc.try_activate_ability_by_tag(&"ability.attack")

# ✅ Bom: Cache de specs + reuse
var ability_spec_cache: Dictionary = {}

func get_ability_spec_cached(asc: ASComponent, tag: StringName) -> ASAbilitySpec:
    var cache_key = "%s_%d" % [tag, asc.get_instance_id()]

    if cache_key not in ability_spec_cache:
        ability_spec_cache[cache_key] = asc.get_ability_spec_by_tag(tag)

    return ability_spec_cache[cache_key]

func _physics_process(_delta):
    for npc in npcs:
        var spec = get_ability_spec_cached(npc.asc, &"ability.attack")
        if spec and not spec.is_on_cooldown():
            npc.asc.try_activate_ability_by_tag(&"ability.attack")
```gdscript

## 3. Effect Application Optimization

**Problema:** Aplicar efeito a muitos targets

```gdscript
# ❌ Ruim: RPC para cada alvo (50 inimigos = 50 RPCs)
func cast_explosion(center: Vector3, radius: float):
    var targets = get_targets_in_radius(center, radius)
    for target in targets:
        target.asc.apply_effect_by_tag(&"effect.fire_damage", asc)

# ✅ Bom: Batch aplicação
func cast_explosion_batched(center: Vector3, radius: float):
    var targets = get_targets_in_radius(center, radius)
    var batch = ASEffectBatch.new()

    for target in targets:
        batch.queue_effect(&"effect.fire_damage", target.asc)

    batch.apply_all()

class ASEffectBatch:
    var queued: Array = []

    func queue_effect(effect_tag: StringName, target_asc: ASComponent):
        queued.append({"effect": effect_tag, "target": target_asc})

    func apply_all():
        for item in queued:
            item["target"].apply_effect_by_tag(item["effect"])
```gdscript

## 4. Attribute System Optimization

**Problema:** Getter frequentes recalculam tudo

```gdscript
# ❌ Ruim: Recalcula drivers a cada frame
func _physics_process(_delta):
    var damage = asc.get_attribute_current_value(&"damage")  # O(drivers count)
    deal_damage(target, damage)

# ✅ Bom: Cache atributo quando drivers mudam
func _on_driver_changed():
    damage_cache_dirty = true

func get_damage_cached() -> float:
    if damage_cache_dirty:
        damage_cache = asc.get_attribute_current_value(&"damage")
        damage_cache_dirty = false
    return damage_cache

# ✅✅ Melhor: Usar tag em vez de atributo
# Em lugar de:
if asc.get_attribute_current_value(&"health") <= 0:
    die()

# Usar:
if asc.has_tag(&"state.dead"):
    die()

# E aplicar effect quando health <= 0 que concede state.dead
```gdscript

## 5. Snapshot System Optimization

**Problema:** 128-tick buffer usa muita memória

```gdscript
# ❌ Ruim: Snapshot tudo, 128 ticks
# Cada snapshot = 1 KB, 128 snapshots = 128 KB por actor

# ✅ Bom: Snapshot apenas para multiplayer authority
func capture_snapshot():
    if not is_multiplayer_authority():
        return  # Não fazer snapshot para clientes

    if Engine.get_physics_frames() % 10 == 0:  # A cada 10 frames
        asc.capture_snapshot()

# ✅✅ Melhor: Snapshot comprimido
class CompressedSnapshot:
    var tick: int
    var health: float
    var mana: float
    var tags: PackedStringArray

    func from_asc(asc: ASComponent) -> CompressedSnapshot:
        var snapshot = CompressedSnapshot.new()
        snapshot.tick = Engine.get_physics_frames()
        snapshot.health = asc.get_attribute_current_value(&"health")
        snapshot.mana = asc.get_attribute_current_value(&"mana")

        # Apenas tags críticas
        var critical_tags = []
        for tag in asc.get_all_tags():
            if tag.begins_with("state.") or tag.begins_with("immune."):
                critical_tags.append(tag)

        snapshot.tags = PackedStringArray(critical_tags)
        return snapshot
```gdscript

## 6. Delivery System Optimization

**Problema:** ASDelivery com muitos raycast checks

```gdscript
# ❌ Ruim: Raycast para cada target
func _physics_process(delta):
    var targets = get_all_actors()
    for target in targets:
        if raycast_to(target):
            apply_effect(target)

# ✅ Bom: Usar collision groups + rayshape
var collision_query = PhysicsShapeQueryParameters3D.new()

func _ready():
    var shape = SphereShape3D.new()
    shape.radius = 5.0
    collision_query.shape = shape
    collision_query.collision_mask = 0b0001  # Layer 1 only

func apply_aoe_effect(center: Vector3, radius: float):
    collision_query.shape.radius = radius
    collision_query.transform.origin = center

    var results = get_world_3d().direct_space_state.intersect_shape(collision_query)

    for result in results:
        var target = result["collider"]
        apply_effect(target)
```gdscript

## 7. Memory Pooling

**Problema:** Criar/destruir specs frequentemente

```gdscript
# ❌ Ruim: new() a cada uso
func use_ability():
    var spec = ASAbilitySpec.new()  # Alloc
    spec.init(ability)
    # ...
    spec = null  # Dealloc (GC delay)

# ✅ Bom: Pool reutilizável
class SpecPool:
    var available: Array[ASAbilitySpec] = []
    var in_use: Array[ASAbilitySpec] = []

    func get_spec(ability: ASAbility) -> ASAbilitySpec:
        var spec: ASAbilitySpec

        if available.is_empty():
            spec = ASAbilitySpec.new()
        else:
            spec = available.pop_back()

        spec.init(ability)
        in_use.append(spec)
        return spec

    func return_spec(spec: ASAbilitySpec):
        in_use.erase(spec)
        spec.reset()
        available.append(spec)

var pool = SpecPool.new()

func use_ability():
    var spec = pool.get_spec(ability)
    # ...
    pool.return_spec(spec)
```gdscript

## 8. Update Frequency Optimization

**Problema:** Atualizar tudo a 60 FPS

```gdscript
# ❌ Ruim: Atualizar todos os atores a 60 FPS
func _physics_process(_delta):
    for actor in all_actors:
        actor.update_state()

# ✅ Bom: Atualização por distância
var update_distances = {
    60.0: 60,      # Close: 60 FPS
    120.0: 30,     # Medium: 30 FPS
    300.0: 10      # Far: 10 FPS
}

var last_update: Dictionary = {}

func update_actor(actor: Node, delta: float):
    var distance = player.global_position.distance_to(actor.global_position)
    var update_interval = 1.0 / get_update_frequency(distance)

    var actor_id = actor.get_instance_id()
    last_update[actor_id] = last_update.get(actor_id, 0.0) + delta

    if last_update[actor_id] >= update_interval:
        actor.update_state()
        last_update[actor_id] = 0.0

func get_update_frequency(distance: float) -> float:
    for dist in update_distances:
        if distance <= dist:
            return update_distances[dist]
    return 1  # 1 FPS para muito longe
```gdscript

## 9. Batch Processing

**Problema:** Processar cada actor individualmente

```gdscript
# ❌ Ruim: Loop aninhado O(n²)
func check_all_damage():
    for attacker in attackers:
        for target in targets:
            if attacker.can_hit(target):
                attacker.damage(target)

# ✅ Bom: Quadtree + spatial queries
class SpatialHash:
    var cells: Dictionary = {}
    var cell_size: float = 10.0

    func add_object(obj: Node3D):
        var cell = get_cell_key(obj.global_position)
        if cell not in cells:
            cells[cell] = []
        cells[cell].append(obj)

    func get_nearby(pos: Vector3, radius: float) -> Array:
        var nearby: Array = []
        var cell = get_cell_key(pos)

        for check_cell in get_nearby_cells(cell, radius):
            if check_cell in cells:
                nearby.append_array(cells[check_cell])

        return nearby

    func get_cell_key(pos: Vector3) -> Vector2i:
        return Vector2i(pos.x / cell_size, pos.z / cell_size)
```gdscript

## 10. Async Processing

**Problema:** Tudo síncrono = travamentos

```gdscript
# ❌ Ruim: Carregar 1000 efeitos síncronamente
func load_all_effects():
    for effect_id in 1000:
        var effect = load("res://effects/%d.tres" % effect_id)

# ✅ Bom: Carregamento assíncrono
func load_effects_async():
    var resource_loader = ResourceLoader

    for effect_id in 1000:
        var path = "res://effects/%d.tres" % effect_id
        resource_loader.load_threaded_request(path)

func _process(_delta):
    # Processar recursos carregados
    if ResourceLoader.is_cached("res://effects/1.tres"):
        var effect = ResourceLoader.load_threaded_get("res://effects/1.tres")
        register_effect(effect)
```gdscript

## 11. GC Pressure Reduction

**Problema:** Muitas alocações = GC pauses

```gdscript
# ❌ Ruim: Array temporário a cada frame
func get_burning_enemies() -> Array:
    return enemies.filter(func(e): return e.asc.has_tag(&"state.burning"))

# ✅ Bom: Reusar array
var burning_cache: Array = []

func update_burning_enemies():
    burning_cache.clear()

    for enemy in enemies:
        if enemy.asc.has_tag(&"state.burning"):
            burning_cache.append(enemy)

    return burning_cache

# ✅✅ Melhor: Usar PackedArray quando possível
var burning_ids: PackedInt64Array = []

func update_burning_ids():
    burning_ids.clear()

    for enemy in enemies:
        if enemy.asc.has_tag(&"state.burning"):
            burning_ids.append(enemy.get_instance_id())
```gdscript

## 12. Benchmark Completo

```gdscript
class_name ABilitySystemBenchmark
extends Node

func run_benchmarks():
    print("\n=== AS BENCHMARK SUITE ===\n")

    var asc = preload("res://test_asc.tscn").instantiate()
    add_child(asc)

    # 1. Tag queries
    benchmark("Tag: has_tag", func():
        asc.has_tag(&"state.burning")
    )

    # 2. Ability activation
    benchmark("Ability: can_activate", func():
        asc.can_activate_ability_by_tag(&"ability.slash")
    )

    # 3. Effect application
    benchmark("Effect: apply", func():
        asc.apply_effect_by_tag(&"effect.burn")
    )

    # 4. Attribute read
    benchmark("Attribute: get_value", func():
        asc.get_attribute_current_value(&"health")
    )

    # 5. Get all tags
    benchmark("Query: get_all_tags", func():
        asc.get_all_tags()
    )

    # 6. Get all abilities
    benchmark("Query: get_all_abilities", func():
        asc.get_all_ability_specs()
    )

    print("\n=== MEMORY USAGE ===")
    print("Estimated AS footprint: ~2 KB per component")
    print("Snapshots (128-tick): ~128 KB per authority")

func benchmark(name: String, callable: Callable, iterations: int = 10000):
    var start = Time.get_ticks_usec()

    for i in range(iterations):
        callable.call()

    var elapsed = Time.get_ticks_usec() - start
    var per_call = float(elapsed) / iterations

    print("%s: %.3f µs/call (total: %d µs)" % [name, per_call, elapsed])
```gdscript

## Performance Checklist

```gdscript
Profiling:
[ ] Baseline measurements
[ ] Identify bottlenecks
[ ] Monitor GC pauses
[ ] Profile memory usage

Optimization (Priority):
[ ] Tag query caching
[ ] Ability spec caching
[ ] Batch effect application
[ ] Reduce snapshot frequency
[ ] Spatial partitioning
[ ] Update LOD system
[ ] Object pooling
[ ] Async resource loading

Testing:
[ ] Verify correctness post-optimization
[ ] Benchmark improvements
[ ] Monitor in-game performance
[ ] Test edge cases (100+ actors)
[ ] Profile production builds

Deployment:
[ ] Document optimization decisions
[ ] Set performance budgets
[ ] Monitor runtime metrics
[ ] Alert on regressions
```gdscript

---

Performance é iterativo: medir → otimizar → verificar.
````
