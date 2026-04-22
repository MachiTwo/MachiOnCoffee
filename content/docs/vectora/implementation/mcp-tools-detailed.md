---
title: Plano de Implementação - MCP Tools (12 Ferramentas Detalhadas)
slug: mcp-tools-detailed
date: "2026-04-21T14:00:00-03:00"
type: docs
tags:
  - ai
  - api-design
  - ast-parsing
  - auth
  - concepts
  - context-engine
  - embeddings
  - engineering
  - errors
  - gemini
  - golang
  - guardian
  - harness-runtime
  - integration
  - mcp
  - mongodb-atlas
  - openai
  - persistence
  - protocol
  - reranker
  - tools
  - vector-search
  - vectora
  - voyage
---

{{< lang-toggle >}}
{{< section-toggle >}}

Este documento detalha a implementação de cada uma das **12 ferramentas MCP** que constituem a interface pública do Vectora. Cada ferramenta tem especificação de entrada/saída, exemplos de código Go, dependências internas, testes, e critérios de aceitação.

## Visão Geral das 12 Ferramentas

As ferramentas estão organizadas em 3 grupos funcionais:

[x] **Grupo 1: Search & Retrieval** (4 ferramentas)

- `search_context` — Busca semântica híbrida (embeddings + AST)
- `search_tests` — Localiza testes relacionados a código
- `find_similar_code` — Encontra padrões de código similares
- `analyze_dependencies` — Mostra quem chama uma função/classe

[x] **Grupo 2: Navigation & Structure** (4 ferramentas)

- `get_file_structure` — Resumo estruturado de arquivo (AST)
- `list_files` — Lista arquivos indexados em namespace
- `list_namespaces` — Lista namespaces configurados
- `get_session_state` — Histórico e contexto da sessão

[x] **Grupo 3: Management & Utilities** (4 ferramentas)

- `index_progress` — Status de indexação em tempo real
- `validate_query` — Valida query antes de executar
- `get_metrics` — Métricas de uso e performance
- `export_context` — Exporta contexto para arquivo/clipboard

---

## Grupo 1: Search & Retrieval (2 semanas)

### 1.1 `search_context` — Busca Semântica Híbrida

**Responsabilidade**: Busca principal do Vectora. Combina embedding (Voyage 4) + AST parsing + reranking (Voyage Rerank 2.5) para máxima precisão.

**Entrada (JSON-RPC params)**:

```json
{
  "query": "como validar tokens JWT?",
  "namespace": "auth-module",
  "top_k": 10,
  "strategy": "hybrid",
  "filters": {
    "language": "typescript",
    "file_path": "src/auth/**"
  },
  "timeout_ms": 30000
}
```

**Saída**:

```json
{
  "chunks": [
    {
      "file_path": "src/auth/jwt-validator.ts",
      "start_line": 42,
      "end_line": 58,
      "content": "export function validateToken(token: string): boolean { ... }",
      "relevance_score": 0.94,
      "matched_entities": ["validateToken", "JWT"],
      "context_type": "function"
    }
  ],
  "metrics": {
    "total_candidates": 234,
    "after_rerank": 10,
    "query_embedding_time_ms": 45,
    "search_time_ms": 120,
    "rerank_time_ms": 35,
    "total_time_ms": 200
  },
  "query_analysis": {
    "detected_intent": "explain",
    "extracted_entities": ["JWT", "validation"],
    "suggested_follow_up": ["token refresh", "expiration handling"]
  }
}
```

**Lógica Interna**:

1. **Query Analysis** (Gemini 3 Flash)

   - Extrai intent (search, explain, compare, debug)
   - Identifica entidades relevantes
   - Detecta linguagem de programação

2. **Embedding**

   - Voyage 4 embedding da query (com retry exponential)
   - Cache de embeddings para queries repetidas

3. **Vector Search**

   - MongoDB Atlas HNSW com namespace filtering
   - Top-K\*5 para dar espaço para reranking

