---
title: MCP Tools
slug: mcp-tools
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - mcp-protocol
  - tools
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

This is a **complete dictionary** of all MCP tools offered by Vectora. Use them via Claude Code, Cursor, VS Code, or ChatGPT to interact with your codebase.

> [!IMPORTANT]
> All tools respect your **Trust Folder** and **Namespace**. No files outside these boundaries are accessible.

## Categories

1. **Search & Retrieval** — Search for context
2. **Analysis** — Analyze code relationships
3. **Metadata** — List and inspect
4. **Indexing** — Manage indexes
5. **Configuration** — Configure Vectora
6. **Monitoring** — Metrics and health

## Search & Retrieval

Search and retrieval tools allow you to extract relevant context from your repository using semantic and structural similarity algorithms.

## `search_context`

Semantic search for relevant chunks.

**Parameters**:

```json
{
  "query": "string", // Your question
  "namespace": "string", // Namespace (default: from config)
  "top_k": 10, // Number of results (default: 10)
  "strategy": "semantic|structural|hybrid" // Search type
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

**Example**:

```text
@vectora search_context "How to validate JWT tokens?"
```

## `search_tests`

Search for tests related to a query.

**Parameters**:

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

Analysis tools allow you to understand complex relationships between code components, dependencies, and structural patterns.

## `analyze_dependencies`

Finds all references to a symbol.

**Parameters**:

```json
{
  "symbol": "getUserById", // Function/variable
  "type": "function|class|variable",
  "include_indirect": true, // Include indirect calls?
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

Finds code similar to a provided snippet.

**Parameters**:

```json
{
  "code": "string", // Code to compare
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

Summarizes a file's structure (imports, functions, classes).

**Parameters**:

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

Inspect the organization of your workspace, list indexed files, and check vital statistics about your namespaces.

## `list_files`

Lists indexed files in the namespace.

**Parameters**:

```json
{
  "namespace": "string",
  "pattern": "**/*.ts", // Glob pattern (optional)
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
  "namespace": "your-namespace"
}
```

## `list_namespaces`

Lists all available namespaces.

**Parameters**:

```json
{
  "filter": "owned|shared|all" // Optional
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
      "owner": "you@your-email.com",
      "permissions": "owner"
    }
  ]
}
```

## `get_namespace_stats`

Returns statistics for a namespace.

**Parameters**:

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

## Indexing

Manage your project's indexing state, forcing updates or checking for pending items in the vector database.

## `index_status`

Checks index status (health, pending items).

**Parameters**:

```json
{
  "namespace": "string",
  "include_pending": true
}
```

**Response**:

```json
{
  "namespace": "your-namespace",
  "health": "healthy",
  "indexed_chunks": 3159,
  "pending_chunks": 12,
  "last_index_time": "2026-04-19T10:30:00Z",
  "index_size_mb": 15.3,
  "estimated_time_remaining": "2 minutes"
}
```

## `reindex`

Forces file re-indexing.

**Parameters**:

```json
{
  "files": ["src/auth/**/*.ts"], // Glob patterns
  "namespace": "string",
  "force": false // Reindex even if unchanged?
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

Access and modify Vectora server operational settings in real-time, allowing for fine-tuning of search strategies.

## `get_config`

Returns current Vectora configuration.

**Parameters**:

```json
{
  "include_secrets": false // Include API keys?
}
```

**Response**:

```json
{
  "project": {
    "name": "My Project",
    "namespace": "your-namespace"
  },
  "context_engine": {
    "strategy": "semantic",
    "max_depth": 3
  }
}
```

## `set_config`

Modifies configuration (requires authentication).

**Parameters**:

```json
{
  "path": "context_engine.strategy", // Path in YAML
  "value": "hybrid"
}
```

## Monitoring

Maintain full visibility into system performance, error rates, and audit logs to ensure security and performance.

## `get_metrics`

Returns execution metrics.

**Parameters**:

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

Returns access and modification logs.

**Parameters**:

```json
{
  "namespace": "string",
  "since": "2026-04-18T00:00:00Z",
  "action": "search|index|delete", // Filter by type
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
      "query": "How to validate tokens?",
      "user": "you@your-email.com",
      "namespace": "your-namespace",
      "result": "success"
    }
  ]
}
```

## Practical Examples (Real Workflows)

In this section, we demonstrate how MCP tools work together to solve real development problems. Each workflow shows the sequence of tools called and expected outputs in practical scenarios.

## Workflow 1: Understanding an Unknown Function

- **Scenario**: You found `validateToken()` in a file. You want to understand where it is used.

  **Step-by-Step with Tools:**

```text
1⃣ get_file_structure("src/auth/jwt.ts")
   Result: validateToken is on line 45, returns boolean

2⃣ analyze_dependencies(symbol="validateToken")
   Result: 47 direct calls in guards.ts, middleware/auth.ts, etc.

3⃣ search_tests(query="validateToken")
   Result: 8 related tests (spec/auth.test.ts)

4⃣ find_similar_code(code="function validateToken...")
   Result: Similar pattern in getUser() (85% match)

Final Output:
   ├─ Function: validateToken (line 45, src/auth/jwt.ts)
   ├─ Used in: 47 places (guards.ts principal)
   ├─ Tests: 8 (auth.test.ts, jwt.test.ts, etc.)
   └─ Similar pattern: getUser() function
```

This workflow shows how to use tools in sequence to identify a function and its complete context.

## Workflow 2: Debugging a Production Error

**Scenario**: API is slow. Need to understand if it's auth validation.

**Tools in Sequence:**

```text
1⃣ get_metrics(period="24h")
   Result: latency avg=234ms, p95=800ms (above the 300ms SLA)

2⃣ search_context(query="token validation")
   Result: 5 chunks (jwt.ts, guards.ts, middleware.ts)

3⃣ get_file_structure("src/auth/jwt.ts")
   Result: validateToken(line 45), signToken(line 89)

4⃣ analyze_dependencies(symbol="validateToken")
   Result: 47 calls, 12 indirect (via middleware)

5⃣ search_tests(query="validateToken performance")
   Result: No specific performance tests!

Conclusion:
    validateToken is called in 47 places
    No specific performance tests
    Recommendation: Profile validateToken, add cache
```

When performance degrades, tools help diagnose the root cause. This workflow combines metrics, search, and structural analysis.

## Workflow 3: Automatic Code Review

**Scenario**: PR adds a new handler. Want to verify patterns.

**Tools:**

```text
1⃣ search_context(query="user handler pattern")
   Result: 8 similar handlers found

2⃣ find_similar_code(code="async function handle(...)")
   Result: Your PR is 92% similar to userController.ts

3⃣ analyze_dependencies(symbol="getUserById")
   Result: Verifies if new handler follows the same pattern

4⃣ search_tests(query="user handler tests")
   Result: 12 tests with a similar pattern

5⃣ get_file_structure(file_path="your-new-handler.ts")
   Result: Structure validated (imports, exports, functions)

Review Output:
    Code follows existing pattern (92% match)
    Similar tests exist (12 found)
    Correct imports (validateToken via guards)
    Error handling: see example in userHandler.ts:56
   → Ready for merge (with suggestion)
```

Validating that a PR follows project standards involves searching for similar code and verifying structure. This workflow automates much of this analysis.

## Workflow 4: Large-Scale Refactoring

**Scenario**: Want to change how tokens are validated. Need to understand the impact.

**Tools:**

```text
1⃣ analyze_dependencies(symbol="validateToken")
   Result: 47 direct calls, 12 indirect calls

2⃣ list_files(pattern="**/*.ts", limit=100)
   Result: 247 Go files

3⃣ search_context(query="JWT validation authentication")
   Result: 15 related chunks

4⃣ get_file_structure for each file touching validateToken
   Result: Confirms 47 + 12 = 59 affected locations

5⃣ search_tests(query="validateToken authorization")
   Result: 8 tests that must pass

6⃣ reindex(files=["src/auth/**/*.ts"], force=true)
   Result: Re-index in preparation for changes

Impact Assessment:
   ├─ Files: 59 (47 direct + 12 indirect)
   ├─ Tests: 8 (all must pass)
   ├─ Risk: MEDIUM (centralized in auth/)
   ├─ Effort: ~2 hours (refactor) + 1 hour (tests)
   └─ Recommendation:
       1. Make change in jwt.ts:45
       2. Run ./src/__tests__/auth.test.ts
       3. Merge when everything passes
```

Understanding the impact of a change is critical. This workflow uses tools to map all affected locations and the estimated effort.

## Workflow 5: Monitoring & Audit

**Scenario**: Security. Want to ensure sensitive data has not been accessed.

**Tools:**

```text
1⃣ get_audit_log(action="search", since="24h")
   Result: All searches from the last 24h

2⃣ get_audit_log(action="index", since="24h")
   Result: All indexing from the last 24h

3⃣ list_files(pattern=".env*")
   Result: No .env files (GOOD - Trust Folder blocked)

4⃣ list_files(pattern="*.key|*.pem|*.secret")
   Result: No sensitive files (GOOD)

5⃣ get_namespace_stats()
   Result:
      ├─ total_chunks: 3159
      ├─ languages: {go: 2100, markdown: 800}
      ├─ searches_24h: 342
      └─ error_rate: 0.009 (healthy)

Security Summary:
    No .env files indexed
    No private keys detected
    No suspicious accesses
    342 legitimate searches
   → Secure system
```

## Error Handling

All tools return structured errors:

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

> **Next**: [CLI Reference](./cli.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
