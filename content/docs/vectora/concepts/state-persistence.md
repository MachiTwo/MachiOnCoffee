---
title: "Persistência de Estado e Memória"
type: docs
sidebar:
  open: true
---

{{< lang-toggle >}}

## O Problema: Agentes Sem Memória (Stateless)

A maioria das ferramentas de IA opera em um modelo _stateless_ (sem estado): cada pergunta é uma nova folha em branco. Para aplicações de código, isso é desastroso. Se o agente esquece que você já explicou que a porta do banco de dados mudou, ou que ele não deve mexer na pasta `src/legacy`, ele cometerá os mesmos erros repetidamente.

O Vectora resolve isso através de um sistema de **Persistência de Estado e Memória Operacional**.

---

## Memória de Curto Prazo vs. Longo Prazo

No Vectora, a persistência é dividida em camadas para otimizar a performance e o custo de tokens:

### 1. Memória Operacional (Curto Prazo)

Reside na coleção `sessions` do MongoDB Atlas.

- **Duração**: Sessão atual do MCP (ativa enquanto o agent principal está rodando).
- **Conteúdo**: Histórico das ferramentas chamadas, planos de execução temporários e outputs de ferramentas recentes.
- **Uso**: Garante que se o agente listou arquivos em um passo, ele não precise listar novamente no próximo passo da mesma tarefa.

### 2. Memória Persistente (Longo Prazo/AGENTS)

Reside na coleção `memory` e é espelhada no arquivo `AGENTS.md` (opcional).

- **Duração**: Vitalícia para o namespace.
- **Conteúdo**: Fatos aprendidos ("O projeto usa Clean Architecture"), regras de segurança ("Nunca edite arquivos .pem"), e preferências do usuário ("Prefira usar `async/await` ao invés de callbacks").
- **Uso**: Fornece o "DNA" do projeto ao agente assim que ele é inicializado.

---

## Como Funciona a Persistência

### Operação via MongoDB Atlas

Quando o agente principal envia uma requisição via MCP, o Vectora:

1. **Recupera o Estado**: Lê a sessão ativa no Atlas.
2. **Injeta Contexto de Memória**: Carrega as regras relevantes do `AGENTS.md` persistido.
3. **Atualiza em Tempo Real**: Cada decisão tomada pelo [Context Engine](/concepts/context-engine/) é gravada no banco.

---

## Auditoria e Governança

A persistência no backend não serve apenas para a IA; serve para o desenvolvedor.

### Audit Logs (Coleção `audit_logs`)

O Vectora registra metadados imutáveis de cada operação:

- **Timestamp**: Milisegundo exato.
- **Identidade**: Qual API Key ou usuário executou.
- **Ferramenta**: `file_edit`, `context_search`, etc.
- **Status**: Sucesso ou Erro (incluindo logs de erro do Harness).

Isso permite que times de segurança e líderes técnicos auditem **exatamente** o que os agentes estão fazendo na codebase.

---

## Isolação e Criptografia (RBAC)

A persistência de estado é rigorosamente isolada por **Namespace**.

- Um agente rodando no `namespace: front-end` jamais verá a memória ou o estado da sessão do `namespace: back-end`.
- Os dados sensíveis no estado (como trechos de código em memória) são criptografados em repouso no MongoDB Atlas (AES-256).

---

## Otimização: Session Compaction

Sessões de agentes podem se tornar imensas, estourando o limite de contexto do LLM. O Vectora aplica **Compaction** no backend:

- **Pruning**: Remove detalhes de ferramentas que falharam ou foram sobrescritas por ações de sucesso.
- **Summarization**: Resume blocos de pensamento intermediários, mantendo apenas as conclusões e fatos críticos.
- **Head/Tail management**: Mantém o início (objetivo) e o fim (estado atual) com detair, compactando o meio.

---

## FAQ de Persistência

**P: Onde fica salvo o arquivo `AGENTS.md`?**
R: Ele é armazenado de forma persistente no MongoDB Atlas. Você também pode habilitar a sincronização para um arquivo físico na raiz do seu projeto para que ele possa ser versionado no Git.

**P: Posso limpar a memória do agente?**
R: Sim. Você pode resetar uma sessão específica via `vectora session reset --id <session_id>` ou limpar a memória persistente do namespace pelo dashboard.

**P: Como o Vectora evita que a memória do agente fique "poluída" com informações erradas?**
R: Através dos **Verification Hooks** do [Harness](/concepts/harness/). Se uma operação falha ou o output é considerado irrelevante, o Harness impede que esse fato seja consolidado na memória persistente.

---

> **Frase para lembrar**:
> _"Inteligência sem memória é apenas um cálculo. Com a persistência do Vectora, seu agente ganha experiência."_
