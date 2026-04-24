---
title: Regression Testing Suite
slug: regression-testing
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - testing
  - regression
  - continuous
---

{{< lang-toggle >}}

Bugs que foram corrigidos não devem reaparecer, e edge cases conhecidos devem continuar funcionando. Esta suite é contínua, executada com cada commit, validando que fixes permanecem e novas mudanças não reintroduzem problemas antigos. Cobertura: **Contínuo** | **Prioridade**: CRÍTICA

## Previously Fixed Bugs

Cada bug reportado em issues que foi fechado deve ter um teste que:

1. **Reproduz o bug original** (antes da fix)
2. **Valida que a fix funciona** (depois da fix)
3. **Continua testando** em regressões futuras

### Example Structure

```text
Issue #42: "Search returns empty for special characters"

Test: TestSpecialCharacterSearch_Issue42
├─ Setup: Query with "C++", "C#", ".NET"
├─ Call: search_context("C++")
├─ Assert: Results returned (não vazio)
└─ Rerun: Com cada commit
```

## Common Integration Issues

- Cache invalidation race conditions (5 testes)
- MongoDB connection pool exhaustion (5 testes)
- JWT token expiration during long queries (3 testes)
- Concurrent write conflicts (5 testes)
- Memory leaks in goroutines (5 testes)
- Rate limiter false positives (3 testes)
- Unicode handling edge cases (3 testes)

## Known Edge Cases

- Empty query handling (3 testes)
- Very large payloads (> 100MB) (2 testes)
- Deeply nested code structures (3 testes)
- Circular dependencies (2 testes)
- Deleted files still in index (2 testes)
- Concurrent namespace modifications (3 testes)
- Network timeout recovery (3 testes)

## Deprecated Features

- Old API endpoints (2 testes)
- Legacy configuration formats (2 testes)
- Deprecated CLI flags (2 testes)
- Old embedding dimensions (1 teste)

**Expectativa**: Deprecated features still work (with warnings)

## Version Compatibility

- Forward compatibility checks (5 testes)
- Backward compatibility checks (5 testes)
- Migration path verification (3 testes)
- Data format upgrades (3 testes)

## Performance Regression Detection

- Query latency p95 < 500ms (ongoing)
- Memory usage stable (ongoing)
- No new goroutine leaks (ongoing)
- Cache hit rates maintained (ongoing)
- Throughput > 100 q/s (ongoing)

---

## Regression Test Organization

```text
tests/regression/
├── fixed_issues/
│ ├── issue_42_special_chars.go
│ ├── issue_51_cache_race.go
│ └── issue_73_jwt_timeout.go
├── edge_cases/
│ ├── empty_queries.go
│ ├── large_payloads.go
│ └── circular_deps.go
├── performance/
│ ├── latency_benchmarks.go
│ ├── memory_stability.go
│ └── throughput_benchmarks.go
└── integration/
    ├── concurrent_writes.go
    ├── connection_pooling.go
    └── error_recovery.go
```

---

## CI/CD Integration

### Pre-commit Hook

```bash
# Run regression suite before allowing commit
pre-commit run regression-tests --all-files
```

### Every Commit

```bash
# Regression tests must pass
go test -race ./tests/regression/... -timeout 10m
```

### Weekly Regression Stress Test

```bash
# Extended regression testing with load
go test -race ./tests/regression/... -timeout 1h -stress
```

---

## Bug Lifecycle

```text
Bug Reported (Issue)
    ↓
Test Created (reproduce bug)
    ↓
Fix Implemented
    ↓
Test Passes (verify fix)
    ↓
Issue Closed
    ↓
Test Added to Regression Suite
    ↓
Test Runs on Every Commit (prevent re-opening)
```

---

## Regression Test Criteria

| Critério               | Alvo           |
| ---------------------- | -------------- |
| Coverage of fixed bugs | 100%           |
| Edge cases covered     | > 90%          |
| Performance baseline   | Maintained     |
| Pass rate              | 100%           |
| Execution time         | < 5 min        |
| Stability              | No flaky tests |

---

## Issue Template for Regression

When closing an issue, ensure:

```markdown
## Regression Test Added

- [ ] Test reproduces original bug
- [ ] Test validates fix
- [ ] Test added to regression suite
- [ ] Test passes locally
- [ ] Test passes in CI
- [ ] No performance impact

**Test File**: `tests/regression/fixed_issues/issue_XXX_description.go`
```

---

## External Linking

| Conceito                   | Recurso        | Link                                                                                                            |
| -------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------- |
| **Regression Testing**     | Wikipedia      | [en.wikipedia.org/wiki/Regression_testing](https://en.wikipedia.org/wiki/Regression_testing)                    |
| **Continuous Integration** | CI/CD          | [martinfowler.com/articles/continuousIntegration](https://martinfowler.com/articles/continuousIntegration.html) |
| **Testing Best Practices** | Google         | [developers.google.com/tech-writing/testing](https://developers.google.com/tech-writing)                        |
| **Bug Tracking**           | Best Practices | [smartbear.com/blog/test-automation-best-practices](https://smartbear.com/blog/test-automation-best-practices/) |
| **Pre-commit Hooks**       | Git            | [pre-commit.com/](https://pre-commit.com/)                                                                      |
