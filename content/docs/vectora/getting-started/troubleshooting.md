---
title: Solução de Problemas
slug: troubleshooting
date: "2026-04-19T08:45:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - auth
  - concepts
  - config
  - context-engine
  - debug
  - embeddings
  - errors
  - gemini
  - getting-started
  - guardian
  - help
  - integration
  - mcp
  - protocol
  - rag
  - reranker
  - security
  - tools
  - troubleshooting
  - trust-folder
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}

Guia de solução de problemas mais frequentes durante instalação, configuração e uso do Vectora.

## Instalação

## Erro: `npm: command not found`

**Causa**: Node.js não está instalado ou não está no PATH.

**Solução**:

```bash
# Instale Node.js: https://nodejs.org (LTS recomendado)
node --version # Deve retornar v18+
npm --version # Deve retornar 9+
```

## Erro: `EACCES: permission denied`

**Causa**: Permissão insuficiente para instalar globalmente.

**Solução**:

```bash
# Configure npm para local installation
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Adicione a linha acima ao ~/.bashrc ou ~/.zshrc
npm install -g @kaffyn/vectora
```

## Erro: `vectora: command not found`

**Causa**: Vectora instalado mas não no PATH.

**Solução**:

```bash
# Verifique instalação
npm list -g @kaffyn/vectora

# Reinstale
npm install -g @kaffyn/vectora

# Teste
vectora --version
```

## Configuração

## Erro: `API key not found`

**Causa**: Variáveis de ambiente não configuradas.

**Solução**:

```bash
# Verifique se as chaves estão definidas
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# Se vazias, configure
export GEMINI_API_KEY="sua_chave_aqui"
export VOYAGE_API_KEY="sua_chave_aqui"

# Ou crie .env file
cat > .env << 'EOF'
GEMINI_API_KEY=sk-xxx
VOYAGE_API_KEY=pa-xxx
EOF
```

## Erro: `Config validation failed`

**Causa**: Sintaxe YAML inválida em `vectora.config.yaml`.

**Solução**:

```bash
# Valide YAML
yamllint vectora.config.yaml

# Ou use online: https://yamllint.com

# Erros comuns:
# - Indentação inconsistente (use 2 espaços)
# - Valores entre aspas faltando
# - Símbolos especiais não escapados
```

## Erro: `Trust folder does not exist`

**Causa**: Caminho em `trust_folder` não existe.

**Solução**:

```yaml
# Atualize vectora.config.yaml
namespace:
  trust_folder: "." # ou caminho válido
```

## MCP Integration

## Erro: `Vectora MCP server not found`

**Causa**: `claude_desktop_config.json` mal formatado.

**Solução**:

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

Verifique:

