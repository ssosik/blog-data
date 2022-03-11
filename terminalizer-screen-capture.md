---
title: How to record a terminal session and export it as a gif
description: ""
lead: ""
date: "2020-09-02T09:41:57-04:00"
lastmod: "2020-09-02T09:41:57-04:00"
tags:
  - tika
  - nix
  - rust
  - nodejs
  - cli
  - screencapture
  - gif
draft: true
weight: 50
images: []
contributors:
  - ""
---

Use <https://github.com/faressoft/terminalizer>

Add `nodejs` to home.packages.pkgs

Install locally
```
npm install terminalizer
```

Record
```
node_modules/terminalizer/bin/app.js record demo
```



