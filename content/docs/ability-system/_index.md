---
title: "Ability System"
date: "2026-04-18T22:30:00-03:00"
slug: ability-system
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
  - gameplay-framework
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

O **Ability System (AS)** é um framework poderoso e modular para criação de combate, habilidades e atributos em Godot
4.x. Projetado para escalar desde mecânicas simples até sistemas complexos de RPG — tudo com alta performance em C++ e
arquitetura baseada em dados (v0.1.0 Stable).

## Princípios Arquiteturais

- **SSOT (Single Source of Truth)**: Estado do ator = suas **Tags** (identificador hierárquico)
- **Desacoplamento Total**: ASComponent orquestra sem conhecer lógica interna de Specs
- **Type-Safety**: Tags registradas globalmente previnem typos (autocomplete no editor)
- **Determinismo**: Multiplayer nativo com predição cliente e rollback automático
- **Performance**: Flyweight pattern—atores compartilham blueprints imutáveis

## 3 Pilares Arquiteturais

### 1. **Tags** — A Matriz de Identidade

Identificadores hierárquicos (`StringName`) que representam verdade absoluta do estado.

### 2. **Blueprints** — O "DNA" Imutável

Resources estáticos (`.tres`) compartilhados entre instâncias (ASAbility, ASEffect, etc).

### 3. **Specs** — Instâncias de Runtime

Leves, dinâmicas, mantêm estado mutável (Cooldowns, Stacks, Duração).

---

Explore a documentação técnica completa organizada por categorias:

- [** Singleton**](classes/singleton/) — Registro global e resolutor central.
- [** Resources**](classes/resources/) — Habilidades, Efeitos e Blueprints imutáveis.
- [** Nodes**](classes/nodes/) — Componentes de cena (ASComponent, ASDelivery).
- [** RefCounted**](classes/refcounted/) — Executores de runtime e utilitários de estado.
- [** Behavior Tree**](classes/behavior-tree/) — Integração nativa com LimboAI.
- [** Editor**](classes/editor/) — Painéis de Tags e inspetores customizados.

---

## Tutoriais e Exemplos

Aprenda na prática como implementar o sistema:

- [** Tutoriais**](tutorials/) — Passo a passo para mecânicas comuns.
- [** Exemplos**](examples/) — Projetos de referência e padrões de design.

---

## Status do Projeto

v0.1.0 Stable | Godot 4.6+ | Dual-Build (GDExtension/Module) | Desenvolvido com por MachiTwo
