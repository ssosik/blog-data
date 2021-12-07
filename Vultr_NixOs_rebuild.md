---
title: Vultr NixOS rebuild
description: ""
lead: ""
date: "2021-10-29T15:15:27-04:00"
lastmod: "2021-10-29T15:15:27-04:00"
categories:
- nixos
- cloud-deployment
tags:
  - vultr
  - nixos
  - little-fluffy.cloud
  - taskserver
  - mail
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Going to stand up a new Vultr VM to try rebuilding mail.little-fluffy.cloud.
This will include restoring backups from rsync.net and getting mail to work
again.

# Create the VM

Cloud Compute, NY/NJ, NixOS 20.09 (from ISO Library), 55 GB SSD 2GB RAM 2TB bandwidth

Hostname: mail2.little-fluffy.cloud

> ssh-keygen -t ed25519 -b 4096 -f .ssh/vultr -C 'New SSH key for new mail2.little-fluffy.cloud vultr instance on 10/29/2021'

Adding an SSH key through the Vultr UI doesn't appear to work for Nixos

Need to create new github repo with a bash script that starts up nix subshell
with git (if needed) and installs ssh authorized key and pulls down nix configs
and applies them

# Retrying with some newer documentation

Remaining steps continue here: https://github.com/ssosik/nixos-configs
