---
title: Golang related notes
description: ""
lead: ""
date: "2019-04-03T14:30:32-04:00"
lastmod: "2019-04-03T14:30:32-04:00"
tags:
  - golang
draft: false
weight: 50
images: []
contributors:
  - steve
---

# Links

- [Golang 1.12 release notes](https://golang.org/doc/go1.12)
- [Working Set Size (WSS) Tools for Linux](https://github.com/brendangregg/wss)
- [Go Memory Management](https://povilasv.me/go-memory-management/)
- [Understanding Real-World Concurrency Bugs in Go](https://songlh.github.io/paper/go-study.pdf)

# Use Go to install Go

Based on this https://golang.org/doc/install#extra_versions

You can use an older installed version of Go to install a newer version:

```sh
$ go get golang.org/dl/go1.12.1
$ go1.12.1 download
$ go1.12.1 version
go version go1.12.1 linux/amd64
```

# Golang race detection

https://medium.com/krakensystems-blog/golang-race-detection-51a1fea43931

# Go executable size visualization using D3

This might come in handy at some point
https://github.com/knz/go-binsize-viz

# Use golang delve to run a precompiled binary

```bash
ENVIRONMENT=variables ./bin/dlv exec ./bin/BINARY <args> -- <flags>
```

## Set a break point

```bash
b file.go:605
# Next
n
```

# An interesting presentation by Dave Cheney on TDD

https://www.youtube.com/watch?v=UKe5sX1dZ0k

Key take-aways:
- Design packages around behavior instead of implementation
- Bubble up unit tests to be at the behavior level instead of the implementation
    level
- shy away from mocks in favor of:
    - focusing on behavior
    - pure functions
    - onion architecture
    - hexagon architecture
    - ports and adapters

Instead of stubbing a DB connection, focus on the behavior; create an interface
that abstracts the DB implementation to provide the required behavioral
interfaces.
