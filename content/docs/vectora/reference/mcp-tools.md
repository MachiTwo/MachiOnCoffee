---
title: MCP Tools
slug: mcp-tools
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - chatgpt
  - concepts
  - config
  - errors
  - mcp
  - mcp-protocol
  - protocol
  - reference
  - security
  - state
  - system
  - tools
  - trust-folder
  - vectora
  - yaml
---

{{< lang-toggle >}}
{{< section-toggle >}}

Este é um **dicionário completo** de todas as ferramentas MCP oferecidas pelo Vectora. Use-as via Claude Code, Cursor, VS Code ou ChatGPT para interagir com seu codebase.

> [!IMPORTANT] Todas as tools respeitam sua **Trust Folder** e **Namespace**. Nenhum arquivo fora desses limites é acessável.

## Categorias

1. **Search & Retrieval** — Buscar contexto
2. **Analysis** — Analisar relações de código
3. **Metadata** — Listar e inspecionar
4. **Indexing** — Gerenciar índices
5. **Configuration** — Configurar Vectora
6. **Monitoring** — Métricas e saúde

## Search & Retrieval

As ferramentas de busca e recuperação permitem extrair contexto relevante do seu repositório usando algoritmos de similaridade semântica e estrutural.

## `search_context`

Busca semântica por chunks relevantes.

**Parâmetros**:

```json
{
  "query": "string", // Sua pergunta
  "namespace": "string", // Namespace (default: config)
  "top_k": 10, // Quantos resultados (default: 10)
  "strategy": "semantic|structural|hybrid" // Tipo de busca
}
```

**Response**:

```json
{
  "chunks": [
    {
      "id": "chunk_123",
      "file": "src/auth/jwt.ts",
      "line_start": 45,
      "line_end": 67,
      "content": "export function validateToken...",
      "precision": 0.87,
      "relevance_score": 0.92
    }
  ],
  "metadata": {
    "query_time_ms": 234,
    "total_chunks_searched": 3159
  }
}
```

**Exemplo**:

```text
@vectora search_context "Como validar JWT tokens?"
```

## `search_tests`

Busca testes relacionados a uma query.

**Parâmetros**:

```json
{
  "query": "string",
  "include_test_files": true,
  "top_k": 5,
  "namespace": "string"
}
```

**Response**:

```json
{
  "tests": [
    {
      "file": "spec/auth.test.ts",
      "test_name": "should validate expired token",
      "line": 45,
      "relevance": 0.89
    }
  ]
}
```

## Analysis

As ferramentas de análise permitem entender as relações complexas entre componentes do código, dependências e padrões estruturais.

## `analyze_dependencies`

Encontra todas as referências a um símbolo.

**Parâmetros**:

```json
{
  "symbol": "getUserById", // Função/variável
  "type": "function|class|variable",
  "include_indirect": true, // Incluir chamadas indiretas?
  "namespace": "string"
}
```

**Response**:

```json
{
  "direct_calls": 47,
  "indirect_calls": 12,
  "callers": [
    {
      "file": "src/middleware/auth.ts",
      "line": 34,
      "context": "const user = await getUserById(id)"
    }
  ],
  "definition": {
    "file": "src/user-service.ts",
    "line": 12
  }
}
```

## `find_similar_code`

Encontra código similar a um trecho fornecido.

**Parâmetros**:

```json
{
  "code": "string", // Código para comparar
  "language": "go|python|typescript",
  "min_similarity": 0.7,
  "top_k": 5,
  "namespace": "string"
}
```

**Response**:

```json
{
  "similar_chunks": [
    {
      "file": "src/auth/guards.ts",
      "similarity": 0.85,
      "content": "..."
    }
  ]
}
```

## `get_file_structure`

Resume a estrutura de um arquivo (imports, funções, classes).

**Parâmetros**:

```json
{
  "file_path": "src/auth/jwt.ts",
  "include_comments": false,
  "namespace": "string"
}
```

**Response**:

```json
{
  "file": "src/auth/jwt.ts",
  "language": "go",
  "imports": ["jsonwebtoken", "./types"],
  "exports": ["validateToken", "signToken"],
  "functions": [
    {
      "name": "validateToken",
      "line": 45,
      "params": ["token: string"],
      "return_type": "boolean"
    }
  ],
  "classes": [],
  "size_bytes": 2048
}
```

## Metadata

Inspecione a organização do seu workspace, liste arquivos indexados e verifique estatísticas vitais sobre seus namespaces.

## `list_files`

Lista arquivos indexados no namespace.

**Parâmetros**:

```json
{
  "namespace": "string",
  "pattern": "**/*.ts", // Glob pattern (opcional)
  "limit": 100
}
```

**Response**:

```json
{
  "files": [
    {
      "path": "src/auth/jwt.ts",
      "chunks": 15,
      "size_bytes": 2048,
      "last_indexed": "2026-04-19T10:30:00Z"
    }
  ],
  "total": 247,
  "namespace": "seu-namespace"
}
```

## `list_namespaces`

Lista todos os namespaces disponíveis.

**Parâmetros**:

```json
{
  "filter": "owned|shared|all" // Opcional
}
```

