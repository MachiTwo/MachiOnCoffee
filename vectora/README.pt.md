# Vectora

> [!TIP]
> Read this file in another language | Leia esse arquivo em outro idioma.
> [English](README.md) | [Português](README.pt.md)

> [!NOTE]
>
> **Contexto correto + execução confiável para desenvolvedores.**
> O sub-agent especialista que potencializa qualquer agent principal em codebases reais.

---

**Agents tradicionais operam em contexto fragmentado.
O Vectora entrega contexto conectado.**

- busca semântica via Qdrant (HNSW + quantization)
- estrutura de código (arquivos, funções, dependências)
- namespaces isolados com RBAC via Supabase
- raciocínio multi-hop com Context Engine

Resultado: agents que entendem como seu sistema realmente funciona — não apenas trechos isolados.

---

## ✨ Destaques

- **Sub-Agent Specialist**: Integra-se via MCP/ACP a Claude Code, Gemini CLI, Cursor e IDEs — sem competir, apenas potencializando.
- **Context Engine Inteligente**: Decide _o que_, _como_ e _quando_ buscar — evita ruído, reduz tokens, entrega contexto estruturado.
- **Namespaces com RBAC**: Isolamento real entre projetos; namespaces públicos compartilhados (Godot, TypeScript, Rust) como "skills" prontas.
- **Hard-Coded Guardian**: Blocklist imutável (.env, .key, .pem, binários) — segurança por código, não por prompt.
- **Provider-Agnostic**: OpenAI, Gemini, Claude, OpenRouter ou llama.cpp local — escolha sua stack, mantenha a mesma interface.
- **Harness de Validação**: Prova objetiva de qualidade com `vectora harness run --compare vectora:on,off`.
- **Cloud-First, Local-Optional**: Qdrant + Supabase + Vercel gerenciados; opção de inferência local via llama.cpp para privacidade extrema.
- **Zero Infra para o Usuário**: `npm install -g vectora-agent` — sem Kubernetes, sem gerenciamento de banco de dados.

---

## 🎯 Para Quem é o Vectora?

| Perfil                       | Por que usar                                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Desenvolvedor Individual** | Entenda codebases legados, refatore com confiança, gere testes contextualizados — sem perder tempo navegando manualmente.                        |
| **Equipes de Engenharia**    | Namespaces compartilhados com RBAC: documentação interna, padrões de arquitetura e decisões técnicas disponíveis como contexto para todo o time. |
| **Integradores de Agents**   | Adicione RAG preciso e execução confiável ao seu agent Tier-1 via MCP — sem reconstruir o motor de contexto.                                     |
| **Privacy-First Users**      | Modo local opcional com llama.cpp: inferência 100% offline, dados nunca saem da sua máquina.                                                     |

> 💡 **Vectora não é um agent autônomo.**  
> É a camada que faz qualquer agent funcionar melhor em código.

---

## 🏗️ Arquitetura EndGame

```
[IDE / Agent Principal]
         ↓ MCP / ACP (stdio)
[Vectora Agent - TypeScript Runtime]
         ├── Protocol Layer: @modelcontextprotocol/server + JSON-RPC
         ├── Tool Router + Guardian Middleware (security first)
         ├── Context Engine: decide o que/como/quando buscar
         ├── Provider Adapter: OpenAI/Gemini/Claude/OpenRouter/llama.cpp
         │
         ├── Qdrant Cloud → Vector Search (payload filtering por namespace)
         └── Supabase → Auth, Projects, Metadata, RLS policies
```

### Stack Oficial

| Camada              | Tecnologia                              | Por que escolhemos                                                                   |
| ------------------- | --------------------------------------- | ------------------------------------------------------------------------------------ |
| **Runtime**         | TypeScript + Node.js 20+                | Ecossistema maduro para MCP/ACP, AI SDK da Vercel pronto para streaming/tool calling |
| **Vector DB**       | Qdrant Cloud (multi-tenant)             | HNSW nativo, payload filtering, quantization, escala sem operação                    |
| **Metadata/Auth**   | Supabase (Postgres + Auth + RLS)        | Row Level Security nativo, realtime, integração simples com Next.js                  |
| **API/Edge**        | Vercel Functions + AI Gateway           | Serverless, edge-ready, billing integrado, zero infra para gerenciar                 |
| **Dashboard**       | Next.js 14 + Tailwind                   | Landing + configuração + billing em um único app, deploy automático                  |
| **Local Inference** | llama.cpp via `@vectora/llama-provider` | Privacidade total opcional, sem depender de APIs externas                            |

