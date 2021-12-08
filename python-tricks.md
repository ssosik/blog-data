---
title: Python Tricks
description: ""
lead: ""
date: "2021-12-08T14:41:44-0500"
tags:
  - python
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Debugging with GDB

https://wiki.python.org/moin/DebuggingWithGdb

```bash
gdb -c <core file> <executable>
(gdb) python
    import sys
    sys.path.append(".")
    import pygdb
(gdb)<ctrl-D>

thread apply all py-list

py-up/py-down to hop up and down the stack
```
