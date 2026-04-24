---
title: Gemini CLI Integration Test Suite
slug: gemini-cli-integration-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - caching
  - cli
  - compliance
  - concepts
  - errors
  - gemini
  - gemini-cli
  - go
  - integration
  - json
  - jwt
  - mcp
  - metrics
  - protocol
  - state
  - testing
  - tools
  - typescript
  - vectora
---

{{< lang-toggle >}}

Gemini CLI deve integrar perfeitamente com Vectora via MCP, reconhecendo quando usar Vectora e quando não usar, fazendo chamadas corretas e recebendo resultados de forma confiável. Esta suite valida a inteligência de decisão, transparência e graceful degradation. Cobertura: **100+ testes** | **Prioridade**: CRÍTICA

## Principles

---

## Princípios

1. **Inteligência de Decisão**: CLI sabe quando chamar Vectora
2. **Transparência**: Usuário vê exatamente o que está acontecendo
3. **Graceful Degradation**: Se Vectora falhar, CLI continua funcionando
4. **Performance**: Resposta final em < 2 segundos para maioria das queries

---

## Segmentos de Testes

### 1. CLI Initialization & Setup (15 testes)

#### Test: CLI Starts with Vectora Available

```text
Given: gemini-cli com Vectora instalado e disponível
When: CLI iniciada
Then:
  - Detecta Vectora no PATH
  - Conecta via MCP (STDIO)
  - Estado: "ready"
  - Timeout de conexão < 5s
```

#### Test: CLI Handles Vectora Unavailable

```text
Given: Vectora não está disponível
When: CLI iniciada
Then:
  - Continua funcionando
  - Avisa user: "Vectora não está disponível"
  - Oferece usar funcionalidades base
  - Comportamento graceful degradation
```

#### Test: MCP Connection Establishment

```text
Given: CLI pronta para conectar
When: MCP handshake iniciado
Then:
  - Initialize request enviado
  - Server info recebido
  - Tools listadas
  - Conectado em < 2s
```

#### Test: Tool Discovery

```text
Given: MCP conectado
When: CLI descobre tools
Then: Lista inclui:
  - search_context
  - search_tests
  - find_similar_code
  - analyze_dependencies
  - get_file_structure
  - Todas com schemas corretos
```

---

### 2. Decision Intelligence (20 testes)

#### Test: Code-Related Query → Use Vectora

```text
Given: User pergunta: "Como encontrar todas as chamadas para getUserById?"
When: CLI processa query
Then:
  - Reconhece como code-related
  - Chama Vectora com query apropriada
  - Mapeia para tool: analyze_dependencies
  - Executa: vectora.analyze_dependencies({symbol: "getUserById"})
  - Retorna results em < 1s
```

#### Test: Non-Code Query → Don't Use Vectora

```text
Given: User pergunta: "Como fazer um bolo de chocolate?"
When: CLI processa query
Then:
  - Reconhece como não code-related
  - NÃO chama Vectora
  - Responde diretamente com conhecimento Gemini
  - Sem menção desnecessária a Vectora
```

#### Test: Ambiguous Query → Offer Vectora Option

```text
Given: User pergunta: "Qual é a melhor forma de autenticar?"
When: CLI processa query
Then: Oferece opções:
  Option A: "Quer buscar exemplos no seu codebase?" (com Vectora)
  Option B: "Ou explicar padrões genéricos?" (sem Vectora)
```

#### Test: Context-Aware Decisions

```text
Given: Conversation com histórico
And: User: "Qual é o bug aqui?" (referenciando código anterior)
When: CLI processa
Then:
  - Entende contexto da conversa
  - Usa Vectora para procurar código similar
  - Conecta findings ao contexto anterior
```

#### Test: Search Concept Decision

```text
Given: Query: "Como fazer error handling em Go?"
When: CLI processa
Then:
  - Pode ir para Vectora (buscar no codebase)
  - Pode responder diretamente (padrão genérico)
  - Ou combinar (responda padrão + exemplos do codebase)
  - Todos os caminhos são válidos
```

