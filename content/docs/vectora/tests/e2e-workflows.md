---
title: End-to-End Workflows Test Suite
slug: e2e-workflows
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - testing
  - e2e
  - integration
  - workflows
---

{{< lang-toggle >}}

Workflows completos ponta a ponta devem funcionar corretamente, desde inicialização até resultado final, passando por múltiplos componentes e integrações sem falhas. Esta suite valida cenários reais de usuário através de toda a stack. Cobertura: **100+ testes** | **Prioridade**: ALTA

## Gemini CLI Complete Flow

- Initialize CLI + auth (8 testes)
- Query Vectora through Gemini (10 testes)
- Get multi-turn conversation (8 testes)
- Context persistence (8 testes)
- Error recovery (5 testes)

**SLA**: Complete query response in < 3s

### Gemini CLI Scenario

```text
User: "How do I validate JWT tokens?"
→ CLI initializes with auth
→ Gemini CLI calls Vectora search
→ Vectora returns code examples
→ Gemini formats response
→ User sees answer in < 2s
```

## VS Code Extension Workflow

- Open extension in VS Code (8 testes)
- Select code + search (10 testes)
- View results inline (8 testes)
- Apply suggestions (8 testes)
- Multi-file workflow (8 testes)

**SLA**: Results shown in < 500ms from selection

### VS Code Extension Scenario

```text
User: Selects "getUserById" in editor
→ Right-click "Search with Vectora"
→ Vectora searches for references
→ Results shown in sidebar
→ User sees 10+ usages in < 200ms
```

## MCP Protocol Flow

- Client connects to server (8 testes)
- Lists available tools (5 testes)
- Invokes tool with params (10 testes)
- Receives result correctly (8 testes)
- Handles errors gracefully (8 testes)

**SLA**: Tool invocation response in < 1s

### MCP Protocol Scenario

```text
JSON-RPC client → MCP server
→ tools/list request
→ Server returns tool schemas
→ Client calls search_context
→ Server returns results
→ Complete in < 500ms
```

## Data Persistence Flow

- Create/update embeddings (10 testes)
- Cache locally (8 testes)
- Sync to cloud (8 testes)
- Retrieve from local cache (8 testes)
- Retrieve from cloud (8 testes)

**SLA**: Sync completes in < 5s for 100 docs

### Data Persistence Scenario

```text
User: Makes 5 searches offline
→ Results cached locally
→ Goes online
→ Data syncs to MongoDB
→ Other devices see updates
→ Sync completes in < 2s
```

## Multi-step Complex Queries

- Analyze dependencies (8 testes)
- Find tests for code (8 testes)
- Generate documentation (8 testes)
- Suggest improvements (8 testes)

**SLA**: Complex query result in < 2s

### Complex Query Scenario

```text
User: "Show me all callers of getUserById and their tests"
→ Vectora analyzes dependencies
→ Finds all calling functions
→ Finds tests for those functions
→ Returns structured results
→ Complete in < 1.5s
```

---

## E2E SLAs

| Workflow       | Target               |
| -------------- | -------------------- |
| CLI Query      | < 3s complete        |
| VS Code Search | < 500ms show results |
| MCP Tool Call  | < 1s response        |
| Cache Sync     | < 5s for 100 docs    |
| Complex Query  | < 2s result          |

---

## Testing Approach

### Tools

- Gemini CLI: Integration testing with mocked Vectora
- VS Code: UI testing with Playwright
- MCP: Protocol testing with JSON-RPC compliance
- Database: Transaction testing with MongoDB
- Performance: Load testing with 50+ concurrent users

### Scenarios Covered

- Happy path (all systems working)
- Partial failures (one component down)
- Network issues (intermittent connectivity)
- Authentication failures (expired tokens)
- Rate limiting (quota exceeded)
- Data conflicts (concurrent modifications)

---

## External Linking

| Conceito                  | Recurso                | Link                                                                                                                                 |
| ------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **E2E Testing Guide**     | Testing Best Practices | [angular.io/guide/testing-code-coverage](https://angular.io/guide/testing-code-coverage)                                             |
| **Cypress Documentation** | UI Testing Tool        | [cypress.io/](https://cypress.io/)                                                                                                   |
| **Playwright**            | Browser Automation     | [playwright.dev/](https://playwright.dev/)                                                                                           |
| **Integration Testing**   | Best Practices         | [medium.com/integrationtests](https://medium.com/javascript-testing-utensils/how-to-code-integration-tests-for-node-js-9f0cf1f3fccd) |
| **Test Automation**       | Strategy & Patterns    | [testautomationu.applitools.com](https://testautomationu.applitools.com/test-automation-basics/)                                     |
