---
title: Harness Runtime
slug: harness-runtime
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - auth
  - concepts
  - config
  - embeddings
  - errors
  - guardian
  - harness
  - harness-runtime
  - mcp
  - persistence
  - reranker
  - runtime
  - security
  - tools
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}
Harness Runtime is the **validation and protection** module that runs immediately before and after tool execution. It captures silent failures, verifies security, and measures quality.

> [!IMPORTANT] Harness does not tolerate silent errors. If a tool fails, Harness stops and reports. If a Guardian check fails, execution is blocked.

## The Problem

Generic agents execute tools "blindly":

- Without validating if output is relevant
- Without checking for security violations
- Without measuring latency or quality

Result: confident answers about invalid data, security breaches, and token waste.

## Architecture

Harness Runtime implements three phases of protection: validation before execution, wrapped execution with resilience, and post-execution validation with metrics.

## Pre-Execution

Before running any tool:

1. **Guardian Check**: Validates permissions against the blocklist
2. **Preconditions**: Checks environment variables, API keys, namespaces
3. **Rate Limit**: Verifies request quota per minute
4. **Input Validation**: Sanitizes strings, arrays, and structures

## Tool Execution (Wrapped)

The tool runs with:

- **Timeout**: Maximum of 30s by default (configurable)
- **Retry Logic**: Up to 3 attempts on transient failures
- **Streaming**: Output is buffered in 4KB chunks
- **Circuit Breaker**: Repeated failures trigger fallback

## Post-Execution

After the tool returns:

1. **Output Validation**: Verifies schema, types, size limits
2. **Metrics Capture**: Latency, tokens, errors, security
3. **Comparison Mode**: Compares result vs. baseline (optional)
4. **Persistence**: Saves execution in AGENTS.md or logs

## Metrics & SLA

Harness captures 5 key metrics from each execution and defines limits for automatic degradation when metrics fall below SLAs.

## Core Metrics

```yaml
retrieval_precision: >= 0.65 # Search relevance
tool_accuracy: >= 0.95 # Success rate
security_events: 0 # Zero violations
latency_p95: < 2000ms # 95th percentile in ms
token_efficiency: >= 0.85 # Useful / total
```

## Comparison Mode (--compare)

Use comparison mode to validate performance changes after changing reranker, embeddings, or index:

## Case 1: Test new reranker

```bash
vectora execute search_context \
  --query "How to validate JWT tokens in middleware?" \
  --compare baseline \
  --reranker voyage-rerank-2.5 # New reranker vs previous
```

## Configuration

```yaml
context_engine:
  harness:
    enabled: true
    pre_execution:
      validate_guardian: true
      validate_preconditions: true
      rate_limit_per_minute: 60
    execution:
      timeout_ms: 30000
      retry_attempts: 3
    post_execution:
      validate_output: true
      capture_metrics: true
```

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
