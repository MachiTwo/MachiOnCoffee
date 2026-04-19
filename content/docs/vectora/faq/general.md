---
title: General
slug: general
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - general
  - mcp
  - vectora
---

{{< lang-toggle >}}

Respostas rápidas para as dúvidas mais comuns sobre Vectora - funcionamento, custo, uso em produção, segurança e muito mais.

## O Que é Vectora?

**Vectora** é um **semantic search engine** para código que indexa seu codebase inteiro e permite buscar por significado semântico, não só por palavras-chave. Se integra com IDEs (Claude Code, Cursor, VS Code) via MCP para fornecer contexto inteligente e governado ao seu agent de IA.

**Como funciona:**
1. Você indexa seu código (`npm install -g vectora && vectora index`)
2. Código é dividido em chunks e embedado via Voyage 4 (1536D vectors)
3. Vetores são armazenados em Qdrant com metadata (arquivo, linhas, namespace)
4. Quando você faz uma query ("Como validar tokens?"), Vectora:
   - Transforma query em vetor
   - Busca chunks similares via HNSW (fast nearest neighbors)
   - Reranqueia top-100 → top-10 via Voyage Rerank 2.5
   - Retorna chunks com contexto estruturado

**Exemplo prático:**
- Query: "Como validar tokens JWT?"
- **Sem Vectora**: Busca por "JWT" retorna 5 arquivos, nenhum útil
- **Com Vectora**: Encontra `validateToken()` em auth.ts, middleware em guards.ts, tipos em jwt.types.ts - tudo relevante

**Resultado**: Seu agent de IA recebe contexto governado + validado, não alucinações.

---

## Como Funciona?

```text
1. Index seu código (uma vez)
   - Divide em chunks
   - Gera embeddings (Voyage 4)
   - Armazena em Qdrant
   
2. Busca semântica
   - Sua pergunta → embedding
   - HNSW busca chunks similares
   - Reranking (Voyage Rerank 2.5)
   - Retorna top-10
   
3. Integração com IDE
   - Claude Code / Cursor / VS Code
   - Mostra chunks contextuais
   - Você continua trabalhando
```

---

## Qual é o Custo?

**Free Tier** (para sempre):
- Unlimited searches locais
- Unlimited indexação
- 60 req/min API limits (Gemini, Voyage)
- BYOK (use suas chaves)

**Pro** ($29/mês):
- Unlimited API requests
- 50 usuários simultâneos
- Webhooks + custom domain
- 99.9% SLA

**Team** (Customizado):
- On-premise + SSO/LDAP
- 99.99% SLA
- Dedicated support

---

## Quanto Tempo Leva para Indexar?

**Pela primeira vez**:
- 10K linhas: <1 minuto
- 100K linhas: 5-10 minutos
- 1M linhas: 30-60 minutos

**Incremental** (apenas mudanças):
- Geralmente <30 segundos

---

## Quanto Espaço em Disco?

A razão é aproximadamente **1:10**.

Se seu código é 50MB:
- Índice Qdrant: ~5MB
- Cache: 100MB

Total: ~105MB

---

## Posso Usar em Produção?

**Free Tier**: Não (1 usuário simultâneo, sem SLA)

**Pro Tier**: Sim (99.9% SLA, até 50 usuários)

**Team Tier**: Sim (99.99% SLA, on-premise option)

---

## Meus Dados São Seguros?

**SIM.**

✅ BYOK - você controla as chaves
✅ Criptografado em disco (AES-256)
✅ Criptografado em trânsito (TLS 1.3)
✅ Guardian blocklist (protege .env, secrets)
✅ RBAC (controle de usuários)
✅ Audit logging (rastreia tudo)

---

## Funciona com Qual Linguagem?

**Sim, todas:**
- TypeScript / JavaScript
- Python
- Go
- Java / Kotlin
- C# / .NET
- Rust
- C++ / C
- Ruby
- PHP
- SQL
- YAML / JSON
- Markdown

Voyage 4 (embedding model) entende estruturas semânticas em qualquer linguagem.

---

## Posso Usar Offline?

**Não completamente, mas quase.**

```text
Embedding: Precisa Voyage API
Reranking: Precisa Voyage Rerank API
LLM: Precisa Gemini API
Search local: 100% offline (Qdrant local)
```

**Alternativa 100% Offline**:
Use Ollama para embeddings locais:

```bash
docker run ollama/ollama
vectora config set EMBEDDING_PROVIDER ollama
```

---

## Quanto Custa para Escalar?

