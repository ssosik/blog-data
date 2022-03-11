---
title: Writeup on Testing in Go
description: ""
lead: ""
date: "2019-04-02T09:19:22-04:00"
lastmod: "2019-04-02T09:19:22-04:00"
tags:
  - golang
  - bookmark
draft: true
weight: 50
images: []
contributors:
  - steve
---

https://blog.afoolishmanifesto.com/posts/testing-in-golang/

> The first cool thing you can see is the trivial creation of ts, a test http
> server that can serve content for the client I’m testing. Another convenience
> is that I can trivially load content from disk because when testing a package
> go test automatically runs the test harness in the package directory, where
> you can put various bits of test data.
> 
> This example isn’t even as good as it could get, but I’m trying to first
> increase coverage before adding various test cases. If you write Go and want
> to get better at testing, I strongly recommend watching [Mitchell Hashimoto’s
> Advanced Testing with Go](https://www.youtube.com/watch?v=8hQG7QlcLBk).
> 
> If you watch that talk you’ll see really powerful examples where, for example,
> in a single function he creates both a client and server socket for use in
> tests. This is something I would never have consider
