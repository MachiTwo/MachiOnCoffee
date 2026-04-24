---
title: "Armazenamento Local do Vectora: Arquitetura de Cache Híbrido"
slug: local-storage
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - config
  - embeddings
  - errors
  - integration
  - persistence
  - protocol
  - state
  - system
  - vectora
  - yaml
---

{{< lang-toggle >}}

O Vectora implementa um sistema de cache de duas camadas para otimizar o desempenho e a persistência, garantindo acesso ultra-rápido a dados frequentes e durabilidade para estados de sessão.

**Status**: Plano de Design e Implementação
**Date**: 2026-04-21
**Architecture**: BadgerDB (L2) + LRU+TTL (L1)
**Target**: Session persistence, search cache, embedding storage

---

## Sumário Executivo

O Vectora implementa um **sistema de cache de duas camadas** para desempenho e persistência ideais:

- **L1: LRU+TTL (Em Memória)** - Cache "quente" para acesso ultra-rápido.
- **L2: BadgerDB (Persistente)** - Armazenamento "frio" com recuperação automática.

Esta abordagem híbrida oferece:

- **Latência sub-milissegundo** para dados acessados frequentemente.
- **Persistência de sessão** entre reinicializações.
- **Promoção automática** do disco para a memória.
- **Degradação graciosa** se o BadgerDB estiver indisponível.

---

## Visão Geral da Arquitetura

### Estratégia de Cache Multi-Camada

```text
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│ L1: In-Memory LRU Cache (5 min TTL) │
│ ├── Embedding vectors │
│ ├── Query results (1000 items max) │
│ ├── Session state │
│ └── Recent searches │
│ HIT RATE: ~85% (typical) │
└─────────────────────────────────────────┘
     │ MISS
     ▼
┌─────────────────────────────────────────┐
│ L2: BadgerDB (24 hour TTL) │
│ ├── Persistent storage │
│ ├── Automatic compression │
│ ├── Index by timestamp │
│ └── Full search history │
│ LATENCY: 10-50ms │
└─────────────────────────────────────────┘
     │ MISS
     ▼
┌─────────────────────────────────────────┐
│ L3: Backend (API/Database) │
│ ├── Re-compute embeddings │
│ ├── Fetch from database │
│ └── Update L1 & L2 │
│ LATENCY: 50-500ms │
└─────────────────────────────────────────┘
```

---

## Locais de Armazenamento

### Caminhos Específicos por Plataforma

```text
WINDOWS:
  %APPDATA%\Vectora\cache\
  └── C:\Users\{username}\AppData\Roaming\Vectora\cache\
      ├── .badgerdb/ (Diretório BadgerDB)
      │ ├── MANIFEST
      │ ├── 000001.sst
      │ └── ...
      ├── metadata.json (Metadados do índice)
      ├── sessions.json (Snapshot de sessões ativas)
      └── config.yaml (Preferências do usuário)

LINUX:
  ~/.config/vectora/cache/
  ├── .badgerdb/
  ├── metadata.json
  ├── sessions.json
  └── config.yaml

MACOS:
  ~/Library/Preferences/Vectora/cache/
  ├── .badgerdb/
  ├── metadata.json
  ├── sessions.json
  └── config.yaml
```

### Por que o Diretório Roaming?

- **Windows**: `%APPDATA%` é sincronizado com OneDrive/nuvem por padrão.
- **Linux**: `~/.config/` segue a especificação XDG Base Directory.
- **macOS**: `~/Library/Preferences/` é o padrão para dados de aplicativos.
- **Multiplataforma**: Mesma estrutura, diferentes caminhos base.

---

## Tipos de Dados de Cache

### L1: In-Memory LRU+TTL

```go
type L1CacheItem struct {
    Key string
    Value interface{}
    TTL time.Duration
    CreatedAt time.Time
    AccessedAt time.Time
    Hits int64
}

type L1Cache struct {
    items map[string]*L1CacheItem
    maxSize int // Default: 1000
    mu sync.RWMutex
}
```

**Itens Armazenados:**