4. **Structural Search** (paralelo a vector)

   - AST parsing (go/parser, @babel/parser)
   - Keyword matching com índices secundários
   - Caminho de arquivo (glob patterns)

5. **Merge de Resultados**

   - Deduplicate (mesmo arquivo/linha)
   - Score normalization (0-1)

6. **Reranking**

   - Voyage Rerank 2.5 top-50 → top-10
   - Fallback se reranker falhar

7. **Composição Final**
   - Contexto estruturado (head/tail compression)
   - Métricas de latência e relevância

**Dependências Internas**:

- `internal/harness` — ExecuteProviderAPI, timeout management
- `internal/guardian` — Validação de paths
- `pkg/mcp/auth` — AuthContext para namespace filtering
- `internal/context-engine` — Parser AST, search methods
- `internal/provider-router` — Gemini, Voyage APIs

**Tests**:

```go
// pkg/mcp/tools/search_context_test.go
func TestSearchContextBasic(t *testing.T) {
    // Setup mock engine, providers
    server := NewTestMCPServer(mockEngine, mockProviders)

    params := SearchContextParams{
        Query: "validate token",
        Namespace: "test-ns",
    }

    result, err := tools.SearchContext(server, params)
    require.NoError(t, err)
    assert.Len(t, result.Chunks, 10) // default top_k
    assert.Greater(t, result.Chunks[0].RelevanceScore, 0.7)
}

func TestSearchContextTimeouts(t *testing.T) {
    // Test 30s timeout, fallback behavior
}

func TestSearchContextEmptyResults(t *testing.T) {
    // Zero matches, graceful handling
}

func TestSearchContextLargeQuery(t *testing.T) {
    // >10000 chars, validation
}
```

**Critério de Aceitação**:

- [x] Latência P95 < 300ms (sem cache), < 50ms (com cache)
- [x] Recall >= 85% em benchmark set (vs OpenAI)
- [x] Suporta `semantic`, `structural`, `hybrid` strategies
- [x] Fallback gracioso se reranker falha
- [x] Namespace isolation (sem vazamento entre users)

---

### 1.2 `search_tests` — Localizar Testes Relacionados

**Responsabilidade**: Encontra testes relacionados a um trecho de código (arquivo, função, classe).

**Entrada**:

```json
{
  "code_path": "src/auth/jwt-validator.ts",
  "code_snippet": "export function validateToken(token: string): boolean",
  "namespace": "auth-module",
  "include_integration_tests": true,
  "max_results": 15
}
```

**Saída**:

```json
{
  "unit_tests": [
    {
      "test_file": "src/auth/__tests__/jwt-validator.test.ts",
      "test_name": "validateToken with valid JWT returns true",
      "relevance": 0.98,
      "test_type": "unit",
      "line_range": [10, 25]
    }
  ],
  "integration_tests": [
    {
      "test_file": "src/e2e/auth-flow.test.ts",
      "test_name": "User login with JWT flow",
      "relevance": 0.72,
      "test_type": "e2e",
      "line_range": [45, 65]
    }
  ],
  "metrics": {
    "unit_tests_found": 5,
    "integration_tests_found": 2,
    "avg_relevance": 0.85
  }
}
```

**Lógica**:

1. Extrai função/classe nome de `code_snippet`
2. Busca `*.test.ts`, `*.spec.ts`, `_test.go` files
3. Procura por imports/references do código
4. Reranking por relevância (match score)

**Dependências**: `internal/context-engine` (AST parsing para extração de função)

**Critério de Aceitação**:

- [x] Encontra >= 90% de testes relacionados
- [x] Ordena por relevância
- [x] Suporta múltiplas convenções de nomes (`*.test.ts`, `*_test.go`, etc)

---

### 1.3 `find_similar_code` — Padrões de Código Similar

**Responsabilidade**: Localiza padrões de código similares (clones, refatoring candidates).

