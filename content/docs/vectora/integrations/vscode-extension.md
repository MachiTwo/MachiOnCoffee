---
title: VS Code Extension
slug: vscode-extension
date: "2026-04-19T09:45:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - ast-parsing
  - auth
  - chatgpt
  - concepts
  - config
  - embeddings
  - extension
  - integration
  - mcp
  - plugins
  - privacy
  - protocol
  - system
  - troubleshooting
  - vectora
  - vscode
  - yaml
---

{{< lang-toggle >}}
{{< section-toggle >}}

**APP PRÓPRIO**: Vectora oferece uma extensão nativa para VS Code com UI integrada (painel sidebar, commands, inline hover) - não precisa de MCP. Desenvolvimento totalmente customizado para VS Code.

> [!IMPORTANT] VS Code Extension (app próprio) vs MCP Protocol (genérico para múltiplas IDEs). Use extension se estiver em VS Code.

## Instalação

## Via VS Code Marketplace

1. Abra VS Code
2. Vá para **Extensions** (Cmd/Ctrl + Shift + X)
3. Procure: `Vectora`
4. Clique em **Install**

## Alternativa: Manual Install

```bash
# Clone do repositório
git clone https://github.com/kaffyn/vectora-vscode.git

# Instale em ~/.vscode/extensions
ln -s $(pwd)/vectora-vscode ~/.vscode/extensions/
```

## Setup Inicial

## Passo 1: Configurar Vectora no Projeto

```bash
cd ~/seu-projeto
vectora init --name "Meu Projeto" --type codebase
```

## Passo 2: Abrir Projeto em VS Code

```bash
code ~/seu-projeto
```

## Passo 3: Configurar Keys

VS Code pedirá chaves de API na primeira execução. Você pode entrar com:

- **Opção A**: Colar chaves diretamente (armazenado em settings.json encriptado)
- **Opção B**: Usar .env local (`.env` será lido automaticamente)
- **Opção C**: Usar variáveis de sistema (PATH, HOME, etc.)

```bash
# Via .env (recomendado)
cat > .env << 'EOF'
GEMINI_API_KEY=sk-...
VOYAGE_API_KEY=sk-...
VECTORA_NAMESPACE=seu-namespace
EOF
```

## Interface & Features

## Sidebar Panel

VS Code mostra um painel "Vectora" na sidebar:

```text
┌─────────────────────────┐
│ Vectora │
├─────────────────────────┤
│ Indexed Files │
│ • src/ (2847 chunks) │
│ • docs/ (312 chunks) │
│ │
│ Search │
│ [Search box] │
│ │
│ Stats │
│ Precision: 0.72 │
│ Latency: 120ms │
│ Indexed: 3159 chunks │
└─────────────────────────┘
```

## Command Palette

Acesse comandos via `Cmd/Ctrl + Shift + P`:

```text
Vectora: Search Context
Vectora: Analyze Dependencies
Vectora: Find Tests
Vectora: Index Status
Vectora: Show Metrics
```

## Inline Hover

Passe o mouse sobre um identificador para ver contexto:

```typescript
function getUserById(|id: string) { ← Hover aqui
  // Mostra:
  // - Tipo: função
  // - Definida em: src/user-service.ts:45
  // - Contexto semelhante: findUserById, getUser, etc.
}
```

## Workflows Passo-a-Passo

Os workflows abaixo mostram a experiência típica de uso da extensão Vectora no VS Code, com interface detalhada e passos claros.

## Workflow 1: Busca Rápida (5s de setup)

**Cenário**: Você quer entender como tokens JWT são validados no projeto.

```text
1. Pressione Cmd/Ctrl + Shift + P (Command Palette)
   → Mostra: caixa de entrada vazia com ">" no topo

2. Digite: "Vectora: Search Context"
   → Autocomplete mostra opção Vectora

3. Pressione Enter
   → Abre painel de busca (direita da sidebar)

4. Digite: "Como faz validação de tokens?"
   → Em tempo real: mostra resultados conforme digita

5. Resultados aparecem em 120-250ms
   ┌─────────────────────────────────┐
   │ Vectora Results (8 chunks) │
   ├─────────────────────────────────┤
   │ src/auth/jwt.ts:45 │ ← Clique para ir
   │ validateToken() { ... │
   │ precision: 0.92 | latency 240ms│
   │ │
   │ src/auth/guards.ts:12 │
   │ VerifyJWT middleware { ... │
   │ precision: 0.88 | latency 240ms│
   │ │
   │ src/auth/types.ts:3 │
   │ interface JWTPayload { ... │
   │ precision: 0.76 │
   │ │
   │ [Mostrar mais] │
   └─────────────────────────────────┘
```

Clique em qualquer resultado → editor salta para o arquivo.

## Workflow 2: Análise Inteligente de Função

**Cenário**: Você clicou em uma função e quer ver TUDO que está relacionado.

```text
1. Posicione cursor em: getUserById
2. Pressione Cmd/Ctrl + Shift + H (Find References)
3. VS Code mostra painel "Find All References":

   ┌─────────────────────────────────┐
   │ 62 References to getUserById │
   ├─────────────────────────────────┤
   │ DIRECT CALLS (47) │
   │ • src/routes/user.ts:23 │
   │ • src/middleware/auth.ts:34 │
   │ • src/services/profile.ts:12 │
   │ │
   │ INDIRECT via getUserData (12) │
   │ • src/handlers/index.ts:5 │
   │ • src/cache/service.ts:99 │
   │ │
   │ TESTS (3) │
   │ • src/__tests__/user.test.ts:45 │
   │ │
   │ [Expandir com Vectora] ← Novo │
   └─────────────────────────────────┘
```

Clique em "Expandir com Vectora" → mostra contexto semântico:

```text
Referências semelhantes não encontradas por AST:
• getUserByEmail() [85% similar]
• fetchUser() [72% similar]
• getActiveUser() [68% similar]
```

## Workflow 3: Code Review com Contexto (Entender PR complexa)

**Cenário**: Revisando PR que toca autenticação, precisa entender impacto.

```text
1. Abra arquivo modificado: auth/jwt.ts
2. Cmd/Ctrl + Alt + F (Find Changes in Context)
3. Painel mostra:

   ┌────────────────────────────────────┐
   │ Vectora: Changes & Impact │
   ├────────────────────────────────────┤
   │ LINHAS MODIFICADAS │
   │ L45: function validateToken │
   │ L52: if (!token.verified) │
   │ │
   │ ARQUIVOS QUE USAM ESSAS FUNÇÕES │
   │ • src/guards/auth.guard.ts (5) │
   │ • src/routes/api.ts (3) │
   │ • src/middleware/verify.ts (8) │
   │ │
   │ TESTES RELACIONADOS │
   │ • auth.guard.test.ts │
   │ • jwt.validation.test.ts │
   │ │
   │ ALERT: 16 dependências │
   │ Recomenda rodar testes completos │
   └────────────────────────────────────┘
```

4. Clique em "Rodar Testes Relacionados"
   → VS Code executa apenas testes relevantes (10s vs 2min full suite)

## Configuração

## settings.json

```json
{
  "vectora.enabled": true,
  "vectora.namespace": "seu-namespace",
  "vectora.trustFolder": "./src",
  "vectora.autoIndex": true,
  "vectora.indexOnSave": true,
  "vectora.maxTokens": 4096,
  "vectora.searchStrategy": "semantic",
  "vectora.showMetrics": true,
  "vectora.debugMode": false
}
```

## Advanced Config

```yaml
# .vscode/vectora.yaml (alternativa)
vectora:
  namespace: seu-namespace
  context_engine:
    strategy: "semantic"
    max_depth: 3
    timeout_ms: 2000

  ui:
    show_metrics: true
    position: "right" # ou "left"
    width_percent: 30

  indexing:
    auto_index: true
    on_save: true
    exclude:
      - node_modules/**
      - .git/**
```

## Extensões Complementares

Para melhor experiência, instale:

1. **ES7+ React/Redux/React-Native snippets** — Autocompletar smart
2. **Prettier** — Formatação consistente
3. **GitLens** — Blame + history (combina bem com Vectora)

## Troubleshooting

## Extension não aparece na sidebar

**Causa**: Não está ativada.

**Solução**:

```text
Cmd/Ctrl + Shift + X → Procure "Vectora" → Clique em "Enable"
```

## "Vectora command not found" no terminal integrado

**Causa**: VS Code usa PATH diferente.

**Solução**:

```bash
# No terminal integrado
which vectora
# Se não encontra:
npm install -g @kaffyn/vectora

# Ou adicionar ao PATH em settings.json
"vectora.commandPath": "/usr/local/bin/vectora"
```

## "API key not configured"

**Solução**:

1. Cmd/Ctrl + Shift + P → "Vectora: Configure"
2. Cole suas chaves
3. Ou use `.env` no projeto root

## Extension muito lenta

**Reduzir escopo**:

```json
{
  "vectora.trustFolder": "./src",
  "vectora.searchStrategy": "structural"
}
```

**Desabilitar auto-index**:

```json
{
  "vectora.autoIndex": false,
  "vectora.indexOnSave": false
}
```

## Performance Tips

1. **Incremental Index**: Apenas arquivos mudados são re-indexados.

   ```bash
   # No terminal VS Code
   vectora index --incremental
   ```

2. **Filter by Extension**:

   ```json
   {
     "vectora.includePatterns": ["**/*.ts", "**/*.tsx"],
     "vectora.excludePatterns": ["**/*.test.ts"]
   }
   ```

3. **Local Embedding**: Para máxima privacidade + performance:

   ```json
   {
     "vectora.embeddingProvider": "local",
     "vectora.embeddingModel": "all-MiniLM-L6-v2"
   }
   ```

## Hotkeys

| Atalho                 | Ação                  |
| ---------------------- | --------------------- |
| `Cmd/Ctrl + Shift + P` | Abrir comando Vectora |
| `Cmd/Ctrl + Shift + V` | Abrir Vectora sidebar |
| `Cmd/Ctrl + Alt + F`   | Find via Vectora      |
| `Cmd/Ctrl + Alt + D`   | Analyze dependencies  |

Customize em: **Code** → **Preferences** → **Keyboard Shortcuts**

## Comparação: Extension vs MCP

| Feature     | VS Code Extension       | MCP (Cursor/Claude) |
| ----------- | ----------------------- | ------------------- |
| Install     | Marketplace             | Config JSON         |
| UI Panel    | Native                  | Chat-based          |
| Hotkeys     | Customizable            | Fixed               |
| Performance | Local                   | Network             |
| Privacy     | Full (local embeddings) | APIs                |

**Recomendação**: Use VS Code Extension para melhor UX. Use MCP para Cursor/Claude.

## Limitações

| Recurso          | Limite                      |
| ---------------- | --------------------------- |
| Busca simultânea | 1                           |
| Context window   | 4K-8K tokens (configurável) |
| Index size       | Unlimited (disk)            |
| Latency target   | < 300ms                     |

---

> **Próximo**: [ChatGPT Plugin](./chatgpt-plugin.md)

---

## External Linking

| Concept              | Resource                             | Link                                                                                   |
| -------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**              | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**       | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **AST Parsing**      | Tree-sitter Official Documentation   | [tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/)       |
| **Anthropic Claude** | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **JWT**              | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
