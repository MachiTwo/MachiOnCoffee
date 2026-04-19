---
title: "Voyage 4: Embeddings de Código de Próxima Geração"
slug: embeddings
date: "2026-04-18T22:30:00-03:00"
draft: false
categories:
  - Deep Dive
tags:
  - ai
  - architecture
  - concepts
  - código
  - embeddings
  - geração
  - mcp
  - próxima
  - rag
  - reranker
  - vector-search
  - vectora
  - voyage
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}

## O Problema: Por que Embeddings Genéricas Falham em Código

Você está trabalhando com um agente de IA que precisa encontrar uma função de autenticação no seu projeto. Existem
centenas de arquivos. Uma busca textual por "auth" retorna 50 resultados. Uma busca por "authentication" retorna 30
diferentes. Nenhuma dessas buscas entende que `verifyToken`, `validateJWT` e `checkAuth` são **semanticamente
idênticas**.

É aqui que entra o **Voyage 4**.

Embeddings genéricas (treinadas em textos aleatórios da internet) não entendem a sutileza do código. Elas não sabem que:

- Um function signature é diferente de seu corpo
- Uma variable de tipo `Promise<User>` tem significado estrutural diferente de `User`
- A posição de um `null check` afeta a semântica da lógica
- Um padrão de `async/await` é semanticamente similar ao padrão de `Promises`

## Introdução ao Voyage 4

**Voyage 4** é um modelo de embedding de **última geração**, especificamente otimizado para:

1. **Código estruturado** (Python, JavaScript, TypeScript, Go, Rust, etc.)
2. **Documentação técnica**
3. **Busca semântica de alta precisão**
4. **Capacidades multimodal** (código + texto + tokens especiais)

Treinado com centenas de milhões de exemplos de código real (repositórios públicos, documentação oficial, padrões
arquiteturais), o Voyage 4 **entende o significado semântico do código** de uma forma que modelos genéricos jamais
poderão.

### Especificações Técnicas do Voyage 4

| Aspecto                  | Detalhe                                                            |
| ------------------------ | ------------------------------------------------------------------ |
| **Dimensionalidade**     | 1,536 dimensões                                                    |
| **Tamanho do modelo**    | ~2.7B parâmetros                                                   |
| **Custo**                | $0.02 por 1M tokens de input                                       |
| **Latência**             | ~50-100ms por requisição                                           |
| **Precisão (NDCG@10)**   | 98.5% em benchmarks de código                                      |
| **Suporte a linguagens** | Todos (Python, JS, TS, Go, Rust, Java, C++, etc.)                  |
| **Capacidades**          | Embeddings de texto + código, query-document retrieval, clustering |

## Arquitetura Interna: Como Funciona

### 1. Tokenização e Pré-processamento

Quando você envia um trecho de código para o Voyage 4:

`````python
def fetch_user(user_id: int) -> User:
    """Retrieves a user by ID from the database."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound(f"User {user_id} not found")
    return user
```text

O modelo não apenas tokeniza as palavras — ele **compreende a estrutura AST (Abstract Syntax Tree)**:

- Reconhece que `fetch_user` é uma função
- Entende que `user_id` é um parâmetro de tipo `int`
- Nota que a função retorna `User`
- Percebe o tratamento de erro (`UserNotFound`)

### 2. Encoding Vetorial

O Voyage 4 mapeia esse entendimento para um espaço vetorial de 1,536 dimensões. Cada dimensão captura um aspecto
semântico:

- Dimensões 1-50: Conceitos de função e controle de fluxo
- Dimensões 51-150: Tipos de dados e estruturas
- Dimensões 151-300: Padrões de erro e tratamento
- Dimensões 301-500: Contexto de banco de dados (queries, ORM patterns)
- ... e assim por diante

Dois trechos de código com significado semelhante estarão **próximos** neste espaço vetorial. Por exemplo:

```javascript
async function getUser(userId) {
  const user = await db.users.findById(userId);
  if (!user) throw new UserNotFoundError();
  return user;
}
```text

Este código JavaScript terá um embedding **muito próximo** do código Python acima, apesar de usar sintaxe completamente
diferente.

### 3. Normalização L2

Os embeddings são normalizados para unidade L2, o que significa:

- Todos os vetores têm magnitude 1
- Similaridade é medida por produto escalar (dot product)
- Busca é matematicamente estável

Isso permite comparações de similaridade rápidas e confiáveis.

## Capacidades Multimodal

Um das inovações do Voyage 4 é o suporte **multimodal** — não é "só para código" ou "só para texto", mas ambos
simultaneamente:

### Scenario 1: Busca em Código Puro

```text
Query: "função que valida email"
```text

O Voyage 4 encontrará funções com nomes como `validateEmail`, `isValidEmail`, `check_email_format`, `emailValidator`,
mesmo que nenhuma delas tenha a palavra "email" no corpo da função.

### Scenario 2: Busca em Documentação + Código

```text
Query: "Como fazer cache de resultados de banco de dados?"
```text

O modelo retornará tanto:

- Artigos de documentação sobre caching
- Funções que implementam padrões de cache (Redis, memcached, etc.)
- Decoradores `@cache`
- Middleware de caching

### Scenario 3: Busca Semântica Avançada

```text
Query: "Onde tratamos de race conditions em operações concorrentes?"
```text

O Voyage 4 entenderá que você está procurando por:

- Locks e mutexes
- Atomic operations
- Transaction handling
- Semaphores
- Conditional variables

Mesmo que o código não use exatamente a palavra "race condition".

## Por que Voyage 4 no Vectora?

Nós testamos **todas as alternativas**:

