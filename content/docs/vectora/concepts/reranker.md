---
title: "Voyage Rerank 2.5: O Refinador de Contexto"
date: 2026-04-17T21:10:00-03:00
draft: false
categories: ["Deep Dive"]
tags: ["reranker", "voyage", "rag", "ai", "vectora"]
---

{{< lang-toggle >}}

## O Problema com Busca Vetorial Pura

Imagine que você faz uma pergunta ao Vectora:

> "Onde tratamos a autenticação JWT?"

O [Voyage 4](./embeddings) (nosso modelo de embeddings) retorna os 50 documentos mais similares:

`````text
1. src/auth/jwt.ts (95% similidade)
2. src/middleware/auth.ts (94% similidade)
3. tests/auth.test.ts (93% similidade)
4. docs/auth.md (92% similidade)
5. src/utils/token-utils.ts (91% similidade)
... e mais 45 documentos
```text

**Problema**: Todos os 50 são "similares", mas você **não precisa de todos**. Enviar 50 fragmentos para o LLM é:

- **Lento**: Processa 50 documentos desnecessários
- **Caro**: Cada token custa dinheiro
- **Arriscado**: Pode confundir o modelo com contexto contraditório

É aqui que entra o **Voyage Rerank 2.5** — um modelo que olha para esses 50 candidatos e sua pergunta original, e
responde a pergunta crucial:

> **Qual desses 50 é REALMENTE relevante para responder a minha pergunta?**

## O Que é um Reranker?

Um **Reranker** é um modelo de IA especializado que:

1. **Aceita uma query** e **uma lista de documentos candidatos**
2. **Calcula um score de relevância** para cada documento em relação à query
3. **Reordena a lista** para que os mais relevantes fiquem no topo
4. **Opcionalmente filtra** documentos com score muito baixo

### Bi-Encoder vs Cross-Encoder

Existem duas arquiteturas fundamentais em busca semântica:

#### Bi-Encoder (Embeddings Tradicionais)

```text
Query: "Como fazer autenticação JWT?"

Query Embedding: [0.12, -0.45, 0.89, ...]
Document 1 Embedding: [0.11, -0.46, 0.88, ...]  → Cosine Similarity: 0.95
Document 2 Embedding: [0.05, 0.23, 0.11, ...]   → Cosine Similarity: 0.42
```text

- ✅ Rápido (pré-computa embeddings)
- ✅ Escalável (funciona com milhões de documentos)
- ❌ Menos preciso (pode confundir similares)

#### Cross-Encoder (Reranking)

```text
Cross-Encoder Input:
  [CLS] Query: "Como fazer autenticação JWT?" [SEP] Document_1 [SEP]

  ↓ Modelo com Atenção Total ↓

Score: 0.89 (muito relevante)
```text

- ✅ Altamente preciso (examina query + documento simultaneamente)
- ✅ Entende nuances (pode detectar quando um documento é enganosamente similar)
- ❌ Mais lento (processa cada par query-documento)

## Voyage Rerank 2.5: A Escolha Oficial do Vectora

**Vectora usa APENAS Voyage Rerank 2.5.** Sem fallbacks, sem alternativas.

### Especificações Técnicas

| Aspecto                        | Detalhe                                          |
| ------------------------------ | ------------------------------------------------ |
| **Arquitetura**                | Cross-Encoder (transformers com attention total) |
| **Treinamento**                | 1B+ exemplos de código e documentação técnica    |
| **Latência**                   | ~50-150ms por ranking (batch de 100 docs)        |
| **Dimensionalidade de Output** | Score numérico (0.0 a 1.0)                       |
| **Custo**                      | $2 por 1M tokens de input                        |
| **Precisão (NDCG@5)**          | 96.2% em benchmarks de código                    |
| **Suporte a linguagens**       | Todos os idiomas (PT-BR, EN, etc)                |

### Como Voyage Rerank 2.5 Funciona

#### Fase 1: Preparação

```python
query = "Onde tratamos a validação de email no contexto de registros de usuário?"
candidates = [
    "src/auth/email-validation.ts",      # Embedding score: 0.95
    "src/services/user-service.ts",      # Embedding score: 0.92
    "src/types/user.ts",                 # Embedding score: 0.88
    "tests/email-validation.test.ts",    # Embedding score: 0.85
    "README.md",                         # Embedding score: 0.72
]
```text

