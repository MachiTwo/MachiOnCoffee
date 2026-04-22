---
title: Plano de Implementação - MCP Server (JSON-RPC)
slug: mcp-server
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - ai
  - auth
  - concepts
  - embeddings
  - engineering
  - errors
  - golang
  - harness-runtime
  - integration
  - json-rpc
  - mcp
  - protocol
  - rbac
  - tools
  - vector-search
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

O **MCP Server** é a interface pública do Vectora, expondo 12 ferramentas via JSON-RPC 2.0 sobre stdio. Este documento detalha a implementação em Go com conformidade total ao spec MCP.

## Especificação MCP Implementada

- **Protocolo**: JSON-RPC 2.0
- **Transporte**: Stdio (pipe-based)
- **Autenticação**: JWT via MCP headers
- **Versão MCP**: 2024-04

## Fases de Implementação

### **Fase 1: JSON-RPC 2.0 Server Framework**

**Duração**: 1 semana

**Deliverables**:

- [ ] Stdio server loop
- [ ] JSON marshaling/unmarshaling
- [ ] Request/response routing
- [ ] Error codes conformes a spec

**Código de Exemplo**:

```go
// pkg/mcp/server.go
package mcp

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io"
    "os"
    "sync"
)

// JSONRPCMessage implementa spec JSON-RPC 2.0
type JSONRPCMessage struct {
    JSONRPC string `json:"jsonrpc"`
    ID interface{} `json:"id,omitempty"`
    Method string `json:"method,omitempty"`
    Params json.RawMessage `json:"params,omitempty"`
    Result interface{} `json:"result,omitempty"`
    Error *JSONRPCError `json:"error,omitempty"`
}

type JSONRPCError struct {
    Code int `json:"code"`
    Message string `json:"message"`
    Data interface{} `json:"data,omitempty"`
}

// Error codes para MCP
const (
    ParseError = -32700 // Invalid JSON
    InvalidRequest = -32600 // Invalid Request
    MethodNotFound = -32601 // Method not found
    InvalidParams = -32602 // Invalid params
    InternalError = -32603 // Internal error
    ServerErrorBase = -32000
)

type MethodHandler func(params json.RawMessage) (interface{}, error)

type Server struct {
    mu sync.RWMutex
    methods map[string]MethodHandler
    reader *bufio.Reader
    writer *bufio.Writer
}

func NewServer() *Server {
    return &Server{
        methods: make(map[string]MethodHandler),
        reader: bufio.NewReader(os.Stdin),
        writer: bufio.NewWriter(os.Stdout),
    }
}

func (s *Server) RegisterMethod(name string, handler MethodHandler) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.methods[name] = handler
}

func (s *Server) Start() error {
    for {
        line, err := s.reader.ReadString('\n')
        if err == io.EOF {
            return nil
        }
        if err != nil {
            s.sendError(nil, ParseError, "Failed to read message")
            continue
        }

        var msg JSONRPCMessage
        if err := json.Unmarshal([]byte(line), &msg); err != nil {
            s.sendError(nil, ParseError, "Invalid JSON")
            continue
        }

        response := s.handleMessage(&msg)
        if response != nil {
            data, _ := json.Marshal(response)
            s.writer.WriteString(string(data) + "\n")
            s.writer.Flush()
        }
    }
}

func (s *Server) handleMessage(msg *JSONRPCMessage) *JSONRPCMessage {
    if msg.JSONRPC != "2.0" {
        return s.errorResponse(msg.ID, InvalidRequest, "jsonrpc must be 2.0")
    }

    if msg.Method == "" {
        return s.errorResponse(msg.ID, InvalidRequest, "method is required")
    }

    s.mu.RLock()
    handler, exists := s.methods[msg.Method]
    s.mu.RUnlock()

    if !exists {
        return s.errorResponse(msg.ID, MethodNotFound, fmt.Sprintf("method %s not found", msg.Method))
    }

    result, err := handler(msg.Params)
    if err != nil {
        return s.errorResponse(msg.ID, InternalError, err.Error())
    }

    return &JSONRPCMessage{
        JSONRPC: "2.0",
        ID: msg.ID,
        Result: result,
    }
}

func (s *Server) errorResponse(id interface{}, code int, message string) *JSONRPCMessage {
    return &JSONRPCMessage{
        JSONRPC: "2.0",
        ID: id,
        Error: &JSONRPCError{
            Code: code,
            Message: message,
        },
    }
}

func (s *Server) sendError(id interface{}, code int, message string) {
    msg := s.errorResponse(id, code, message)
    data, _ := json.Marshal(msg)
    s.writer.WriteString(string(data) + "\n")
    s.writer.Flush()
}
```