**Entrada**:

```json
{
  "code_snippet": "function hashPassword(pwd) { return bcrypt.hash(pwd, 10); }",
  "language": "typescript",
  "namespace": "auth-module",
  "similarity_threshold": 0.75,
  "limit": 10
}
```

**Saída**:

```json
{
  "similar_chunks": [
    {
      "file_path": "src/user/password-utils.ts",
      "start_line": 30,
      "content": "const hashedPwd = await bcrypt.hash(password, 10);",
      "similarity_score": 0.89,
      "similarity_type": "semantic"
    }
  ],
  "potential_refactoring": "Extrair ambos em função utilitária compartilhada"
}
```

**Lógica**:

1. Normaliza código (remove comentários, whitespace)
2. Gera embedding do snippet
3. Busca chunks similares em embeddings
4. Calcula AST similarity também
5. Combina scores

**Critério de Aceitação**:

- [x] Detecta code clones com 90%+ similarity
- [x] Suporta threshold customizável

---

### 1.4 `analyze_dependencies` — Quem Chama X?

**Responsabilidade**: Mostra call graph (quem chama função/classe).

**Entrada**:

```json
{
  "target_name": "validateToken",
  "target_type": "function",
  "target_file": "src/auth/jwt-validator.ts",
  "namespace": "auth-module",
  "depth": 2
}
```

**Saída**:

```json
{
  "direct_callers": [
    {
      "caller_file": "src/routes/login.ts",
      "caller_name": "loginHandler",
      "line": 42,
      "context": "const isValid = await validateToken(token);"
    }
  ],
  "indirect_callers": [
    {
      "caller_file": "src/middleware/auth.ts",
      "depth": 1
    }
  ],
  "dependency_graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

**Lógica**: AST traversal, importância análise

**Critério de Aceitação**:

- [x] Encontra callers em profundidade customizável
- [x] Suporta múltiplas linguagens

---

## Grupo 2: Navigation & Structure (1.5 semanas)

### 2.1 `get_file_structure` — Resumo Estruturado

**Responsabilidade**: AST parsing → estrutura hierárquica (funções, classes, imports).

**Entrada**:

```json
{
  "file_path": "src/auth/jwt-validator.ts",
  "namespace": "auth-module",
  "detail_level": "summary"
}
```

**Saída**:

```json
{
  "file_path": "src/auth/jwt-validator.ts",
  "language": "typescript",
  "summary": "Validates JWT tokens with custom claims...",
  "imports": [
    { "name": "jsonwebtoken", "alias": "jwt" },
    { "name": "./types", "imports": ["TokenPayload"] }
  ],
  "exports": ["validateToken", "verifySignature"],
  "functions": [
    {
      "name": "validateToken",
      "type": "function",
      "line": 42,
      "params": ["token: string"],
      "returns": "boolean",
      "jsdoc": "Validates JWT token and returns true if valid"
    }
  ],
  "classes": [...],
  "types": [
    { "name": "TokenPayload", "definition": "interface TokenPayload { ... }" }
  ]
}
```

**Lógica**: AST parsing com comentários extraídos

**Critério de Aceitação**:

- [x] Suporta Go, TypeScript, Python
- [x] Extrai comments/docstrings

---

### 2.2 `list_files` — Arquivos Indexados

**Responsabilidade**: Lista arquivos/recursos no namespace.

**Entrada**:

```json
{
  "namespace": "auth-module",
  "pattern": "*.ts",
  "limit": 50
}
```

**Saída**:

```json
{
  "files": [
    {
      "path": "src/auth/jwt-validator.ts",
      "size_bytes": 2048,
      "indexed_at": "2026-04-21T10:00:00Z",
      "last_modified": "2026-04-20T15:30:00Z",
      "language": "typescript",
      "lines": 145
    }
  ],
  "total": 23,
  "namespace": "auth-module"
}
```

**Critério de Aceitação**:

- [x] Filtra por padrão
- [x] Retorna metadados

---

### 2.3 `list_namespaces` — Namespaces

**Responsabilidade**: Lista namespaces disponíveis.

**Entrada**: `{}`

**Saída**:

```json
{
  "namespaces": [
    {
      "name": "auth-module",
      "files_count": 23,
      "total_lines": 2500,
      "indexed_at": "2026-04-20T10:00:00Z"
    }
  ]
}
```

---

### 2.4 `get_session_state` — Contexto de Sessão

**Responsabilidade**: Retorna histórico de queries e contexto da sessão.

**Entrada**:

```json
{
  "session_id": "sess_abc123",
  "limit": 10
}
```

**Saída**:

```json
{
  "session_id": "sess_abc123",
  "user_id": "user_123",
  "created_at": "2026-04-21T10:00:00Z",
  "queries": [
    {
      "query": "validate token",
      "timestamp": "2026-04-21T10:05:00Z",
      "results_count": 10
    }
  ],
  "context_window": {
    "total_tokens": 5000,
    "remaining_tokens": 2000
  }
}
```

---

## Grupo 3: Management & Utilities (1 semana)

### 3.1 `index_progress` — Status de Indexação

**Saída**:

```json
{
  "status": "indexing",
  "progress_percent": 65,
  "files_processed": 150,
  "files_total": 230,
  "estimated_time_remaining_seconds": 120,
  "current_file": "src/auth/oauth-handler.ts"
}
```

---

### 3.2 `validate_query` — Validação de Query

**Entrada**: `{ "query": "..." }`

**Saída**:

```json
{
  "valid": true,
  "warnings": [],
  "estimated_results": 12,
  "estimated_latency_ms": 200
}
```

---

### 3.3 `get_metrics` — Métricas

**Saída**:

```json
{
  "queries_today": 150,
  "avg_latency_ms": 180,
  "avg_relevance_score": 0.87,
  "errors": 2,
  "cache_hit_rate": 0.34
}
```

---

### 3.4 `export_context` — Exportar Contexto

**Entrada**:

```json
{
  "format": "markdown",
  "include_metrics": true
}
```

**Saída**: Base64-encoded contexto completo

---

## Timeline & Dependências

```text
Semana 1:
  Dia 1-3: Group 1 — search_context (framework JSON-RPC já existe)
  Dia 4-5: Group 1 — search_tests, find_similar_code
  Dia 5-7: Group 1 — analyze_dependencies

