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
{{< section-toggle >}}

Vectora is **100% BYOK** (Bring Your Own Keys). You control your API keys. Your data is NEVER saved on Vectora infrastructure. Complete privacy.

> [!IMPORTANT]
> BYOK means: You have full control. Vectora never sees your raw data. Only processed results leave your servers.

## Data Model

Vectora's data model is designed to ensure that information sovereignty remains with the user, utilizing local infrastructure or private clouds.

## Secure Flow

```text
Your Code
  ↓
1. Vectorization (Voyage - you host via BYOK key)
   "How to validate tokens?" → [0.12, 0.45, ..., 0.89]
  ↓
2. Search (Qdrant - your local server or private cloud)
   Search vectors in your index
  ↓
3. Reranking (Voyage - you host via BYOK key)
   Refines top-100 → top-10
  ↓
4. LLM (Gemini - you host via BYOK key)
   Optional analysis
  ↓
5. Response
   Relevant chunks return
```

**Your data NEVER leaves your network, except for APIs you control.**

## What's Included in BYOK

The Bring Your Own Key concept in Vectora spans from vectorization to final storage, ensuring that no secrets are shared.

## APIs You Control

| Service           | Where it Runs     | You Control      |
| ----------------- | ----------------- | ---------------- |
| **Voyage 4**      | Voyage Servers    | Via your API key |
| **Voyage Rerank** | Voyage Servers    | Via your API key |
| **Gemini 3**      | Google Servers    | Via your API key |
| **Qdrant**        | Your local server | Completely       |

## What Vectora Can See

```text
Via your API keys:
- Requests you send (query, context)
- Responses you receive (embeddings, reranking)

Via your logs:
- Everything, if you enable audit logging
```

## What Vectora CANNOT See

```text
 Source code (in .git, files)
 Private data (.env, secrets)
 Chat/analysis history
 Metadata about your project
 User activity (without Harness)
```

## BYOK Configuration

Configuring BYOK in Vectora is a simple process that involves collecting keys from supported providers and integrating them securely.

## Step 1: Get Keys

**Gemini** (Google):

```bash
# https://aistudio.google.com/app/apikey
# Free tier: 60 req/min, 1.5M tokens/month
GEMINI_API_KEY="AIzaSyD..."
```

**Voyage** (VoyageAI):

```bash
# https://dash.voyageai.com/api-keys
# Free tier: 50 req/min, 100M tokens/month
VOYAGE_API_KEY="pa-..."
```

**Qdrant** (you host):

```bash
# Local or cloud
QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY="qdrant-key-xyz" # If auth enabled
```

## Step 2: Configure Vectora

```bash
# Via .env
cat > .env << 'EOF'
GEMINI_API_KEY=AIzaSyD...
VOYAGE_API_KEY=pa-...
QDRANT_URL=http://localhost:6333
EOF

# Or via config
vectora config set --key GEMINI_API_KEY
vectora config set --key VOYAGE_API_KEY
```

## Step 3: Verify

```bash
vectora config validate

# Output:
# GEMINI_API_KEY: Valid (free tier)
# VOYAGE_API_KEY: Valid (free tier)
# QDRANT_URL: Connected (healthy)
```

## Data Residency & Compliance

Vectora allows you to choose exactly where your data resides, offering options ranging from local servers to isolated private clouds.

## Local Deployment

Everything runs locally (maximum privacy):

```text
┌─────────────────────────────────────┐
│ Your Local Server │
│ ├─ Vectora (indexing, search) │
│ ├─ Qdrant (vector DB) │
│ ├─ Redis (cache) │
│ └─ PostgreSQL (metadata) │
└─────────────────────────────────────┘
    │
    ├─ Voyage API (embedding)
    ├─ Gemini API (LLM)
    └─ (You control these calls)
```

## Private Cloud (VPC)

Your cloud account, you control:

```yaml
deployment:
  provider: "AWS|Azure|GCP"
  region: "us-east-1"
  vpc: "vpc-xxxxx"
  private_endpoints: true
  encryption: "KMS-managed"
```

## On-Premise

No cloud. Your datacenter:

```bash
docker run \
  -e VECTORA_LICENSE=enterprise \
  -e QDRANT_URL=http://internal-qdrant:6333 \
  -v /data/vectora:/data \
  vectora:latest
```

## Encryption

Data security is reinforced by multiple layers of encryption, protecting information both at rest and in transit.

## At Rest

Data on disk is encrypted:

```yaml
encryption:
  at_rest:
    enabled: true
    cipher: "AES-256-GCM"
    key_management: "envelope_encryption" # Key separated
    key_rotation: "automatic_90d"
```

Test:

```bash
# Data encrypted on disk
ls -la .vectora/index/
# vectors.db.enc (encrypted)

# Decrypted only in memory during search
vectora search "query" --verify-encryption
# Encryption verified
```

## In Transit

All communication is HTTPS/TLS 1.3:

```yaml
ssl:
  enabled: true
  version: "1.3"
  certificate: "/etc/ssl/cert.pem"
  key: "/etc/ssl/key.pem"
```

## Privacy Guarantees

Our technical architecture enforces strict privacy guarantees, ensuring that control remains entirely in the hands of the data owner.

## Vectora Never

- Stores your code
- Stores embeddings
- Stores responses
- Shares data
- Trains models with your data
- Sells data
- Performs correlation between users

## You Always

-

- Control your keys
- Can delete everything
- Can audit access
- Can use local/on-prem
- Can use your own models
- Can export data

## Compliance Frameworks

Vectora respects and helps you comply with key global compliance frameworks, adapting to the specific needs of each sector.

## GDPR (EU)

```yaml
gdpr:
  data_residency: "EU" # Data in EU
  right_to_deletion: true # Delete everything
  data_portability: true # Export data
  audit_logs: true # Track access
```

Setup:

```bash
vectora config set --key GDPR_REGION eu-west-1
vectora config set --key DATA_RESIDENCY "EU"
```

## HIPAA (Healthcare)

```yaml
hipaa:
  phi_encryption: "required" # PHI always encrypted
  audit_logging: "required" # All access logged
  data_isolation: "required" # Data isolated
```

## PCI-DSS (Payment Cards)

```yaml
pci_dss:
  credit_card_blocking: true # CC numbers blocked
  encryption_transit: "TLS 1.2+"
  audit_retention: "1 year"
```

## SOC 2

```yaml
soc2:
  security: true # Implemented
  availability: true
  processing_integrity: true
  confidentiality: true
  privacy: true
```

## Data Deletion & Export

You have total freedom over your data, with integrated tools for full export or permanent removal of any information.

## Export Data

```bash
# Export everything
vectora export --output backup.tar.gz

# Or specific
vectora export --namespace your-namespace --format json
```

Output:

```json
{
  "namespace": "your-namespace",
  "chunks": 3159,
  "vectors": [...],
  "metadata": {...},
  "created_at": "2026-04-19T10:00:00Z",
  "exported_at": "2026-04-19T15:30:00Z"
}
```

## Delete Everything

```bash
# Delete namespace
vectora namespace delete --name your-namespace
# PERMANENT - non-recoverable

# Delete user
vectora user delete --email user@company.com
# Logs preserved, data deleted
```

## Audit & Transparency

To ensure full transparency, Vectora offers detailed audit logs that allow you to track every operation performed on the system.

## Enable Audit Logging

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

## Privacy Dashboard

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

## FAQs

**Q: Can Vectora access my keys?**
A: No. Your keys are yours. Encrypted locally in `~/.vectora/credentials.enc`. Vectora uses them only to make requests on your behalf.

**Q: Is my data shared?**
A: No. BYOK means total isolation. Your data never leaves your servers, except for APIs you control.

**Q: How do I migrate to BYOK?**
A: All plans use BYOK. Configure your keys and you're good to go.

**Q: Can I use local models?**
A: Yes. Use Ollama or Hugging Face for local embedding (100% offline).

```bash
# Local embedding via Ollama
docker run -d -p 11434:11434 ollama/ollama
vectora config set --key EMBEDDING_PROVIDER "ollama"
vectora config set --key EMBEDDING_MODEL "all-MiniLM-L6-v2"
```

**Q: What is your retention policy?**
A: You control it. Local storage = you maintain backups. Cloud storage = you choose retention.

## Security Checklist

- [ ] BYOK keys configured and tested
- [ ] Audit logging enabled
- [ ] TLS 1.3 mandatory
- [ ] Automated backup (encrypted)
- [ ] Trust folder configured
- [ ] Guardian rules applied
- [ ] RBAC configured
- [ ] Compliance framework selected
- [ ] Data residency aligned
- [ ] Access logs reviewed regularly

---

> **Next**: [FAQ - General](../faq/general.md)

---

_Part of the Vectora ecosystem_ · Open Source (MIT)
