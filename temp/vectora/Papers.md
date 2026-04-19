# 📚 Biblioteca Técnica Vectora: Papers Expandidos + Análise Completa

> [!IMPORTANT] > **Fonte Única de Verdade Técnica** | Esta análise consolida 45+ papers acadêmicos e técnicos que
> fundamentam as decisões arquiteturais do Vectora EndGame.

---

## 🗂️ Lista Expandida de Papers (45+ Referências)

### 🔷 Núcleo Original (Solicitado)

| ID      | Paper                                                                                                       | Link                                      | Relevância para Vectora                                     |
| ------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| **P01** | Hierarchical Navigable Small World (HNSW) [[1603.09320]](https://arxiv.org/abs/1603.09320)                  | [arXiv](https://arxiv.org/abs/1603.09320) | Base do índice vetorial no Qdrant — busca ANN escalável     |
| **P02** | QJL: 1-Bit Quantized Johnson-Lindenstrauss [[2406.03482]](https://arxiv.org/abs/2406.03482)                 | [arXiv](https://arxiv.org/abs/2406.03482) | Fundamento teórico para quantização extrema de vetores      |
| **P03** | PolarQuant: Polar Transformation for KV Caches [[2502.02617]](https://arxiv.org/abs/2502.02617)             | [arXiv](https://arxiv.org/abs/2502.02617) | Pré-condicionamento ortogonal + quantização polar           |
| **P04** | TurboQuant: Extreme Compression for LLMs [[2504.19874]](https://arxiv.org/abs/2504.19874)                   | [arXiv](https://arxiv.org/abs/2504.19874) | Pipeline 3-estágios: rotação → QJL → bit packing            |
| **P05** | Large Language Models: A Survey [[2402.06196]](https://arxiv.org/abs/2402.06196)                            | [arXiv](https://arxiv.org/abs/2402.06196) | Panorama de arquiteturas, capacidades e limitações de LLMs  |
| **P06** | Model Context Protocol (MCP): Landscape & Security [[2503.23278]](https://arxiv.org/abs/2503.23278)         | [arXiv](https://arxiv.org/abs/2503.23278) | Ameaças, mitigação e direções futuras para MCP              |
| **P07** | Understanding Generative AI Content with Embedding Models [[2408.10437]](https://arxiv.org/abs/2408.10437)  | [arXiv](https://arxiv.org/abs/2408.10437) | Como embeddings capturam semântica de conteúdo gerado       |
| **P08** | Evaluating Embedding Models for AI Search Quality [[2511.22240]](https://arxiv.org/abs/2511.22240)          | [arXiv](https://arxiv.org/abs/2511.22240) | Métricas e benchmarks para seleção de modelos de embedding  |
| **P09** | Generative Reasoning Re-ranker [[2602.07774]](https://arxiv.org/abs/2602.07774)                             | [arXiv](https://arxiv.org/abs/2602.07774) | Reranking com raciocínio generativo para RAG                |
| **P10** | Rethinking the Reranker: Boundary-Aware Evidence Selection [[2602.03689]](https://arxiv.org/abs/2602.03689) | [arXiv](https://arxiv.org/abs/2602.03689) | Seleção de evidência com consciência de limites contextuais |
| **P11** | LLM-Confidence Reranker: Training-Free RAG Enhancement [[2602.13571]](https://arxiv.org/abs/2602.13571)     | [arXiv](https://arxiv.org/abs/2602.13571) | Reranking baseado em confiança do LLM, sem fine-tuning      |
| **P12** | Retrieval-Augmented Generation for LLMs: A Survey [[2312.10997]](https://arxiv.org/abs/2312.10997)          | [arXiv](https://arxiv.org/abs/2312.10997) | Survey abrangente de arquiteturas RAG                       |
| **P13** | RAG-Anything: All-in-One RAG Framework [[2510.12323]](https://arxiv.org/abs/2510.12323)                     | [arXiv](https://arxiv.org/abs/2510.12323) | Framework unificado para RAG multi-modal                    |

### 🔷 Expansão: Vetores, Quantização e Busca

| ID      | Paper                                                                                                                                                                            | Link                                                                                                              | Relevância para Vectora                                                |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **P14** | Distribution-Aware Exploration for Adaptive HNSW Search [[2512.06636]](https://arxiv.org/abs/2512.06636)                                                                         | [arXiv](https://arxiv.org/abs/2512.06636)                                                                         | Otimização adaptativa de busca HNSW baseada em distribuição            |
| **P15** | Optimization of Embeddings Storage for RAG using Binary Quantization [[2505.00105]](https://arxiv.org/abs/2505.00105)                                                            | [arXiv](https://arxiv.org/abs/2505.00105)                                                                         | Quantização binária (1-bit) para armazenamento eficiente de embeddings |
| **P16** | OneBit: Towards Extremely Low-bit LLMs [[2402.11295]](https://arxiv.org/abs/2402.11295)                                                                                          | [arXiv](https://arxiv.org/abs/2402.11295)                                                                         | Metodologia de treinamento para LLMs 1-bit nativos                     |
| **P17** | Embedding Quantization: Techniques and Trends [[EmergentMind]](https://www.emergentmind.com/topics/embedding-quantization)                                                       | [Link](https://www.emergentmind.com/topics/embedding-quantization)                                                | Panorama de técnicas de quantização para embeddings                    |
| **P18** | Efficient Code Embeddings from Code Generation Models [[2508.21290]](https://arxiv.org/abs/2508.21290)                                                                           | [arXiv](https://arxiv.org/abs/2508.21290)                                                                         | Embeddings especializados para código, derivados de modelos de geração |
| **P19** | jina-code-embeddings: Novel Suite for Code Retrieval [[NeurIPS 2025]](https://neurips.cc/virtual/2025/131652)                                                                    | [Link](https://neurips.cc/virtual/2025/131652)                                                                    | Família de embeddings para código com footprint reduzido               |
| **P20** | Code Isn't Just Text: Deep Dive into Code Embedding Models [[Medium]](https://medium.com/@abhilasha4042/code-isnt-just-text-a-deep-dive-into-code-embedding-models-418cf27ea576) | [Link](https://medium.com/@abhilasha4042/code-isnt-just-text-a-deep-dive-into-code-embedding-models-418cf27ea576) | Análise prática de embeddings para código vs texto geral               |

### 🔷 Expansão: Reranking e RAG Avançado

| ID      | Paper                                                                                                                     | Link                                                   | Relevância para Vectora                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| **P21** | Achieving Risk-aware Reranking with Information Gain for RAG [[ACM 2025]](https://dl.acm.org/doi/10.1145/3774904.3792085) | [Link](https://dl.acm.org/doi/10.1145/3774904.3792085) | Reranking que balanceia risco e benefício na seleção de contexto       |
| **P22** | HopRAG: Multi-Hop Reasoning for Logic-Aware Retrieval [[2502.12442]](https://arxiv.org/abs/2502.12442)                    | [arXiv](https://arxiv.org/abs/2502.12442)              | RAG com raciocínio lógico multi-hop via grafos de conhecimento         |
| **P23** | MultiHop-RAG: Benchmarking RAG for Multi-Hop Queries [[OpenReview]](https://openreview.net/forum?id=t4eB3zYWBK)           | [Link](https://openreview.net/forum?id=t4eB3zYWBK)     | Dataset e métricas para avaliar RAG em queries multi-hop               |
| **P24** | RT-RAG: Reasoning Trees for Multi-Hop Question Answering [[2601.11255]](https://arxiv.org/abs/2601.11255)                 | [arXiv](https://arxiv.org/abs/2601.11255)              | Decomposição estruturada de queries complexas em árvores de raciocínio |
| **P25** | cAST: Enhancing Code RAG with AST-based Recursive Chunking [[2506.15655]](https://arxiv.org/abs/2506.15655)               | [arXiv](https://arxiv.org/abs/2506.15655)              | Chunking de código guiado por AST para RAG mais preciso                |
| **P26** | GNN-Coder: Boosting Semantic Code Retrieval with Graph Neural Networks [[2502.15202]](https://arxiv.org/abs/2502.15202)   | [arXiv](https://arxiv.org/abs/2502.15202)              | Uso de GNNs em ASTs para recuperação semântica de código               |

### 🔷 Expansão: Code LLMs e Representação de Código

| ID      | Paper                                                                                                                                       | Link                                                       | Relevância para Vectora                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------- |
| **P27** | A Survey on Large Language Models for Code Generation [[ACM 2026]](https://dl.acm.org/doi/10.1145/3747588)                                  | [Link](https://dl.acm.org/doi/10.1145/3747588)             | Survey abrangente de LLMs especializados em geração de código   |
| **P28** | SemRep: Generative Code Representation Learning [[2603.13640]](https://arxiv.org/abs/2603.13640)                                            | [arXiv](https://arxiv.org/abs/2603.13640)                  | Representação generativa de código para transformação e análise |
| **P29** | Code Representation Learning at Scale [[2402.01935]](https://arxiv.org/abs/2402.01935)                                                      | [arXiv](https://arxiv.org/abs/2402.01935)                  | Pré-treinamento em larga escala para representação de código    |
| **P30** | ASTNN: Neural Source Code Representation Based on Abstract Syntax Tree [[ResearchGate]](https://www.researchgate.net/publication/335427176) | [Link](https://www.researchgate.net/publication/335427176) | Representação neural de código via decomposição de AST          |
| **P31** | Repository-level Code Search with Neural Retrieval Methods [[2025]](https://www.researchgate.net/publication/388919874)                     | [Link](https://www.researchgate.net/publication/388919874) | Combinação de BM25 + CodeBERT para busca neural em repositórios |

### 🔷 Expansão: KV Cache e Otimização de Inferência

| ID      | Paper                                                                                                                                                                  | Link                                                                                                           | Relevância para Vectora                                       |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **P32** | EvolKV: Evolutionary KV Cache Compression for LLM Inference [[2025]](https://aclanthology.org/2025.findings-emnlp.88.pdf)                                              | [Link](https://aclanthology.org/2025.findings-emnlp.88.pdf)                                                    | Compressão adaptativa de KV cache por camada e tarefa         |
| **P33** | KV Cache Compression for Inference Efficiency: A Review [[2508.06297]](https://arxiv.org/abs/2508.06297)                                                               | [arXiv](https://arxiv.org/abs/2508.06297)                                                                      | Survey de técnicas: pruning, quantização, retenção adaptativa |
| **P34** | KVComp: LLM-Aware KV Cache Compression [[EmergentMind]](https://www.emergentmind.com/topics/kvcomp)                                                                    | [Link](https://www.emergentmind.com/topics/kvcomp)                                                             | Framework de compressão com limite de erro controlado         |
| **P35** | Decoupled KV Cache Compression for Long-Context LLMs [[HKUST]](https://urop.hkust.edu.hk/projects/decoupled-kv-cache-compression-efficient-long-context-llm-inference) | [Link](https://urop.hkust.edu.hk/projects/decoupled-kv-cache-compression-efficient-long-context-llm-inference) | Compressão desacoplada para contextos longos                  |

### 🔷 Expansão: Tool Calling e Confiabilidade de Agents

| ID      | Paper                                                                                                                                                                                        | Link                                                                                                                                  | Relevância para Vectora                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **P36** | Improving Tool Calling Accuracy for Large Language Models [[OpenReview 2026]](https://openreview.net/forum?id=gkTx4sPyAw)                                                                    | [Link](https://openreview.net/forum?id=gkTx4sPyAw)                                                                                    | Geração baseada em templates para tool calling mais preciso      |
| **P37** | A Comprehensive Survey of Benchmarks for Tool Calling in LLMs [[HuggingFace]](https://huggingface.co/datasets/tuandunghcmut/BFCL_v4_information)                                             | [Link](https://huggingface.co/datasets/tuandunghcmut/BFCL_v4_information)                                                             | Benchmarks e métricas para avaliar tool calling                  |
| **P38** | Alignment for Efficient Tool Calling of LLMs [[2503.06708]](https://arxiv.org/abs/2503.06708)                                                                                                | [arXiv](https://arxiv.org/abs/2503.06708)                                                                                             | Alinhamento multi-objetivo para decisão dinâmica de uso de tools |
| **P39** | Mastering LLM Tool Calling: Complete Framework [[ML Mastery]](https://machinelearningmastery.com/mastering-llm-tool-calling-the-complete-framework-for-connecting-models-to-the-real-world/) | [Link](https://machinelearningmastery.com/mastering-llm-tool-calling-the-complete-framework-for-connecting-models-to-the-real-world/) | Framework prático: Data Access, Computation, Action              |

### 🔷 Expansão: Segurança, Isolamento e Multi-Tenancy

| ID      | Paper                                                                                                                                                                                                     | Link                                                                                                                                | Relevância para Vectora                                              |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **P40** | Advanced Sandboxing Techniques for Secure AI Agent Deployment [[GetUnleash 2026]](https://www.getunleash.io/en/blog/advanced-sandboxing-techniques-for-secure-ai-agent-deployment)                        | [Link](https://www.getunleash.io/en/blog/advanced-sandboxing-techniques-for-secure-ai-agent-deployment)                             | WebAssembly, MicroVMs e MITM proxies para sandboxing de agents       |
| **P41** | Practical Security Guidance for Sandboxing Agentic Workflows [[NVIDIA 2026]](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/) | [Link](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/) | Controles de segurança: isolamento de kernel, rede e filesystem      |
| **P42** | OS-Level Sandboxing: Kernel Isolation for AI Agents [[DEV Community 2026]](https://dev.to/uenyioha/os-level-sandboxing-kernel-isolation-for-ai-agents-3fdg)                                               | [Link](https://dev.to/uenyioha/os-level-sandboxing-kernel-isolation-for-ai-agents-3fdg)                                             | Isolamento em nível de SO: bwrap, namespaces, cgroups                |
| **P43** | Multi-Tenancy in Vector Databases: Isolation Strategies [[Pinecone]](https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/vector-database-multi-tenancy/)               | [Link](https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/vector-database-multi-tenancy/)       | Namespaces, metadata filtering e RBAC para isolamento multi-tenant   |
| **P44** | 5 Ironclad Rules for Multi-Tenant Vector Isolation [[Medium 2025]](https://medium.com/@ThinkingLoop/5-ironclad-rules-for-multi-tenant-vector-isolation-41d8ec2c3a20)                                      | [Link](https://medium.com/@ThinkingLoop/5-ironclad-rules-for-multi-tenant-vector-isolation-41d8ec2c3a20)                            | Regras para isolamento: namespaces, rate limits, QoS, key management |
| **P45** | When LLMs Meet Vector Databases: A Survey [[2402.01763]](https://arxiv.org/abs/2402.01763)                                                                                                                | [arXiv](https://arxiv.org/abs/2402.01763)                                                                                           | Desafios de isolamento, segurança e eficiência em sistemas híbridos  |

---

## 🔍 Análise Técnica por Domínio

### 🧭 1. Vetores e Busca Semântica (HNSW + Quantização)

#### HNSW: A Base Escalável

- **Princípio**: Grafos small-world em camadas permitem busca ANN com complexidade logarítmica [[1]][[2]].
- **Para Vectora**: Qdrant implementa HNSW com `memmap` para índices em disco, permitindo codebases grandes sem esgotar
  RAM [[3]].
- **Otimização Recente**: Adaptive HNSW ajusta parâmetros `M` e `ef_construction` dinamicamente baseado na distribuição
  da query [[P14]].

#### Quantização Extrema: Do Teórico ao Prático

| Técnica                  | Compressão | Perda de Acurácia | Uso Recomendado                 |
| ------------------------ | ---------- | ----------------- | ------------------------------- |
| **Scalar Quant (8-bit)** | 4x         | <1%               | Default para produção           |
| **Binary Quant (1-bit)** | 32x        | 2-5%              | Datasets públicos muito grandes |
| **QJL (1-bit teórico)**  | 32x+       | ~0% (teórico)     | Pesquisa, não produção ainda    |
| **PolarQuant**           | 8-16x      | <1%               | KV cache de LLMs locais         |
| **TurboQuant**           | 6-20x      | ~0%               | KV cache + embeddings vetoriais |

**Insight Crítico**: TurboQuant combina PolarQuant (pré-condicionamento ortogonal) + QJL (estabilização 1-bit) + bit
packing [[P04]][[P46]][[P47]]. Isso permite:

- Busca Hamming acelerada (XOR + Popcount em hardware)
- Contextos de 128k-1M tokens em GPUs de consumo
- Zero calibração (diferente de KVTC da NVIDIA)

**Para Vectora**: Usar TurboQuant no pipeline de embeddings locais (llama.cpp) para reduzir RAM em 8-16x sem perda
mensurável de precisão.

---

### 🔁 2. Reranking: O Filtro de Precisão

#### Por que Reranking é Obrigatório para Código

Vector DBs retornam por similaridade cossena. Em código, isso traz ruído:

- `node_modules/` semanticamente parecidos com código do usuário
- `test/` files que espelham `src/` mas são irrelevantes para a query
- Comentários/docstrings que "parecem" a query mas não têm lógica executável

#### Técnicas de Reranking Comparadas

| Técnica                                   | Latência | Precisão em Código    | Custo      | Recomendação                    |
| ----------------------------------------- | -------- | --------------------- | ---------- | ------------------------------- |
| **BM25 + RRF**                            | ~5ms     | Baixa                 | $0         | Fallback rápido                 |
| **Cross-Encoder (BGE)**                   | ~120ms   | Boa                   | $0 (local) | Produção local                  |
| **Cohere Rerank v3.5**                    | ~50ms    | Alta                  | $$         | Produção cloud                  |
| **Voyage Rerank 2**                       | ~40ms    | Alta + code-optimized | $$         | Produção cloud (código)         |
| **Generative Reasoning Reranker** [[P09]] | ~200ms   | Muito Alta            | $$$        | Casos críticos                  |
| **LLM-Confidence Reranker** [[P11]]       | ~150ms   | Alta (sem treino)     | $$         | Quando fine-tuning não é viável |

**Pipeline Recomendado para Vectora**:

```text
Query → Embedding → Qdrant (top-K=50) → Reranker (top-N=10) → Context Engine → LLM
```

**Feature Chave**: `retrieval_precision` no Harness mede a eficácia do reranker:

```yaml
expectations:
  retrieval:
    min_reranker_score: 0.72
    noise_reduction_ratio: 0.65 # % de ruído removido vs top-K bruto
```

---

### 💻 3. Code LLMs e Representação de Código

#### Embeddings Especializados para Código

- **jina-code-embeddings** [[P19]]: Fine-tuned em 2.5B+ snippets de código, suporta NL→Code e Code→Code retrieval.
- **Voyage-3-Code**: Otimizado para imports, AST-aware, captura similaridade funcional (`validateToken` ≈ `checkJWT`).
- **Qwen3-Embedding**: Open-weight, bom equilíbrio entre código e documentação técnica.

**Para Vectora**: Oferecer seleção por caso de uso:

```yaml
embedding:
  strategy: "auto" # ou "code", "docs", "hybrid"
  models:
    code: "voyage-3-code"
    docs: "qwen3-embedding"
    hybrid: "jina-code-v2"
```

#### Representação Estrutural: AST + GNN

- **ASTNN** [[P30]]: Decompõe ASTs grandes em sequências de sub-árvores para representação neural.
- **GNN-Coder** [[P26]]: Usa Graph Neural Networks em ASTs para capturar dependências estruturais.
- **cAST** [[P25]]: Chunking recursivo guiado por AST para RAG de código mais preciso.

**Para Vectora**: Integrar parsing AST (via `tree-sitter`) no pipeline de ingestão:

```ts
// packages/context/src/ast-parser.ts
export function parseCodeForRAG(filePath: string, content: string): CodeChunk[] {
  const ast = treeSitter.parse(content);
  return recursiveChunk(ast, {
    maxSize: 512, // tokens por chunk
    preserveSymbols: true, // manter nomes de funções/variáveis
    includeImports: true, // anexar lista de imports ao chunk
  });
}
```

---

### ⚡ 4. KV Cache e Otimização de Inferência Local

#### O Problema do KV Cache

Em modelos com contexto longo (100k+ tokens), o KV Cache (ativações de tokens anteriores) pode consumir mais memória que
os pesos do modelo [[P33]].

#### Técnicas de Compressão

| Técnica                     | Princípio                      | Compressão | Uso no Vectora                     |
| --------------------------- | ------------------------------ | ---------- | ---------------------------------- |
| **Quantização (int8/int4)** | Reduz precisão numérica        | 2-4x       | Default para inferência local      |
| **Pruning Adaptativo**      | Remove tokens menos relevantes | 2-8x       | Contextos muito longos             |
| **EvolKV** [[P32]]          | Compressão por camada + tarefa | 4-12x      | Quando há múltiplos tipos de query |
| **TurboQuant** [[P04]]      | Rotação + QJL + bit packing    | 6-20x      | Modo "ultra-local" com llama.cpp   |

**Para Vectora**: Habilitar compressão dinâmica baseado no hardware:

```ts
// packages/llm/src/local-inference.ts
export function selectKVCompression(hardware: HardwareProfile): KVCompressionConfig {
  if (hardware.vramGB < 8) {
    return { method: "turboquant", bits: 1, target: "vram" };
  }
  if (hardware.ramGB < 16) {
    return { method: "evolkv", bits: 4, target: "ram" };
  }
  return { method: "scalar", bits: 8, target: "disk" }; // fallback
}
```

---

### 🛠️ 5. Tool Calling: Confiabilidade e Validação

#### O Desafio: LLMs Não São Determinísticos

Mesmo com temperature=0, LLMs podem:

- Gerar args de tool em formato inconsistente
- Chamar tools não permitidas
- Ignorar constraints de namespace

#### Soluções da Literatura

- **Template-Based Generation** [[P36]]: Usar schemas JSON pré-definidos em vez de geração livre.
- **Multi-Objective Alignment** [[P38]]: Treinar o modelo para estimar seus próprios limites de conhecimento e decidir
  quando chamar tools.
- **Confidence-Aware Routing** [[P11]]: Usar a confiança do LLM para decidir entre resposta direta vs tool call.

**Para Vectora**: Camada de adaptação + validação Zod:

```ts
// packages/core/src/tool-router.ts
export async function executeToolCall(
  rawCall: LLMToolCall,
  schema: ZodSchema,
  guardian: Guardian,
): Promise<ToolResult> {
  // 1. Validar schema com Zod (falha rápido se args inválidos)
  const validated = schema.safeParse(rawCall.args);
  if (!validated.success) {
    throw new ToolValidationError(`Invalid args: ${validated.error.message}`);
  }

  // 2. Validar segurança com Guardian
  if (!guardian.validateToolCall(rawCall.tool, validated.data)) {
    throw new SecurityError(`Tool call blocked: ${rawCall.tool}`);
  }

  // 3. Executar com interceptação para Harness
  return await interceptor.wrapExecution(() => toolRegistry.execute(rawCall.tool, validated.data));
}
```

---

### 🔐 6. Segurança, Isolamento e Multi-Tenancy

#### Sandboxing de Agents: Níveis de Isolamento

| Nível         | Técnica                       | Isolamento            | Overhead | Uso no Vectora                            |
| ------------- | ----------------------------- | --------------------- | -------- | ----------------------------------------- |
| **Process**   | Namespaces Linux, cgroups     | Médio                 | Baixo    | Default para Trust Folder                 |
| **Container** | Docker, Podman                | Alto                  | Médio    | Modo "team" com isolamento por projeto    |
| **MicroVM**   | Firecracker, Cloud Hypervisor | Muito Alto            | Alto     | Modo "enterprise" com compliance rigoroso |
| **WASM**      | Wasmer, Wasmtime              | Alto (somente código) | Baixo    | Execução de snippets de código gerado     |

**Para Vectora**: Implementar isolamento em camadas:

```yaml
# vectora.config.yaml
security:
  trust_folder: "/home/user/projects/my-app"
  isolation:
    default: "process" # namespaces + cgroups
    team_mode: "container" # Docker por projeto
    enterprise: "microvm" # Firecracker para compliance
  guardian:
    hard_blocklist: [".env", "*.key", "*.pem", "node_modules/**"]
    sanitize_output: true
    audit_log: true
```

#### Multi-Tenancy em Vector Databases

- **Namespaces no Qdrant**: Isolamento lógico com payload filtering obrigatório [[P43]][[P44]].
- **RLS no Supabase**: Row Level Security no Postgres para metadados e permissões.
- **Payload Encryption**: Criptografia de vetores sensíveis em repouso (opcional para namespaces `private`).

**Para Vectora**: Garantir que toda query vetorial inclua filtro por `namespace_id`:

```ts
// packages/infra/src/qdrant-client.ts
export async function searchWithIsolation(
  collection: string,
  query: number[],
  namespace: string,
  visibility: "public" | "team" | "private",
) {
  return await qdrant.search(collection, {
    vector: query,
    limit: 50,
    filter: {
      must: [
        { key: "namespace_id", match: { value: namespace } },
        { key: "visibility", match: { value: visibility } },
      ],
    },
  });
}
```

---

## 🎯 Síntese: Decisões Arquiteturais Fundamentadas

### ✅ O Que Manter (Com Base nos Papers)

| Decisão                                                 | Fundamentação Acadêmica | Implementação no Vectora                                 |
| ------------------------------------------------------- | ----------------------- | -------------------------------------------------------- |
| **HNSW + Quantização Escalar (8-bit)**                  | P01, P14, P17           | Qdrant collection com `scalar: { type: 'int8' }`         |
| **Reranker em 2-estágios**                              | P09, P10, P11, P21      | `top-K=50 → rerank → top-N=10` no Context Engine         |
| **Embeddings Especializados para Código**               | P18, P19, P20, P27      | Seleção por `embedding.strategy: "code"`                 |
| **AST-Guided Chunking para RAG**                        | P25, P26, P30           | `tree-sitter` + `recursiveChunk` no pipeline de ingestão |
| **TurboQuant para Inferência Local**                    | P03, P04, P32, P34      | Habilitar via `--local-llm --kv-compression turboquant`  |
| **Validação Zod + Guardian para Tool Calling**          | P36, P38, P40           | Middleware em `ToolRouter` com schema enforcement        |
| **Isolamento Multi-Camada (Process/Container/MicroVM)** | P40, P41, P42, P43      | Configuração por `security.isolation` no YAML            |

### ⚠️ O Que Evitar (Com Base nos Papers)

| Prática                                          | Risco Identificado                                                  | Alternativa Recomendada                                                    |
| ------------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Binary Quant (1-bit) para produção**           | Perda de 2-5% em acurácia pode impactar retrieval precision [[P15]] | Usar apenas para datasets públicos muito grandes, com validação no Harness |
| **Reranking sem fallback determinístico**        | Latência alta pode degradar UX em queries simples [[P21]]           | Implementar `deterministic_fallback: true` no judge config                 |
| **Tool calling sem schema validation**           | LLMs podem gerar args inválidos mesmo com temperature=0 [[P36]]     | Sempre usar Zod + Guardian antes de executar qualquer tool                 |
| **Isolamento apenas lógico (namespaces)**        | Não protege contra escape via symlink ou syscall [[P42]]            | Combinar namespaces com process-level isolation (cgroups, namespaces)      |
| **KV cache sem compressão em hardware limitado** | Pode esgotar RAM em contextos >32k tokens [[P33]]                   | Habilitar compressão adaptativa baseada em `hardwareProfile`               |

---

## 🚀 Próximos Passos Técnicos

1. **Implementar Pipeline de Reranking** (`packages/reranker/`) com suporte a Cohere, Voyage e BGE local
2. **Adicionar AST Parsing** no ingestor de código (`packages/context/src/ast-parser.ts`)
3. **Configurar TurboQuant** no provider local (`packages/llm/src/local-inference.ts`)
4. **Atualizar Schema do Harness** com métricas de reranking (`retrieval_precision`, `noise_reduction_ratio`)
5. **Documentar Guia de Seleção de Modelos** baseado em caso de uso (code/docs/hybrid)

---

> 💡 **Frase para guardar**:  
> _"Embedding encontra candidatos. Reranker filtra os relevantes. AST estrutura o contexto. TurboQuant comprime sem
> perder. Guardian protege. Harness valida. Vectora orquestra tudo."_

---

_Parte do ecossistema Vectora · Open Source · TypeScript · Provider-Agnostic_
