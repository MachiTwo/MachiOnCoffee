---
title: Model Context Protocol (MCP)
slug: mcp-protocol
date: "2026-04-19T10:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - ast-parsing
  - auth
  - chatgpt
  - claude
  - concepts
  - config
  - context-protocol
  - cursor
  - embeddings
  - errors
  - gemini
  - ide
  - integration
  - json-rpc
  - mcp
  - mcp-protocol
  - mongodb-atlas
  - plugins
  - protocol
  - reranker
  - tools
  - troubleshooting
  - vector-search
  - vectora
  - voyage
---

{{< lang-toggle >}}

## Protocolo MCP: Conecte Vectora a Qualquer IDE

**Model Context Protocol** é um padrão aberto que permite que IDEs e aplicações se conectem a servidores de ferramentas externas. Vectora implementa MCP para que você acesse busca semântica de código diretamente em sua IDE preferida.

> [!IMPORTANT] **Melhor para**: IDEs modernas (Claude Code, Cursor, Zed). Se estiver em VS Code, use a [VS Code Extension](./vscode-extension.md) nativa.

## Como Funciona: Fluxo MCP

```mermaid
graph LR
    A[Você escreve no IDE] -->|@vectora search_context| B[IDE]
    B -->|JSON-RPC 2.0 via stdio| C["Vectora MCP Server<br/>(processo local)"]
    C -->|Query embedding| D["MongoDB Atlas<br/>Vector Search"]
    D -->|Chunks relevantes| C
    C -->|Tool result JSON| B
    B -->|Mostra no contexto| A
```

### Sequência de Comunicação

1. **IDE startup**: IDE lê config MCP
2. **Launch server**: IDE executa `vectora mcp --stdio`
3. **Initialize**: IDE envia handshake JSON-RPC
4. **Tool discovery**: Vectora responde com 12 tools disponíveis
5. **User calls tool**: Usuario digita `@vectora search_context "..."`
6. **JSON-RPC call**: IDE envia request via stdin
7. **Vectora processes**: Busca no vector DB
8. **Response**: Vectora retorna resultado via stdout
9. **Display**: IDE mostra contexto ao usuário

## Setup Passo a Passo por IDE

### IDE 1: Claude Code (Recomendado)

#### Pré-requisitos

- Claude Code instalado (gratuito)
- Vectora instalado: `npm install -g @kaffyn/vectora`
- API Keys: Gemini e Voyage

#### Passo 1: Localizar Configuração (Claude)

```bash
# macOS/Linux
cat ~/.claude/claude_desktop_config.json

# Windows
cat $APPDATA\Claude\claude_desktop_config.json

# Se não existir, crie um vazio
cat > ~/.claude/claude_desktop_config.json << 'EOF'
{}
EOF
```

#### Passo 2: Configure Vectora como MCP Server

```bash
# Edite o arquivo
cat > ~/.claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "GEMINI_API_KEY": "seu-gemini-api-key",
        "VOYAGE_API_KEY": "seu-voyage-api-key",
        "VECTORA_NAMESPACE": "seu-projeto"
      }
    }
  }
}
EOF
```

#### Passo 3: Reinicie Claude Code

Feche e reabra Claude Code completamente.

#### Passo 4: Use Vectora

Em qualquer conversa:

```text
Usuário: "Você tem acesso a Vectora. Como validamos tokens?"

Claude: Vou procurar no seu codebase...
└─ @vectora search_context("token validation")
└─ Mostra chunks relevantes
└─ Explica baseado no código real
```

### IDE 2: Cursor

#### Passo 1: Localizar Configuração (Cursor)

```bash
# macOS/Linux
~/.cursor/cursor_settings/cursor_desktop_config.json

# Windows
$APPDATA\Cursor\User\cursor_desktop_config.json
```

