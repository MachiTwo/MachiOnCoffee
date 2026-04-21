---
title: "Sub-Agents vs MCP: Ferramentas passivas vs Governança ativa"
slug: sub-agents
date: "2026-04-18T22:30:00-03:00"
draft: false
categories:
  - Deep Dive
  - Arquitetura
tags:
  - agents
  - ai
  - architecture
  - ativa
  - concepts
  - context-engine
  - embeddings
  - ferramentas
  - governança
  - guardian
  - mcp
  - mcp-protocol
  - passivas
  - rag
  - sub-agents
  - vector-search
  - vectora
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}
{{< callout type="tip" >}} **TL;DR**: MCP é um protocolo excelente para expor ferramentas. Mas expor ferramentas não é a
mesma coisa que entregar **contexto governado**. O Vectora é um Sub-Agent porque RAG de qualidade exige interceptação,
validação e orquestração que ferramentas passivas não podem fornecer. {{< /callout >}}

---

## A Pergunta Incômoda

Você provavelmente já viu o **Model Context Protocol (MCP)** funcionando: Claude lê arquivos, busca na web, executa
comandos no terminal. Funciona bem para casos simples.

Mas aqui está a pergunta que poucos fazem:

> _"Se MCP permite acesso a ferramentas... por que Vectora não é 'apenas mais um servidor MCP'?"_

A resposta curta: **porque acesso não é entendimento.**

A resposta longa é o que você vai ler abaixo.

---

## O Que MCP Faz (E Seus Limites)

## MCP: Acesso Padronizado

