---
title: Quickstart MCP
slug: quickstart-mcp
date: "2026-04-19T08:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - mcp
  - quickstart
  - claude-desktop
  - integration
  - vectora
---

{{< lang-toggle >}}
Este guia permite que você integre o Vectora com Claude Desktop via MCP em menos de 5 minutos.

> [!IMPORTANT]
> Pré-requisitos: Vectora instalado globalmente (`vectora --version`) e Claude Desktop instalado ([download](https://claude.ai/download)).

---

## Passo 1: Localizar o Arquivo de Configuração

## macOS / Linux

```bash
# Arquivo de configuração do Claude Desktop
open ~/.claude/claude_desktop_config.json

# Se não existir, crie com:
mkdir -p ~/.claude
touch ~/.claude/claude_desktop_config.json
```

## Windows

```powershell
# Arquivo de configuração (WSL2 ou Windows)
"$env:APPDATA\Claude\claude_desktop_config.json"

# Se não existir, crie com:
New-Item -Path "$env:APPDATA\Claude" -ItemType Directory -Force
```

---

## Passo 2: Adicionar Vectora como MCP Server

Edite `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp-serve"],
      "env": {
        "GEMINI_API_KEY": "sk-xxx...",
        "VOYAGE_API_KEY": "pa-xxx...",
        "VECTORA_NAMESPACE": "my-project"
      }
    }
  }
}
```

## Alternativa: Usar Variáveis de Ambiente do Sistema

Se já tiver `GEMINI_API_KEY` e `VOYAGE_API_KEY` definidas:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "vectora",
      "args": ["mcp-serve"]
    }
  }
}
```

---

## Passo 3: Reiniciar Claude Desktop

```bash
# Feche completamente Claude Desktop e abra novamente
# Isso carrega a nova configuração MCP
```

---

## Passo 4: Testar a Conexão

## Via Claude Desktop Chat

Abra Claude Desktop e teste:

```text
Me mostre os arquivos disponíveis usando o Vectora
```

Claude deve responder algo como:

```text
I have access to Vectora, a code context engine. Let me check what files are available in your project.

[Vectora is now searching your codebase...]

Available files in namespace 'my-project':
- src/auth/jwt.ts (authentication)
- src/services/database.ts (database layer)
- docs/README.md (documentation)
...
```

## Verificar Status do MCP

Se receber erro:

1. **Abra MCP Inspector** (no Claude Desktop: Menu → Configurações → Ferramentas do Desenvolvedor)
2. **Procure por "vectora"** na lista de servidores
3. **Status deve ser "Connected"**

Se não estiver conectado:

- Verifique que `vectora --version` funciona no terminal
- Confira o arquivo `claude_desktop_config.json` (sintaxe JSON)
- Reinicie Claude Desktop

---

## Passo 5: Seu Primeiro Comando

## Explorar o Codebase

```text
Qual é a estrutura deste projeto? Liste os diretórios principais.
```

Claude usa `file_list` via Vectora.

## Buscar Contexto

```text
Como funciona a autenticação JWT neste projeto? Encontre a implementação.
```

Claude usa `context_search` para busca semântica.

## Analisar Um Arquivo

```text
Leia e explique o arquivo src/main.ts
```

Claude usa `file_read` para ler o arquivo.

---

## Estrutura do Projeto

Depois de `vectora init`, você terá:

```text
meu-projeto/
├── vectora.config.yaml # Configuração do projeto
├── AGENTS.md # Memória do agente (auto-gerado)
├── .vectora/ # Cache e índices locais
│ ├── embeddings/ # Cache de embeddings
│ └── index.json # Metadados do índice
├── src/ # Seu código
└── .env # Variáveis de ambiente (não commitar!)
```

---

## Comandos MCP Disponíveis

| Comando          | O que faz                     | Exemplo             |
| ---------------- | ----------------------------- | ------------------- |
| `context_search` | Busca semântica no codebase   | "autenticação JWT"  |
| `file_read`      | Lê um arquivo                 | `src/main.ts`       |
| `file_list`      | Lista arquivos recursivamente | `src/`              |
| `file_write`     | Escreve ou modifica arquivo   | Criar novo arquivo  |
| `file_edit`      | Edita parte de um arquivo     | Mudar uma função    |
| `grep_search`    | Busca por regex               | Padrões específicos |

---

## Troubleshooting

### Erro: `Vectora MCP server not found`

**Causa**: O binário `vectora` não está no PATH.

**Solução**: Verifique se a instalação via Winget ou script foi concluída e reinicie seu terminal.

### Erro: `Connection refused`

**Causa**: Vectora não consegue conectar à API do Gemini/Voyage.

**Solução**: Verifique seu status de autenticação com `vectora auth status` ou faça login novamente com `vectora auth login`.

### Erro: `Project not found`

**Causa**: Namespace não existe.

**Solução**:

```bash
# Inicialize o projeto
vectora init --name "Meu Projeto"

# Ou especifique em claude_desktop_config.json:
"VECTORA_NAMESPACE": "my-project"
```

### Claude não usa Vectora automaticamente

**Causa**: Claude não detecta que a ferramenta é relevante.

**Solução**: Seja explícito:

```text
Use o Vectora para buscar informações sobre autenticação neste projeto.
```

---

## Próximos Passos

- **Aprofundar**: Leia [Context Engine](../concepts/context-engine.md)
- **Integrar com Cursor**: [Cursor Integration](../integrations/cursor.md)
- **Entender Segurança**: [Guardian & RBAC](../security/guardian.md)

---

## FAQ

**P: Posso usar Vectora com outros agentes além de Claude?**
R: Sim! Veja [Gemini Integration](../integrations/gemini-integration.md) e [Custom Agents](../integrations/custom-agents.md).

**P: Vectora funciona offline?**
R: Parcialmente. Context search precisa de internet (Voyage API). File operations funcionam offline.

**P: Como debugar conexões MCP?**
R: Use o MCP Inspector em Claude Desktop (Menu → Developer Tools → MCP Inspector).

---

> **Próximo**: Aprenda sobre [Troubleshooting](./troubleshooting.md).

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