#### Passo 2: Configure (Mesmo do Claude Code)

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "GEMINI_API_KEY": "...",
        "VOYAGE_API_KEY": "...",
        "VECTORA_NAMESPACE": "seu-projeto"
      }
    }
  }
}
```

#### Passo 3: Reinicie Cursor

Feche e reabra o editor.

### IDE 3: Zed (Experimental)

Zed tem suporte incipiente a MCP. Setup similar:

```json
{
  "assistant": {
    "external_tools": {
      "vectora": {
        "command": "vectora",
        "args": ["mcp", "--stdio"]
      }
    }
  }
}
```

## 12 Tools Disponíveis via MCP

### 1. search_context

**Descrição**: Busca semântica por code chunks, documentação.

```json
{
  "method": "tools/call",
  "params": {
    "name": "search_context",
    "arguments": {
      "query": "Como validar JWTs?",
      "top_k": 5,
      "threshold": 0.7
    }
  }
}
```

**Retorna**: Array de chunks com código, arquivo, linha, precisão.

### 2. search_tests

**Descrição**: Encontra testes relacionados a uma query.

```json
{
  "params": {
    "name": "search_tests",
    "arguments": {
      "query": "autenticação",
      "top_k": 10
    }
  }
}
```

### 3. analyze_dependencies

**Descrição**: Análise de dependências - quem chama função X?

```json
{
  "params": {
    "name": "analyze_dependencies",
    "arguments": {
      "symbol": "getUserById",
      "depth": 2,
      "include_indirect": true
    }
  }
}
```

**Retorna**: Call graph com chamadores diretos e indiretos.

### 4. find_similar_code

**Descrição**: Encontra código similar ao snippet fornecido.

```json
{
  "params": {
    "name": "find_similar_code",
    "arguments": {
      "code_snippet": "async function validateToken(token) { ... }",
      "language": "typescript",
      "top_k": 5
    }
  }
}
```

### 5. get_file_structure

**Descrição**: Retorna estrutura do arquivo (funções, classes, tipos).

```json
{
  "params": {
    "name": "get_file_structure",
    "arguments": {
      "path": "src/auth/validate.ts"
    }
  }
}
```

### 6. list_files

**Descrição**: Lista arquivos indexados no namespace.

```json
{
  "params": {
    "name": "list_files",
    "arguments": {
      "pattern": "*.ts",
      "limit": 100
    }
  }
}
```

### 7. list_namespaces

**Descrição**: Lista todos os namespaces (projetos) disponíveis.

```json
{
  "params": {
    "name": "list_namespaces",
    "arguments": {}
  }
}
```

### 8. get_namespace_stats

**Descrição**: Estatísticas do namespace: documentos, tamanho, etc.

```json
{
  "params": {
    "name": "get_namespace_stats",
    "arguments": {
      "namespace": "seu-projeto"
    }
  }
}
```

### 9. index_status

**Descrição**: Status atual do índice (em progresso, completo, etc).

```json
{
  "params": {
    "name": "index_status",
    "arguments": {
      "namespace": "seu-projeto"
    }
  }
}
```

### 10. reindex

**Descrição**: Força re-indexação do namespace.

```json
{
  "params": {
    "name": "reindex",
    "arguments": {
      "namespace": "seu-projeto",
      "force": true
    }
  }
}
```

### 11. get_config

**Descrição**: Retorna configuração atual.

```json
{
  "params": {
    "name": "get_config",
    "arguments": {}
  }
}
```

### 12. get_metrics

**Descrição**: Métricas de execução (latências, hits, etc).

```json
{
  "params": {
    "name": "get_metrics",
    "arguments": {
      "namespace": "seu-projeto"
    }
  }
}
```

## Workflows Práticos Completos

### Workflow 1: Entender Feature do Zero

```text
Usuário: "Explique como funciona autenticação neste projeto"

1. IDE chama: @vectora search_context("autenticação")
2. Vectora retorna:
   - src/auth/validate.ts (precisão 0.95)
   - src/middleware/auth.ts (0.89)
   - src/guards/jwt.ts (0.85)
   - tests/auth.test.ts (0.82)

3. Claude analisa chunks:
   - "Vejo que usam JWT com expiração de 1h"
   - "Middleware valida em cada request"
   - "3 guards diferentes: Bearer, Session, OAuth"

4. Explicação final com código real do projeto
```

### Workflow 2: Debug de Bug

```text
Usuário: "Este teste falha. Por quê?"

1. IDE: @vectora search_tests("erro 401")
   └─ Encontra testes falhando

2. IDE: @vectora analyze_dependencies("validateToken")
   └─ Mostra quem chama a função

3. IDE: @vectora get_file_structure("src/auth/validate.ts")
   └─ Mostra estrutura do arquivo

4. Claude debugga com contexto real
```

### Workflow 3: Code Review com Padrões

```text
Usuário: "Revise essa função de cache"

1. IDE: @vectora find_similar_code(seu_código)
   └─ Encontra funções similares existentes

2. IDE: @vectora search_context("cache implementation")
   └─ Mostra padrões de cache no projeto

3. Claude: "Vejo que o projeto usa Pattern X, sua implementação deveria..."
```

## Configuração Avançada

### Usar Namespace Diferente (Staging vs Prod)

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp", "--stdio"],
      "env": {
        "VECTORA_NAMESPACE": "staging"
      }
    }
  }
}
```

### Múltiplas IDEs Sincronizadas

