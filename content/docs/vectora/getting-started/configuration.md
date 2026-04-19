---
title: Configuração
slug: configuration
date: "2026-04-19T08:15:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - configuration
  - yaml
  - environment
  - vectora
  - setup
---

{{< lang-toggle >}}

## Visão Geral

A configuração do Vectora é controlada por:

1. **`vectora.config.yaml`** — Configuração do projeto (local)
2. **Variáveis de Ambiente** — Chaves e credenciais (global)
3. **CLI Commands** — Configuração dinâmica via terminal

---

## Arquivo `vectora.config.yaml`

Criado automaticamente com `vectora init`, este arquivo controla o comportamento do agente.

### Estrutura Completa

```yaml
# Metadados do Projeto
project:
  name: "Meu Projeto"
  id: "proj_auth_service"
  type: "codebase" # ou 'documentation', 'api'
  description: "Backend de autenticação em Go"

# Configuração de Namespace e Segurança
namespace:
  id: "backend" # Isolamento lógico
  trust_folder: "." # Raiz permitida para operações
  visibility: "private" # 'private', 'team', 'public'

# Providers de IA (Stack Curada)
providers:
  embedding:
    provider: "voyage"
    model: "voyage-4" # ou fallback: "gemini-embedding-2"
    dimension: 1024
    batch_size: 32

  reranker:
    enabled: true
    provider: "voyage" # ou "cohere", "local-bge"
    model: "voyage-rerank-2.5"

  llm:
    primary:
      provider: "gemini"
      model: "gemini-3-flash"
      temperature: 0.1
      max_tokens: 4096
    fallback:
      - provider: "openai"
        model: "gpt-4o"
      - provider: "local"
        model: "qwen3-1.7b-instruct"

# Context Engine (RAG Inteligente)
context_engine:
  strategy: "auto" # ou 'semantic', 'structural', 'hybrid'
  max_depth: 3 # Para buscas multi-hop
  compaction: true
  include_ast: true # Metadados de AST
  include_dependencies: true # Grafo de imports

# Segurança (Guardian + RBAC)
security:
  guardian:
    hard_blocklist:
      - ".env*"
      - "*.key"
      - "*.pem"
      - "*.crt"
      - "node_modules/**"
      - ".git/**"
    sanitize_output: true

  rbac:
    enabled: true
    roles:
      - name: "reader"
        permissions: ["context_search", "file_read", "plan_mode"]
      - name: "contributor"
        permissions: ["context_search", "file_read", "file_write", "context_ingest"]
      - name: "admin"
        permissions: ["*"]

# Indexação (Qdrant)
indexing:
  auto_ingest: true # Monitora mudanças de arquivo
  watch_patterns:
    - "src/**/*.{ts,js,go,py}"
    - "docs/**/*.md"
  ignore_patterns:
    - "node_modules/**"
    - ".git/**"
    - "*.test.*"
  chunk_size: 512 # Tokens por chunk
  overlap: 50 # Sobreposição entre chunks

# Harness (Validação + Métricas)
harness:
  enabled: true
  validate_retrieval: true
  min_retrieval_score: 0.65
  validate_tool_calls: true

# Logging
logging:
  level: "info" # 'debug', 'info', 'warn', 'error'
  format: "json" # ou 'text'
  output: "console" # ou "file", "both"
```

---

## Variáveis de Ambiente

### Obrigatórias

```bash
GEMINI_API_KEY=sk-xxx... # Google AI Studio
VOYAGE_API_KEY=pa-xxx... # Voyage AI
```

### Opcionais

```bash
VECTORA_NAMESPACE=my-project # Sobrescreve vectora.config.yaml
VECTORA_TRUST_FOLDER=/path # Sobrescreve trust_folder
VECTORA_LOG_LEVEL=debug # 'debug', 'info', 'warn', 'error'
VECTORA_CACHE_DIR=~/.vectora # Diretório de cache
QDRANT_URL=http://localhost:6333 # Se usar Qdrant local
SUPABASE_URL=https://xxx.supabase.co # Para auth customizada
```

### Arquivo `.env`

