---
title: Plano de Implementação - Vectora Cloud Platform
slug: vectora-cloud-platform
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - engineering
  - cloud
  - saas
  - react
  - authentication
  - subscriptions
---

{{< lang-toggle >}}
{{< section-toggle >}}

O **Vectora Cloud** é a plataforma SaaS que gerencia autenticação, assinaturas, painel de controle e hosting gerenciado do Vectora. Este documento descreve a arquitetura separada do core (Go) com frontend em React e backend em TypeScript/Node.js.

## Stack Técnico - Cloud vs Core

| Componente              | Core Vectora            | Vectora Cloud                                 |
| :---------------------- | :---------------------- | :-------------------------------------------- |
| **Linguagem Principal** | Go (binário)            | TypeScript/Node.js                            |
| **UI**                  | Systray (Go)            | React 18+                                     |
| **Banco de Dados**      | MongoDB Atlas (vetores) | PostgreSQL (users, subs) + MongoDB (metadata) |
| **API**                 | MCP JSON-RPC            | REST/GraphQL                                  |
| **Auth**                | JWT (local)             | OAuth 2.0 + SSO                               |
| **Hospedagem**          | User machine + Edge     | Vercel/AWS + Node.js backend                  |
| **Padrão**              | Sub-Agent               | SaaS Platform                                 |

## Arquitetura de Alto Nível

```text
┌─────────────────────┐
│ vectora.ai (website)
│ React 18 + Next.js
│ - Landing Page
│ - Pricing
│ - Docs
│ - Blog
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────────┐
│ Auth Server (Node.js) │
│ - SSO (Google, GitHub, email) │
│ - JWT generation │
│ - Rate limiting │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│ API Server (Node.js/Express) │
│ - /api/v1/auth │
│ - /api/v1/subscriptions │
│ - /api/v1/namespaces │
│ - /api/v1/usage │
└──────────┬──────────────────────────┘
           │
     ┌─────┴─────┐
     ↓ ↓
┌──────────┐ ┌──────────────┐
│PostgreSQL│ │ Stripe API │
│ Users │ │ Webhooks │
│ Plans │ │ │
│ Invoices│ └──────────────┘
└──────────┘

     And:

┌─────────────────────────────────────┐
│ Managed Vectora Instances │
│ - Claude Code agents (remote MCP) │
│ - Hosted on AWS/GCP │
└─────────────────────────────────────┘
```

## Fases de Implementação

### **Fase 1: Infraestrutura & Banco de Dados**

**Duração**: 2 semanas

**Deliverables**:

- [ ] PostgreSQL (RDS)
- [ ] Redis (cache de sessões)
- [ ] Stripe integration setup
- [ ] Email service (SendGrid)
- [ ] Logging (CloudWatch)

**Código de Exemplo - Schema PostgreSQL**:

```sql
-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    profile_picture_url VARCHAR(512),
    auth_provider VARCHAR(50), -- google, github, email
    auth_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);

-- subscriptions table
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    plan_id VARCHAR(50) NOT NULL, -- free, pro, team, enterprise
    stripe_subscription_id VARCHAR(255) UNIQUE,
    status VARCHAR(50), -- active, canceled, past_due
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    canceled_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- usage table
CREATE TABLE usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    namespace VARCHAR(255),
    metric_type VARCHAR(50), -- embeddings, reranking, searches
    count INT DEFAULT 1,
    recorded_at TIMESTAMP DEFAULT NOW(),
    billing_period DATE
);

-- api_keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    last_used_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP NULL
);
```

### **Fase 2: Authentication Server (OAuth 2.0 + SSO)**

**Duração**: 2 semanas

**Deliverables**:

- [ ] Google OAuth integration
- [ ] GitHub OAuth integration
- [ ] Email/password with magic links
- [ ] JWT token generation & refresh
- [ ] Rate limiting per IP

**Código de Exemplo - Auth Server (TypeScript/Express)**:

