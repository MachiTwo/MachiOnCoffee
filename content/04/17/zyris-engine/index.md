---
title: "Zyris Engine: Controle, Performance e Opinada por Design"
date: "2026-04-17T16:00:00-03:00"
slug: zyris-engine
tags:
  - engine
  - gamedev
  - zyris
draft: false
---

Olá mundo! Hoje quero apresentar a **Zyris Engine**, um projeto que nasceu da necessidade de **controle estrutural, previsibilidade e escalabilidade** no desenvolvimento de jogos profissionais.

## O que é a Zyris?

A **Zyris** é um **fork da Godot Engine**. Isso significa que ela mantém total compatibilidade com a base da Godot — seus projetos, seu conhecimento em GDScript e o fluxo de trabalho permanecem familiares.

No entanto, a Zyris possui sua própria **governança e roadmap**. Não aplicamos atualizações da Godot cegamente; cada mudança do "upstream" é analisada, filtrada e integrada de forma controlada para garantir a estabilidade de longo prazo.

## Uma Filosofia Opinada

Ao contrário de engines que oferecem liberdade absoluta e podem acabar gerando códigos caóticos, o Zyris é **intencionalmente opinado**. Acreditamos que convenções claras reduzem a necessidade de reinventar soluções fundamentais em cada projeto.

Você ainda tem liberdade total, mas por padrão o Zyris oferece:
- **Estruturas previsíveis** para sistemas complexos.
- **Gerenciamento determinístico de estados**.
- **Base arquitetural consistente** para IA e gameplay.

## Recursos Já Implementados

Atualmente, a engine já conta com sistemas robustos integrados ao seu núcleo:

- **Virtual Input Devices**: Camada de abstração de entrada multi-plataforma (Joysticks, D-Pads) integrada diretamente ao core.
- **Save Server**: Orquestrador de persistência de alta performance com compressão **ZSTD** e criptografia **AES-256**, rodando em threads dedicadas para garantir *autosaves* fluídos.

## O Futuro: Ability System e Mais

Estamos trabalhando na integração nativa do [**Ability System**](../ability-system/), um framework de gameplay orientado a dados para escalar mecânicas de combate.

Nosso roadmap de desenvolvimento ainda inclui:
- **Behavior Tree**: IA modular e reativa baseada em nós.
- **Inventory System**: Gestão autoritativa de itens e equipamentos.
- **Camera System (vCam)**: Arbitragem cinematográfica para transições suaves.
- **AOT Export System**: Geração de binários nativos para máxima performance sem o overhead da VM.

O Zyris é focado em quem busca **maturidade técnica** e longevidade para seus projetos.

---
*Acompanhe o desenvolvimento oficial nos canais da [Machi](https://www.youtube.com/@machiatodev) e do [Alen](https://www.youtube.com/@yatsuragames).*
