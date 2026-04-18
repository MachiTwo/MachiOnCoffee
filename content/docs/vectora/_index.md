---
title: "Vectora"
date: "2026-04-17T18:00:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: true
---

{{< lang-toggle >}} ## O Problema

Agentes de IA tradicionais costumam **alucinar** porque operam em contextos fragmentados, sem visão estruturada do
codebase. Uma busca por "função de autenticação" retorna 50 resultados desconexos. O contexto entregue é raso, sem
compreensão de fluxo, dependências ou padrões arquiteturais.

## A Solução: Vectora

O **Vectora** resolve isso não sendo "mais um chat", mas sim um **Motor de Conhecimento Contextual** que funciona como
um **Sub-Agent Tier 2**. Ele não apenas recupera código — ele **entende estrutura, semântica e relações** através de:

- **AST-Aware Parsing**: Análise estrutural usando Tree-sitter, não busca textual
- **RAG Conectado**: Recuperação aumentada que conecta fragmentos em contexto coeso
- **Context Engine**: Decisor inteligente de _o que_, _como_ e _quando_ buscar
- **Reranking Inteligente**: Classifica resultados por relevância semântica, não por frequência

O Vectora nasceu para ser a camada de inteligência que **conecta os pontos**, entregando o que chamamos de
**Conhecimento Conectado** — contexto estruturado, multi-hop, pronto para o LLM produzir código de qualidade.

## 📦 Stack Oficial

Vectora é construído sobre estas tecnologias **curadas e suportadas oficialmente**:

| Componente           | Solução                     | Razão                                                                |
| -------------------- | --------------------------- | -------------------------------------------------------------------- |
| **LLM**              | Google Gemini 3 Flash       | Velocidade 30ms, custo 90% menor, performance suficiente para código |
| **Embeddings**       | Voyage AI 4                 | 1,536 dimensões, suporte multimodal (código + texto), precisão 98.5% |
| **Reranking**        | Voyage Rerank 2.5           | Cross-encoder de precisão, foi treinado em código, latência <100ms   |
| **Vector DB**        | Qdrant Cloud                | HNSW com TurboQuant, filtros payload, performance <50ms              |
| **Metadata & Auth**  | Supabase (PostgreSQL + RLS) | Namespace isolation, escalável, serverless                           |
| **API & Serverless** | Vercel Functions            | Deploy global, cold start <100ms, escalabilidade automática          |

**Nota importante**: Vectora usa **APENAS** este stack. Não suportamos fallbacks para Voyage 3-large, Gemini Embedding
2.0, ou modelos alternativos. A escolha foi rigorosa após meses de benchmarking.

## 🏗️ Filosofia e Design

Vectora é mais que um script — é um **ecossistema** projetado para latência baixa, precisão alta e segurança total:

- **Protocolos MCP & ACP**: Comunicação ultra-rápida com IDEs (VS Code, JetBrains) e agentes autônomos
- **Context Engine**: O "cérebro" que decide dinamicamente o que buscar, em que ordem e com qual profundidade
- **Guardian (Hard-Coded)**: Blocklist imutável em nível de binário TypeScript — jamais acessa `.env`, `.key`, `.pem` ou
  binários
- **Harness (Validação)**: Sistema de avaliação de qualidade com judge engine + comparação vetorial
- **Namespace Isolation**: Multi-tenant seguro via Supabase RLS + Qdrant payload filtering

---

## 🚀 Por Onde Começar?

- 📖 [**Getting Started**](getting-started/) — Configure Vectora em minutos, obtenha suas chaves API
- 🏗️ [**Conceitos Fundamentais**](concepts/) — Entenda RAG Conectado, embeddings, reranking e o Context Engine
- 📚 [**Arquitetura Profunda**](architecture/) — Deep dive em cada componente do sistema
- 🛠️ [**API Reference**](api/) — Documentação completa de endpoints e payloads
- ❓ [**FAQ & Troubleshooting**](faq/) — Respostas a perguntas comuns e resolução de problemas
