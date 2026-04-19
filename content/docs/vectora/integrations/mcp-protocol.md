---
title: MCP Protocol Integration
slug: mcp-protocol
date: "2026-04-19T10:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - claude
  - cursor
  - ide
  - integration
  - mcp
  - mcp-protocol
  - vectora
---

{{< lang-toggle >}}

Vectora implementa **Model Context Protocol (MCP)**, padrão OpenAI que permite qualquer IDE com suporte a MCP se conectar e usar Vectora como servidor de contexto. Funciona nativamente em Claude Code e Cursor.

## O Que é MCP?

**MCP** é um protocolo padronizado para conectar modelos de IA a ferramentas externas. Vectora expõe suas funções (busca, análise) como ferramentas MCP que qualquer IDE compatível pode usar.

```text
IDE (Claude Code / Cursor / outro com MCP)
    ↓
  MCP Protocol (JSON-RPC)
    ↓
Vectora Server (localhost:9090 ou remote)
    ↓
  12 Tools disponíveis
```

---

## Instalação Rápida

### Pré-requisitos

- Node.js 18+
- Vectora instalado: `npm install -g @kaffyn/vectora`
- Chaves de API (Gemini, Voyage)
- IDE com suporte a MCP (Claude Code, Cursor, etc)

### Passo 1: Inicializar Projeto

```bash
cd ~/seu-projeto
vectora init --name "Seu Projeto"
```

### Passo 2: Configurar MCP em Sua IDE

**Arquivo de config** (localização varia por IDE):

- Claude Code: `~/.claude/claude_desktop_config.json`
- Cursor: `~/.cursor/cursor_config.json`
- Outras IDEs: Consulte documentação do MCP

**Adicione Vectora:**

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "GEMINI_API_KEY": "seu-valor",
        "VOYAGE_API_KEY": "seu-valor",
        "VECTORA_NAMESPACE": "seu-namespace"
      }
    }
  }
}
```

### Passo 3: Testar

1. Reinicie sua IDE
2. Procure pela tool `search_context` no menu MCP
3. Teste: `@vectora search_context "Como validar tokens?"`

---

## 12 Ferramentas Disponíveis

| Tool                   | Função                       |
| ---------------------- | ---------------------------- |
| `search_context`       | Busca semântica por chunks   |
| `search_tests`         | Busca testes relacionados    |
| `analyze_dependencies` | Encontra quem chama função X |
| `find_similar_code`    | Encontra código similar      |
| `get_file_structure`   | Resume estrutura do arquivo  |
| `list_files`           | Lista arquivos indexados     |
| `list_namespaces`      | Lista namespaces             |
| `get_namespace_stats`  | Estatísticas do namespace    |
| `index_status`         | Status do índice             |
| `reindex`              | Força re-indexação           |
| `get_config`           | Retorna config atual         |
| `get_metrics`          | Métricas de execução         |

---

## Workflows Práticos

### Workflow 1: Entender Feature

```text
Você: "Explique como funciona autenticação"
IDE: @vectora search_context "autenticação"
Vectora: Retorna chunks relevantes
IDE: Mostra chunks no contexto
```

### Workflow 2: Debugging

```text
Você: "Por que esse teste falha?"
IDE: @vectora search_context "teste X"
IDE: @vectora analyze_dependencies "função sendo testada"
Vectora: Retorna contexto relevante
```

### Workflow 3: Code Review

```text
Você: "Revise essa função"
IDE: @vectora find_similar_code "seu código"
Vectora: Encontra padrões similares
IDE: Compara com código existente
```

---

## Configuração Avançada

### Custom Namespace

```json
{
  "mcpServers": {
    "vectora": {
      "env": {
        "VECTORA_NAMESPACE": "staging" // Use namespace diferente
      }
    }
  }
}
```

### Multiple IDEs Sincronizadas

Se usar múltiplas IDEs, ambas apontam para mesma config e namespace:

```json
// Claude Code
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "VECTORA_NAMESPACE": "seu-namespace"
      }
    }
  }
}

// Cursor - mesma config
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp"],
      "env": {
        "VECTORA_NAMESPACE": "seu-namespace"
      }
    }
  }
}
```

Ambas veem os mesmos chunks, índices, namespaces.

---

## Troubleshooting

### "Vectora command not found"

```bash
# Verificar instalação
npm list -g @kaffyn/vectora

# Reinstalar se necessário
npm install -g @kaffyn/vectora --force
```

### "Connection refused"

Vectora não está rodando como servidor:

```bash
# Iniciar manualmente
vectora mcp

# Ou via config com porta customizada
{
  "env": {
    "VECTORA_MCP_PORT": "9091"
  }
}
```

### "API key not found"

Verificar variáveis de ambiente:

```bash
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# Se vazio, configure em .env ou no config JSON
```

---

## Performance

- **Latência esperada**: ~300-500ms (rede + APIs)
- **Local search**: ~100ms (sem APIs)
- **Cache**: Resultados cacheados em `.vectora/`
- **Concurrent**: Suporta múltiplos IDEs apontando para mesmo servidor

---

## IDEs Compatíveis

| IDE             | Suporte        | Status                |
| --------------- | -------------- | --------------------- |
| **Claude Code** | MCP nativo     | Testado               |
| **Cursor**      | MCP nativo     | Testado               |
| **VS Code**     | MCP não nativo | Use extension própria |
| **Zed**         | MCP suportado  | Não testado           |
| **Neovim**      | MCP via plugin | Não testado           |

Para VS Code, use [VS Code Extension](./vscode-extension.md).

---

## Próximos Passos

- **VS Code?** → [VS Code Extension](./vscode-extension.md)
- **ChatGPT?** → [ChatGPT Plugin](./chatgpt-plugin.md)
- **Gemini?** → [Gemini API](./gemini-api.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
