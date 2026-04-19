# Kaffyn SSO

> [!NOTE] > **Identidade Unificada para o Ecossistema Vectora.** Uma conta. Todos os seus projetos, dispositivos e
> integrações.

---

O **Kaffyn SSO** é a camada de autenticação e identidade centralizada que conecta todos os componentes do ecossistema
Vectora Cloud.

Ele não é apenas um "login". É o sistema que garante que o contexto que você criou na IDE do trabalho esteja disponível
no seu notebook em casa, que as API Keys dos seus apps estejam seguras, e que os limites do seu plano sejam respeitados
em todos os pontos de entrada — sem que você precise configurar nada manualmente.

> [!IMPORTANT] O Kaffyn SSO é **Closed Source / SaaS**. É exclusivo do Kaffyn Cloud e não está disponível para
> self-host. O **Vectora KV Local** e o **Vectora Agent** funcionam completamente sem SSO no modo Local/Open Source.

---

## 🏛️ O Papel do SSO no Ecossistema

```text
Vectora Agent (local)  ─────┐
Vectora Chat (web/mobile) ──┼──▶  Kaffyn SSO  ──▶  Vectora KV Cloud (K8s)
Extensions (VS Code etc.) ──┘         │
                                       ▼
                              Cloudflare D1 (SQL)
                         [Auth · Billing · API Keys · Quota]
```

O SSO é o ponto de decisão para toda requisição ao Kaffyn Cloud:

1. **Quem é você?** (Autenticação via JWT)
2. **O que você pode fazer?** (RBAC + Escopos de API Key)
3. **Quanto você tem?** (Quota de storage em GB)
4. **Onde estão seus dados?** (Mapeamento de Shard: `User_ID → Node K8s`)

---

## 🔐 Segurança: Arquitetura "Air Gap"

Os dados de identidade e pagamento **nunca tocam o cluster Kubernetes** onde o Vectora KV roda.

| Camada           | Tecnologia             | O que armazena                                        |
| :--------------- | :--------------------- | :---------------------------------------------------- | ----------- | ---------------- | ----------- |
| **Identidade**   | Cloudflare D1 (SQL)    | `kaffyn_uuid`, email, perfis OAuth                    |
| **Billing**      | Cloudflare D1 + Stripe | Plano, datas de renovação, histórico                  |
| **API Keys**     | Cloudflare D1          | **Hash** da chave (nunca o segredo em texto plano)    |
| **Quota**        | Cloudflare D1          | `user_id                                              | plan        | storage_limit_gb | used_bytes` |
| **Shard Map**    | Cloudflare D1          | `user_id                                              | bucket_name | k8s_node_id`     |
| **Conhecimento** | BadgerDB (K8s Volume)  | Vetores e documentos — isolados por namespace/coleção |

**Se o cluster K8s for comprometido:** O atacante vê vetores do Tenant atacado. Não vê API Keys de outros usuários,
dados de pagamento ou credenciais de acesso. Esses dados estão na Cloudflare, protegidos pelo WAF e pelos Workers de
borda.

---

## 🧩 Funcionalidades

### Autenticação Unificada

- Login social: **GitHub**, **Google**, e-mail + senha
- JWT com refresh automático — sessão persistente entre dispositivos
- One-click login no Vectora Agent via browser redirect (sem copiar tokens manualmente)

### Gestão de API Keys (Vetora API Key)

Disponível nos planos **Pro** e **Enterprise**:

- Crie chaves com escopos granulares: `read`, `write`, `search`, `admin`
- Rate limiting configurável por chave
- Revogação imediata via dashboard
- Rotação automática com período de sobreposição (evita downtime nos seus apps)

> [!TIP] A **Vectora API Key** é o que transforma o Vectora KV em uma plataforma. Com ela, qualquer desenvolvedor pode
> integrar busca semântica e memória de agentes em qualquer app — sem gerenciar infraestrutura.

### Controle de Quota em Tempo Real

- Gauge de uso de storage (Input Quota em GB) atualizado a cada operação de ingestão
- Alertas configuráveis (ex: notificação ao atingir 80% do limite)
- Histórico de consumo por coleção e por período

### Gerenciamento de Plano

- Upgrade / Downgrade com efeito imediato
- Faturamento baseado em **GB de arquivo original (Input Quota)** — sem contagem de tokens ou dimensões de vetor

---

## 🔄 Fluxo de Autenticação (Vectora Agent)

```text
1. Usuário executa: vectora-agent login
2. Browser abre: https://sso.kaffyn.com/authorize?client=agent&...
3. Usuário faz login (GitHub / Google / e-mail)
4. SSO gera JWT com escopos do plano atual
5. Token é armazenado localmente em ~/.vectora/auth.json
6. Agent usa o JWT em todas as requisições ao KV Cloud
7. Refresh automático antes da expiração (sem re-login)
```

---

## 📊 Planos e Limites

| Plano                | Storage     | API Keys     | Créditos de IA | Preço             |
| :------------------- | :---------- | :----------- | :------------- | :---------------- |
| **Gratuito (Local)** | Disco local | —            | BYOK           | Grátis            |
| **Simbólico**        | 5 GB Cloud  | —            | BYOK           | Custo operacional |
| **Pro**              | 20 GB Cloud | ✅           | ✅ Inclusos    | Assinatura        |
| **Enterprise**       | Ilimitado   | ✅ Multi-key | ✅ Volume      | Contrato          |

> [!NOTE] O **Plano Simbólico** não gera lucro para a Kaffyn — ele cobre apenas os custos operacionais de
> infraestrutura. O objetivo é garantir que todo programador tenha acesso a uma memória agêntica real na nuvem sem
> barreira financeira.

---

## Self-Host e Open Source

O Kaffyn SSO não está disponível para self-host. Para uso 100% privado e sem dependência da Kaffyn:

1. Use o **Vectora KV** no modo local (binário + BadgerDB local)
2. Use o **Vectora Agent** com BYOK (suas próprias chaves de LLM)
3. Implemente sua própria camada de auth (o KV aceita qualquer JWT válido configurado pelo operador)

O **Vectora KV Local** e o **Vectora Agent** funcionam sem dependência do SSO. A camada **Vectora KV Cloud** (control
plane, tenancy management, quotas/billing e operação gerenciada) é proprietária.

---

_Parte do ecossistema [Vectora](https://github.com/Kaffyn/Vectora) — mantido pela [Kaffyn](https://kaffyn.com)._ _SaaS
Proprietário · Powered by Cloudflare · Segurança em camadas_
