---
title: Plano de Implementação - Migração do Núcleo (TypeScript → Golang)
slug: core-migration
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - engineering
  - golang
  - migration
  - performance
  - architecture
---

{{< lang-toggle >}}
{{< section-toggle >}}

A transição do Vectora de **TypeScript (Node.js)** para **Golang** é uma reengenharia completa para atender aos requisitos de performance, distribuição nativa e segurança compilada. Este documento define o plano de implementação em detalhes.

## Justificativa Técnica

| Fator              | TypeScript (Node.js)              | Golang                          | Impacto no Vectora                           |
| :----------------- | :-------------------------------- | :------------------------------ | :------------------------------------------- |
| **Distribuição**   | Requer Node.js instalado (+100MB) | Binário Estático Único (~20MB)  | Instalação via Winget sem dependências.      |
| **Concorrência**   | Event Loop (Single-threaded)      | Goroutines (Nativo/Paralelo)    | Processamento de RAG 3x mais rápido.         |
| **Consumo Memory** | Alto (V8 Garbage Collector)       | Baixo (Gerenciamento Eficiente) | Menor pegada em máquinas de desenvolvedores. |
| **Segurança**      | Tipagem em tempo de escrita       | Tipagem forte compilada         | Menos erros de runtime em produção.          |
| **Startup Time**   | ~300ms (iniciar VM)               | ~10ms (executável nativo)       | Resposta imediata a tool calls MCP.          |

## Fases de Implementação

### **Fase 1: Setup & Infraestrutura de Build**

**Objetivo**: Estabelecer pipeline de desenvolvimento em Go com testes automatizados.

**Duração Estimada**: 2 semanas

**Deliverables**:

- [ ] Estrutura de projeto Go (`cmd/`, `pkg/`, `internal/`)
- [ ] Configuração de `go.mod` com dependências principais
- [ ] GitHub Actions CI/CD (linting, testes, builds multiplataforma)
- [ ] Makefile para automação local

**Dependências**:

- Go 1.21+
- GitHub Actions configurado

**Código de Exemplo - Estrutura de Diretórios**:

```bash
vectora/
├── cmd/
│ ├── vectora/
│ │ └── main.go # Ponto de entrada principal
│ └── vectora-systray/ # Aplicativo Systray em Go
├── pkg/
│ ├── core/ # Núcleo (Context Engine, Harness)
│ ├── guardian/ # Motor de segurança
│ ├── mcp/ # Protocolo MCP
│ ├── models/ # Provider router (Gemini, Voyage)
│ └── storage/ # MongoDB Atlas client
├── internal/
│ ├── config/ # Parsing de YAML
│ ├── logger/ # Logging estruturado
│ └── utils/ # Funções auxiliares
├── tests/
│ ├── unit/ # Testes unitários
│ └── integration/ # Testes de integração
├── .github/workflows/
│ ├── ci.yml # Linting + testes
│ └── release.yml # Build + Winget
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

### **Fase 2: Núcleo de Validação & Configuração**

**Objetivo**: Implementar sistema de leitura de `vectora.config.yaml` com validação tipada.

**Duração Estimada**: 1 semana

**Deliverables**:

- [ ] Parser YAML com `gopkg.in/yaml.v3`
- [ ] Structs de configuração com validação
- [ ] Testes de parsing de configurações válidas/inválidas

**Código de Exemplo - Structs de Configuração**:

```go
// pkg/config/config.go
package config

import (
    "fmt"
    "os"
    "gopkg.in/yaml.v3"
)

type VectoraConfig struct {
    APIKey string `yaml:"api_key" validate:"required"`
    Namespace string `yaml:"namespace" validate:"required"`
    TrustFolder string `yaml:"trust_folder" validate:"required,dirpath"`
    Debug bool `yaml:"debug"`
    Models ModelsConfig `yaml:"models"`
}

type ModelsConfig struct {
    LLM string `yaml:"llm" validate:"required,oneof=gemini-3-flash"`
    Embedder string `yaml:"embedder" validate:"required,oneof=voyage-4"`
    Reranker string `yaml:"reranker" validate:"required,oneof=voyage-rerank-2.5"`
}

func LoadConfig(path string) (*VectoraConfig, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read config: %w", err)
    }

    var cfg VectoraConfig
    if err := yaml.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }

    // Validação estruturada
    if err := cfg.Validate(); err != nil {
        return nil, fmt.Errorf("config validation failed: %w", err)
    }

    return &cfg, nil
}

