---
title: Error Codes Reference
slug: errors
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - errors
  - reference
  - troubleshooting
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}
Complete error code reference: HTTP codes, messages, root causes, and solutions.

## 400 - Bad Request

Your request is malformed or has invalid parameters.

| Error                    | Cause                                     | Solution                                                         |
| ------------------------ | ----------------------------------------- | ---------------------------------------------------------------- |
| `INVALID_QUERY`          | Query too short (<3 chars) or long (>10K) | Reformulate: "How to validate tokens?" (5-100 chars recommended) |
| `INVALID_NAMESPACE`      | Namespace does not exist                  | Create with `vectora namespace create your-ns`                   |
| `INVALID_PARAMS`         | top_k is not a number, invalid filter     | Check types: `{"top_k": 10, "namespace": "proj"}`                |
| `MISSING_REQUIRED_FIELD` | Missing required fields                   | Query and namespace are required                                 |

**Debug**: Use `vectora search --debug` to see the exact payload.

## 401 - Unauthorized

Authentication or permission failure.

| Error                 | Cause                              | Solution                                                |
| --------------------- | ---------------------------------- | ------------------------------------------------------- |
| `INVALID_TOKEN`       | Expired or invalid token           | Generate new: `vectora auth token create`               |
| `MISSING_CREDENTIALS` | API key not configured             | `vectora config set GEMINI_API_KEY "your-key"`          |
| `PERMISSION_DENIED`   | Your role does not have permission | Contact admin for upgrade (Owner/Admin can change RBAC) |
| `SESSION_EXPIRED`     | Session > 7 days                   | Reauthenticate: `vectora auth login`                    |

**Debug**: `vectora auth status` shows current token and expiration.

## 404 - Not Found

Resource does not exist.

| Error                 | Cause                           | Solution                           |
| --------------------- | ------------------------------- | ---------------------------------- |
| `NAMESPACE_NOT_FOUND` | Namespace deleted or not shared | List with `vectora namespace list` |
| `FILE_NOT_FOUND`      | File is not indexed             | Reindex: `vectora index --force`   |
| `CHUNK_NOT_FOUND`     | Chunk was deleted               | No solution, chunk was removed     |

## 429 - Rate Limited

You exceeded rate limit or API quotas.

| Error                 | Limit                        | Solution                                             |
| --------------------- | ---------------------------- | ---------------------------------------------------- |
| `RATE_LIMIT_EXCEEDED` | 60 req/min                   | Wait 1 min or implement exponential backoff          |
| `QUOTA_EXCEEDED`      | Monthly token limit reached  | Upgrade to Pro (500k tokens/month) or wait for reset |
| `CONCURRENT_LIMIT`    | Too many concurrent requests | Use connection pooling, max 10 concurrent            |

**Debug**: Response headers show `X-RateLimit-Remaining`.

## 500 - Server Error

Internal error in Vectora or dependencies.

| Error              | Cause                  | Solution                                              |
| ------------------ | ---------------------- | ----------------------------------------------------- |
| `EMBEDDING_FAILED` | Voyage API unavailable | Check `VOYAGE_API_KEY` and Voyage status              |
| `SEARCH_FAILED`    | Database unavailable   | Check network connection, cluster status              |
| `RERANK_FAILED`    | Reranker offline       | Wait for automatic recovery (3s retry)                |
| `LLM_ERROR`        | Gemini API error       | Check `GEMINI_API_KEY` and quota on Google AI Console |
| `TIMEOUT`          | Request > 30s          | Query too complex, simplify                           |

**Debug**: Full stack trace in `~/.vectora/logs/error.log`.

## CLI Exit Codes

```text
0 Success
1 Generic error
2 Configuration error (invalid YAML file)
3 API error (500, timeout)
4 Auth failed (401, invalid token)
5 Namespace not found (404)
127 Command not found
```

## Enable Debug Mode

For complex issues, debug mode provides a detailed view of the system's inner workings, including network logs and raw API payloads.

```bash
# Debug mode shows stack traces and verbose logging
VECTORA_DEBUG=true vectora search "query"

# Or with flag
vectora --debug search "query"

# Or globally
vectora config set DEBUG true
```

## Example: Common Troubleshoot

To facilitate resolution, keep your environment updated and check network settings before performing manual token exchange procedures.

**Scenario**: `INVALID_TOKEN` when using MCP in Claude Code

```bash
# 1. Verify if token exists
vectora auth status
# Output: Token: exp_...abc | Expires: 2026-05-19

# 2. If expired, regenerate
vectora auth token create
# Output: New token: exp_...xyz | Valid until: 2026-06-19

# 3. Update Claude Code config
# ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_TOKEN": "exp_...xyz" # New token here
      }
    }
  }
}

# 4. Restart Claude Code
```

## Reporting Bugs

If you see an undocumented error:

1. Collect logs: `vectora logs --since 1h`
2. Enable debug: `VECTORA_DEBUG=true vectora ...`
3. Open issue: <https://github.com/Kaffyn/Vectora/issues>
4. Include: error, stack trace, command used

---

> Found an undocumented error here? [Report it](https://github.com/Kaffyn/Vectora/issues)

_Part of the Vectora ecosystem_ · Open Source (MIT)
