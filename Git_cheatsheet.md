---
title: Git cheatsheet
description: ""
lead: ""
date: "2021-09-01T19:31:58-04:00"
lastmod: "2021-09-01T19:31:58-04:00"
tags:
  - git
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

How to delete a tag locally and on a remote
https://www.manikrathee.com/how-to-delete-a-tag-in-git.html

Delete the tag locally
    git tag -d refs/heads/main

Delete it from the remote, in this case the tag was confusingly named `refs/heads/main`
    git push origin :refs/tags/refs/heads/main