Todas apontam para mesmo namespace:

```bash
# Claude Code + Cursor + Zed
# Todos compartilham mesmo cacheE indices via namespace

VECTORA_NAMESPACE="seu-projeto"
```

### Logging Detalhado para Debug

```json
{
  "mcpServers": {
    "vectora": {
      "env": {
        "VECTORA_LOG_LEVEL": "debug",
        "VECTORA_LOG_FILE": "~/.vectora/mcp.log"
      }
    }
  }
}
```

### Port Customizado (se padrão está em uso)

```json
{
  "mcpServers": {
    "vectora": {
      "env": {
        "VECTORA_MCP_PORT": "9091"
      }
    }
  }
}
```

## Troubleshooting

### "Vectora command not found"

```bash
# Verifique instalação
which vectora
vectora --version

# Reinstale se necessário
npm install -g @kaffyn/vectora@latest

# Ou use caminho absoluto em config
{
  "command": "/usr/local/bin/vectora"
}
```

### "Connection refused / MCP server not starting"

```bash
# Teste manualmente
vectora mcp --stdio

# Envie handshake:
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | vectora mcp --stdio

# Se falha, verifique logs
VECTORA_LOG_LEVEL=debug vectora mcp --stdio
```

### "API Key not found"

```bash
# Verifique variáveis
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# Se vazio, configure em config JSON ou .env
export GEMINI_API_KEY="seu-valor"
export VOYAGE_API_KEY="seu-valor"

# Teste
vectora config show
```

### "Namespace não encontrado"

```bash
# Liste namespaces
vectora namespace list

# Configure o namespace correto
{
  "env": {
    "VECTORA_NAMESPACE": "seu-projeto-real"
  }
}
```

### IDE não vê Vectora após restart

1. Verifique arquivo de config (não há sintaxe JSON errada)
2. Teste `vectora mcp --stdio` manualmente
3. Reinicie IDE completamente (não apenas a janela)
4. Verificar se porta 9090 não está em uso

## Performance & Otimizações

### Latência Esperada

| Operação                  | Latência   | Nota                       |
| ------------------------- | ---------- | -------------------------- |
| Local search (sem API)    | ~100ms     | Índice em cache            |
| Semantic search (com API) | ~300-500ms | Inclui embedding + ranking |
| Cached result             | ~20ms      | Segundo hit idêntico       |
| Analyze dependencies      | ~200ms     | AST parsing                |

### Dicas de Performance

1. **Cache**: Mesma query 2x é ~15x mais rápido
2. **Batch queries**: Agrupe múltiplas buscas em uma
3. **Namespace mínimo**: Use namespace específico para seu projeto
4. **Monitor**: `@vectora get_metrics` mostra hit rate

## IDEs & Suporte

| IDE             | Suporte           | Status        | Docs                                          |
| --------------- | ----------------- | ------------- | --------------------------------------------- |
| **Claude Code** | MCP nativo        | Testado       | [Setup acima](#ide-1-claude-code-recomendado) |
| **Cursor**      | MCP nativo        | Testado       | [Setup acima](#ide-2-cursor)                  |
| **Zed**         | MCP suportado     | Experimental  | [Setup acima](#ide-3-zed-experimental)        |
| **Neovim**      | MCP via plugin    | Não testado   | Requer plugin MCP                             |
| **VS Code**     | MCP não suportado | Use extension | [VS Code Extension](./vscode-extension.md)    |
| **Vim**         | Não suportado     |               | Não há planos                                 |

## Próximas Integrações

- **VS Code?** → [VS Code Extension](./vscode-extension.md) (UI nativa)
- **ChatGPT?** → [ChatGPT Plugin](./chatgpt-plugin.md) (Custom GPT)
- **Gemini?** → [Gemini CLI](./gemini-cli.md) ou [Gemini API](./gemini-api.md)

## External Linking

| Concept                | Resource                                    | Link                                                                                                       |
| ---------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **MCP**                | Model Context Protocol Specification        | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                     |
| **MCP Go SDK**         | Go SDK for MCP (anthropics/go-sdk)          | [github.com/anthropics/anthropic-sdk-go](https://github.com/anthropics/anthropic-sdk-go)                   |
| **Anthropic Claude**   | Claude API Documentation                    | [docs.anthropic.com/](https://docs.anthropic.com/)                                                         |
| **Anthropic Cookbook** | Recipes and patterns for using Claude       | [github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)               |
| **MongoDB Atlas**      | Atlas Vector Search Documentation           | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **Gemini API**         | Google AI Studio & Gemini API Documentation | [ai.google.dev/docs](https://ai.google.dev/docs)                                                           |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