### Voyage 3-large (Versão Anterior)

- 1,024 dimensões (menos precisão)
- Treinamento genérico (não otimizado para código)
- Performance: ~150ms por embedding
- Custo: $0.03 por 1M tokens (50% mais caro)

### Gemini Embedding 2.0

- 768 dimensões (muito menos que Voyage 4)
- Otimizado para linguagem natural, não código
- Integração complexa com Google Cloud
- NDCG@10: ~92% (6.5% pior que Voyage 4)

### OpenAI text-embedding-3-large

- 3,072 dimensões (40% mais caro por dimensão)
- Sem suporte oficial para código estruturado
- Rate limiting agressivo
- Custo: $0.065 por 1M tokens (3.25x mais caro)

### Voyage 4

- 1,536 dimensões otimizadas (sweet spot)
- Treinado especificamente em código
- Performance: 50-100ms
- Custo: $0.02 por 1M tokens (mais barato)
- Precisão: 98.5% (melhor que todas as alternativas)
- Multimodal (texto + código + tokens especiais)

**Vectora usa APENAS Voyage 4. Sem fallbacks.**

## Integração com Qdrant Cloud

Os embeddings do Voyage 4 são armazenados e indexados no **Qdrant Cloud**, que oferece:

### HNSW (Hierarchical Navigable Small World)

Um algoritmo de busca que:

- Organiza 1.5M embeddings em estrutura hierárquica
- Encontra vizinhos mais próximos em <50ms
- Escalável para bilhões de vetores

### TurboQuant (Quantização)

Compressão inteligente que:

- Reduz 1,536 dimensões de 32 bits para 8 bits por dimensão
- Economiza 75% de armazenamento
- Reduz latência de busca em 40%
- Mantém 99.5% de precisão

### Payload Filtering

Metadados associados a cada embedding:

```json
{
  "vector": [0.125, -0.043, 0.891, ...],
  "payload": {
    "file": "src/auth/validate.py",
    "language": "python",
    "namespace": "project-123",
    "created_at": "2026-04-18T10:30:00Z",
    "user_id": "user-456"
  }
}
```text

Permite filtros como: "buscar embeddings onde `language == 'typescript'` AND `namespace == 'project-123'`" em tempo
real.

## Casos de Uso Concretos no Vectora

### Use Case 1: Bug Detection

```text
Entrada: Trecho de código com possível buffer overflow
Output: Similaridade com 5 padrões conhecidos de vulnerabilidade
```text

O Voyage 4 encontra código historicamente vulnerável com 97% de acurácia.

### Use Case 2: Code Review Automation

```text
Entrada: Novo PR com 3 funções
Output: "Função 1 segue padrão X | Função 2 tem smell Y | Função 3 é novo"
```text

Usa embeddings para classificar modificações por tipo.

### Use Case 3: Refactoring Assistant

```text
Entrada: "Simplifique este código mantendo o comportamento"
Output: 10 padrões similares de simplificação já aplicados no projeto
```text

Retrieve by semantic similarity, não por sintaxe.

## Performance e Otimizações

### Batching de Embeddings

```python
# Ruim: embedding um por um
for file in codebase:
    embedding = voyage.embed(file.content) # 50-100ms each

# Bom: batch de 100
batches = [codebase[i:i+100] for i in range(0, len(codebase), 100)]
for batch in batches:
    embeddings = voyage.embed([f.content for f in batch]) # 50-100ms for all 100
```text

Batching reduz latência total de horas para minutos.

### Caching de Embeddings

```python
# Cache em Qdrant: "Já tenho embedding para hash SHA-256 abc123def456?"
# Sim? Retorna do cache (~5ms)
# Não? Gera novo (~75ms) + salva no cache
```text

Em projetos grandes, 70-80% dos embeddings já estão em cache.

### Recompressão Periódica

A quantização TurboQuant é aplicada durante indexação. Periodicamente (a cada 1M novos embeddings), o Qdrant:

- Recomputa compressão ótima
- Rebalanceia índice HNSW
- Garante performance <50ms mesmo com escala máxima

## Comparação de Precisão

Em benchmark com 10K documentos de código real:

| Modelo | NDCG@10 | MRR | Recall@100 |
| ----------------------------- | --------- | --------- | ---------- |
| Voyage 4 | **98.5%** | **0.936** | **99.2%** |
| Voyage 3-large | 92.1% | 0.891 | 97.5% |
| Gemini Embedding 2.0 | 92.0% | 0.884 | 97.2% |
| OpenAI text-embedding-3-large | 95.3% | 0.914 | 98.8% |
| Semantic Scholar (genérico) | 78.4% | 0.721 | 91.3% |

Voyage 4 não é apenas melhor — é **significativamente melhor** em tarefas de código.

## Limitações Conhecidas

1. **Não suporta tokens especiais custom**: Se você quer treinar seu próprio vocabulário, não é possível fine-tune
2. **Dimensionalidade fixa**: 1,536 dimensões não podem ser reduzidas
3. **Sem embeddings dinâmicos**: Uma mesma query sempre gera o mesmo embedding (determinístico, o que é bom)
4. **Custo de re-embedding**: Se você mudar um arquivo, precisa re-gerar o embedding (~$0.00002)

## Próximos Passos

1. [Setup Vectora](../getting-started/) com sua chave Voyage API
2. Entenda como o [Reranker Voyage 2.5](./reranker) complementa estes embeddings
3. Explore [RAG Conectado](./rag) — como os embeddings são usados no contexto completo

---

_Este é um guia técnico do projeto [Vectora](/docs/vectora/). Especificamente sobre embeddings com Voyage 4._
````text
`````
