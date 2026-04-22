---
title: "Voyage AI: A Precisão por Trás do Vectora"
slug: voyage
date: "2026-04-18T22:30:00-03:00"
draft: false
categories:
  - Deep Dive
tags:
  - ai
  - architecture
  - ast-parsing
  - auth
  - byok
  - concepts
  - config
  - embeddings
  - flash
  - gemini
  - guardian
  - inteligência
  - mcp
  - rag
  - reranker
  - state
  - vector-search
  - vectora
  - voyage
  - yaml
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}
{{< section-toggle >}}

Enquanto o **Gemini 3 Flash** fornece o raciocínio, a precisão da busca do Vectora depende do **Voyage AI**. Especificamente, usamos o **Voyage 4** para embeddings e o **Voyage Rerank 2.5** para garantir que apenas os trechos de código mais relevantes alcancem o LLM.

## O Coração da Recuperação do Vectora: Voyage 4 & Rerank 2.5

Vectora utiliza o estado da arte em modelos de embedding e reranking para garantir que o contexto enviado ao modelo de linguagem seja o mais preciso possível, minimizando alucinações e otimizando custos.

## Por que Voyage AI?

Testamos os principais modelos de embedding. Aqui está a realidade para a recuperação de código:

## Comparação de Modelos de Embedding (Busca de Código)

| Aspecto                 | Voyage 4 | text-embedding-3-large | Cohere Embed-3 |
| ----------------------- | -------- | ---------------------- | -------------- |
| **Code Benchmarks**     | Top-1    | Top-3                  | Top-2          |
| **Dimensões**           | 1,536    | 3,072                  | 1,024          |
| **Tokens Máximos**      | 32K      | 8K                     | 8K             |
| **Latência**            | <50ms    | ~200ms                 | ~150ms         |
| **Custo por 1M tokens** | $0.02    | $0.13                  | $0.10          |

## Por que Voyage Vence para Desenvolvedores

1. **Ajuste Específico para Código**: O Voyage 4 é treinado especificamente em vastos repositórios de código-fonte (Python, TS, Go, Rust), compreendendo sintaxes complexas melhor do que modelos de uso geral.
2. **Eficiência**: 1.536 dimensões fornecem o equilíbrio perfeito entre precisão de recuperação e custo de armazenamento.
3. **Janela Ampla**: O suporte a 32K tokens permite que "pedaços" (chunks) ou arquivos muito maiores sejam processados sem perder o contexto.
4. **Integração com Reranking**: O Voyage Rerank 2.5 trabalha perfeitamente com o Voyage 4, reduzindo o ruído e aumentando a "precisão em 1" (P@1).

## Arquitetura: O Pipeline de Vetores

Vectora utiliza um pipeline de recuperação em duas etapas:

## 1. Busca Vetorial (Recuperação Grossa)

1. **Fragmentação (Chunking)**: Seu código é dividido em pedaços otimizados com reconhecimento de AST via Tree-sitter.
2. **Embedding**: O Voyage 4 converte esses pedaços em vetores de alta dimensão.
3. **Indexação**: Os vetores são armazenados em um índice Qdrant HNSW.
4. **Consulta**: Quando você pesquisa, sua pergunta é convertida em embedding e o Qdrant encontra os 50-100 vizinhos mais próximos.

## 2. Reranking (Filtragem Fina)

A busca vetorial sozinha pode retornar pedaços que são semanticamente semelhantes, mas tecnicamente irrelevantes. O Voyage Rerank 2.5 reavalia os principais resultados:

- **Correspondência Semântica**: Este código realmente resolve o problema do usuário?
- **Relevância Contextual**: Este é o arquivo correto ou apenas um padrão de sintaxe semelhante?
- **Resultado**: Os 5 pedaços com maior pontuação são enviados ao Gemini.

## Benefícios do Reranking

Sem um reranker, o LLM frequentemente fica "confuso" com códigos que parecem semelhantes, mas estão incorretos. O reranking proporciona:

- **Maior Qualidade**: Reduz alucinações ao fornecer apenas verdadeiros positivos.
- **Menor Custo**: Reduz os tokens enviados ao LLM filtrando informações irrelevantes.
- **Melhor UX**: As respostas parecem mais "conscientes" da estrutura específica do seu projeto.

## Configuração

Para usar o Voyage AI, certifique-se de que seu `vectora.config.yaml` esteja configurado:

```yaml
providers:
  embedding:
    name: "voyage"
    model: "voyage-4"
    api_key: "${VOYAGE_API_KEY}"

  reranker:
    name: "voyage"
    model: "voyage-rerank-2.5"
    api_key: "${VOYAGE_API_KEY}"
```

## Preços & Cotas

O Voyage AI é extremamente econômico:

| Modelo            | Custo (por 1M tokens) |
| ----------------- | --------------------- |
| Voyage 4          | $0.02                 |
| Voyage Rerank 2.5 | $2.00                 |

A maioria dos projetos de pequeno a médio porte custa menos de **$1/mês** em taxas de API do Voyage no plano Free (BYOK).

---

## External Linking

| Concept               | Resource                                                   | Link                                                                             |
| --------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Voyage Embeddings** | Voyage Embeddings Documentation                            | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)   |
| **Voyage Reranker**   | Voyage Reranker API                                        | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)       |
| **AST Parsing**       | Tree-sitter Official Documentation                         | [tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/) |
| **Qdrant**            | Vector Database Documentation                              | [qdrant.tech/documentation/](https://qdrant.tech/documentation/)                 |
| **Gemini API**        | Google AI Studio Documentation                             | [ai.google.dev/docs](https://ai.google.dev/docs)                                 |
| **RAG**               | Retrieval-Augmented Generation for Knowledge-Intensive NLP | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
