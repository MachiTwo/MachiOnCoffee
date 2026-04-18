---
title: "Guia: Troubleshooting e Debugging"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# Guia: Troubleshooting e Debugging

Soluções para problemas comuns.

## Problema: "Ability não ativa"

**Sintomas:** `try_activate_ability_by_tag()` retorna false

**Checklist:**

```gdscript
# 1. Verificar se ASComponent existe
var asc = AbilitySystem.resolve_component(self)
if not asc:
    print("ERROR: No ASComponent found!")
    return

# 2. Verificar se ability está registrada
if not AbilitySystem.is_tag_registered(&"ability.slash"):
    print("ERROR: Tag not registered!")
    return

# 3. Verificar se pode ativar
var can_activate = asc.can_activate_ability_by_tag(&"ability.slash")
print("Can activate: ", can_activate)

# 4. Se não, descobrir por quê
var spec = asc.get_ability_spec_by_tag(&"ability.slash")
if spec:
    print("Cooldown remaining: ", spec.get_cooldown_remaining())
    print("On cooldown: ", spec.is_on_cooldown())

# 5. Verificar custos
var ability = asc.get_ability_resource_by_tag(&"ability.slash")
print("Can afford costs: ", asc.can_afford_costs(ability))

# 6. Verificar requisitos de tag
var has_required = asc.has_all_tags(ability.activation_required_all_tags)
print("Has required tags: ", has_required)

# 7. Verificar bloqueios
var blocked_by = asc.has_any_tags(ability.activation_blocked_any_tags)
print("Blocked by tags: ", blocked_by)
```

**Soluções Comuns:**

```
Issue: Cooldown
Fix: Aguarde ou use longer_cooldown em ASAbility

Issue: Recurso insuficiente (mana)
Fix: Aumentar mana ou reduzir custo

Issue: Tag bloqueadora
Fix: Remover tag bloqueadora antes

Issue: Requisito faltando
Fix: Adicionar tag requisitada primeiro
```

## Problema: "Efeito não aplicado"

**Sintomas:** `apply_effect_by_tag()` executa mas nada acontece

```gdscript
# Debug
var effect = asc.get_effect_resource_by_tag(&"effect.burn")
print("Effect exists: ", effect != null)

# Verificar se target é válido
var target_asc = AbilitySystem.resolve_component(target)
print("Target ASComponent: ", target_asc != null)

# Aplicar e verificar
asc.apply_effect_by_tag(&"effect.burn", target_asc)

# Verificar se foi aplicado
var specs = target_asc.get_all_effect_specs()
for spec in specs:
    if spec.get_effect().effect_tag == &"effect.burn":
        print("Effect applied! Duration: ", spec.get_duration_remaining())
```

**Soluções:**

```
Issue: Target_asc é null
Fix: Certificar que target é Node válido

Issue: Efeito tem requisitos não atendidos
Fix: Remover bloqueios ou adicionar requisitos

Issue: Efeito é INSTANT e some imediatamente
Fix: Verificar effect.duration_policy
```

## Problema: "Animação não sincroniza com ability"

```gdscript
# Sincronizar com evento de ability
var spec = asc.get_ability_spec_by_tag(&"ability.slash")

asc.ability_activated.connect(func(spec):
    anim.play("slash_animation")
    print("Animation started at: ", Time.get_ticks_msec())
)

# Monitorar fases
asc.effect_applied.connect(func(effect_spec):
    var phase = asc.get_ability_spec_by_tag(&"ability.slash").get_current_phase_index()
    print("Phase: ", phase, " Effect: ", effect_spec.get_effect().effect_tag)
)
```

**Soluções:**

```
Issue: Animation player desincronizado
Fix: Usar callbacks de animation_finished

Issue: Dano aplicado no frame errado
Fix: Sincronizar com frame exato via dispatch_event

Issue: Fase avança muito rápido
Fix: Aumentar phase_duration ou usar transition_trigger
```

## Problema: "Tag não está funcionando"

