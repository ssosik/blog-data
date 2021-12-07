---
title: Use nix and direnv and pipenv to create a Python venv
description: ""
lead: ""
date: "2021-09-24T14:35:31-04:00"
lastmod: "2021-09-24T14:35:31-04:00"
categories:
- nixos
- cli
tags:
  - python
  - pip
  - nix
  - venv
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Idea from https://gist.github.com/araa47/10537f74ee061b26e18ae21d4bfca7d9

Add `pipenv` to home.packages in home.nix

```
╰─ cat .envrc Pipfile
───────┬────────────────────────────────────────────────────────────────────────
       │ File: .envrc
───────┼────────────────────────────────────────────────────────────────────────
   1   │ source_up
   2   │ use nix
   3   │ layout_pipenv
   4   │
───────┴────────────────────────────────────────────────────────────────────────
───────┬────────────────────────────────────────────────────────────────────────
       │ File: Pipfile
───────┼────────────────────────────────────────────────────────────────────────
   1   │ [[source]]
   2   │ name = "pypi"
   3   │ url = "https://pypi.org/simple"
   4   │ verify_ssl = true
   5   │
   6   │ [dev-packages]
   7   │
   8   │ [packages]
   9   │
  10   │ [requires]
  11   │ python_version = "3.8"
───────┴────────────────────────────────────────────────────────────────────────

# Allow the directory
direnv allow

# Initialize pipenv
pipenv --python $(which python)

# Add dependencies
pip install cryptography
```
