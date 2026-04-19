---
title: "Classes"
date: "2026-04-18T22:30:00-03:00"
slug: classes
tags:
  - zyris-engine
  - godot-plugin
  - ability-system
  - gamedev
draft: false
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}}

Bem-vindo à referência técnica do **Ability System**. Esta seção contém o detalhamento de todas as classes, estruturas e utilitários disponíveis no framework.

## Categorias Técnicas

### [Singleton](singleton/)

O ponto de entrada global para o sistema. Gerencia o registro de tags e a resolução de componentes em runtime.

### [Resources](resources/)

Blueprints e Definições de Dados. Aqui você define o "DNA" das habilidades, efeitos e atributos (Resources do Godot).

### [Nodes](nodes/)

Componentes de cena. Os blocos de construção que você anexa aos seus personagens e objetos no editor.

### [RefCounted](refcounted/)

Instâncias de execução leves. Objetos que gerenciam o estado mutável durante o gameplay (Specs e Utilitários).

### [Behavior Tree](behavior-tree/)

Nós de IA integrados. Tarefas e condições para o LimboAI que permitem que agentes utilizem o sistema naturalmente.

### [Editor](editor/)

Extensões do editor Godot. Ferramentas que facilitam a vida do designer no dia a dia.

---

Para começar, recomendamos a leitura da classe principal: [**AbilitySystem (Singleton)**](singleton/ability-system).
