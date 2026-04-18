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

O **Ability System (AS)** é a espinha dorsal do gameplay de combate. Mais do que gerenciar habilidades, ele oferece um framework orientado a dados para orquestrar estados complexos com **alta performance em C++**.

## Paradigma Orientado a Dados

A grande revolução do AS é mover a lógica de gameplay do código fonte para o **Editor da Godot**. Utilizando recursos (`.tres`), designers podem configurar comportamentos complexos sem recompilações.
- **ASAbitilies**: Definem o "fazer" — custos, cooldowns e requisitos.
- **ASEffects**: Gerenciam a modificação de atributos no tempo (Dano por tempo, Buffs de atributos).
- **ASContainers**: Funcionam como arquétipos que conectam múltiplos efeitos e habilidades a um personagem.

## Hierarquia de Tags: A Linguagem do Estado

O sistema utiliza um vocabulário rigoroso de **Tags Hierárquicas** para comunicação entre sistemas desassociados:
- **$NAME**: Define a identidade única de uma peça de gameplay.
- **$CONDITIONAL**: Representa estados persistentes e lógicos (Ex: `IsStunned`, `IsReloading`).
- **$EVENT**: Gatilhos instantâneos que disparam reações (Ex: `OnDamageTaken`, `OnJump`).

## Lógica de Fases e Fluxo de Gameplay

Uma habilidade no AS não é apenas um "disparo". Ela é dividida em estágios nativos que permitem um controle fino da experiência:
1. **Windup**: O tempo de preparação (telegrafia).
2. **Execution**: Quando a lógica principal e o *hitbox* são ativados.
3. **Recovery**: O cooldown de ação necessário após o uso.

## Engenharia de Rede: Rollback Nativo

Desenvolvido com o multiplayer em mente, o **Ability System** utiliza **buffers circulares de estado**. Isso permite que o sistema suporte **Rollback Networking**, onde o cliente pode prever o estado do jogo e o servidor pode reconciliar erros de predição voltando no tempo e re-executando a lógica de forma determinística.

## Integração Dual Build

Para garantir que ninguém fique para trás, mantemos duas formas de uso:
- **Nativo Zyris**: Máxima integração com as ferramentas core da engine.
- **GDExtension**: Plugin estável para qualquer projeto Godot 4.x oficial, levando o poder do C++ para desenvolvedores GDScript.

---
*Desenvolvido com ❤️ por **MachiTwo**.*