---

### 3. Tool Invocation (25 testes)

#### Test: Search Context Tool

```text
Given: Query mapeada para search_context
When: Tool invocado com:
  {query: "authentication handler", top_k: 5}
Then:
  - Vectora processa
  - Resultados retornados
  - CLI formata como resposta natural
  - Usuário vê: "Found 3 authentication handlers in your code..."
```

#### Test: Analyze Dependencies Tool

```text
Given: Query mapeada para analyze_dependencies
When: Tool invocado com:
  {symbol: "processPayment"}
Then:
  - Dependências mapeadas
  - Grafo de chamadas retornado
  - CLI visualiza como texto/diagrama
  - Risco de circular dependencies alertado
```

#### Test: Tool Error Handling

```text
Given: Tool invocado com dados inválidos
When: Error retornado de Vectora
Then:
  - CLI recebe erro
  - Mostra mensagem clara ao user
  - Sugere como refinar query
  - Continua conversa sem crash
```

#### Test: Large Result Handling

```text
Given: Tool retorna 1000+ resultados
When: Processado
Then:
  - Pagina resultados
  - User vê top 10 por padrão
  - Opção para ver mais
  - Performance não degrada
```

#### Test: Timeout Handling

```text
Given: Tool demora > 10s
When: Processado
Then:
  - Timeout acionado após 10s
  - User avisado: "Query está demorando"
  - Oferta para cancelar
  - Se cancelado, sem crash
```

---

### 4. Conversation Continuity (15 testes)

#### Test: Context Carries Over

```text
Given: User: "Qual é a função getCachedUser?"
And: CLI busca com Vectora
And: Retorna: "In auth/cache.ts, linha 42"
When: User: "Qual é o bug nela?"
Then:
  - Contexto da conversa mantido
  - CLI sabe qual função é "nela"
  - Proxima busca em Vectora é para essa função
```

#### Test: Multi-Step Investigation

```text
Given: 5-step investigation usando Vectora
When: Cada passo completado
Then:
  - Contexto preservado entre steps
  - Findings acumulam
  - Diagrama mental construído
  - Final summary conecta todos steps
```

#### Test: User Refinement

```text
Given: Primeira query retorna muitos resultados
When: User: "Mais específico, apenas TypeScript"
Then:
  - Novo parâmetro aplicado
  - Mesma estrutura de conversa mantida
  - Resultados refinados
```

---

### 5. Response Formatting (15 testes)

#### Test: Natural Language Formatting

```text
Given: Tool retorna dados estruturados:
  [{file: "auth/jwt.ts", line: 42, score: 0.95}]
When: Formatado para user
Then: Exibido como:
  "Found JWT validation in auth/jwt.ts (line 42, match: 95%)"
  Não como: "{file: ..., line: ...}"
```

#### Test: Code Highlighting

```text
Given: Tool retorna código snippet
When: Formatado
Then:
  - Sintaxe highlightada
  - Line numbers mostrados
  - Contexto visível
  - Fácil de ler no terminal
```

#### Test: Summary vs Details

```text
Given: 50 resultados de search
When: User solicitou resumo
Then: Mostrado sumário (5 top results)
And: User pode pedir detalhes
When: Usuário pede detalhes
Then: Todos 50 mostrados com paginação
```

---

### 6. Error & Edge Cases (10 testes)

#### Test: Network Failure Recovery

```text
Given: Network goes down during tool invocation
When: Vectora desconecta
Then:
  - Reconhece desconexão
  - User avisado
  - Oferece retry ou offline alternatives
  - Reconnect automático quando online
```

#### Test: Invalid Query Formatting

```text
Given: User query é malformado
When: CLI processa
Then:
  - Detecta problema
  - Sugere correção
  - Oferece exemplo de boa query
  - Oferece retry
```

#### Test: Empty Codebase Handling

```text
Given: Codebase vazio ou muito pequeno
When: Search executado
Then:
  - Não crash
  - Mensagem clara: "No matching code found"
  - Sugestão para adicionar código
```