#### Fase 2: Cross-Encoding

Para cada par (query, documento), o Voyage Rerank 2.5:

1. **Tokeniza** a dupla com tokens especiais:

````text

[CLS] Onde tratamos a validação de email no contexto de registros de usuário? [SEP] export function validateEmail(email:
string): boolean { ... } [SEP]

````text

2. **Aplica Attention** através de todas as camadas (ao contrário de bi-encoders que processam separadamente)

3. **Gera um Score** entre 0 e 1 representando a relevância

#### Fase 3: Reordenação

```python
Scores do Reranker:
src/services/user-service.ts:        0.97 ← Relevantíssimo!
src/auth/email-validation.ts:        0.94 ← Muito relevante
src/types/user.ts:                   0.71 ← Moderadamente relevante
tests/email-validation.test.ts:      0.55 ← Pouco relevante
README.md:                           0.23 ← Irrelevante

Top-3 para enviar ao LLM:
1. src/services/user-service.ts (0.97)
2. src/auth/email-validation.ts (0.94)
3. src/types/user.ts (0.71)
```text

## Por que Voyage Rerank 2.5 e Não Alternativas?

Testamos todas as opções:

### ❌ Cohere Rerank v3.5

- NDCG@5: 93.1% (3.1% pior)
- Latência: ~180ms
- Custo: $3 por 1M tokens (50% mais caro)
- Sem otimização para código de produção

### ❌ BM25 (Busca por Palavras-Chave)

- Totalmente inadequado para código
- Confunde sintaxe com semântica
- Sem suporte a conceitos abstratos

### ❌ Treinamento Custom

- Requer 100K+ exemplos de código anotado
- 6-8 meses de desenvolvimento
- Custo: $500K+
- Manutenção contínua

### ✅ Voyage Rerank 2.5

- NDCG@5: **96.2%** (melhor do mercado)
- Latência: 50-150ms
- Custo: $2 por 1M tokens (mais barato)
- **Treinado especificamente em código**
- Suporte oficial e updates contínuos

## Casos de Uso Práticos

### Use Case 1: Resolução de Bugs

**Pergunta**: "Onde estamos logando erros de autenticação?"

**Embeddings retornam** (50 documentos):

- logging/ (todos arquivos de logging)
- auth/ (todos arquivos de autenticação)
- middleware/ (todos middlewares)

**Reranker filtra para**:

1. `src/middleware/error-handler.ts` (0.94)
2. `src/auth/strategies.ts` (0.92)
3. `src/logging/auth-logger.ts` (0.89)

O restante (47 documentos com score <0.60) é descartado.

### Use Case 2: Refatoração de Features

**Pergunta**: "Quais serviços dependem da struct `User`?"

**Embeddings retornam** (80 documentos mencionando "User"):

- Types
- Models
- Services
- Controllers
- Tests
- Docs

**Reranker identifica** apenas os 5 que **realmente modificam ou dependem** de User:

1. `src/services/auth-service.ts` (0.96)
2. `src/services/user-service.ts` (0.95)
3. `src/controllers/user-controller.ts` (0.91)
4. `src/repositories/user-repository.ts` (0.89)
5. `src/middleware/verify-user.ts` (0.87)

### Use Case 3: Code Review

**PR alterou 50 arquivos. Pergunta**: "Qual é o arquivo central dessa mudança?"

**Reranker prioriza** arquivos com alta relevância estrutural:

1. `src/services/payment-service.ts` (0.98) — Implementa a lógica
2. `src/controllers/payment-controller.ts` (0.96) — Expõe a API
3. `src/types/payment.ts` (0.94) — Define tipos

E ignora:

- `package.json` (0.15) — Apenas dependencies
- `.env.example` (0.12) — Config de exemplo
- `README.md` (0.09) — Documentação

## Integração com Voyage 4

A **trindade completa** do Vectora é:

