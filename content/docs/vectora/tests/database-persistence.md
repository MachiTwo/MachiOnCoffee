---
title: Database & Persistence Test Suite
slug: database-persistence-tests
date: "2026-04-23T22:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - caching
  - concepts
  - database
  - embeddings
  - errors
  - go
  - mongodb
  - persistence
  - testing
  - vector-search
  - vectora
---

{{< lang-toggle >}}

Esta suite valida que Vectora persiste dados corretamente, recupera-os eficientemente e sincroniza entre local e cloud sem perda de integridade. Cobertura: **80+ testes** | **Prioridade**: CRÍTICA

## Objetivo

Verificar que Vectora persiste dados corretamente, recupera-os eficientemente e sincroniza entre local e cloud sem perda de integridade.

---

## Componentes Testados

1. MongoDB Atlas connection
2. Embedding storage & retrieval
3. Chunk persistence
4. API key management
5. Local cache (híbrido)
6. Data roaming (cloud sync)
7. Vector indices
8. Aggregation pipelines
9. Transaction handling

---

## Segmentos de Testes

### 1. Conectividade MongoDB (15 testes)

#### Test: Connection Establishment

```text
Given: MongoDB Atlas URI válida
When: Vectora inicia
Then: Conexão estabelecida em < 2s
And: Pool de conexões > 10
And: Timeout em 30s
```

#### Test: Connection Retry Logic

```text
Given: MongoDB offline
When: Vectora tenta conectar
Then: 3 retries com backoff exponencial
And: Alerta logado após falha
And: Recuperação automática quando online
```

#### Test: Connection Pooling

```text
Given: 50 requisições simultâneas
When: Todas executadas em paralelo
Then: Todas usam pool (< 10 conexões)
And: Latência p95 < 100ms
And: Sem conexões pendentes
```

#### Test: Connection Timeout

```text
Given: Servidor MongoDB não responde
When: Query enviada
Then: Timeout em 30s (configurável)
And: Erro retornado graciosamente
And: Connection descartada
```

---

### 2. Operações CRUD com Embeddings (20 testes)

#### Test: Insert Vector

```text
Given: Embedding válido [384-dim, float32]
When: Inserido em MongoDB
Then: Documento salvo com _id único
And: Vector indexado
And: Metadata preservada
And: Timestamp registrado
```

#### Test: Search Vector

```text
Given: 1000 embeddings no banco
When: Query com vector search
Then: Top 5 resultados retornados
And: Ordenados por similaridade (cosine)
And: Latência < 200ms
And: Score > 0.7 para relevância
```

#### Test: Update Vector

```text
Given: Embedding existente
When: Vector e metadata atualizados
Then: Documento modificado
And: Histórico preservado
And: Vector index recalculado
And: Versão incrementada
```

#### Test: Delete Vector

```text
Given: Embedding no banco
When: Deletado
Then: Documento removido
And: Index atualizado
And: Referências limpas
And: Soft delete com timestamp
```

#### Test: Batch Operations

```text
Given: 500 embeddings para inserir
When: Batch insert executado
Then: Todos inseridos em < 5s
And: Transação atômica
And: Rollback se erro
And: Progress tracked
```

#### Test: Vector Dimension Validation

```text
Given: Embedding com dimensão errada
When: Insert tentado
Then: Erro rejeitado
And: Mensagem clara sobre esperado
And: Banco não modificado
```

---

### 3. Persistência de Chunks (15 testes)

#### Test: Chunk Storage

```text
Given: Código fonte analisado
When: Chunks criados e salvos
Then: Cada chunk tem:
  - ID único
  - Embedding (384-dim)
  - Metadata (file, line, type)
  - Timestamp
  - Version
```

#### Test: Chunk Retrieval by Query

```text
Given: 1000 chunks no banco
When: Query "authentication"
Then: Chunks relevantes retornados
And: Ordenados por relevância
And: Latência < 300ms
And: Top 10 retornados
```

#### Test: Chunk Relationships

```text
Given: Chunks de arquivo interrelacionado
When: Buscados por relacionamento
Then: Dependências carregadas
And: Contexto completo disponível
And: No circular references
```

