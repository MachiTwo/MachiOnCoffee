---
title: Guidelines
slug: guidelines
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - byok
  - concepts
  - guidelines
  - mcp
  - protocol
  - security
  - vector-search
  - vectora
---

{{< lang-toggle >}}

Guia completo para contribuir com Vectora: setup, código, commits, PRs e melhores práticas.

## Setup

```bash
git clone https://github.com/kaffyn/vectora
cd vectora
go mod tidy
go build -o vectora ./cmd/vectora
```

## Code Style

- **Golang**: Go 1.22+, seguir [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- **Formatting**: `gofmt` ou `goimports`
- **Linting**: `golangci-lint` (rodar `golangci-lint run`)
- **Tests**: `go test`, cobertura >80%

## Git Workflow

1. Fork repo
2. Create branch: `git checkout -b feature/your-feature`
3. Commit: conventional commits (`feat:`, `fix:`, `docs:`)
4. Push: `git push origin feature/your-feature`
5. PR com descrição clara

## PR Requirements

- Testes passando (`go test ./...`)
- Linting limpo (`golangci-lint run`)
- Sem `fmt.Printf` (usar logger interno)
- Documentação atualizada (PT + EN)
- Descrição do PR explica o PORQUÊ

## Commit Message Format

```text
type(scope): brief description

Longer explanation if needed.

Closes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

## Documentation

- Update CHANGELOG.md
- Add JSDoc para funções públicas
- Portuguese + English (i18n)

## Testing

```bash
go test ./... # Rodar todos os testes
go test -v ./pkg/core # Testar pacote específico
go test -coverprofile=coverage.out ./... # Relatório de cobertura
```

## Performance

- Benchmark antes/depois: `go test -bench=. ./...`
- Vector search deve ser <500ms
- Não adicione dependências pesadas

## Security

- Use BYOK para APIs
- Sem segredos hardcoded
- Rodar `go nancy` ou `govulncheck` antes do PR

## Questions?

- GitHub Discussions: [github.com/kaffyn/vectora/discussions](https://github.com/kaffyn/vectora/discussions)
- Issues: [github.com/kaffyn/vectora/issues](https://github.com/kaffyn/vectora/issues)

---

## External Linking

| Concept        | Resource                             | Link                                                                                   |
| -------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
