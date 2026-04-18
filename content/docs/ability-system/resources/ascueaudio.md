---
title: "ASCueAudio"
date: "2026-04-18T12:00:00-03:00"
type: docs
---


**Badge:** `Resource` • `ASCue`

## Descrição Breve

Cue especializado para reproduzir áudio durante execução de abilities.

## Descrição Completa

`ASCueAudio` é um feedback sonoro que executa um `AudioStream` em resposta a eventos do Ability System. Integra-se automaticamente com `AudioStreamPlayer`, `AudioStreamPlayer2D` e `AudioStreamPlayer3D` registrados no `ASComponent`.

Crie um resource `.tres` do tipo `ASCueAudio`, atribua um `AudioStream` (.wav, .ogg, .mp3), e adicione à lista `cues` de qualquer `ASAbility` ou `ASEffect`. Quando o trigger ocorre, o áudio toca automaticamente.

**Fluxo de Execução:**

1. Ability/Effect ativa cue trigger
2. ASComponent cria `ASCueSpec` com contexto
3. ASCueAudio busca `AudioStreamPlayer` no registry ou componentes
4. Dispara `play()` com o `audio_stream` configurado

## Herança

```gdscript
Resource
 └─ ASCue
     └─ ASCueAudio
```gdscript

## Propriedades

| Propriedade    | Tipo      | Descrição                                                                  |
| -------------- | --------- | -------------------------------------------------------------------------- |
| `audio_stream` | AudioStream | Som a reproduzir (.wav, .ogg, .mp3)                                       |
| `cue_tag`      | StringName | Identificador da cue — deve ser NAME type                                 |
| `node_name`    | StringName | Alias do nó `AudioStreamPlayer*` no registry (herdado)                     |
| `event_type`   | int        | Trigger: ON_EXECUTE (0), ON_ACTIVE (1), ON_REMOVE (2) (herdado)           |

## Métodos

## Getters

## `get_audio_stream() → AudioStream` (const)

Retorna o AudioStream configurado.

## Setters

## `set_audio_stream(stream: AudioStream) → void`

Define o áudio a ser tocado.

## Comportamento Automático

**Resolução de Nó Alvo:**

Se `node_name` vazio, ASCueAudio tenta nesta ordem:

1. AudioStreamPlayer (3D espacial)
2. AudioStreamPlayer2D (2D espacial)
3. AudioStreamPlayer3D (3D avançado)

Se encontra primeira match, usa aquela instância.

**Segurança:**

- Se nó não encontrado: falha silenciosa
- Se `audio_stream` vazio: pula (sem erro)
- Se player já tocando: interrompe e começa novo

## Casos de Uso

## Som de Ataque

```gdscript
# sword_hit.tres (ASCueAudio)
# cue_tag: "cue.sword_hit"
# audio_stream: res://sounds/sword_hit.ogg
# event_type: ON_EXECUTE

# Na ASAbility:
ability.cues.append(sword_hit_resource)
# Quando ataque executa → som de impacto toca
```gdscript

## Som Contínuo (Habilidade Ativa)

```gdscript
# channeling_loop.tres (ASCueAudio)
# cue_tag: "cue.channeling"
# audio_stream: res://sounds/channeling_loop.ogg
# event_type: ON_ACTIVE

# Na ASAbility:
ability.duration_policy = ASAbility.DURATION
ability.cues.append(channeling_loop_resource)
# Enquanto ability ativa → som toca continuamente
```gdscript

## Som de Cleanup (Effect Removido)

```gdscript
# burn_end.tres (ASCueAudio)
# cue_tag: "cue.burn_end"
# audio_stream: res://sounds/burn_extinguish.wav
# event_type: ON_REMOVE

burn_effect.cues.append(burn_end_resource)
# Quando estado burning removido → som de extinção
```gdscript

## Feedback Auditivo com Variação

```gdscript
# Criar múltiplas cues para variedade
var hit_sound_1 = ASCueAudio.new()
hit_sound_1.audio_stream = load("res://sounds/hit1.ogg")

var hit_sound_2 = ASCueAudio.new()
hit_sound_2.audio_stream = load("res://sounds/hit2.ogg")

var hit_sound_3 = ASCueAudio.new()
hit_sound_3.audio_stream = load("res://sounds/hit3.ogg")

# Aleatoriamente escolher durante ativação (via custom code)
# Ou atribuir diferentes cues a diferentes effects
```gdscript

## Som 3D Espacializado

```gdscript
# Para áudio que varia por distância/direção
# cue_tag: "cue.explosion_3d"
# node_name: "AudioStreamPlayer3D"  # Busca player 3D
# audio_stream: res://sounds/explosion.wav

# ASComponent automaticamente usa AudioStreamPlayer3D se `node_name` vazio
# Som varia por posição relativa do jogador
```gdscript

## Performance

**Muito Leve:** AudioStreamPlayer é nativo Godot—ASCueAudio só dispara `play()`.

**Melhor Prática:** Compartilhe resources de áudio comum:

```gdscript
# ✅ Compartilhado
var footstep_audio = preload("res://sounds/footstep.ogg")
cue1.audio_stream = footstep_audio
cue2.audio_stream = footstep_audio

# Pool de AudioStreamPlayers
# Godot cuida de multiplex automático se múltiplos toques simultâneos
```gdscript

## Integração com ASComponent

```gdscript
asc.try_activate_ability_by_tag(&"ability.fireball")
# → Ability cues disparadas
# → ASCueAudio busca AudioStreamPlayer
# → Som de explosion toca
```gdscript

Conecte a sinais para feedback adicional:

```gdscript
asc.ability_activated.connect(func(spec):
    print("Som já disparado por cue")
)
```gdscript

## Configuração de Stream

**Godot Audio Formats Suportados:**

- `.wav` — Sem compressão, melhor qualidade
- `.ogg` — Comprimido, balanceado qualidade/tamanho
- `.mp3` — Comprimido legacy

**Importação (Editor):**

1. Coloque arquivo em `res://` (ex: `res://sounds/`)
2. Editor auto-detecta formato
3. Configure import settings se necessário (loop, trim silence)
4. Arraste para propriedade `audio_stream` no inspector

## Referências Relacionadas

- [ASCue](ascue.md) — Classe base
- [ASComponent](../nodes/ascomponent.md) — Orquestra cues
- [ASAbility](asability.md) — Define cues
- [ASEffect](aseffect.md) — Effects disparam cues

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
