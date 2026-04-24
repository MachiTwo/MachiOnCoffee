---
title: Queries & Tools Test Suite
slug: queries-tools-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - caching
  - compliance
  - concepts
  - embeddings
  - errors
  - gemini
  - go
  - integration
  - json
  - jwt
  - metrics
  - mongodb
  - queries
  - react
  - reranker
  - search
  - semantic-search
  - testing
  - tools
  - tree-sitter
  - typescript
  - vector-db
  - vector-search
  - vectora
  - voyage
---

{{< lang-toggle >}}

Toda query e tool de Vectora deve funcionar corretamente, retornar resultados precisos e executar dentro dos SLAs de performance. Esta suite é o coração funcional de Vectora, testando todos os 12+ tools e suas integrações com search, embeddings e reranking. Cobertura: **150+ testes** | **Prioridade**: CRÍTICA

## Objetivo

---

## Principais Tools

1. `search_context` - Busca contextual no codebase
2. `search_tests` - Encontra testes relacionados
3. `find_similar_code` - Procura código similar
4. `analyze_dependencies` - Analisa dependências
5. `get_file_structure` - Retorna estrutura de arquivos
6. `list_files` - Lista arquivos no namespace
7. `list_namespaces` - Lista namespaces disponíveis
8. `validate_query` - Valida uma query
9. `get_metrics` - Retorna metrics do servidor
10. `export_context` - Exporta contexto

---

## Segmentos de Testes

### 1. Search Context (30 testes)

#### Test: Basic Query Execution

```text
Given: Namespace "production" com 5000 chunks
And: Query "authentication handler"
When: search_context executado
Then:
  - Top 5 resultados retornados
  - Ordenados por relevância (score)
  - Score > 0.7 para resultado #1
  - Metadata incluída (file, line, type)
  - Latência < 300ms
```

#### Test: Semantic Search Accuracy

```text
Given: Codebase com funções de autenticação
When: Query "JWT validation"
Then:
  - Retorna JWT-related code
  - Mesmo que keywords específicos não mencionem "JWT"
  - Semântica bate (validação + tokens)
  - Precision > 0.85
  - Recall > 0.80
```

#### Test: Large Result Sets

```text
Given: Query que retorna 1000+ resultados
When: search_context com top_k=100
Then:
  - Top 100 retornados em < 500ms
  - Paginação disponível
  - Primeira página accuracy > segunda
```

#### Test: Empty Result Handling

```text
Given: Query "xyzabc123nomeRandomoQueNaoExiste"
When: search_context executado
Then:
  - Array vazio retornado (não erro)
  - Status code 200
  - Mensagem clara: "No results found"
```

#### Test: Special Characters in Query

```text
Given: Query contendo "C++", "C#", ".NET", "React.js"
When: search_context executado
Then:
  - Query parseada corretamente
  - Resultados relevantes retornados
  - Sem SQL injection vulnerabilidade
```

#### Test: Context Window

```text
Given: Query "getUserById"
When: search_context executado
Then: Cada resultado inclui:
  - Função/classe encontrada
  - Linhas anteriores (contexto)
  - Linhas posteriores (contexto)
  - Total: janela de ~20 linhas
```

#### Test: Filters & Constraints

```text
Given: Query com filtros:
  - file: "*.service.ts"
  - type: "function"
  - complexity: "> 3"
When: search_context com filtros
Then: Resultados respeitam todos filtros
And: Latência +50ms vs query simples
```

#### Test: Multi-Language Support

```text
Given: Codebase com Go, TypeScript, Python
When: Query em português: "função de validação"
Then: Resultados de todas as linguagens
And: Semântica transcende linguagem
```

#### Test: Caching Impact

```text
Given: Mesma query executada 10x
When: Executadas sequencialmente
Then:
  - Query 1: 300ms
  - Queries 2-10: < 50ms
  - Hit rate: 90%+
```

---

### 2. Search Tests (25 testes)

#### Test: Test Discovery