**Response**:

```json
{
  "namespaces": [
    {
      "name": "kaffyn-vectora-prod",
      "chunks": 3159,
      "created_at": "2026-01-10T00:00:00Z",
      "owner": "você@seu-email.com",
      "permissions": "owner"
    }
  ]
}
```

## `get_namespace_stats`

Retorna estatísticas de um namespace.

**Parâmetros**:

```json
{
  "namespace": "string"
}
```

**Response**:

```json
{
  "namespace": "kaffyn-vectora-prod",
  "total_chunks": 3159,
  "total_files": 247,
  "total_size_mb": 15.3,
  "languages": {
    "go": 2100,
    "markdown": 800,
    "yaml": 259
  },
  "search_stats_24h": {
    "total_queries": 342,
    "avg_precision": 0.78,
    "avg_latency_ms": 234
  }
}
```

</details>

## Indexing

Gerencie o estado de indexação do seu projeto, forcando atualizações ou verificando pendências no banco de dados vetorial.

<details>
<summary>Expandir/Recolher seção de Indexing</summary>

## `index_status`

Verifica o status do índice (saúde, pendências).

**Parâmetros**:

```json
{
  "namespace": "string",
  "include_pending": true
}
```

**Response**:

```json
{
  "namespace": "seu-namespace",
  "health": "healthy",
  "indexed_chunks": 3159,
  "pending_chunks": 12,
  "last_index_time": "2026-04-19T10:30:00Z",
  "index_size_mb": 15.3,
  "estimated_time_remaining": "2 minutes"
}
```

## `reindex`

Força re-indexação de arquivos.

**Parâmetros**:

```json
{
  "files": ["src/auth/**/*.ts"], // Glob patterns
  "namespace": "string",
  "force": false // Reindexar mesmo se não mudou?
}
```

**Response**:

```json
{
  "status": "started",
  "files_queued": 45,
  "estimated_time_sec": 120,
  "job_id": "index_job_abc123"
}
```

## Configuration

Acesse e modifique as configurações operacionais do servidor Vectora em tempo real, permitindo ajustes finos de estratégias de busca.

## `get_config`

Retorna configuração atual do Vectora.

**Parâmetros**:

```json
{
  "include_secrets": false // Incluir chaves de API?
}
```

**Response**:

```json
{
  "project": {
    "name": "Meu Projeto",
    "namespace": "seu-namespace"
  },
  "context_engine": {
    "strategy": "semantic",
    "max_depth": 3
  }
}
```

## `set_config`

Modifica configuração (requer autenticação).

**Parâmetros**:

```json
{
  "path": "context_engine.strategy", // Caminho no YAML
  "value": "hybrid"
}
```

## Monitoring

Mantenha a visibilidade total sobre o desempenho do sistema, taxas de erro e logs de auditoria para garantir segurança e performance.

## `get_metrics`

Retorna métricas de execução.

**Parâmetros**:

```json
{
  "namespace": "string",
  "period": "24h|7d|30d",
  "metrics": ["precision", "latency", "errors"]
}
```

**Response**:

```json
{
  "period": "24h",
  "metrics": {
    "queries": 342,
    "avg_precision": 0.78,
    "avg_latency_ms": 234,
    "errors": 3,
    "error_rate": 0.009
  }
}
```

## `get_audit_log`

Retorna log de acessos e modificações.

**Parâmetros**:

```json
{
  "namespace": "string",
  "since": "2026-04-18T00:00:00Z",
  "action": "search|index|delete", // Filtrar por tipo
  "limit": 100
}
```

**Response**:

```json
{
  "logs": [
    {
      "timestamp": "2026-04-19T10:30:00Z",
      "action": "search",
      "query": "Como validar tokens?",
      "user": "você@seu-email.com",
      "namespace": "seu-namespace",
      "result": "success"
    }
  ]
}
```

## Exemplos Práticos (Workflows Reais)

Nesta seção, demonstramos como as ferramentas MCP trabalham em conjunto para resolver problemas reais de desenvolvimento. Cada workflow mostra a sequência de tools chamadas e outputs esperados em cenários práticos.

## Workflow 1: Entender Função Desconhecida

**Cenário**: Você encontrou `validateToken()` em um arquivo. Quer entender onde é usada.

**Step-by-Step com Tools:**

```text
1⃣ get_file_structure("src/auth/jwt.ts")
   Resultado: validateToken está em linha 45, retorna boolean

2⃣ analyze_dependencies(symbol="validateToken")
   Resultado: 47 chamadas diretas em guards.ts, middleware/auth.ts, etc

3⃣ search_tests(query="validateToken")
   Resultado: 8 testes relacionados (spec/auth.test.ts)

4⃣ find_similar_code(code="function validateToken...")
   Resultado: Similar pattern em getUser() (85% match)

Output Final:
   ├─ Função: validateToken (linha 45, src/auth/jwt.ts)
   ├─ Usado em: 47 places (guards.ts principal)
   ├─ Testes: 8 (auth.test.ts, jwt.test.ts, etc)
   └─ Padrão similar: getUser() function
```

