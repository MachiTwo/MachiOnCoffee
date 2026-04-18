---
title: "RAG Conectado"
type: docs
---

Você já perguntou a um agente de IA sobre uma função no seu projeto e ele respondeu algo que parecia certo, mas que
ignorava completamente como aquela função era usada no resto do sistema? Isso é o sintoma clássico do **RAG
fragmentado**.

## O que é RAG?

**RAG (Retrieval-Augmented Generation)** é a técnica de fornecer dados externos (como seus arquivos de código) para um
LLM no momento da pergunta. Em vez de o modelo "adivinhar" baseado no que ele aprendeu no treino, ele consulta seus
documentos e responde baseado neles.

Parece perfeito, certo? Mas para código, o RAG comum é perigoso.

## O Problema do RAG Tradicional

A maioria dos bancos de dados vetoriais foca em **similaridade semântica de pedaços isolados**.

Se você busca por `login`, ele vai te dar os blocos de código que contêm a palavra `login`. Mas ele pode ignorar o
middleware de autenticação, o arquivo de configuração de banco de dados ou a dependência que gerencia os tokens JWT.

Para o LLM, é como tentar montar um quebra-cabeça recebendo apenas 5 peças aleatórias e sem a caixa para ver o desenho
completo.

## A Solução: RAG Conectado (Context Engine)

No [Vectora](/docs/vectora/), o RAG não é apenas "buscar texto". Ele funciona através de um **Context Engine** que
entende a estrutura:

1. **Busca Multimodal**: Combina busca vetorial (semântica) com busca estrutural (AST e Grep).
2. **Multi-hop Reasoning**: O motor de contexto não faz apenas uma busca. Se ele encontra uma referência a uma
   interface, ele faz um "salto" para buscar a implementação dessa interface.
3. **Composição Estruturada**: O contexto entregue ao Agente principal não é uma lista de textos, mas uma árvore
   organizada de arquivos, dependências e metadados.

## Por que isso importa?

Quando o contexto é **conectado**:

- As alucinações caem drasticamente.
- O Agente para de sugerir mudanças que quebram outras partes do sistema.
- Você gasta menos tokens, pois o contexto enviado é cirúrgico, não um "dump" de arquivos.

O RAG tradicional te dá dados. O RAG Conectado do Vectora te dá **conhecimento**.

---

_Este é um guia técnico do projeto [Vectora](../)._