```text
Given: Codebase com 200+ testes
And: Query "authentication tests"
When: search_tests executado
Then:
  - Testes auth encontrados
  - Test framework identificado (Jest, Go, Pytest)
  - Coverage info incluída
  - Execution time estimada
```

#### Test: Test Classification

```text
Given: Resultado de search_tests
When: Analisado
Then: Cada teste classificado como:
  - Unit / Integration / E2E
  - Fast (< 100ms) / Medium (100ms-1s) / Slow (> 1s)
  - Critical / Normal / Optional
```

#### Test: Related Tests Discovery

```text
Given: Function "validateJWT"
When: search_tests procura testes relacionados
Then:
  - Encontra "validateJWT.test.js"
  - Encontra "auth.integration.test.js"
  - Encontra testes que usam validateJWT indiretamente
```

#### Test: Missing Tests Detection

```text
Given: Function sem testes
When: search_tests executado
Then:
  - Identifica como "untested"
  - Sugere criar testes
  - Estima coverage gap
```

---

### 3. Find Similar Code (30 testes)

#### Test: Structural Similarity

```text
Given: Snippet:
  function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0)
  }
When: find_similar_code executado
Then: Encontra padrões similares mesmo com nomes diferentes
```

#### Test: Algorithm Recognition

```text
Given: Código de BFS traversal
When: find_similar_code executado
Then:
  - Encontra outros BFS implementations
  - Mesmo com estruturas de dados diferentes
  - Mesmo em linguagens diferentes
  - Score baseado em algoritmo, não sintaxe
```

#### Test: Anti-Pattern Detection

```text
Given: Anti-pattern (e.g., n+1 queries)
When: find_similar_code procura por padrão
Then: Encontra todas instâncias do anti-pattern
And: Sugere refactoring
```

---

### 4. Analyze Dependencies (25 testes)

#### Test: Direct Dependencies

```text
Given: Function "getUserById"
When: analyze_dependencies executado
Then: Encontra:
  - Funções que chama
  - Libraries usadas
  - External APIs chamadas
  - Database queries
```

#### Test: Transitive Dependencies

```text
Given: Function A → B → C → D
When: analyze_dependencies com depth=all
Then:
  - Cadeia completa mapeada
  - Risco de circular dependencies detectado
  - Saída estruturada como grafo
```

#### Test: Dependency Version Conflicts

```text
Given: Codebase com múltiplas versões da mesma lib
When: analyze_dependencies executado
Then:
  - Conflitos identificados
  - Recomendações de resolução
  - Risk assessment
```

#### Test: Breaking Change Detection

```text
Given: Dependência com breaking change
When: analyze_dependencies com versioning
Then:
  - Breaking change detectado
  - Code impact análise
  - Migration path sugerido
```

---

### 5. File Structure Operations (15 testes)

#### Test: File Tree Generation

```text
Given: Directory com estrutura:
  src/
    components/
      Button.tsx
      Input.tsx
    utils/
      format.ts
When: get_file_structure executado
Then: Retorna árvore JSON estruturada
And: Includes file sizes, line counts
```

#### Test: Large Directory Handling

```text
Given: Directory com 10000+ arquivos
When: get_file_structure executado
Then:
  - Completa em < 5s
  - Suporta paginação
  - Opcao de profundidade máxima
```

---

### 6. Validation (15 testes)

#### Test: Query Validation

```text
Given: Query: "find all XXX that YYY"
When: validate_query executado
Then:
  - Sintaxe validada
  - Ambiguidades detectadas
  - Sugestões de refinamento
  - Score de qualidade (0-100)
```

#### Test: Query Ambiguity Detection

```text
Given: Query ambígua: "get calls"
When: validate_query executado
Then:
  - Detecta ambiguidade
  - Sugere refinamentos:
    * "Get all functions that make calls"
    * "Get all incoming calls to function"
  - Oferece para clarificar
```

---

### 7. Metrics & Performance (10 testes)

