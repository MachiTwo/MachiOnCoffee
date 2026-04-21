---
title: Guidelines
slug: guidelines
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - guidelines
  - mcp
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

Complete guide for contributing to Vectora: setup, code, commits, PRs, and best practices.

## Setup

```bash
git clone https://github.com/kaffyn/vectora
cd vectora
go mod tidy
go build -o vectora ./cmd/vectora
```

## Code Style

- **Golang**: Go 1.22+, follow [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- **Formatting**: `gofmt` or `goimports`
- **Linting**: `golangci-lint` (run `golangci-lint run`)
- **Tests**: `go test`, coverage >80%

## Git Workflow

1. Fork repo
2. Create branch: `git checkout -b feature/your-feature`
3. Commit: conventional commits (`feat:`, `fix:`, `docs:`)
4. Push: `git push origin feature/your-feature`
5. PR with clear description

## PR Requirements

- Tests passing (`go test ./...`)
- Clean linting (`golangci-lint run`)
- No `fmt.Printf` (use internal logger)
- Updated documentation (PT + EN)
- PR description explains the WHY

## Commit Message Format

```text
type(scope): brief description

Longer explanation if needed.

Closes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

## Documentation

- Update CHANGELOG.md
- Add JSDoc/GoDoc for public functions
- Portuguese + English (i18n)

## Testing

```bash
go test ./... # Run all tests
go test -v ./pkg/core # Test specific package
go test -coverprofile=coverage.out ./... # Coverage report
```

## Performance

- Benchmark before/after: `go test -bench=. ./...`
- Vector search must be < 500ms
- Do not add heavy dependencies

## Security

- Use BYOK for APIs
- No hardcoded secrets
- Run `go nancy` or `govulncheck` before the PR

## Questions?

- GitHub Discussions: [github.com/kaffyn/vectora/discussions](https://github.com/kaffyn/vectora/discussions)
- Issues: [github.com/kaffyn/vectora/issues](https://github.com/kaffyn/vectora/issues)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