func (c *VectoraConfig) Validate() error {
    if c.APIKey == "" {
        return fmt.Errorf("api_key is required")
    }
    if c.Namespace == "" {
        return fmt.Errorf("namespace is required")
    }
    // Validações adicionais
    return nil
}
```

### **Fase 3: Harness Runtime - Orquestração**

**Objetivo**: Implementar motor de orquestração que gerencia lifecycle de tool calls.

**Duração Estimada**: 3 semanas

**Deliverables**:

- [ ] Struct `Harness` com gerenciamento de contexto
- [ ] Interface `ToolExecutor` para abstração de execução
- [ ] Pipeline de validação (pré-execução)
- [ ] Persistência de estado em arquivo/MongoDB

**Código de Exemplo - Harness Runtime**:

```go
// pkg/core/harness.go
package core

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type ToolCall struct {
    ID string `json:"id"`
    Name string `json:"name"`
    Args map[string]interface{} `json:"arguments"`
    Timestamp time.Time `json:"timestamp"`
}

type ToolResult struct {
    ID string `json:"id"`
    Success bool `json:"success"`
    Output string `json:"output"`
    Error string `json:"error,omitempty"`
    Duration time.Duration `json:"duration"`
}

type Harness struct {
    mu sync.RWMutex
    config *Config
    executor ToolExecutor
    guardianEngine *guardian.Engine
    stateManager *StateManager
    contextCtx context.Context
    cancel context.CancelFunc
}

type ToolExecutor interface {
    Execute(ctx context.Context, call *ToolCall) (*ToolResult, error)
}

func NewHarness(cfg *Config, executor ToolExecutor) (*Harness, error) {
    ctx, cancel := context.WithCancel(context.Background())

    h := &Harness{
        config: cfg,
        executor: executor,
        contextCtx: ctx,
        cancel: cancel,
    }

    // Inicializar Guardian
    guardianEngine, err := guardian.NewEngine(cfg.GuardianRules)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize Guardian: %w", err)
    }
    h.guardianEngine = guardianEngine

    // Inicializar State Manager
    stateManager, err := NewStateManager(cfg.StateDir)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize StateManager: %w", err)
    }
    h.stateManager = stateManager

    return h, nil
}

func (h *Harness) ExecuteToolCall(ctx context.Context, call *ToolCall) (*ToolResult, error) {
    h.mu.Lock()
    defer h.mu.Unlock()

    start := time.Now()

    // 1. Validação com Guardian (pré-execução)
    if err := h.guardianEngine.ValidateToolCall(call); err != nil {
        return &ToolResult{
            ID: call.ID,
            Success: false,
            Error: fmt.Sprintf("Guardian validation failed: %v", err),
            Duration: time.Since(start),
        }, nil
    }

    // 2. Executar ferramenta
    result, err := h.executor.Execute(ctx, call)
    result.Duration = time.Since(start)

    if err != nil {
        result.Error = err.Error()
        result.Success = false
    } else {
        result.Success = true
    }

    // 3. Persistir no StateManager
    h.stateManager.RecordToolCall(call)
    h.stateManager.RecordToolResult(result)

    return result, nil
}

func (h *Harness) Close() error {
    h.cancel()
    return h.stateManager.Close()
}
```

### **Fase 4: Guardian Security Engine**

**Objetivo**: Implementar validação de segurança compilada em Go.

**Duração Estimada**: 2 semanas

**Deliverables**:

- [ ] Blocklist compilada (padrões sensíveis)
- [ ] Trust Folder resolver
- [ ] Sanitização de output
- [ ] Testes de segurança

**Código de Exemplo - Guardian Engine**:

```go
// pkg/guardian/engine.go
package guardian

import (
    "fmt"
    "regexp"
    "strings"
)

type Engine struct {
    blocklist []*regexp.Regexp
    secretPatterns []*regexp.Regexp
}

func NewEngine(rules map[string]interface{}) (*Engine, error) {
    e := &Engine{
        blocklist: make([]*regexp.Regexp, 0),
        secretPatterns: make([]*regexp.Regexp, 0),
    }

    // Padrões compilados de bloqueio (imutáveis)
    blockPatterns := []string{
        `\.env`,
        `\.pem$`,
        `\.key$`,
        `\.p12$`,
        `/etc/passwd`,
        `/etc/shadow`,
        `secret`,
        `password`,
    }

    for _, pattern := range blockPatterns {
        re, err := regexp.Compile(pattern)
        if err != nil {
            return nil, fmt.Errorf("failed to compile blocklist pattern: %w", err)
        }
        e.blocklist = append(e.blocklist, re)
    }

    // Padrões para detectar segredos em output
    secretPatterns := []string{
        `(api[_-]?key)[:\s=]+([a-zA-Z0-9\-_]{32,})`,
        `(password)[:\s=]+([^\s]+)`,
        `(token)[:\s=]+([a-zA-Z0-9\-_]{20,})`,
    }

    for _, pattern := range secretPatterns {
        re, err := regexp.Compile(pattern)
        if err != nil {
            return nil, fmt.Errorf("failed to compile secret pattern: %w", err)
        }
        e.secretPatterns = append(e.secretPatterns, re)
    }

    return e, nil
}

