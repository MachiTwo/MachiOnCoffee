---
title: ChatGPT Plugin
slug: chatgpt-plugin
date: "2026-04-19T09:50:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - chatgpt
  - integration
  - plugins
  - openai
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

**VECTORA CLOUD INTEGRATION**: Vectora functions as a **Custom GPT Plugin** that extends ChatGPT with codebase context search. The plugin connects directly to **Vectora Cloud**, which runs Vectora Core internally with no local server configuration needed.

> [!IMPORTANT]
> ChatGPT Custom GPT Plugin (via Vectora Cloud) vs MCP Protocol (local IDE). Choose based on your preference: Cloud for ChatGPT, MCP for Claude Code/Cursor.

## Installation

## Prerequisites

- ChatGPT Plus (with Custom GPTs access)
- Account at [Vectora Cloud](https://console.vectora.app) (Pro, Team, or Enterprise)
- Project with complete indexing

## Step 1: Get Vectora Cloud Credentials

1. Visit [console.vectora.app](https://console.vectora.app)
2. Select your project
3. Go to **Settings → API Keys**
4. Click **"New API Key"**
5. Configure:
   - **Name**: "ChatGPT Plugin"
   - **Scope**: `search` (read-only)
   - **Expires**: 1 year
6. Copy the generated token: `vca_live_xxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Create Custom GPT in ChatGPT

1. Go to [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor)
2. Click **"Create a new GPT"**
3. Name: "Vectora Codebase Assistant"
4. Description: "Intelligent assistant for codebase analysis with Vectora Cloud"

## Step 3: Configure OpenAPI Schema

In **"Configure"** → **"Actions"**, add the Vectora Cloud endpoint:

```yaml
openapi: 3.0.0
info:
  title: Vectora Cloud API
  version: 1.0.0
servers:
  - url: https://api.vectora.app/v1/plugins # Managed Vectora Cloud endpoint
paths:
  /search:
    post:
      summary: Search codebase context
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: "Search query (semantic)"
                namespace:
                  type: string
                  description: "Project namespace"
                top_k:
                  type: integer
                  default: 10
      responses:
        "200":
          description: Search results
  /analyze-dependencies:
    post:
      summary: Find all usages of a function
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                function_name:
                  type: string
                namespace:
                  type: string
      responses:
        "200":
          description: Dependency analysis
  /file-summary:
    post:
      summary: Get file structure and summary
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                file_path:
                  type: string
                namespace:
                  type: string
      responses:
        "200":
          description: File summary
```

## Step 4: Add System Instruction

In **"Instructions"** tab, copy:

```text
You are an expert code analysis assistant using Vectora.

When user asks about code:
1. Use "search" action to find relevant context
2. Use "analyze-dependencies" to find related code
3. Use "file-summary" to understand structure

Always cite file and line when referencing code.
Prioritize accuracy over speed.

Good example:
"Found this in src/auth/jwt.ts:45:
function validateToken(token) { ... }"

Bad example:
"I think the function is somewhere"
```

## Step 5: Publish

Click **"Publish to Store"** and share with your team.

## Detailed Workflows

The workflows below demonstrate real-world use cases of Vectora integrated with ChatGPT, showing practical conversations and concrete results.

## Workflow 1: Understanding Complex Feature (Onboarding)

**Scenario**: New dev wants to understand how JWT authentication works.

```text
You: "How does the JWT authentication system work here?"

ChatGPT (with Vectora):
Found implementation in 3 main files:

1. **src/auth/jwt.ts** (definition)
   function validateToken(token: string) {
     const decoded = jwt.verify(token, SECRET_KEY);
     return decoded.payload;
   }

2. **src/guards/auth.guard.ts** (applied to routes)
   @UseGuards(AuthGuard)
   async getProfile(@Req() req) {
     // Already authenticated here
   }

3. **src/tests/auth.test.ts** (examples)
   it('should reject expired token', () => {
     // Test shows expected behavior
   })

**Flow**:
request → AuthGuard.canActivate() → validateToken() → req.user = payload

**Next steps**: Add your route like this...
```

Click any file → opens in editor/browser.

## Workflow 2: Strategic Debugging

**Scenario**: You have an error and need to understand root cause.

```text
You: "Test 'should create user' is failing with
     'Cannot read property id of undefined'.
     Where's the problem?"

ChatGPT (with Vectora):
Searching for test and related code...

**Found it!**

File: src/__tests__/user.service.test.ts:145
  it('should create user', () => {
    const user = userService.create({ name: 'John' });
    expect(user.id).toBeDefined(); // ← Fails here
  })

Analyzing userService.create():

  // src/services/user.service.ts:23
  create(data: CreateUserInput) {
    // Problem: doesn't return created user
    db.insert(users).values(data);
    // Should be:
    return db.insert(users).values(data).returning();
  }

**3 instances of this pattern in code:**
  • src/services/order.service.ts:34
  • src/services/product.service.ts:12
  • src/services/invoice.service.ts:88

**Suggestion**: Apply same fix in all 3 places.
```

## Workflow 3: Assisted Code Review (Complex PR)

**Scenario**: Reviewing a PR that touches multiple auth files.

```text
You: "Review this PR that refactors auth middleware.
     [paste 50 lines of code]"

ChatGPT (with Vectora):
Analyzing changes...

**Estimated Impact**: 12 files affected
- 8 route files (GET /profile, etc)
- 2 auth tests
- 2 guards

**Issues detected**:

1. Behavior changed at line 23
   BEFORE: guard.canActivate() returns boolean
   NOW: returns Promise<boolean>

   This breaks in 4 places:
   - src/routes/admin.ts:45
   - src/routes/api.ts:78
   - src/middleware/verify.ts:12
   - src/guards/optional.ts:3

2. Positive: New isTokenValid() method reused well
   (found 6 usages)

3. Security: GuardBlacklist properly respected
   (checks all 4 patterns)

**Related tests that MUST pass**:
□ auth.guard.test.ts
□ jwt.validation.test.ts
□ permission.test.ts
□ integration/auth-flow.test.ts

**Conclusion**: Approve with conditions:
1. Fix the 4 async/await files
2. Run full test suite
3. Verify: no SECRET_KEY exposed
```

## Authentication & Security

## Token-based Auth

If your server requires authentication:

```yaml
# OpenAPI Schema
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

Configure in GPT:

```text
Go to "Configure" → "Authentication"
Select "API Key"
Paste your token
```

## Rate Limiting

Protect your server:

```bash
# In vectora config
server:
  rate_limit_per_hour: 1000
  max_concurrent: 5
```

## Privacy & Compliance

## What's Sent to OpenAI

- Your question (text)
- Search parameters (namespace, top_k)
- **Chunks are NOT saved** on OpenAI

## What Stays Local

- Vector indices (Qdrant)
- Raw embeddings
- API credentials

## Encrypted Data

```bash
# Enable end-to-end encryption
vectora config set --key "ENCRYPT_TRANSIT" --value "true"

# SSL/TLS certificate
openssl req -x509 -newkey rsa:4096 -out cert.pem -keyout key.pem

# Use with HTTPS
vectora server --cert cert.pem --key key.pem
```

## Troubleshooting

## "Plugin not responding"

**Cause**: Vectora server offline.

**Solution**:

```bash
# Check if running
curl https://your-endpoint/health

# If returns 404, start it
vectora mcp
```

## "Unauthorized"

**Cause**: Invalid or expired token.

**Solution**:

```bash
# Generate new token
vectora auth create-token --name "ChatGPT Plugin" --ttl 365d

# Update in Custom GPT settings
```

## "Timeout"

**Cause**: Search too slow.

**Solution**:

```bash
# Reduce top_k
# In GPT instructions, modify to:
"Use top_k=5 instead of 10"

# Or increase timeout
curl -X POST https://your-endpoint/search \
  -H "Timeout: 10000" \
  -d "{...}"
```

## Performance & Limits

| Resource         | Limit  | Upgrade         |
| ---------------- | ------ | --------------- |
| Searches/day     | 10,000 | Pro Plan        |
| Latency          | <2s    | SSD + more CPU  |
| Response size    | 5MB    | Compaction      |
| Concurrent users | 10     | Managed Vectora |

## Advanced Examples

## Custom GPT for Design Review

```text
Instruction:
"You are a Design Reviewer powered by Vectora.
When user shows code:
1. Search for similar patterns in project
2. Evaluate consistency
3. Suggest improvements based on existing style guides
4. Cite codebase examples"
```

## Custom GPT for Onboarding

```text
Instruction:
"You are an Onboarding Assistant.
New engineers ask how code works.
Use Vectora to:
1. Search documentation
2. Find examples
3. List dependencies
4. Suggest files to read first"
```

## Monitoring

Via Vectora console:

```bash
vectora logs --service chatgpt_plugin --level info

# Example output:
# [2026-04-19 10:30:45] POST /search - 200 - 234ms
# [2026-04-19 10:31:12] POST /analyze-dependencies - 200 - 156ms
# [2026-04-19 10:32:00] POST /file-summary - 200 - 89ms
```

---

> **Next**: [Gemini API](./gemini-api.md)

---

_Part of Vectora ecosystem_ · Open Source (MIT)
