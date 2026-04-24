---
title: VS Code Extension Integration Test Suite
slug: vscode-integration-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - concepts
  - config
  - errors
  - extension
  - gemini
  - gemini-cli
  - go
  - integration
  - json
  - mcp
  - metrics
  - persistence
  - protocol
  - reference
  - state
  - testing
  - tutorial
  - typescript
  - ui
  - vectora
  - vscode
---

{{< lang-toggle >}}

VS Code extension deve integrar perfeitamente com Vectora, fornecendo UX intuitiva, respondendo rapidamente e usando Vectora quando apropriado para fornecer code intelligence superior sem interromper o workflow do desenvolvedor. Cobertura: **100+ testes** | **Prioridade**: CRÍTICA

## Principles

---

## Princípios

1. **Seamless Integration**: Não interrompe workflow do user
2. **Instant Feedback**: Resultados em < 500ms
3. **Visual Clarity**: UI clara e intuitiva
4. **Smart Defaults**: Usa Vectora quando apropriado
5. **Offline Support**: Funciona mesmo sem Vectora

---

## Segmentos de Testes

### 1. Extension Activation & Initialization (15 testes)

#### Test: Extension Loads Successfully

```text
Given: VS Code com Vectora extension instalada
When: Extension ativada
Then:
  - Status bar mostra "Vectora: Ready"
  - Commands disponíveis
  - Sidebar icon visível
  - Sem errors no console
```

#### Test: MCP Server Connection

```text
Given: Extension ativada
When: Tenta conectar ao Vectora MCP
Then:
  - Conexão estabelecida em < 2s
  - Server info recebida
  - Status: "Connected"
  - Timeout graceful se falhar
```

#### Test: Command Palette Registration

```text
Given: Extension ativada
When: Command palette aberto
Then: Comandos visíveis:
  - Vectora: Search
  - Vectora: Analyze File
  - Vectora: Find Similar
  - Vectora: Show Metrics
  - Etc.
```

#### Test: Sidebar Panel Initialization

```text
Given: Extension ativada
When: Sidebar aberto
Then:
  - Painel Vectora visível
  - Status section
  - Recent searches
  - Settings button
  - Help button
```

---

### 2. Search Functionality (25 testes)

#### Test: Quick Search from Editor

```text
Given: User tem arquivo aberto
And: Seleciona texto: "getUserById"
When: Click Vectora search
Then:
  - Search panel abre
  - Query pré-populado
  - Results mostram < 300ms
  - Resultados formatados com sintaxe
```

#### Test: Advanced Search Dialog

```text
Given: User clica "Advanced Search"
When: Dialog abre
Then: Opções disponíveis:
  - Query text
  - Filters (file type, complexity)
  - Sort by (relevance, recency)
  - Top K results
  - Submit & Results
```

#### Test: Search Results Navigation

```text
Given: 20 resultados retornados
When: User clica num resultado
Then:
  - Editor abre no arquivo
  - Linha do resultado visível
  - Highlight visual aplicado
  - Context window visível
```

#### Test: Result Breadcrumb

```text
Given: Resultado clicado
When: File aberto
Then: Breadcrumb mostra:
  /path/to/file.ts > Function > Line: 42
```

#### Test: Pagination

```text
Given: 100+ resultados
When: User vê top 10
Then: Opção "Load More" disponível
And: Carrega próximos 10 sem refresh
```

---

### 3. File Analysis (20 testes)

#### Test: Analyze Current File

```text
Given: Arquivo TypeScript aberto
When: "Vectora: Analyze File" executado
Then: Panel mostra:
  - Estrutura do arquivo (funções, classes)
  - Complexidade
  - Funções sem testes
  - Potenciais issues
  - Dependências
```

#### Test: Inline Hover Information

```text
Given: User hover no mouse em function name
When: Espera 500ms
Then: Tooltip mostra:
  - Function signature
  - Documentation
  - Call count
  - Test coverage
```

#### Test: File Metrics

```text
Given: File aberto
When: Metrics panel solicitado
Then: Mostra:
  - Total functions: N
  - Average complexity: X
  - Test coverage: Y%
  - Lines of code: Z
  - Dependencies: W
```

---

### 4. Code Analysis & Suggestions (20 testes)

#### Test: Find Similar Code

```text
Given: User seleciona função
When: "Find Similar" executado
Then:
  - Similar patterns encontrados
  - Mostrados em nova panel
  - Comparação visual
  - Refactoring suggestions
```

#### Test: Dependency Analysis

```text
Given: Function no editor
When: "Analyze Dependencies" executado
Then:
  - Grafo de dependências mostrado
  - Chamadas entrantes/saintes
  - Transitive deps mapeadas
  - Circular refs alertados
```

#### Test: Code Smell Detection

```text
Given: File contém código questionável
When: Analysis executado
Then: Issues destacados:
  - Long functions (> 50 LOC)
  - High complexity (> 5)
  - Duplicated code
  - Missing tests
  - Dead code
```

---

### 5. Diagnostics & Quick Fixes (15 testes)

#### Test: Inline Diagnostics

```text
Given: File com potencial issues
When: Aberto
Then:
  - Squiggly lines no código
  - Hover mostra explanation
  - Quick fix sugestões
  - Luz amarela se aviso
```

#### Test: Quick Fix Suggestions

```text
Given: Issue detectado
When: User clica quick fix
Then: Opções oferecidas:
  - Extract to function
  - Add tests
  - Add documentation
  - Refactor pattern
```

