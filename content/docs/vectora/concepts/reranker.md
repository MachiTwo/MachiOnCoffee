---
title: "Reranker: Por que a similaridade não é o suficiente para código"
date: 2026-04-17T21:10:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["reranker", "rag", "ai", "vectora"]
---

{{< lang-toggle >}}

Muitas vezes, uma busca vetorial (Embedding) te devolve 50 arquivos que "parecem" relevantes, mas apenas 3 realmente são
úteis para resolver o bug. Enviar os 50 para o LLM é um desperdício de tokens e pode confundir a IA. É aqui que entra o
**Reranker**.

## O Filtro de Precisão

Enquanto o Embedding é excelente em encontrar candidatos rapidamente em uma base gigante, ele costuma trazer muito ruído
(como arquivos de teste ou boilerplates que usam as mesmas palavras).

O **Reranker** é um modelo de IA mais lento e "profundo" que analisa apenas esses 50 candidatos e a sua pergunta
original. Ele faz um cruzamento direto (cross-attention) para reordenar a lista, colocando o que é **crucial** no topo.

## Por que o Vectora exige um Reranker?

Em código, a precisão é tudo. Um erro de contexto pode levar a uma refatoração desastrosa. O pipeline do
[Vectora](/04/17/vectora/) utiliza modelos como o **Cohere Rerank v3.5** ou o **Voyage Rerank 2** para:

1. **Eliminar Ruído**: Ignora arquivos que são semanticamente próximos, mas funcionalmente irrelevantes.
2. **Priorizar Dependências**: Se você pergunta sobre um erro, o Reranker entende que o arquivo de log e a lógica de
   tratamento de erro devem vir antes de um arquivo `README`.
3. **Eficiência de Tokens**: Ao filtrar apenas o "Top N" realmente relevante, o Vectora economiza até 40% em custos de
   API.

## A Trindade do Contexto

O [Vectora](/04/17/vectora/) orquestra a trindade perfeita:

1. **Embedding**: Encontra os candidatos.
2. **Reranker**: Filtra os relevantes.
3. **LLM**: Age sobre o contexto refinado.

---

_Este é um guia técnico do projeto [Vectora](/docs/vectora/)._
