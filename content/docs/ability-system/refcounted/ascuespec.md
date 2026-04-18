---
title: "ASCueSpec"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

**Badge:** `RefCounted`

## Descrição Breve

Contexto runtime para execução de uma cue (feedback audiovisual).

## Descrição Completa

`ASCueSpec` encapsula o estado e contexto para uma cue durante execução. Mantém referências a:

- **Definição**: `ASCue` resource (imutável)
- **Source**: Qual `ASComponent` originou (atacante, lançador)
- **Target**: Qual `ASComponent` recebe (alvo)
- **Effect Context**: `ASEffectSpec` que disparou a cue
- **Magnitude**: Valor calculado (para escala de efeito)
- **Nível**: Power level para ajuste visual
- **Hit Position**: Onde o efeito ocorreu
- **Extra Data**: Payload customizado

Criada automaticamente pelo `ASComponent`—raramente instanciada manualmente.

## Herança

````gdscript
RefCounted
 └─ ASCueSpec
```gdscript

## Métodos

## Inicialização

## `init(cue: ASCue, level: float = 1.0) → void`

Inicializa spec com definição de cue e nível.

## Acesso a Definição

## `get_cue() → ASCue` (const)

Retorna resource ASCue original (imutável).

## Nível e Magnitude

## `get_level() → float` (const)

Power level da instância de cue (herança de effect).

## `set_level(level: float) → void`

Define nível (afeta magnitude de modificadores visuais).

## `get_magnitude() → float` (const)

Magnitude calculada do effect que disparou cue.

**Uso:** Escalar tamanho de partículas, volume de som, etc.

```gdscript
func _on_cue_triggered(spec: ASCueSpec):
    var magnitude = spec.get_magnitude()
    vfx.scale = Vector3.ONE * (1.0 + magnitude * 0.1)  # Escala visual
```gdscript

## Componentes

## `get_source_asc() → ASComponent` (const)

`ASComponent` que originou o effect (atacante).

Pode ser `null` se damage origem indeterminada (environmental).

## `get_target_asc() → ASComponent` (const)

`ASComponent` que recebe o effect (alvo).

Sempre não-null (cue dispara no alvo).

## `get_target_node() → Object` (const)

Nó visual alvo onde cue executa (pode ser diferente de target_asc owner).

**Uso:** Reproduzir animação em sprite específico, não no owner completo.

```gdscript
var target_node = spec.get_target_node()
if target_node:
    target_node.play_animation(&"hit")
```gdscript

## Effect Context

## `get_effect_spec() → ASEffectSpec` (const)

`ASEffectSpec` que disparou esta cue.

Permite acessar modificadores, duração, source attribute values, etc.

```gdscript
var effect_spec = spec.get_effect_spec()
var damage_modifier = effect_spec.get_magnitude(&"health")  # -30.0
var attacker_strength = effect_spec.get_source_attribute_value(&"strength")
```gdscript

## Posição e Extra Data

## `get_hit_position() → Variant` (const)

Posição onde impact ocorreu (Vector3 ou null).

**Uso:** Spawnar efeito visual em coordenada específica.

```gdscript
var pos = spec.get_hit_position()
if pos:
    vfx_particle_system.global_position = pos
```gdscript

## `get_source_attribute_value(attribute: StringName) → float` (const)

Valor de atributo no source (atacante).

## `get_target_attribute_value(attribute: StringName) → float` (const)

Valor de atributo no target (alvo).

**Uso:** Escalar efeitos por resistência do alvo.

```gdscript
var target_fire_resistance = spec.get_target_attribute_value(&"fire_resistance")
var final_damage = 100 * (1.0 - target_fire_resistance * 0.01)
```gdscript

## `get_extra_data() → Dictionary` (const)

Payload customizado passado durante dispatch.

```gdscript
var extra = spec.get_extra_data()
var crit_chance = extra.get("crit_chance", 0.0)
if randf() < crit_chance:
    play_critical_vfx()
