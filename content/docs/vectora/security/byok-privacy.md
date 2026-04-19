---
title: BYOK & Privacy
slug: byok-privacy
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - byok
  - governance
  - mcp
  - privacy
  - security
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

Vectora é **100% BYOK** (Bring Your Own Keys). Você controla suas chaves de API. Seus dados NUNCA são salvos na infraestrutura Vectora. Privacidade completa.

> [!IMPORTANT]
> BYOK significa: Você tem controle total. Vectora nunca vê seus dados brutos. Apenas resultados processados saem de seus servidores.

---

## Modelo de Dados

### Fluxo Seguro

```text
Seu Código
  ↓
1. Vetorização (Voyage - você hospeda via chave BYOK)
   "How to validate tokens?" → [0.12, 0.45, ..., 0.89]
  ↓
2. Busca (Qdrant - seu servidor local ou private cloud)
   Busca vetores no seu índice
  ↓
3. Reranking (Voyage - você hospeda via chave BYOK)
   Refina top-100 → top-10
  ↓
4. LLM (Gemini - você hospeda via chave BYOK)
   Análise opcional
  ↓
5. Resposta
   Chunks relevantes retornam
```

**Seus dados NUNCA deixam sua rede, exceto para APIs que você controla.**

---

## O Que Está Incluído em BYOK

### APIs que Você Controla

| Serviço           | Onde Roda          | Você Controla   |
| ----------------- | ------------------ | --------------- |
| **Voyage 4**      | Servers Voyage     | Via sua API key |
| **Voyage Rerank** | Servers Voyage     | Via sua API key |
| **Gemini 3**      | Servers Google     | Via sua API key |
| **Qdrant**        | Seu servidor local | Completamente   |

### O Que Vectora Pode Ver

```text
Via suas chaves de API:
- Requisições que você envia (query, contexto)
- Responses que você recebe (embeddings, reranking)

Via seus logs:
- Tudo, se você ativar audit logging
```

### O Que Vectora NÃO Pode Ver

```text
 Código-fonte (em .git, arquivos)
 Dados privados (.env, secrets)
 Histórico de chat/análise
 Metadados sobre seu projeto
 User activity (sem Harness)
```

---

## Configuração BYOK

### Passo 1: Obter Chaves

**Gemini** (Google):

```bash
# https://aistudio.google.com/app/apikey
# Free tier: 60 req/min, 1.5M tokens/mês
GEMINI_API_KEY="AIzaSyD..."
```

**Voyage** (VoyageAI):

```bash
# https://dash.voyageai.com/api-keys
# Free tier: 50 req/min, 100M tokens/mês
VOYAGE_API_KEY="pa-..."
```

**Qdrant** (você hospeda):

```bash
# Local ou cloud
QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY="qdrant-key-xyz" # Se auth habilitada
```

### Passo 2: Configurar Vectora

```bash
# Via .env
cat > .env << 'EOF'
GEMINI_API_KEY=AIzaSyD...
VOYAGE_API_KEY=pa-...
QDRANT_URL=http://localhost:6333
EOF

# Ou via config
vectora config set --key GEMINI_API_KEY
vectora config set --key VOYAGE_API_KEY
```

### Passo 3: Verificar

```bash
vectora config validate

# Output:
# GEMINI_API_KEY: Valid (free tier)
# VOYAGE_API_KEY: Valid (free tier)
# QDRANT_URL: Connected (healthy)
```

---

## Data Residency & Compliance

### Local Deployment

Tudo roda localmente (máxima privacidade):

```text
┌─────────────────────────────────────┐
│ Seu Servidor Local │
│ ├─ Vectora (indexação, search) │
│ ├─ Qdrant (vector DB) │
│ ├─ Redis (cache) │
│ └─ PostgreSQL (metadata) │
└─────────────────────────────────────┘
    │
    ├─ API Voyage (embedding)
    ├─ API Gemini (LLM)
    └─ (Você controla estas chamadas)
```

### Private Cloud (VPC)

Sua conta cloud, você controla:

```yaml
deployment:
  provider: "AWS|Azure|GCP"
  region: "us-east-1"
  vpc: "vpc-xxxxx"
  private_endpoints: true
  encryption: "KMS-managed"
```

### On-Premise

Sem cloud. Seu datacenter:

```bash
docker run \
  -e VECTORA_LICENSE=enterprise \
  -e QDRANT_URL=http://internal-qdrant:6333 \
  -v /data/vectora:/data \
  vectora:latest
```

---

## Encryption

### At Rest

Dados no disco são criptografados:

```yaml
encryption:
  at_rest:
    enabled: true
    cipher: "AES-256-GCM"
    key_management: "envelope_encryption" # Key separated
    key_rotation: "automatic_90d"
```

Teste:

```bash
# Dados criptografados em disco
ls -la .vectora/index/
# vectors.db.enc (encrypted)

# Decriptado apenas em memória durante busca
vectora search "query" --verify-encryption
# Encryption verified
```

