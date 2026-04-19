---
title: Guardian
slug: guardian
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - governance
  - guardian
  - mcp
  - security
  - vectora
---

{{< lang-toggle >}}

## Visão Geral

**Guardian** é o **sistema de segurança hard-coded** que bloqueia acesso a arquivos sensíveis no Vectora. Opera em 3 camadas: Trust Folder (path isolation), pattern matching (regex rules), e audit logging.

> [!IMPORTANT]
> Guardian não é um firewall - é um gatekeeper. Uma violação Guardian é BLOQUEADA antes de chegar ao filesystem, sem exceções.

---

## Arquitetura

```text
Request para ler arquivo
    ↓
┌─────────────────┐
│  Trust Folder   │ Está dentro do perímetro?
│  Check          │
└────────┬────────┘
         │ SIM
         ↓
┌─────────────────────┐
│  Guardian Rules     │ Matches allow/deny pattern?
│  Pattern Matching   │
└────────┬────────────┘
         │ ALLOW (ou SEM MATCH)
         ↓
┌──────────────────┐
│  RBAC Check      │ Usuário tem permissão?
│                  │
└────────┬─────────┘
         │ SIM
         ↓
┌──────────────────────┐
│  File Access         │ Arquivo pode ser lido
│  Permitido           │
└──────────────────────┘

Se qualquer check FALHA → Request é BLOQUEADO + Audit Log
```

---

## Configuração

### Trust Folder (Camada 1)

Define o perímetro de segurança:

```yaml
# vectora.config.yaml
project:
  trust_folder: "./src"
  # Apenas arquivos em ./src/* podem ser acessados
```

Qualquer tentativa de ler fora deste diretório é bloqueada:

```text
Request: ../../../.env
Trust Folder: ./src
Resultado: ❌ BLOQUEADO (fora do périmetro)
```

### Guardian Rules (Camada 2)

Padrões de regex para allow/deny:

```yaml
# vectora.config.yaml
guardian:
  rules:
    # DENY tem prioridade
    - name: "block_env"
      pattern: "\.env.*"              # .env, .env.local, .env.production
      action: "deny"
    
    - name: "block_secrets"
      pattern: "secrets/.*"
      action: "deny"
    
    - name: "block_credentials"
      pattern: ".*credentials.*"      # Any file with "credentials"
      action: "deny"
    
    # ALLOW (opcional, mais específico)
    - name: "allow_src_docs"
      pattern: "^(src|docs)/.*"
      action: "allow"
```

Ordem importa: regras são avaliadas top→bottom, primeira match vence.

### RBAC (Camada 3)

Além disso, Vectora respeita permissões de user:

```yaml
# Definido em RBAC config
roles:
  owner:
    permissions:
      - search
      - index
      - configure
      - manage_users
  editor:
    permissions:
      - search
      - index
  viewer:
    permissions:
      - search
```

---

## Padrões Pré-Configurados

Guardian vem com padrões de segurança pré-set:

```yaml
# Defaults (sempre ativa)
defaults:
  block_patterns:
    - "\.env.*"
    - ".*\.key$"
    - ".*\.pem$"
    - ".*secret.*"
    - "\.git/.*"
    - "\.ssh/.*"
    - "node_modules/.*"              # Opcional
    - "__pycache__/.*"
    - "\.venv/.*"
```

Para customizar, sobrescreva em config:

```yaml
guardian:
  override_defaults: true
  rules:
    - name: "my_rule"
      pattern: "custom.*"
      action: "deny"
```

---

## Audit Logging

Toda tentativa de acesso (bloqueada ou permitida) é logged:

```bash
VECTORA_AUDIT_LOG=true vectora search "query"
```

Log output:

```json
{
  "timestamp": "2026-04-19T10:30:00Z",
  "event": "guardian_check",
  "action": "file_access",
  "requested_file": ".env",
  "trust_folder": "/home/user/project/src",
  "status": "BLOCKED",
  "reason": "matches_deny_pattern",
  "pattern": "\.env.*",
  "user": "dev@company.com",
  "user_role": "editor",
  "ip": "192.168.1.100"
}
```

Inspecionar logs:

```bash
# Últimas 24h
vectora audit --action file_access --since 24h

# Apenas bloqueados
vectora audit --filter "BLOCKED"

# Por padrão
vectora audit --filter "pattern:\.env"
```

---

## Casos de Uso

### Case 1: Proteger .env

```yaml
guardian:
  rules:
    - name: "block_dotenv"
      pattern: "\.env.*"
      action: "deny"
```

Resultado: `.env`, `.env.local`, `.env.production` são todos bloqueados.

### Case 2: Proteger dados privados

```yaml
guardian:
  rules:
    - name: "block_private"
      pattern: "private/.*"
      action: "deny"
    
    - name: "block_test_data"
      pattern: "test_data/.*\.csv"
      action: "deny"
```

### Case 3: Allow-list específico

```yaml
project:
  trust_folder: "."                  # Confio em tudo

guardian:
  rules:
    # Explicitamente permitir apenas src/ e docs/
    - name: "allow_src_docs"
      pattern: "^(src|docs)/"
      action: "allow"
    
    # Tudo mais é bloqueado
    - name: "deny_everything_else"
      pattern: ".*"
      action: "deny"
```

