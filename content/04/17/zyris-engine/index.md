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

Bem-vindos à **Zyris Engine**. Este projeto não é apenas um fork da Godot; é uma declaração de intenção sobre como manter uma arquitetura de jogo profissional, estável e escalável em longo prazo.

## Uma Filosofia Opinada (Convention over Configuration)

Enquanto a Godot Engine preza pela flexibilidade máxima — muitas vezes permitindo que projetos cresçam de forma caótica — a Zyris adota a filosofia **"opinada"**. Acreditamos que o tempo do desenvolvedor deve ser gasto criando gameplay, não reinventando sistemas fundamentais.

No Zyris, estabelecemos padrões arquiteturais claros. Se você está construindo um projeto profissional, a engine espera certas estruturas, o que facilita o trabalho em equipe e a manutenção de codebases legados.

## Engenharia no Núcleo (Core Features)

Diferente de plugins convencionais, a Zyris integra funcionalidades críticas diretamente no seu núcleo em C++:

### Save Server Determinístico
Implementamos um subsistema de persistência de alta performance que opera em threads dedicadas.
- **Performance**: Zero bloqueio do loop principal de gameplay.
- **Compressão**: Utiliza algoritmos **ZSTD** de última geração para reduzir drasticamente o tamanho dos arquivos.
- **Segurança**: Criptografia nativa **AES-256** integrada ao fluxo de escrita.

### Virtual Input Devices
Uma camada de abstração que permite tratar entradas físicas de qualquer plataforma (Joysticks, D-Pads, Touch) como eventos virtuais consistentes. Isso remove a necessidade de mapeamentos complexos repetitivos em cada novo projeto.

### AOT Export System
Estamos desenvolvendo um sistema de exportação **Ahead-of-Time (AOT)** que gera binários nativos otimizados para cada plataforma alvo, removendo o overhead da máquina virtual e garantindo performance máxima em dispositivos de hardware limitado.

## O Roadmap de Maturidade

A Zyris evolui focada em ferramentas de produção:
- **Behavior Tree Integrada**: Fluxos de IA reativos via grafos de nós nativos.
- **Camera System (vCam)**: Arbitragem de câmeras cinematográficas inspirada em padrões da indústria (Cinemachine).
- **Inventory System Autoritatitvo**: Gestão de itens integrada ao core com suporte nativo a redes.

O Zyris é a escolha para desenvolvedores que entendem que **liberdade sem estrutura é apenas dívida técnica.**

---
*Mantenha-se informado sobre o desenvolvimento nos canais da [Machi](https://www.youtube.com/@machiatodev) e do [Alen](https://www.youtube.com/@yatsuragames).*