```bash
# .env (nunca commitar!)
GEMINI_API_KEY=sk-xxx
VOYAGE_API_KEY=pa-xxx
VECTORA_NAMESPACE=backend
VECTORA_LOG_LEVEL=debug
```

Carregado automaticamente ao executar Vectora.

---

## Configuração via CLI

### Listar Configurações

```bash
vectora config list
# Output:
# GEMINI_API_KEY: ••••••••••
# VOYAGE_API_KEY: ••••••••••
# VECTORA_NAMESPACE: my-project
```

### Definir Valores

```bash
# Interativo
vectora config set GEMINI_API_KEY

# Direto
vectora config set --key GEMINI_API_KEY --value sk-xxx

# Múltiplos valores
vectora config set \
  --key VOYAGE_API_KEY --value pa-xxx \
  --key VECTORA_NAMESPACE --value backend
```

### Resetar Configuração

```bash
vectora config reset --confirm
# Remove todas as chaves locais (não afeta .env)
```

---

## Exemplos de Configuração por Caso de Uso

### Caso 1: Projeto Backend (Go/Rust)

```yaml
project:
  name: "Auth Service"
  type: "codebase"

providers:
  embedding:
    model: "voyage-4" # Especializado em código
  reranker:
    enabled: true

context_engine:
  strategy: "hybrid" # Código + documentação
  include_dependencies: true # Importante para Go imports

indexing:
  watch_patterns:
    - "src/**/*.go"
    - "internal/**/*.go"
    - "*.md"
```

### Caso 2: Documentação Técnica

```yaml
project:
  name: "Technical Docs"
  type: "documentation"

providers:
  embedding:
    model: "qwen3-embedding" # Bom para texto
  reranker:
    enabled: true

indexing:
  watch_patterns:
    - "docs/**/*.md"
    - "guides/**/*.md"
```

### Caso 3: Desenvolvimento Local (CPU Limitado)

```yaml
providers:
  embedding:
    provider: "voyage"
    fallback: "gemini" # Fallback rápido

  llm:
    primary:
      provider: "local"
      model: "qwen3-1.7b-instruct" # Rodando via ollama
    fallback:
      - provider: "gemini"
        model: "gemini-3-flash"

context_engine:
  compaction: true # Economize memória
  max_depth: 2 # Menos hops

harness:
  enabled: false # Desative métricas para ganho de speed
```

---

## Validação de Configuração

```bash
# Verificar sintaxe YAML
vectora config validate

# Output esperado:
# vectora.config.yaml is valid
# All required keys present
# Environment variables loaded
# API keys accessible
```

---

## Troubleshooting

### Erro: `Config validation failed`

**Causa**: Arquivo YAML inválido.

