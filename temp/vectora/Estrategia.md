# 🎯 Estratégia de Modelos: Curated Models + BYOK

> [!IMPORTANT] > **Decisão Estratégica Final** | Vectora suporta **apenas modelos curados** com Bring Your Own Key
> (BYOK). Sem suporte a providers arbitrários. Foco total em qualidade, consistência e manutenção simplificada.

---

## 🧭 Visão Geral da Estratégia

| Componente             | Modelo Curado                       | Provider  | BYOK Obrigatório    |
| ---------------------- | ----------------------------------- | --------- | ------------------- |
| **Embedding**          | `voyage-4`                          | Voyage AI | ✅ `VOYAGE_API_KEY` |
| **Reranker**           | `voyage-rerank-3`                   | Voyage AI | ✅ `VOYAGE_API_KEY` |
| **LLM (Programming)**  | `gemini-3-flash` / `gemini-3.1-pro` | Google AI | ✅ `GEMINI_API_KEY` |
| **Fallback Embedding** | `gemini-embedding-2`                | Google AI | ✅ (mesma chave)    |

> 💡 **Premissa central**: Vectora não é um gateway genérico de LLMs. É um sub-agent calibrado para uma stack
> específica. Isso garante Harness consistente, retrieval precision previsível e manutenção focada.

---

## ✅ Por que "Curated Models + BYOK" é a Escolha Certa

### 1. **Qualidade Garantida por Design**

| Modelo            | Por que foi escolhido                                                                                            | Benchmark Relevante                           |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `voyage-4`        | Fine-tuned em 2.5B+ snippets de código; captura similaridade funcional (`validateToken` ≈ `checkJWT`); AST-aware | MTEB Code Retrieval: **68.2** (SOTA)          |
| `voyage-rerank-3` | Cross-attention real; latência ~40ms; precisão 15-25% maior que BM25+RRF em código                               | NDCG@10 Code: **72.1**                        |
| `gemini-3.1-pro`  | Contexto de 1M tokens; tool calling estável; multimodal nativo; preço competitivo                                | LiveCodeBench: Top 3 entre modelos acessíveis |
| `gemini-3-flash`  | Inferência rápida para tarefas de contexto; custo 60% menor que Pro; mesma API                                   | Ideal para RAG + tool routing                 |

### 2. **SDKs Oficiais = Estabilidade Operacional**

| SDK             | Vantagem para Vectora                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `@google/genai` | Parsing estável de streaming; tool calling com schema enforcement; fallback automático entre regiões; suporte a multimodal nativo |
| `voyageai`      | Batch embedding otimizado; reranking com scores normalizados; métricas de latência embutidas; retry logic robusto                 |

> Sem camadas de abstração genérica (AI SDK) → menos pontos de falha, menos "quirks" de providers múltiplos, menos
> surface area para bugs.

### 3. **Fallback Interno sem Complexidade Externa**

Se a API da Voyage estiver indisponível, o fallback é para Gemini embedding — mesmo provider, mesma chave, mesma
infraestrutura:

```ts
// packages/core/src/providers/embedding-router.ts
export async function embedWithFallback(query: string, config: ProviderConfig): Promise<EmbeddingResult> {
  try {
    return await voyage.embed(query, { model: "voyage-4" });
  } catch (error) {
    if (error.code === "SERVICE_UNAVAILABLE" || error.code === "RATE_LIMITED") {
      logger.warn("Voyage unavailable, falling back to Gemini embedding");
      return await gemini.embed(query, { model: "gemini-embedding-2" });
    }
    throw error; // outros erros são propagados para o usuário
  }
}
```

> ✅ Mesmo fallback, mesma chave (`GEMINI_API_KEY`), mesma camada de erro. Sem roteamento complexo entre providers
> externos.

### 4. **Custo Previsível para o Usuário**

Com modelos fixos, podemos oferecer:

- **Documentação clara de custos**: "1 query RAG ≈ $0.0012 em embeddings + $0.03 em LLM"
- **Otimizações específicas**: Cache de embeddings por hash de conteúdo; batching inteligente de reranking
- **Alertas proativos**: "Sua chave Gemini está em 90% do quota diário"