Esse workflow mostra como usar tools em sequência para identificar uma função e seu contexto completo.

## Workflow 2: Debugging de Erro em Production

**Cenário**: API está lenta. Precisa entender se é auth validation.

**Tools em Sequência:**

```text
1⃣ get_metrics(period="24h")
   Resultado: latency avg=234ms, p95=800ms (acima do SLA 300ms)

2⃣ search_context(query="validação de tokens")
   Resultado: 5 chunks (jwt.ts, guards.ts, middleware.ts)

3⃣ get_file_structure("src/auth/jwt.ts")
   Resultado: validateToken(line 45), signToken(line 89)

4⃣ analyze_dependencies(symbol="validateToken")
   Resultado: 47 chamadas, 12 indiretas (via middleware)

5⃣ search_tests(query="validateToken performance")
   Resultado: Nenhum teste de performance específico!

Conclusão:
    validateToken é chamado em 47 places
    Sem testes de performance específicos
    Recomendação: Profile validateToken, adicionar cache
```

Quando performance degrada, as tools ajudam a diagnosticar a causa raiz. Este workflow combina métricas, busca e análise estrutural.

## Workflow 3: Code Review Automático

**Cenário**: PR adiciona novo handler. Quer verificar padrão.

**Tools:**

```text
1⃣ search_context(query="user handler pattern")
   Resultado: 8 handlers similares encontrados

2⃣ find_similar_code(code="async function handle(...)")
   Resultado: Seu PR é 92% similar a userController.ts

3⃣ analyze_dependencies(symbol="getUserById")
   Resultado: Verifica se novo handler segue mesmo padrão

4⃣ search_tests(query="user handler tests")
   Resultado: 12 testes de padrão similar

5⃣ get_file_structure(file_path="seu-novo-handler.ts")
   Resultado: Estrutura validada (imports, exports, functions)

Review Output:
    Código segue padrão existente (92% match)
    Testes similares existem (12 found)
    Imports corretos (validateToken via guards)
    Erro handling: veja exemplo em userHandler.ts:56
   → Pronto para merge (com sugestão)
```

Validar que uma PR segue os padrões do projeto envolve buscar código similar e verificar estrutura. Este workflow automatiza boa parte dessa análise.

## Workflow 4: Refatoração em Escala

**Cenário**: Quer mudar como tokens são validados. Precisa entender impacto.

**Tools:**

```text
1⃣ analyze_dependencies(symbol="validateToken")
   Resultado: 47 chamadas diretas, 12 indiretas

2⃣ list_files(pattern="**/*.ts", limit=100)
   Resultado: 247 arquivos Go

3⃣ search_context(query="JWT validation authentication")
   Resultado: 15 chunks relacionados

4⃣ get_file_structure para cada arquivo que toca validateToken
   Resultado: Confirma 47 + 12 = 59 locais afetados

5⃣ search_tests(query="validateToken authorization")
   Resultado: 8 testes que precisam passar

6⃣ reindex(files=["src/auth/**/*.ts"], force=true)
   Resultado: Re-index em preparação para mudanças

Impact Assessment:
   ├─ Files: 59 (47 direct + 12 indirect)
   ├─ Tests: 8 (todos precisam passar)
   ├─ Risco: MÉDIO (centralizado em auth/)
   ├─ Esforço: ~2 horas (refactor) + 1 hora (testes)
   └─ Recomendação:
       1. Fazer mudança em jwt.ts:45
       2. Rodar ./src/__tests__/auth.test.ts
       3. Merge quando tudo passar
```

Entender o impacto de uma mudança é crítico. Este workflow usa tools para mapear todos os locais afetados e o esforço estimado.

## Workflow 5: Monitoramento & Auditoria

**Cenário**: Segurança. Quer garantir que dados sensíveis não foram acessados.

**Tools:**

```text
1⃣ get_audit_log(action="search", since="24h")
   Resultado: Todas as buscas das últimas 24h

2⃣ get_audit_log(action="index", since="24h")
   Resultado: Todas as indexações das últimas 24h

3⃣ list_files(pattern=".env*")
   Resultado: Nenhum arquivo .env (GOOD - Trust Folder blocked)

4⃣ list_files(pattern="*.key|*.pem|*.secret")
   Resultado: Nenhum arquivo sensível (GOOD)

5⃣ get_namespace_stats()
   Resultado:
      ├─ total_chunks: 3159
      ├─ languages: {go: 2100, markdown: 800}
      ├─ searches_24h: 342
      └─ error_rate: 0.009 (saudável)

Security Summary:
    Sem arquivos .env indexados
    Sem chaves privadas detectadas
    Sem acessos suspeitos
    342 buscas legítimas
   → Sistema seguro
```

## Error Handling

Todas as tools retornam erros estruturados:

```json
{
  "error": {
    "code": "INVALID_NAMESPACE",
    "message": "Namespace 'unknown' not found",
    "timestamp": "2026-04-19T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

---

> **Próximo**: [CLI Reference](./cli.md)

---

## External Linking

| Concept              | Resource                             | Link                                                                                   |
| -------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **JWT**              | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |
| **MCP**              | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**       | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude** | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