---

### 4. Data Roaming (15 testes)

#### Test: Local Cache Sync

```text
Given: Usuário offline
When: Faz 10 searches
Then: Resultados vêm do cache local
And: Sincronização queued
When: Online novamente
Then: Cache sincroniza com cloud
And: Sem conflitos
And: Merge strategy aplicada
```

#### Test: Conflict Resolution

```text
Given: Mesma query em 2 devices simultâneamente
When: Ambos modificam documento
Then: Último write (timestamp) vence
Or: Merge automático se possível
And: Usuário notificado de conflito
```

#### Test: Data Roaming Latency

```text
Given: 100 documentos para sincronizar
When: Sincronização iniciada
Then: Completa em < 5s
And: Compressão delta aplicada
And: Bandwidth < 1MB
```

#### Test: Encryption at Rest

```text
Given: Dados locais
When: Salvos em AppData
Then: Criptografados com chave do usuário
And: AES-256 ou equivalente
And: Integridade verificável
```

---

### 5. Índices Vetoriais (10 testes)

#### Test: Vector Index Creation

```text
Given: 10000 embeddings
When: Vector index criado
Then: Index completo em < 30s
And: Type: sphere (cosine)
And: Dimensionalidade: 384
And: Queryable em < 100ms
```

#### Test: Index Maintenance

```text
Given: Index existente com 5000 docs
When: Mais 5000 adicionados
Then: Index atualizado incrementalmente
And: Performance não degrada
And: Sem downtime
```

#### Test: Index Search Accuracy

```text
Given: Query vector
When: Top 10 resultados buscados
Then: Precisão > 0.95 vs brute-force
And: Recall > 0.90
```

---

### 6. Aggregation Pipelines (5 testes)

#### Test: Complex Aggregation

```text
Given: 10000 chunks em 100 arquivos
When: Agregação executada:
  $match: {type: "function"}
  $group: {_id: "$file", count}
  $sort: {count: -1}
Then: Resultado em < 1s
And: 50 grupos retornados
```

---

## Critérios de Aceitação

| Critério            | Alvo                |
| ------------------- | ------------------- |
| Taxa de sucesso     | 100%                |
| Cobertura MongoDB   | > 90%               |
| Latência query p95  | < 300ms             |
| Latência insert p95 | < 200ms             |
| Cache hit rate      | > 70%               |
| Data sync < 5s      | > 1000 docs         |
| Zero data loss      | Em qualquer cenário |
| Sem race conditions | Concurrent 50+      |

---

## Dependências de API

Para executar esta suite, você precisa:

```env
MONGODB_ATLAS_URI=mongodb+srv://user:pass@cluster.mongodb.net
MONGODB_DATABASE=vectora_test
VOYAGE_API_KEY=xxxx (para embeddings)
```

---

## Como Executar

```bash
# Todos os testes de banco de dados
go test -v ./tests/database/...

# Com coverage
go test -v -cover ./tests/database/...

# Específico
go test -v -run TestInsertVector ./tests/database/...

# Com race detection
go test -v -race ./tests/database/...

# Com timeout customizado
go test -v -timeout 5m ./tests/database/...
```

---

## Mapa de Implementação

- [ ] Conectividade MongoDB (15 testes)
- [ ] Operações CRUD (20 testes)
- [ ] Persistência de chunks (15 testes)
- [ ] Data roaming (15 testes)
- [ ] Índices vetoriais (10 testes)
- [ ] Aggregations (5 testes)

**Total**: 80 testes

---

## External Linking

| Concept           | Resource                          | Link                                                                                                       |
| ----------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **MongoDB Atlas** | Atlas Vector Search Documentation | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |

---

**Vectora v0.1.0** · [GitHub](https://github.com/Kaffyn/Vectora) · [Licença (MIT)](https://github.com/Kaffyn/Vectora/blob/master/LICENSE) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)

_Parte do ecossistema Vectora AI Agent. Construído com [ADK](https://adk.dev/), [Claude](https://claude.ai/) e [Go](https://golang.org/)._

© 2026 Contribuidores do Vectora. Todos os direitos reservados.
