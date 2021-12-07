---
title: nix home-manager ssosik-vm hacking
description: ""
lead: ""
date: "2020-06-03T19:25:13-04:00"
lastmod: "2020-06-03T19:25:13-04:00"
categories:
- nixos
- cli
tags:
  - nix
  - home-manager
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

If the path is messed up, run these:
```bash
export PATH=.nix-profile/bin:$PATH
export NIX_PATH=$HOME/.nix-defexpr/channels${NIX_PATH:+:}$NIX_PATH
```

From https://github.com/rycee/home-manager
