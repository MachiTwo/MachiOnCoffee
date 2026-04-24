---
title: Harness Runtime
slug: harness-runtime
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - agents
  - ai
  - architecture
  - auth
  - claude
  - concepts
  - config
  - embeddings
  - errors
  - gemini
  - go
  - governance
  - guardian
  - harness
  - harness-runtime
  - jwt
  - mcp
  - metrics
  - mongodb
  - otel
  - persistence
  - protocol
  - reranker
  - runtime
  - security
  - state
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

Harness Runtime is the **distributed nervous system** that orchestrates observation, auto-correction and governance across all Vectora layers. It is NOT a validation module, but the intelligence that enables Gemini to watch its own tool execution and adjust reasoning in real-time.

> [!WARNING] CRITICAL REDEFINITION: Harness Runtime is NOT a folder `/harness` in code, NOT a protocol, NOT a single module. It is an ARCHITECTURAL PATTERN that permeates system prompts, tool schemas, state management, and configuration. It emerges from the INTERACTION of observation hooks, immutable state threads, recovery strategies, and distributed governance.

## What Harness Really Is

Harness has **evolved** from a validation module to a distributed system pattern:

```yaml
old_view:
  harness: "Safety wrapper that validates before/after tool execution"

new_view:
  harness: "Distributed nervous system that enables real-time observation, self-correction and governance"
  harness_reality: "Not implemented as code, but as a PATTERN across 5 distributed layers"

transformation: "From (guardian_check → run_tool → validate_output) to (context_pipeline → streaming_execution → recovery_ladder → termination_conditions → state_threading)"
```

## The 5 Distributed Layers of Harness

Harness emerges from the orchestration of 5 distributed layers:

### 1. Context Pipeline (Preparation)

**What it does**: Prepares the environment and context before execution

- Validates permissions via Guardian blocklist
- Checks preconditions (API keys, namespaces)
- Injects metrics baseline into system prompt
- Loads recovery strategies from YAML config

**Code Pattern**:

```yaml
harness:
  layer_1_context_pipeline:
    pre_execution_checks:
      - validate_guardian
      - check_preconditions
      - load_baseline_metrics
      - inject_recovery_ladder
    timeout_ms: 500
```

### 2. Streaming Execution (Observation)

**What it does**: Runs tool with observation hooks at every step

- Captures output in 4KB chunks with metadata
- Watches latency, token count, error patterns
- Injects metrics DURING execution (not after)
- Enables Gemini to "see" what's happening

**Code Pattern**:

```yaml
harness:
  layer_2_streaming_execution:
    observation_points:
      search_context: ["query_received", "embedding_generated", "vector_search_completed", "reranking_started"]
      bash_terminal: ["command_sent", "output_chunk_received", "exit_code_captured"]
      voyage_rerank: ["chunk_n_processed", "confidence_scores_updated"]
    metrics_injection_frequency_ms: 100
```

### 3. Recovery Ladder (Resilience)

**What it does**: Ordered strategies to recover from failures, each with a cost

- Attempt 1: Retry immediately (cost: latency)
- Attempt 2: Refine query and retry (cost: reranking latency)
- Attempt 3: Use local reranker (cost: lower precision)
- Attempt 4: Fallback to basic search (cost: speed, not quality)
- Attempt 5: Return null with explanation (cost: no response)

**Code Pattern**:

```yaml
harness:
  layer_3_recovery_ladder:
    strategies:
      - name: "retry_immediate"
        max_attempts: 1
        cost: "latency:10ms"
        enabled: true
      - name: "refine_and_retry"
        max_attempts: 1
        cost: "latency:200ms"
        enabled: true
      - name: "local_reranker"
        max_attempts: 1
        cost: "precision:-0.15"
        enabled: true
      - name: "basic_search"
        max_attempts: 1
        cost: "latency:50ms"
        enabled: true
      - name: "graceful_degradation"
        returns_null: true
        enabled: true
```

### 4. Termination Conditions (Control)

**What it does**: Decides WHEN to stop trying and move on

- Success: precision >= 0.65 OR confidence >= 0.80
- Timeout: execution time >= 2000ms
- Resource exhausted: recovery attempts > 5
- User preference: --fast flag forces immediate return

**Code Pattern**:

```yaml
harness:
  layer_4_termination_conditions:
    success_criteria:
      - precision >= 0.65
      - confidence >= 0.80
    timeout_ms: 2000
    max_recovery_attempts: 5
    user_preferences:
      --fast: "return after attempt 1"
      --thorough: "run all recovery attempts"
      --safe: "require precision >= 0.75"
```