---

## Violações Conhecidas

### Directory Traversal Attempts

```text
Tentativa: ../../.env
Resolução: Normalizado para /absolute/path/.env
Trust Folder: /absolute/path/src
Resultado: ❌ BLOQUEADO (fora do perímetro)
```

### Symlink Attacks

```text
File: ./src/link-to-secret → ../../secret.key
Resolução: Resolvido para /absolute/path/secret.key
Trust Folder: /absolute/path/src
Resultado: ❌ BLOQUEADO (symlink fora do perímetro)
```

Para permitir symlinks específicos:

```yaml
guardian:
  symlink_handling: "follow"         # ou "deny"
  symlink_whitelist:
    - "./src/allowed-link"
```

### Case Sensitivity (Windows)

Windows é case-insensitive, padrões são case-sensitive por padrão:

```yaml
guardian:
  case_sensitive: false              # Match .ENV, .Env, .env
```

---

## Testing & Validation

### Dry-Run Mode

Testar regras sem bloquear:

```bash
vectora guardian validate --dry-run
```

Output:

```text
Guardian Validation Report
├─ Trust Folder: ./src ✓
├─ Default Deny Patterns: 9 ✓
├─ Custom Rules: 3 ✓
└─ Test Cases:
   ├─ .env → BLOCKED (pattern: \.env.*)
   ├─ src/main.ts → ALLOWED
   └─ secrets/key.pem → BLOCKED (pattern: secrets/.*)
```

### Rule Testing

```bash
# Testar padrão específico
vectora guardian test-pattern "\.env.*" ".env.local"
# Output: MATCH

vectora guardian test-pattern "\.env.*" "src/index.ts"
# Output: NO MATCH
```

---

## Monitoring & Alerts

### Métricas

Guardian captura métricas de segurança:

```bash
vectora metrics --filter guardian
```

Output:

```yaml
guardian_metrics:
  period: "24h"
  total_checks: 12543
  allowed: 12500
  blocked: 43
  
  blocked_by_reason:
    deny_pattern: 35
    outside_trust_folder: 8
    rbac_violation: 0
  
  top_blocked_patterns:
    - "\.env.*": 15
    - "\.key$": 12
    - "secret": 8
```

### Alertas

Configure alertas para violações:

```yaml
guardian:
  alerts:
    enabled: true
    notify_on_violations: true
    threshold_per_hour: 10            # Alerta se > 10 bloqueios/h
    webhook: "https://your-slack.com/webhook"
```

---

## Best Practices

### 1. Trust Folder Mínimo

Não confie em `./` - seja específico:

```yaml
# ❌ Inseguro
project:
  trust_folder: "."

# ✅ Seguro
project:
  trust_folder: "./src"
```

### 2. Deny-by-Default

Quando possível, use padrão "deny all, allow specific":

```yaml
guardian:
  rules:
    - name: "allow_src_docs"
      pattern: "^(src|docs)/"
      action: "allow"
    
    - name: "deny_everything"
      pattern: ".*"
      action: "deny"
```

### 3. Audit Regularmente

```bash
# Weekly review
vectora audit --since 7d --filter "BLOCKED" | wc -l
```

### 4. Avoid Exceptions

Não crie "exception rules" para .env - use valores default:

```yaml
# ❌ Ruim - exceção
guardian:
  rules:
    - name: "allow_local_env"
      pattern: "\.env\.local"        # Exceção!
      action: "allow"

# ✅ Melhor - usar variáveis
guardian:
  rules:
    - name: "block_env"
      pattern: "\.env"
      action: "deny"

# Use .env via environment variables ao invés
export GEMINI_API_KEY="..."
```

---

## Troubleshooting

### Arquivo legítimo bloqueado

```text
Error: ./src/config.secrets.ts is blocked by pattern
```

**Diagnóstico**:
```bash
vectora guardian explain "./src/config.secrets.ts"
# Output: Matches deny_pattern ".*secret.*"
```

**Solução 1**: Renomear arquivo
```bash
mv src/config.secrets.ts src/config.secure.ts
```

**Solução 2**: Ajustar padrão (menos recomendado)
```yaml
guardian:
  rules:
    - name: "block_secrets"
      pattern: "secret_keys/.*"       # Mais específico
      action: "deny"
```

### "Guardian disabled" messages

Se Guardian está desabilitado (dev mode):

```bash
# Verificar status
vectora config get guardian.enabled

# Reabilitar
vectora config set guardian.enabled true
```

---

## Compliance & Regulations

Guardian ajuda a cumprir:

- **GDPR**: Dados pessoais protegidos
- **HIPAA**: Medical records não indexados
- **PCI-DSS**: Números de cartão bloqueados
- **SOC 2**: Audit trail completo

Configure regras específicas:

```yaml
# HIPAA
guardian:
  rules:
    - pattern: "patient_data/.*"
      action: "deny"
    - pattern: ".*\.phi\..*"           # Protected Health Info
      action: "deny"
```

---

> 💡 **Próximo**: [RBAC System](./rbac.md)

---

_Parte do ecossistema Vectora · Open Source (MIT) · TypeScript_
