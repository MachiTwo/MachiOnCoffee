---
title: "ASAbility"
date: "2026-04-18T12:00:00-03:00"
type: docs
---


**Badge:** `Resource`

## Descrição Breve

Resource que define a lógica e dados de uma ação específica.

## Descrição Completa

`ASAbility` encapsula toda a lógica de uma ação dentro do framework. Define:

- **Custos**: Quais atributos são consumidos ao ativar
- **Requisitos**: Quais atributos/tags são necessários para ativar
- **Cooldowns**: Tempo antes de poder ativar novamente (com tags opcionais durante cooldown)
- **Owned Tags**: Tags concedidas enquanto a ability está ativa
- **Efeitos**: Quais effects são aplicados
- **Triggers**: Ativação automática baseada em eventos/tags
- **Fases**: Subdivisão em estágios granulares (Windup, Execution, Recovery)
- **Cues**: Feedback audiovisual (animação, som)
- **Duração**: Instant, Duration, ou Infinite

## Herança

```gdscript
Resource
 └─ ASAbility
```gdscript

## Propriedades

## Identidade

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `ability_name` | String | `""` | Nome único da ability |
| `ability_tag` | StringName | `&""` | Tag identificadora (tipo NAME) |

## Duração

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `ability_duration_policy` | int (enum) | `POLICY_INSTANT` | `POLICY_INSTANT` (0), `POLICY_DURATION` (1), `POLICY_INFINITE` (2) |
| `ability_duration` | float | `0.0` | Base duration quando `POLICY_DURATION` |
| `ability_use_custom_duration` | bool | `false` | Se `true`, trigger callback customizado para cálculo de duração |

## Custos e Requisitos

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `costs` | Dictionary[] | `[]` | Array de custos nativos (atributo → amount) |
| `costs_use_custom` | bool | `false` | Se `true`, trigger callback para cálculo customizado |
| `requirements` | Dictionary[] | `[]` | Array de requisitos (atributo → amount mínimo) |

## Cooldown

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `cooldown_duration` | float | `0.0` | Base duration do cooldown |
| `cooldown_tags` | StringName[] | `[]` | Tags aplicadas durante cooldown |
| `cooldown_use_custom` | bool | `false` | Se `true`, trigger callback customizado |

## Validação de Ativação (Tags)

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `activation_required_all_tags` | StringName[] | `[]` | Owner DEVE ter TODAS estas tags (AND) |
| `activation_required_any_tags` | StringName[] | `[]` | Owner DEVE ter PELO MENOS UMA (OR) |
| `activation_blocked_any_tags` | StringName[] | `[]` | Falha se owner tiver QUALQUER UMA (OR) |
| `activation_blocked_all_tags` | StringName[] | `[]` | Falha se owner tiver TODAS SIMULTANEAMENTE (AND) |

## Estado Enquanto Ativa

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `activation_owned_tags` | StringName[] | `[]` | Tags concedidas enquanto ability está ativa |
| `activation_cancel_tags` | StringName[] | `[]` | Tags de abilities ativas que serão canceladas ao ativar esta |

## Conteúdo

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `effects` | ASEffect[] | `[]` | Effects aplicados por esta ability |
| `cues` | ASCue[] | `[]` | Feedback audiovisual (animação, som) |
| `phases` | ASAbility[] | `[]` | Fases sequenciais (ASAbilityPhase) |
| `sub_abilities` | ASAbility[] | `[]` | Sub-abilities desbloqueadas junto |
| `sub_abilities_auto_activate` | StringName[] | `[]` | Tags de sub-abilities que ativam automaticamente |

## Eventos

| Propriedade | Tipo | Padrão | Descrição |
|------------|------|--------|----------|
| `events_on_activate` | StringName[] | `[]` | Events disparados ao sucesso |
| `events_on_end` | StringName[] | `[]` | Events disparados ao término |
| `triggers` | Dictionary[] | `[]` | Automação reativa (tag added/removed/event) |

## Constantes (Enums)

