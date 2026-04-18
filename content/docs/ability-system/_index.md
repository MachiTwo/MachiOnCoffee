---
title: "Ability System"
date: "2026-04-17T18:00:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

O **Ability System (AS)** é um framework poderoso e modular para criação de combate, habilidades e atributos em Godot
4.x. Projetado para escalar desde mecânicas simples até sistemas complexos de RPG — tudo com alta performance em C++ e
arquitetura baseada em dados (v0.1.0 Stable).

## 🛡️ Princípios Arquiteturais

- **SSOT (Single Source of Truth)**: Estado do ator = suas **Tags** (identificadores hierárquicos)
- **Desacoplamento Total**: ASComponent orquestra sem conhecer lógica interna de Specs
- **Type-Safety**: Tags registradas globalmente previnem typos (autocomplete no editor)
- **Determinismo**: Multiplayer nativo com predição cliente e rollback automático
- **Performance**: Flyweight pattern—atores compartilham blueprints imutáveis

## 🏗️ 3 Pilares Arquiteturais

### 1. **Tags** — A Matriz de Identidade

Identificadores hierárquicos (`StringName`) que representam verdade absoluta do estado:

| Tipo            | Semântica              | Uso                       | Exemplo                             |
| --------------- | ---------------------- | ------------------------- | ----------------------------------- |
| **NAME**        | Identidade estática    | Identificador de Resource | `class.warrior`, `ability.fireball` |
| **CONDITIONAL** | Estado persistente     | Requisitos/Bloqueios      | `state.stunned`, `immune.fire`      |
| **EVENT**       | Ocorrência instantânea | Despacho transiente       | `event.damage`, `event.hit`         |

**Regra de Ouro**: NAME identifica. CONDITIONAL bloqueia. EVENT dispara. Nunca misturar.

### 2. **Blueprints** — O "DNA" Imutável

Resources estáticos (`.tres`) compartilhados entre centenas de instâncias:

| Classe             | Propósito                                      | Acessar por                       |
| ------------------ | ---------------------------------------------- | --------------------------------- |
| **ASAbility**      | Define ação (custos, cooldown, triggers)       | `try_activate_ability_by_tag()`   |
| **ASEffect**       | Modificador de estado (duração, stacks, mods)  | `apply_effect_by_tag()`           |
| **ASAttributeSet** | Esquema de stats (HP, Mana, Força)             | Atribuído ao Container            |
| **ASContainer**    | Arquétipo completo (abilities, effects, stats) | `apply_container()`               |
| **ASPackage**      | Envelope de entrega (effects + cues)           | `apply_package()` via ASDelivery  |
| **ASCue**          | Feedback audiovisual                           | Emitido automaticamente por Specs |

### 3. **Specs** — Instâncias de Runtime

Leves, dinâmicas, mantêm estado mutável:

- **ASAbilitySpec**: Habilidade executando (cooldown, fase atual)
- **ASEffectSpec**: Efeito ativo (duração restante, stacks, nível)
- **ASCueSpec**: Feedback tocando (lifecycle gerenciado)
- **ASTagSpec**: Refcount de tag (garante cleanup automático)
- **ASStateCache**: Buffer circular (128 ticks) para rollback multiplayer

## 🔄 Fluxo Essencial (A Ordem Natural)

```
INPUT (jogador pressiona "atacar")
  ↓
TRIGGER (tag adicionada / evento disparado)
  ↓
ESCUTA (try_activate_ability_by_tag(&"ability.slash"))
  ↓
VALIDAÇÃO (can_activate_ability → tags, custos, cooldown)
  ↓ [Se passou]
MUTAÇÃO (activate_ability → aplica efeitos, tags owned, cooldowns)
  ↓
SINAIS (ability_activated, effect_applied, tag_changed)
  ↓
FEEDBACK (Cues—animação, som, partículas)
```

## 📚 Categorias de API

### [🔐 Singleton](singleton/) — Registro Global

- **AbilitySystem**: Registro central de tags, resolutor de componentes

### [📦 Resources](resources/) — Blueprints Imutáveis

- **ASAbility**: Lógica de ação com fases, custos, cooldowns, triggers
- **ASAbilityPhase**: Fases granulares (Windup → Execution → Recovery)
- **ASEffect**: Modificadores com duração, empilhamento, requisitos
- **ASAttribute**: Metadados de stat (min, max, drivers)
- **ASAttributeSet**: Coleção de stats de um ator
- **ASContainer**: Arquétipo (abilities, effects iniciais, attribute set)
- **ASPackage**: Envelope de entrega (effects + cues)
- **ASCue**: Base de feedback (AnimationPlayer, Audio, Partículas)

### [🎬 Nodes](nodes/) — Componentes de Cena

- **ASComponent**: Hub orquestrador (abilities, effects, atributos, tags)
- **ASDelivery**: Injetor de física (projéteis, AoEs)

### [⚙️ RefCounted](refcounted/) — Instâncias Leves

- **ASAbilitySpec**, **ASEffectSpec**, **ASCueSpec**: Executores de runtime
- **ASTagSpec**: Refcount de tags
- **ASStateCache**: Buffer rollback (128 ticks)
- **ASStateSnapshot**: Persistência estado para multiplayer/saves
- **ASTagUtils**: Utilitários tag-histórico (was_added, did_occur, etc)
- **ASStateUtils**: Utilitários estado

### [🎮 Behavior Tree](behavior-tree/) — Integração IA

- **BTActionAS_ActivateAbility**: Ativar via behavior tree
- **BTActionAS_DispatchEvent**: Disparar evento
- **BTConditionAS_CanActivate**: Verificar se pode ativar
- **BTConditionAS_HasTag**, **BTConditionAS_EventOccurred**: Condições

