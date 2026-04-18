---
title: "Matriz de Identidade: Tags"
type: docs
weight: 1
---

{{< lang-toggle >}}

No Zyris Ability System, as **Tags** não são apenas labels; elas são a verdade absoluta sobre o estado do seu jogo. Elas
formam a **Matriz de Identidade** de um Ator.

## 🏷️ O Que São Tags?

Tags são identificadores hierárquicos baseados em `StringName` (ex: `state.stunned`, `ability.warrior.powerhit`). Elas
permitem consultas de alta performance e organização visual automática em árvore.

## Os 3 Tipos Canônicos

Para garantir a governança, as tags são divididas em tipos obrigatórios:

| Tipo          | Papel Semântico     | Restrição de Uso                                                          |
| :------------ | :------------------ | :------------------------------------------------------------------------ |
| `NAME`        | **Quem eu Sou**     | Usado exclusivamente para identificar Recursos (`ASAbility`/`ASEffect`).  |
| `CONDITIONAL` | **Como eu Estou**   | Usado para Portões Lógicos (`Required`/`Blocked`). Persistem no RefCount. |
| `EVENT`       | **O que Aconteceu** | Ocorrências instantâneas (1 tick). Usado para despacho de eventos.        |

---

## 🏛️ Hierarquia e Grupos

As tags usam pontos (`.`) para definir ancestrais. Se um ator possui a tag `state.stunned.frozen`, ele tecnicamente
também possui `state.stunned` e `state`. Isso permite verificações amplas:

```gdscript
# Retorna true se o alvo estiver de alguma forma atordoado
ASTagUtils.has_tag(target, "state.stunned")
```gdscript

---

## 🕒 Memória Temporal (Histórico)

O `ASComponent` mantém buffers circulares de **128 entradas** para rastrear o passado recente:

- **NAME History**: Quando identidades foram adicionadas/removidas.
- **CONDITIONAL History**: Mudanças em permissões e imunidades.
- **EVENT History**: O que aconteceu nos últimos frames (magnitude, instigador).

## Exemplo de Reatividade

Habilidades de contra-ataque podem perguntar: _"Ocorreu um evento de bloqueio nos últimos 0.4 segundos?"_

```cpp
ASTagUtils::event_did_occur("event.damage.block", target, 0.4f);
```gdscript

---

## ⚖️ Regras de Ouro (Segurança)

1. **Nunca use tags NAME para lógica**: Tentar bloquear uma habilidade usando uma tag `NAME` é uma violação de
   segurança. A lógica deve depender apenas de tags `CONDITIONAL`.
2. **Registro no Singleton**: Todas as tags (exceto payloads de eventos) devem ser registradas no singleton global para
   garantir autocompletar e evitar erros de digitação.
3. **Dispatch de Eventos**: Nunca dispare um evento cujo nome não esteja registrado com o tipo `EVENT`.
