---
title: Plano de Implementação - Vector Database (MongoDB Atlas)
slug: vector-database-implementation
date: "2026-04-20T10:30:00-03:00"
type: docs
tags:
  - ai
  - architecture
  - backend
  - concepts
  - config
  - embeddings
  - engineering
  - errors
  - golang
  - mongodb
  - mongodb-atlas
  - security
  - state
  - vector-database
  - vector-search
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

O Vectora usa **MongoDB Atlas** como backend unificado para vetores, metadados, sessões e audit logs. Este documento descreve a implementação do cliente MongoDB em Go com isolamento multi-tenant.

## Arquitetura de Collections

```text
vectora (database)
├── documents
│ ├── _id
│ ├── namespace_id
│ ├── file_path
│ ├── embedding_vector (1536D)
│ ├── content (truncado)
│ └── metadata
├── sessions
│ ├── session_id
│ ├── user_id
│ ├── namespace
│ ├── current_plan
│ ├── tool_history
│ └── created_at (TTL: 30 dias)
└── audit_logs
    ├── log_id
    ├── session_id
    ├── action
    ├── timestamp
    └── security_flags
```

## Fases de Implementação

### **Fase 1: MongoDB Client Setup & Connection Pooling**

**Duração**: 1 semana

**Deliverables**:

- [ ] Inicialização do cliente com pooling
- [ ] Health check periódico
- [ ] Reconnection logic com backoff
- [ ] Context timeout em operações

**Código de Exemplo**:

```go
// pkg/storage/mongodb.go
package storage

import (
    "context"
    "fmt"
    "time"

    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "go.mongodb.org/mongo-driver/mongo/readpref"
)

type MongoDBClient struct {
    client *mongo.Client
    db *mongo.Database
}

func NewMongoDBClient(ctx context.Context, uri string) (*MongoDBClient, error) {
    opts := options.Client().
        ApplyURI(uri).
        SetMaxPoolSize(100).
        SetMinPoolSize(10).
        SetMaxConnIdleTime(5 * time.Minute)

    client, err := mongo.Connect(ctx, opts)
    if err != nil {
        return nil, fmt.Errorf("failed to connect: %w", err)
    }

    // Ping para validar conexão
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    if err := client.Ping(ctx, readpref.Primary()); err != nil {
        return nil, fmt.Errorf("ping failed: %w", err)
    }

    return &MongoDBClient{
        client: client,
        db: client.Database("vectora"),
    }, nil
}

func (mc *MongoDBClient) Close(ctx context.Context) error {
    return mc.client.Disconnect(ctx)
}

func (mc *MongoDBClient) HealthCheck(ctx context.Context) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    return mc.client.Ping(ctx, readpref.Primary())
}
```

### **Fase 2: Collection Documents (Embeddings + Metadados)**

**Duração**: 1 semana

**Deliverables**:

- [ ] Schema e índices para documents
- [ ] HNSW index configuration
- [ ] Operações CRUD
- [ ] Batch insertion

**Código de Exemplo**:

