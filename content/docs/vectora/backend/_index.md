---
title: Backend
slug: backend
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - backend
  - byok
  - concepts
  - config
  - embeddings
  - governance
  - harness-runtime
  - mcp
  - mongodb-atlas
  - persistence
  - privacy
  - protocol
  - rag
  - rbac
  - state
  - vector-search
  - vectora
  - voyage
---

{{< lang-toggle >}}
A infraestrutura de backend do Vectora foi projetada para resolver o maior gargalo dos agentes de IA modernos: a **gestão de estado em escala**. Enquanto o runtime do Vectora processa a inteligência, o backend garante que essa inteligência seja fundamentada em dados persistentes, seguros e buscáveis.

O Vectora utiliza uma arquitetura unificada baseada em **MongoDB Atlas**, permitindo que vetores, metadados e memória operacional coexistam no mesmo ecossistema.

## O Motor por Trás do Contexto

## Tópicos desta seção

| Página                                                 | Descrição                                                                                       |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [MongoDB Atlas](/backend/mongodb-atlas/)               | Por que escolhemos o Atlas e como ele serve como nossa fundação de dados.                       |
| [Busca Vetorial](/concepts/vector-search/)             | Mergulho técnico em embeddings, similaridade de cosseno e o algoritmo HNSW.                     |
| [Persistência e Memória](/concepts/state-persistence/) | Como o Vectora mantém o estado entre sessões e constrói a memória de longo prazo (`AGENTS.md`). |

## Visão Geral da Arquitetura

O backend do Vectora não é apenas um local de armazenamento; é uma extensão do **Harness Runtime**.

```mermaid
graph TD
    A[Vectora Runtime] --> B{Service Layer}
    B --> C[Vector Service]
    B --> D[Session Service]
    B --> E[Audit Service]

    subgraph "MongoDB Atlas (Gerenciado pela Kaffyn)"
        C --> F[(Documents & Vectors)]
        D --> G[(Operational State)]
        E --> H[(Audit Logs)]
    end
```

## Princípios de Backend

1. **Isolamento por Namespace (RBAC)**: O backend impõe limites rígidos. Dados de um projeto nunca se misturam com outros, garantindo privacidade multi-tenant.
2. **Atomicidade**: Vetores e metadados de código são armazenados juntos. Se um arquivo é atualizado, o índice vetorial e o documento são atualizados simultaneamente.
3. **Escalabilidade Transparente**: Usando MongoDB Atlas, o Vectora escala de pequenos projetos individuais a codebases corporativas com milhões de linhas de código sem perda de performance.
4. **Governança Ativa**: Cada interação é persistida e auditável, permitindo transparência total sobre as ações da IA.

## Modos de Backend

| Modo                    | Descrição                                                                                               | Uso Ideal                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **Gerenciado (SaaS)**   | Backend MongoDB Atlas provisionado pela Kaffyn. Zero configuração.                                      | Planos Free, Pro e Team.                       |
| **Híbrido (BYOK)**      | Você fornece as chaves de API do [Voyage](/concepts/embeddings/), mas o Atlas é gerenciado pela Kaffyn. | Controle de custo de API com facilidade infra. |
| **Enterprise / Custom** | Conexão com seu próprio cluster MongoDB Atlas ou infraestrutura on-premise.                             | Requisitos rígidos de soberania de dados.      |

## Perguntas Frequentes

**P: Onde meus vetores ficam armazenados fisicamente?**
R: Nos clusters do MongoDB Atlas gerenciados pela Kaffyn, geralmente localizados em regiões AWS ou Google Cloud de baixa latência.

**P: Meus dados de backend são usados para treinar modelos da Kaffyn?**
R: **Não.** Seguimos uma política estrita de privacidade. Seus vetores e metadados são de sua propriedade exclusiva e usados apenas para fornecer contexto ao seu agente.

**P: O backend é necessário para o modo offline?**
R: O Vectora permite caching local de alguns metadados, mas a busca vetorial semântica completa e a memória persistente de longo prazo dependem da conectividade com o backend.

---

## External Linking

| Concept           | Resource                                                   | Link                                                                                                       |
| ----------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **MongoDB Atlas** | Atlas Vector Search Documentation                          | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **MCP**           | Model Context Protocol Specification                       | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                     |
| **MCP Go SDK**    | Go SDK for MCP (mark3labs)                                 | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                                         |
| **RBAC**          | NIST Role-Based Access Control Standard                    | [csrc.nist.gov/projects/rbac](https://csrc.nist.gov/projects/rbac)                                         |
| **RAG**           | Retrieval-Augmented Generation for Knowledge-Intensive NLP | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)                                               |
| **HNSW**          | Efficient and robust approximate nearest neighbor search   | [arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320)                                               |

---

> **Frase para lembrar**:
> _"O runtime é o cérebro; o backend é a biblioteca. Sem uma biblioteca organizada, o cérebro não tem onde buscar as respostas."_

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
