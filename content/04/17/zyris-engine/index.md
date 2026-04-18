---
title: "Zyris Engine: Controle, Performance e Opinada por Design"
date: "2026-04-17T19:00:00-03:00"
slug: zyris-engine
tags:
  - engine
  - gamedev
  - zyris
draft: false
---

{{< lang-toggle >}}

Bem-vindos à **Zyris Engine**. Este projeto não é apenas um fork da Godot; é uma declaração de intenção sobre como
manter uma arquitetura de jogo profissional, estável e escalável em longo prazo.

## Uma Filosofia Opinada (Convention over Configuration)

Enquanto a Godot Engine preza pela flexibilidade máxima — muitas vezes permitindo que projetos cresçam de forma caótica
— a Zyris adota a filosofia **"opinada"**. Acreditamos que o tempo do desenvolvedor deve ser gasto criando gameplay, não
reinventando sistemas fundamentais.

No Zyris, estabelecemos padrões arquiteturais claros. Se você está construindo um projeto profissional, a engine oferece
estruturas previsíveis que facilitam o trabalho em equipe e a manutenção de codebases complexos.

## Engenharia no Núcleo (Core Features)

Diferente de plugins convencionais, a Zyris integra funcionalidades críticas diretamente no seu núcleo em C++:

### Save Server: Orquestrador de Persistência

Um sistema de persistência robusto e assíncrono integrado ao core.

- **Protocolo Declarativo**: Automação via `@persistent` no GDScript.
- **Threaded Architecture**: Compressão ZSTD e criptografia AES-256 rodando em threads dedicadas.
- **Sistema Incremental**: Rastreia modificações e aplica patches cirúrgicos, reduzindo a escrita em disco em até 95%.

### Virtual Input Devices

Abstração total de entrada. O sistema detecta automaticamente se o jogador está no Toque, Teclado ou Gamepad e adapta a
UI dinamicamente. Inclui nós nativos como `VirtualJoystick` e `VirtualDPad` integrados ao InputMap da Godot.

### Ability System (GAS)

Um framework de gameplay de alto desempenho para RPGs e jogos de combate. Baseado em `Resources` para ser data-driven,
permite que designers criem habilidades complexas (Costs, Cooldowns, Effects) sem tocar em código, com processamento
total em C++.

## O Ecossistema de Produção

A Zyris expande os horizontes da engine base com sistemas pensados para o "EndGame" do desenvolvimento:

### Inventory & Equipment System

Gestão autoritativa de itens com um **Equipment Bridge** que injeta habilidades do GAS automaticamente ao equipar itens.
Inclui nós de UI inteligentes e validação no lado do servidor para evitar trapaças.

### Camera System (vCam)

Arbitragem cinematográfica inspirada no padrão Cinemachine. O `vCamServer` gerencia prioridades entre câmeras virtuais e
realiza transições (blends) suaves, além de possuir um sistema de tremor (Procedural Shake) baseado em ruído de Perlin.

### Audio System Pro

Expansão do sistema de áudio nativo com suporte a áudio baseado em eventos e contexto. Introduz DSP por stream e mixagem
reativa, onde o estado do jogo influencia diretamente o ambiente sonoro.

## Roadmap de Maturidade

O Zyris continua evoluindo com foco em robustez:

- **Behavior Tree Nativa**: IA modular e reativa com editor visual dedicado e live debugging.
- **Multiplayer Update**: Replicação por camadas (Network LOD) e predição autoritativa nativa.
- **Cloud Providers**: Abstração polimórfica para Steam, Epic Online Services (EOS) e PlayFab.

O Zyris é a escolha para desenvolvedores que entendem que **liberdade sem estrutura é apenas dívida técnica.**

---

_Mantenha-se informado sobre o desenvolvimento nos canais da [Machi](https://www.youtube.com/@machiatodev) e do
[Alen](https://www.youtube.com/@yatsuragames)._