---

## 🔌 Protocolos de Integração

### MCP (Model Context Protocol)

Para integração com agents Tier-1: Claude Code, Gemini CLI, Antigravity, etc.

```bash
# No seu config.json do Claude Desktop:
{
  "mcpServers": {
    "vectora": {
      "command": "npx",
      "args": ["vectora-agent", "mcp-serve"],
      "env": {
        "VECTORA_API_KEY": "sua_chave_aqui"
      }
    }
  }
}
```

- **Foco em Contexto**: O Vectora expõe tools de RAG, filesystem e análise de código.
- **Tool Calling Estável**: AI SDK + adapter layer normaliza respostas entre providers.
- **Streaming Nativo**: Tokens chegam em tempo real, sem buffering artificial.

### ACP (Agent Client Protocol)

Para integração direta com IDEs via JSON-RPC 2.0 over stdio/Unix Sockets.

- **Baixa Latência**: Alvo <100ms do evento da IDE até resposta do contexto.
- **Escopo Restrito**: Todas as operations validam Trust Folder + namespace antes de executar.
- **Fallback Transparente**: Se o provider primário falhar, roteia automaticamente para o fallback configurado.

---

## 🤖 IA Agnóstica: Escolha Seu Provider

O Vectora não te prende a nenhum provedor. Configure via CLI ou dashboard:

```bash
# Exemplo: OpenRouter como gateway unificado
vectora config --provider openrouter --key $OPENROUTER_KEY

# Exemplo: Gemini para multimodalidade
vectora config --provider gemini --key $GEMINI_KEY

# Exemplo: Modo local com llama.cpp
vectora config --provider local --model ~/.vectora/models/qwen3-1.7b-instruct.Q4_K_M.gguf
```

### Providers Suportados

| Provider       | SDK                       | Modelos                                 | Modo         |
| -------------- | ------------------------- | --------------------------------------- | ------------ |
| **OpenRouter** | `ai` + OpenAI compat.     | Qualquer modelo no gateway              | Cloud        |
| **Google**     | `@google/genai`           | Gemini 2.0 Flash/Pro, Embedding 2.0     | Cloud        |
| **Anthropic**  | `@anthropic-ai/sdk`       | Claude 3.5/3.7 Sonnet/Opus              | Cloud        |
| **Alibaba**    | `openai` compat.          | Qwen3.5, Qwen3-Embedding                | Cloud        |
| **Local**      | `@vectora/llama-provider` | Qwen3-1.7B, Gemma3, Phi-4 via llama.cpp | 100% Offline |

> [!TIP]
> **Gateway Support**: Aponte para OpenRouter ou qualquer gateway OpenAI-compatible para fazer load balancing entre modelos sem mudar configuração.

---

## 🧩 Toolkit Agêntico (Core Tools)

Todas as tools são expostas via schema JSON, validadas por Zod antes da execução:

### Filesystem & Code

| Tool          | Descrição                                           | Escopo                   |
| ------------- | --------------------------------------------------- | ------------------------ |
| `file_read`   | Leitura paginada de arquivos (suporta grandes)      | Trust Folder + namespace |
| `file_write`  | Escrita controlada com Git snapshot automático      | Trust Folder + namespace |
| `file_edit`   | Patching cirúrgico sem reescrever o arquivo inteiro | Trust Folder + namespace |
| `file_list`   | Listagem recursiva com metadados de estrutura       | Trust Folder + namespace |
| `file_find`   | Busca por glob patterns (`**/*.ts`, `src/**/*.tsx`) | Trust Folder + namespace |
| `grep_search` | Busca regex via ripgrep com filtros e limite        | Trust Folder + namespace |

### Context & RAG

| Tool             | Descrição                                     | Diferencial                             |
| ---------------- | --------------------------------------------- | --------------------------------------- |
| `context_search` | Busca semântica + estrutural no codebase      | Context Engine decide o que buscar      |
| `context_ingest` | Indexação sob demanda de arquivos/diretórios  | Multi-modal: texto, PDF, imagem, áudio  |
| `context_build`  | Composição de contexto estruturado para o LLM | Evita overfetch, entrega só o relevante |

### Web & External

