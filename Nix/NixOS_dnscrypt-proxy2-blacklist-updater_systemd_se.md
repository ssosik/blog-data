---
title: NixOS dnscrypt-proxy2-blacklist-updater systemd service periodic task work
description: ""
lead: ""
date: "2020-05-07T20:29:00-04:00"
lastmod: "2020-05-07T20:29:00-04:00"
categories:
- nixos
- cli
- home-network
tags:
  - nixos
  - dnscrypt
  - home-network
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Following:
- https://www.freedesktop.org/software/systemd/man/systemd.timer.html
- https://nixos.wiki/wiki/Nix_Cookbook
- https://www.reddit.com/r/NixOS/comments/4gj8bc/how_to_writing_a_systemd_service/
- https://wiki.archlinux.org/index.php/Systemd/Timers
- https://nixos.wiki/wiki/NixOS:extend_NixOS
- https://nixos.org/nixos/options.html#systemd
- https://www.reddit.com/r/NixOS/comments/8xfbfn/invoke_script_as_systemd_service/

Temporarily updated configuration.nix to point to local branch:
```nix
        # My custom packages
~       #<nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix>
+       /home/steve/workspace/nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix
```

Updated dnscrypt-proxy2-blacklist-updater.nix

Commands
```bash
sudo nixos-rebuild switch

systemctl status dnscrypt-proxy2-blacklist-updater.service

systemctl list-timers
systemctl list-timers --all

# Wipe persistent state
systemctl clean --what=state …

systemctl status dnscrypt-proxy2.service
```

Looking good, commit abc6e0b1a2f94bcbc3860c7f01f6935963d91c27 on https://github.com/horkhork/nixpkgs-ssosik.git

Git push, then check Travis: https://travis-ci.com/github/horkhork/nixpkgs-ssosik

Don't forget to update the channel!
`sudo nix-channel --update`

Revert configuration.nix and switch again:
`sudo nixos-rebuild switch`
