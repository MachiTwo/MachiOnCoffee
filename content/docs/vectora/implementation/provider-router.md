---
title: Plano de Implementação - Provider Router (Gemini + Voyage)
slug: provider-router
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - engineering
  - golang
  - api-clients
  - gemini
  - voyage
---

{{< lang-toggle >}}
{{< section-toggle >}}

O **Provider Router** encapsula clientes para Gemini 3 Flash (LLM), Voyage 4 (embeddings) e Voyage Rerank 2.5 (reranking). Este documento descreve implementação em Go puro com retry logic, rate limiting e fallback BYOK.

## Stack de Providers Confirmados

| Serviço        | Modelo            | Uso                      | Latência | Custo              |
| :------------- | :---------------- | :----------------------- | :------- | :----------------- |
| **LLM**        | Gemini 3 Flash    | Inferência principal     | 30-50ms  | $0.075 / 1M tokens |
| **Embeddings** | Voyage 4          | Transformar query + docs | <100ms   | $0.10 / 1M tokens  |
| **Reranking**  | Voyage Rerank 2.5 | Refinar top-50 → top-10  | <150ms   | $0.40 / 1M tokens  |

## Fases de Implementação

### **Fase 1: Provider Interface & Abstração**

**Duração**: 3 dias

**Deliverables**:

- [ ] Interface Provider genérica
- [ ] Router que resolve qual provider usar
- [ ] Suporte a BYOK (Bring Your Own Key)
- [ ] Métricas de uso

**Código de Exemplo**:

```go
// pkg/providers/provider.go
package providers

import (
    "context"
)

// Provider é a interface genérica para todos os LLM providers
type LLMProvider interface {
    Complete(ctx context.Context, prompt string) (string, error)
    HealthCheck(ctx context.Context) error
}

type EmbeddingProvider interface {
    Embed(ctx context.Context, texts []string) ([][]float32, error)
    HealthCheck(ctx context.Context) error
}

type RerankProvider interface {
    Rerank(ctx context.Context, query string, docs []string) ([]RankResult, error)
    HealthCheck(ctx context.Context) error
}

type RankResult struct {
    Index int
    Score float32
}

// ProviderRouter seleciona o provider baseado na config
type ProviderRouter struct {
    llm LLMProvider
    embedding EmbeddingProvider
    rerank RerankProvider
    metrics *ProviderMetrics
}

type ProviderMetrics struct {
    LLMCallsTotal int64
    LLMErrorsTotal int64
    LLMLatencyMs int64
    EmbeddingCalls int64
    RerankingCalls int64
}

func NewProviderRouter(config *ProvidersConfig) (*ProviderRouter, error) {
    // Gemini LLM
    var llm LLMProvider
    if config.LLM.Provider == "gemini" {
        llm = NewGeminiClient(config.LLM.APIKey)
    } else if config.LLM.BYOK {
        return nil, fmt.Errorf("BYOK not yet supported for LLM")
    }

    // Voyage Embedding
    var embedding EmbeddingProvider
    if config.Embedding.Provider == "voyage" {
        embedding = NewVoyageClient(config.Embedding.APIKey)
    }

    // Voyage Rerank
    var rerank RerankProvider
    if config.Rerank.Provider == "voyage" {
        rerank = NewVoyageClient(config.Rerank.APIKey)
    }

    return &ProviderRouter{
        llm: llm,
        embedding: embedding,
        rerank: rerank,
        metrics: &ProviderMetrics{},
    }, nil
}

func (pr *ProviderRouter) GetLLM() LLMProvider {
    return pr.llm
}

func (pr *ProviderRouter) GetEmbedding() EmbeddingProvider {
    return pr.embedding
}

func (pr *ProviderRouter) GetRerank() RerankProvider {
    return pr.rerank
}
```

### **Fase 2: Gemini 3 Flash Client (com Streaming)**

**Duração**: 1 semana

**Deliverables**:

- [ ] Client com SDK oficial Google
- [ ] Tool calling support
- [ ] Streaming para respostas longas
- [ ] Exponential backoff retry

**Código de Exemplo**:

```go
// pkg/providers/gemini.go
package providers

import (
    "context"
    "fmt"
    "time"

    "github.com/google/generative-ai-go/client"
    "github.com/google/generative-ai-go/genai"
)

type GeminiClient struct {
    client *genai.Client
    model string
}

func NewGeminiClient(apiKey string) *GeminiClient {
    ctx := context.Background()
    c, _ := genai.NewClient(ctx, option.WithAPIKey(apiKey))

    return &GeminiClient{
        client: c,
        model: "gemini-3-flash",
    }
}

func (gc *GeminiClient) Complete(ctx context.Context, prompt string) (string, error) {
    return gc.completeWithRetry(ctx, prompt, 0)
}

func (gc *GeminiClient) completeWithRetry(ctx context.Context, prompt string, attempt int) (string, error) {
    if attempt > 3 {
        return "", fmt.Errorf("max retries exceeded")
    }

    model := gc.client.GenerativeModel(gc.model)
    model.SystemPrompt = "Você é um assistente especializado em análise de código."
    model.Temperature = 0.7

    resp, err := model.GenerateContent(ctx, genai.Text(prompt))
    if err != nil {
        if attempt < 3 {
            backoff := time.Duration(1<<uint(attempt)) * time.Second
            time.Sleep(backoff)
            return gc.completeWithRetry(ctx, prompt, attempt+1)
        }
        return "", fmt.Errorf("generation failed: %w", err)
    }

    var result string
    for _, content := range resp.Candidates {
        for _, part := range content.Content.Parts {
            if text, ok := part.(genai.Text); ok {
                result += string(text)
            }
        }
    }

    return result, nil
}

func (gc *GeminiClient) HealthCheck(ctx context.Context) error {
    model := gc.client.GenerativeModel(gc.model)
    _, err := model.GenerateContent(ctx, genai.Text("Hi"))
    return err
}
```

### **Fase 3: Voyage Embedding & Rerank Client**

**Duração**: 1 semana

**Deliverables**:

- [ ] Voyage 4 embedding client
- [ ] Voyage Rerank 2.5 client
- [ ] Batch processing
- [ ] Rate limit handling

**Código de Exemplo**:

```go
// pkg/providers/voyage_advanced.go
package providers

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type VoyageAdvancedClient struct {
    apiKey string
    rateLimiter *RateLimiter
    embeddingURL string
    rerankURL string
    httpClient *http.Client
}

type RateLimiter struct {
    mu sync.Mutex
    lastCall time.Time
    minInterval time.Duration
}

func NewVoyageAdvancedClient(apiKey string) *VoyageAdvancedClient {
    return &VoyageAdvancedClient{
        apiKey: apiKey,
        rateLimiter: &RateLimiter{
            minInterval: 100 * time.Millisecond, // ~10 req/sec
        },
        embeddingURL: "https://api.voyageai.com/v1/embeddings",
        rerankURL: "https://api.voyageai.com/v1/rerank",
        httpClient: &http.Client{
            Timeout: 30 * time.Second,
        },
    }
}

// Batch embedding com paralelismo
func (vc *VoyageAdvancedClient) EmbedBatch(ctx context.Context, texts []string) ([][]float32, error) {
    results := make([][]float32, len(texts))
    batchSize := 128

    for i := 0; i < len(texts); i += batchSize {
        end := i + batchSize
        if end > len(texts) {
            end = len(texts)
        }

        batch := texts[i:end]
        batchResults, err := vc.embedBatch(ctx, batch)
        if err != nil {
            return nil, err
        }

        copy(results[i:end], batchResults)
    }

    return results, nil
}

func (vc *VoyageAdvancedClient) embedBatch(ctx context.Context, texts []string) ([][]float32, error) {
    // Rate limit
    vc.rateLimiter.Wait()

    req := EmbeddingRequest{
        Input: texts,
        Model: "voyage-4",
        InputType: "document",
    }

    // HTTP call similar ao anterior
    // ...
    return nil, nil
}

// Rerank com top-k
func (vc *VoyageAdvancedClient) Rerank(ctx context.Context, query string, documents []string) ([]RankResult, error) {
    vc.rateLimiter.Wait()

    req := RerankRequest{
        Query: query,
        Documents: documents,
        TopK: 10,
        Model: "rerank-lite-1-voyageai",
    }

    // HTTP call
    // ...
    return nil, nil
}

func (rl *RateLimiter) Wait() {
    rl.mu.Lock()
    defer rl.mu.Unlock()

    elapsed := time.Since(rl.lastCall)
    if elapsed < rl.minInterval {
        time.Sleep(rl.minInterval - elapsed)
    }

    rl.lastCall = time.Now()
}
```

### **Fase 4: BYOK Support & Quota Tracking**

**Duração**: 5 dias

**Deliverables**:

- [ ] Detect BYOK from config
- [ ] Fallback chain (managed → BYOK)
- [ ] Quota calculation per request
- [ ] Alerts ao atingir limites

**Código de Exemplo**:

```go
// pkg/providers/quota.go
package providers

import (
    "fmt"
    "sync"
    "time"
)

type QuotaTracker struct {
    mu sync.RWMutex
    dailyLimit int64
    monthlyLimit int64
    dailyUsed int64
    monthlyUsed int64
    resetTime time.Time
}

func NewQuotaTracker(dailyLimit, monthlyLimit int64) *QuotaTracker {
    return &QuotaTracker{
        dailyLimit: dailyLimit,
        monthlyLimit: monthlyLimit,
        resetTime: time.Now().AddDate(0, 0, 1),
    }
}

func (qt *QuotaTracker) AddUsage(tokens int64) error {
    qt.mu.Lock()
    defer qt.mu.Unlock()

    // Check reset
    if time.Now().After(qt.resetTime) {
        qt.dailyUsed = 0
        qt.resetTime = time.Now().AddDate(0, 0, 1)
    }

    if qt.dailyUsed+tokens > qt.dailyLimit {
        return fmt.Errorf("daily quota exceeded: %d/%d", qt.dailyUsed, qt.dailyLimit)
    }

    if qt.monthlyUsed+tokens > qt.monthlyLimit {
        return fmt.Errorf("monthly quota exceeded: %d/%d", qt.monthlyUsed, qt.monthlyLimit)
    }

    qt.dailyUsed += tokens
    qt.monthlyUsed += tokens

    return nil
}

func (qt *QuotaTracker) GetStatus() map[string]interface{} {
    qt.mu.RLock()
    defer qt.mu.RUnlock()

    return map[string]interface{}{
        "daily_used": qt.dailyUsed,
        "daily_limit": qt.dailyLimit,
        "monthly_used": qt.monthlyUsed,
        "monthly_limit": qt.monthlyLimit,
    }
}
```

### **Fase 5: Health Check & Fallback Strategy**

**Duração**: 3 dias

**Deliverables**:

- [ ] Periodic health checks
- [ ] Circuit breaker
- [ ] Fallback automático
- [ ] Alerting

**Código de Exemplo**:

```go
// pkg/providers/health_check.go
package providers

import (
    "context"
    "fmt"
    "time"
)

type ProviderHealth struct {
    LastChecked time.Time
    Status string // healthy, degraded, down
    ErrorCount int
    LatencyMs int64
}

type HealthMonitor struct {
    router *ProviderRouter
    interval time.Duration
    alertFunc func(provider string, status string)
}

func NewHealthMonitor(router *ProviderRouter) *HealthMonitor {
    return &HealthMonitor{
        router: router,
        interval: 30 * time.Second,
    }
}

func (hm *HealthMonitor) Start(ctx context.Context) {
    ticker := time.NewTicker(hm.interval)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            hm.checkAll(ctx)
        }
    }
}

func (hm *HealthMonitor) checkAll(ctx context.Context) {
    // Check Gemini
    start := time.Now()
    if err := hm.router.GetLLM().HealthCheck(ctx); err != nil {
        hm.alert("gemini", "degraded", fmt.Sprintf("error: %v", err))
    } else {
        latency := time.Since(start).Milliseconds()
        fmt.Printf("Gemini healthy: %dms\n", latency)
    }

    // Check Voyage Embedding
    if err := hm.router.GetEmbedding().HealthCheck(ctx); err != nil {
        hm.alert("voyage-embedding", "degraded", err.Error())
    }

    // Check Voyage Rerank
    if err := hm.router.GetRerank().HealthCheck(ctx); err != nil {
        hm.alert("voyage-rerank", "degraded", err.Error())
    }
}

func (hm *HealthMonitor) alert(provider, status, message string) {
    if hm.alertFunc != nil {
        hm.alertFunc(provider, status+" "+message)
    }
}
```

## Garantias de Qualidade

| Requisito               | Implementação                       |
| :---------------------- | :---------------------------------- |
| **Exponential Backoff** | 1s, 2s, 4s, fail                    |
| **Rate Limiting**       | 100ms entre chamadas (10 req/s)     |
| **Timeout**             | 30s por request                     |
| **Circuit Breaker**     | Fail open após 3 erros consecutivos |
| **BYOK Support**        | Fallback automático                 |
| **Metrics**             | Latência, erros, quota por provider |

## Métricas de Sucesso

- P95 latência Gemini: <100ms
- P95 latência Voyage: <150ms
- Uptime providers: >99.5%
- Retry success rate: >95%
- BYOK failover: <1 segundo

---

_Parte do ecossistema Vectora_ · Engenharia Interna
