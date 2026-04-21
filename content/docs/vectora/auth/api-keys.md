---
title: API Keys
slug: api-keys
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - keys
  - mcp
  - vectora
---

{{< lang-toggle >}}
As Chaves de API são credenciais programáticas que permitem acesso seguro e limitado ao backend do Vectora sem necessidade de autenticação interativa. Elas são projetadas para comunicação máquina-a-máquina, pipelines de CI/CD, integrações de agentes personalizados e acesso direto via HTTP/REST aos seus namespaces indexados.

## Chaves de API do Vectora

> [!IMPORTANT]
> As Chaves de API estão **disponíveis apenas nos planos Pro, Team e Enterprise**. Usuários do plano Free/Local autenticam-se via `vectora auth login` (JWT interativo).

## Capacidades Principais

| Recurso                   | Descrição                                                                      |
| ------------------------- | ------------------------------------------------------------------------------ |
| **Escopos Granulares**    | `read`, `write`, `search`, `admin` — atribua o privilégio mínimo necessário    |
| **Rate Limiting**         | Requisições/minuto configuráveis por chave para evitar exaustão de quota       |
| **Auto-Rotação**          | Troca de chave sem interrupção (zero downtime durante atualizações)            |
| **Revogação Instantânea** | Invalidação imediata em todos os nós via dashboard ou CLI                      |
| **Armazenamento Seguro**  | Chaves são armazenadas como hash criptográfico (bcrypt) — nunca em texto claro |

## Escopos e Permissões Disponíveis

| Escopo   | Operações Permitidas                                         | Caso de Uso Típico                                              |
| -------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| `search` | `context_search`, `context_build`, leitura de namespace only | Agentes RAG, bots de documentação, analytics read-only          |
| `read`   | `file_read`, `file_list`, `file_find`, `context_search`      | Ferramentas de navegação de código, análise estática, auditoria |
| `write`  | `file_write`, `file_edit`, `context_ingest`, `memory_save`   | Bots de indexação em CI/CD, agentes de refatoração automática   |
| `admin`  | Gestão total de namespace, rotação de chaves, quota          | Automação de plataforma, gestão de times, infraestrutura        |

> [!WARNING]
> As Chaves de API operam **fora da sessão SSO interativa**. Elas são vinculadas a um namespace específico e à quota do plano. Exceder a quota dispara o fallback para suas [credenciais BYOK](/providers/gemini/) ou retorna `429 Too Many Requests`.

## Exemplos de Integração

### 1. Configuração do Servidor MCP

Passe a chave de API via variáveis de ambiente ao iniciar o servidor MCP do Vectora:

```json
{
  "mcpServers": {
    "vectora": {
      "command": "npx",
      "args": ["@kaffyn/vectora", "mcp-serve"],
      "env": {
        "VECTORA_API_KEY": "vca_live_xxxxxxxxxxxxxxxxxxxxxxxx",
        "VECTORA_NAMESPACE": "meu-projeto-auth",
        "VECTORA_SCOPE": "search"
      }
    }
  }
}
```

#### 2. Acesso Direto via HTTP/REST

Autentique usando o cabeçalho `Authorization` para ferramentas customizadas:

```bash
curl -X POST "https://api.vectora.dev/v1/search" \
  -H "Authorization: Bearer vca_live_xxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "JWT validation middleware", "namespace": "meu-projeto", "top_k": 5}'
```

#### 3. Uso Programático (TypeScript)

```ts
import { VectoraClient } from "@kaffyn/sdk";

const client = new VectoraClient({
  apiKey: process.env.VECTORA_API_KEY!,
  namespace: "ci-pipeline-indexer",
  scope: "write",
});

// Indexa codebase no push
await client.context.ingest("./src");
```

## Boas Práticas de Segurança

**Princípio do Menor Privilégio**: Use `search` para agentes de leitura, `write` apenas para pipelines de indexação automáticos.
**Injeção via Ambiente**: Nunca coloque chaves no código. Use `.env`, segredos de CI/CD ou KMS em nuvem.
**Política de Rotação**: Rotacione chaves a cada 90 dias ou imediatamente após qualquer incidente.
**Logs de Auditoria**: Todo uso de chave de API é registrado no seu [Audit Trail](/security/rbac/) com timestamp, IP e ferramenta executada.
**Validação de Escopo**: O Vectora impõe escopo na camada [Guardian](/security/guardian/) — chaves não ignoram bloqueios hard-coded.

> [!TIP]
> Combine Chaves de API com [SSO](/auth/sso/) para usuários humanos e [Trust Folders](/security/trust-folder/) para isolamento de filesystem. Chaves de API garantem acesso lógico; políticas de segurança impõem limites de runtime.

## Gestão do Ciclo de Vida das Chaves

| Ação          | Dashboard                               | CLI                                                     |
| ------------- | --------------------------------------- | ------------------------------------------------------- |
| Criar Chave   | `Settings → API Keys → New`             | `vectora api-key create --scope search --name "ci-bot"` |
| Revogar Chave | Botão `Revoke` (imediato)               | `vectora api-key revoke --id vca_live_...`              |
| Rotacionar    | `Rotate` (cria período de sobreposição) | `vectora api-key rotate --id vca_live_...`              |
| Ver Uso       | Medidor de quota + histórico            | `vectora api-key usage --id vca_live_...`               |

**Período de Sobreposição**: Ao rotacionar, a chave antiga permanece válida por uma janela configurável (padrão: 2h). Ambas contam contra sua quota. Isso evita downtime durante deploys de agentes ou CI/CD.

## Perguntas Frequentes

**P: Posso compartilhar uma Chave de API entre múltiplos namespaces?**
R: Não. Cada chave é estritamente vinculada a um único namespace na criação. Acesso cross-namespace requer múltiplas chaves ou [RBAC de Time](/plans/team/).

**P: O que acontece se minha chave for comprometida?**
R: Revogue-a imediatamente via dashboard ou CLI. Todas as sessões ativas usando essa chave são encerradas em segundos.

**P: Chaves de API ignoram o Guardian?**
R: Absolutamente não. O [Guardian](/security/guardian/) roda na camada de aplicação antes de qualquer execução de ferramenta, independente do método de autenticação. `.env`, `.key` e `node_modules/` permanecem inacessíveis.

---

> **Frase para lembrar**:
> _"API Keys abrem a porta. Escopos definem a sala. Guardian tranca o cofre."_