### **Fase 2: 12 Ferramentas MCP**

**Duração**: 2 semanas

**Deliverables**:

- [ ] `search_context` (busca semântica)
- [ ] `search_tests` (busca testes relacionados)
- [ ] `analyze_dependencies` (quem chama X)
- [ ] `find_similar_code` (código similar)
- [ ] `get_file_structure` (resume arquivo)
- [ ] `list_files` (lista arquivos indexados)
- [ ] `list_namespaces` (lista namespaces)
- [ ] `get_session_state` (histórico)
- [ ] `index_progress` (progresso de indexação)
- [ ] `validate_query` (validar query)
- [ ] `get_metrics` (métricas de uso)
- [ ] `export_context` (exportar contexto)

**Código de Exemplo - search_context**:

```go
// pkg/mcp/tools/search_context.go
package tools

import (
    "context"
    "encoding/json"
    "fmt"
)

type SearchContextParams struct {
    Query string `json:"query"`
    Namespace string `json:"namespace"`
    TopK int `json:"top_k,omitempty"`
    Strategy string `json:"strategy,omitempty"` // semantic, structural, hybrid
}

type SearchContextResult struct {
    Chunks []map[string]interface{} `json:"chunks"`
    Metrics map[string]interface{} `json:"metrics"`
}

func RegisterSearchContext(server *Server, engine *engine) {
    server.RegisterMethod("search_context", func(rawParams json.RawMessage) (interface{}, error) {
        var params SearchContextParams
        if err := json.Unmarshal(rawParams, &params); err != nil {
            return nil, fmt.Errorf("invalid params: %w", err)
        }

        if params.Query == "" {
            return nil, fmt.Errorf("query is required")
        }

        if params.TopK == 0 {
            params.TopK = 10
        }

        if params.Strategy == "" {
            params.Strategy = "hybrid"
        }

        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()

        // Embed query
        queryEmbed, err := engine.ProviderRouter.GetEmbedding().Embed(ctx, []string{params.Query})
        if err != nil {
            return nil, fmt.Errorf("embedding failed: %w", err)
        }

        // Vector search
        searchResults, err := engine.SearchVector(ctx, queryEmbed[0], params.Namespace, params.TopK*5)
        if err != nil {
            return nil, fmt.Errorf("search failed: %w", err)
        }

        // Rerank
        docs := make([]string, len(searchResults))
        for i, r := range searchResults {
            docs[i] = r.Content
        }

        rerankResults, err := engine.ProviderRouter.GetRerank().Rerank(ctx, params.Query, docs)
        if err != nil {
            // Fallback sem rerank
            rerankResults = make([]RankResult, len(docs))
            for i := range docs {
                rerankResults[i] = RankResult{Index: i, Score: searchResults[i].Score}
            }
        }

        // Limitar a top K
        finalResults := make([]map[string]interface{}, 0, params.TopK)
        for i := 0; i < len(rerankResults) && i < params.TopK; i++ {
            idx := rerankResults[i].Index
            chunk := searchResults[idx]

            finalResults = append(finalResults, map[string]interface{}{
                "file_path": chunk.FilePath,
                "start_line": chunk.StartLine,
                "content": chunk.Content,
                "relevance": rerankResults[i].Score,
            })
        }

        return SearchContextResult{
            Chunks: finalResults,
            Metrics: map[string]interface{}{
                "total_candidates": len(searchResults),
                "returned": len(finalResults),
            },
        }, nil
    })
}
```

### **Fase 3: Autenticação & Autorização via Headers**

**Duração**: 1 semana

**Deliverables**:

- [ ] JWT validation
- [ ] Namespace extraction
- [ ] RBAC enforcement
- [ ] Audit logging