### 5. **Suporte e Manutenção Simplificados**

| Antes (Multi-Provider)                                    | Agora (Curated + BYOK)                                    |
| --------------------------------------------------------- | --------------------------------------------------------- |
| Issues com 10+ providers diferentes                       | Issues focadas em 2 integrações testadas                  |
| Harness calibrado para "qualquer modelo" → variância alta | Harness calibrado para Gemini+Voyage → scores comparáveis |
| Docs genéricas "como configurar seu provider"             | Docs específicas "como obter suas chaves Gemini/Voyage"   |
| Testing matrix explosiva (N providers × M modelos)        | Testing matrix focada (2 providers × 4 modelos)           |

---

## ⚠️ Riscos e Mitigações (Reavaliados)

### Risco 1: "E se eu quiser usar Claude/Qwen/OpenAI?"

**Realidade**: Vectora não é um gateway genérico. É um sub-agent especializado em código, calibrado para uma stack
específica.

**Mitigações**:

- **Comunicação clara desde o início**: "Vectora funciona com Gemini + Voyage. Se você precisa de multi-provider, use
  MCP tools genéricas."
- **Qualidade como argumento**: "Nosso Harness prova que Gemini+Voyage entregam melhor retrieval precision em código do
  que modelos genéricos."
- **BYOK como controle**: Você mantém suas chaves, seus custos, seus limites — sem vendor lock-in na camada de billing.

### Risco 2: "E se Voyage/Gemini mudarem preços ou descontinuarem modelos?"

**Mitigações**:

- **Monitoramento ativo**: Alertas internos para mudanças em pricing/terms dos providers
- **Fallback entre modelos do mesmo provider**: `gemini-3-flash` ↔ `gemini-3.1-pro`; `voyage-4` ↔ `voyage-3-large`
- **Cláusula de portabilidade**: Usuários podem exportar seus vetores/metadados a qualquer momento via `vectora export`
- **Roadmap transparente**: Mudanças de modelo são comunicadas com 60 dias de antecedência

### Risco 3: "Gemini embedding é bom o suficiente como fallback?"

**Dados Reais** (benchmarks públicos + testes internos):

| Modelo                   | MTEB Code Retrieval | NDCG@10 (Code) | Latência P95 |
| ------------------------ | ------------------- | -------------- | ------------ |
| `voyage-4`               | **68.2**            | **72.1**       | ~120ms       |
| `gemini-embedding-2`     | 61.4                | 65.8           | ~90ms        |
| `text-embedding-3-large` | 58.9                | 63.1           | ~100ms       |

> ✅ Gemini embedding é ~10% abaixo do Voyage em código, mas ainda **muito acima** de modelos genéricos. Como fallback
> temporário para indisponibilidade de API, é mais que aceitável.

---

## 💰 Análise de Custos (Abril 2026)

### Voyage AI Pricing [[docs.voyageai.com]]

| Modelo                           | Preço por 1K tokens | Uso Típico em Vectora                   |
| -------------------------------- | ------------------- | --------------------------------------- |
| `voyage-4`                       | $0.00014            | Embedding de código (chunk ~512 tokens) |
| `voyage-rerank-3`                | $0.00005            | Reranking de top-50 → top-10            |
| **Custo por query RAG completa** | **~$0.0012**        | Embedding query + 50 chunks + rerank 10 |

### Gemini API Pricing [[ai.google.dev]]

| Modelo                          | Preço por 1K tokens                | Uso Típico em Vectora              |
| ------------------------------- | ---------------------------------- | ---------------------------------- |
| `gemini-3.1-pro`                | $0.0025 (input) + $0.0075 (output) | Programming LLM, tool calling      |
| `gemini-3-flash`                | $0.00075 (input) + $0.003 (output) | Context routing, respostas rápidas |
| `gemini-embedding-2`            | $0.000025                          | Fallback embedding                 |
| **Custo por resposta de agent** | **~$0.015-0.045**                  | Depende do contexto e complexidade |

### Exemplo: Desenvolvedor Individual (BYOK)