```typescript
// src/routes/auth.ts
import express from "express";
import { OAuth2Client } from "google-auth-library";
import jwt from "jsonwebtoken";

const router = express.Router();
const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

// POST /auth/google/callback
router.post("/google/callback", async (req, res) => {
  const { token } = req.body;

  try {
    const ticket = await googleClient.verifyIdToken({
      idToken: token,
      audience: process.env.GOOGLE_CLIENT_ID,
    });

    const payload = ticket.getPayload()!;

    // Buscar ou criar usuário
    let user = await db.users.findOne({ email: payload.email });
    if (!user) {
      user = await db.users.create({
        email: payload.email,
        name: payload.name,
        profile_picture_url: payload.picture,
        auth_provider: "google",
        auth_id: payload.sub,
      });
    }

    // Gerar JWT
    const jwtToken = jwt.sign(
      {
        userId: user.id,
        email: user.email,
        namespace: `${user.id}-default`,
      },
      process.env.JWT_SECRET!,
      { expiresIn: "30d" },
    );

    res.json({
      token: jwtToken,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
    });
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
});

// POST /auth/refresh
router.post("/refresh", async (req, res) => {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!);

    const newToken = jwt.sign({ userId: decoded.userId, email: decoded.email }, process.env.JWT_SECRET!, {
      expiresIn: "30d",
    });

    res.json({ token: newToken });
  } catch {
    res.status(401).json({ error: "Invalid refresh token" });
  }
});

export default router;
```

### **Fase 3: API Server (REST para Gestão)**

**Duração**: 2 semanas

**Deliverables**:

- [ ] CRUD de namespaces
- [ ] Gestão de API keys
- [ ] Endpoints de usage/quota
- [ ] Webhook para Stripe
- [ ] Rate limiting global

**Código de Exemplo - API REST**:

```typescript
// src/routes/api.ts
import express from "express";
import { authMiddleware } from "../middleware/auth";
import { rateLimitMiddleware } from "../middleware/rateLimit";

const router = express.Router();

// GET /api/v1/user/profile
router.get("/user/profile", authMiddleware, async (req, res) => {
  const user = await db.users.findById(req.user.id);
  const subscription = await db.subscriptions.findOne({ user_id: req.user.id });

  res.json({
    user,
    subscription,
    quotas: {
      embeddings: subscription.plan.monthly_embedding_quota,
      reranking: subscription.plan.monthly_rerank_quota,
    },
  });
});

// GET /api/v1/namespaces
router.get("/namespaces", authMiddleware, async (req, res) => {
  const namespaces = await db.query("SELECT * FROM namespaces WHERE user_id = $1", [req.user.id]);
  res.json(namespaces);
});

// POST /api/v1/namespaces
router.post("/namespaces", authMiddleware, async (req, res) => {
  const { name, description } = req.body;

  const namespace = await db.namespaces.create({
    user_id: req.user.id,
    name,
    description,
    namespace_id: `${req.user.id}-${Date.now()}`,
  });

  res.status(201).json(namespace);
});

// GET /api/v1/usage
router.get("/usage", authMiddleware, async (req, res) => {
  const usage = await db.query(
    `
        SELECT metric_type, SUM(count) as total
        FROM usage
        WHERE user_id = $1
        AND billing_period = CURRENT_DATE
        GROUP BY metric_type
    `,
    [req.user.id],
  );

  res.json(usage);
});

// POST /api/v1/stripe/webhook
router.post("/stripe/webhook", express.raw({ type: "application/json" }), async (req, res) => {
  const event = req.body;

  if (event.type === "customer.subscription.updated") {
    const customerId = event.data.object.customer;
    const user = await db.users.findOne({ stripe_customer_id: customerId });

    await db.subscriptions.update({
      user_id: user.id,
      status: event.data.object.status,
    });
  }

  res.json({ received: true });
});

export default router;
```

### **Fase 4: Website em React/Next.js**

**Duração**: 3 semanas

**Deliverables**:

- [ ] Landing page elegante
- [ ] Pricing page com 4 planos
- [ ] Documentation site (MDX)
- [ ] Blog
- [ ] Dashboard autenticado

**Estrutura de Projeto**:

```text
vectora-web/
├── app/
│ ├── page.tsx # Landing
│ ├── pricing/page.tsx # Pricing
│ ├── docs/[...slug]/page.tsx # Docs
│ ├── dashboard/page.tsx # Dashboard (auth required)
│ └── api/
│ └── auth/[...nextauth]/route.ts
├── components/
│ ├── landing/Hero.tsx
│ ├── landing/Features.tsx
│ ├── landing/Pricing.tsx
│ ├── dashboard/Sidebar.tsx
│ ├── dashboard/UsageChart.tsx
│ └── auth/LoginButton.tsx
├── lib/
│ ├── api.ts # API client
│ ├── auth.ts # Auth utilities
│ └── stripe.ts # Stripe integration
└── styles/
    └── globals.css # Tailwind
```

