---
title: WIP Dev notes on hugo blog
description: ""
lead: ""
date: "2021-12-06T14:23:23-0500"
lastmod: "2021-12-06T14:23:23-0500"
tags:
  - hugo
  - blog
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
brew install hugo
hugo new site sosik-notes-papermod -f yml
cd sosik-notes-papermod
git init
git branch -m main
git submodule add --depth 1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule add https://horkhork@github.com/horkhork/vimdiary.git content/notes
git submodule update --init --recursive # needed when you reclone your repo (submodules may not get cloned automatically)

# Write config.yml: Set `theme: "PaperMod"

hugo server

hugo new blog/first_post.md
```
