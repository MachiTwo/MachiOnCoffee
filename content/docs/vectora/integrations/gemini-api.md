---
title: Gemini API
slug: gemini-api
date: "2026-04-19T10:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - gemini
  - google
  - integration
  - llm
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

**APP PRÓPRIO**: Vectora oferece integração profunda com **Gemini 3 Flash** via API REST própria. Use Gemini como "motor de raciocínio" sobre código - análise, review, geração de código com contexto do Vectora.

> [!IMPORTANT]
> Gemini API (sistema próprio) vs MCP Protocol ou Extension. Escolha conforme seu workflow: análise de código, code review, documentação automática.

---

## Configuração Básica

### Obter Chave de API Gemini

1. Vá para [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Clique em **"Create API Key"**
3. Copie a chave

### Configurar em Vectora

```bash
# Opção A: Via CLI interativo
vectora config set --key GEMINI_API_KEY

# Opção B: Via .env
echo "GEMINI_API_KEY=sk-..." >> .env

# Opção C: Via config.yaml
# vectora.config.yaml
providers:
  llm:
    name: "gemini"
    model: "gemini-3-flash"
    api_key: "${GEMINI_API_KEY}"
```

### Verificar

```bash
vectora config list
# Deve mostrar GEMINI_API_KEY: ••••••••••
```

---

## Modelos Disponíveis

| Modelo           | Tokens | Latência | Custo    | Caso de Uso                  |
| ---------------- | ------ | -------- | -------- | ---------------------------- |
| `gemini-3-flash` | 1M     | <500ms   | Grátis\* | Default, análise rápida      |
| `gemini-2-flash` | 1M     | <500ms   | $$       | Legacy (descontinuado)       |
| `gemini-pro`     | 32K    | <1s      | $$       | Análise profunda             |
| `gemini-vision`  | 4K     | <2s      | $$       | Análise visual (screenshots) |

\*Free tier: 60 req/min, 1.5M tokens/mês

### Selecting Model

```yaml
# vectora.config.yaml
providers:
  llm:
    model: "gemini-3-flash"

    # Fallback se primary falha
    fallback_model: "gemini-pro"
    fallback_on:
      - "rate_limit_exceeded"
      - "timeout"
```

---

## Workflows com Exemplos Reais

Os workflows abaixo ilustram como Gemini 3 Flash pode ser usado com contexto do Vectora para análises profundas de código, documentação automática e otimização de performance.

### Workflow 1: Code Review Automático (Arquitetura)

**Cenário**: Revisar novo módulo de cache antes de merge

```bash
vectora review \
  --file src/cache/redis.ts \
  --context "padrões de cache no projeto" \
  --criteria "segurança, performance, testabilidade" \
  --model gemini-pro \
  --output review.md
```

**Saída Gemini (com contexto do Vectora)**:

```markdown
# Code Review: src/cache/redis.ts

## Segurança

Redis PASSWORD no .env (não hardcoded)
TTL implementado (evita stale cache)
Não há rate limiting para invalidação
Comparado com: src/cache/memory.ts (melhor implementado)

## Performance

Cache hit de 89% (projeto tem 3 implementações similares)
Evita N+1 queries (padrão seguido em ordem.service.ts)

## Testabilidade

Faltam mocks de RedisClient
Veja exemplo em: src/**tests**/cache.mock.ts:23

## Recomendações

1. Adicione invalidação baseada em eventos
   (Veja patterns em src/events/cache-invalidator.ts)

2. Implementar circuit breaker
   (Similar a: src/resilience/circuit-breaker.ts)

3. Testes de fallback quando Redis falha
   Teste exemplo: src/**tests**/cache-fallback.test.ts

## Alinhamento

Este código segue 95% dos padrões do projeto.
Pronto para merge após feedback acima.
```

### Workflow 2: Documentação Automática (API)

**Cenário**: Gerar documentação de novos endpoints

```bash
vectora generate-docs \
  --from "src/routes/api.ts" \
  --type "openapi" \
  --llm gemini-3-flash \
  --output docs/api.openapi.yaml
```

**Exemplo de output:**

```yaml
openapi: 3.0.0
info:
  title: Vectora API
  version: 1.0.0

paths:
  /search:
    post:
      summary: "Busca semântica (gerado por Gemini + contexto)"
      description: |
        Busca por similaridade semântica usando embeddings.
        Implementação: src/routes/search.ts
        Usa: Context Engine com Voyage 4
        Latência: ~230ms
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SearchRequest"
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SearchResponse"
        "429":
          description: "Rate limited (veja: src/middleware/rate-limit.ts)"
```

### Workflow 3: Análise de Performance (Investigação)

**Cenário**: API está lenta, precisa identificar gargalos

```bash
vectora analyze-performance \
  --query "A busca está tomando 2s. Qual é o problema?" \
  --include-logs "vectora.log" \
  --model gemini-pro \
  --output perf-report.md
```

**Análise Gemini:**

```markdown
# Performance Analysis Report

## Problema Identificado

Busca levando 2000ms quando SLA é 300ms.

## Root Cause

Reranking via Voyage Rerank 2.5 está levando 1.2s.

**Evidência no código:**

- src/context-engine.ts:145
  `const reranked = await reranker.rank(topK=100, maxTokens=2048)`

- Problema: maxTokens muito alto
- Comparação: outro projeto usa maxTokens=512 (src/search/optimized.ts:23)
  Resultado: 180ms vs seu 1200ms

## Soluções

1. **Quick win** (implementar hoje)
   Reduzir maxTokens de 2048 → 512
   Resultado esperado: 1.8s → 0.8s

2. **Medium-term** (próxima sprint)
   Implementar cache de embeddings
   Veja padrão em: src/cache/embedding-cache.ts

3. **Long-term**
   Usar Gemini 3 Flash como reranker ao invés de Voyage
   Trade-off: mais rápido mas menos preciso
   Teste: src/**tests**/reranker-comparison.ts

## Impacto

- Current: p95=2000ms, p99=3000ms
- After fix #1: p95=800ms, p99=1500ms
- After fix #2: p95=400ms, p99=600ms

## Recomendação

Aplicar fix #1 hoje (10 min change), medir antes de #2.
```

### Workflow 4: Geração de Tipos (TypeScript)

**Cenário**: API retorna JSON complexo, precisa de tipos

```bash
vectora generate-types \
  --from "src/responses/" \
  --target "typescript" \
  --model gemini-3-flash \
  --output "src/types/generated.ts"
```

**Output (tipos geralmente usados no projeto):**

```typescript
// src/types/generated.ts
// Auto-generated por Gemini via Vectora Context Engine

export interface SearchResponse {
  chunks: SearchChunk[];
  metadata: {
    retrieval_precision: number;
    latency_ms: number;
    total_searched: number;
  };
  // Padrão visto em src/types/search.ts
}

export interface SearchChunk {
  file: string;
  line_start: number;
  line_end: number;
  content: string;
  precision: number; // 0.0 - 1.0
  // Compatível com: src/__tests__/search.mock.ts
}

// Tipos gerados são 98% compatíveis com codebase existente
// Segue convenções de src/types/*
// Inclui tipos de guardrails (src/security/guardian.types.ts)
```

---

## Configuração Avançada

### Custom System Prompt

```yaml
providers:
  llm:
    model: "gemini-3-flash"
    system_prompt: |
      Você é um expert em código TypeScript.
      Sempre cite linhas de código ao responder.
      Mantenha explicações concisas.
      Foque em segurança e performance.
```

### Temperature & Parameters

```yaml
providers:
  llm:
    model: "gemini-3-flash"
    temperature: 0.7 # 0=determinístico, 1=criativo
    top_p: 0.95 # Nucleus sampling
    max_tokens: 2048
    stop_sequences:
      - "\n---\n"
```

### Streaming

Para respostas em tempo real:

```bash
vectora analyze \
  --query "Explique o módulo de autenticação" \
  --stream # Output em tempo real
  --model gemini-pro
```

---

## Integração com Context Engine

### Automatic Context Passing

Vectora passa automaticamente chunks do Context Engine para Gemini:

```text
Seu prompt: "Por que esse teste está falhando?"

Contexto enviado a Gemini:
{
  "chunks": [
    {"file": "spec/auth.test.ts", "content": "..."},
    {"file": "src/auth/jwt.ts", "content": "..."},
    {"file": "src/auth/guards.ts", "content": "..."}
  ],
  "precision": 0.78,
  "retrieval_time_ms": 234
}

Gemini lê contexto + seu prompt → resposta
```

### Reranking with Gemini

Opcionalmente, use Gemini como reranker ao invés de Voyage:

```yaml
providers:
  reranker:
    name: "gemini" # Ao invés de "voyage"
    model: "gemini-3-flash"
    # Gemini avalia relevância de cada chunk
    # Mais preciso, mas mais lento
```

---

## Safety & Guardrails

### Built-in Guardrails

Gemini tem proteções contra:

- Geração de código malicioso
- Vazamento de dados sensíveis
- Conteúdo ofensivo

### Custom Safety Rules

```yaml
providers:
  llm:
    safety:
      block_on_sensitive_patterns:
        - "api_key"
        - "password"
        - "secret"

      block_keywords:
        - "exploit"
        - "malware"
```

### Audit Logging

```bash
VECTORA_LOG_LEVEL=debug vectora analyze "..."

# Logs include:
# [Gemini Request] tokens=500, prompt_hash=abc123
# [Gemini Response] tokens=200, safety_rating=safe
```

---

## Pricing & Quotas

### Free Tier

- **Rate**: 60 requisições/minuto
- **Tokens**: 1.5M tokens/mês
- **Models**: gemini-3-flash apenas

### Pro Tier

- **Rate**: 2000 req/min
- **Tokens**: Unlimited
- **Models**: Todos

Upgrade em: [Google Cloud Console](https://console.cloud.google.com/billing)

### Monitoring Costs

```bash
vectora cost-report --period month

# Output:
# Gemini API usage:
# gemini-3-flash: $0.00 (within free tier)
# Tokens: 1,234,567 / 1,500,000
```

---

## Troubleshooting

### "API key invalid"

```bash
# Verificar se key está configurada
echo $GEMINI_API_KEY

# Se vazio, configure
export GEMINI_API_KEY="seu-valor"

# Verificar se é válida
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent" \
  -H "Content-Type: application/json" \
  -d "{\"contents\": [{\"parts\": [{\"text\": \"test\"}]}]}" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
```

### "Quota exceeded"

**Causa**: Atingiu limite de free tier.

**Solução**:

1. Upgrade para plano Pro
2. Ou aguarde reset mensal (1º do mês)
3. Ou use fallback model local:

```yaml
providers:
  llm:
    name: "gemini"
    fallback_model: "local-mistral" # Ollama local
```

### "Model not found"

**Verificar modelos disponíveis**:

```bash
vectora models list
# Mostra: gemini-3-flash, gemini-pro, ...
```

---

## Comparação: Gemini vs Alternativas

| Modelo             | Speed | Qualidade | Custo | Context     |
| ------------------ | ----- | --------- | ----- | ----------- |
| **Gemini 3 Flash** |       |           | Free  | 1M tokens   |
| Claude 3 Opus      |       |           | $$    | 200K tokens |
| GPT-4              |       |           | $$    | 128K tokens |
| Llama 2 (local)    |       |           | Free  | 4K tokens   |

**Recomendação**: Gemini é melhor para RAG (rápido + eficiente).

---

> **Próximo**: [MCP Tools Reference](../reference/mcp-tools.md)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