#### Test: Batch Fixes

```text
Given: 5 issues no arquivo
When: "Fix All" selecionado
Then:
  - Todos fixados automaticamente
  - User confirmação antes
  - Undo disponível
```

---

### 6. UI/UX Components (15 testes)

#### Test: Status Bar Updates

```text
Given: Extension operando
When: Various states
Then: Status bar mostra:
  - "Vectora: Ready" (normal)
  - "Vectora: Searching..." (loading)
  - "Vectora: Error" (error)
  - "Vectora: Offline" (disconnected)
```

#### Test: Sidebar Persistence

```text
Given: Sidebar com abas (search, analysis)
When: User muda abas
Then:
  - Estado preservado
  - Scroll position mantido
  - Data cached
  - Performance ótima
```

#### Test: Dark Mode Support

```text
Given: VS Code em dark mode
When: Extension UI renderizado
Then:
  - Colors legíveis
  - Contrast > 4.5:1
  - Icons visíveis
  - No strain in eyes
```

#### Test: Keyboard Shortcuts

```text
Given: Extension ativada
When: Atalhos usados:
  - Ctrl+Shift+V (Search)
  - Ctrl+Shift+A (Analyze)
  - Ctrl+Shift+D (Dependencies)
Then: Comandos executados sem mouse
```

---

### 7. Settings & Configuration (10 testes)

#### Test: Settings UI

```text
Given: Settings panel aberto
When: Vectora settings visível
Then: Opções:
  - Enable/disable extension
  - Vectora server URL
  - Max results
  - Timeout
  - Auto-analyze on save
```

#### Test: Settings Persistence

```text
Given: User customiza settings
When: VS Code reaberto
Then: Todas settings preservadas
And: Aplicadas imediatamente
```

#### Test: Workspace vs User Settings

```text
Given: Projeto com vectora.config.json
When: Extension inicia
Then: Workspace settings override user settings
And: Hierarchia respectada
```

---

### 8. Performance (10 testes)

#### Test: Search Response Time

```text
Given: Search query executado
When: Processado
Then: Results em < 300ms
And: UI não freezes
And: Responsivo durante espera
```

#### Test: Memory Usage

```text
Given: Extension rodando por 1 hora
When: Memory monitorado
Then:
  - Sem memory leaks
  - Uso < 100MB
  - Garbage collection funciona
```

#### Test: Large File Handling

```text
Given: Arquivo de 10000+ linhas
When: Aberto
Then:
  - Análise rápida (< 2s)
  - Syntax highlighting funciona
  - Scroll sem lag
  - Search funciona bem
```

---

## Performance SLAs

| Operation        | Target Latency |
| ---------------- | -------------- |
| Search           | < 300ms        |
| File Analysis    | < 500ms        |
| Find Similar     | < 800ms        |
| Dependency Graph | < 1s           |
| Load More        | < 200ms        |

---

## Critérios de Aceitação

| Critério            | Alvo    |
| ------------------- | ------- |
| Extension load time | < 2s    |
| Search response     | < 300ms |
| UI responsiveness   | 60 FPS  |
| Memory usage        | < 100MB |
| Success rate        | 99%+    |
| Zero crashes        | 100%    |
| User satisfaction   | 95%+    |

---

## Como Executar

```bash
# VS Code Extension Testing Framework
npm install --save-dev @vscode/test-electron

# Rodar testes
npm test

# Roda testes específicos
npm test -- --grep "Search Functionality"

# Integração testing
npm run test:integration

# Performance profiling
npm run test:perf

# UI snapshot testing
npm run test:snapshots
```

---

## Test Data

Usaremos fixtures com:

- Projetos TypeScript reais
- JavaScript com diferentes styles
- Python, Go, outros
- Arquivos de vários tamanhos (1KB - 100MB)

---

## Mapa de Implementação

- [ ] Extension Activation (15 testes)
- [ ] Search Functionality (25 testes)
- [ ] File Analysis (20 testes)
- [ ] Code Analysis & Suggestions (20 testes)
- [ ] Diagnostics & Quick Fixes (15 testes)
- [ ] UI/UX Components (15 testes)
- [ ] Settings & Configuration (10 testes)
- [ ] Performance (10 testes)

**Total**: 100+ testes

---

## Integration with Gemini CLI

Esta suite de testes do VS Code espelha a suite do Gemini CLI:

- Decision intelligence similar
- Performance targets similares
- Error handling patterns iguais
- Messaging consistent

Isso garante que ambas integrações sejam "padrão ouro" em qualidade.

---

## External Linking

| Concept        | Resource                                    | Link                                                                                     |
| -------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification        | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)   |
| **MCP Go SDK** | Go SDK for MCP (anthropics/go-sdk)          | [github.com/anthropics/anthropic-sdk-go](https://github.com/anthropics/anthropic-sdk-go) |
| **Gemini API** | Google AI Studio & Gemini API Documentation | [ai.google.dev/docs](https://ai.google.dev/docs)                                         |
| **TypeScript** | TypeScript: Typed superset of JavaScript    | [www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)                     |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [Licença (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Parte do ecossistema Vectora AI Agent. Construído com [ADK](https://adk.dev/), [Claude](https://claude.ai/) e [Go](https://golang.org/)._

© 2026 Contribuidores do Vectora. Todos os direitos reservados.