```gdscript
# 1. Verificar se está registrada
print("Registered: ", AbilitySystem.is_tag_registered(&"state.burning"))
print("Type: ", AbilitySystem.get_tag_type(&"state.burning"))

# 2. Verificar se foi adicionada ao ator
print("Actor has tag: ", asc.has_tag(&"state.burning"))

# 3. Verificar hierarchically
print("Has 'state' parent: ", asc.has_tag(&"state"))

# 4. Listar todas as tags
print("All tags: ", asc.get_all_tags())

# 5. Verificar se foi removida
asc.tag_added.connect(func(tag):
    print("Tag added: ", tag)
)
asc.tag_removed.connect(func(tag):
    print("Tag removed: ", tag)
)
```

## Problema: "Multiplayer não sincroniza"

```gdscript
# 1. Verificar snapshot
if not asc.snapshot_state:
    print("ERROR: Snapshot_state não configurado!")
    return

# 2. Capturar estado
asc.capture_snapshot()
print("Captured at tick: ", Engine.get_frame_count())

# 3. Realizar ação local
asc.try_activate_ability_by_tag(&"ability.slash")

# 4. Enviar para servidor
asc.request_activate_ability.rpc_id(1, &"ability.slash")

# 5. Server valida
if asc.can_activate_ability_by_tag(&"ability.slash"):
    asc.try_activate_ability_by_tag(&"ability.slash")
    asc.confirm_ability_activation.rpc(&"ability.slash")
else:
    # Rollback
    var current_tick = Engine.get_frame_count()
    asc.apply_snapshot(current_tick)
```

## Performance Issues

**Problema:** Jogo lento com muitos atores AS

```gdscript
# Profile
var ms_start = Time.get_ticks_msec()
for i in range(1000):
    var asc = asc_list[i]
    asc.has_tag(&"state.burning")
var ms_end = Time.get_ticks_msec()
print("1000 queries: %dms" % (ms_end - ms_start))
```

**Soluções:**

```
Issue: Muitos ASComponent com snapshots
Fix: Apenas player/NPCs importantes usam snapshots

Issue: Query_tags muito frequente
Fix: Cache resultado se não muda frequentemente

Issue: ASDelivery com muitos alvos
Fix: Use collision groups para filtrar
```

## Debugging Úteis

```gdscript
# Print estado completo
func debug_full_state(asc: ASComponent):
    print("=== Actor State ===")
    print("Tags: ", asc.get_all_tags())

    print("\nAbilities:")
    for ability_spec in asc.get_all_ability_specs():
        print("  - %s (cooldown: %.2f)" % [
            ability_spec.get_ability().ability_tag,
            ability_spec.get_cooldown_remaining()
        ])

    print("\nEffects:")
    for effect_spec in asc.get_all_effect_specs():
        print("  - %s (duration: %.2f)" % [
            effect_spec.get_effect().effect_tag,
            effect_spec.get_duration_remaining()
        ])

    print("\nAttributes:")
    for attr_name in asc.get_all_attributes():
        var base = asc.get_attribute_base_value(attr_name)
        var current = asc.get_attribute_current_value(attr_name)
        print("  - %s: %.1f (base: %.1f)" % [attr_name, current, base])
```

## Logging Estruturado

```gdscript
# Criar logger customizado
class_name ASLogger
extends Node

static var log_level = 0  # 0=all, 1=warn, 2=error

static func debug(msg: String):
    if log_level <= 0:
        print("[AS:DEBUG] ", msg)

static func warn(msg: String):
    if log_level <= 1:
        print("[AS:WARN] ", msg)

static func error(msg: String):
    push_error("[AS:ERROR] ", msg)

# Uso:
ASLogger.debug("Ability activated: %s" % ability_tag)
ASLogger.warn("Cooldown active: %.2f" % remaining)
ASLogger.error("ASComponent not found!")
```

## Checklist de Debug

```
[ ] Ability tag registrada?
[ ] ASComponent presente?
[ ] Pode ativar? (cooldown, requisitos, custos)
[ ] Efeito sendo aplicado?
[ ] Target_asc válido?
[ ] Tags sendo adicionadas/removidas?
[ ] Atributos sendo modificados?
[ ] Animações sincronizadas?
[ ] Snapshots funcionando?
[ ] Performance aceitável?
```

---

**Relacionado:** [Guia de Best Practices](guide-best-practices.md)