| Tipo de Item        | TTL    | Contagem Máx | Caso de Uso               |
| ------------------- | ------ | ------------ | ------------------------- |
| Resultados de Busca | 5 min  | 100          | Consultas recentes        |
| Embeddings          | 10 min | 500          | Vetores frequentes        |
| Estado de Sessão    | 1 hora | 10           | Sessões de usuário ativas |
| Chunks de Código    | 15 min | 300          | Cache de análise de files |
| Metadados do Índice | 1 hora | 1            | Estado atual do índice    |

### L2: Armazenamento Persistente BadgerDB

```go
type L2CacheItem struct {
    Key string
    Value []byte // Comprimido
    TTL time.Duration
    ExpiresAt time.Time
    CreatedAt time.Time
    LastAccess time.Time
    Tags []string // Para filtragem
    Compressed bool
}

type BadgerDBCache struct {
    db *badger.DB
    opts BadgerOptions
}
```

**Categorias de Armazenamento:**

| Categoria  | TTL | Compressão | Índice    | Caso de Uso          |
| ---------- | --- | ---------- | --------- | -------------------- |
| embeddings | 7d  | Sim (LZ4)  | timestamp | Histórico de busca   |
| sessions   | 24h | Sim        | user_id   | Sessões de usuário   |
| chunks     | 24h | Sim        | file_path | Chunks de código     |
| queries    | 48h | Sim        | hash      | Cache de consultas   |
| metadata   | 7d  | Não        | key       | Metadados do sistema |

---

## Detalhes de Implementação

### 1. LRU Cache (L1)

```go
// internal/cache/lru.go

package cache

import (
    "sync"
    "time"
)

type LRUCache struct {
    items map[string]*CacheItem
    order []*CacheItem // LRU order
    maxSize int
    mu sync.RWMutex
}

type CacheItem struct {
    Key string
    Value interface{}
    TTL time.Duration
    CreatedAt time.Time
    AccessedAt time.Time
    Hits int64
}

func NewLRUCache(maxSize int) *LRUCache {
    return &LRUCache{
        items: make(map[string]*CacheItem),
        order: make([]*CacheItem, 0, maxSize),
        maxSize: maxSize,
    }
}

func (lru *LRUCache) Set(key string, value interface{}, ttl time.Duration) error {
    lru.mu.Lock()
    defer lru.mu.Unlock()

    if len(lru.items) >= lru.maxSize {
        lru.evict()
    }

    item := &CacheItem{
        Key: key,
        Value: value,
        TTL: ttl,
        CreatedAt: time.Now(),
        AccessedAt: time.Now(),
    }

    lru.items[key] = item
    lru.order = append(lru.order, item)

    return nil
}

func (lru *LRUCache) Get(key string) (interface{}, error) {
    lru.mu.RLock()
    defer lru.mu.RUnlock()

    item, exists := lru.items[key]
    if !exists {
        return nil, ErrNotFound
    }

    if time.Since(item.CreatedAt) > item.TTL {
        return nil, ErrExpired
    }

    item.AccessedAt = time.Now()
    item.Hits++

    return item.Value, nil
}

func (lru *LRUCache) evict() {
    if len(lru.order) == 0 {
        return
    }

    removed := lru.order[0]
    delete(lru.items, removed.Key)
    lru.order = lru.order[1:]
}

func (lru *LRUCache) Stats() CacheStats {
    lru.mu.RLock()
    defer lru.mu.RUnlock()

    return CacheStats{
        Items: len(lru.items),
        MaxSize: lru.maxSize,
        HitRate: lru.calculateHitRate(),
    }
}
```

### 2. BadgerDB Cache (L2)

