---
title: Data Retention
slug: retention
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - byok
  - concepts
  - embeddings
  - mcp
  - privacy
  - protocol
  - retention
  - security
  - vectora
---

{{< lang-toggle >}}

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

## External Linking

| Concept        | Resource                             | Link                                                                                   |
| -------------- | ------------------------------------ | -------------------------------------------------------------------------------------- |
| **MCP**        | Model Context Protocol Specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) |
| **MCP Go SDK** | Go SDK for MCP (mark3labs)           | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                     |

---

_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)
