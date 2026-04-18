---
title: "ASDelivery"
date: "2026-04-18T12:00:00-03:00"
type: docs
---

# ASDelivery

**Badge:** `Node`

## Descrição Breve

Node especializado para entrega e injeção de payloads (projéteis, AoEs).

## Descrição Completa

`ASDelivery` é um Node leve projetado para carregar e entregar `ASPackage`s a alvos `ASComponent`. Diferentemente de
`ASComponent`, que é um hub completo, `ASDelivery` é um utilitário que pode ser anexado a qualquer node (como Area2D de
um projétil) para injetar efeitos ao impacto.

Pode ser usado para:

- **Projéteis**: Bolas de fogo que voam e explodem
- **AoEs**: Círculos que aplicam effects a quem entrar
- **Armadilhas**: Perigos passivos que esperam por vítimas
- **Ataques Melee**: Hit boxes temporárias

## Herança

```
Node
 └─ ASDelivery
```

## Propriedades

| Propriedade        | Tipo         | Padrão  | Descrição                                |
| ------------------ | ------------ | ------- | ---------------------------------------- |
| `package`          | ASPackage    | `null`  | O payload a entregar                     |
| `source_component` | ASComponent  | `null`  | Quem originou (atacante)                 |
| `level`            | float        | `1.0`   | Magnitude/força da entrega               |
| `life_span`        | float        | `0.0`   | Duração máxima (0 = infinito)            |
| `is_active`        | bool         | `false` | Estado de ativação                       |
| `auto_connect`     | bool         | `false` | Conectar automaticamente a Area2D/Area3D |
| `one_shot`         | bool         | `false` | Desativar após primeira entrega          |
| `target_groups`    | StringName[] | `[]`    | Grupos que alvos devem pertencer         |

## Métodos Públicos

### Ativação

#### `activate(duration: float = -1.0) → void`

Ativa a entrega. Se `duration` > 0, substitui `life_span`.

**Exemplo:**

```gdscript
delivery.activate()           # Ativa indefinidamente
delivery.activate(5.0)        # Ativa por 5 segundos
```

#### `deactivate() → void`

Desativa a entrega.

### Entrega

#### `deliver(target: Node) → void`

Entrega o payload a um alvo específico.

Automaticamente:

- Encontra ASComponent do target
- Aplica package via `apply_package()`
- Emite events do package
- Emite sinal `delivered`

**Exemplo:**

```gdscript
delivery.deliver(enemy_node)
```

#### `can_deliver_to(target: Node) → bool` (const)

Verifica se pode entregar a um target (valida grupos).

### Validação

#### `is_delivery_valid() → bool` (const)

Retorna se ativa e não expirou.

## Sinais

#### `delivered(target: Object) → void`

Emitido após entrega bem-sucedida.

#### `expired() → void`

Emitido quando `life_span` atinge zero.

## Casos de Uso

### Projétil de Fireball

```gdscript
# Cena: FireballProjectile
#  └─ Area2D
#      └─ ASDelivery
#          └─ CollisionShape2D

func _ready():
    var delivery = $ASDelivery
    delivery.package = fireball_package
    delivery.one_shot = true  # Explodir uma vez
    delivery.auto_connect = true  # Conectar a signals de Area2D
    delivery.activate()  # Ativar

func _physics_process(delta):
    position += velocity * delta
```

### Auto-Connect via Area2D

```gdscript
# Area2D com ASDelivery como child
# Configur ASDelivery no Inspector:
#  - package = FireballPackage
#  - auto_connect = true
#  - one_shot = true

# ASDelivery conecta automaticamente:
# Area2D.area_entered → delivery.deliver(area)
# Sem código necessário!
```

### Armadilha Passiva

```gdscript
# Cena: PoisonTrapTile
#  └─ Area2D (immobile)
#      └─ ASDelivery
#          └─ CollisionShape2D

func _ready():
    var delivery = $ASDelivery
    delivery.package = poison_package
    delivery.is_active = true  # Sempre ativa
    delivery.life_span = 0.0   # Infinito
    delivery.auto_connect = true

# Qualquer thing que entrar recebe poison!
```

### Entrega Manual com Validação

```gdscript
func _on_explosion_triggered(position: Vector2):
    var delivery = ASDelivery.new()
    delivery.package = explosion_package
    delivery.source_component = self.asc
    delivery.level = 2.0  # Explosão forte

    var targets = get_nearby_components(position, 10.0)
    for target in targets:
        if delivery.can_deliver_to(target):
            delivery.deliver(target)
```

### Hit Box Melee Temporário

```gdscript
# Durante animação de ataque
func _on_attack_animation_hit_frame():
    var hit_box = $AttackHitBox
    var delivery = hit_box.get_node("ASDelivery")

    delivery.package = melee_damage_package
    delivery.source_component = asc
    delivery.one_shot = true
    delivery.activate(0.1)  # Ativo por 100ms

    # Colisões durante este tempo entregam damage
```

## Integração com ASComponent

```gdscript
# ASDelivery automaticamente chama:
target_asc.apply_package(
    delivery.package,
    level=delivery.level,
    source_component=delivery.source_component
)

# E emite events do package:
target_asc.dispatch_event(&"event.fireball_hit")
```

## Referências Relacionadas

- [ASPackage](../resources/aspackage.md) — Payload a entregar
- [ASComponent](ascomponent.md) — Alvo que recebe
- [ASEffect](../resources/aseffect.md) — Effects no package
- [ASCue](../resources/ascue.md) — Feedback no package

---

**Parte do Ability System v0.1.0 | Godot 4.6+**