## DurationPolicy

```gdscript
enum DurationPolicy {
    POLICY_INSTANT = 0,   # Executa uma vez e termina imediatamente
    POLICY_DURATION = 1,  # Tem duração fixa
    POLICY_INFINITE = 2   # Permanece até explicitamente cancelada
}
```gdscript

## TriggerType

```gdscript
enum TriggerType {
    TRIGGER_ON_TAG_ADDED = 0,    # Ativa quando tag é adicionada
    TRIGGER_ON_TAG_REMOVED = 1,  # Ativa quando tag é removida
    TRIGGER_ON_EVENT = 2         # Ativa quando evento é disparado (preferido)
}
```gdscript

## Métodos Públicos (Gameplay)

## Ativação Segura

## `try_activate_ability(owner: ASComponent, spec: ASAbilitySpec = null, target_node: Object = null) → void`

Tenta ativar a ability com todas as validações. Integra verificação e ação.

**Parâmetros:**

- `owner`: Componente que ativa (deve ter o spec)
- `spec`: Instância de ability ativa (criada automaticamente se null)
- `target_node`: Alvo específico (usado por effects)

**Valida automaticamente:**

- Tags requeridas/bloqueadas
- Custos (se tem recursos suficientes)
- Cooldown (se não está em espera)

**Emite sinais:**

- `ability_activated` se sucesso
- `ability_failed` se falha

## `can_activate_ability(owner: ASComponent, spec: ASAbilitySpec = null) → bool` (const)

Pré-validação sem efeitos colaterais. Retorna se ativação é teoricamente permitida.

**Exemplo:**

```gdscript
if ability.can_activate_ability(owner, spec):
    ability.activate_ability(owner, spec)
else:
    print("Faltam recursos ou não pode ativar")
```gdscript

## `activate_ability(owner: ASComponent, spec: ASAbilitySpec = null, target_node: Object = null) → void`

Inicia execução. Aplica custos e cooldown automaticamente. **Uso de infraestrutura**—prefer `try_activate_ability` para gameplay.

## Validações

## `can_afford_costs(owner: ASComponent, spec: ASAbilitySpec = null) → bool` (const)

Verifica se owner tem atributos suficientes para os custos.

## `can_satisfy_requirements(owner: ASComponent, spec: ASAbilitySpec = null) → bool` (const)

Verifica se owner satisfaz requisitos de atributo.

## Cálculos

## `calculate_ability_duration(owner: ASComponent) → float` (const)

Calcula duração final (considerando `ability_use_custom_duration`).

## `apply_costs(owner: ASComponent, spec: ASAbilitySpec = null) → void` (const)

Aplica custos de atributo ao owner. Chamado automaticamente por `activate_ability`.

## Gerenciamento de Custos e Requisitos (Runtime)

## `add_cost(attribute: StringName, amount: float) → void`

Adiciona custo de atributo em runtime.

## `remove_cost(attribute: StringName) → bool`

Remove custo. Retorna `true` se existia.

## `get_cost_amount(attribute: StringName) → float` (const)

Retorna valor do custo para um atributo.

## `add_requirement(attribute: StringName, amount: float) → void`

Adiciona requisito de atributo em runtime.

## `remove_requirement(attribute: StringName) → bool`

Remove requisito. Retorna `true` se existia.

## `get_requirement_amount(attribute: StringName) → float` (const)

Retorna valor mínimo requerido.

## `get_requirement_count() → int` (const)

Retorna total de requisitos.

## Triggers (Automação)

## `add_trigger(tag: StringName, type: int) → void`

Registra ativação automática baseada em evento/tag.

**Parâmetros:**

- `tag`: Tag ou event para trigger
- `type`: `TRIGGER_ON_TAG_ADDED`, `ON_TAG_REMOVED`, ou `ON_EVENT`

**Exemplo:**

