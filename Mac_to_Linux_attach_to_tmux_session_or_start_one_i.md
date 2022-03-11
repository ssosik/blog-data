---
title: Mac to Linux attach to tmux session or start one if it does not exist
description: ""
lead: ""
date: "2019-08-12T09:05:13-04:00"
lastmod: "2019-08-12T09:05:13-04:00"
tags:
  - work
  - tmux
  - ssh
  - bash
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

```sh
ssh ssosik -oForwardAgent=yes -t tmux -2CC new-session -A -s main
```
