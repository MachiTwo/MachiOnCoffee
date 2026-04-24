---
title: Billing
slug: billing
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - billing
  - byok
  - concepts
  - embeddings
  - errors
  - gemini
  - guardian
  - mcp
  - privacy
  - protocol
  - rbac
  - reranker
  - security
  - sso
  - vectora
  - voyage
---

{{< lang-toggle >}}

Dúvidas sobre planos, preço, faturamento e upgrade de Vectora respondidas com clareza.

## Por Quanto Tempo Posso Usar Free?

**Para sempre.** Free tier é permanente e sem expiração. Use Vectora gratuitamente indefinidamente se:

- 1 usuário
- < 1000 buscas/dia
- Sem necessidade de webhooks
- Sem SLA

## Como Faço Upgrade?

```bash
# Via CLI
vectora upgrade --plan plus

# Via Dashboard
# https://console.vectora.app/settings/billing
```

**Processo**:

1. Escolha plano (Pro ou Team)
2. Add método de pagamento (cartão ou invoice)
3. Upgrade imediato
4. Todos os dados preservados

## Há Taxa de Setup ou Contrato?

**Free → Pro**: Sem taxa, sem contrato

- Cancele anytime
- Sem penalidades
- Próximo ciclo de faturamento

## Qual é a Moeda?

## USD (Dólares Americanos)

- Free: $0
- Pro: $29 USD/mês
- Team: Customizado (USD)

Se você está em outra região, conversor automático no pagamento.

## Quando Sou Cobrado?

**Monthly billing** (ciclo renovado todo dia da assinatura).

Exemplo:

- Assina em 19 de abril
- Renovações: 19 de maio, 19 de junho, etc.

## Posso Pagar Anualmente?

**Sim, há desconto.**

- **Monthly**: $29/mês = $348/ano
- **Annual**: $290/ano = ~$24/mês (17% desconto)

## Qual é a Política de Reembolso?

**Sem reembolso.**

- Pagamentos são não-reembolsáveis
- Porém você pode cancelar anytime
- Sem cobranças futuras após cancelamento

## Posso Downgrade?

**Sim, sem penalidades.**

```bash
vectora downgrade --plan free

# Resultado:
# - Seus dados são preservados
# - Features Pro desabilitadas imediatamente
# - Pro features param de funcionar (webhooks, etc)
# - Próximo billing cycle: grátis novamente
```

## Há Desconto para Startups/Nonprofits?

**Sim, entre em contato.**

**<sales@vectora.app>**

Oferecemos:

- 50% desconto para nonprofits (verificado)
- 50% para startups em Y Combinator / similar
- Custom pricing para volume/educação

## Como Cancelo minha Assinatura?

```bash
vectora subscription cancel

# Ou via dashboard:
# https://console.vectora.app/settings/billing
# → "Cancel Plan"
```

**Resultado**:

- Cancelamento imediato
- Sem cobranças futuras
- Dados preservados (5 dias antes de purga)

## Quanto Custa Exceder Limites?

**Free → Pro**:

| Recurso    | Free   | Pro       |
| ---------- | ------ | --------- |
| Buscas/mês | 30K    | Unlimited |
| Usuários   | 1      | 50        |
| Rate limit | 60/min | 2000/min  |

**Se você excede limites Free**:
→ Requisições são bloqueadas (error 429)
→ Upgrade para Pro para continuar

## Há Taxa de Transação?

**Não.**

Você paga apenas a taxa base ($29 para Pro, custom para Team).

Sem taxas escondidas, sem taxa de gateway, sem taxa de processamento.

## Qual é a Política de Dados Deletados?

**Free Tier**:

- Cancelamento
- Dados permanecem 5 dias
- Depois deletados automaticamente
- Recuperação não-possível

**Pro/Team**:

- Backup diário
- Retenção 30+ dias
- Recuperação disponível (contate support)

## Há Desconto para Volume?

**Sim.**

- **Pro base**: $29 (até 50 usuários)
- **Extra users**: $0.50/mês por user acima de 50
- **Storage extra**: $0.10/GB/mês acima de 5GB

Exemplo:

- 100 usuários: $29 + (50 × $0.50) = $54/mês

## Como Funciona Billing no Team?

**Customizado por organização.**

Baseado em:

- Número de usuários
- Features customizadas (SSO, webhooks, etc)
- Support tier (24/7, dedicated, etc)
- Deployment (cloud vs on-prem)

**Contato**:
**<sales@vectora.app>** para proposta

## Há Teste Grátis do Pro?

**Não, use Free tier indefinidamente.**

Free tier é suficiente para testar:

- Indexação
- Busca
- Integração com IDEs
- RBAC
- Guardian
- CLI

## Como Vejo Meu Uso e Fatura?

```bash
vectora billing current

# Output:
# Current Period: Apr 19 - May 19, 2026
# Plan: Pro
# Status: Active ($29)
# Next charge: May 19, 2026
```

**Dashboard**:

- <https://console.vectora.app/settings/billing>
- Histórico de faturas
- Detalhes de uso
- Methods of payment

## Qual é sua Política de Privacidade de Dados?

Leia: [BYOK & Privacy](../security/byok-privacy.md)

**Resumo**:

- BYOK (suas chaves)
- Dados nunca são salvos
- Criptografado em trânsito
- Audit logs opcionais
- Você controla tudo

## Há Garantia de Uptime?

| Plano    | SLA     | Compensação   |
| -------- | ------- | ------------- |
| **Free** | Nenhuma | N/A           |
| **Pro**  | 99.9%   | 10-50% refund |
| **Team** | 99.99%  | 10-50% refund |

Se Vectora não atinge SLA, você recebe crédito automaticamente.

## Qual é Meu Limite de API?

**Free**:

- Gemini: 60 requisições/min (Google free tier)
- Voyage: 50 requisições/min (Voyage free tier)

**Pro/Team**:

- Unlimited (você paga para Google/Voyage, não Vectora)

## Posso Usar Cartão de Crédito Corporativo?

**Sim.**

Vectora aceita:

- Visa, Mastercard, American Express
- Depósito bancário (Team)
- PO (invoice)

Verificar com seu departamento de contabilidade para corporate cards.

## Há Imposto/VAT?

**Sim, se aplicável.**

- **US**: Sem sales tax (SaaS isento em muitos estados)
- **EU**: 0-27% VAT (conforme seu país)
- **Other**: Conforme regulação local

Calculado automaticamente no checkout.

## Como Cancelo e Recupero Dados?

```bash
# 1. Exportar dados
vectora export --output backup.tar.gz

# 2. Cancelar
vectora subscription cancel

# 3. Guardar backup
mv backup.tar.gz ~/backups/

# 4. Dados permanecem 5 dias, depois deletados
```

---

> **Próximo**: [FAQ - Security](./security.md)

---

## External Linking

| Concept               | Resource                                | Link                                                                                   |
| --------------------- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| **Voyage Embeddings** | Voyage Embeddings Documentation         | [docs.voyageai.com/docs/embeddings](https://docs.voyageai.com/docs/embeddings)         |
| **Voyage Reranker**   | Voyage Reranker API                     | [docs.voyageai.com/docs/reranker](https://docs.voyageai.com/docs/reranker)             |
| **MCP**               | Model Context Protocol Specification    | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK**        | Go SDK for MCP (mark3labs)              | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |
| **RBAC**              | NIST Role-Based Access Control Standard | [csrc.nist.gov/projects/rbac](https://csrc.nist.gov/projects/rbac)                     |
| **Gemini API**        | Google AI Studio Documentation          | [ai.google.dev/docs](https://ai.google.dev/docs)                                       |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