**Código de Exemplo - Dashboard Component**:

```typescript
// app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';
import { apiClient } from '@/lib/api';

export default function Dashboard() {
    const { data: session } = useSession();
    const [usage, setUsage] = useState(null);
    const [subscription, setSubscription] = useState(null);

    useEffect(() => {
        if (!session) {
            redirect('/auth/login');
        }

        const fetchData = async () => {
            const [usageRes, subRes] = await Promise.all([
                apiClient.get('/api/v1/usage'),
                apiClient.get('/api/v1/user/profile'),
            ]);

            setUsage(usageRes.data);
            setSubscription(subRes.data.subscription);
        };

        fetchData();
    }, [session]);

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 py-4">
                    <h1 className="text-2xl font-bold">Vectora Dashboard</h1>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto px-4 py-8">
                <div className="grid grid-cols-2 gap-6 mb-8">
                    <div className="bg-white rounded-lg p-6 shadow">
                        <h2 className="text-gray-600 text-sm font-semibold">
                            Embeddings This Month
                        </h2>
                        <p className="text-3xl font-bold mt-2">
                            {usage?.embeddings || 0}
                        </p>
                        <p className="text-gray-500 text-xs mt-1">
                            of {subscription?.plan?.monthly_quota || 'unlimited'}
                        </p>
                    </div>

                    <div className="bg-white rounded-lg p-6 shadow">
                        <h2 className="text-gray-600 text-sm font-semibold">
                            Plan
                        </h2>
                        <p className="text-2xl font-bold mt-2">
                            {subscription?.plan_id || 'free'}
                        </p>
                        <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded text-sm">
                            Upgrade Plan
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
}
```

### **Fase 5: Pricing & Stripe Integration**

**Duração**: 2 semanas

**Deliverables**:

- [ ] 4 planos: Free, Pro, Team, Enterprise
- [ ] Checkout com Stripe
- [ ] Invoice geração automática
- [ ] Webhook handling
- [ ] Renewals automáticos

**Planos Propostos**:

| Plano          | Preço   | Storage | Embeddings | Reranking | Suporte       |
| :------------- | :------ | :------ | :--------- | :-------- | :------------ |
| **Free**       | $0      | 512 MB  | 100K/mês   | 10K/mês   | Community     |
| **Pro**        | $29/mês | 5 GB    | 10M/mês    | 1M/mês    | Email         |
| **Team**       | $99/mês | 50 GB   | 100M/mês   | 10M/mês   | Slack + Phone |
| **Enterprise** | Custom  | Custom  | Unlimited  | Unlimited | Dedicated     |

### **Fase 6: Dashboard Admin & Analytics**

**Duração**: 2 semanas

**Deliverables**:

- [ ] Gráficos de uso por usuário
- [ ] Revenue dashboard
- [ ] User management
- [ ] Quota management
- [ ] Support ticket system

### **Fase 7: Managed Vectora Instances (Core + Integrações)**

**Duração**: 4 semanas

**Deliverables**:

- [ ] Kubernetes cluster setup para instâncias gerenciadas do Core
- [ ] Auto-scaling por namespace com rate limiting
- [ ] Integration hooks para ChatGPT Plugin, MCP, REST API
- [ ] Monitoring com Prometheus + AlertManager
- [ ] Backup automático + disaster recovery
- [ ] Plugin gateway (normaliza requisições de diferentes clientes)

**Código de Exemplo - Managed Instance Initialization**:

```go
// pkg/cloud/managed_instance.go
package cloud

import (
    "context"
    "fmt"
    "time"

    "vectora/pkg/core"
    "vectora/pkg/mcp"
    "vectora/pkg/guardian"
)

type ManagedInstance struct {
    ProjectID string
    Namespace string
    Core *core.Vectora
    MCPServer *mcp.Server
    Guardian *guardian.Engine
    Created time.Time
    LastActivity time.Time
}

func NewManagedInstance(ctx context.Context, projectID, namespace string) (*ManagedInstance, error) {
    // 1. Inicializar Core (RAM + disk alocados no Kubernetes Pod)
    coreInstance, err := core.NewVectora(&core.Config{
        Namespace: namespace,
        VectorDB: "mongodb+srv://user:pass@vectora-db",
        ProviderRouter: initProviders(), // Gemini, Voyage
    })
    if err != nil {
        return nil, fmt.Errorf("failed to init core: %w", err)
    }

    // 2. Inicializar MCP Server (stdio + HTTP gateway)
    mcpServer := mcp.NewServer()
    registerTools(mcpServer, coreInstance)

    // 3. Inicializar Guardian com regras do projeto
    guardianEngine, err := guardian.NewEngine(projectID)
    if err != nil {
        return nil, fmt.Errorf("failed to init guardian: %w", err)
    }

    return &ManagedInstance{
        ProjectID: projectID,
        Namespace: namespace,
        Core: coreInstance,
        MCPServer: mcpServer,
        Guardian: guardianEngine,
        Created: time.Now(),
        LastActivity: time.Now(),
    }, nil
}

// ExecutePluginRequest expõe endpoint para ChatGPT Plugin
func (mi *ManagedInstance) ExecutePluginRequest(ctx context.Context, req *PluginRequest) (*PluginResponse, error) {
    // 1. Validar API Key
    if err := mi.Guardian.ValidateAPIKey(req.APIKey); err != nil {
        return nil, fmt.Errorf("unauthorized: %w", err)
    }

    // 2. Validar request
    if err := mi.Guardian.ValidateRequest(req); err != nil {
        return nil, fmt.Errorf("invalid request: %w", err)
    }

    // 3. Executar operação (search, analyze, etc)
    var result interface{}
    switch req.Operation {
    case "search_context":
        result, _ = mi.Core.SearchContext(ctx, req.Query, req.TopK)
    case "analyze_dependencies":
        result, _ = mi.Core.AnalyzeDependencies(ctx, req.SymbolName)
    case "file_summary":
        result, _ = mi.Core.GetFileSummary(ctx, req.FilePath)
    }

    // 4. Sanitizar output
    sanitized := mi.Guardian.SanitizeOutput(result)

    // 5. Log auditoria
    mi.Guardian.AuditLog("plugin_call", req.Operation, true)

    mi.LastActivity = time.Now()
    return &PluginResponse{
        Success: true,
        Data: sanitized,
        Latency: time.Since(ctx.Done()),
    }, nil
}

type PluginRequest struct {
    APIKey string
    Operation string // search_context, analyze_dependencies, file_summary
    Query string
    TopK int
    SymbolName string
    FilePath string
}

type PluginResponse struct {
    Success bool
    Data interface{}
    Latency time.Duration
}
```

**Plugin Gateway (HTTP Bridge)**:

```go
// pkg/cloud/plugin_gateway.go
package cloud

import (
    "context"
    "net/http"
    "time"
)

type PluginGateway struct {
    instances map[string]*ManagedInstance
}

// POST /v1/plugins/:project-id/search
func (pg *PluginGateway) HandlePluginRequest(w http.ResponseWriter, r *http.Request) {
    projectID := r.PathValue("project-id")
    apiKey := r.Header.Get("X-API-Key")

    // 1. Recuperar instância gerenciada do projeto
    instance, ok := pg.instances[projectID]
    if !ok {
        http.Error(w, "Project not found", 404)
        return
    }

    // 2. Parse request body
    var req PluginRequest
    json.NewDecoder(r.Body).Decode(&req)
    req.APIKey = apiKey

    // 3. Executar com timeout de 30s
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    resp, err := instance.ExecutePluginRequest(ctx, &req)
    if err != nil {
        http.Error(w, err.Error(), 400)
        return
    }

    // 4. Retornar resposta (JSON-RPC 2.0 ou OpenAPI)
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}
```

## Stack Final - Vectora Cloud

**Frontend**:

- React 18 + Next.js 14
- Tailwind CSS
- TypeScript
- Next-Auth.js para SSO
- SWR/React Query para data fetching

**Backend**:

- Node.js + Express
- TypeScript
- PostgreSQL (users, subscriptions)
- Redis (cache, rate limiting)
- Stripe API
- SendGrid (email)

**Infrastructure**:

- Vercel (frontend)
- AWS ECS/Lambda (backend)
- RDS PostgreSQL
- ElastiCache Redis
- CloudWatch (logs)
- Route 53 (DNS)

## Métricas de Sucesso

- Signup flow: <60 segundos
- Login: <1 segundo
- Dashboard load: <2 segundos
- API response: <200ms p95
- Uptime: 99.9%
- NPS: >50

---

_Parte do ecossistema Vectora Cloud_ · Plataforma SaaS