```go
// pkg/storage/documents.go
package storage

import (
    "context"
    "fmt"
    "time"

    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

type Document struct {
    ID string `bson:"_id"`
    NamespaceID string `bson:"namespace_id"`
    FilePath string `bson:"file_path"`
    StartLine int `bson:"start_line"`
    EndLine int `bson:"end_line"`
    Content string `bson:"content"`
    EmbeddingVector []float32 `bson:"embedding_vector"`
    Metadata map[string]interface{} `bson:"metadata"`
    Visibility string `bson:"visibility"` // public, private
    Checksum string `bson:"checksum"`
    IndexedAt time.Time `bson:"indexed_at"`
}

type DocumentStore struct {
    collection *mongo.Collection
}

func NewDocumentStore(db *mongo.Database) *DocumentStore {
    return &DocumentStore{
        collection: db.Collection("documents"),
    }
}

func (ds *DocumentStore) Initialize(ctx context.Context) error {
    // Criar índices
    indexModel := mongo.IndexModel{
        Keys: bson.D{
            {Key: "embedding_vector", Value: "cosmosSearch"},
            {Key: "namespace_id", Value: 1},
            {Key: "visibility", Value: 1},
        },
        Options: options.Index().SetUnique(false),
    }

    indexModel2 := mongo.IndexModel{
        Keys: bson.D{
            {Key: "namespace_id", Value: 1},
            {Key: "file_path", Value: 1},
        },
        Options: options.Index().SetUnique(true),
    }

    _, err := ds.collection.Indexes().CreateMany(ctx, []mongo.IndexModel{indexModel, indexModel2})
    return err
}

func (ds *DocumentStore) InsertDocument(ctx context.Context, doc *Document) error {
    doc.IndexedAt = time.Now()

    result, err := ds.collection.InsertOne(ctx, doc)
    if err != nil {
        return fmt.Errorf("insert failed: %w", err)
    }

    doc.ID = result.InsertedID.(string)
    return nil
}

func (ds *DocumentStore) BatchInsertDocuments(ctx context.Context, docs []*Document) error {
    if len(docs) == 0 {
        return nil
    }

    interfaces := make([]interface{}, len(docs))
    for i, doc := range docs {
        doc.IndexedAt = time.Now()
        interfaces[i] = doc
    }

    _, err := ds.collection.InsertMany(ctx, interfaces)
    return err
}

func (ds *DocumentStore) GetDocument(ctx context.Context, id string) (*Document, error) {
    var doc Document
    err := ds.collection.FindOne(ctx, bson.M{"_id": id}).Decode(&doc)
    if err == mongo.ErrNoDocuments {
        return nil, fmt.Errorf("document not found")
    }
    return &doc, err
}

func (ds *DocumentStore) DeleteByNamespace(ctx context.Context, namespaceID string) error {
    result, err := ds.collection.DeleteMany(ctx, bson.M{"namespace_id": namespaceID})
    if err != nil {
        return err
    }
    fmt.Printf("Deleted %d documents from namespace %s\n", result.DeletedCount, namespaceID)
    return nil
}
```

### **Fase 3: Collection Sessions (Estado Operacional)**

**Duração**: 1 semana

**Deliverables**:

- [ ] Session lifecycle management
- [ ] TTL index (30 dias de inatividade)
- [ ] CRUD operações
- [ ] Serialização segura

**Código de Exemplo**:

```go
// pkg/storage/sessions.go
package storage

import (
    "context"
    "fmt"
    "time"

    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

type Session struct {
    SessionID string `bson:"session_id"`
    UserID string `bson:"user_id"`
    Namespace string `bson:"namespace"`
    CurrentPlan map[string]interface{} `bson:"current_plan"`
    ToolHistory []map[string]interface{} `bson:"tool_history"`
    ContextCache map[string]interface{} `bson:"context_cache"`
    CreatedAt time.Time `bson:"created_at"`
    LastActivity time.Time `bson:"last_activity"`
}

type SessionStore struct {
    collection *mongo.Collection
}

func NewSessionStore(db *mongo.Database) *SessionStore {
    return &SessionStore{
        collection: db.Collection("sessions"),
    }
}

func (ss *SessionStore) Initialize(ctx context.Context) error {
    // Criar TTL index (30 dias após last_activity)
    ttlIndex := mongo.IndexModel{
        Keys: bson.D{{Key: "last_activity", Value: 1}},
        Options: options.Index().SetExpireAfter(30 * 24 * time.Hour),
    }

    _, err := ss.collection.Indexes().CreateOne(ctx, ttlIndex)
    return err
}

func (ss *SessionStore) CreateSession(ctx context.Context, userID, namespace string) (*Session, error) {
    sessionID := generateSessionID() // UUID v4

    session := &Session{
        SessionID: sessionID,
        UserID: userID,
        Namespace: namespace,
        CurrentPlan: make(map[string]interface{}),
        ToolHistory: make([]map[string]interface{}, 0),
        ContextCache: make(map[string]interface{}),
        CreatedAt: time.Now(),
        LastActivity: time.Now(),
    }

    _, err := ss.collection.InsertOne(ctx, session)
    if err != nil {
        return nil, fmt.Errorf("failed to create session: %w", err)
    }

    return session, nil
}

func (ss *SessionStore) GetSession(ctx context.Context, sessionID string) (*Session, error) {
    var session Session
    err := ss.collection.FindOne(ctx, bson.M{"session_id": sessionID}).Decode(&session)
    if err == mongo.ErrNoDocuments {
        return nil, fmt.Errorf("session not found")
    }
    return &session, err
}

func (ss *SessionStore) UpdateLastActivity(ctx context.Context, sessionID string) error {
    _, err := ss.collection.UpdateOne(
        ctx,
        bson.M{"session_id": sessionID},
        bson.M{"$set": bson.M{"last_activity": time.Now()}},
    )
    return err
}

func (ss *SessionStore) AppendToolCall(ctx context.Context, sessionID string, toolCall map[string]interface{}) error {
    _, err := ss.collection.UpdateOne(
        ctx,
        bson.M{"session_id": sessionID},
        bson.M{
            "$push": bson.M{"tool_history": toolCall},
            "$set": bson.M{"last_activity": time.Now()},
        },
    )
    return err
}
```