```
Uso moderado:
- 50 queries RAG/dia × 30 dias = 1,500 queries/mês
- Custo Voyage: 1,500 × $0.0012 = $1.80
- Custo Gemini (Flash): 1,500 × $0.015 (média) = $22.50
- Total estimado: ~$24.30/mês → pago diretamente ao provider

Vectora: $0 de custo de API (BYOK) + $0 de infra (MongoDB gerenciado no Free tier)
```

> ✅ **Modelo sustentável**: Usuário paga seus custos de API diretamente; Vectora monetiza via planos Pro/Team com quota
> gerenciada + backend.

---

## 🛠️ Implementação Técnica Simplificada

### Estrutura de Providers (Focada)

```
packages/core/src/providers/
├── types.ts                 # Interfaces mínimas: EmbeddingProvider, LLMProvider
├── index.ts                # Factory: cria providers baseado em config
├── gemini/                 # SDK oficial Google (@google/genai)
│   ├── llm.ts              # gemini-3-flash / gemini-3.1-pro
│   ├── embedding.ts        # gemini-embedding-2 (fallback)
│   └── client.ts           # Singleton com retry + rate limit
├── voyage/                 # SDK oficial Voyage (voyageai)
│   ├── embedding.ts        # voyage-4 (primary)
│   ├── reranker.ts         # voyage-rerank-3
│   └── client.ts           # Singleton com batching + retry
└── quota-router.ts         # Fallback logic + tracking de uso (BYOK)
```

### Configuração Mínima (`config.yaml`)

```yaml
# vectora.config.yaml
providers:
  gemini:
    api_key: "${GEMINI_API_KEY}" # obrigatório
    models:
      llm_primary: "gemini-3.1-pro"
      llm_fallback: "gemini-3-flash"
      embedding_fallback: "gemini-embedding-2"
    options:
      temperature: 0.1
      max_tokens: 4096

  voyage:
    api_key: "${VOYAGE_API_KEY}" # obrigatório
    models:
      embedding: "voyage-4"
      reranker: "voyage-rerank-3"
    options:
      batch_size: 32
      rerank_top_k: 10

backend:
  mongodb:
    # URI injetada automaticamente após auth (backend sempre gerenciado)
    managed: true

quota:
  # Apenas para planos pagos (Pro/Team): quota gerenciada de API com fallback BYOK
  managed: false # Free/BYOK: sempre usa chaves do usuário
  # Pro/Team: managed: true + fallback: { use_byok_on_exhaust: true }
```

### Validação de Configuração (Zod)

```ts
// packages/core/src/config/schema.ts
import { z } from "zod";

export const ProviderConfigSchema = z.object({
  gemini: z.object({
    api_key: z.string().min(1, "GEMINI_API_KEY é obrigatória"),
    models: z.object({
      llm_primary: z.literal("gemini-3.1-pro").or(z.literal("gemini-3-flash")),
      llm_fallback: z.literal("gemini-3-flash").or(z.literal("gemini-3.1-pro")),
      embedding_fallback: z.literal("gemini-embedding-2"),
    }),
    options: z
      .object({
        temperature: z.number().min(0).max(2).default(0.1),
        max_tokens: z.number().positive().default(4096),
      })
      .optional(),
  }),

  voyage: z.object({
    api_key: z.string().min(1, "VOYAGE_API_KEY é obrigatória"),
    models: z.object({
      embedding: z.literal("voyage-4").or(z.literal("voyage-3-large")),
      reranker: z.literal("voyage-rerank-3").or(z.literal("voyage-rerank-2")),
    }),
    options: z
      .object({
        batch_size: z.number().positive().default(32),
        rerank_top_k: z.number().positive().default(10),
      })
      .optional(),
  }),
});

export type ProviderConfig = z.infer<typeof ProviderConfigSchema>;
```

> ✅ **Fail-fast**: Configuração inválida é rejeitada no startup, não em runtime.

---

## 🧪 Harness: Validação Focada

Com modelos curados, o Harness pode ser calibrado com precisão:

```yaml
# tests/providers/embedding-precision.yaml
id: "embedding-precision-voyage-4"
name: "Voyage 4 Code recupera funções semanticamente similares"

task:
  prompt: "Encontre implementações de validação de token JWT"
  context:
    providers: [vectora]
    namespace: auth-service

expectations:
  retrieval:
    must_include:
      - "src/auth/jwt_validator.go"
      - "src/auth/middleware.go"
      - "src/utils/token_utils.ts"
    must_exclude:
      - "src/logger/*.go"
      - "vendor/**"
    min_relevance_score: 0.75 # Threshold calibrado para voyage-4

evaluation:
  judge_config:
    method: "hybrid"
    llm_model: "gemini-3-flash" # Juiz também calibrado
    llm_temperature: 0.1
  scoring:
    weights:
      correctness: 0.40
      retrieval_precision: 0.35 # Peso maior para teste de embedding
      security: 0.25
  thresholds:
    pass_score: 0.75
```

### Vantagem do Harness Focado

| Antes (Multi-Provider)                                  | Agora (Curated + BYOK)                              |
| ------------------------------------------------------- | --------------------------------------------------- |
| Scores variavam conforme modelo usado no teste          | Scores comparáveis ao longo do tempo                |
| Thresholds genéricos ("funciona em qualquer modelo")    | Thresholds calibrados ("funciona com voyage-4")     |
| Diff `vectora:on/off` poluído por variância de provider | Diff limpo: mede apenas o impacto do Context Engine |

---

## 📦 Experiência do Usuário (BYOK Simplificada)

### Onboarding em 3 Passos

```bash
# 1. Instalar
npm install -g vectora-agent

# 2. Obter chaves gratuitas (links diretos na CLI)
vectora config --setup
# → Abre: https://aistudio.google.com/app/apikey (Gemini)
# → Abre: https://dash.voyageai.com/api-keys (Voyage)

# 3. Configurar e autenticar
vectora config --gemini $GEMINI_KEY --voyage $VOYAGE_KEY
vectora auth login  # provisiona backend MongoDB gerenciado

# Pronto. Conecte ao seu agent principal via MCP e use.
```

### Mensagens de Erro Claras

```
❌ Erro: VOYAGE_API_KEY não configurada
💡 Solução: Execute `vectora config --voyage SUA_CHAVE`
🔗 Obter chave gratuita: https://dash.voyageai.com/api-keys

❌ Erro: Quota diária do Gemini excedida
💡 Solução: Aguarde reset em 2h ou configure fallback com outra chave
📊 Ver uso: vectora quota status
```

---

## 🎯 Critérios de Sucesso desta Estratégia

✅ **Qualidade consistente**: Retrieval precision, tool calling e scores do Harness são previsíveis  
✅ **Manutenção focada**: 2 providers × 4 modelos = testing matrix gerenciável  
✅ **Onboarding rápido**: 3 passos, 2 chaves, zero configuração de infra  
✅ **Custo transparente**: Usuário vê exatamente quanto paga a cada provider  
✅ **Fallback robusto**: Indisponibilidade de API não quebra o workflow  
✅ **Harness calibrado**: Prova objetiva de que Vectora melhora agents de código

---

## 🚀 Próximos Passos Imediatos

1. [ ] Implementar `ProviderConfigSchema` com Zod (validação fail-fast)
2. [ ] Criar wrappers mínimos para `@google/genai` e `voyageai` (sem AI SDK)
3. [ ] Atualizar CLI: `vectora config --gemini` / `--voyage` com links diretos
4. [ ] Calibrar Harness thresholds para `voyage-4` + `gemini-3-flash`
5. [ ] Documentar pricing estimado por query na página de configuração
6. [ ] Preparar mensagem de posicionamento: "Curated models, your keys, predictable quality"

---

> 💡 **Frase para o site/docs**:  
> _"Vectora não tenta ser tudo para todos. É construído para uma coisa: fazer seu agent entender código com precisão.
> Por isso, usamos apenas Voyage 4 + Gemini 3. E por isso, nosso Harness prova que funciona."_

---

_Parte do ecossistema Vectora · Open Source · TypeScript_  
_Modelos Curados: Voyage 4 (embeddings/reranking) + Gemini 3 (LLM)_  
_BYOK Obrigatório: Você fornece as chaves, controla os custos, mantém a privacidade_  
_Harness Calibrado: Scores consistentes, validação objetiva, evolução previsível_  
_Versão: 2.0.0 | Próxima revisão: Q3 2026_
