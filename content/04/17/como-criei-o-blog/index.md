---
title: "Como eu criei meu novo blog"
date: "2026-04-17T16:00:00-03:00"
slug: como-criei-o-blog
tags:
  - infra
  - python
  - hugo
draft: false
---

## A Inspiração

Recentemente me deparei com o artigo do grande Fabio Akita sobre como ele arquitetou a nova versão do blog dele ([Meu Novo Blog - Como Eu Fiz](https://akitaonrails.com/2025/09/10/meu-novo-blog-como-eu-fiz/)), e decidi seguir o mesmo caminho de adotar a simplicidade de páginas estáticas e fugir de dores de cabeça com banco de dados!

O problema que programadores encontram frequentemente é a fadiga da ferramenta. Todo mundo quer construir a "engine de blog ideal" e no final esquecemos de escrever o conteúdo real. Dessa vez eu decidi usar a estratégia que foca puramente nos textos com uma infraestrutura super simples.

### A Ferramenta: Hugo + Hextra

O Hugo é incrivelmente rápido e eficiente, pois é construído em Go. E ele suporta o formato do desenvolvedor: Markdown!
Ao invés do Jekyll ou tentar configurar um framework NextJS imenso para um CMS que mal vou usar as features, eu utilizei Hugo junto do tema minimalista **Hextra**.

A grande sacada é que o meu workflow agora virou apenas criar pastas e arquivos dentro de `content/{MM}/{DD}/{slug}/index.md`, escrever tudo em Markdown e fazer commit.

### Hospedagem Gratuita: GitHub Pages

Um detalhe muito importante da infraestrutura que decidi seguir foi adotar o **GitHub Pages** para hospedar o blog. Enquanto algumas ferramentas exigem integração com o Vercel ou Netlify, o GitHub Pages nos fornece um ambiente incrível de forma nativa e 100% gratuita.

**Mas atenção, tem um pulo do gato para o Action funcionar sem dar erro `404 Not Found`:**

1. Primeiro o seu repositório precisa ser **Público** (A hospedagem do Github Pages só é de graça para repositórios públicos).
2. Vá na aba `Settings` > `Pages` do seu repositório.
3. Em "Build and deployment", altere o "Source" (Fonte) para **GitHub Actions**.
4. (Opcional) Configure o seu domínio personalizado logo abaixo se você tiver um.

Feito isso, eu só precisei criar um arquivo `.github/workflows/pages.yaml` que contém um passo de _GitHub Action_ instrucionado para fazer o build no Hugo. Assim, a cada `git push`, o deploy ocorre magicamente sem custo algum!

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["master"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false
defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.160.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          submodules: recursive
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.24"
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4
      - name: Setup Hugo
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: |
          hugo \
            --gc --minify \
          --baseURL "https://${{ github.repository_owner }}.github.io/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### Usando Domínio Customizado no Cloudflare

Uma dica de ouro se você, assim como eu, quiser colocar o seu próprio domínio apontando pro GitHub Pages passando pela CDN maravilhosa (e gratuita) da Cloudflare:

1. No painel do Cloudflare (aba de **DNS**), crie 4 registros do tipo `A` apontando o seu domínio raiz para os IPs centrais do GitHub: `185.199.108.153`, `185.199.109.153`, `185.199.110.153` e `185.199.111.153`.
2. Crie 1 registro `CNAME` chamado `www` apontando para a sua url do GitHub (ex: `seu_usuario.github.io`).
3. **O grande truque:** Na hora de criar esses registros, deixe a "Nuvenzinha" laranja do Cloudflare **inativa (Cinza - DNS Only)** momentaneamente. Acesse a tela do repositório no GitHub, coloque seu domínio em `Settings` > `Pages` e espere ficar verdinho informando _DNS check successful_.
4. Somente após a checagem passar no GitHub, volte no Cloudflare e ative/ligue a nuvem laranja (indo para o modo _Proxied_). Para evitar a famosa tela preta de "Too Many Redirects", acesse obrigatoriamente a aba de Segurança **SSL/TLS -> Overview** do Cloudflare e force o modo de criptografia para **"Full (strict)"**.

Para arrematar a segurança, vá na seção Edge Certificates e ligue a chavinha _Always Use HTTPS_. O Cloudflare cuidará milagrosamente de encriptar todos os cantos do seu blog em altíssima velocidade!

### Python salvando o dia (Tchau, Ruby!)

O Akita usou Ruby pra gerar o script de indexação porque... bom, ele literalmente tem o nome da linguagem tatuado na carreira dele. Eu não tinha o Ruby instalado e queria que a engine inteira fosse mais compatível com os meus scripts locais.

Então, ao invés de usar o mesmo _script_ Ruby do artigo original para agrupar as pastas baseadas na data `Ano - Mês`, eu transformei ele todo em Python puro, usando apenas lib standard e o pacote yaml. O Python é incrivelmente bom pra ler arquivos e manipular textos sem esforço.

E, assim como ele deixou os blocos do GitHub Actions dele no post original, segue aqui o código do meu `generate_index.py` que eu uso para parsear tudo e cuspir os links perfeitamente!

```python
import os
import yaml
from datetime import datetime
from collections import defaultdict

def escape_markdown(text):
    return str(text).replace('[', '\\[').replace(']', '\\]')

entries = []

for root, _, files in os.walk('content'):
    for file in files:
        if file != 'index.md':
            continue

        path = os.path.join(root, file)

        # Ignorar o index principal e o _index.md
        if path.replace('\\', '/') in ['content/index.md', 'content/_index.md']:
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines or lines[0].strip() != '---':
                continue

            fm_lines = []
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                fm_lines.append(lines[i])
                i += 1

            if i < len(lines) and lines[i].strip() == '---':
                front = yaml.safe_load(''.join(fm_lines))
                if front and front.get('title') and front.get('date'):
                    try:
                        # Hugo usa formato RFC 3339, usando fromisoformat do python
                        # Algumas vezes pode ter Z ao inves de +00:00
                        date_str = str(front['date']).replace('Z', '+00:00')
                        date_obj = datetime.fromisoformat(date_str)

                        url = path.replace('\\', '/').replace('content/', '').replace('/index.md', '/')
                        entries.append({
                            'title': front['title'],
                            'url': url,
                            'date': date_obj
                        })
                    except ValueError:
                        pass
        except Exception as err:
            print(f"Erro processando {path}: {err}")

# Ordenar mais recentes primeiro
entries.sort(key=lambda e: e['date'], reverse=True)

# Agrupar por ano e mes
grouped = defaultdict(list)
for e in entries:
    grouped[(e['date'].year, e['date'].month)].append(e)

# Meses em pt-br para ficar mais legal (ou ingles como no original)
MONTHNAMES = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

sorted_keys = sorted(grouped.keys(), reverse=True)

new_content = "---\ntitle: MachiOnCoffee\n---\n\n"

for year, month in sorted_keys:
    month_name = MONTHNAMES[month]
    new_content += f"## {year} - {month_name}\n\n"

    for post in grouped[(year, month)]:
        new_content += f"- [{escape_markdown(post['title'])}]({post['url']})\n"

    new_content += "\n"

# Remove todos os \n sobrando do fim e garante que o arquivo acabe só com 1 \n
# Isso previne que o end-of-file-fixer do pre-commit fique brigando com o nosso script o tempo todo!
new_content = new_content.rstrip() + "\n"

target_file = 'content/_index.md'
write_file = True

if os.path.exists(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    if existing_content == new_content:
        write_file = False

if write_file:
    with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    print("Generated content/_index.md with posts grouped by year & month.")
else:
    print("content/_index.md is already up to date.")
```

### Lidando com Imagens (Tchau, AWS S3!)

No setup original do Akita, ele mantinha um script em bash complexo atado ao gerenciador de arquivos Nautilus do Linux para fazer upload das fotos e capturas de tela diretamente para um bucket S3 da AWS.

Eu decidi **simplificar**. Para quê ter complexidade na nuvem se podemos armazenar tudo localmente no repositório?

No Hugo, tudo que é jogado na pasta `static/` é transportado magicamente para a raiz do site na pasta `public/` durante o build. Isso significa que podemos guardar todas as imagens dentro do diretório do projeto, deixar o Github hospedar isso tudo para nós de graça dentro do mesmo repositório e referenciar via caminhos relativos sem pagar nenhum centavo extra nem dependermos dos serviços da Amazon!

### Automatizando tudo com Pre-Commit

Para garantir que eu não precise nunca lembrar de rodar o `generate_index.py` ou de ter que formatar meus textos Markdown (acredite, espaçamentos importam), eu configurei o framework **Pre-Commit** em Python.

Simplesmente adicionei o Prettier (para auto-formatação) e um hook local que roda o indexador. A cada tentativa de `git commit`, o sistema roda as verificações na minha máquina, arruma meus arquivos, re-gera a árvore de posts, e aí sim joga pro GitHub!

Com toda essa base setada, o único esforço que eu terei agora será criar esse arquivo (que neste momento tem o nome de `index.md`), abri-lo, editar o texto, e commitar. A indexação, a formatação e o publish pra página acontecem sozinhos!

Para que você possa copiar, esse é o código final do meu `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
        args: ["--allow-multiple-documents"]
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types: [markdown, yaml]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.1
    hooks:
      - id: mypy
        files: \.py$
        types_or: [text]

  - repo: https://github.com/pre-commit/pygrep-hooks
    rev: v1.10.0
    hooks:
      - id: text-unicode-replacement-char
        exclude: (?x)^(.*\.md*)$

  - repo: local
    hooks:
      - id: generate-index
        name: Generate Index
        entry: python generate_index.py
        language: system
        pass_filenames: false
```
