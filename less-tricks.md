---
title: Less Tricks
description: "How to filter out irrelevant lines when viewing a file in less"
lead: ""
date: "2021-12-14T13:52:12-0500"
categories:
  - cli
tags:
  - less
  - bash
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

When viewing a file in Less, especially really verbose log files, it can be
helpful to exclude lines that match certain patterns. Use the `&!` operator!
Alternatively, you can use a positive filter to only show lines that match the
pattern with the `&` operator.

With a file open, hit `&!` and then enter in an exclusion pattern, separating
unique patterns with a `|`

    boring1|boring thing 2|i'm not interesting either

You can even trigger this filtering when opening file(s) from the command line

    less +'&!thing 1|thing 2'
