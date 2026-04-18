---
title: "Vectora: O Sub-Agente que Conecta o Contexto do Seu Código"
date: "2026-04-17T18:00:00-03:00"
slug: vectora
tags:
  - ai
  - productivity
  - tools
draft: false
---

Agentes de IA tradicionais costumam alucinar porque operam em contextos fragmentados. O **Vectora** resolve isso não
sendo "mais um chat", mas sim um **Motor de Conhecimento Contextual** que funciona como um **Sub-Agent Tier 2**.

<div class="hx:flex hx:justify-center hx:my-8">
  <img src="/images/vectora.svg" alt="Vectora Logo" class="hx:max-w-md hx:w-full hx:rounded-2xl hx:shadow-2xl hx:border hx:border-gray-200 hx:dark:border-gray-800">
</div>

## O Problema: Contexto Fragmentado

A maioria dos agentes hoje (Claude Code, Cursor, GitHub Copilot) sofre do mesmo mal: eles veem o código como pedaços
isolados de texto. Eles não entendem a **árvore de dependências**, as decisões arquiteturais passadas (ADRs) ou a
intenção por trás de um módulo.

O Vectora nasceu para ser a camada de inteligência que conecta esses pontos, entregando o que chamamos de **Conhecimento
Conectado**.

## 🏗️ Arquitetura EndGame

O Vectora não é apenas um script; é um ecossistema projetado para latência baixa e alta precisão:

- **Protocolos MCP & ACP**: Integração via [Model Context Protocol (MCP)](/04/17/sub-agents-mcp/) para agentes como
  Claude e Antigravity, e ACP para comunicação ultra-rápida com IDEs.
- **Context Engine**: O "cérebro" que decide _o que_, _como_ e _quando_ buscar informação, evitando o ruído que consome
  seus tokens.
- **Vector DB (Qdrant Cloud)**: Utiliza busca vetorial com [HNSW e Quantização](/04/17/embeddings-vector-db/) para
  encontrar similaridades funcionais em milissegundos.
- **Reranker Proeminente**: Uma camada de [Reranking](/04/17/reranker-contexto/) que reordena os resultados para
  garantir que o código mais relevante esteja no topo.

## 🔐 Segurança por Design: O Guardian

Segurança em agentes de IA não pode ser apenas "prompts de sistema" (que são fáceis de burlar). No Vectora, a segurança
é **hard-coded**:

1. **Hard-Coded Guardian**: Uma blocklist imutável compilada no binário que impede o acesso a arquivos sensíveis
   (`.env`, `.key`, `.pem`, binários) independente do que o usuário ou o agente peça.
2. **Namespaces com RBAC**: Isolamento real entre projetos. Seus dados de um projeto nunca vazam para outro, e
   namespaces públicos podem ser montados como "habilidades" prontas para uso.
3. **Trust Folder**: O agente só opera dentro de diretórios explicitamente autorizados por você.

## 🧪 Vectora Harness: Prova de Valor

Como saber se o agente está realmente melhorando? O **Vectora Harness** é o nosso sistema de validação objetiva. Ele
permite rodar testes comparativos: `vectora harness run --compare vectora:on,off`

Isso gera métricas reais de ganho de precisão, redução de tokens e prevenção de violações de segurança. Não é intuição,
é evidência quantitativa.

---

### Quer se aprofundar na tecnologia?

Explore nossos guias técnicos de base:

- [O que é RAG e por que o contexto conectado importa?](/04/17/rag-conectado/)
- [Embeddings e Bancos Vetoriais: O coração da busca semântica](/04/17/embeddings-vector-db/)
- [Reranker: Por que a similaridade não é o suficiente para código](/04/17/reranker-contexto/)
- [Sub-Agents vs MCP: Ferramentas passivas vs Governança ativa](/04/17/sub-agents-mcp/)

O runtime do Vectora foi desenvolvido em **TypeScript (Node.js 20+)**, utilizando a **AI SDK da Vercel** para garantir
um roteamento de modelos estável e agnóstico de provedores (OpenRouter, Google, Anthropic, OpenAI).

### Componentes Core

- **Context Engine**: Realiza **raciocínio multi-hop** e análise estrutural via **AST (Tree-sitter)**. Ele não busca
  apenas palavras; ele segue dependências, imports e fluxos de execução para montar um grafo da sua codebase.
- **Nativo Cloud & Local**: Integração com **Qdrant Cloud** para busca vetorial escalável (usando HNSW e quantização
  escalar) e suporte opcional para inferência 100% local via **llama.cpp**.
- **Infraestrutura**: Backend de metadados e autenticação via **Supabase**, com as camadas de API rodando em **Vercel
  Edge Functions**.

## Validação Objetiva: Vectora Harness

Como saber se a IA realmente melhorou? Criamos o **Vectora Harness**, o "sistema nervoso central" do nosso agent. Ele
permite:

1. **Medir a Precisão**: Compara objetivamente o output da IA com `vectora:on` vs `vectora:off`.
2. **Eficiência de Tokens**: Otimiza a recuperação para evitar o "overfetch" de contexto, reduzindo custos e latência.
3. **Auditabilidade**: Gera relatórios estruturados sobre como o agente usou cada ferramenta para chegar na resposta.

## Segurança: Hard-Coded Guardian

Segurança em IA não pode depender apenas de prompts. O Vectora implementa o **Guardian**, um middleware imutável em
código que:

- **Bloqueia Paths Sensíveis**: Arquivos como `.env`, `.key`, `.pem` e lockfiles nunca são lidos ou embedados.
- **Sanitização de Output**: Regex nativa que mascara segredos e PATs antes que eles saiam do seu ambiente.
- **Git Snapshots**: Commits atômicos automáticos antes de qualquer operação de escrita, garantindo reversibilidade
  total.

O Vectora é a camada de confiança que faltava para tornar o desenvolvimento assistido por IA profissional, seguro e
mensurável.

---

_Vectora faz parte do ecossistema Kaffyn · Open Source · TypeScript · Provider-Agnostic._