```gdscript
# Ativa automaticamente quando "state.on_fire" é adicionado
ability.add_trigger(&"state.on_fire", ASAbility.TRIGGER_ON_TAG_ADDED)

# Ativa quando evento "event.parry_success" dispara
ability.add_trigger(&"event.parry_success", ASAbility.TRIGGER_ON_EVENT)
```gdscript

## Callbacks Virtuais (Para Subclasses)

## `_on_can_activate_ability(owner: Object, spec: RefCounted) → bool` (virtual const)

Override para lógica customizada de validação.

## `_on_activate_ability(owner: Object, spec: RefCounted) → void` (virtual)

Override para lógica customizada de ativação.

## `_on_end_ability(owner: Object, spec: RefCounted) → void` (virtual)

Override para cleanup customizado.

## Encerramento

## `end_ability(owner: ASComponent, spec: ASAbilitySpec = null) → void`

Encerra execução e limpa owned tags.

## Casos de Uso

## Ability de Combate Simples

```gdscript
var slash = ASAbility.new()
slash.ability_name = "Slash"
slash.ability_tag = &"ability.slash"

# Duração instant
slash.ability_duration_policy = ASAbility.POLICY_INSTANT

# Sem custo (melee)
# Cooldown 1s
slash.cooldown_duration = 1.0

# Não pode atacar se atordoado
slash.activation_blocked_any_tags.append(&"state.stunned")

# Adiciona "state.attacking" enquanto ativa
slash.activation_owned_tags.append(&"state.attacking")

# Aplica efeito de dano
slash.effects.append(damage_effect)
```gdscript

## Ability com Custo e Requisito

```gdscript
var fireball = ASAbility.new()
fireball.ability_name = "Fireball"
fireball.ability_tag = &"ability.fireball"
fireball.ability_duration_policy = ASAbility.POLICY_INSTANT

# Custa 30 Mana
fireball.add_cost(&"mana", 30.0)

# Requer 50 Intelligence
fireball.add_requirement(&"intelligence", 50.0)

# Cooldown 3s
fireball.cooldown_duration = 3.0

# Dispara evento ao ativar
fireball.events_on_activate.append(&"event.fireball_cast")
```gdscript

## Ability com Fases

```gdscript
var charged_strike = ASAbility.new()
charged_strike.ability_name = "Charged Strike"
charged_strike.ability_duration_policy = ASAbility.POLICY_DURATION
charged_strike.ability_duration = 0.5  # Total: 500ms

# Fase 1: Windup (200ms)
var windup = ASAbilityPhase.new()
windup.phase_duration = 0.2
windup.granted_tags.append(&"state.charging")
charged_strike.phases.append(windup)

# Fase 2: Execution (50ms, aplica dano)
var execution = ASAbilityPhase.new()
execution.phase_duration = 0.05
execution.effects.append(heavy_damage_effect)
charged_strike.phases.append(execution)

# Fase 3: Recovery (250ms)
var recovery = ASAbilityPhase.new()
recovery.phase_duration = 0.25
# Sem tags—estado normal
charged_strike.phases.append(recovery)
```gdscript

## Trigger Reativo (Counter-Attack)

```gdscript
var parry = ASAbility.new()
parry.ability_name = "Parry"
parry.ability_tag = &"ability.parry"

# Ativa automaticamente quando "state.hit" é adicionado nos últimos 0.5s
parry.add_trigger(&"event.incoming_damage", ASAbility.TRIGGER_ON_EVENT)
parry.ability_duration_policy = ASAbility.POLICY_DURATION
parry.ability_duration = 0.3

# Cancela outras abilities ao ativar (executa defesa)
parry.activation_cancel_tags.append(&"ability.attack")

# Aplica invulnerabilidade durante parry
parry.granted_tags.append(&"state.parrying")
```gdscript

## Referências Relacionadas

- [ASAbilitySpec](../refcounted/asabilityspec.md) — Instância em execução
- [ASEffect](aseffect.md) — Effects aplicados por esta ability
- [ASAbilityPhase](asabilityphase.md) — Fases granulares
- [ASComponent](../nodes/ascomponent.md) — Owner que executa

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
