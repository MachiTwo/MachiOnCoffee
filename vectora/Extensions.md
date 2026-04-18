# Vectora Extensions

> [!NOTE]
> **Contexto de IA onde o código acontece.**
> Plugins oficiais que integram o Vectora Agent ao seu workflow de desenvolvimento.

---

As **Vectora Extensions** são os pontos de entrada que embarcam ou conectam o **Vectora Agent** ao ambiente onde o programador já trabalha.

Elas não possuem lógica de busca ou IA própria — essa responsabilidade é do **Vectora Agent** (e, por extensão, do **Vectora KV**). O papel das extensões é ser uma ponte precisa: capturar eventos da IDE, repassar ao Agent via ACP/MCP e renderizar a resposta de forma nativa no ambiente do usuário.

---

## 🧩 Extensões Disponíveis

### 1. VS Code Extension

A extensão principal. Embarca o **Vectora Agent** como parte do pacote — sem download separado.

#### Modo Agent (Interativo)

- Painel lateral dedicado com interface de chat completa
- Feedback visual do processo de busca HNSW em tempo real
- Execução de ferramentas com confirmação explícita do usuário
- Snapshots Git automáticos antes de qualquer edição no código

#### Modo Sub-Agent (MCP Bridge)

- Registra o Vectora como um servidor MCP disponível para o **Antigravity**, **Claude Dev (Cline)** ou qualquer cliente MCP instalado no VS Code
- O agente principal pode delegar para o Vectora tarefas específicas de RAG profundo e análise de codebase
- Sem painel visual — opera silenciosamente como motor especialista

#### Indexação Live

- File watcher integrado ao VS Code que detecta saves e envia diffs ao Vectora Agent
- O índice HNSW é atualizado em background sem interromper o workflow
- Indicador de status na barra inferior: `Vectora: indexing...` / `Vectora: ready`

```
Requisitos: VS Code 1.85+
Instalação: Extensions Marketplace → "Vectora"
```

---

### 2. JetBrains Plugin (IntelliJ, PyCharm, GoLand...)

Implementação estrita do **Agent Client Protocol (ACP)** para integração profunda com o ecossistema JetBrains.

- Aproveita o sistema de indexação nativo da IDE para sincronizar com o Vectora Agent
- Acesso à estrutura de PSI (Program Structure Interface) do IntelliJ para contexto mais rico sobre dependências de código
- Painel de busca semântica integrado ao painel de busca nativo da IDE
- Suporte a todos os runtimes suportados pelo JetBrains (JVM, Python, Go, etc.)

```
Compatibilidade: IntelliJ IDEA 2024.1+, GoLand 2024.1+, PyCharm 2024.1+
Instalação: JetBrains Marketplace → "Vectora"
```

---

### 3. Vectora CLI (Terminal-first)

Para quem vive no terminal. Interface baseada em **Cobra** com TUI imersiva via **Bubbletea/Charmland**.

```bash
# Comandos principais
vectora ask "Como funciona o sistema de pagamentos?"
vectora embed --path ./src/
vectora search "padrão repository pattern"
vectora memory --save "Preferência: usar sync.Pool para buffers"

# TUI interativa (estilo chat com histórico)
vectora tui

# Modo MCP Server para Claude Desktop / Gemini CLI
vectora mcp --port 3000
```

**Funcionalidades do CLI:**

- History de buscas com navegação por setas
- Output formatado com syntax highlighting para código Go/TS/Python
- Progresso de indexação com barra animada
- Export de resultados de busca em JSON ou Markdown

---

### 4. Gemini CLI Integration

Integração como **Sub-Agent MCP** para o Gemini CLI da Google.

O Vectora expõe seu arsenal de ferramentas via MCP para que o Gemini CLI possa:

- Delegar buscas semânticas no codebase local ao Vectora
- Usar as ferramentas `read_file`, `edit`, `run_shell_command` do Agent
- Manter sessão conectada ao Vectora KV (local ou cloud) sem configuração adicional

```bash
# Configuração no Gemini CLI
gemini mcp add vectora --command "vectora-agent start --mode mcp"
```

---

### 5. Claude Code Integration

Integração nativa como **Sub-Agent MCP** para o Claude Code da Anthropic.

O **Vectora Agent** se registra como um servidor MCP que o Claude Code pode invocar para tarefas de contexto profundo:

- Busca semântica em todo o codebase do projeto
- Recuperação de histórico de conversas anteriores (Token Embeddings)
- Execução de ferramentas com escopo restrito ao Trust Folder

```jsonc
// .claude/mcp_config.json
{
  "vectora": {
    "command": "vectora-agent",
    "args": ["start", "--mode", "mcp"],
    "env": {
      "VECTORA_KV_URL": "local",
    },
  },
}
```

---

## 🔄 Arquitetura das Extensions

```
IDE / CLI Tool
      │
      │  ACP (JSON-RPC/stdio)    MCP (stdio / HTTP+SSE)
      ▼
Vectora Extension / Plugin
      │
      │  Events: file_saved, query_request, tool_call
      ▼
Vectora Agent (binário local)
      │
      ├── IPC (local)  ──▶  Vectora KV Local  (BadgerDB + HNSW)
      └── HTTPS (cloud) ──▶  Vectora KV Cloud  (K8s + Kaffyn SSO)
```

As extensões são thin clients. Toda a inteligência (busca, compressão, RAG, tool execution) reside no **Vectora Agent** e no **Vectora KV**.

> [!NOTE]
> O **Vectora KV Local** é Open Source. O **Vectora KV Cloud** é a oferta gerenciada/proprietária operada pela Kaffyn.

---

## 📦 Bundle vs. Standalone

| Extensão        | Agent incluído?          | Requisito externo       |
| :-------------- | :----------------------- | :---------------------- |
| **VS Code**     | ✅ Bundled                | Nenhum                  |
| **JetBrains**   | ✅ Bundled                | Nenhum                  |
| **CLI**         | ✅ É o Agent              | Nenhum                  |
| **Gemini CLI**  | ❌ Requer Agent instalado | `vectora-agent` no PATH |
| **Claude Code** | ❌ Requer Agent instalado | `vectora-agent` no PATH |

---

## Contribuindo

As extensões são **Open Source** e contribuições são bem-vindas:

- [VS Code Extension](https://github.com/Kaffyn/Vectora/tree/main/extensions/vscode)
- [JetBrains Plugin](https://github.com/Kaffyn/Vectora/tree/main/extensions/jetbrains)
- [CLI](https://github.com/Kaffyn/Vectora/tree/main/cmd/vectora)

Para desenvolver uma extensão para uma nova plataforma, consulte o [Guia de Integração ACP/MCP](https://docs.kaffyn.com/vectora/extensions/create).

---

_Parte do ecossistema [Vectora](https://github.com/Kaffyn/Vectora) — mantido pela [Kaffyn](https://kaffyn.com)._
_Open Source · ACP + MCP · VS Code · JetBrains · CLI · Gemini CLI · Claude Code_