func (e *Engine) ValidateToolCall(call *ToolCall) error {
    // Validar nome da ferramenta
    if call.Name == "" {
        return fmt.Errorf("tool name is empty")
    }

    // Validar argumentos contra blocklist
    for key, value := range call.Arguments {
        strValue := fmt.Sprintf("%v", value)

        for _, pattern := range e.blocklist {
            if pattern.MatchString(strValue) {
                return fmt.Errorf("blocked pattern detected in argument '%s'", key)
            }
        }
    }

    return nil
}

func (e *Engine) SanitizeOutput(output string) string {
    sanitized := output

    // Mascarar segredos detectados
    for _, pattern := range e.secretPatterns {
        sanitized = pattern.ReplaceAllString(sanitized, "$1: [REDACTED]")
    }

    return sanitized
}
```

### **Fase 5: MCP Server Implementation**

**Objetivo**: Implementar servidor JSON-RPC conforme spec MCP.

**Duração Estimada**: 2 semanas

**Deliverables**:

- [ ] JSON-RPC 2.0 server (transporte stdio)
- [ ] Tool registry dinâmico
- [ ] Message routing
- [ ] Testes de conformidade MCP

**Código de Exemplo - MCP Server**:

```go
// pkg/mcp/server.go
package mcp

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io"
    "os"
)

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

type Server struct {
    toolHandlers map[string]ToolHandler
    reader *bufio.Reader
    writer *bufio.Writer
}

type ToolHandler func(params json.RawMessage) (interface{}, error)

func NewServer() *Server {
    return &Server{
        toolHandlers: make(map[string]ToolHandler),
        reader: bufio.NewReader(os.Stdin),
        writer: bufio.NewWriter(os.Stdout),
    }
}

func (s *Server) RegisterTool(name string, handler ToolHandler) {
    s.toolHandlers[name] = handler
}

