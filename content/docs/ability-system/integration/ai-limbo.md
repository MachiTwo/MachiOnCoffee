---
title: "IA: Integração com LimboAI"
type: docs
weight: 1
---

A inteligência artificial na Zyris Engine não opera no vácuo. Ela interage com o **Ability System** através de uma
camada lógica chamada **ASBridge**.

## 🌉 O Que é a Camada ASBridge?

O status v0.2.0 descomissionou o Singleton `ASBridge` em favor de uma integração nativa e atômica. Agora, "Bridge"
refere-se à coleção de:

- **BT Actions**: Tarefas de Behaviour Tree (LimboAI).
- **BT Conditions**: Condições lógicas para galhos da árvore.
- **LimboState**: Estados para máquinas de estado hierárquicas (HSM).

---

## 🚦 A Autoridade de Resolução

O Singleton principal do **AbilitySystem** agora atua como o juiz de referências. As árvores de comportamento usam o
método `resolve_component()` para encontrar o ASC do agente, sem precisar saber onde ele está fisicamente na árvore de
cena.

```cpp
// Exemplo interno das tarefas da Bridge
AbilitySystem::get_singleton()->resolve_component(agente);
```

---

## 🤖 Tarefas Comuns (BTNodes)

| Nodo                         | Descrição                                                                 |
| :--------------------------- | :------------------------------------------------------------------------ |
| `BTActionAS_ActivateAbility` | Envia o comando de ativação para o ASC.                                   |
| `BTConditionAS_HasTag`       | Verifica se o alvo possui uma tag específica para decidir o próximo ramo. |
| `BTConditionAS_CanActivate`  | Pré-checa se a habilidade tem custos e tags para ser usada.               |
| `BTActionAS_DispatchEvent`   | Dispara um evento (ex: `event.ai.spotted`) que pode triggar reações.      |

## 🔄 Sinergia HSM (Máquinas de Estado)

O `ASComponent` interage intimamente com o **LimboHSM**. O estado da máquina de estados do personagem pode ser conduzido
de forma reativa através dos **Events** e **Tags**.

Isso significa que sua IA pode mudar de estado simplesmente porque o Ability System detectou que a tag `state.stunned`
foi adicionada, sem que você precise escrever código de verificação manual em cada frame.

> [!CAUTION] > **Desacoplamento Rigoroso**: Nunca deixe sua IA manipular atributos diretamente. Ela deve sempre "pedir"
> através de habilidades ou efeitos, respeitando o Contrato de Governança.
