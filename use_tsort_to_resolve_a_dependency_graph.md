---
title: use tsort to resolve a dependency graph
description: ""
lead: ""
date: "2020-02-20T13:55:20-05:00"
lastmod: "2020-02-20T13:55:20-05:00"
tags:
  - work
  - gnu
  - dag
  - tsort
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

From <https://en.wikipedia.org/wiki/Tsort>

Given a list of dependencies, use tsort to derive the proper sequencing of
events:
```bash
tsort <<EOF                                                                                                                                          
a b c d
a c
b c
EOF
a
b
c
d

tsort <<EOF                                                                                                                                        1
a b
a c
b c
d a
EOF
d
a
b
c

tsort <<EOF                                                                                                                                          
3 8
3 10
5 11
7 8
7 11
8 9
11 2
11 9
11 10
EOF
3
5
7
11
8
10
2
9
```
