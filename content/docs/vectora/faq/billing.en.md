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
  - errors
  - gemini
  - guardian
  - integration
  - mcp
  - privacy
  - rbac
  - security
  - sso
  - vectora
  - voyage
---

{{< lang-toggle >}}
{{< section-toggle >}}

Questions about plans, pricing, billing, and upgrading Vectora answered clearly.

## How Long Can I Use the Free Plan?

**Forever.** The Free tier is permanent and has no expiration. Use Vectora for free indefinitely if:

- 1 user
- < 1,000 searches/day
- No need for webhooks
- No SLA

## How Do I Upgrade?

```bash
# Via CLI
vectora upgrade --plan plus

# Via Dashboard
# https://console.vectora.app/settings/billing
```

**Process**:

1. Choose a plan (Pro or Team).
2. Add a payment method (card or invoice).
3. Immediate upgrade.
4. All data preserved.

## Are There Setup Fees or Contracts?

**Free → Pro**: No fees, no contracts.

- Cancel anytime.
- No penalties.
- Changes apply to the next billing cycle.

## What is the Currency?

## USD (US Dollars)

- Free: $0
- Pro: $29 USD/month
- Team: Custom (USD)

If you are in another region, there will be an automatic conversion at checkout.

## When Am I Billed?

**Monthly billing** (cycle renewed each subscription day).

Example:

- Subscribed on April 19.
- Renewals: May 19, June 19, etc.

## Can I Pay Annually?

**Yes, there is a discount.**

- **Monthly**: $29/month = $348/year
- **Annual**: $290/year = ~$24/month (17% discount)

## What is the Refund Policy?

**No refunds.**

- Payments are non-refundable.
- However, you can cancel anytime.
- No future charges after cancellation.

## Can I Downgrade?

**Yes, without penalties.**

```bash
vectora downgrade --plan free

# Result:
# - Your data is preserved
# - Pro features disabled immediately
# - Pro features stop working (webhooks, etc.)
# - Next billing cycle: free again
```

## Are There Discounts for Startups/Nonprofits?

**Yes, please contact us.**

**<sales@vectora.app>**

We offer:

- 50% discount for nonprofits (verified).
- 50% for startups in Y Combinator or similar.
- Custom pricing for volume/education.

## How Do I Cancel My Subscription?

```bash
vectora subscription cancel

# Or via dashboard:
# https://console.vectora.app/settings/billing
# → "Cancel Plan"
```

**Result**:

- Immediate cancellation.
- No future charges.
- Data preserved for 5 days before purge.

## What Does It Cost to Exceed Limits?

**Free vs. Pro**:

| Resource       | Free   | Pro       |
| -------------- | ------ | --------- |
| Searches/month | 30K    | Unlimited |
| Users          | 1      | 50        |
| Rate limit     | 60/min | 2000/min  |

**If you exceed Free limits**:
→ Requests are blocked (error 429).
→ Upgrade to Pro to continue.

## Are There Transaction Fees?

**No.**

You only pay the base fee ($29 for Pro, custom for Team).

No hidden fees, no gateway fees, no processing fees.

## What is the Deleted Data Policy?

**Free Tier**:

- On cancellation.
- Data remains for 5 days.
- Then deleted automatically.
- Recovery is not possible.

**Pro/Team**:

- Daily backup.
- 30+ days retention.
- Recovery available (contact support).

## Are There Volume Discounts?

**Yes.**

- **Pro base**: $29 (up to 50 users).
- **Extra users**: $0.50/month per user above 50.
- **Extra storage**: $0.10/GB/month above 5GB.

Example:

- 100 users: $29 + (50 × $0.50) = $54/month.

## How Does Billing Work for Team Plans?

**Customized per organization.**

Based on:

- Number of users.
- Custom features (SSO, webhooks, etc.).
- Support tier (24/7, dedicated, etc.).
- Deployment (cloud vs. on-prem).

**Contact**:
**<sales@vectora.app>** for a proposal.

## Is There a Free Pro Trial?

**No, use the Free tier indefinitely.**

The Free tier is sufficient to test:

- Indexing
- Search
- IDE integration
- RBAC
- Guardian
- CLI

## How Can I See My Usage and Invoice?

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
- Invoice history.
- Usage details.
- Payment methods.

## What is Your Data Privacy Policy?

Read: [BYOK & Privacy](../security/byok-privacy.md)

**Summary**:

- BYOK (your keys).
- Data is never saved.
- Encrypted in transit.
- Optional audit logs.
- You control everything.

## Is There an Uptime Guarantee?

| Plan     | SLA    | Compensation  |
| -------- | ------ | ------------- |
| **Free** | None   | N/A           |
| **Pro**  | 99.9%  | 10-50% refund |
| **Team** | 99.99% | 10-50% refund |

If Vectora does not meet the SLA, you automatically receive credit.

## What is My API Limit?

**Free**:

- Gemini: 60 requests/min (Google free tier).
- Voyage: 50 requests/min (Voyage free tier).

**Pro/Team**:

- Unlimited (you pay Google/Voyage indirectly, not through Vectora).

## Can I Use a Corporate Credit Card?

**Yes.**

Vectora accepts:

- Visa, Mastercard, American Express.
- Bank transfer (Team).
- PO (invoice).

Check with your accounting department regarding corporate card usage.

## Is There Tax/VAT?

**Yes, if applicable.**

- **US**: No sales tax (SaaS exempt in many states).
- **EU**: 0-27% VAT (depending on your country).
- **Other**: Depends on local regulation.

Calculated automatically at checkout.

## How Do I Cancel and Retrieve My Data?

```bash
# 1. Export data
vectora export --output backup.tar.gz

# 2. Cancel
vectora subscription cancel

# 3. Save backup
mv backup.tar.gz ~/backups/

# 4. Data remains for 5 days, then deleted
```

---

> **Next**: [FAQ - Security](./security.md)

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
