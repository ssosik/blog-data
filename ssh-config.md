---
title: Useful SSH config settings
date: "2022-03-23T09:57:54-0400"
tags:
- ssh
- cli
weight: 50
---

```
Host bos-lhvrol bos-lhvrol.bos01.<TLD>
  GSSAPIAuthentication yes
  GSSAPIDelegateCredentials yes
  User ssosik
  ForwardX11Trusted no
  ForwardX11 no
  ForwardAgent yes
  Hostname bos-lhvrol.<TLD>
  StrictHostKeyChecking yes
  RequestTTY yes
  ServerAliveInterval 60
  RequestTTY force
  # start new tmux session if if does not exist and then connect/reconnect to it
  RemoteCommand /home/ssosik/.nix-profile/bin/tmux -u -2CC new-session -A -s main
  # Port forwarding for Nvim
  LocalForward 6666 localhost:6666
```
