---
title: "Ability System: O Coração das Mecânicas de Gameplay no Zyris"
date: "2026-04-17T17:00:00-03:00"
slug: ability-system
tags:
  - gamedev
  - gameplay-system
  - zyris
draft: false
---

O **Ability System (AS)** é um framework poderoso projetado para a criação de combates, habilidades e atributos modulares. Ele foi pensado para escalar desde mecânicas simples até sistemas complexos de RPG, tudo com **alta performance em C++**.

## Arquitetura de Build Dual

Um dos maiores diferenciais deste sistema é a sua flexibilidade de integração, garantindo o melhor dos dois mundos:

- **Nativo (Zyris Engine):** Integrado diretamente ao núcleo da engine, aproveitando a automação centralizada e validação rigorosa do core.
- **Plugin (GDExtension):** Uma versão em biblioteca dinâmica para projetos **Godot 4.x** padrão. Oferece 100% de paridade lógica sem exigir a recompilação do motor.

## Conceitos Chave

O framework introduz conceitos avançados para desacoplar a lógica de jogo:

- **Tags Hierárquicas**: Utiliza identificadores como `NAME` (Identidade), `CONDITIONAL` (Estado persistente) e `EVENT` (Ocorrência instantânea).
- **Ability Phases**: Divida suas habilidades em estágios como `Windup`, `Execution` e `Recovery` de forma nativa.
- **Multiplayer com Rollback**: Projetado para alta performance em rede com **predição no cliente** e reconciliação pelo servidor através de buffers circulares de estado.

## Lógica Orientada a Dados

No **Ability System**, a lógica de jogo é transformada em dados. Isso significa que designers podem projetar mecânicas complexas editando apenas recursos (`.tres`) no editor da Godot:

1. **Defina o Vocabulário**: Crie as Tags que representam o estado do seu jogo.
2. **Crie o Esquema**: Configure o `AttributeSet` com atributos como Saúde, Mana ou Força.
3. **Projete a Habilidade**: Configure custos, cooldowns e requisitos lógicos diretamente no recurso de `Ability`.

## Por que usar?

Ao desacoplar a lógica de **"como um impacto é calculado"** de **"quem causou o impacto"**, o sistema elimina o código "espaguete" e garante uma arquitetura limpa, testável e extremamente performática para projetos de qualquer porte.

---
*Desenvolvido com ❤️ por **MachiTwo**.*
