---
title: "ASComponent: O Hub Central"
type: docs
weight: 1
---

O **ASComponent** (ASC) é o cérebro do sistema de habilidades dentro da sua cena. Ele é o orquestrador que conecta
Atributos, Tags e Habilidades a um Ator.

## 🧠 Papel e Responsabilidade

O ASC não contém a lógica de "como" uma espada corta; ele contém a lista de "quais" habilidades este personagem pode
usar e gerencia o estado delas.

- **Gestor de Coleções**: Mantém a lista de `active_specs` (em execução) e `unlocked_specs` (conhecidas).
- **Dono do Estado**: É o único que pode adicionar/remover tags de forma definitiva.
- **Autoridade de Atributos**: Contém o `ASAttributeSet` e processa todas as modificações de status.

---

## 🛰️ Networking: Predição e Rollback

O ASC foi construído do zero para multiplayer autoritativo:

### ASStateCache

Mantém um buffer circular leve dos últimos **128 ticks**.

- **Predição**: O cliente executa a habilidade localmente e guarda o resultado.
- **Rollback**: Se o servidor discordar do resultado de um tick, o ASC reverte seu estado inteiro via `ASStateSnapshot`
  e re-simula os frames necessários.

---

## 🛠️ Métodos Principais

| Método                 | Intenção              | Descrição                                                             |
| :--------------------- | :-------------------- | :-------------------------------------------------------------------- |
| `try_activate_ability` | **Execução Segura**   | Tenta ativar uma habilidade checando todos os custos e tags.          |
| `apply_effect_to_self` | **Mutação Direta**    | Injeta um `ASEffect` diretamente no componente.                       |
| `dispatch_event`       | **Reatividade**       | Emite uma ocorrência de frame (Tag tipo EVENT).                       |
| `resolve_component`    | **Busca Inteligente** | Método estático para localizar um ASC em uma árvore de cena complexa. |

---

## 🔒 Segurança Hard-Coded: Guardian

Localizado dentro do ASC, o **Guardian** é um middleware que impede:

- Leitura de arquivos sensíveis por agentes de IA.
- Acesso a namespaces de outros projetos.
- Modificações de estado em ticks inválidos.

> [!IMPORTANT] O ASC nunca deve ser acessado diretamente para mutação manual de variáveis. Use sempre a API de `try_` ou
> `request_` para garantir a integridade do Contrato de Governança.
