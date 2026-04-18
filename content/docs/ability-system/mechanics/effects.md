---
title: "Effects: Modificadores de Estado"
type: docs
weight: 2
---

{{< lang-toggle >}}

Os **Effects** (`ASEffect`) são os agentes de mudança. Tudo que altera um atributo ou adiciona uma tag por um tempo
determinado é um efeito.

## 🕒 Políticas de Duração

- **INSTANT**: Aplica-se em um frame e some (ex: Dano Direto, Cura).
- **DURATION**: Dura um tempo fixo (ex: Buff de Força por 5s).
- **INFINITE**: Persiste até ser removido manualmente ou por outra lógica (ex: Aura de Veneno).

---

## 🥞 Stacking (Empilhamento)

Como o sistema lida quando você aplica o mesmo "Veneno" duas vezes?

1. **STACK_NEW_INSTANCE**: Cada aplicação é independente (dois timers rodando).
2. **STACK_OVERRIDE**: A nova aplicação reseta o tempo da antiga.
3. **STACK_INTENSITY**: Aumenta o "nível" ou magnitude (ex: Veneno x1 -> Veneno x2).
4. **STACK_DURATION**: Soma a duração da nova à restante da antiga.

---

## 💓 Modificadores e Operações

Um efeito pode conter múltiplos modificadores que agem sobre atributos diferentes:

| Operação        | Descrição                                                     |
| :-------------- | :------------------------------------------------------------ |
| **OP_ADD**      | Soma o valor à base (ex: +10 de Vida).                        |
| **OP_MULTIPLY** | Multiplica o valor (ex: x1.5 de Dano).                        |
| **OP_OVERRIDE** | Ignora a base e fixa um valor (ex: Morfou -> Velocidade = 0). |

### Periodicidade (Ticking)

Efeitos de duração podem ter um `period`. Isso permite criar efeitos de DoT (Damage over Time) ou HoT (Heal over Time)
que "ticam" a cada X segundos.

---

## 🎨 Granted Tags

Efeitos são o principal meio de aplicar **Tags CONDITIONAL**. Se você está sob o efeito "Congelado", o efeito te concede
a tag `state.frozen`. Assim que o efeito expira, a tag é removida automaticamente pelo sistema de **RefCount**.