```go
// internal/cache/badger.go

package cache

import (
    "encoding/json"
    "time"

    "github.com/dgraph-io/badger/v3"
)

type BadgerDBCache struct {
    db *badger.DB
    opts *BadgerOptions
}

type BadgerOptions struct {
    Dir string
    ValueLogFileSize int64
    Compression bool
    TTLCheckFreq time.Duration
}

func NewBadgerDBCache(opts *BadgerOptions) (*BadgerDBCache, error) {
    badgerOpts := badger.DefaultOptions(opts.Dir)
    badgerOpts.ValueLogFileSize = opts.ValueLogFileSize

    db, err := badger.Open(badgerOpts)
    if err != nil {
        return nil, err
    }

    return &BadgerDBCache{
        db: db,
        opts: opts,
    }, nil
}

func (b *BadgerDBCache) Set(category string, key string, value interface{}, ttl time.Duration) error {
    data, err := json.Marshal(value)
    if err != nil {
        return err
    }

    fullKey := b.makeKey(category, key)
    entry := badger.NewEntry([]byte(fullKey), data)

    if ttl > 0 {
        entry = entry.WithTTL(ttl)
    }

    return b.db.Update(func(txn *badger.Txn) error {
        return txn.SetEntry(entry)
    })
}

func (b *BadgerDBCache) Get(category string, key string) ([]byte, error) {
    fullKey := b.makeKey(category, key)
    var value []byte

    err := b.db.View(func(txn *badger.Txn) error {
        item, err := txn.Get([]byte(fullKey))
        if err != nil {
            return err
        }

        return item.Value(func(val []byte) error {
            value = val
            return nil
        })
    })

    return value, err
}

func (b *BadgerDBCache) Delete(category string, key string) error {
    fullKey := b.makeKey(category, key)
    return b.db.Update(func(txn *badger.Txn) error {
        return txn.Delete([]byte(fullKey))
    })
}

func (b *BadgerDBCache) DeleteByCategory(category string) error {
    prefix := category + ":"

    return b.db.Update(func(txn *badger.Txn) error {
        opts := badger.DefaultIteratorOptions
        opts.Prefix = []byte(prefix)

        it := txn.NewIterator(opts)
        defer it.Close()

        for it.Seek([]byte(prefix)); it.Valid(); it.Next() {
            if err := txn.Delete(it.Item().Key()); err != nil {
                return err
            }
        }

        return nil
    })
}

func (b *BadgerDBCache) Close() error {
    return b.db.Close()
}

func (b *BadgerDBCache) makeKey(category, key string) string {
    return category + ":" + key
}

func (b *BadgerDBCache) Stats() map[string]interface{} {
    return map[string]interface{}{
        "size": b.db.Size(),
    }
}
```

### 3. Hybrid Cache (Orchestration)

```go
// internal/cache/hybrid.go

package cache

import (
    "context"
    "time"
)

type HybridCache struct {
    l1 *LRUCache
    l2 *BadgerDBCache
}

func NewHybridCache(lruSize int, badgerDir string) (*HybridCache, error) {
    l1 := NewLRUCache(lruSize)

    badgerOpts := &BadgerOptions{
        Dir: badgerDir,
        ValueLogFileSize: 64 * 1024 * 1024, // 64MB
        Compression: true,
        TTLCheckFreq: 1 * time.Hour,
    }

    l2, err := NewBadgerDBCache(badgerOpts)
    if err != nil {
        return nil, err
    }

    return &HybridCache{
        l1: l1,
        l2: l2,
    }, nil
}

func (h *HybridCache) Set(ctx context.Context, category, key string, value interface{}, ttl time.Duration) error {
    // L1: Always set in memory
    if err := h.l1.Set(key, value, ttl); err != nil {
        return err
    }

    // L2: Also set in persistent storage
    go func() {
        _ = h.l2.Set(category, key, value, ttl)
    }()

    return nil
}

func (h *HybridCache) Get(ctx context.Context, category, key string) (interface{}, error) {
    // Try L1 first (fast path)
    if val, err := h.l1.Get(key); err == nil {
        return val, nil
    }

    // Fall back to L2 (cold cache)
    data, err := h.l2.Get(category, key)
    if err != nil {
        return nil, err
    }

    // Promote to L1 for next access
    go func() {
        var val interface{}
        if err := json.Unmarshal(data, &val); err == nil {
            _ = h.l1.Set(key, val, 5*time.Minute)
        }
    }()

    return data, nil
}

func (h *HybridCache) Delete(ctx context.Context, category, key string) error {
    h.l1.Delete(key)
    return h.l2.Delete(category, key)
}

func (h *HybridCache) Close() error {
    return h.l2.Close()
}

func (h *HybridCache) Stats() CacheStats {
    l1Stats := h.l1.Stats()
    l2Stats := h.l2.Stats()

    return CacheStats{
        L1Items: l1Stats.Items,
        L1HitRate: l1Stats.HitRate,
        L2Size: l2Stats["size"].(int64),
    }
}
```