### [✏️ Editor](editor/) — Ferramentas de Edição

- **ASEditorPlugin**: Bootloader
- **ASInspectorPlugin**: Seletores inteligentes (dropdowns de tags)
- **ASTagsPanel**: Interface visual para gerenciar tags globais

## ⚡ Padrões de API (Crítico)

### Nomenclatura Gameplay (Público)

- `try_activate_...`: Ativação segura (verifica requisitos, aplica custos)
- `can_...`: Pré-autorização sem efeitos colaterais
- `is_...` / `has_...`: Consultas de estado
- `get_...`: Leitura segura
- `request_...`: Intenção em rede (RPC multiplayer)
- `cancel_...`: Interrupção voluntária

### Nomenclatura Infraestrutura (Privado)

- `apply_...`: Força aplicação (ignora validações)
- `add_...` / `remove_...`: Mutação baixo nível
- `unlock_...` / `lock_...`: Gestão inventário
- `set_...`: Mutação direta
- `capture_...`: Persistência snapshot

> **NUNCA** use `activate` direto. Sempre `try_activate_ability_by_tag()`.

## 🏷️ System de Tags: Segurança v0.2.0

Cada tag é **registrada globalmente** com tipo obrigatório:

```gdscript
AbilitySystem.register_tag(&"ability.fireball", AbilitySystem.ASTagType.NAME)
AbilitySystem.register_tag(&"state.burning", AbilitySystem.ASTagType.CONDITIONAL)
AbilitySystem.register_tag(&"event.damage", AbilitySystem.ASTagType.EVENT)
```

**Inspector garante type-safety**:

- Campo de "required_tags" recusa NAME tags
- Campo de "ability_name" recusa CONDITIONAL tags
- Campo de "event_dispatch" recusa tudo exceto EVENT

**Hierarquia automática** (pontos criam ramos):

```
state.stunned
state.burning    → agrupa visualmente sob "state"
state.frozen
```

Consultas funcionam em qualquer nível:

```gdscript
has_tag(&"state.stunned")  # específico
has_tag(&"state")           # qualquer sub-state
```

## 🔗 Multiplayer: Predição & Rollback

Construído nativamente para determinismo online:

**Client Prediction:**

```gdscript
asc.capture_snapshot()                          # Estado pre-pred
asc.try_activate_ability_by_tag(&"ability.hit")  # Executa local
asc.request_activate_ability.rpc_id(1, tag)    # Informa server
```

**Server Reconciliation:**

```gdscript
if asc.can_activate_ability_by_tag(tag):
    asc.try_activate_ability_by_tag(tag)
    asc.confirm_ability_activation.rpc(tag)    # Confirma client
else:
    # Predição falhou—client vai rollback
```

**Automatic Rollback:**

```gdscript
asc.apply_snapshot(tick_id)  # Restaura de ASStateCache (128 ticks)
```

ASStateCache mantém buffer automático em `_physics_process`, permitindo rollback instantâneo sem alocação.

## 📊 Sistema de Atributos

Cada ator = **ASAttributeSet** único (deep-cloned):

```gdscript
asc.set_attribute_base_value(&"health", 100.0)
effect.add_modifier(&"health", ASEffect.OP_MULTIPLY, 0.5)  # Reduz 50%
var hp = asc.get_attribute_current_value(&"health")        # 50.0
```

**Drivers** (Attribute Derivation):

```gdscript
attribute_set.add_driver(&"health", &"strength", ASAttributeSet.DRIVER_MULTIPLY, 2.0)
# Health base = 2 * Strength (recalcula automaticamente)
```

## 🎬 Ability Phases (Máquinas de Estado)

Habilidades complexas divididas em fases:

```
Windup [200ms, Slow tag]
  ↓ (advancement por tempo)
Execution [50ms, Apply damage]
  ↓ (advancement por evento: animation_finished)
Recovery [300ms, Normal speed]
```

Cada fase: duração própria, effects transitórios, triggers de avanço.

## 🎮 Integração IA (LimboAI)

Behavior Trees nativos controlam abilities:

```gdscript
BTActionAS_ActivateAbility
  ability_tag: &"ability.slash"
  resolve_mode: BY_TAG

BTConditionAS_HasTag
  tag: &"state.stunned"
  expect_true: false  # Pode atacar se NÃO atordoado
```

**ASBridge** (pasta `src/bridge/`) = camada de tradução nativa LimboAI → ASComponent.

## 📖 Referências Rápidas

- [AbilitySystem](singleton/ability-system.md) — Registro global, resolutor
- [ASComponent](nodes/ascomponent.md) — Hub orquestrador
- [ASAbility](resources/asability.md) — Lógica de ação
- [ASEffect](resources/aseffect.md) — Modificador estado
- [ASContainer](resources/ascontainer.md) — Arquétipo ator
- [ASAbilitySpec](refcounted/asabilityspec.md) — Instância ability
- [ASStateCache](refcounted/asstatecache.md) — Rollback multiplayer

## 🚀 Quick Start

1. Abrir **Ability System Tags** panel (Editor abaixo)
2. Registrar tags: `ability.fireball`, `state.burning`, `event.damage`
3. Criar **AttributeSet**: Health (0–100), Mana (0–50)
4. Criar **ASAbility**: cost 20 Mana, cooldown 2s
5. Criar **ASEffect**: +50 damage, apply `state.burning`
6. Criar **ASContainer**: atribua AttributeSet, abilities, effects
7. Adicionar **ASComponent** ao personagem, atribua Container
8. Usar `asc.try_activate_ability_by_tag(&"ability.fireball")`

---

**v0.1.0 Stable | Godot 4.6+ | Desenvolvido com ❤️ por MachiTwo**