### In Transit

Todas as comunicações são HTTPS/TLS 1.3:

```yaml
ssl:
  enabled: true
  version: "1.3"
  certificate: "/etc/ssl/cert.pem"
  key: "/etc/ssl/key.pem"
```

---

## Privacy Guarantees

### Vectora Nunca

- Armazena seu código
- Armazena embeddings
- Armazena respostas
- Compartilha dados
- Treina modelos com seus dados
- Vende dados
- Faz correlação entre usuários

### Você Sempre

- Controla suas chaves
- Pode deletar tudo
- Pode auditar acessos
- Pode usar local/on-prem
- Pode usar seus próprios modelos
- Pode exportar dados

---

## Compliance Frameworks

Vectora respeita:

### GDPR (EU)

```yaml
gdpr:
  data_residency: "EU" # Dados na EU
  right_to_deletion: true # Deletar tudo
  data_portability: true # Exportar dados
  audit_logs: true # Rastrear acesso
```

Setup:

```bash
vectora config set --key GDPR_REGION eu-west-1
vectora config set --key DATA_RESIDENCY "EU"
```

### HIPAA (Healthcare)

```yaml
hipaa:
  phi_encryption: "required" # PHI sempre criptografado
  audit_logging: "required" # Todos os acessos logged
  data_isolation: "required" # Dados isolados
```

### PCI-DSS (Payment Cards)

```yaml
pci_dss:
  credit_card_blocking: true # CC números bloqueados
  encryption_transit: "TLS 1.2+"
  audit_retention: "1 year"
```

### SOC 2

```yaml
soc2:
  security: true # Implementado
  availability: true
  processing_integrity: true
  confidentiality: true
  privacy: true
```

---

## Data Deletion & Export

### Exportar Dados

```bash
# Exportar tudo
vectora export --output backup.tar.gz

# Ou específico
vectora export --namespace seu-namespace --format json
```

Output:

```json
{
  "namespace": "seu-namespace",
  "chunks": 3159,
  "vectors": [...],
  "metadata": {...},
  "created_at": "2026-04-19T10:00:00Z",
  "exported_at": "2026-04-19T15:30:00Z"
}
```

### Deletar Tudo

```bash
# Deletar namespace
vectora namespace delete --name seu-namespace
# PERMANENTE - não recuperável

# Deletar usuário
vectora user delete --email user@company.com
# Logs preservados, dados deletados
```

---

## Audit & Transparency

### Enable Audit Logging

```bash
export VECTORA_AUDIT_LOG=true
vectora search "query"

# Logs every access
cat .vectora/audit.log
```

Sample audit entry:

```json
{
  "timestamp": "2026-04-19T15:30:45Z",
  "event": "search",
  "user": "dev@company.com",
  "query_hash": "abc123",
  "files_accessed": 0,
  "api_call": "gemini",
  "data_sent_bytes": 245,
  "data_received_bytes": 512,
  "encryption": "TLS 1.3"
}
```

### Privacy Dashboard

```bash
vectora privacy report

# Output:
# Privacy Report
# ══════════════════════════════════════
# Data Classification:
# - Public: 50%
# - Internal: 40%
# - Sensitive: 10%
#
# Encryption:
# - At rest: AES-256
# - In transit: TLS 1.3
#
# Compliance:
# - GDPR: Compliant
# - SOC 2: Attestation
#
# Third-party APIs:
# - Gemini: 342 calls (your key)
# - Voyage: 128 calls (your key)
```

---

## FAQs

**P: Vectora pode acessar minhas chaves?**
R: Não. Suas chaves são suas. Criptografadas localmente em `~/.vectora/credentials.enc`. Vectora usa apenas para fazer requisições em seu nome.

**P: Meus dados são compartilhados?**
R: Não. BYOK significa isolamento total. Seus dados nunca saem de seus servidores, exceto para APIs que você controla.

**P: Como migro para BYOK?**
R: Todos os planos usam BYOK. Configure suas chaves e pronto.

**P: Posso usar modelos locais?**
R: Sim. Use Ollama ou Hugging Face para embedding local (100% offline).

```bash
# Local embedding via Ollama
docker run -d -p 11434:11434 ollama/ollama
vectora config set --key EMBEDDING_PROVIDER "ollama"
vectora config set --key EMBEDDING_MODEL "all-MiniLM-L6-v2"
```

**P: Qual é sua política de retenção?**
R: Você controla. Local storage = você mantém backups. Cloud storage = você escolhe retenção.

---

## Security Checklist

- [ ] BYOK chaves configuradas e testadas
- [ ] Audit logging habilitado
- [ ] TLS 1.3 obrigatório
- [ ] Backup automatizado (encriptado)
- [ ] Trust folder configurado
- [ ] Guardian rules aplicadas
- [ ] RBAC configurado
- [ ] Compliance framework selecionado
- [ ] Data residency alinhado
- [ ] Access logs revisados regularmente

---

> **Próximo**: [FAQ - General](../faq/general.md)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
