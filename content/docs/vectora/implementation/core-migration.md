---
title: Migração do Núcleo
slug: core-migration
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - engineering
  - golang
  - migration
  - performance
---

{{< lang-toggle >}}
{{< section-toggle >}}

## Migração do Núcleo (TS para Go)

A transição do Vectora de **TypeScript (Node.js)** para **Golang** não foi apenas uma troca de linguagem, mas uma reengenharia completa para atender aos requisitos de performance e distribuição nativa. Este documento detalha as motivações técnicas e as mudanças estruturais.

### Por que Golang?

| Fator              | TypeScript (Node.js)              | Golang                          | Impacto no Vectora                           |
| :----------------- | :-------------------------------- | :------------------------------ | :------------------------------------------- |
| **Distribuição**   | Requer Node.js instalado (+100MB) | Binário Estático Único (~20MB)  | Instalação via Winget sem dependências.      |
| **Concorrência**   | Event Loop (Single-threaded)      | Goroutines (Nativo/Paralelo)    | Processamento de RAG 3x mais rápido.         |
| **Consumo Memory** | Alto (V8 Garbage Collector)       | Baixo (Gerenciamento Eficiente) | Menor pegada em máquinas de desenvolvedores. |
| **Segurança**      | Tipagem em tempo de escrita       | Tipagem forte compilada         | Menos erros de runtime em produção.          |

### Mudanças Estruturais Core

#### 1. De Zod para Struct Tags

Na versão legado, usávamos **Zod** para validar schemas em tempo real. No Go, utilizamos `structs` nativas com tags de validação (`validate:"required"`), o que reduz o overhead de parsing e garante que o binário rejeite inputs malformados antes mesmo da execução lógica.

#### 2. Harness Runtime Nátivo

O **Harness Runtime**, que antes dependia de pontes assíncronas no Node, agora opera diretamente no sistema de arquivos e rede do OS. Isso permite que interceptações do [Guardian](../security-engine.md) sejam feitas em nível de kernel-space simulado, aumentando a confiabilidade da sandbox.

#### 3. Concorrência no Context Engine

O pipeline de `Embed → Search → Rerank` agora é orquestrado via `Channels` e `Contexts` do Go. Enquanto o Node processava um chunk por vez, o motor em Go dispara múltiplas requisições paralelas para o MongoDB Atlas e Voyage AI, reduzindo a latência total da resposta MCP.

### Desafios da Migração

- **Interoperabilidade MCP**: Manter a conformidade com o protocolo MCP (JSON-RPC) enquanto migrávamos de bibliotecas Node para implementações nativas em Go.
- **Distribuição de Binários**: Configurar o pipeline de build multiplataforma (Windows/macOS/Linux) para garantir que o comportamento do sub-agent seja idêntico em todos os SOs.

---

_Parte do ecossistema Vectora_ · Engenharia Interna
