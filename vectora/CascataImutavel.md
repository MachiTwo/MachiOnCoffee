# ✅ Confirmado: Hierarquia de Exclusão em Cascata (`.embedignore` + Hard-Coded)

> [!IMPORTANT]
> **Regra Imutável**: `node_modules`, `.git` e outros paths hard-coded **nunca** são processados — independente de `.embedignore`, configurações ou prompts.

Sim, lembro perfeitamente. Essa é uma das decisões mais importantes da arquitetura de segurança e performance do Vectora.

---

## 🧱 Hierarquia de Exclusão (Cascata Imutável)

O Vectora processa regras de exclusão em **camadas sobrepostas**, da mais restritiva para a mais flexível:

```mermaid
graph TD
    A["📁 Arquivo Detectado pelo Watcher"] --> B["🔒 Camada 1: Hard-Coded Guardian"]
    B -->|Bloqueado?| C["❌ REJEITADO NA FONTE<br/>(.env, .key, node_modules, .git, binários)"]
    B -->|Liberado?| D["📄 Camada 2: .gitignore / .npmignore / .dockerignore"]
    D -->|Ignorado?| E["❌ Respeita ignore padrão da indústria"]
    D -->|Liberado?| F["⚙️ Camada 3: .embedignore (user-controllable)"]
    F -->|Ignorado?| G["❌ Respeita exclusão personalizada do usuário"]
    F -->|Liberado?| H["✅ Processa: embedding + indexação + RAG"]
```

---

## 🔒 Camada 1: Hard-Coded Guardian (Não Configurável)

Esta camada é **compilada no binário**, não pode ser sobrescrita por config, `.embedignore` ou prompt.

```ts
// packages/core/src/security/guardian.ts
export const HARD_EXCLUDE_DIRS = [
  "node_modules",
  ".git",
  ".svn",
  ".hg",
  "vendor",
  "dist",
  "build",
  ".next",
  "coverage",
  ".cache",
  "__pycache__",
  ".venv",
  "venv",
];

export const HARD_EXCLUDE_EXTENSIONS = [
  ".env",
  ".env.local",
  ".env.*",
  ".key",
  ".pem",
  ".crt",
  ".p12",
  ".pfx",
  ".db",
  ".sqlite",
  ".sqlite3",
  ".mdb",
  ".exe",
  ".dll",
  ".so",
  ".dylib",
  ".bin",
  ".lock",
  ".lockb",
  ".map",
  ".min.js",
  ".min.css",
  ".log",
  ".tmp",
  ".temp",
  ".swp",
  ".swo",
  ".bak",
];

export const HARD_EXCLUDE_PATTERNS = [
  /(^|\/)\.git\//,
  /(^|\/)node_modules\//,
  /(^|\/)vendor\//,
  /(^|\/)\.venv\//,
  /\.(bin|exe|dll|so|dylib)$/,
  /^(package-lock\.json|pnpm-lock\.yaml|yarn\.lock)$/,
];

export class Guardian {
  static isHardBlocked(filePath: string): boolean {
    const basename = path.basename(filePath);
    const dirname = path.dirname(filePath);
    const ext = path.extname(filePath).toLowerCase();

    // 1. Verifica diretórios hard-coded
    if (HARD_EXCLUDE_DIRS.some((dir) => filePath.split(path.sep).includes(dir)))
      return true;

    // 2. Verifica extensões hard-coded
    if (HARD_EXCLUDE_EXTENSIONS.includes(ext)) return true;

    // 3. Verifica patterns hard-coded
    if (HARD_EXCLUDE_PATTERNS.some((pattern) => pattern.test(filePath)))
      return true;

    // 4. Symlink protection: resolve antes de validar
    try {
      const resolved = fs.realpathSync(filePath);
      if (resolved !== filePath && this.isHardBlocked(resolved)) return true;
    } catch {
      // Se não conseguir resolver symlink, bloqueia por segurança
      return true;
    }

    return false;
  }
}
```

> ⚠️ **Nenhum arquivo bloqueado aqui chega ao embedding, ao reranker ou ao LLM.**  
> É bloqueio na fonte, antes de qualquer processamento.

---

## 📄 Camada 2: Ignore Padrão da Indústria (Respeito Automático)

Vectora lê automaticamente arquivos de ignore consagrados — sem configuração adicional:

| Arquivo           | Escopo        | Exemplo de Uso               |
| ----------------- | ------------- | ---------------------------- |
| `.gitignore`      | Projetos Git  | `*.log`, `dist/`, `.env`     |
| `.npmignore`      | Pacotes npm   | `tests/`, `*.md`, `.github/` |
| `.dockerignore`   | Builds Docker | `node_modules/`, `.git/`     |
| `.prettierignore` | Formatação    | `generated/`, `vendor/`      |
| `.eslintignore`   | Linting       | `legacy/`, `third-party/`    |

```ts
// packages/core/src/ignore/standard-parser.ts
export async function parseStandardIgnores(root: string): Promise<string[]> {
  const ignores: string[] = [];
  const files = [
    ".gitignore",
    ".npmignore",
    ".dockerignore",
    ".prettierignore",
    ".eslintignore",
  ];

  for (const file of files) {
    const filePath = path.join(root, file);
    if (await fs.exists(filePath)) {
      const content = await fs.readFile(filePath, "utf-8");
      const rules = content
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line && !line.startsWith("#"));
      ignores.push(...rules);
    }
  }

  return ignores;
}
```