func (s *Server) Start() error {
    for {
        line, err := s.reader.ReadString('\n')
        if err == io.EOF {
            return nil
        }
        if err != nil {
            return err
        }

        var msg JSONRPCMessage
        if err := json.Unmarshal([]byte(line), &msg); err != nil {
            s.sendError(nil, -32700, "Parse error")
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
    handler, exists := s.toolHandlers[msg.Method]
    if !exists {
        return &JSONRPCMessage{
            JSONRPC: "2.0",
            ID: msg.ID,
            Error: &JSONRPCError{
                Code: -32601,
                Message: "Method not found",
            },
        }
    }

    result, err := handler(msg.Params)
    if err != nil {
        return &JSONRPCMessage{
            JSONRPC: "2.0",
            ID: msg.ID,
            Error: &JSONRPCError{
                Code: -32603,
                Message: fmt.Sprintf("Internal error: %v", err),
            },
        }
    }

    return &JSONRPCMessage{
        JSONRPC: "2.0",
        ID: msg.ID,
        Result: result,
    }
}

func (s *Server) sendError(id interface{}, code int, message string) {
    msg := JSONRPCMessage{
        JSONRPC: "2.0",
        ID: id,
        Error: &JSONRPCError{
            Code: code,
            Message: message,
        },
    }
    data, _ := json.Marshal(msg)
    s.writer.WriteString(string(data) + "\n")
    s.writer.Flush()
}
```

### **Fase 6: Context Engine & RAG Pipeline**

**Objetivo**: Implementar pipeline de embedding, busca e reranking.

**Duração Estimada**: 3 semanas

**Deliverables**:

- [ ] AST parser para código
- [ ] Wrapper para Voyage 4 (embedding)
- [ ] Wrapper para Voyage Rerank 2.5
- [ ] MongoDB Atlas vector search client
- [ ] Pipeline completo com compaction

**Código de Exemplo - Context Engine**:

```go
// pkg/core/context_engine.go
package core

import (
    "context"
    "fmt"
    "sync"
)

type ContextEngine struct {
    mongoClient *mongo.Client
    voyageClient *VoyageClient
    config *ContextConfig
}

type EmbeddingRequest struct {
    Query string
    Content []string
}

type EmbeddingResult struct {
    Embeddings [][]float32
    Tokens int
}

type SearchResult struct {
    ID string
    Content string
    Score float32
    Metadata map[string]interface{}
}

func NewContextEngine(mongoURI string, voyageAPIKey string) (*ContextEngine, error) {
    client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(mongoURI))
    if err != nil {
        return nil, fmt.Errorf("failed to connect to MongoDB: %w", err)
    }

    voyageClient := NewVoyageClient(voyageAPIKey)

    return &ContextEngine{
        mongoClient: client,
        voyageClient: voyageClient,
    }, nil
}

func (ce *ContextEngine) EmbedQuery(ctx context.Context, query string) ([]float32, error) {
    result, err := ce.voyageClient.Embed(ctx, &EmbeddingRequest{
        Query: query,
    })
    if err != nil {
        return nil, fmt.Errorf("embedding failed: %w", err)
    }

    return result.Embeddings[0], nil
}

func (ce *ContextEngine) SearchVector(ctx context.Context, embedding []float32, namespace string, limit int) ([]SearchResult, error) {
    collection := ce.mongoClient.Database("vectora").Collection("documents")

    results, err := collection.Aggregate(ctx, mongo.Pipeline{
        bson.M{"$search": bson.M{
            "cosmosSearch": bson.M{
                "vector": embedding,
                "k": limit,
            },
        }},
        bson.M{"$match": bson.M{
            "namespace": namespace,
        }},
        bson.M{"$project": bson.M{
            "similarityScore": bson.M{"$meta": "searchScore"},
            "document": "$$ROOT",
        }},
    })

    if err != nil {
        return nil, fmt.Errorf("vector search failed: %w", err)
    }

    var output []SearchResult
    if err := results.All(ctx, &output); err != nil {
        return nil, err
    }

    return output, nil
}

func (ce *ContextEngine) Rerank(ctx context.Context, query string, documents []string) ([]RerankResult, error) {
    // Usar Voyage Rerank 2.5 para refinar resultados
    results, err := ce.voyageClient.Rerank(ctx, &RerankRequest{
        Query: query,
        Documents: documents,
    })
    if err != nil {
        return nil, fmt.Errorf("reranking failed: %w", err)
    }

    return results, nil
}
```

### **Fase 7: Cobra CLI & Systray Integration**

**Objetivo**: Implementar interface CLI com Cobra + Systray em Go.

**Duração Estimada**: 2 semanas

**Deliverables**:

- [ ] Comando base `vectora` com subcomandos
- [ ] Aplicativo Systray com menu nativo
- [ ] Sincronização de estado entre CLI e Systray

**Código de Exemplo - Cobra Estrutura**:

```go
// cmd/vectora/main.go
package main

import (
    "log"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use: "vectora",
    Short: "Vectora - AI Sub-Agent for Code Context",
    Long: "Vectora is a Tier-2 sub-agent that manages context and security for AI coding agents.",
}

var authCmd = &cobra.Command{
    Use: "auth",
    Short: "Manage authentication",
}

var authLoginCmd = &cobra.Command{
    Use: "login",
    Short: "Login to Vectora via SSO",
    RunE: func(cmd *cobra.Command, args []string) error {
        gui, _ := cmd.Flags().GetBool("gui")
        // Lógica de login
        if gui {
            // Disparar Systray para SSO
        }
        return nil
    },
}

func init() {
    rootCmd.AddCommand(authCmd)
    authCmd.AddCommand(authLoginCmd)
    authLoginCmd.Flags().Bool("gui", false, "Use GUI for authentication")
}

func main() {
    if err := rootCmd.Execute(); err != nil {
        log.Fatal(err)
    }
}
```

### **Fase 8: Distribuição via Winget & GoReleaser**

**Objetivo**: Configurar pipeline de release automatizado com assinatura de binários.

**Duração Estimada**: 1 semana

**Deliverables**:

- [ ] Configuração GoReleaser
- [ ] GitHub Actions para build multiplataforma
- [ ] Winget manifest pronto para submissão

**Código de Exemplo - .goreleaser.yml**:

```yaml
# .goreleaser.yml
project_name: vectora

builds:
  - id: vectora-cli
    main: ./cmd/vectora
    binary: vectora
    goos:
      - windows
      - darwin
      - linux
    goarch:
      - amd64
      - arm64
    ldflags:
      - -s -w -X main.Version={{.Version}}

  - id: vectora-systray
    main: ./cmd/vectora-systray
    binary: vectora-systray
    goos:
      - windows
    goarch:
      - amd64

archives:
  - id: default
    format: zip
    format_overrides:
      - goos: windows
        format: zip

release:
  github:
    owner: kaffyn
    name: vectora
```

## Métricas de Sucesso

- Build multiplataforma em <2 minutos
- Startup time <50ms
- Memory footprint <30MB
- 100% de conformidade com MCP spec
- 95%+ cobertura de testes

---

_Parte do ecossistema Vectora_ · Engenharia Interna