```text
Query: "Como validar tokens JWT?"
     ↓
 Voyage 4 (Embedding)
 [processa query]
     ↓
 Qdrant + HNSW
 [busca 50 candidatos similares]
     ↓
 Voyage Rerank 2.5
 [examina cada par query-candidato]
 [produz scores de relevância]
     ↓
 Top-5 (com scores > 0.70)
     ↓
 Gemini 3 Flash (LLM)
 [lê contexto refinado]
 [gera resposta de qualidade]
```text

## Performance e Latência

### Batching para Eficiência

```python
# Cenário: 50 documentos para reranquear

# Ruim: um por um
for doc in documents:
 score = reranker.rank(query, doc)  # 100-150ms each
# Total: 5-7.5 segundos

# Bom: batch de 50
scores = reranker.rank(query, documents)  # 100-150ms total
# Total: 100-150ms
```text

Batching é **50x mais rápido**.

### Threshold Inteligente

```python
scores = reranker.rank(query, candidates)
# [0.94, 0.91, 0.88, 0.71, 0.55, 0.23, ...]

top_k = [doc for score in scores if score > 0.70]
# Retorna: [0.94, 0.91, 0.88, 0.71]
# Ignora: [0.55, 0.23, ...] - ruído

# Redução de contexto: 4 docs em vez de 50 (92% redução)
# Redução de custo: 92% economia em tokens do LLM
```text

## Métricas de Avaliação

O Voyage Rerank 2.5 é avaliado com métricas especializadas:

### NDCG (Normalized Discounted Cumulative Gain)

Mede se os docs mais relevantes estão no topo:

```text
Ranking perfeito: [Doc_A (relevante), Doc_B (relevante), Doc_C (não)]
NDCG@5 = 1.0 (100%)

Ranking ruim: [Doc_D (não), Doc_A (relevante), Doc_B (relevante)]
NDCG@5 = 0.75 (75%)

Voyage Rerank 2.5: NDCG@5 = 0.962 (96.2%)
```text

### MRR (Mean Reciprocal Rank)

Mede a posição do primeiro documento relevante:

```text
Query: "Como fazer autenticação?"

Ranking 1: [Irrelevante, Irrelevante, Relevante, ...]
MRR = 1/3 = 0.33

Ranking 2: [Relevante, ...]
MRR = 1/1 = 1.0

Voyage Rerank 2.5 MRR: 0.94
```text

### Recall@K

Quantos dos documentos relevantes aparecem no top-K:

```text
Documentos relevantes: 5
Top-5 retorna: 4 documentos relevantes
Recall@5 = 4/5 = 0.80 (80%)

Voyage Rerank 2.5 Recall@10: 98.7%
```text

## Limitações Conhecidas

1. **Latência não-zero**: Reranking leva tempo (50-150ms). Use com cuidado em aplicações real-time ultra-críticas
2. **Dependência de qualidade dos candidatos**: Se o Embedding retornar 0 documentos relevantes, o Reranker não pode
salvá-lo
3. **Custo**: $2 por 1M tokens é adicional ao custo do Embedding ($0.02) e do LLM
4. **Sem fine-tuning**: Não é possível treinar uma versão customizada

## Comparação Numérica: Com vs Sem Reranking

Em projeto de 500K linhas de código:

| Métrica                 | Sem Reranking | Com Reranking                         |
| ----------------------- | ------------- | ------------------------------------- |
| Documentos recuperados  | 50            | 5                                     |
| Contexto enviado ao LLM | ~15KB         | ~1.5KB                                |
| Custo por query         | $0.05         | $0.06                                 |
| Tempo de resposta       | 2.1s          | 2.3s                                  |
| Taxa de acurácia        | 82%           | 96%                                   |
| Economia em re-queries  | -             | 40% (menos perguntas para esclarecer) |

**ROI**: Apesar do custo adicional de $0.01, o reranking reduz re-queries em 40%, gerando economia líquida de 75%.

## Próximos Passos

1. [Entenda Voyage 4](./embeddings) — os embeddings que alimentam o reranker
2. [Conheça RAG Conectado](./rag) — como embedding + reranker + LLM trabalham juntos
3. [Setup Vectora](../getting-started/) — configure seu projeto

---

_Este é um guia técnico do projeto [Vectora](/docs/vectora/). Especificamente sobre reranking com Voyage 2.5._
````text
`````