| Tool         | Descrição                                       | Segurança                                             |
| ------------ | ----------------------------------------------- | ----------------------------------------------------- |
| `web_fetch`  | Fetch de URL com extração de conteúdo relevante | Sanitização de output, bloqueio de domains maliciosos |
| `web_search` | Busca web para contexto externo atualizado      | Resultados filtrados por relevância e frescor         |

### System & Memory

| Tool           | Descrição                                                  | Uso                                             |
| -------------- | ---------------------------------------------------------- | ----------------------------------------------- |
| `terminal_run` | Execução de comandos com stdout/stderr em tempo real       | Timeout configurável, approval opcional         |
| `memory_save`  | Persistência de fatos/preferências (global ou por projeto) | Isolado por namespace, criptografado em repouso |
| `plan_mode`    | Modo estruturado para validar plano antes de executar      | UX para revisão humana de ações complexas       |

> [!IMPORTANT]
> **Hard-Coded Guardian**: Todas as tools validam paths contra blocklist imutável (.env, .key, .pem, binários, lockfiles). Arquivos bloqueados nunca são lidos, embedados ou enviados ao LLM — independente do provider ou prompt.

---

## 🔐 Segurança por Design

### Hard-Coded Guardian (TypeScript Middleware)

```ts
// packages/core/src/security/guardian.ts
export const HARD_BLOCKLIST = [
  /\.env(\..+)?$/,
  /\.key$/,
  /\.pem$/,
  /\.crt$/,
  /\.p12$/,
  /(^|\/)\.git\//,
  /(^|\/)node_modules\//,
  /(^|\/)\.venv\//,
  /\.(bin|exe|dll|so|dylib|pyc|pyo)$/,
  /^(package-lock\.json|pnpm-lock\.yaml|yarn\.lock)$/,
];

export class Guardian {
  static isBlocked(path: string): boolean {
    return HARD_BLOCKLIST.some((pattern) => pattern.test(path));
  }

  static sanitizeOutput(content: string): string {
    return content
      .replace(
        /(?:aws_access_key_id|aws_secret_access_key)\s*[:=]\s*['"]?[\w+/]{20,}['"]?/gi,
        "[REDACTED_AWS]",
      )
      .replace(/ghp_[\w]{36}/g, "[REDACTED_GITHUB]")
      .replace(/sk-[a-zA-Z0-9]{48}/g, "[REDACTED_OPENAI]");
  }
}
```

### Namespaces com RBAC (Supabase + Qdrant)

```yaml
# Exemplo: namespace público godot-4.6-api
namespace:
  id: "godot-4.6-api"
  visibility: "public" # public | team | private
  owner: "kaffyn"
  rbac:
    read: ["*"] # qualquer usuário autenticado pode ler
    write: ["org:kaffyn"] # só a organização dona pode atualizar
    delete: ["org:kaffyn"]
```

- **Supabase RLS**: Row Level Security no Postgres para controle de metadados e permissões.
- **Qdrant Payload Filtering**: Todas as queries vetoriais incluem filtro obrigatório por `namespace_id` + `visibility`.
- **Isolamento Real**: Contextos nunca vazam entre namespaces; você controla quais estão "montados" na sessão.

### Trust Folder + Symlink Protection

```ts
// Validação de escopo antes de qualquer operação
export function validateTrustFolder(
  requestedPath: string,
  trustFolder: string,
): boolean {
  const resolved = fs.realpathSync(requestedPath);
  const normalizedTrust = path.resolve(trustFolder);
  return resolved.startsWith(normalizedTrust);
}
```

---

## 🧪 Vectora Harness: Validação Objetiva

> [!NOTE]
> O Harness NÃO valida "inteligência geral". Ele valida **consistência operacional + uso correto de contexto + segurança de execução**.

### Objetivo

Garantir que qualquer agent usando o Vectora → se comporte melhor, mais seguro e mais previsível.

### Feature Chave: Comparativo Objetivo

```bash
# Executa suite de testes com e sem Vectora, gera diff estruturado
vectora harness run ./tests --compare vectora:on,vectora:off
```

Resultado:

```json
{
  "suite_score_delta": "+22%",
  "retrieval_precision_delta": "+31%",
  "token_usage_delta": "-18%",
  "security_violations": { "with_vectora": 0, "without_vectora": 3 },
  "failures": { "with_vectora": 1, "without_vectora": 7 }
}
```

### Tipos de Testes

