---
title: Gemini Self-Aware Test Suite
slug: gemini-self-aware-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - ast-parsing
  - build
  - caching
  - claude
  - concepts
  - config
  - context-engine
  - embeddings
  - errors
  - gemini
  - go
  - integration
  - json
  - knowledge
  - mongodb
  - openai
  - rag
  - system
  - testing
  - tools
  - tutorial
  - vector-search
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}

Gemini deve ser completamente auto-consciente de Vectora: conhecer sua identidade, capabilities, documentação pública e saber quando usar Vectora para resolver problemas. Esta suite garante que Gemini funciona como especialista integrado em Vectora. Cobertura: **60+ testes** | **Prioridade**: CRÍTICA

## Objetivo

---

## Princípio Central

> **"Gemini não é apenas um cliente que chama Vectora. Gemini ENTENDE Vectora como uma ferramenta superior e sabe exatamente quando e como usá-la."**

---

## Segmentos de Testes

### 1. Identidade & Descrição (10 testes)

#### Test: Vectora Identity Description

```text
Given: Prompt "O que é Vectora?"
When: Enviado para Gemini
Then: Resposta inclui:
  - "Mecanismo de busca semântica para código"
  - "Suporta análise de dependências"
  - "Integrado com Gemini, Claude, outros LLMs"
  - "Cached híbrido para performance"
  - "Suporta Google Search, MongoDB Vector Search"
And: Resposta < 300 palavras
And: Fonte citada (cafegame.dev/docs/vectora)
```

#### Test: Vectora vs Outras Ferramentas

```text
Given: Prompt "Como Vectora se compara com Elasticsearch?"
When: Enviado para Gemini
Then: Gemini explica:
  - Vectora é específico para código
  - Usa embeddings ao invés de BM25
  - Melhor para análise semântica
  - Integração nativa com LLMs
  - Cache híbrido e data roaming
```

#### Test: Vectora Founding Principles

```text
Given: Prompt sobre filosofia de Vectora
When: Enviado para Gemini
Then: Gemini cita:
  - "Entendimento semântico profundo"
  - "Cache híbrido inteligente"
  - "Multi-provider LLM support"
  - "Experiência local-first"
```

---

### 2. Capabilities & Features (15 testes)

#### Test: Core Features Awareness

```text
Given: Prompt "Quais são as principais features de Vectora?"
When: Enviado para Gemini
Then: Resposta lista:
  - [x] Context Engine (busca contextual)
  - [x] Hybrid Search (local + cloud)
  - [x] Reranking (Voyage)
  - [x] Dependency Analysis
  - [x] AST Parsing
  - [x] Test Discovery
  - [x] Multi-provider support
```

#### Test: Tools & Queries Knowledge

```text
Given: Prompt sobre tools disponíveis em Vectora
When: Enviado para Gemini
Then: Gemini conhece essas tools:
  - search_context(query, top_k)
  - search_tests(query, top_k)
  - find_similar_code(snippet)
  - analyze_dependencies(symbol)
  - get_file_structure()
  - validate_query(query)
  - list_namespaces()
  - get_metrics()
```

#### Test: API Keys & Configuration

```text
Given: Prompt "Como configurar Vectora?"
When: Enviado para Gemini
Then: Gemini descreve:
  - GOOGLE_API_KEY (Gemini)
  - VOYAGE_API_KEY (embeddings)
  - MONGODB_URI (storage)
  - JWT_SECRET (auth)
  - Arquivo .env
  - config.yaml
```

#### Test: Supported Providers

```text
Given: Prompt sobre providers
When: Enviado para Gemini
Then: Gemini sabe que Vectora suporta:
  - Google Gemini (LLM + embeddings)
  - Anthropic Claude (LLM only)
  - Voyage (embeddings + reranking)
  - OpenAI (potential future)
```

---

### 3. Documentation Knowledge (15 testes)

#### Test: Public Documentation Access

```text
Given: Prompt "Onde está a documentação de Vectora?"
When: Enviado para Gemini
Then: Gemini responde:
  - "cafegame.dev/docs/vectora"
  - "github.com/Kaffyn/Vectora"
  - "Documentação em PT-BR e EN"
And: Links funcionam
And: Conteúdo atualizado
```

#### Test: Documentation Citation

```text
Given: Pergunta sobre funcionalidade Vectora
When: Gemini busca responder
Then: Cita documentação oficial:
  - Incluir source URL
  - Versão da documentação
  - Timestamp da última atualização
Example:
  "Segundo a documentação oficial
  (cafegame.dev/docs/vectora/context-engine, v0.1.0):
  O Context Engine..."
```

#### Test: Setup Guide Knowledge

```text
Given: Prompt "Como instalar Vectora?"
When: Enviado para Gemini
Then: Gemini guia:
  - Clonar repositório
  - Instalar dependências (go mod)
  - Configurar API keys
  - Setup MongoDB
  - Rodar: go build ./cmd/vectora
  - Testar: vectora --version
```

#### Test: CLI Usage Knowledge

```text
Given: Prompt "Como usar CLI de Vectora?"
When: Enviado para Gemini
Then: Gemini demonstra comandos:
  vectora search "query"
  vectora analyze --file code.go
  vectora --help
  vectora config --list
```

---

### 4. Decision Intelligence (15 testes)

#### Test: When to Use Vectora

```text
Given: Pergunta "Como encontrar todas as funções que usam getUserById?"
When: Enviado para Gemini
Then: Gemini:
  - Reconhece como tarefa de código
  - Sugere usar Vectora
  - Explica por quê (análise semântica > grep)
  - Fornece comando:
    vectora search "calls to getUserById"
    OR
    vectora analyze --symbol getUserById
```

