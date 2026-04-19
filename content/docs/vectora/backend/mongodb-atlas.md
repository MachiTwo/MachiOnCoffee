---
title: MongoDB Atlas
slug: mongodb-atlas
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
breadcrumbs: true
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

- Vetores em um provedor especializado
- Metadados em Postgres ou outro banco relacional
- Estado da sessão em Redis ou armazenamento volátil
- Logs de auditoria em sistemas separados

Essa fragmentação introduz latência, inconsistência entre sistemas e complexidade operacional significativa. O Vectora resolve isso consolidando tudo no MongoDB Atlas.

## O Que é o MongoDB Atlas

O MongoDB Atlas é uma plataforma de dados multinuvem totalmente gerenciada. Embora tenha começado como um banco de dados de documentos NoSQL, ele evoluiu para incluir uma implementação robusta de Vector Search integrada nativamente ao modelo de documentos.

No Vectora, o Atlas não é apenas um banco de dados; é a infraestrutura que sustenta a governança de contexto, permitindo que vetores, metadados, estado operacional e logs de auditoria coexistam no mesmo ecossistema com consistência garantida.

### Especificações Técnicas (Nível Gerenciado Kaffyn)

| Recurso                | Detalhe                                           |
| ---------------------- | ------------------------------------------------- |
| Tipo de Banco          | Multicluster Document + Vector Search integrado   |
| Indexação Vetorial     | HNSW (Hierarchical Navigable Small World)         |
| Escalabilidade         | Sharding automático com balanceamento dinâmico    |
| Disponibilidade        | 99.99% com Replica Sets em múltiplas zonas        |
| Criptografia           | AES-256 em repouso e TLS 1.3 em trânsito          |
| Backup                 | Snapshots contínuos com retenção configurável     |
| Isolamento             | Namespaces lógicos com filtering obrigatório      |

## Por Que MongoDB Atlas para o Vectora

A seleção do MongoDB Atlas como backend unificado foi fundamentada em três pilares arquiteturais:

### 1. Atomicidade Metadado-Vetor

No Atlas, o vetor de embedding e os metadados do código residem no mesmo documento BSON. Isso elimina problemas de consistência como "vetores órfãos" ou metadados desatualizados. Quando um arquivo é modificado, a atualização do embedding e dos metadados ocorre em uma única operação atômica.

### 2. Filtragem de Namespace com Performance Nativa

O Vectora isola dados de diferentes projetos e usuários através de namespaces lógicos. O MongoDB Atlas permite aplicar filtros de metadados diretamente dentro da consulta vetorial HNSW. Isso garante que buscas semânticas nunca retornem dados de namespaces não autorizados, implementando isolamento multi-tenant no nível do índice.

### 3. Estado e Memória em Camada Única

Diferente de soluções especializadas apenas em vetores, o Atlas armazena de forma eficiente tanto embeddings semânticos quanto dados estruturais como histórico de sessões, estado operacional do agente e memória persistente. Isso permite que o Vectora recupere contexto histórico e vetores semânticos em uma única conexão, reduzindo latência e complexidade.

## Estrutura de Coleções no Vectora

O backend é organizado em coleções otimizadas para suportar o Harness Runtime e o fluxo de operação via MCP:

### Coleção documents

Armazena os chunks de código processados, metadados de AST, caminhos de arquivos e os embeddings gerados pelo Voyage 4.

- Campo embedding_vector: vetor de 1024 dimensões (Voyage 4)
- Índice HNSW configurado com efConstruction e maxConnections otimizados
- Filtros obrigatórios por namespace_id e visibility em todas as consultas

### Coleção sessions

Armazena o histórico de interações do agent principal via MCP, decisões tomadas pelo Context Engine e estado atual do plano de execução.

- Chave de sessão por userId + namespace
- TTL configurável para limpeza automática de sessões inativas
- Criptografia em repouso para dados sensíveis de sessão

### Coleção audit_logs

Registros imutáveis de cada ferramenta executada, identificando quem executou, quando, qual ferramenta e resultado da operação (apenas metadados, nunca conteúdo de código).

- Estrutura append-only para integridade forense
- Indexação por timestamp e userId para consultas de auditoria eficientes
- Retenção configurável conforme plano e políticas de compliance

## Como o Vectora Otimiza o Atlas

### Configuração Dinâmica de Índices HNSW

O Vectora ajusta dinamicamente os parâmetros efConstruction e maxConnections do índice HNSW baseando-se no volume e distribuição dos dados do usuário. Codebases menores recebem configurações otimizadas para baixa latência; codebases grandes recebem configurações que priorizam precisão de recall.

### Compaction Semântica Pré-Indexação

Antes de salvar documentos no Atlas, o Vectora aplica algoritmos de compaction que removem ruído sintático e preservam apenas conteúdo semanticamente relevante. Isso reduz o volume de armazenamento e melhora a eficiência das buscas vetoriais sem comprometer a qualidade do contexto recuperado.

### Fallback Transparente para Embeddings

Em cenários de indisponibilidade do provider primário (Voyage 4), o Vectora roteia automaticamente para gemini-embedding-2, mantendo a mesma dimensão de vetor (1024) para compatibilidade com índices existentes. O fallback é transparente para o agent principal e não requer reindexação.

## Gerenciamento Kaffyn (Zero Ops)

Quando você usa o Vectora, não precisa configurar instâncias manualmente no console do MongoDB. A Kaffyn provisiona e gerencia o backend automaticamente:

- Plano Free: Cluster compartilhado otimizado, limite de 512MB de armazenamento total, retenção de 30 dias após inatividade para índice vetorial
- Plano Pro: Cluster dedicado ou serverless de alta performance, limite de 10GB, backups prioritários e retenção de 90 dias pós-cancelamento
- Plano Team: Clusters com VPC peering, limite de 50GB, RBAC granular e retenção de 180 dias pós-cancelamento
- Segurança: Cada usuário e time recebe credenciais isoladas, namespaces criptografados e políticas de acesso validadas no runtime

## FAQ de Backend

P: Os dados do meu código são enviados para a nuvem?
R: Sim, os embeddings (vetores numéricos) e metadados estruturais (AST, caminhos, timestamps) são armazenados no MongoDB Atlas gerenciado pela Kaffyn. O conteúdo bruto do código é processado localmente pelo Guardian para garantir que segredos e arquivos sensíveis nunca sejam indexados ou transmitidos.

P: Posso usar meu próprio cluster do MongoDB Atlas?
R: Sim, no plano Enterprise ou através da configuração backend.custom_connection_string no vectora.config.yaml. Esta opção requer configuração manual de collections, índices e políticas de segurança.

P: O que acontece se o backend ficar indisponível?
R: O Vectora implementa fallback local para operações básicas de filesystem e caching de embeddings recentes. O Harness Runtime detecta indisponibilidade e degrada gracefully, mantendo funcionalidade essencial enquanto notifica o usuário.

P: Como é garantido o isolamento entre namespaces?
R: Todas as consultas ao Atlas incluem filtros obrigatórios por namespace_id e visibility. O RBAC na camada de aplicação valida permissões antes de qualquer consulta, e o Guardian bloqueia acessos não autorizados mesmo se a validação de aplicação falhar.

P: Posso exportar meus dados do Atlas?
R: Sim. O comando vectora export permite exportar metadados, embeddings (como base64) e logs de auditoria em formato portável. A exportação está disponível a qualquer momento, independentemente do plano ou status da assinatura.

Frase para lembrar:
"O MongoDB Atlas é onde o Vectora guarda o conhecimento estruturado. A inteligência está no runtime; a memória está no Atlas; a governança está na aplicação."