### **Fase 4: Collection Audit Logs (Compliance)**

**Duração**: 5 dias

**Deliverables**:

- [ ] Imutabilidade de logs
- [ ] Indexação por timestamp
- [ ] Retenção configurável
- [ ] Queries de auditoria

**Código de Exemplo**:

```go
// pkg/storage/audit_logs.go
package storage

import (
    "context"
    "fmt"
    "time"

    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

type AuditLog struct {
    LogID string `bson:"log_id"`
    SessionID string `bson:"session_id"`
    UserID string `bson:"user_id"`
    Action string `bson:"action"`
    InputHash string `bson:"input_hash"`
    OutputMetadata map[string]interface{} `bson:"output_metadata"`
    SecurityFlags []string `bson:"security_flags"`
    Timestamp time.Time `bson:"timestamp"`
}

type AuditLogStore struct {
    collection *mongo.Collection
}

func NewAuditLogStore(db *mongo.Database) *AuditLogStore {
    return &AuditLogStore{
        collection: db.Collection("audit_logs"),
    }
}

func (als *AuditLogStore) Initialize(ctx context.Context) error {
    // Índices para auditoria eficiente
    indexes := []mongo.IndexModel{
        {
            Keys: bson.D{{Key: "timestamp", Value: 1}},
        },
        {
            Keys: bson.D{{Key: "session_id", Value: 1}},
        },
        {
            Keys: bson.D{{Key: "user_id", Value: 1}},
        },
        {
            Keys: bson.D{{Key: "action", Value: 1}},
        },
    }

    _, err := als.collection.Indexes().CreateMany(ctx, indexes)
    return err
}

func (als *AuditLogStore) LogAction(ctx context.Context, log *AuditLog) error {
    log.LogID = generateUUID()
    log.Timestamp = time.Now()

    _, err := als.collection.InsertOne(ctx, log)
    if err != nil {
        return fmt.Errorf("failed to log action: %w", err)
    }

    return nil
}

func (als *AuditLogStore) GetSessionLogs(ctx context.Context, sessionID string) ([]AuditLog, error) {
    cursor, err := als.collection.Find(
        ctx,
        bson.M{"session_id": sessionID},
        options.Find().SetSort(bson.M{"timestamp": -1}),
    )
    if err != nil {
        return nil, err
    }

    var logs []AuditLog
    if err := cursor.All(ctx, &logs); err != nil {
        return nil, err
    }

    return logs, nil
}

func (als *AuditLogStore) QuerySecurityEvents(ctx context.Context, startTime, endTime time.Time) ([]AuditLog, error) {
    cursor, err := als.collection.Find(
        ctx,
        bson.M{
            "timestamp": bson.M{
                "$gte": startTime,
                "$lte": endTime,
            },
            "security_flags": bson.M{"$exists": true, "$ne": bson.A{}},
        },
        options.Find().SetSort(bson.M{"timestamp": -1}),
    )
    if err != nil {
        return nil, err
    }

    var logs []AuditLog
    if err := cursor.All(ctx, &logs); err != nil {
        return nil, err
    }

    return logs, nil
}
```

