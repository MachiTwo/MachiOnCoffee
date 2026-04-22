---
title: "Vectora Local Storage: Hybrid Cache Architecture"
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
{{< section-toggle >}}

Vectora implements a two-tier cache system to optimize performance and persistence, ensuring ultra-fast access to frequent data and durability for session states.

**Status**: Design & Implementation Plan
**Date**: 2026-04-21
**Architecture**: BadgerDB (L2) + LRU+TTL (L1)
**Target**: Session persistence, search cache, embedding storage

---

## Executive Summary

Vectora implements a **two-tier cache system** for optimal performance and persistence:

- **L1: LRU+TTL (In-Memory)** - Hot cache for ultra-fast access
- **L2: BadgerDB (Persistent)** - Cold storage with automatic recovery

This hybrid approach provides:

- **Sub-millisecond latency** for frequently accessed data
- **Session persistence** across restarts
- **Automatic promotion** from disk to memory
- **Graceful degradation** if BadgerDB unavailable

---

## Architecture Overview

### Multi-Tier Cache Strategy

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

## Storage Locations

### Platform-Specific Paths

```text
WINDOWS:
  %APPDATA%\Vectora\cache\
  └── C:\Users\{username}\AppData\Roaming\Vectora\cache\
      ├── .badgerdb/ (BadgerDB directory)
      │ ├── MANIFEST
      │ ├── 000001.sst
      │ └── ...
      ├── metadata.json (Index metadata)
      ├── sessions.json (Snapshot of active sessions)
      └── config.yaml (User preferences)

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

### Why Roaming Directory?

- **Windows**: `%APPDATA%` is synced with OneDrive/cloud by default
- **Linux**: `~/.config/` follows XDG Base Directory specification
- **macOS**: `~/Library/Preferences/` is standard for app data
- **Cross-platform**: Same structure, different base paths

---

## Cache Data Types

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

**Stored Items:**

| Item Type      | TTL    | Max Count | Use Case                |
| -------------- | ------ | --------- | ----------------------- |
| Search Results | 5 min  | 100       | Recent queries          |
| Embeddings     | 10 min | 500       | Frequently used vectors |
| Session State  | 1 hour | 10        | Active user sessions    |
| Code Chunks    | 15 min | 300       | File analysis cache     |
| Index Metadata | 1 hour | 1         | Current index state     |

### L2: BadgerDB Persistent Storage

```go
type L2CacheItem struct {
    Key string
    Value []byte // Compressed
    TTL time.Duration
    ExpiresAt time.Time
    CreatedAt time.Time
    LastAccess time.Time
    Tags []string // For filtering
    Compressed bool
}

type BadgerDBCache struct {
    db *badger.DB
    opts BadgerOptions
}
```

**Storage Categories:**

| Category   | TTL | Compression | Index     | Use Case        |
| ---------- | --- | ----------- | --------- | --------------- |
| embeddings | 7d  | Yes (LZ4)   | timestamp | Search history  |
| sessions   | 24h | Yes         | user_id   | User sessions   |
| chunks     | 24h | Yes         | file_path | Code chunks     |
| queries    | 48h | Yes         | hash      | Query cache     |
| metadata   | 7d  | No          | key       | System metadata |

---

## Implementation Details

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

## Configuration

### Environment Variables

```bash
# Cache sizing
VECTORA_CACHE_L1_SIZE=1000 # LRU max items
VECTORA_CACHE_L1_TTL=5m # LRU TTL
VECTORA_CACHE_L2_DIR=~/.config/vectora/cache

# BadgerDB options
VECTORA_CACHE_BADGER_LOG_SIZE=67108864 # 64MB value log
VECTORA_CACHE_BADGER_COMPRESSION=true
VECTORA_CACHE_BADGER_TTL_CHECK=1h

# Cache behavior
VECTORA_CACHE_ENABLE_L1=true
VECTORA_CACHE_ENABLE_L2=true
VECTORA_CACHE_AUTOPROMOTION=true
```

### YAML Configuration

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
      blockCacheSize: 0 # Use system memory
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

## Performance Characteristics

### Latency Profile

```text
L1 Cache Hit: 0.1-1ms (sub-millisecond)
L2 Cache Hit: 10-50ms (disk I/O)
L2 Compression: 2-5ms (LZ4 codec)
L3 Backend: 50-500ms (API call)

Typical Distribution:
- 85% L1 hits (0.1-1ms)
- 12% L2 hits (10-50ms)
- 3% L3 misses (50-500ms)

Average Latency: ~5ms
```

### Memory Usage

```text
L1 Cache (1000 items):
- Per item: ~200 bytes overhead + value size
- Typical: 50-100 MB (depending on payload)

