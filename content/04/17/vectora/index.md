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

Agentes de IA tradicionais costumam alucinar porque operam em contextos fragmentados. O **Vectora** resolve isso não sendo "mais um chat", mas sim um **Motor de Conhecimento Contextual** que funciona como um **Sub-Agent Tier 2**.

## O Posicionamento: De RAG para Conhecimento Conectado

Diferente do RAG (Retrieval-Augmented Generation) tradicional que apenas busca fragmentos isolados de texto, o Vectora entende a **estrutura sistêmica** do seu código.

Ele não compete com agentes como Claude Code, Gemini CLI ou Cursor; ele os **potencializa**. O Vectora atua como uma camada de inteligência intermediária que entrega contexto estruturado via protocolos abertos (**MCP** e **ACP**).

## Arquitetura Técnica: Confiabilidade em TypeScript

O runtime do Vectora foi desenvolvido em **TypeScript (Node.js 20+)**, utilizando a **AI SDK da Vercel** para garantir um roteamento de modelos estável e agnóstico de provedores (OpenRouter, Google, Anthropic, OpenAI).

### Componentes Core:
- **Context Engine**: Realiza **raciocínio multi-hop** e análise estrutural via **AST (Tree-sitter)**. Ele não busca apenas palavras; ele segue dependências, imports e fluxos de execução para montar um grafo da sua codebase.
- **Nativo Cloud & Local**: Integração com **Qdrant Cloud** para busca vetorial escalável (usando HNSW e quantização escalar) e suporte opcional para inferência 100% local via **llama.cpp**.
- **Infraestrutura**: Backend de metadados e autenticação via **Supabase**, com as camadas de API rodando em **Vercel Edge Functions**.

## Validação Objetiva: Vectora Harness

Como saber se a IA realmente melhorou? Criamos o **Vectora Harness**, o "sistema nervoso central" do nosso agent. Ele permite:
1. **Medir a Precisão**: Compara objetivamente o output da IA com `vectora:on` vs `vectora:off`.
2. **Eficiência de Tokens**: Otimiza a recuperação para evitar o "overfetch" de contexto, reduzindo custos e latência.
3. **Auditabilidade**: Gera relatórios estruturados sobre como o agente usou cada ferramenta para chegar na resposta.

## Segurança: Hard-Coded Guardian

Segurança em IA não pode depender apenas de prompts. O Vectora implementa o **Guardian**, um middleware imutável em código que:
- **Bloqueia Paths Sensíveis**: Arquivos como `.env`, `.key`, `.pem` e lockfiles nunca são lidos ou embedados.
- **Sanitização de Output**: Regex nativa que mascara segredos e PATs antes que eles saiam do seu ambiente.
- **Git Snapshots**: Commits atômicos automáticos antes de qualquer operação de escrita, garantindo reversibilidade total.

O Vectora é a camada de confiança que faltava para tornar o desenvolvimento assistido por IA profissional, seguro e mensurável.

---
*Vectora faz parte do ecossistema Kaffyn · Open Source · TypeScript · Provider-Agnostic.*