| Tipo           | Valida                                        | Exemplo YAML                                                        |
| -------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| **Tooling**    | Sequência correta de tools, args válidos      | `strict_sequence: [{tool: "file_read", args: {path: "auth.go"}}]`   |
| **Retrieval**  | Achou os arquivos certos, ignorou ruído       | `must_include: ["auth.go"], must_exclude: ["unrelated/logger.go"]`  |
| **Reasoning**  | Resposta correta, conclusão válida            | `semantic_checks: [{pattern: "expiration", case_sensitive: false}]` |
| **Safety**     | Não vaza segredos, não acessa .env            | `blocked_tools: ["terminal_run"], blocked_paths: [".env"]`          |
| **Resilience** | Recupera-se de falhas (timeout, erro parcial) | `fault_injection: [{type: "timeout", tool: "file_read"}]`           |

> 💡 **Isso é arma de produto**: Prova objetiva de que Vectora melhora qualidade, reduz custos e aumenta segurança.

---

## 🌐 Shared Namespaces: Asset Library

O **Vectora Assets** é um catálogo de namespaces compartilhados com RBAC — não um marketplace tradicional.

### Namespaces Públicos (Curated)

Disponíveis para montagem instantânea em qualquer workspace:

| Namespace         | Conteúdo                                    | Uso                                               |
| ----------------- | ------------------------------------------- | ------------------------------------------------- |
| `godot-4.6-api`   | Documentação oficial + exemplos de GDScript | "Como implementar um estado machine em Godot?"    |
| `typescript-docs` | Specs da linguagem + padrões de tipagem     | "Qual a diferença entre `unknown` e `any`?"       |
| `rust-patterns`   | Idiomas, traits e padrões de concorrência   | "Como compartilhar estado entre threads em Rust?" |
| `web-security`    | OWASP Top 10, headers, CSP, autenticação    | "Quais headers de segurança devo configurar?"     |

### Como Usar

```bash
# Listar namespaces públicos disponíveis
vectora assets list

# Montar um namespace público no workspace atual
vectora assets mount godot-4.6-api

# Desmontar
vectora assets unmount godot-4.6-api

# Publicar um namespace como público (requer aprovação)
vectora assets publish ./my-docs --namespace my-lib --visibility public
```

> [!IMPORTANT]
> **Política de Privacidade**: Namespaces `private` e `team` permanecem exclusivamente na sua instância do Qdrant/Supabase. **Nem a Kaffyn tem acesso aos dados contidos em workspaces privados ou de equipe.**

---

## 🚀 Quick Start

### Instalação

```bash
# Instale globalmente via npm
npm install -g vectora-agent

# Verifique a instalação
vectora-agent --version
```

### Configuração Inicial

```bash
# Configurar provider (ex: OpenRouter)
vectora-agent config --provider openrouter --key $OPENROUTER_KEY

# Configurar backend cloud (opcional, padrão já vem pré-configurado)
vectora-agent config --qdrant-url $QDRANT_URL --supabase-url $SUPABASE_URL

# Ou ativar modo local com llama.cpp
vectora-agent setup-local --model qwen3-1.7b-instruct
```

### Execução

```bash
# Iniciar como MCP server (para Claude Code, Gemini CLI, etc)
vectora-agent mcp-serve

# Ou iniciar como ACP client para um projeto específico
vectora-agent acp-start --workspace ./my-project

# Usar CLI básico para tarefas rápidas
vectora-agent ask "Quais funções dependem do módulo de autenticação?"
vectora-agent embed --path ./docs/
vectora-agent search "padrão repository pattern"
```

### Integração com VS Code

1. Instale a extensão **Vectora** da marketplace
2. A extensão já inclui o binário do Agent — sem setup adicional
3. Use o painel dedicado para chat interativo ou invoque como sub-agent via comando

---

## 💰 Modelos de Uso

### 🟢 Free (BYOK - Bring Your Own Keys)

- Todas as tools e Context Engine incluídos
- Você fornece suas próprias chaves de API (OpenRouter, Gemini, etc.)
- Qdrant + Supabase: use suas próprias instâncias ou o tier free da Kaffyn
- Harness completo para validação local
- **Custo**: $0 + suas APIs

### 🔵 Pro (~$20/mês)

- Qdrant + Supabase gerenciados pela Kaffyn (multi-tenant, auto-scaling)
- Embeddings limitados incluídos (ex: 100k tokens/mês)
- Dashboard com usage tracking, billing e gestão de API keys
- Suporte prioritário e acesso antecipado a features
- **Ideal para**: Desenvolvedores profissionais que querem zero configuração

### 🟣 Team (Custom)