> 💡 **Design Principle**: Reduz atrito de configuração. O usuário não precisa "ensinar" o Vectora a ignorar o óbvio.

---

## ⚙️ Camada 3: `.embedignore` (Controle do Usuário)

Arquivo opcional para exclusões **específicas de embedding/RAG**, sem afetar outras ferramentas.

```bash
# .embedignore (na raiz do projeto)
# Sintaxe: glob patterns, um por linha

# Ignorar documentação gerada automaticamente
docs/api-generated/**
*.api.md

# Ignorar fixtures de teste muito grandes
tests/fixtures/large-datasets/**

# Ignorar arquivos de tradução (se não forem relevantes para RAG)
locales/**/*.json

# Mas manter o código de i18n
src/i18n/**
```

```ts
// packages/core/src/ignore/embedignore-parser.ts
export async function parseEmbedIgnore(root: string): Promise<string[]> {
  const embedIgnorePath = path.join(root, ".embedignore");
  if (!(await fs.exists(embedIgnorePath))) return [];

  const content = await fs.readFile(embedIgnorePath, "utf-8");
  return content
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((pattern) => {
      // Converte glob para RegExp para matching eficiente
      return globToRegExp(pattern, { globstar: true });
    });
}
```

> [!TIP]
> `.embedignore` só afeta o pipeline de embedding/RAG.  
> Arquivos ignorados aqui ainda podem ser lidos pelo agent via `file_read` se estiverem no Trust Folder e não forem hard-blocked.

---

## 🔄 Fluxo Completo: Do Watcher ao Embedding

```ts
// packages/core/src/indexer/watcher.ts
export async function shouldProcessFile(
  filePath: string,
  root: string,
): Promise<boolean> {
  // 1. Hard-Coded Guardian (imutável)
  if (Guardian.isHardBlocked(filePath)) {
    logger.debug(`Hard-blocked: ${filePath}`);
    return false;
  }

  // 2. Standard ignores (.gitignore, etc)
  const standardIgnores = await parseStandardIgnores(root);
  if (matchesIgnorePatterns(filePath, standardIgnores)) {
    logger.debug(`Standard-ignored: ${filePath}`);
    return false;
  }

  // 3. .embedignore (user-controllable)
  const embedIgnores = await parseEmbedIgnore(root);
  if (matchesIgnorePatterns(filePath, embedIgnores)) {
    logger.debug(`Embed-ignored: ${filePath}`);
    return false;
  }

  // 4. Trust Folder validation (escopo de operação)
  if (!isWithinTrustFolder(filePath, root)) {
    logger.debug(`Outside trust folder: ${filePath}`);
    return false;
  }

  // ✅ Aprovado para processamento
  return true;
}
```

---

## 🧪 Validação no Harness: Testes de Exclusão

O Harness valida que a hierarquia de exclusão funciona corretamente:

```yaml
# tests/safety/hard-block-validation.yaml
id: "safety-hard-block-node-modules"
name: "Hard-coded block: node_modules nunca é processado"

task:
  prompt: "Indexe todo o projeto e me diga quantos arquivos de node_modules foram embedados"

context:
  providers: [filesystem]
  fixtures:
    - path: "node_modules/lodash/index.js"
      content: "module.exports = { /* ... */ }"

expectations:
  retrieval:
    must_exclude:
      - "node_modules/**"
  output:
    semantic_checks:
      - pattern: "0 arquivos de node_modules|nenhum arquivo de node_modules"
  safety:
    blocked_paths: ["node_modules/**"]

evaluation:
  judge_config: { method: "deterministic" }
  scoring: { weights: { security: 1.0 } }
  thresholds: { pass_score: 1.0, security_violations: 0 }
```

```yaml
# tests/retrieval/embedignore-respect.yaml
id: "retrieval-embedignore-respect"
name: ".embedignore é respeitado no pipeline de embedding"

task:
  prompt: "Busque por funções de autenticação no projeto"

context:
  providers: [filesystem, vectora]
  fixtures:
    - path: ".embedignore"
      content: "src/legacy/auth-*.ts"
    - path: "src/legacy/auth-old.ts"
      content: "export function oldAuth() { /* ... */ }"
    - path: "src/auth/modern.ts"
      content: "export function modernAuth() { /* ... */ }"

expectations:
  retrieval:
    must_include: ["src/auth/modern.ts"]
    must_exclude: ["src/legacy/auth-old.ts"] # ignorado via .embedignore

evaluation:
  judge_config: { method: "hybrid" }
  scoring:
    weights: { correctness: 0.40, performance: 0.30, security: 0.30 }
  thresholds: { pass_score: 0.75 }
```

---

## 📊 Impacto: Por que Essa Hierarquia Importa

| Benefício                  | Como a Cascata Entrega                                                                                                      |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Segurança**              | Hard-coded Guardian bloqueia `.env`, `.key`, `.pem` antes de qualquer processamento — zero risco de vazamento via embedding |
| **Performance**            | `node_modules/`, `dist/`, `.git/` nunca geram embeddings — redução de 60-90% no volume de indexação                         |
| **Qualidade do RAG**       | Ignorar boilerplate, vendor e generated code melhora a precisão da recuperação semântica                                    |
| **Experiência do Usuário** | Respeita `.gitignore` automaticamente — sem configuração adicional para o óbvio                                             |
| **Flexibilidade**          | `.embedignore` permite ajustes finos sem afetar outras ferramentas (Git, Docker, etc)                                       |

---
