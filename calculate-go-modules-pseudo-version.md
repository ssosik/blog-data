---
title: How to calculate go modules pseudo version tag string
description: ""
lead: ""
date: "2020-10-13T14:07:54-04:00"
lastmod: "2020-10-13T14:07:54-04:00"
tags:
  - work
  - git
  - golang
  - go-modules
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

In go.mod we can specify "replace" directives to point to custom module
locations, either locally or on private bitbucket.

```
replace private/syssec v1.6.0 => git.private.com/sources/syscomm-security-golang-libs.git/core/src/private/syssec v0.0.0-20200821183613-3374156d683e
```

Golang is pretty particular about the trailing version string. This page helps
explain it: https://stackoverflow.com/questions/52242077/go-modules-finding-out-right-pseudo-version-vx-y-z-timestamp-commit-of-re

To calculate it:

```
╰─ git clone ssh://git@git.private.com:7999/sources/syscomm-security-golang-libs.git
╰─ cd syscomm-security-golang-libs
╰─ git checkout v1.6.0
╰─ TZ=UTC git --no-pager show \
  --quiet \
  --abbrev=12 \
  --date='format-local:%Y%m%d%H%M%S' \
  --format="%cd-%h"
20200821183613-3374156d683e
```

In order to take a new version, update your local repo, checkout the tag, and
then run the above command to get the timestamp-commithash part of the string.
Then, plug that into the v0.0.0 version:
> v0.0.0-20200821183613-3374156d683e
