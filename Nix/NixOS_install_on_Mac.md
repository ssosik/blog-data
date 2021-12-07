---
title: NixOS install on Mac
description: ""
lead: ""
date: "2020-06-01T20:19:13-04:00"
lastmod: "2020-06-01T20:19:13-04:00"
categories:
- nixos
- cli
tags:
  - nixos
  - nix
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Running
```bash
sh <(curl https://nixos.org/nix/install) --darwin-use-unencrypted-nix-store-volume

     ------------------------------------------------------------------
    | This installer will create a volume for the nix store and        |
    | configure it to mount at /nix.  Follow these steps to uninstall. |
     ------------------------------------------------------------------

  1. Remove the entry from fstab using 'sudo vifs'
  2. Destroy the data volume using 'diskutil apfs deleteVolume'
  3. Remove the 'nix' line from /etc/synthetic.conf or the file
```


Meh, hit an error, giving up
