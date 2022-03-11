---
title: Dangers of large datastructures in Golang
description: ""
lead: ""
date: "2019-04-02T09:08:37-04:00"
lastmod: "2019-04-02T09:08:37-04:00"
tags:
  - golang
  - bookmark
draft: true
weight: 50
images: []
contributors:
  - steve
---

https://syslog.ravelin.com/further-dangers-of-large-heaps-in-go-7a267b57d487

> If you have a large heap, a large amount of allocated memory that you need to
> keep throughout the lifetime of a process (for example large lookup tables, or
> an in-memory database of some kind), then to keep the amount of GC work down
> you essentially have two choices as follows.

>  1. Make sure the memory you allocate contains no pointers. That means no
>     slices, no strings, no time.Time, and definitely no pointers to other
>     allocations. If an allocation has no pointers it gets marked as such and
>     the GC does not scan it.
>  2. Allocate the memory off-heap by directly calling the mmap syscall
>     yourself. Then the GC knows nothing about the memory. This has upsides and
>     downsides. The downside is that this memory can’t really be used to
>     reference objects allocated normally, as the GC may think they are no
>     longer in-use and free them.
>
> ...
>
> So what are the lessons to learn here? If you are using Go for data-processing
> then you either can’t have any long-term large heap allocations or you must
> ensure that they don’t contain any pointers. And this means no strings, no
> slices, no time.Time (it contains a pointer to a locale), no nothing with a
> hidden pointer in it. I hope to follow up with some blog posts about tricks
> I’ve used to do that.
