---
title: Performance & Benchmarks Test Suite
slug: performance
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - testing
  - performance
  - benchmarks
  - profiling
---

{{< lang-toggle >}}

Vectora deve atender todos os SLAs de performance com latência, throughput, utilização de recursos e escalabilidade comprovadas através de benchmarks rigorosos. Esta suite valida que Vectora escala para 50+ usuários simultâneos e mantém p95 latency < 500ms. Cobertura: **80+ testes** | **Prioridade**: ALTA

## Query Latency Testing

- Latência p50 < 100ms (12 testes)
- Latência p95 < 500ms (12 testes)
- Latência p99 < 1s (10 testes)
- Warmup vs cold start (8 testes)

**Target**: p95 < 500ms, p99 < 1s

## Embedding Latency

- Embedding single query < 2s (8 testes)
- Batch embeddings < 5s (8 testes)
- Reranking latency < 1s (8 testes)
- Cache hit latency < 50ms (8 testes)

**Target**: Single < 2s, batch < 5s

## Throughput Testing

- Queries/segundo > 100 (10 testes)
- Embeddings/segundo > 50 (8 testes)
- Concurrent users > 50 (10 testes)
- Sustained load testing (8 testes)

**Target**: > 100 queries/sec sustained

## Resource Utilization

- Memory footprint < 500MB (8 testes)
- CPU usage < 50% (8 testes)
- Disk I/O optimized (8 testes)
- Goroutine count stable (8 testes)

**Target**: < 500MB mem, < 50% CPU

## Scalability Testing

- 100 concurrent requests (8 testes)
- 1000 requests/min sustained (8 testes)
- Large result sets (> 1MB) (8 testes)
- Connection pooling efficiency (5 testes)

**Target**: 100+ concurrent, sustained 1000 req/min

---

## Performance SLAs

| Métrica          | Alvo              |
| ---------------- | ----------------- |
| Latência p50     | < 100ms           |
| Latência p95     | < 500ms           |
| Latência p99     | < 1s              |
| Throughput       | > 100 queries/sec |
| Memory           | < 500MB           |
| CPU              | < 50%             |
| Concurrent Users | > 50              |

---

## External Linking

| Conceito                | Recurso     | Link                                                                                                                                                  |
| ----------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Go Profiling**        | Official    | [blog.golang.org/profiling-go-programs](https://blog.golang.org/profiling-go-programs)                                                                |
| **Benchmarking**        | pkg.go.dev  | [pkg.go.dev/testing#B](https://pkg.go.dev/testing#B)                                                                                                  |
| **Performance Testing** | Guide       | [medium.com/performance-testing-go](https://medium.com/go-with-confidence/performance-testing-in-go-dd35dbcc63ae)                                     |
| **Load Testing Tools**  | Artillery   | [artillery.io/](https://artillery.io/)                                                                                                                |
| **Latency Percentiles** | Engineering | [engineering.linkedin.com/latency-percentiles](https://engineering.linkedin.com/blog/2019/02/latency-percentiles-tell-you-more-about-user-experience) |