Semana 2:
  Dia 1-3: Group 2 — get_file_structure, list_files
  Dia 4-6: Group 2 — list_namespaces, get_session_state
  Dia 7: Buffer/testing

Semana 3:
  Dia 1-3: Group 3 — index_progress, validate_query
  Dia 4-5: Group 3 — get_metrics, export_context
  Dia 6-7: Integration testing, conformance tests
```

**Dependências Críticas**:

- [x] Harness Runtime (para execução segura)
- [x] Context Engine (AST parsing, búsqueda)
- [x] Provider Router (Gemini, Voyage APIs)
- [x] Guardian (validação de paths)
- [x] MongoDB driver (persistência)

---

## Critérios de Aceitação Globais

[x] Todas as 12 ferramentas implementadas em Go
[x] JSON-RPC 2.0 compliant (spec MCP 2024-04)
[x] Latência P95 < 500ms para cada ferramenta
[x] Teste coverage >= 80%
[x] Documentação completa (exemplos, schemas)
[x] Especification conformance tests passing

---

## External Linking

| Concept               | Resource                             | Link                                                                                   |
| --------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **AST Parsing**       | Tree-sitter Official Documentation   | [tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/)       |
| **JWT**               | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |
| **MCP**               | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Voyage Embeddings** | Voyage Embeddings Documentation      | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)         |
| **Voyage Reranker**   | Voyage Reranker API                  | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)             |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
