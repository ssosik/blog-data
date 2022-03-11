---
title: Create or reconnect to tmux session
description: ""
lead: ""
date: "2019-06-28T08:07:56-04:00"
lastmod: "2019-06-28T08:07:56-04:00"
tags:
  - tmux
  - cli
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

This will create the named session `main` if it does not exist, or reconnect to
it if it does exist.
```sh
ssh ssosik -oForwardAgent=yes -t tmux -2CC new-session -A -s main
```
