---
title: sqlparse / sqlformat tool - sqlformatter
description: ""
lead: ""
date: "2019-03-27T13:06:55-04:00"
lastmod: "2019-03-27T13:06:55-04:00"
tags:
  - sql
  - vim
  - python
  - pip
draft: true
weight: 50
images: []
contributors:
  - steve
---

Install locally into `$USER/.local/bin`:

```sh
pip3 install --user sqlparse
```

Ensure `$USER/.local/bin/` is added to PATH

And then in Vim select a visual range and do the following
```
'<,'>%!sqlformat --reindent --keywords upper --identifiers lower -
```
