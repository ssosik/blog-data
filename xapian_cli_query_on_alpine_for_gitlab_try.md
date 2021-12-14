---
title: xapian cli query on alpine for gitlab try
description: ""
lead: ""
date: "2021-08-30T08:14:07-04:00"
lastmod: "2021-08-30T08:14:07-04:00"
tags:
  - work
  - docker
  - alpine
  - xq
  - git
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

Gitlab looks like it might be easier to build XQ on. Try to get XQ building in
an Alpine docker container and then try that in Gitlab.

```bash

docker run -ti alpine /bin/sh
docker run -ti rust /bin/sh

apk --update add git rust cargo alpine-sdk xz && \
    git clone --recurse-submodules https://github.com/ssosik/xapian-query-cli.git && \
    cd xapian-query-cli && \
    make
```