L2 Cache (BadgerDB):
- Depends on stored data
- Typical: 50-500 MB for 24h history
- Automatic compression: 70-80% size reduction
```

### Disk I/O

```text
BadgerDB Operations:
- Random read: 10-30ms (SSD), 50-100ms (HDD)
- Sequential read: 1-5ms
- Write: 5-20ms (with durability)
- Batch write: 2-10ms per item

Optimization:
- Value log file size: 64MB (balance between size and performance)
- Block cache: Auto-managed
- Index cache: Auto-managed
```

---

## Eviction & Cleanup

### L1 Eviction Strategy

```text
LRU + TTL Hybrid:
1. Check TTL expiration (every 1 minute)
2. If full, evict least recently used
3. Promote frequently accessed items

Priority:
- Session state (keep longest)
- Recent searches (medium priority)
- Embeddings (low priority, can recompute)
```

### L2 Cleanup

```text
BadgerDB TTL:
- Items automatically expire per TTL
- Background garbage collection every 1 hour
- Value log compaction every 24 hours
- Automatic cleanup on startup
```

---

## Failure Modes & Recovery

### L1 Failure (In-Memory)

```text
Scenario: L1 cache lost (e.g., restart)
Impact: 15-20% performance degradation temporarily
Recovery: L2 automatically restores within 10 seconds
User Impact: Minimal (fallback to L2 cache)
```

### L2 Failure (Disk)

```text
Scenario: BadgerDB corrupted
Impact: Cache loss, fallback to L3 (backend API)
Recovery:
  1. Delete corrupted .badgerdb directory
  2. Restart application
  3. Automatic rebuild from backend
Mitigation: Enable backup before write-heavy operations
```

### Both Failures

```text
Scenario: Both L1 and L2 unavailable
Impact: No caching, direct backend queries
Latency: 50-500ms per request (no cache)
Recovery: Rebuild caches as queries come in
User Impact: Noticeable slowdown but functional
```

---

## Testing Strategy

### Unit Tests

```go
TestLRUSet() // Set items in LRU
TestLRUGet() // Retrieve items
TestLRUExpiration() // TTL expiration
TestLRUEviction() // LRU eviction
TestBadgerSet() // Set in BadgerDB
TestBadgerTTL() // TTL in BadgerDB
TestHybridPromotion() // L2 to L1 promotion
TestHybridFallback() // L1 miss → L2 fallback
```

### Integration Tests

```go
TestCacheUnderLoad() // 1000 concurrent requests
TestRecoveryAfterCrash()
TestCacheConsistency()
TestCachePerformance()
```

---

## Monitoring & Observability

### Metrics to Track

```text
L1 Cache:
- Hit rate (target: >80%)
- Miss rate
- Eviction rate
- Average latency
- Max latency (p99)

L2 Cache:
- Size (bytes)
- Item count
- Compression ratio
- GC frequency
- Compaction time

System:
- Memory usage (L1)
- Disk usage (L2)
- CPU time (compression)
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

## Migration Path

### Phase 1: In-Memory Only (Current)

- Use only LRU+TTL
- No persistence
- Perfect for single-instance testing

### Phase 2: Add BadgerDB (Next)

- Introduce L2 cache
- Automatic persistence
- Improved recovery

### Phase 3: Distributed Cache (Future)

- Redis for multi-instance
- Cache invalidation protocol
- Distributed session storage

---

## Dependencies

```go
go get github.com/dgraph-io/badger/v3
// Size: ~1.5MB
// Pure Go, no C dependencies
// License: Apache 2.0
```

---

## Trade-offs Summary

| Aspect      | LRU+TTL | BadgerDB | Hybrid      |
| ----------- | ------- | -------- | ----------- |
| Speed       | High    | Medium   | High        |
| Persistence | No      | Yes      | Yes         |
| Memory      | Low     | Medium   | Medium      |
| Complexity  | Low     | Medium   | Medium-High |
| Recovery    | Poor    | Good     | Excellent   |

---

## Conclusion

The **Hybrid Cache Architecture** (BadgerDB + LRU+TTL) provides Vectora with:

1. Ultra-fast in-memory access (L1)
2. Persistent storage with TTL (L2)
3. Graceful degradation on failures
4. Automatic promotion/demotion
5. Cross-platform roaming support
6. Zero external service dependencies

This design scales from single-instance development to multi-instance production deployments.

---

## Implementation Checklist

- [ ] Create `internal/cache/interface.go` (interfaces)
- [ ] Implement `internal/cache/lru.go` (L1)
- [ ] Implement `internal/cache/badger.go` (L2)
- [ ] Implement `internal/cache/hybrid.go` (orchestration)
- [ ] Add platform-specific path resolution
- [ ] Add environment variable configuration
- [ ] Add health check endpoint
- [ ] Add metrics collection
- [ ] Write comprehensive tests
- [ ] Add documentation
- [ ] Integration with main server
- [ ] Benchmark performance

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