**Código de Exemplo**:

```go
// pkg/mcp/auth.go
package mcp

import (
    "fmt"
    "strings"
)

type AuthContext struct {
    UserID string
    Namespace string
    Roles []string
    SessionID string
}

func (s *Server) ExtractAuthContext(headers map[string]string) (*AuthContext, error) {
    // Extract JWT do header Authorization
    authHeader, ok := headers["Authorization"]
    if !ok {
        return nil, fmt.Errorf("missing Authorization header")
    }

    parts := strings.Split(authHeader, " ")
    if len(parts) != 2 || parts[0] != "Bearer" {
        return nil, fmt.Errorf("invalid Authorization format")
    }

    token := parts[1]
    claims, err := validateJWT(token)
    if err != nil {
        return nil, fmt.Errorf("invalid token: %w", err)
    }

    return &AuthContext{
        UserID: claims.UserID,
        Namespace: claims.Namespace,
        Roles: claims.Roles,
        SessionID: claims.SessionID,
    }, nil
}

// Decorator para autorização
func (s *Server) AuthorizedMethod(requiredRole string, handler MethodHandler) MethodHandler {
    return func(params json.RawMessage) (interface{}, error) {
        // Extract do contexto (implementar via context.Context)
        // Verificar role
        return handler(params)
    }
}
```

### **Fase 4: Testes de Conformidade MCP**

**Duração**: 1 semana

**Deliverables**:

- [ ] Unit tests para cada ferramenta
- [ ] Integration tests com harness
- [ ] Spec compliance tests
- [ ] Performance benchmarks

**Código de Exemplo**:

```go
// pkg/mcp/server_test.go
package mcp

import (
    "bytes"
    "encoding/json"
    "testing"
)

func TestSearchContext(t *testing.T) {
    server := NewServer()

    // Mock handler
    server.RegisterMethod("search_context", func(params json.RawMessage) (interface{}, error) {
        return map[string]interface{}{
            "chunks": []interface{}{},
            "metrics": map[string]interface{}{},
        }, nil
    })

    // Test request
    request := JSONRPCMessage{
        JSONRPC: "2.0",
        ID: 1,
        Method: "search_context",
        Params: json.RawMessage(`{"query": "test"}`),
    }

    reqData, _ := json.Marshal(request)
    response := server.handleMessage(&request)

    if response.ID != 1 {
        t.Errorf("response ID mismatch")
    }

    if response.Error != nil {
        t.Errorf("unexpected error: %v", response.Error)
    }
}

func TestInvalidMethod(t *testing.T) {
    server := NewServer()

    request := JSONRPCMessage{
        JSONRPC: "2.0",
        ID: 1,
        Method: "nonexistent",
    }

    response := server.handleMessage(&request)

    if response.Error == nil {
        t.Errorf("expected error for nonexistent method")
    }

    if response.Error.Code != MethodNotFound {
        t.Errorf("expected MethodNotFound error, got %d", response.Error.Code)
    }
}
```

## Spec MCP Conformance

| Requisito           | Implementação                          |
| :------------------ | :------------------------------------- |
| **JSON-RPC 2.0**    | Implementado com todos os error codes  |
| **Stdio Transport** | Via bufio.Reader/Writer                |
| **Tool Registry**   | Dinâmico, descoberta via introspection |
| **Timeouts**        | 30s por request                        |
| **Batch Requests**  | Não suportado (serial)                 |
| **Notifications**   | Não suportado (sempre responses)       |

## Métricas de Sucesso

- 100% conformidade com spec MCP 2024-04
- Latência P95: <500ms por request
- Throughput: 100 req/s
- Uptime: 99.99%
- Zero memory leaks (validado com pprof)

---

## External Linking

| Concept        | Resource                                | Link                                                                                   |
| -------------- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification    | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)              | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **JSON-RPC**   | JSON-RPC 2.0 Specification              | [www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)                 |
| **JWT**        | RFC 7519: JSON Web Token Standard       | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |
| **RBAC**       | NIST Role-Based Access Control Standard | [csrc.nist.gov/projects/rbac](https://csrc.nist.gov/projects/rbac)                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
