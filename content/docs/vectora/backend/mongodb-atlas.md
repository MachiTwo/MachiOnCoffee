---
title: MongoDB Atlas
slug: mongodb-atlas
date: "2026-04-18T22:30:00-03:00"
weight: 36
type: docs
sidebar:
  open: true
tags:
  - ai
  - atlas
  - mcp
  - mongodb
  - vectora
---

{{< lang-toggle >}}

## O Desafio: Armazenamento Unificado para Agentes

Ao construir sistemas de agentes, os desenvolvedores geralmente enfrentam uma "fragmentação de dados":

- **Vetores** em Pinecone ou Qdrant.
- **Metadados** em Postgres.
- **Estado da Sessão** em Redis.
- **Logs de Auditoria** em arquivos brutos ou ELK.

Essa fragmentação introduz latência, inconsistência (race conditions entre o vetor e o metadado) e complexidade operacional. O Vectora resolve isso consolidando tudo no **MongoDB Atlas**.

---

## O Que é o MongoDB Atlas?

O **MongoDB Atlas** é uma plataforma de dados multinuvem totalmente gerenciada. Embora tenha começado como um banco de dados de documentos NoSQL, ele evoluiu para incluir uma das implementações mais robustas de **Vector Search** do mercado.

No Vectora, o Atlas não é apenas um banco de dados; é a infraestrutura que sustenta a governança de contexto.

### Especificações Técnicas (Nível Gerenciado Kaffyn)

| Recurso                | Detalhe                                           |
| ---------------------- | ------------------------------------------------- |
| **Tipo de Banco**      | Multicluster Document + Vector Search             |
| **Indexação Vetorial** | HNSW (Hierarchical Navigable Small World)         |
| **Escalabilidade**     | Sharding automático (escala de GBs a TBs)         |
| **Disponibilidade**    | 99.99% (Replica Sets em múltiplas zonas)          |
| **Criptografia**       | AES-256 em repouso + TLS 1.3 em trânsito          |
| **Backup**             | Snapshots contínuos com retenção conforme o plano |

---

## Por Que MongoDB Atlas para o Vectora?

Nós analisamos diversas alternativas (Pinecone, Milvus, Qdrant puro) e escolhemos o Atlas por três pilares fundamentais:

### 1. Atomicidade Metadado-Vetor

No Atlas, o vetor (`embedding`) e o código/documento estão no **mesmo documento JSON**. Isso elimina o problema de "vetores órfãos" ou metadados desatualizados. Se o arquivo muda, a atualização é atômica.

### 2. Filtragem de Namespace de Alta Performance

O Vectora隔离 os dados usando `namespaces`. O Atlas permite aplicar filtros de metadados (ex: `where namespace_id == 'team-a'`) **dentro** do índice HNSW. Isso garante que buscas vetoriais nunca "vazem" dados entre projetos ou usuários.

### 3. State & Memory Unificados

Diferente de bancos de dados "vector-only", o Atlas armazena perfeitamente o estado da sessão do agente e a memória persistente (`AGENTS.md`). Isso permite que o Vectora recupere o contexto histórico e os vetores semânticos em uma única conexão.

---

## Estrutura de Coleções no Vectora

O backend é organizado em coleções otimizadas para o **Harness Runtime**:

### 1. `documents` (A Fonte da Verdade)

Armazena os chunks de código, metadados de AST, paths de arquivos e os embeddings gerados pelo **Voyage 4**.

- **Índice**: HNSW sobre o campo `embedding_vector`.

### 2. `sessions` (Memória Operacional)

Armazena o histórico de interações do agente principal via MCP, as decisões tomadas pelo **Context Engine** e o estado atual do plano de execução.

### 3. `audit_logs` (Governança)

Registros imutáveis de cada ferramenta executada, quem executou, quando e qual foi o impacto (metadados apenas).

---

## Como o Vectora Otimiza o Atlas

### Indexação HNSW Inteligente

O Vectora configura dinamicamente os parâmetros `efConstruction` e `maxConnections` do índice HNSW baseando-se no tamanho da codebase do usuário, equilibrando velocidade de indexação e precisão de busca.

### Compactor & Compaction

Para economizar tokens e armazenamento, o Vectora aplica algoritmos de **compaction** antes de salvar no Atlas, removendo ruído sintático e preservando apenas o que é semanticamente relevante para o LLM.

---

## Gerenciamento Kaffyn (Zero Ops)

Quando você usa o Vectora, você não precisa configurar instâncias no console do MongoDB. A Kaffyn provisiona e gerencia o backend automaticamente:

- **Plano Free**: Cluster compartilhado otimizado, limite de 512MB, retenção de 30 dias após inatividade.
- **Plano Pro/Team**: Clusters dedicados ou serverless de alta performance, maior armazenamento e backups prioritários.
- **Segurança**: Cada usuário/time recebe credenciais isoladas e namespaces criptografados.

---

## FAQ de Backend

**P: Os dados do meu código são enviados para a nuvem?**
R: Sim, os embeddings (vetores numéricos) e metadados estruturais (AST, caminhos) são armazenados no MongoDB Atlas gerenciado pela Kaffyn. O conteúdo bruto do código é processado pelo [Guardian](/security/guardian/) para garantir que segredos nunca saiam do seu ambiente.

**P: Posso usar meu próprio cluster do MongoDB Atlas?**
R: Sim, no plano Enterprise ou através da configuração `backend.custom_connection_string`.

**P: O que acontece se o banco ficar lento?**
R: O Vectora implementa **fallback local** para buscas básicas no sistema de arquivos e caching de embeddings para manter a fluidez da IDE.

---

> **Frase para lembrar**:
> _"O MongoDB Atlas é onde o Vectora guarda o conhecimento. A inteligência está no runtime; a memória está no Atlas."_