#### Test: Metrics Retrieval

```text
Given: Vectora rodando há 1 hora
When: get_metrics executado
Then: Retorna:
  - Queries processadas: N
  - Cache hit rate: X%
  - Avg latency: Yms
  - Memory usage: ZMB
  - Uptime: 1h
```

#### Test: Performance Over Time

```text
Given: Metrics coletadas por 24h
When: get_metrics analisado
Then:
  - Detecta degradação de performance
  - Identifica picos de uso
  - Sugere otimizações
```

---

### 8. End-to-End Query Workflows (10 testes)

#### Test: Complete Investigation

```text
Given: Bug report: "getUserById is slow"
When: Investigação completa executada:
  1. search_tests para encontrar testes
  2. analyze_dependencies para entender calls
  3. find_similar_code para padrões
  4. search_context para implementação
Then: Diagnóstico completo com findings
```

#### Test: Code Review Scenario

```text
Given: Pull request com mudanças
When: Queries executadas:
  1. Encontra testes afetados
  2. Descobre dependências
  3. Procura impacto em código similar
Then: Report de review automatizado
```

---

## Performance SLAs

| Query                | P95 Latency | P99 Latency | Cache Hit |
| -------------------- | ----------- | ----------- | --------- |
| search_context       | < 300ms     | < 500ms     | 70%+      |
| search_tests         | < 200ms     | < 300ms     | 80%+      |
| find_similar_code    | < 500ms     | < 1s        | 60%+      |
| analyze_dependencies | < 200ms     | < 400ms     | 75%+      |
| validate_query       | < 100ms     | < 150ms     | 90%+      |

---

## Critérios de Aceitação

| Critério                    | Alvo   |
| --------------------------- | ------ |
| Query success rate          | 100%   |
| Result accuracy (precision) | > 0.85 |
| Result accuracy (recall)    | > 0.80 |
| Latency p95 compliance      | 100%   |
| Cache hit targets           | 100%   |
| Zero crashes/errors         | 100%   |
| Handling of edge cases      | 100%   |

---

## Dependências de API

```env
GOOGLE_API_KEY=xxxx # Google Search
VOYAGE_API_KEY=xxxx # Embeddings + Reranking
MONGODB_ATLAS_URI=xxx # Vector database
```

---

## Como Executar

```bash
# Todos os testes de queries
go test -v ./tests/queries/...

# Tool específica
go test -v -run TestSearchContext ./tests/queries/...

# Com benchmarks
go test -v -bench=. ./tests/queries/...

# Com coverage
go test -v -cover ./tests/queries/...

# Load test
go test -v -timeout 30m ./tests/queries/load_tests.go
```

---

## Mapa de Implementação

- [ ] Search Context (30 testes)
- [ ] Search Tests (25 testes)
- [ ] Find Similar Code (30 testes)
- [ ] Analyze Dependencies (25 testes)
- [ ] File Structure (15 testes)
- [ ] Validation (15 testes)
- [ ] Metrics (10 testes)
- [ ] E2E Workflows (10 testes)

**Total**: 150+ testes

---

## External Linking

| Concept               | Resource                                    | Link                                                                                                       |
| --------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **MongoDB Atlas**     | Atlas Vector Search Documentation           | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **JWT**               | RFC 7519: JSON Web Token Standard           | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)                     |
| **AST Parsing**       | Tree-sitter Official Documentation          | [tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/)                           |
| **Voyage Embeddings** | Voyage Embeddings Documentation             | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)                             |
| **Voyage Reranker**   | Voyage Reranker API                         | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)                                 |
| **Gemini API**        | Google AI Studio & Gemini API Documentation | [ai.google.dev/docs](https://ai.google.dev/docs)                                                           |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [Licença (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Parte do ecossistema Vectora AI Agent. Construído com [ADK](https://adk.dev/), [Claude](https://claude.ai/) e [Go](https://golang.org/)._

© 2026 Contribuidores do Vectora. Todos os direitos reservados.