- Namespaces compartilhados com RBAC granular
- Múltiplos usuários, isolamento por projeto/time
- Audit logs, SSO opcional, SLA garantido
- **Ideal para**: Equipes de engenharia que precisam de conhecimento compartilhado seguro

---

## 📦 Estrutura do Projeto (Monorepo)

```
vectora/
├── packages/
│   ├── core/          # Agent runtime: protocols, tools, security, context engine
│   ├── llm/           # Providers: openai, gemini, claude, openrouter, llama.cpp
│   ├── context/       # Context Engine + RAG multi-namespace + multi-hop
│   ├── harness/       # Validation system: runner, judge, schema (Zod)
│   └── shared/        # Types, utils, config, logger, constants
│
├── apps/
│   ├── agent/         # Entry point: MCP/ACP server, CLI commands
│   └── web/           # Next.js: landing + dashboard + billing + auth
│
├── infra/
│   ├── qdrant/        # Collections config, quantization, payload indexes
│   ├── supabase/      # Migrations, RLS policies, auth/projects schema
│   └── vercel/        # Functions config, AI Gateway, edge settings
│
├── assets/            # Shared namespaces definitions (YAML)
│   ├── public/
│   │   ├── godot-4.6-api.yaml
│   │   ├── typescript-docs.yaml
│   │   └── rust-patterns.yaml
│   └── README.md      # Como publicar um namespace público
│
├── tests/
│   ├── e2e/           # MCP/ACP integration tests
│   ├── harness-suites/# YAML test cases (security, retrieval, resilience)
│   └── fixtures/      # Small codebases for testing
│
├── package.json       # pnpm workspace + turbo
├── tsconfig.json      # Base config + paths aliases
└── README.md          # Você está aqui
```

---

## 🤝 Contribuindo

Vectora é open source e construído pela comunidade. Contribuições são bem-vindas!

### Primeiros Passos

```bash
# Clone o repo
git clone https://github.com/Kaffyn/Vectora.git
cd Vectora

# Instale dependências (pnpm + turbo)
pnpm install

# Rode o agent em modo desenvolvimento
pnpm --filter agent dev

# Rode os testes do Harness
pnpm --filter harness test
```

### Diretrizes

- **TypeScript estrito**: Sem `any`, tipos explícitos, Zod para validation boundaries
- **Tests primeiro**: Nova tool? Escreva o teste no Harness antes da implementação
- **Security by default**: Nenhuma feature que bypass o Guardian ou Trust Folder
- **Docs atualizadas**: Mudou a API? Atualize o schema e os exemplos

### Roadmap Público

- [ ] Harness: LLM-as-a-Judge com cache de julgamentos
- [ ] Context Engine: Multi-hop com ranking híbrido (semântico + estrutural)
- [ ] Assets: Sistema de curadoria comunitária para namespaces públicos
- [ ] IDEs: Suporte nativo para JetBrains via ACP estrito
- [ ] Local: Otimizações para llama.cpp em Apple Silicon / NVIDIA CUDA

---

## ❓ FAQ

**P: Vectora é um agent autônomo?**  
R: Não. Vectora é um sub-agent especialista em contexto de código. Você o aciona via MCP/ACP durante o desenvolvimento — ele não roda 24/7 nem toma decisões sem seu comando.

**P: Preciso de conta na Kaffyn?**  
R: Para o modo Free (BYOK), não. Para Pro/Team ou para usar namespaces públicos, sim — autenticação via Supabase Auth.

**P: Meus dados vão para a nuvem?**  
R: Apenas se você configurar o backend cloud. No modo local, tudo roda na sua máquina. Namespaces `private` nunca saem da sua instância, mesmo no cloud.

**P: Posso usar Vectora com Cursor / Copilot / Antigravity?**  
R: Sim! Via MCP, qualquer client compatível pode usar o Vectora como sub-agent. Para IDEs com ACP nativo (VS Code), a integração é ainda mais profunda.

**P: E se o provider de IA cair?**  
R: O Agent tem failover automático. Configure um provider secundário e, em caso de erro (429, timeout, outage), a requisição é roteada transparentemente — sua IDE não percebe a troca.

---

## 📄 Licença

Vectora é distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

> 💡 **Frase para guardar**:  
> _"Vectora não compete com o agent. Ele torna qualquer agent competente em código."_

---

_Parte do ecossistema Kaffyn · Open Source · TypeScript · Provider-Agnostic_  
