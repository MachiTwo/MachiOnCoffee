---
title: CLI
slug: cli
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

Vectora oferece uma **interface CLI completa** para configuração, indexação, e debugging. Use para automação, CI/CD, ou desenvolvimento local.

> [!TIP]
> Use `vectora --help` para ver todos os comandos, ou `vectora [command] --help` para detalhes específicos.

---

## Estrutura Geral

```bash
vectora [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

---

## Global Options

```bash
--version, -v # Mostra versão
--help, -h # Mostra ajuda
--config PATH # Caminho customizado ao vectora.config.yaml
--namespace NS # Override namespace padrão
--debug # Ativa modo debug (verbose logging)
--quiet, -q # Suprime output (exceto erros)
--json # Output em JSON (para parsing)
```

Exemplos:

```bash
vectora --version
vectora --debug index
vectora --namespace staging init
vectora --config ./custom.yaml search "query"
```

---

## Commands

### `vectora init`

Inicializa um novo projeto Vectora.

```bash
vectora init [OPTIONS]

OPTIONS:
  --name NAME # Nome do projeto (default: diretório)
  --type TYPE # Tipo: codebase|docs|hybrid (default: codebase)
  --namespace NS # Namespace customizado (default: org-project-env)
  --trust-folder PATH # Trust folder (default: .)
  --providers YAML # Config de providers (veja config docs)
```

**Exemplos**:

```bash
vectora init --name "Meu App" --type codebase
# Cria vectora.config.yaml + .vectora/

vectora init --namespace kaffyn-backend-prod --type codebase
# Cria com namespace específico
```

---

### `vectora index`

Indexa arquivos no namespace.

```bash
vectora index [OPTIONS]

OPTIONS:
  --force # Reindexar mesmo se não mudou
  --incremental # Apenas arquivos novos/modificados (default: true)
  --exclude PATTERN # Excluir globs (ex: node_modules/**)
  --include PATTERN # Incluir apenas globs (ex: src/**)
  --dry-run # Mostra o que seria indexado, sem fazer
  --progress # Mostra barra de progresso
  --watch # Fica observando mudanças (dev mode)
```

**Exemplos**:

```bash
# Indexar incremental (padrão)
vectora index

# Reindexar tudo
vectora index --force

# Apenas TypeScript
vectora index --include "**/*.ts" --include "**/*.tsx"

# Mode desenvolvimento (watch)
vectora index --watch

# Verificar o que seria indexado
vectora index --dry-run
```

---

### `vectora search`

Busca semântica pela CLI.

```bash
vectora search QUERY [OPTIONS]

OPTIONS:
  --strategy STRATEGY # semantic|structural|hybrid (default: semantic)
  --top-k NUM # Quantidade de resultados (default: 10)
  --format FORMAT # text|json|markdown (default: text)
  --include-snippets # Incluir trecho de código
  --compare-baseline # Comparar com versão anterior
```

**Exemplos**:

```bash
# Busca simples
vectora search "Como faz login?"

# Busca estrutural para relações de código
vectora search "Quem chama getUserById?" --strategy structural

# Output em JSON
vectora search "validação" --format json

# Busca com snippets de código
vectora search "middleware" --include-snippets
```

---

### `vectora analyze`

Análise profunda com LLM (Gemini).

```bash
vectora analyze QUERY [OPTIONS]

OPTIONS:
  --model MODEL # llm a usar (default: gemini-3-flash)
  --context NUM # Quantos chunks usar (default: 10)
  --output FILE # Salvar em arquivo (ex: report.md)
  --compare-baseline # Comparar com análise anterior
```

**Exemplos**:

```bash
# Análise simples
vectora analyze "Como funciona autenticação?"

# Análise profunda
vectora analyze "Revise esse código para segurança" --model gemini-pro --context 20

# Salvar em arquivo
vectora analyze "Escreva documentação de API" --output docs/api.md
```

---

### `vectora config`

Gerencia configuração.

```bash
vectora config [SUBCOMMAND]

SUBCOMMANDS:
  get KEY # Obter valor
  set KEY VALUE # Definir valor
  list # Listar tudo
  validate # Validar config atual
  reset # Reset para padrão
  show-schema # Mostrar schema YAML
```

**Exemplos**:

```bash
# Ver configuração atual
vectora config list

# Ver chave específica
vectora config get project.namespace

# Definir chave
vectora config set context_engine.strategy semantic

# Validar config
vectora config validate

# Ver schema disponível
vectora config show-schema
```

---

### `vectora namespace`

Gerenciar namespaces.

```bash
vectora namespace [SUBCOMMAND]

SUBCOMMANDS:
  create --name NS # Criar novo namespace
  delete --name NS # Deletar namespace (PERMANENTE)
  list # Listar todos os namespaces
  info --name NS # Detalhes de um namespace
  reset --name NS # Limpar chunks de um namespace