### 5. State Threading (Persistence)

**What it does**: Maintains immutable typed state across the entire execution

- AgentState: `{iteration, precision, confidence, recovery_used, audit_trail}`
- Audit trail: every decision logged with timestamp, metrics, reason
- Enables Gemini to "remember" what happened and why
- Enables humans to understand the full reasoning chain

**Code Pattern**:

```yaml
harness:
  layer_5_state_threading:
    state_type:
      iteration: int
      precision: float
      confidence: float
      recovery_ladder_step: string
      metrics_snapshot:
        latency_ms: int
        tokens_used: int
        safety_events: int
      audit_trail: [event]
    immutable: true
    persistence: mongodb
```

## Tool Observation

Harness injects observation points into EACH TOOL where Gemini can "watch" execution and adjust reasoning in real-time.

### Per-Tool Observation Points

```yaml
search_context:
  observation_points:
    - "vector_search_completed: top_k_results_received"
    - "reranking_completed: precision_calculated"
    - "precision_threshold_check: if precision < 0.65 then suggest_retry"

voyage_rerank:
  observation_points:
    - "chunk_0_processed: confidence_score_assigned"
    - "chunk_n_processed: running_confidence_average_calculated"
    - "reranking_complete: final_precision_known"

bash_terminal:
  observation_points:
    - "command_sent: shell_type_identified"
    - "output_chunk_received: error_pattern_detected"
    - "exit_code_captured: success_or_failure_known"
```

### Example: Gemini Watches search_context

```text
1. Gemini calls search_context("validate JWT tokens")
2. At "reranking_completed": Gemini receives {precision: 0.72, top_5: [...]}
3. Gemini evaluates: "0.72 >= 0.65 Good enough, proceed with response"
4. But if precision was 0.58: "0.58 < 0.65 Refine and retry with different query"
5. Gemini uses recovery ladder: attempts query refinement before giving up
```

## Metrics & SLAs

Harness captures metrics at EVERY observation point and defines SLA thresholds for automatic behavior adjustment.

### Core Metrics & Thresholds

```yaml
metrics:
  retrieval_precision:
    description: "Quality of retrieved chunks (0-1)"
    target: ">= 0.65"
    action_if_below: "trigger recovery ladder"

  tool_accuracy:
    description: "Success rate of tool execution (0-1)"
    target: ">= 0.95"
    action_if_below: "increase retry attempts"

  confidence_score:
    description: "Gemini's confidence in answer (0-1)"
    target: ">= 0.80"
    action_if_below: "add disclaimer to response"

  latency_p95:
    description: "95th percentile execution time"
    target: "< 2000ms"
    action_if_above: "use local reranker or fallback"

  token_efficiency:
    description: "Useful tokens / total tokens (0-1)"
    target: ">= 0.85"
    action_if_below: "refine prompt or truncate context"
```

### Execution Example

```text
Query: "How is JWT validation done in Go?"
├─ Context Pipeline:
│ ├─ Guardian: User has access
│ ├─ Preconditions: API keys loaded
│ └─ Baseline: {precision_target: 0.65, confidence_target: 0.80}
│
├─ Streaming Execution:
│ ├─ Embedding generated: latency=45ms
│ ├─ Vector search completed: results=1200, latency=120ms
│ ├─ Reranking started: top_100 input
│ └─ Reranking completed:
│ ├─ precision=0.72 (target 0.65)
│ ├─ confidence=0.87 (target 0.80)
│ ├─ latency_p95=165ms (target 2000ms)
│
├─ Termination Conditions:
│ ├─ Success criteria met: precision >= 0.65
│ └─ Decision: RETURN top_5 to Gemini
│
└─ State Threading:
   ├─ Iteration: 1
   ├─ Precision: 0.72
   ├─ Recovery used: none
   └─ Audit trail: [{timestamp, step, metrics}]
```

## Configuring Harness

Harness configuration is distributed across system prompt, tool schemas, and YAML config:

```yaml
harness:
  enabled: true

  # Layer 1: Context Pipeline
  context_pipeline:
    guardian_validation: true
    precondition_checks: true
    baseline_metrics_injection: true

  # Layer 2: Streaming Execution
  streaming_execution:
    observation_enabled: true
    metrics_injection_frequency_ms: 100
    output_chunk_size_bytes: 4096

  # Layer 3: Recovery Ladder
  recovery_ladder:
    strategies:
      - retry_immediate: { max_attempts: 1 }
      - refine_and_retry: { max_attempts: 1 }
      - local_reranker: { max_attempts: 1 }
      - basic_search: { max_attempts: 1 }
      - graceful_degradation: { enabled: true }

  # Layer 4: Termination Conditions
  termination_conditions:
    success_thresholds:
      precision: 0.65
      confidence: 0.80
    timeouts:
      max_execution_ms: 2000
      max_recovery_attempts: 5

  # Layer 5: State Threading
  state_threading:
    immutable_state: true
    audit_trail_enabled: true
    persistence_backend: mongodb
```

