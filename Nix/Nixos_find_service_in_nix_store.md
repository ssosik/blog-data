---
title: Nixos find service in nix store
description: ""
lead: ""
date: "2021-10-28T16:12:59-04:00"
lastmod: "2021-10-28T16:12:59-04:00"
categories:
- nixos
- cli
tags:
  - nixos
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
nix-store --query $(nix-instantiate '<nixpkgs>' -A taskserver)
```
