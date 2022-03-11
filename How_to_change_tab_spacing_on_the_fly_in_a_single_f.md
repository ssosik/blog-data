---
title: How to change tab spacing on the fly in a single file
description: ""
lead: ""
date: "2019-03-06T10:16:00-05:00"
lastmod: "2019-03-06T10:16:00-05:00"
tags:
  - vim
  - blog
draft: true
weight: 50
images: []
contributors:
  - steve
---

Useful link:
https://stackoverflow.com/questions/2054627/how-do-i-change-tab-size-in-vim

Call `:set expandtab tabstop=2 shiftwidth=2 softtabstop=2` and then
visually select the region to re-indent and hit `=`.
