---
title: Hugo site frontmatter notes
description: ""
lead: ""
date: "2021-12-02T16:05:42-05:00"
lastmod: "2021-12-02T16:05:42-05:00"
tags:
  - hugo
  - blog
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Existing frontmatter example:
```
---
title: VIM how to format XML region in file
date: "2021-09-16T08:43:15-04:00"
tags:
  - vim
  - xml
authors:
  - Steve Sosik
id: MucpkUH1SxuS_AEBbHAxgA
origid: MucpkUH1SxuS_AEBbHAxgA
weight: 0
revision: 1
latest: true
---
```

Remove from above:
- id
- origid
- revision

Keep:
- title
- date
- tags
- authors
- weight

Add:
- draft
- description?
- images?
- type?
- lastmod
- slug?
- summary?