### **Fase 5: Query Builders & Abstrações**

**Duração**: 5 dias

**Deliverables**:

- [ ] Query builders para cada operação comum
- [ ] Pipeline builders para aggregation
- [ ] Error handling consistente
- [ ] Testes de operações críticas

**Código de Exemplo**:

```go
// pkg/storage/query_builder.go
package storage

import (
    "context"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
)

type QueryBuilder struct {
    db *mongo.Database
}

func NewQueryBuilder(db *mongo.Database) *QueryBuilder {
    return &QueryBuilder{db: db}
}

// Busca vetorial com filtro de namespace obrigatório
func (qb *QueryBuilder) VectorSearch(ctx context.Context, embedding []float32, namespace string, k int) ([]Document, error) {
    collection := qb.db.Collection("documents")

    pipeline := mongo.Pipeline{
        bson.EM{
            "$search": bson.M{
                "cosmosSearch": bson.M{
                    "vector": embedding,
                    "k": k,
                    "similarityMetric": "cosine",
                },
            },
        },
        // OBRIGATÓRIO: Filtro de namespace
        bson.EM{
            "$match": bson.M{
                "namespace_id": namespace,
                "visibility": "public",
            },
        },
        bson.EM{
            "$addFields": bson.M{
                "score": bson.M{"$meta": "searchScore"},
            },
        },
    }

    cursor, err := collection.Aggregate(ctx, pipeline)
    if err != nil {
        return nil, err
    }
    defer cursor.Close(ctx)

    var docs []Document
    if err := cursor.All(ctx, &docs); err != nil {
        return nil, err
    }

    return docs, nil
}

// Contar documentos por namespace
func (qb *QueryBuilder) CountByNamespace(ctx context.Context, namespace string) (int64, error) {
    collection := qb.db.Collection("documents")
    return collection.CountDocuments(ctx, bson.M{"namespace_id": namespace})
}

// Atualizar metadados de documento
func (qb *QueryBuilder) UpdateMetadata(ctx context.Context, docID string, metadata map[string]interface{}) error {
    collection := qb.db.Collection("documents")
    _, err := collection.UpdateOne(
        ctx,
        bson.M{"_id": docID},
        bson.M{"$set": bson.M{"metadata": metadata}},
    )
    return err
}
```

## Garantias de Segurança

| Requisito                   | Implementação                                          |
| :-------------------------- | :----------------------------------------------------- |
| **Isolamento Multi-tenant** | Filtro `namespace_id` obrigatório em TODA query        |
| **Atomicidade**             | Vetor + metadados no mesmo documento BSON              |
| **Imutabilidade de Logs**   | Insert-only no `audit_logs`, sem updates               |
| **Criptografia**            | MongoDB Atlas: AES-256 em repouso, TLS 1.3 em trânsito |
| **Backup**                  | Snapshots contínuos com retenção 90 dias               |

## Métricas de Sucesso

- Latência de vector search <300ms para 1M+ documentos
- Throughput de batch insert: 10K docs/segundo
- TTL de sessão: 30 dias exato
- 99.99% availability com Multi-AZ
- 100% isolamento de namespace (zero vazamento)

---

## External Linking

| Concept           | Resource                                                 | Link                                                                                                       |
| ----------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **BSON Spec**     | Binary JSON Specification                                | [bsonspec.org/](https://bsonspec.org/)                                                                     |
| **MongoDB Atlas** | Atlas Vector Search Documentation                        | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **HNSW**          | Efficient and robust approximate nearest neighbor search | [arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320)                                               |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