```

**Exemplos**:

```bash
# Listar namespaces
vectora namespace list

# Criar novo
vectora namespace create --name kaffyn-new-project

# Ver detalhes
vectora namespace info --name kaffyn-vectora-prod

# Limpar namespace
vectora namespace reset --name kaffyn-old-project
```

---

### `vectora mcp`

Inicia servidor MCP para Claude Code, Cursor, etc.

```bash
vectora mcp [OPTIONS]

OPTIONS:
  --port PORT # Porta (default: 9090)
  --host HOST # Host (default: localhost)
  --namespace NS # Namespace padrão
  --no-auth # Desabilitar autenticação (dev only)
```

**Exemplos**:

```bash
# Iniciar servidor
vectora mcp

# Com porta customizada
vectora mcp --port 9091

# Servidor público
vectora mcp --host 0.0.0.0 --port 9090
```

---

### `vectora server`

Inicia HTTP server completo (com UI, webhooks).

```bash
vectora server [OPTIONS]

OPTIONS:
  --port PORT # Porta (default: 3000)
  --host HOST # Host (default: localhost)
  --ui # Ativar dashboard web
  --webhooks # Ativar suporte a webhooks
  --cert FILE # Certificado SSL/TLS
  --key FILE # Chave SSL/TLS
```

**Exemplos**:

```bash
# Servidor básico
vectora server

# Com UI web
vectora server --ui

# HTTPS com certificado
vectora server --cert cert.pem --key key.pem
```

---

### `vectora auth`

Gerenciar tokens e autenticação.

```bash
vectora auth [SUBCOMMAND]

SUBCOMMANDS:
  login # Login interativo
  logout # Logout
  token create # Gerar novo token
  token list # Listar tokens
  token delete ID # Revogar token
  token validate TOKEN # Validar token
```

**Exemplos**:

```bash
# Login
vectora auth login

# Criar token com TTL
vectora auth token create --name "CI/CD" --ttl 365d

# Validar token
vectora auth token validate sk-abc123...
```

---

### `vectora logs`

Ver logs de execução.

```bash
vectora logs [OPTIONS]

OPTIONS:
  --level LEVEL # debug|info|warn|error (default: info)
  --service SERVICE # Filtrar por serviço
  --since DURATION # Últimas N horas (ex: 24h)
  --follow, -f # Stream logs em tempo real
  --format FORMAT # text|json (default: text)
```

**Exemplos**:

```bash
# Ver logs recentes
vectora logs --since 1h

# Debug logs em tempo real
vectora logs --level debug --follow

# Logs apenas de busca
vectora logs --service search --since 24h

# JSON para parsing
vectora logs --format json | jq '.[]'
```

---

### `vectora metrics`

Ver métricas de operação.

```bash
vectora metrics [OPTIONS]

OPTIONS:
  --period PERIOD # 24h|7d|30d (default: 24h)
  --export FORMAT # csv|json|prometheus (default: text)
  --output FILE # Salvar em arquivo
```

**Ejemplos**:

```bash
# Métricas do último dia
vectora metrics --period 24h

# Exportar como CSV
vectora metrics --period 7d --export csv --output metrics.csv

# Formato Prometheus
vectora metrics --export prometheus
```

---

### `vectora audit`

Ver log de auditoria (quem fez o quê).

```bash
vectora audit [OPTIONS]

OPTIONS:
  --action ACTION # Filtrar por ação (search|index|delete)
  --user USER # Filtrar por usuário
  --since DURATION # Desde quando (ex: 7d)
  --limit NUM # Limite de linhas (default: 100)
```

**Exemplos**:

```bash
# Auditoria completa
vectora audit

# Buscas dos últimos 7 dias
vectora audit --action search --since 7d

# Deletions por usuário
vectora audit --action delete --user "seu-email@company.com"
```

---

### `vectora health`

Verifica saúde do sistema.

```bash
vectora health [OPTIONS]

OPTIONS:
  --detailed # Mostrar detalhes de cada componente
  --fix # Tentar corrigir problemas
```

**Exemplos**:

```bash
# Saúde rápida
vectora health

# Com detalhes
vectora health --detailed

# Tentar corrigir
vectora health --fix
```

---

## Exit Codes

```text
0 # Sucesso
1 # Erro genérico
2 # Erro de configuração
3 # API error
4 # Autenticação falhou
5 # Namespace não encontrado
```

---

## Variáveis de Ambiente

Substitua options de CLI:

```bash
VECTORA_NAMESPACE=staging vectora search "..."
VECTORA_LOG_LEVEL=debug vectora index
VECTORA_CONFIG=./custom.yaml vectora init
VECTORA_TRUST_FOLDER=./src vectora index
```

---

> **Próximo**: [Architecture Overview](./overview.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
