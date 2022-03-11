---
title: MAC OS X how to forward SSH agent into a container
description: ""
lead: ""
date: "2019-07-29T11:23:38-04:00"
lastmod: "2019-07-29T11:23:38-04:00"
tags:
  - work
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

Use this tool https://github.com/avsm/docker-ssh-agent-forward

Follow install instructions

In the docker-compose file, use these settings:

+ volumes:
+   ssh-agent:
+     external: true
…
      environment:
~       - SSH_AUTH_SOCK=/ssh-agent/ssh-agent.sock
      volumes:
~       - ssh-agent:/ssh-agent

Where the above values come from the output of
`pinata-ssh-mount`
> -v ssh-agent:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent/ssh-agent.sock

The trick was setting the top-level ssh-agent volume with the “external: true” option
