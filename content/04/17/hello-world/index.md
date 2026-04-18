---
title: "Olá Mundo!"
date: "2026-04-17T15:00:00-03:00"
slug: hello-world
tags:
  - introducao
  - pessoal
  - trajetoria
draft: false
---

Olá mundo! Sou o Bruno, e decidi que este blog seria mais do que um diário; seria o porto seguro para a documentação e
evolução dos sistemas que venho construindo. Minha jornada começou em 2020 com Java, passou pelo GameMaker e se
consolidou na Godot Engine, mas hoje meu foco está na interseção entre **Engenharia de Engines** e **Agentes de IA**.

Abaixo, detalho os três pilares que definem meu trabalho atual:

### 1. Zyris Engine: O Próximo Nível da Godot

A **Zyris** não é apenas um fork; é uma visão **opinada** de como o desenvolvimento de jogos profissionais deve ser.
Enquanto a Godot preza pela liberdade absoluta, a Zyris foca em **estabilidade e convenção**.

- **Arquitetura Core**: Implementamos um **Save Server** nativo em C++ que utiliza compressão **ZSTD** e criptografia
  **AES-256** em threads dedicadas, garantindo que o gameplay nunca sofra _stutter_ durante persistência de dados.
- **Input System**: O **Virtual Input Devices** abstrai a complexidade de mapeamento multi-plataforma diretamente no
  núcleo, oferecendo uma camada de tradução determinística para Joysticks e D-Pads.
- [**Leia mais sobre a Zyris Engine aqui**](../zyris-engine/)

### 2. Ability System: Gameplay Orientado a Dados

Nascido como um módulo para a Zyris, o **Ability System (AS)** é um framework de gameplay de alta performance que escala
de micro-projetos a RPGs massivos.

- **Dual Build**: Disponível tanto nativamente na Zyris quanto via **GDExtension** para Godot 4.x oficial.
- **Tags Hierárquicas**: Utilizamos um sistema rigoroso de Tags (`NAME`, `CONDITIONAL`, `EVENT`) para orquestrar estados
  de combate sem código "espaguete".
- **Lógica de Fases**: Suporte nativo para fases de habilidade (Windup, Execution, Recovery) e buffers circulares
  prontos para **Multiplayer com Rollback**.
- [**Explore o Ability System detalhadamente**](../ability-system/)

### 3. Vectora: O Motor de Conhecimento Contextual

O **Vectora** é o meu projeto mais ambicioso no campo da IA. Ele não é um "chat" genérico; é um **Sub-Agent Especialista
(Tier 2)** projetado para conectar o contexto do seu código aos agentes principais (como Claude Code ou Gemini CLI).

- **Runtime**: Construído em **TypeScript/Node.js 20+**, integrando os protocolos **MCP** e **ACP**.
- **Context Engine**: Diferente do RAG tradicional, o Vectora realiza **raciocínio multi-hop** e análise estrutural (via
  **Tree-sitter**) para entender como funções e dependências se conectam globalmente.
- **Validação com Harness**: Criamos o **Vectora Harness**, um sistema de métricas objetivas que prova (através de
  scores de precisão e eficiência de tokens) como o contexto entregue melhora a performance da IA.
- **Segurança**: O **Hard-Coded Guardian** protege segredos (.env, .keys) diretamente no runtime, garantindo que dados
  sensíveis nunca saiam do seu ambiente.
- [**Entenda a arquitetura do Vectora**](../vectora/)

---

Tudo isso acontece enquanto concilio o desenvolvimento com minha realidade fora das telas. Já fui balconista, garçom e
hoje trabalho em uma padaria. Essa dualidade entre "massa e código" é o que me mantém com os pés no chão e a cabeça
focada em criar ferramentas que realmente resolvam problemas reais de engenharia.

Este blog é o início dessa nova fase de publicação técnica. Bem-vindos ao MachiOnCoffee.