---

## Configuração

### Variáveis de Ambiente

```bash
# Dimensionamento do cache
VECTORA_CACHE_L1_SIZE=1000 # Máximo de itens LRU
VECTORA_CACHE_L1_TTL=5m # TTL do LRU
VECTORA_CACHE_L2_DIR=~/.config/vectora/cache

# Opções do BadgerDB
VECTORA_CACHE_BADGER_LOG_SIZE=67108864 # Log de valores de 64MB
VECTORA_CACHE_BADGER_COMPRESSION=true
VECTORA_CACHE_BADGER_TTL_CHECK=1h

# Comportamento do cache
VECTORA_CACHE_ENABLE_L1=true
VECTORA_CACHE_ENABLE_L2=true
VECTORA_CACHE_AUTOPROMOTION=true
```

### Configuração YAML

```yaml
cache:
  l1:
    enabled: true
    maxSize: 1000
    ttl: 5m

  l2:
    enabled: true
    dir: ~/.config/vectora/cache
    options:
      valueLogFileSize: 67108864 # 64MB
      compression: true
      blockCacheSize: 0 # Usar memória do sistema
      indexCacheSize: 0

  categories:
    embeddings:
      ttl: 7d
      compress: true
    sessions:
      ttl: 24h
      compress: true
    chunks:
      ttl: 24h
      compress: true
    queries:
      ttl: 48h
      compress: true
```

---

## Características de Desempenho

### Perfil de Latência

```text
Hit no Cache L1: 0.1-1ms (sub-millisecond)
Hit no Cache L2: 10-50ms (I/O de disco)
Compressão L2: 2-5ms (codec LZ4)
L3 Backend: 50-500ms (chamada de API)

Distribuição Típica:
- 85% hits L1 (0.1-1ms)
- 12% hits L2 (10-50ms)
- 3% misses L3 (50-500ms)

Latência Média: ~5ms
```

### Uso de Memória

```text
Cache L1 (1000 itens):
- Por item: ~200 bytes overhead + tamanho do valor
- Típico: 50-100 MB (dependendo do payload)

Cache L2 (BadgerDB):
- Depende dos dados armazenados
- Típico: 50-500 MB para 24h de histórico
- Compressão automática: 70-80% de redução de tamanho
```

### I/O de Disco

```text
Operações BadgerDB:
- Leitura aleatória: 10-30ms (SSD), 50-100ms (HDD)
- Leitura sequencial: 1-5ms
- Escrita: 5-20ms (com durabilidade)
- Escrita em lote: 2-10ms por item

Otimização:
- Tamanho do log de valores: 64MB (equilíbrio entre tamanho e desempenho)
- Block cache: Gerenciado automaticamente
- Index cache: Gerenciado automaticamente
```

---

## Evicção e Limpeza

### Estratégia de Evicção L1

```text
Híbrido LRU + TTL:
1. Verifica expiração de TTL (a cada 1 minuto)
2. Se cheio, remove o item menos recentemente usado (LRU)
3. Promove itens acessados frequentemente

Prioridade:
- Estado da sessão (manter por mais tempo)
- Buscas recentes (prioridade média)
- Embeddings (baixa prioridade, podem ser recomputados)
```

### Limpeza L2

```text
TTL do BadgerDB:
- Itens expiram automaticamente conforme o TTL
- Coleta de lixo em background a cada 1 hora
- Compactação do log de valores a cada 24 horas
- Limpeza automática na inicialização
```

---

## Modos de Falha e Recuperação

### Falha L1 (Em Memória)

```text
Cenário: Perda do cache L1 (ex: reinicialização)
Impacto: Degradação temporária de 15-20% no desempenho
Recuperação: L2 restaura automaticamente em até 10 segundos
Impacto ao Usuário: Mínimo (fallback para o cache L2)
```

### Falha L2 (Disco)

```text
Cenário: Corrupção do BadgerDB
Impacto: Perda do cache, fallback para L3 (API backend)
Recuperação:
  1. Deletar diretório .badgerdb corrompido
  2. Reiniciar aplicação
  3. Reconstrução automática a partir do backend
Mitigação: Habilitar backup antes de operações intensas de escrita
```

