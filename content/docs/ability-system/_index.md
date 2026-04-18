---
title: "Ability System"
date: "2026-04-17T18:00:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: false
---

{{< lang-toggle >}} O **Zyris Ability System** é um framework robusto de gameplay, desenhado para gerenciar habilidades,
atributos e estados (Tags) de forma profissional e escalável. Inspirado no _Gameplay Ability System (GAS)_ da Unreal,
mas otimizado para a **Zyris Engine** e **Godot**, ele rejeita o "Vibe-Coding" em favor de contratos de engenharia
rigorosos.

## 🛡️ O Contrato de Governança

Diferente de sistemas de habilidades baseados em scripts avulsos, o nosso framework opera sob uma **Lei de Ferro**:

- **SSOT (Single Source of Truth)**: O estado do ator é definido exclusivamente por suas **Tags**.
- **Desacoplamento Total**: O Componente (ASC) não conhece a lógica interna das habilidades (Specs); ele apenas
  orquestra sua execução.
- **Rigor Técnico**: Nenhuma lógica de negócio existe sem um teste que a justifique (Protocolo TDD).

## 🏗️ Estrutura do Sistema

A documentação está dividida em pilares fundamentais:

- [**Core (O Coração)**](./core/) - Componentes, Containers e o Singleton.
- [**Mecânicas (A Lógica)**](./mechanics/) - Como criar Habilidades, Efeitos e Atributos.
- [**Infraestrutura (A Rede)**](./infrastructure/) - Sistema de Tags, Cues e Regras de Negócio.
- [**Integração (IA)**](./integration/) - Como conectar com LimboAI via ASBridge.

---

### Por onde começar?

Se você é novo no sistema, recomendamos ler primeiro sobre a [**Matriz de Identidade: Tags**](./infrastructure/tags/),
que é a base de todo o fluxo de lógica do jogo.
