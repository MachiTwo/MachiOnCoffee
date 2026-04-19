---
title: RAG Conectado (Connected RAG)
slug: rag
date: "2026-04-18T22:30:00-03:00"
type: docs
tags:
  - ai
  - architecture
  - concepts
  - context-engine
  - mcp
  - rag
  - vectora
sidebar:
  open: true
---

{{< lang-toggle >}}

Você já perguntou a um agente de IA sobre uma função no seu projeto e ele respondeu algo que parecia certo, mas que ignorava completamente como aquela função era usada no resto do sistema? Isso é o sintoma clássico do **RAG fragmentado**.

## O que é RAG?

**RAG (Retrieval-Augmented Generation)** é a técnica de fornecer dados externos (como seus arquivos de código) para um LLM no momento da pergunta. Em vez de o modelo "adivinhar" baseado no que aprendeu no treino, ele consulta seus documentos e responde baseado neles.

```text
Query ("Como authenticar?")
    ↓
Retrieval (Busca em codebase)
    ↓
Augmentation (Enriquece prompt)
    ↓
Generation (LLM responde com contexto)
```

Parece perfeito, certo? Mas para código, o RAG comum é perigoso.

## O Problema: RAG Tradicional vs Código

| Aspecto | RAG Tradicional | Problema para Código |
|---------|-----------------|----------------------|
| **Busca** | Similaridade semântica | Ignora dependências implícitas |
| **Contexto** | Fragmentos isolados | Sem visão de fluxo de dados |
| **Resultado** | "5 blocos de texto" | LLM não vê padrões arquiteturais |
| **Uso** | Documentação, artigos | ❌ Não funciona para código |

**Exemplo Real:**

Busca: "Como faço login?"

RAG Tradicional retorna:
```javascript
// Trecho 1: loginUser function
async function loginUser(email, password) {
  const user = await db.findUser(email);
  // ... código de validação
}
```

Mas **não retorna**:
- O middleware de autenticação que chama `loginUser`
- A interface `User` que define os tipos
- A configuração de JWT que usa as credenciais
- Os testes que mostram o comportamento esperado

Resultado: LLM responde incompleto ou incorreto.

## A Solução: RAG Conectado (Context Engine)

No Vectora, o RAG não é apenas "buscar texto". Ele funciona através de um **Context Engine** que entende a estrutura:

### 1. **Busca Multimodal**

Combina 3 estratégias:

```text
Query: "Como validar JWT?"
    ↓
├─ Embeddings (Voyage 4) → "validateToken function"
├─ AST Analysis (Estrutural) → "imports de jwt, configuração"
└─ Grep (Keywords) → "JWT_SECRET, token validation"
    ↓
Combine results → Top-5 chunks estruturados
```

### 2. **Multi-hop Reasoning**

O motor não faz só uma busca:

```text
1. Busca inicial: "validateToken" → encontra src/auth/jwt.ts
2. Análise: Vê que chama "decode(token)"
3. Salto 1: Busca "decode" → encontra lib crypto
4. Análise: Vê uso de JWT_SECRET
5. Salto 2: Busca "JWT_SECRET" → encontra config.ts
    ↓
Resultado: Token validado → Estrutura completa
```

### 3. **Composição Estruturada**

O contexto retornado não é lista de strings:

```json
{
  "main_file": "src/auth/jwt.ts",
  "functions": ["validateToken", "refreshToken"],
  "dependencies": [
    { "file": "src/config.ts", "why": "Provides JWT_SECRET" },
    { "file": "src/models/User.ts", "why": "Defines User type" }
  ],
  "tests": ["spec/jwt.test.ts (8 tests)"],
  "usage_locations": [
    { "file": "src/middleware/auth.ts", "line": 34 }
  ]
}
```

## Por que isso importa?

Quando o contexto é **conectado**:

| Métrica | RAG Tradicional | RAG Conectado |
|---------|-----------------|-------------|
| **Alucinações** | Alto (30%+) | Baixo (<5%) |
| **Quebra de sistema** | Frequente | Raro |
| **Tokens gastos** | Alto (dump arquivo) | Otimizado (cirúrgico) |
| **Tempo resposta** | Inconsistente | Previsível <300ms |

## Exemplo Comparativo

### Cenário: Refatorar autenticação

**RAG Tradicional:**
- "Mude de JWT para OAuth2"
- LLM não vê que a mudança quebra 47 places
- Resultado: Sistema quebra em produção

**RAG Conectado (Vectora):**
- Busca "authenticação"
- Retorna: auth middleware (3 places), JWT validation (47 places), config (1 place)
- LLM vê contexto completo
- Resultado: Refactoring correto, sem quebras

---

## Próximos Passos

- [Context Engine](./context-engine.md) — Como o engine busca
- [Vector Search](./vector-search.md) — Técnica de embeddings
- [Reranker](./reranker.md) — Refinamento de resultados

---

> 💡 RAG Conectado é o diferencial do Vectora para código.