### Falha em Ambas

```text
Cenário: L1 e L2 indisponíveis
Impacto: Sem caching, consultas diretas ao backend
Latência: 50-500ms por requisição (sem cache)
Recuperação: Reconstrói os caches conforme as consultas ocorrem
Impacto ao Usuário: Lentidão perceptível, mas funcional
```

---

## Estratégia de Teste

### Testes Unitários

```go
TestLRUSet() // Definir itens no LRU
TestLRUGet() // Recuperar itens
TestLRUExpiration() // Expiração de TTL
TestLRUEviction() // Evicção LRU
TestBadgerSet() // Definir no BadgerDB
TestBadgerTTL() // TTL no BadgerDB
TestHybridPromotion() // Promoção L2 para L1
TestHybridFallback() // Miss L1 → Fallback L2
```

### Testes de Integração

```go
TestCacheUnderLoad() // 1000 requisições concorrentes
TestRecoveryAfterCrash() // Recuperação após crash
TestCacheConsistency() // Consistência do cache
TestCachePerformance() // Desempenho do cache
```

---

## Monitoramento e Observabilidade

### Métricas para Acompanhar

```text
Cache L1:
- Taxa de acerto (target: >80%)
- Taxa de erro (miss)
- Taxa de evicção
- Latência média
- Latência máxima (p99)

Cache L2:
- Tamanho (bytes)
- Contagem de itens
- Razão de compressão
- Frequência de GC
- Tempo de compactação

Sistema:
- Uso de memória (L1)
- Uso de disco (L2)
- Tempo de CPU (compressão)
```

### Health Checks

```text
// Endpoint: /health/cache
{
  "status": "healthy",
  "l1": {
    "items": 850,
    "hitRate": 0.87,
    "avgLatency": "0.8ms"
  },
  "l2": {
    "size": "124MB",
    "items": 45000,
    "compression": 0.72
  }
}
```

---

## Caminho de Migração

### Fase 1: Somente em Memória (Atual)

- Usa apenas LRU+TTL
- Sem persistência
- Ideal para testes em instância única

### Fase 2: Adição do BadgerDB (Próxima)

- Introdução do cache L2
- Persistência automática
- Melhor recuperação

### Fase 3: Cache Distribuído (Futuro)

- Redis para multi-instância
- Protocolo de invalidação de cache
- Armazenamento de sessão distribuído

---

## Dependências

```go
go get github.com/dgraph-io/badger/v3
// Tamanho: ~1.5MB
// Pure Go, sem dependências C
// Licença: Apache 2.0
```

---

## Resumo de Trade-offs

| Aspecto      | LRU+TTL | BadgerDB | Híbrido    |
| ------------ | ------- | -------- | ---------- |
| Velocidade   | Alta    | Média    | Alta       |
| Persistência | Não     | Sim      | Sim        |
| Memória      | Baixa   | Média    | Média      |
| Complexidade | Baixa   | Média    | Média-Alta |
| Recuperação  | Ruim    | Boa      | Excelente  |

---

## Conclusão

A **Arquitetura de Cache Híbrido** (BadgerDB + LRU+TTL) fornece ao Vectora:

1. Acesso ultra-rápido em memória (L1)
2. Armazenamento persistente com TTL (L2)
3. Degradação graciosa em falhas
4. Promoção/demoção automática
5. Suporte a roaming multiplataforma
6. Zero dependências de serviços externos

Este design escala desde o desenvolvimento em instância única até implantações de produção multi-instância.

---

## Checklist de Implementação

- [ ] Criar `internal/cache/interface.go` (interfaces)
- [ ] Implementar `internal/cache/lru.go` (L1)
- [ ] Implementar `internal/cache/badger.go` (L2)
- [ ] Implementar `internal/cache/hybrid.go` (orquestração)
- [ ] Adicionar resolução de caminho específico da plataforma
- [ ] Adicionar configuração de variáveis de ambiente
- [ ] Adicionar endpoint de health check
- [ ] Adicionar coleta de métricas
- [ ] Escrever testes abrangentes
- [ ] Adicionar documentação
- [ ] Integração com o servidor principal
- [ ] Benchmark de desempenho

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