## Testing Harness

Test that observation, auto-correction and governance work together:

```gherkin
Scenario: Harness auto-corrects low precision
  Given Gemini asks for "JWT validation patterns"
  When search_context returns precision=0.58
  Then Harness triggers recovery_ladder
  And Gemini refines query with "JWT authentication middleware"
  And search_context returns precision=0.74
  Then Gemini proceeds with high-confidence response

Scenario: Harness respects termination conditions
  Given recovery_ladder attempts = 5
  When precision still < 0.65
  Then Harness stops recovery
  And returns graceful_degradation response

Scenario: Harness maintains state threading
  Given execution iteration = 3
  When Gemini retrieves AgentState
  Then state includes {iteration, precision, recovery_used, audit_trail}
  And audit_trail has 15 entries (5 per iteration)
  And state is immutable
```

## File Structure (Harness is a Pattern, Not a Folder)

Harness is NOT a folder named `/harness`. It is a PATTERN distributed across:

```text
Vectora/
├─ internal/
│ ├─ llm/
│ │ └─ gemini.go ← System prompt with observation hooks
│ ├─ storage/
│ │ └─ state.go ← AgentState immutable threading
│ ├─ tools/
│ │ ├─ search_context.go ← Observation points in each tool
│ │ └─ analyze_deps.go
│ └─ server/
│ └─ handler.go ← Recovery ladder logic
│
├─ config/
│ ├─ harness.yaml ← Recovery strategies, metrics, thresholds
│ └─ guardian.yaml ← Permission blocklist
│
└─ docs/
   └─ concepts/
      └─ harness-runtime.md ← This file
```

**Key insight**: Harness "lives" in the INTERACTION between these components, not in a single folder.

## FAQ

<details>
<summary>Is Harness Runtime a module I import in my code?</summary>

No. Harness is a PATTERN, not a library. You DON'T `import harness`. Instead, you:

1. Inject observation hooks into your tool implementations
2. Define recovery strategies in YAML config
3. Thread immutable state through your agent execution
4. Let Gemini's system prompt enable "watching" behavior

Harness emerges from the interaction of these patterns, not from a single codebase component.

</details>

<details>
<summary>Why is Harness called a "nervous system"?</summary>

Like a nervous system, Harness:

- **Observes**: Watches every tool execution via observation points
- **Communicates**: Sends metrics to Gemini in real-time
- **Responds**: Triggers recovery strategies when metrics fall below SLAs
- **Learns**: Updates state and audit trail for continuous improvement
- **Protects**: Guardian checks prevent dangerous operations before execution

It's distributed, reactive, and permeates every layer of Vectora.

</details>

<details>
<summary>Can I disable Harness?</summary>

Yes, by setting `harness.enabled: false` in config. But this is NOT recommended for production because:

- Gemini can't "watch" tool execution
- No auto-correction on precision < 0.65
- Recovery ladder disabled
- State threading disabled
- Audit trail lost

For development/testing only.

</details>

---

> Questions about Harness? [GitHub Discussions](https://github.com/Kaffyn/Vectora/discussions) · [Consult the system prompt](../architecture/gemini-system-prompt.md)

## External Linking

| Concept                | Resource                                        | Link                                                                                                       |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Gemini API**         | Google AI Studio & Gemini API Documentation     | [ai.google.dev/docs](https://ai.google.dev/docs)                                                           |
| **JWT**                | RFC 7519: JSON Web Token Standard               | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)                     |
| **Anthropic Claude**   | Claude API Documentation                        | [docs.anthropic.com/](https://docs.anthropic.com/)                                                         |
| **Anthropic Cookbook** | Recipes and patterns for using Claude           | [github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)               |
| **MongoDB Atlas**      | Atlas Vector Search Documentation               | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **OpenTelemetry**      | Observability framework for distributed systems | [opentelemetry.io/docs/](https://opentelemetry.io/docs/)                                                   |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [License (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Part of the Vectora AI Agent ecosystem. Built with [ADK](https://adk.dev/), [Claude](https://claude.ai/), and [Go](https://golang.org/)._

© 2026 Vectora Contributors. All rights reserved.