**Solução**: Valide em [yamllint.com](https://yamllint.com) ou use:

```bash
yamllint vectora.config.yaml
```

### Erro: `API key not found in environment`

**Causa**: Variáveis de ambiente não carregadas.

**Solução**:

```bash
# Verifique se .env está no diretório correto
ls -la .env

# Carregue manualmente
export $(cat .env | xargs)
```

### Erro: `Trust folder does not exist`

**Causa**: `trust_folder` aponta para diretório inválido.

**Solução**: Atualize em `vectora.config.yaml`:

```yaml
namespace:
  trust_folder: "." # ou caminho válido
```

---

## FAQ

**P: Posso ter múltiplas configurações para diferentes projetos?**
R: Sim. Crie um `vectora.config.yaml` em cada diretório de projeto. Vectora lê o arquivo mais próximo da raiz.

**P: Como usar modelos locais em vez de APIs?**
R: Configure `provider: "local"` e instale Ollama:

```bash
ollama pull qwen3:1.7b-instruct
# Depois configure em vectora.config.yaml
```

**P: Posso compartilhar `vectora.config.yaml`?**
R: Sim, commite no git. Nunca commite `.env` ou chaves sensíveis (use `.env.example` sem valores).

**P: Como resetar a configuração?**
R: Use `vectora config reset --confirm`, ou delete `~/.vectora/config.json`.

---

> **Próximo**: Configure sua IDE em [Quickstart MCP](./quickstart-mcp.md).

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
title: Configuration
slug: configuration
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
open: true
tags:

- ai
- configuration
- mcp
- setup
- vectora

---

title: Configuração
slug: configuration
date: "2026-04-19T08:15:00-03:00"
type: docs
sidebar:
open: true
tags:

- getting-started
- configuration
- yaml
- environment
- vectora
- setup

---

{{< lang-toggle >}}

## Visão Geral

A configuração do Vectora é controlada por:

1. **`vectora.config.yaml`** — Configuração do projeto (local)
2. **Variáveis de Ambiente** — Chaves e credenciais (global)
3. **CLI Commands** — Configuração dinâmica via terminal

---

## Arquivo `vectora.config.yaml`

Criado automaticamente com `vectora init`, este arquivo controla o comportamento do agente.

### Estrutura Completa

```yaml
# Metadados do Projeto
project:
  name: "Meu Projeto"
  id: "proj_auth_service"
  type: "codebase" # ou 'documentation', 'api'
  description: "Backend de autenticação em Go"

# Configuração de Namespace e Segurança
namespace:
  id: "backend" # Isolamento lógico
  trust_folder: "." # Raiz permitida para operações
  visibility: "private" # 'private', 'team', 'public'

# Providers de IA (Stack Curada)
providers:
  embedding:
    provider: "voyage"
    model: "voyage-4" # ou fallback: "gemini-embedding-2"
    dimension: 1024
    batch_size: 32

  reranker:
    enabled: true
    provider: "voyage" # ou "cohere", "local-bge"
    model: "voyage-rerank-2.5"

  llm:
    primary:
      provider: "gemini"
      model: "gemini-3-flash"
      temperature: 0.1
      max_tokens: 4096
    fallback:
      - provider: "openai"
        model: "gpt-4o"
      - provider: "local"
        model: "qwen3-1.7b-instruct"

# Context Engine (RAG Inteligente)
context_engine:
  strategy: "auto" # ou 'semantic', 'structural', 'hybrid'
  max_depth: 3 # Para buscas multi-hop
  compaction: true
  include_ast: true # Metadados de AST
  include_dependencies: true # Grafo de imports

# Segurança (Guardian + RBAC)
security:
  guardian:
    hard_blocklist:
      - ".env*"
      - "*.key"
      - "*.pem"
      - "*.crt"
      - "node_modules/**"
      - ".git/**"
    sanitize_output: true

  rbac:
    enabled: true
    roles:
      - name: "reader"
        permissions: ["context_search", "file_read", "plan_mode"]
      - name: "contributor"
        permissions: ["context_search", "file_read", "file_write", "context_ingest"]
      - name: "admin"
        permissions: ["*"]

# Indexação (Qdrant)
indexing:
  auto_ingest: true # Monitora mudanças de arquivo
  watch_patterns:
    - "src/**/*.{ts,js,go,py}"
    - "docs/**/*.md"
  ignore_patterns:
    - "node_modules/**"
    - ".git/**"
    - "*.test.*"
  chunk_size: 512 # Tokens por chunk
  overlap: 50 # Sobreposição entre chunks

# Harness (Validação + Métricas)
harness:
  enabled: true
  validate_retrieval: true
  min_retrieval_score: 0.65
  validate_tool_calls: true

# Logging
logging:
  level: "info" # 'debug', 'info', 'warn', 'error'
  format: "json" # ou 'text'
  output: "console" # ou "file", "both"
```

---

## Variáveis de Ambiente

### Obrigatórias

```bash
GEMINI_API_KEY=sk-xxx... # Google AI Studio
VOYAGE_API_KEY=pa-xxx... # Voyage AI
```

### Opcionais

```bash
VECTORA_NAMESPACE=my-project # Sobrescreve vectora.config.yaml
VECTORA_TRUST_FOLDER=/path # Sobrescreve trust_folder
VECTORA_LOG_LEVEL=debug # 'debug', 'info', 'warn', 'error'
VECTORA_CACHE_DIR=~/.vectora # Diretório de cache
QDRANT_URL=http://localhost:6333 # Se usar Qdrant local
SUPABASE_URL=https://xxx.supabase.co # Para auth customizada
```

### Arquivo `.env`

```bash
# .env (nunca commitar!)
GEMINI_API_KEY=sk-xxx
VOYAGE_API_KEY=pa-xxx
VECTORA_NAMESPACE=backend
VECTORA_LOG_LEVEL=debug
```

Carregado automaticamente ao executar Vectora.

---

## Configuração via CLI

### Listar Configurações

```bash
vectora config list
# Output:
# GEMINI_API_KEY: ••••••••••
# VOYAGE_API_KEY: ••••••••••
# VECTORA_NAMESPACE: my-project
```

### Definir Valores

```bash
# Interativo
vectora config set GEMINI_API_KEY

# Direto
vectora config set --key GEMINI_API_KEY --value sk-xxx

# Múltiplos valores
vectora config set \
  --key VOYAGE_API_KEY --value pa-xxx \
  --key VECTORA_NAMESPACE --value backend
```

### Resetar Configuração

```bash
vectora config reset --confirm
# Remove todas as chaves locais (não afeta .env)
```

---

## Exemplos de Configuração por Caso de Uso

### Caso 1: Projeto Backend (Go/Rust)

```yaml
project:
  name: "Auth Service"
  type: "codebase"

providers:
  embedding:
    model: "voyage-4" # Especializado em código
  reranker:
    enabled: true

context_engine:
  strategy: "hybrid" # Código + documentação
  include_dependencies: true # Importante para Go imports

indexing:
  watch_patterns:
    - "src/**/*.go"
    - "internal/**/*.go"
    - "*.md"
```

### Caso 2: Documentação Técnica

```yaml
project:
  name: "Technical Docs"
  type: "documentation"

providers:
  embedding:
    model: "qwen3-embedding" # Bom para texto
  reranker:
    enabled: true

indexing:
  watch_patterns:
    - "docs/**/*.md"
    - "guides/**/*.md"
```

### Caso 3: Desenvolvimento Local (CPU Limitado)

```yaml
providers:
  embedding:
    provider: "voyage"
    fallback: "gemini" # Fallback rápido

  llm:
    primary:
      provider: "local"
      model: "qwen3-1.7b-instruct" # Rodando via ollama
    fallback:
      - provider: "gemini"
        model: "gemini-3-flash"

context_engine:
  compaction: true # Economize memória
  max_depth: 2 # Menos hops

harness:
  enabled: false # Desative métricas para ganho de speed
```

---

## Validação de Configuração

```bash
# Verificar sintaxe YAML
vectora config validate

# Output esperado:
# vectora.config.yaml is valid
# All required keys present
# Environment variables loaded
# API keys accessible
```

---

## Troubleshooting

### Erro: `Config validation failed`

**Causa**: Arquivo YAML inválido.

**Solução**: Valide em [yamllint.com](https://yamllint.com) ou use:

```bash
yamllint vectora.config.yaml
```

### Erro: `API key not found in environment`

**Causa**: Variáveis de ambiente não carregadas.

**Solução**:

```bash
# Verifique se .env está no diretório correto
ls -la .env

# Carregue manualmente
export $(cat .env | xargs)
```

### Erro: `Trust folder does not exist`

**Causa**: `trust_folder` aponta para diretório inválido.

**Solução**: Atualize em `vectora.config.yaml`:

```yaml
namespace:
  trust_folder: "." # ou caminho válido
```

---

## FAQ

**P: Posso ter múltiplas configurações para diferentes projetos?**
R: Sim. Crie um `vectora.config.yaml` em cada diretório de projeto. Vectora lê o arquivo mais próximo da raiz.

**P: Como usar modelos locais em vez de APIs?**
R: Configure `provider: "local"` e instale Ollama:

```bash
ollama pull qwen3:1.7b-instruct
# Depois configure em vectora.config.yaml
```

**P: Posso compartilhar `vectora.config.yaml`?**
R: Sim, commite no git. Nunca commite `.env` ou chaves sensíveis (use `.env.example` sem valores).

**P: Como resetar a configuração?**
R: Use `vectora config reset --confirm`, ou delete `~/.vectora/config.json`.

---

> **Próximo**: Configure sua IDE em [Quickstart MCP](./quickstart-mcp.md).

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_

{{< lang-toggle >}}
