---
title: Data Retention
slug: retention
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - mcp
  - retention
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

This page details the data retention policies for different plans and types of information in Vectora.

## Policies by Data Type

| Data Type        | Free              | Pro                    | Team                   |
| :--------------- | :---------------- | :--------------------- | :--------------------- |
| **Embeddings**   | Lifetime (local)  | While active + 30 days | While active + 90 days |
| **Audit Logs**   | 30 days           | 90 days                | 7 years (Compliance)   |
| **MCP Sessions** | 24h of inactivity | 14 days                | Customized             |
| **Backup Files** | Manual            | Automatic (30 days)    | Automatic (Customized) |

## Cancellation and Expiration

If you cancel your subscription or your account expires:

1. **Account Suspended**: You have 5 days to export your data.
2. **Intermediate Purge**: Logs and session metadata are deleted after 15 days.
3. **Final Purge**: All embeddings and configurations are permanently removed after 30 days (Pro) or 90 days (Team).

---

> To exercise your privacy rights, please refer to our [Privacy Policy](../security/byok-privacy.md).