---

### 7. Transparency & Debugging (10 testes)

#### Test: Show Tool Usage

```text
Given: User query que usa Vectora
When: Query processada
Then: CLI mostra:
  "Using Vectora tool: search_context"
  "Query: 'authentication handler'"
  "Results: 3 found (score > 0.7)"
```

#### Test: Verbose Mode

```text
Given: CLI em verbose mode
When: Tool invocado
Then: Mostra:
  - Exact query enviado
  - Response recebido (JSON)
  - Parsing steps
  - Final formatting
```

#### Test: Performance Metrics

```text
Given: Tool executado
When: Completo
Then: Exibido:
  "Query took 250ms (cache hit)"
  "Network: 120ms, Processing: 130ms"
```

---

### 8. Hybrid Mode Tests (10 testes)

#### Test: Combination Response

```text
Given: Query que beneficia de ambas respostas
When: CLI processa:
  1. Busca em Vectora (exemplos reais)
  2. Responde com conhecimento Gemini (padrões)
Then: Response combina ambas:
  "Here are the patterns, and in your code specifically..."
```

#### Test: Confidence-Based Decision

```text
Given: Query onde Vectora pode ajudar
When: Score de relevância é baixo (< 0.6)
Then:
  - Usa resposta Gemini como primária
  - Vectora como supplementary
  - User vê diferença na apresentação
```

---

## Performance SLAs

| Scenario                | Target Latency |
| ----------------------- | -------------- |
| Simple search (Vectora) | < 500ms        |
| Complex analysis        | < 2s           |
| User response time      | < 3s           |
| Error handling          | < 1s           |
| Formatting output       | < 500ms        |

---

## Critérios de Aceitação

| Critério                       | Alvo |
| ------------------------------ | ---- |
| Decision intelligence accuracy | 90%+ |
| Tool invocation success rate   | 99%+ |
| Response formatting quality    | 95%+ |
| Error recovery                 | 100% |
| Latency compliance             | 99%+ |
| Zero crashes                   | 100% |
| User satisfaction              | 90%+ |

---

## Como Executar

```bash
# Todos os testes
go test -v ./tests/gemini-cli/...

# Suite específica
go test -v -run TestDecisionIntelligence ./tests/gemini-cli/...

# Com conversation replay
python scripts/test_conversation_flows.py

# Load test (100 concurrent conversations)
go test -v -timeout 10m ./tests/gemini-cli/load_test.go

# Manual testing
gemini-cli --verbose # Mostra detail
```

---

## Test Data

Usaremos fixture de código real de:

- Open source projects (Go, TypeScript, Python)
- Real Vectora codebase
- Community contributed examples

---

## Mapa de Implementação

- [ ] CLI Initialization (15 testes)
- [ ] Decision Intelligence (20 testes)
- [ ] Tool Invocation (25 testes)
- [ ] Conversation Continuity (15 testes)
- [ ] Response Formatting (15 testes)
- [ ] Error & Edge Cases (10 testes)
- [ ] Transparency & Debugging (10 testes)
- [ ] Hybrid Mode (10 testes)

**Total**: 100+ testes

---

## External Linking

| Concept        | Resource                                    | Link                                                                                     |
| -------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Gemini API** | Google AI Studio & Gemini API Documentation | [ai.google.dev/docs](https://ai.google.dev/docs)                                         |
| **MCP**        | Model Context Protocol Specification        | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)   |
| **MCP Go SDK** | Go SDK for MCP (anthropics/go-sdk)          | [github.com/anthropics/anthropic-sdk-go](https://github.com/anthropics/anthropic-sdk-go) |
| **JWT**        | RFC 7519: JSON Web Token Standard           | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)   |
| **TypeScript** | TypeScript: Typed superset of JavaScript    | [www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)                     |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [Licença (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Parte do ecossistema Vectora AI Agent. Construído com [ADK](https://adk.dev/), [Claude](https://claude.ai/) e [Go](https://golang.org/)._

© 2026 Contribuidores do Vectora. Todos os direitos reservados.