O [Model Context Protocol](https://modelcontextprotocol.io) padroniza como um LLM pode:

1. **Descobrir** quais ferramentas existem
2. **Chamar** essas ferramentas com argumentos estruturados
3. **Receber** resultados formatados

Pense em MCP como um contrato de interface universal. Assim como APIs REST permitem que qualquer cliente converse com um
backend, MCP permite que qualquer agent use suas ferramentas.

## O Que Funciona Bem com MCP

| Cenário                       | Por que MCP é suficiente                        |
| ----------------------------- | ----------------------------------------------- |
| Leitura pontual de um arquivo | O agent sabe qual arquivo quer                  |
| Busca web simples             | O agent formula a query e interpreta resultados |
| Execução isolada de comandos  | O agent controla o comando                      |

## O Que NÃO Funciona Bem com MCP Puro

| Cenário                       | Por que MCP sozinho falha                                                              |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| **RAG em codebases grandes**  | Agentes principais não têm modelo de embedding para busca semântica                    |
| **Segurança consistente**     | Blocklists dependem de prompts (vulneráveis a jailbreak)                               |
| **Isolamento entre projetos** | Sem namespace/RBAC, há risco de vazamento de contexto                                  |
| **Validação de qualidade**    | Sem interceptação interna, não há métricas de `tool_accuracy` ou `retrieval_precision` |
| **Failover entre providers**  | Agente principal lida com erro de cada API individualmente                             |

---

## Por Que Vectora é um Sub-Agent Completo

### A Decisão Arquitetural

A escolha de construir Vectora como um **Sub-Agent** — e não como servidor MCP genérico — foi deliberada:

````text
Agente Funcional = Modelo de Linguagem + Harness de Orquestração
```text

No caso do Vectora:

```text
Vectora = Gemini 3.5 (LLM) + Voyage 4 (Embeddings) + Harness Runtime (TypeScript)
```text

O **Harness** é a camada crítica que:

- Intercepta tool calls **antes** da execução para validar segurança
- Decide **o que**, **como** e **quando** buscar contexto
- Roteia entre providers com fallback automático
- Sanitiza outputs **antes** de retornar ao agente principal
- Coleta métricas de precisão e segurança em tempo real

Nenhuma dessas responsabilidades pode ser delegada ao agente principal sem perder controle.

---

## Parte 1: O Desafio Técnico dos Embeddings

## A Realidade dos Agentes Principais em 2026

| Agent Principal | Embedding Integrado? | RAG Nativo?    | Observação                            |
| --------------- | -------------------- | -------------- | ------------------------------------- |
| GitHub Copilot  | Não                  | Não            | Autocomplete, não RAG profundo        |
| Cursor          | Não                  | Não            | Indexação própria, não extensível     |
| Claude Code     | Não                  | Não            | Espera contexto pronto                |
| Gemini CLI      | Via API cloud        | Não localmente | Sem pipeline integrado                |
| Windsurf/Trae   | Não                  | Não            | Features próprias, não interoperáveis |

## Por Que Isso Importa para RAG Real

Para recuperar contexto relevante em um codebase, você precisa de um pipeline completo:

```text
Query → Embedding → Busca Vetorial → Filtragem → Compaction → Injeção Estruturada → LLM
```text

Cada etapa exige decisões especializadas que agentes principais não fazem:

| Etapa         | Decisão                                                        | Por que agente principal não faz      |
| ------------- | -------------------------------------------------------------- | ------------------------------------- |
| **Embedding** | Escolher `voyage-4-code` vs. `voyage-3` vs. `gemini-embedding` | Agentes não têm embeddings integrados |
| **Busca**     | Aplicar filtros por namespace, `file_type`, relevância         | MCP retorna dados brutos              |
| **Filtragem** | Manter head/tail de outputs grandes + pointers                 | Limite de contexto exige decisão      |
| **Injeção**   | Estruturar contexto com metadados e dependências               | Relações se perdem em texto plano     |

## A Solução Vectora: Interpreter Especializado

```text
Agente Principal → Vectora (Camada de Interpretação) → Contexto Estruturado
                      ↓
               Context Engine decide:
               - Que informação buscar?
               - De quais fontes?
               - Com quais filtros?
               - Como estruturar para o LLM?
```text

---

## Parte 2: O Desafio Estratégico do Controle

## O Que Você Perde Sem Sub-Agent

Mesmo para ferramentas que NÃO envolvem embeddings, atuar como servidor MCP genérico significa perder:

| Recurso                  | Por que importa                                                     | Sem Sub-Agent                                            |
| ------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------- |
| **Harness**              | Valida _como_ o agente usou as tools                                | Sem métricas de `tool_sequence` ou `security_compliance` |
| **Guardian Middleware**  | Blocklist hard-coded (`.env`, `.key`) executada antes de tool calls | Depende de prompts (vulnerável a jailbreak)              |
| **Namespace RBAC**       | Isolamento real entre projetos                                      | Acesso direto ao filesystem (risco de vazamento)         |
| **Failover Automático**  | Roteia entre providers se um falhar                                 | Agente principal lida com cada erro                      |
| **Tool Calling Estável** | Adapter normaliza quirks entre SDKs                                 | Parsing frágil, tool calls inconsistentes                |

## A Ilusão do "Treinamento via Docs"

Você pode escrever `AGENTS.md`, `CLAUDE.md` para ensinar o agente a usar as ferramentas. Mas docs NÃO resolvem problemas
de runtime:

```yaml
# O que docs CONSEGUEM fazer:
 Ensinar formato esperado de argumentos
 Sugerir sequência recomendada
 Documentar políticas de segurança

# O que docs NÃO CONSEGUEM fazer:
 Validar argumentos antes da execução (Native Struct Validation)
 Bloquear tool calls perigosas em runtime
 Interceptar e medir métricas de precisão
 Garantir isolamento de namespace
 Controlar fallover entre providers
 Acessar SDK do provider para parsing estável
 Sanitizar output antes de retornar ao agente
```text

> **Prompts são sugestões. Código é lei.** Vectora escolheu código para segurança, validação e governança.

---

## Comparação Direta: Cenário Real

### Cenário: "Refatore o módulo de autenticação para adicionar expiração JWT"

#### Abordagem: MCP Tools Genérico

```text
1. Claude Code lê: file_read("src/auth.go")
2. Claude busca: grep_search("JWT", "*.go")
3. Claude recebe: 47 arquivos (muitos irrelevantes)
4. Claude filtra manualmente (consome tokens)
5. Claude propõe refatoração
6. Claude escreve: file_write() → modifica arquivo
```text

**Problemas**:

- Não há validação de que `auth.go` era o arquivo **principal**
- 39 dos 47 arquivos recuperados eram ruído
- Não há bloqueio se `file_write` tentasse modificar `.env`
- Não há snapshot Git automático antes da escrita
- Sem métricas: não há como provar que funcionou melhor

#### Abordagem: Vectora Sub-Agent

```text
1. Claude Code delega: refactor_with_context(module="auth", change="add_jwt_expiry")
   ↓
2. Vectora intercepta e valida:
   - Namespace validation
   - Guardian: blocklist check
   ↓
3. Context Engine decide:
   - Buscar em filesystem + vector search?
   - Com quais filtros de namespace?
   ↓
4. Vectora retorna contexto estruturado:
   - 5 arquivos relevantes (relevance ≥ 0.75)
   - 0 arquivos bloqueados
   - embedding_model: voyage-4-code
   - retrieval_precision: 0.89
   ↓
5. Claude propõe refatoração com contexto validado
   ↓
6. Vectora executa file_write com:
   - Git snapshot automático
   - Lint + type-check
   - Output sanitization
```text

**Vantagens**:

- Validação **antes** da execução
- Métricas objetivas: `retrieval_precision: 0.89`, `tool_accuracy: 1.0`
- Segurança por código (Guardian hard-coded)
- Isolamento por namespace (RBAC real)
- Prova de valor: `--compare vectora:on,off`

---

## Arquitetura: Camadas Exclusivas do Sub-Agent

### Runtime TypeScript

```typescript
export class VectoraSubAgent {
  // 1. Tool Router com validação nativa (fail-fast)
  private router: ToolRouter;

  // 2. Guardian middleware (hard-coded, imutável)
  private guardian: Guardian;

  // 3. Context Engine (decisão multi-hop)
  private contextEngine: ContextEngine;

  // 4. Harness (interceptação e métricas)
  private harnessInterceptor?: HarnessInterceptor;

  // 5. Provider adapter (failover automático)
  private providerAdapter: ProviderAdapter;

  async execute(request: AgentRequest): Promise<AgentResponse> {
    // Validação de namespace ANTES de qualquer ação
    if (!this.guardian.validateNamespace(request.namespace)) {
      throw new SecurityError(`Namespace validation failed`);
    }

    // Interceptação para Harness (coleta métricas em tempo real)
    if (this.harnessInterceptor) {
      await this.harnessInterceptor.onCall(request);
    }

    // Decisão de contexto: o que/como/quando buscar
    const context = await this.contextEngine.build(request);

    // Execução com validação via Go Struct Tags
    const result = await this.router.execute(request.tool, request.args, context);

    // Sanitização de output antes de retornar ao agente
    const sanitized = this.guardian.sanitizeOutput(result);

    return {
      context: sanitized,
      metrics: this.collectMetrics(),
      audit: this.generateAuditLog(request, result),
    };
  }
}
```text

### Contraste: Tool MCP Genérica

```typescript
// Tool MCP: função passiva, sem governança
export async function file_read(args: { path: string }): Promise<string> {
  // Sem validação de namespace
  // Sem blocklist do Guardian
  // Sem interceptação para Harness
  // Sem sanitização de output
  // Sem métricas de observabilidade

  return fs.readFileSync(args.path, "utf-8");
}
```text

> **Diferença fundamental**:
>
> - MCP tools = funções passivas
> - Vectora Sub-Agent = sistema ativo de governança

---

## Impacto para Você

## Desenvolvedores

| Benefício      | Como Sub-Agent Entrega                                             |
| -------------- | ------------------------------------------------------------------ |
| **Confiança**  | Segurança por código (Guardian), não por prompt                    |
| **Qualidade**  | Harness prova objetivamente melhorias (`+42% retrieval_precision`) |
| **Controle**   | Você decide namespaces, providers, políticas                       |
| **Eficiência** | Context Engine evita overfetch (menos tokens)                      |

## Equipes

| Benefício       | Como Sub-Agent Entrega                        |
| --------------- | --------------------------------------------- |
| **Governança**  | RBAC por namespace + audit logs via Harness   |
| **Colaboração** | Namespaces compartilhados com isolamento real |
| **Evolução**    | Harness detecta regressões antes de deploy    |
| **Custo**       | Redução mensurável de tokens (ROI comprovado) |

### Integradores

| Benefício              | Como Sub-Agent Entrega                                                    |
| ---------------------- | ------------------------------------------------------------------------- |
| **Interoperabilidade** | MCP/ACP padrão — integra com Claude Code, Gemini CLI, Cursor              |
| **Extensibilidade**    | Provider-agnostic — troque `gemini-3.5` por `gemini-3.1-pro` sem mudanças |
| **Validação**          | Harness como serviço — valide seu próprio agente                          |
| **Foco**               | Você constrói a experiência; Vectora cuida do contexto                    |

---

## E Se Eu Quiser Apenas MCP Tools?

Você **pode** usar Vectora em modo simplificado:

```bash
vectora-agent mcp-serve --mode tools-only
```text

**O que você ganha**:

- Integração rápida com qualquer client MCP
- Menor overhead de configuração

**O que você perde**:

- Context Engine inteligente (decide o que/como buscar)
- Harness (prova objetiva de qualidade)
- Guardian middleware (segurança por código)
- Namespace isolation (RBAC real)
- Failover automático entre providers
- Métricas de `retrieval_precision` e `tool_accuracy`

> **Recomendação**: Comece com o Sub-Agent completo. A maioria dos usuários descobre que as camadas de controle são
> justamente o que faltava para confiar em produção.

---

## Conclusão

> **Vectora não é um conjunto de tools MCP. É a camada que faz qualquer agente funcionar melhor em código — com
> controle, validação e segurança por design.**

| Se você quer...                                                | Use...                |
| -------------------------------------------------------------- | --------------------- |
| Tools genéricas de arquivo/busca                               | MCP tools do mercado  |
| **Contexto correto + execução confiável + validação objetiva** | **Vectora Sub-Agent** |

> **Frase para guardar**: _"Tools MCP te dão funções. Vectora Sub-Agent te dá governança."_

---

<!-- Parte do ecossistema Vectora · Open Source · Provider-Agnostic -->
````