- JSON é válido (use [jsonlint.com](https://jsonlint.com))
- Arquivo em local correto: `~/.claude/claude_desktop_config.json`
- Reinicie Claude Desktop após salvar

## Erro: `Connection refused`

**Causa**: Vectora não consegue conectar à API.

**Solução**:

```bash
# Verifique chaves de API
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY

# Teste conectividade
curl https://generativelanguage.googleapis.com/v1beta/models

# Se falhar, sua chave pode estar inválida
# Gere nova chave em https://aistudio.google.com/app/apikey
```

## Claude não usa Vectora automaticamente

**Causa**: Claude não detecta que a ferramenta é relevante.

**Solução**: Seja explícito na requisição:

```text
Use Vectora para buscar contexto sobre autenticação.
Procure no codebase por implementações de JWT.
```

## API & Providers

## Erro: `403 Quota Exceeded (Gemini)`

**Causa**: Limite de requisições excedido (60/min no tier gratuito).

**Solução**:

```bash
# Aguarde o reset do quota (próximo minuto)
# Ou faça upgrade para plano Plus em https://vectora.dev/plans

# Para debug: verifique uso
vectora stats --provider gemini
```

## Erro: `401 Unauthorized (Voyage)`

**Causa**: Chave de API inválida ou expirada.

**Solução**:

```bash
# Gere nova chave em https://dash.voyageai.com/api-keys
vectora config set --key VOYAGE_API_KEY --value "nova_chave"

# Teste
vectora test --provider voyage
```

## Erro: `Network timeout`

**Causa**: Conexão lenta ou API indisponível.

**Solução**:

```bash
# Aumenta timeout (padrão: 30s)
export VECTORA_TIMEOUT_MS=60000

# Teste conectividade
ping generativelanguage.googleapis.com

# Se VPN/proxy:
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=https://proxy:port
```

## Indexação & RAG

## Erro: `Project not found`

**Causa**: Namespace não existe.

**Solução**:

```bash
# Inicialize projeto
vectora init --name "Meu Projeto"

# Ou especifique em claude_desktop_config.json
"VECTORA_NAMESPACE": "my-project"
```

## Erro: `No results found`

**Causa**: Codebase não indexado ou query irrelevante.

**Solução**:

```bash
# Force reindexing
vectora ingest --project . --force

# Verifique status
vectora status --project .

# Tente query diferente ou mais específica
# Exemplo: em vez de "auth", tente "JWT validation in middleware"
```

## Embedding muito lento

**Causa**: Codebase grande ou conexão lenta.

**Solução**:

```bash
# Use batch processing
vectora ingest --batch-size 16 # default: 32

# Ou configure em vectora.config.yaml
indexing:
  batch_size: 16

# Para desenvolvimento local, use fallback
providers:
  embedding:
    fallback: "local" # local embedding via ollama
```

## Performance

## Claude Desktop é lento

**Causa**: Muitas requisições simultâneas ou codebase grande.

**Solução**:

```bash
# Limite indexação automática
vectora config set VECTORA_AUTO_INGEST=false

# Ou agende indexação em horário off-peak
vectora schedule ingest --time 02:00 --recurring daily
```

## Alto uso de memória

**Causa**: Cache local grande ou índices não limpos.

**Solução**:

```bash
# Limpe cache
vectora cache clear

# Reduza cache size
vectora config set VECTORA_CACHE_SIZE=100MB

# Verifique consumo
vectora stats --memory
```

## Debug & Logging

## Ativar modo debug

```bash
# Via CLI
vectora --log-level debug

# Via variável
export VECTORA_LOG_LEVEL=debug

# Salve logs em arquivo
vectora mcp-serve --log-file debug.log
```

## Obter mais informações

```bash
# Status geral
vectora status

# Detalhes da configuração
vectora config list

# Estatísticas de uso
vectora stats

# Verificar indexação
vectora index --list --verbose
```

## Onde Buscar Ajuda

1. **FAQ Específicos**:

   - [General FAQ](../faq/general.md)
   - [Security FAQ](../faq/security.md)
   - [Billing FAQ](../faq/billing.md)

2. **Documentação**:

   - [Configuration Guide](./configuration.md)
   - [MCP Integration](../integrations/claude-code.md)
   - [Security & Guardian](../security/guardian.md)

3. **Comunidade**:

   - GitHub Issues: [vectora/issues](https://github.com/kaffyn/vectora/issues)
   - Discussions: [vectora/discussions](https://github.com/kaffyn/vectora/discussions)
   - Discord: [Vectora Community](https://discord.gg/vectora)

4. **Reportar Bug**:

   ```bash
   vectora bug-report --include-logs --include-config
   # Gera arquivo com informações sanitizadas para enviar
   ```

## FAQ

**P: Onde estão meus dados?**
R: Localmente em `.vectora/` (cache) e Qdrant (embeddings indexados). Kaffyn nunca acessa seu código bruto.

**P: Como resetar tudo?**
R: Use `vectora reset --full --confirm`. Isso remove cache, índices e config local.

**P: Posso usar Vectora sem internet?**
R: Parcialmente. Busca semântica precisa de API. File operations funcionam offline.

---

> **Próximo**: Aprenda sobre [Context Engine](../concepts/context-engine.md).

---

## External Linking

| Concept               | Resource                             | Link                                                                                   |
| --------------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**               | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **Anthropic Claude**  | Claude Documentation                 | [docs.anthropic.com/](https://docs.anthropic.com/)                                     |
| **Voyage Embeddings** | Voyage Embeddings Documentation      | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)         |
| **Voyage Reranker**   | Voyage Reranker API                  | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)             |
| **JWT**               | RFC 7519: JSON Web Token Standard    | [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519) |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
