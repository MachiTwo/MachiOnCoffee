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

Guia completo para contribuir com Vectora: setup, código, commits, PRs e melhores práticas.

### Setup

```bash
git clone https://github.com/kaffyn/vectora
cd vectora
npm install
npm run dev
```

### Code Style

- **TypeScript**: strict mode, no `any`
- **Formatting**: Prettier (run `npm run format`)
- **Linting**: ESLint (run `npm run lint`)
- **Tests**: Jest, coverage >80%

### Git Workflow

1. Fork repo
2. Create branch: `git checkout -b feature/your-feature`
3. Commit: conventional commits (`feat:`, `fix:`, `docs:`)
4. Push: `git push origin feature/your-feature`
5. PR com descrição clara

### PR Requirements

- Tests passing
- TypeScript strict
- No console.log
- Updated docs
- PR description explains WHY

### Commit Message Format

```text
type(scope): brief description

Longer explanation if needed.

Closes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

### Documentation

- Update CHANGELOG.md
- Add JSDoc para funções públicas
- Portuguese + English (i18n)

### Testing

```bash
npm run test # Run all tests
npm run test:watch # Watch mode
npm run test:coverage # Coverage report
```

### Performance

- Benchmark antes/depois: `npm run bench`
- Vector search deve ser <500ms
- Não adicione dependências pesadas

### Security

- Use BYOK for APIs
- No hardcoded secrets
- Run `npm audit` antes de PR

### Questions?

- GitHub Discussions: [github.com/kaffyn/vectora/discussions](https://github.com/kaffyn/vectora/discussions)
- Issues: [github.com/kaffyn/vectora/issues](https://github.com/kaffyn/vectora/issues)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
