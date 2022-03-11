---
title: quick notmuch python bindings test
description: ""
lead: ""
date: "2019-09-24T09:03:14-04:00"
lastmod: "2019-09-24T09:03:14-04:00"
tags:
  - notmuch
  - python
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

# python3.7
```python
from notmuch import Query, Database
db = Database('/Users/ssosik/mail', create=False)
msgs = Query(db, 'from:abijoor').search_messages()
for msg in msgs:
    print(msg)
```
