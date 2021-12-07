---
title: Nix cheatsheet
description: ""
lead: ""
date: "2020-04-14T16:35:25-04:00"
lastmod: "2020-04-14T16:35:25-04:00"
categories:
- nixos
- cli
tags:
  - nix
  - cheat
  - cli
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Reload and rebuild nix configuration
```bash
sudo nixos-rebuild switch --upgrade
```

# Add a specific package
```bash
nix-shell '<nixpkgs>' -A dovecot
```

# Search for a package
```bash
nix search package
```