| Aspecto | Free | Pro | Team |
|---------|------|-----|------|
| **Código** | Unlimited | Unlimited | Unlimited |
| **Usuários** | 1 | 50 | Unlimited |
| **API calls** | 60/min | Unlimited | Custom |
| **Custo extra** | Grátis | $0.50/user | Por contato |

**Exemplo escalando**:
- 1 pessoa: Free
- 5 pessoas: Pro ($29)
- 50+ pessoas: Team ($X)

---

## Como Funciona com Múltiplos Projetos?

Cada projeto tem seu namespace:

```bash
# Projeto A
vectora init --namespace "empresa-projectA"

# Projeto B
vectora init --namespace "empresa-projectB"

# São completamente isolados
# Busca em A não encontra chunks de B
```

---

## Posso Usar Vectora com Git?

**Sim.**

```bash
# Ignorar índice
echo ".vectora/" >> .gitignore

# Reconstririr em novo clone
git clone ...
vectora index
```

**Sugestão**: Commit vectora.config.yaml, ignore .vectora/

---

## Qual IDE é Melhor?

| IDE | Vectora | Vantagem |
|-----|---------|----------|
| Claude Code | MCP nativo | Integração perfeita |
| Cursor | MCP nativo | Similar a Claude Code |
| VS Code | Extension | UI nativa no editor |
| ChatGPT | Custom GPT | Sem sair do ChatGPT |

**Recomendação**: Use qual você já usa. Vectora funciona igualmente bem.

---

## Posso Deletar um Arquivo?

Você ainda quer que ele seja indexado?

**Sim**: Reorganizar (mover arquivo)
```bash
mv src/old-api.ts src/deprecated/old-api.ts
vectora index --incremental
# Novo path é indexado, antigo removido
```

**Não**: Deletar completamente
```bash
rm src/old-api.ts
vectora index --incremental
# Chunks relacionados são removidos
```

---

## Quanto Tempo Leva para Buscar?

Geralmente:
- **Embedding**: ~100ms
- **Search (HNSW)**: ~80ms
- **Reranking**: ~50ms
- **Total**: **~230ms**

Com rede (APIs):
- **Com latência**: ~300-500ms

---

## Há Limite de Tamanho de Projeto?

**Local (Free)**: Não (disk space é o limite)

**Pro**: Não (AWS managed)

**Team**: Testado até 10M chunks

---

## Posso Compartilhar um Projeto?

**Sim:**

```bash
# Convidar usuário
vectora user create \
  --email colleague@company.com \
  --namespace seu-projeto \
  --role editor

# Colleague pode buscar e indexar
```

---

## Como Faço Backup?

```bash
# Exportar tudo
vectora export --namespace seu-projeto --output backup.tar.gz

# Depois:
# Guardar em S3, Azure, ou local
```

Para restore:
```bash
vectora import --from backup.tar.gz --namespace seu-projeto
```

---

## Posso Usar Meu Próprio LLM?

**Sim, via API.**

```yaml
# vectora.config.yaml
providers:
  llm:
    name: "openai"  # ou "anthropic", "custom"
    model: "gpt-4"
    api_key: "${OPENAI_API_KEY}"
```

Ou local (Ollama):
```bash
docker run ollama/ollama
vectora config set LLM_PROVIDER ollama
```

---

## Suporta Múltiplas Linguagens?

**Código**: Sim, todas as linguagens

**Interface**: Sim
- Português ✅
- English ✅
- Español (coming soon)
- Français (coming soon)

---

## Há API REST?

**Sim, em Pro e Team.**

```bash
curl -X POST https://seu-dominio.vectora.app/search \
  -H "Authorization: Bearer sk-proj-..." \
  -d '{"query": "login", "top_k": 10}'
```

---

## Posso Usar em Monorepo?

**Sim.**

```yaml
# vectora.config.yaml
indexing:
  paths:
    - packages/backend/src
    - packages/frontend/src
    - packages/shared/src
  exclude:
    - node_modules
    - build
    - dist
```

---

## Qual é a Comunidade?

**Open Source (MIT License)**

- GitHub: [github.com/kaffyn/vectora](https://github.com/kaffyn/vectora)
- Discussions: [GitHub Discussions](https://github.com/kaffyn/vectora/discussions)
- Issues: [Bug reports](https://github.com/kaffyn/vectora/issues)
- Docs: [vectora.app/docs](https://vectora.app/docs)

---

> 💡 **Próximo**: [FAQ - Billing](./billing.md)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
