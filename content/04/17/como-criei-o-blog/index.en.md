---
title: "How I created my new blog"
date: "2026-04-17T16:00:00-03:00"
slug: how-i-created-the-blog
tags:
  - infra
  - python
  - hugo
draft: false
---

## The Inspiration

Recently I came across Fabio Akita's article on how he architected the new version of his blog
([My New Blog - How I Did It](https://akitaonrails.com/2025/09/10/meu-novo-blog-como-eu-fiz/)), and I decided to follow
the same path of adopting the simplicity of static pages and avoiding database headaches!

The problem programmers often encounter is tool fatigue. Everyone wants to build the "ideal blog engine" and in the end,
we forget to write actual content. This time I decided to use a strategy that focuses purely on text with a super simple
infrastructure.

### The Tool: Hugo + Hextra

Hugo is incredibly fast and efficient since it's built in Go. And it supports the developer's format: Markdown! Instead
of Jekyll or trying to configure a massive NextJS framework for a CMS I'll barely use, I utilized Hugo with the
minimalist **Hextra** theme.

The big trick is that my workflow has now become just creating folders and files inside
`content/{MM}/{DD}/{slug}/index.md`, writing everything in Markdown, and committing.

### Free Hosting: GitHub Pages

A very important detail of the infrastructure I decided to follow was adopting **GitHub Pages** to host the blog. While
some tools require integration with Vercel or Netlify, GitHub Pages provides an amazing environment natively and 100%
free.

**But beware, there's a trick to make the Action work without giving a `404 Not Found` error:**

1. First, your repository needs to be **Public**.
2. Go to the `Settings` > `Pages` tab of your repository.
3. Under "Build and deployment", change the "Source" to **GitHub Actions**.

Once that's done, I just needed to create a `.github/workflows/pages.yaml` file containing a _GitHub Action_ step
instructed to build with Hugo. Thus, on every `git push`, the deploy happens magically without any cost!

### Python Saving the Day (Bye, Ruby!)

Akita used Ruby to generate the indexing script. I didn't have Ruby installed and wanted the entire engine to be more
compatible with my local scripts.

So instead of using the same Ruby script as the original article to group folders based on the `Year - Month` date, I
transformed it all into pure Python, using only the standard library and the `yaml` package. Python is incredibly good
at reading files and manipulating text effortlessly.

### Handling Images (Bye, AWS S3!)

In the original setup, Akita maintained a complex bash script tied to the Linux Nautilus file manager to upload photos
directly to an AWS S3 bucket.

I decided to **simplify**. Everything thrown into the `static/` folder is magically transported to the root of the site
during build. This means we can keep all images inside the project directory, let GitHub host it all for us for free,
and reference them via relative paths!

### Automating everything with Pre-Commit

To ensure I never have to remember to run `generate_index.py` or format my Markdown texts, I configured the
**Pre-Commit** framework in Python.

I simply added Prettier (for auto-formatting) and local hooks that run the indexer and the **full Hugo Build**. Every
time I try to `git commit`, the system runs the checks on my machine, fixes my files, regenerates the post tree,
executes the optimized build, and places the ready pages into the `static/` folder. This way, GitHub Pages receives the
site already processed and ready for deployment!

With this foundation set, my only effort now will be creating the content. Indexing, formatting, building, and
publishing happen on their own!