#### Test: When NOT to Use Vectora

```text
Given: Pergunta "Como fazer um bolo?"
When: Enviado para Gemini
Then: Gemini:
  - NÃO sugere Vectora
  - Responde a pergunta normalmente
  - Não menciona unnecessariamente Vectora
```

#### Test: Partial Vectora Usage

```text
Given: Pergunta "Explicar padrões de autenticação em Go com exemplos do código"
When: Enviado para Gemini
Then: Gemini pode:
  Option A: "Vou usar Vectora para encontrar exemplos"
  Option B: "Vou explicar com meus conhecimentos"
  Option C: "Vou combinar Vectora + conhecimentos"
All são válidos, desde que fundamentados
```

#### Test: Error Recognition

```text
Given: Query malformada enviada para Vectora
When: Gemini detecta erro
Then: Gemini:
  - Reconhece o erro
  - Corrige a query
  - Retenta com query corrigida
  - Explica ao usuário a correção
```

---

### 5. Integration Scenario Tests (10 testes)

#### Test: Code Review with Vectora

```text
Given: Usuário: "Review este código e sugira melhorias"
       (fornece snippet)
When: Enviado para Gemini
Then: Gemini:
  - Analisa snippet
  - Usa Vectora para encontrar patterns similares
  - Compara com best practices do codebase
  - Fornece sugestões baseadas em Vectora findings
```

#### Test: Bug Investigation

```text
Given: Usuário: "Este erro ocorre em X, qual é a causa provável?"
When: Enviado para Gemini
Then: Gemini:
  - Faz search em Vectora: "X error"
  - Procura por similar bugs históricos
  - Analisa dependências relacionadas
  - Fornece diagnóstico com evidências
```

#### Test: Documentation Generation

```text
Given: Usuário: "Cria documentação para esta função"
When: Enviado para Gemini
Then: Gemini:
  - Busca funções similares em Vectora
  - Examina padrões de documentação
  - Gera docs consistentes
  - Inclui exemplos de código real
```

---

### 6. Knowledge Freshness (5 testes)

#### Test: Documentation Version Awareness

```text
Given: Pergunta sobre feature recente
When: Enviado para Gemini
Then: Gemini:
  - Sabe versão atual (v0.1.0)
  - Conhece changelog
  - Menciona quando feature foi adicionada
  - Avisa sobre breaking changes
```

#### Test: Updated Information

```text
Given: Qualquer pergunta sobre Vectora
When: Enviado para Gemini
Then: Gemini responde com:
  - Informação atual (re-validated contra docs)
  - Sem informações obsoletas
  - Com timestamp de última verificação
```

---

## Critérios de Aceitação

| Critério                                | Alvo                  |
| --------------------------------------- | --------------------- |
| Gemini menciona Vectora apropriadamente | 95% das vezes         |
| Descrição de Vectora precisa            | 100%                  |
| Conhecimento de capabilities            | > 90%                 |
| Citation de documentation               | 100% quando relevante |
| Decision intelligence                   | 90%+ acurácia         |
| Sem hallucination sobre features        | 100%                  |
| Conhecimento de setup/CLI               | 95%                   |

---

## Dependências de API

```env
GOOGLE_API_KEY=xxxx # Para Gemini
VECTORA_DOCS_URL=https://cafegame.dev/docs/vectora
```

---

## Como Executar

```bash
# Prompt testing (manual)
python scripts/test_gemini_awareness.py

# Testes automatizados
go test -v ./tests/gemini-awareness/...

# Teste específico
go test -v -run TestVectoraIdentity ./tests/gemini-awareness/...

# Coleta de respostas para análise manual
python scripts/collect_gemini_responses.py --output results.json
```

---

## Script de Teste Manual

```python
# scripts/test_gemini_awareness.py
import anthropic

client = anthropic.Anthropic()

prompts = [
    "O que é Vectora?",
    "Como posso usar Vectora para encontrar funções?",
    "Qual é a diferença entre Vectora e grep?",
    "Como instalar Vectora?",
    "Como Vectora usa embeddings?",
]

for prompt in prompts:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print(f"\n**Prompt**: {prompt}")
    print(f"**Response**: {response.content[0].text}")
```

---

## Mapa de Implementação

- [ ] Identidade & Descrição (10 testes)
- [ ] Capabilities & Features (15 testes)
- [ ] Documentation Knowledge (15 testes)
- [ ] Decision Intelligence (15 testes)
- [ ] Integration Scenarios (10 testes)
- [ ] Knowledge Freshness (5 testes)

**Total**: 60 testes

---

## External Linking

| Concept                | Resource                                    | Link                                                                                                       |
| ---------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Gemini API**         | Google AI Studio & Gemini API Documentation | [ai.google.dev/docs](https://ai.google.dev/docs)                                                           |
| **Anthropic Claude**   | Claude API Documentation                    | [docs.anthropic.com/](https://docs.anthropic.com/)                                                         |
| **Anthropic Cookbook** | Recipes and patterns for using Claude       | [github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)               |
| **OpenAI**             | OpenAI API Documentation                    | [platform.openai.com/docs/](https://platform.openai.com/docs/)                                             |
| **MongoDB Atlas**      | Atlas Vector Search Documentation           | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **Voyage Embeddings**  | Voyage Embeddings Documentation             | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)                             |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [Licença (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Parte do ecossistema Vectora AI Agent. Construído com [ADK](https://adk.dev/), [Claude](https://claude.ai/) e [Go](https://golang.org/)._

© 2026 Contribuidores do Vectora. Todos os direitos reservados.
