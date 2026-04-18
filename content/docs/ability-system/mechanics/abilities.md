---
title: "Abilities: Lógica de Gameplay"
type: docs
weight: 1
---

As **Abilities** (`ASAbility`) são os blocos de construção da ação. Elas definem o que um personagem faz, quanto custa e
como ele é impedido de fazê-lo.

## 🧬 Anatomia de uma Ability

Uma habilidade no Zyris System é dividida entre o **Resource** (DNA imutável) e o **Spec** (instância de runtime).

- **Custos**: Modificadores de atributos consumidos no início.
- **Requisitos**: Tags (CONDITIONAL) que devem ou não estar presentes.
- **Cooldown**: Tempo de espera marcado por Tags específicas.

---

## 🎭 Ability Phases (Ciclos Complexos)

Uma das funcionalidades mais poderosas para designers é o sistema de **Fases**. Se uma habilidade padrão é um "click",
uma habilidade com Fases é um "ritual".

Exemplo de um Ataque Pesado:

1. **Windup (0.5s)**: O personagem prepara o golpe. Aplica tag `state.vulnerable`.
2. **Execution**: O golpe ocorre. Dispara `event.damage`.
3. **Recovery (0.3s)**: O personagem se recupera.

### Transições

As fases podem transicionais por **Tempo** (duração fixa) ou por **Evento** (ex: o mestre de animação envia o sinal
`.Hit`).

---

## ⚡ Triggers: Automação Reativa

Habilidades não precisam ser ativadas apenas por botões. Elas podem ser **Reativas**:

- `TRIGGER_ON_TAG_ADDED`: Ativa automaticamente quando o personagem recebe uma tag (ex: "Escudo Ativado" quando entra em
  combate).
- `TRIGGER_ON_EVENT`: Ativa em resposta a uma ocorrência (ex: "Contra-ataque" ao tomar dano).

---

## 💻 Exemplo de Implementação (Virtuals)

Designer define os dados no Inspector, e o programador implementa a lógica:

```cpp
void _on_activate_ability(Object* owner, RefCounted* spec) {
    // Lógica pura de gameplay aqui
    // Os custos e cooldowns já foram tratados pela engine!
}
```

> [!TIP] Use **Sub-Abilities** para criar habilidades compostas que são desbloqueadas em conjunto, mantendo a hierarquia
> limpa.