```gdscript

## `set_extra_data(data: Dictionary) → void`

Define extra data (antes de execução de cue).

## `get_source_attribute_value(attribute: StringName) → float`

Query atributo no source para escaling baseado em source stats.

## Setters

## `set_cue(cue: ASCue) → void`

Define resource cue (raramente usado).

## `set_effect_spec(effect: ASEffectSpec) → void`

Define effect context.

## `set_source_asc(asc: ASComponent) → void`

Define source component.

## `set_target_asc(asc: ASComponent) → void`

Define target component.

## `set_target_node(node: Object) → void`

Define nó visual alvo.

## `set_hit_position(pos: Variant) → void`

Define posição de impacto.

## `set_magnitude(mag: float) → void`

Define magnitude manualmente.

## Casos de Uso

## Escalar VFX por Magnitude

```gdscript
func _on_effect_applied(effect_spec: ASEffectSpec):
    var cue_spec = ASCueSpec.new()
    cue_spec.init(fire_burst_cue)
    cue_spec.set_magnitude(effect_spec.get_magnitude(&"health"))

    # Partículas maiores para damage maior
    var magnitude = cue_spec.get_magnitude()
    vfx.emission_range_y = 10.0 + (magnitude * 0.5)
```gdscript

## Cue com Contexto de Source

```gdscript
func play_impact_cue(spec: ASCueSpec):
    var source = spec.get_source_asc()
    var target = spec.get_target_asc()

    # Efeito de knockback baseado em força do atacante
    var source_strength = spec.get_source_attribute_value(&"strength")
    target.apply_knockback(source_strength * 0.5)

    # Efeito visual no target
    target.play_impact_animation()
```gdscript

## Cue com Hit Position

```gdscript
func spawn_impact_effect(spec: ASCueSpec):
    var pos = spec.get_hit_position()
    var target_node = spec.get_target_node()

    if pos and target_node:
        var vfx = preload("res://vfx/impact.tscn").instantiate()
        target_node.add_child(vfx)
        vfx.global_position = pos
        vfx.play(&"impact")
```gdscript

## Cascata de Efeitos (Criando Cues Customizadas)

```gdscript
func _on_burn_effect_applied(effect_spec: ASEffectSpec):
    # Criar spec de cue customizado
    var cue_spec = ASCueSpec.new()
    cue_spec.init(burn_cue)
    cue_spec.set_source_asc(effect_spec.get_source_component())
    cue_spec.set_target_asc(effect_spec.get_target_component())

    # Extra data para lógica visual
    var extra = {
        "stack_count": effect_spec.get_stack_count(),
        "duration": effect_spec.get_duration_remaining()
    }
    cue_spec.set_extra_data(extra)

    # Fire cue
    fire_cue(cue_spec)
```gdscript

## Integração com ASComponent

`ASComponent` cria automaticamente `ASCueSpec` quando efeito dispara cue:

```gdscript
# Interno ao ASComponent:
var cue_spec = ASCueSpec.new()
cue_spec.init(cue_resource, level)
cue_spec.set_source_asc(source_component)
cue_spec.set_target_asc(target_component)
cue_spec.set_effect_spec(effect_spec)  # Contexto do effect
cue_spec.set_magnitude(effect_spec.get_magnitude(&"health"))
# Dispara cue com spec como contexto
```gdscript

Você pode conectar sinais para interceptar:

```gdscript
asc.effect_applied.connect(func(effect_spec):
    # Effect já foi aplicado, cues já disparadas internamente
    pass
)
```gdscript

## Performance

**Leve:** `ASCueSpec` é RefCounted—auto-deletado quando não referenciado.

Sem alocações por frame na crítica.

## Referências Relacionadas

- [ASCue](../resources/ascue.md) — Definição de cue
- [ASCueAnimation](../resources/ascueanimation.md) — Cue animation
- [ASCueAudio](../resources/ascueaudio.md) — Cue audio
- [ASEffectSpec](aseffectspec.md) — Contexto de effect
- [ASComponent](../nodes/ascomponent.md) — Cria e dispara specs

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
````
