# MachiOnCoffee

Bem-vindo ao repositório do **MachiOnCoffee**, um blog minimalista desenhado para priorizar a leitura contínua e a
escrita sem atritos!

Este projeto não depende de bancos de dados nem frameworks pesados (como Next.js ou React). Todo o site é gerado
estaticamente utilizando o [Hugo](https://gohugo.io/) juntamente ao tema estético e responsivo
[Hextra](https://hextra.imfing.com/).

## Como Funciona o Nosso Setup?

O blog foi desenhado com o objetivo de dar o menor trabalho possível:

- Todo tipo de publicação é feita através de arquivos limpos em Markdown (`.md`).
- A indexação, catalogação de anos, meses e formatação do portal é totalmente cuidada por um **Script Python
  Automático**.
- O GitHub faz o Deploy de graça e magicamente na _branch principal_ por meio de GitHub Actions usando a infraestrutura
  do **GitHub Pages**.

## Requisitos Iniciais para Contribuição Local

Como o próprio formato de automatização exige ferramentas enxutas, recomendamos a seguinte instalação caso deseje gerar
os builds ou rodar as validações de script:

1. **Hugo (Extended)** Usado apenas para realizar um "preview" local da plataforma.
   - Windows: `winget install Hugo.Hugo.Extended`
   - Linux: `sudo apt install hugo` (ou similar)
2. **Pre-Commit** (Python/Pip) Ferramenta incrivelmente útil para assegurar a beleza do repositório, formatar markdowns
   (usando _Prettier_), arrumar espaços duplos, validar tipos da linguagem com Mypy, e rodá-lo invisivelmente.
   - Instale-o com: `pip install pre-commit`

### Instalando a Automação do Repositório

Uma vez iniciado nessa pasta, para que o sistema funcione na hora do seu commit e atualize a página principal para você,
basta ativar o hook na raiz:

```bash
pre-commit install
```

Pronto, você nunca mais terá que se preocupar com indexações manuais!

## Como escrever e publicar artigos?

Criar um post é literalmente só criar uma pasta sob o capô!

1. Crie um diretório para o seu post dividido pelo Mês e pelo Dia diretamente na pasta `content/`: Exemplo:
   `content/04/17/minha-receita-de-cafe/index.md`

2. O seu novo arquivo `index.md` DEVE obrigatoriamente possuir um Front Matter (cabeçalho de metadados) limpo. Adicione
   este padrão no topo:

```markdown
---
title: "Minha Receita de Café"
date: "2026-04-17T15:00:00-03:00"
slug: minha-receita-de-cafe
tags:
  - cafe
  - programacao
draft: false
---

E agora você é livre para dissertar livremente... Tudo suportado pelo ecosistema de texto **Markdown** puro.
```

3. Salve, jogue pro repositório pelo `git add .` e `git commit -m "novo post"`. Seu terminal vai acionar a trava
   automática de prévias, formatar espaçamentos faltantes, recriar magicamente a Homepage interativa, e o seu commit
   passará com sucesso. Quando o _Push_ for lançado, o Github Pages assumirá o leme da publicação real!

## Como ver as mudanças em sua máquina?

Muitas vezes você quer ver o resultado do seu post em tempo real antes de commitar, você pode iniciar o servidor
instantâneo do Hugo assim:

```bash
hugo server --buildDrafts --disableFastRender
```

_Em seguida acesse no seu navegador: `http://localhost:1313/`_

---

> Baseado livremente nas brilhantes ideias técnicas abordadas por Akita no post _"Meu Novo Blog - Como Eu Fiz"_
> (setembro de 2025). Trocamos os pipelines enferrujados de Ruby pelo conforto do Python!
