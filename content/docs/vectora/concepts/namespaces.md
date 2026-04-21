---
title: Namespaces
slug: namespaces
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - concepts
  - mcp
  - namespaces
  - vectora
---

{{< lang-toggle >}}
Namespaces são **isoladores lógicos** de índices vetoriais dentro de um único cluster. Cada projeto, ambiente ou contexto roda em seu próprio namespace, evitando contaminação de resultados.

> [!IMPORTANT]
> Um namespace é como um "banco de dados virtual" dentro do Qdrant. Buscas em um namespace NUNCA retornam chunks de outro namespace.

---

## O Problema

Sem namespaces:

- Busca por "login" retorna chunks de 50 projetos diferentes
- Fácil "vazar" contexto entre equipes
- Impossível gerenciar índices por projeto ou ambiente

Com namespaces:

- Busca é isolada: "login" retorna APENAS do projeto X
- Múltiplas equipes podem compartilhar uma instância Qdrant sem contaminação
- Escalabilidade: adiciona novo projeto = novo namespace

---

## Nomenclatura & Convenções

A padronização dos nomes de namespaces é fundamental para a organização e automação em clusters multitenant.

## Padrão Recomendado

```text
<org>-<project>-<environment>
```

Exemplos:

```yaml
kaffyn-vectora-prod # Organização-Projeto-Env
kaffyn-vectora-dev # Mesmo projeto, ambiente diferente
acme-backend-staging # Outro projeto
acme-docs-prod # Documentação do mesmo org
```

## Validação

Namespaces devem:

- Ter 3-63 caracteres
- Usar apenas `[a-z0-9-]` (lowercase, números, hífens)
- Começar com letra
- NÃO incluir underscores ou espaços

```bash
# Válidos
kaffyn-vectora-prod
my-app-v2
docs-search

# Inválidos
Kaffyn-Vectora-Prod # Maiúscula
my_app_prod # Underscore
my-app-prod! # Caractere especial
my.app.prod # Ponto
```

---

## Ciclo de Vida

O gerenciamento de namespaces compreende desde a sua inicialização técnica até o descarte seguro dos dados indexados.

## Criação

```bash
# Via CLI
vectora namespace create --name kaffyn-vectora-prod

# Via config
vectora.config.yaml:
  project:
    namespace: kaffyn-vectora-prod
```

Quando criado:

1. Qdrant cria uma nova collection
2. Indices vazios são inicializados (HNSW para embeddings)
3. Guardian registra namespace em audit log

## Indexing

Uma vez criado, o namespace aceita chunks:

```yaml
# indexing.yaml
paths:
  - ./src/**/*.ts
  - ./docs/**/*.md

namespace: kaffyn-vectora-prod
# Chunks são inseridos como:
# {
# id: "uuid",
# vector: [0.12, 0.45, ...],
# payload: {
# namespace: "kaffyn-vectora-prod",
# file: "src/context-engine.ts",
# ...
# }
# }
```

## Busca

Toda busca especifica namespace:

```typescript
// Search é filtrada por namespace
const results = await vectoraClient.search({
  query: "Como validar tokens?",
  namespace: "kaffyn-vectora-prod",
  top_k: 10,
});
// Retorna APENAS chunks com namespace === "kaffyn-vectora-prod"
```

## Deletion & Cleanup

```bash
# Deletar namespace inteiro
vectora namespace delete --name kaffyn-vectora-prod

# Resetar índices de um namespace
vectora namespace reset --name kaffyn-vectora-prod
```

> Deletar namespace é PERMANENTE e não recuperável.

---

## Multi-Tenancy Patterns

O uso de namespaces permite a implementação de diferentes padrões de isolamento dependendo da necessidade do projeto ou da organização.

## Pattern 1: One Namespace per Project

```yaml
# Team A
namespace: acme-backend-prod

# Team B
namespace: acme-frontend-prod

# Isolation: Completa
# Sharing: Impossível
```

Use quando: Times completamente separados, compliance/segurança rigorosa.

## Pattern 2: Environments in Same Project

```yaml
# Prod
namespace: acme-backend-prod

# Staging
namespace: acme-backend-staging

# Dev
namespace: acme-backend-dev

# Isolation: Por environment
# Sharing: Mesmo projeto em dev/prod
```

Use quando: Mesmo projeto, múltiplos environments.

## Pattern 3: Shared Services + Private Teams

```yaml
# Shared (documentação, utilidades)
namespace: acme-shared-docs

# Team A (isolada)
namespace: acme-teamA-prod

# Team B (isolada)
namespace: acme-teamB-prod

# Isolation: Por time
# Sharing: Via namespace acme-shared-docs
```

Use quando: Equipes paralelas com uma base comum.

---

## Métricas por Namespace

A observabilidade é aplicada individualmente a cada namespace, permitindo auditorias precisas de performance e uso.

## Inspecting

```bash
vectora namespace info --name kaffyn-vectora-prod
```

Output:

```yaml
namespace: kaffyn-vectora-prod
created_at: "2026-04-19T10:00:00Z"
chunks_indexed: 2847
chunks_pending: 12
collection_size_mb: 15.3
last_indexed: "2026-04-19T14:32:00Z"
index_health: healthy
search_latency_p99_ms: 245
searches_total_24h: 3421
```

## Alerts

Monitor via Harness:

```yaml
harness:
  namespace_health:
    alert_on_latency_p99 > 500ms: true
    alert_on_pending_chunks > 100: true
    alert_on_index_corruption: true
```

---

## Configuração

```yaml
# vectora.config.yaml
project:
  name: "Meu Projeto"
  namespace: kaffyn-vectora-prod

# Múltiplos namespaces (advanced)
namespaces:
  default: kaffyn-vectora-prod
  fallback: kaffyn-vectora-backup
  exclude_from_search:
    - kaffyn-old-archive
```

---

## Limitações & Considerar

| Recurso                | Limite                        |
| ---------------------- | ----------------------------- |
| Namespaces por cluster | 1000+                         |
| Chunks por namespace   | Unlimited (disk)              |
| Latência de busca      | O(log n) em HNSW              |
| Isolamento             | Lógico (mesmo cluster físico) |

Para isolamento **físico** (compliance rigorosa):

- Use clusters Qdrant separados
- Configure endpoints diferentes por namespace
- Implemente network isolation

---

> **Próximo**: [Trust Folder](./trust-folder.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
