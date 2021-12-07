---
title: NixOS Vultr setup
description: ""
lead: ""
date: "2020-05-15T16:47:10-04:00"
lastmod: "2020-05-15T16:47:10-04:00"
categories:
- nixos
- cli
tags:
  - nixos
  - vultr
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Ideas from:
- https://eipi.xyz/blog/nixos-on-vultr/
- https://www.vultr.com/docs/install-nixos-on-vultr


# How to create a snapshot to clone

Boot a new instance from the NixOS ISO under the ISO Library.

One the console, once available, install the OS
```bash
curl https://raw.githubusercontent.com/horkhork/nixos-home/master/vultr.sh | sudo bash
```

# Once the above is complete, remove the ISO and create a snapshot:

This should be done by selecting Settings > Custom ISO and Remove ISO on the web
interface, which restarts the server at the same time as unmounting the install
ISO.

Once the server is back up, test that you can log in as root on the console with
the password defined in vultr.sh

Add a Firewall group to allow SSH and attach it to the server

Update DNS to point to Instance IP

Set server hostname/label if desired

Log in as root on the console using the password defined in vultr.sh

# Bootstrap the NixOS configuration
```bash
curl https://raw.githubusercontent.com/horkhork/nixos-home/master/install-bootstrap.sh | bash -s -- mail.little-fluffy.cloud
```

Verify I can SSH in as steve now:
```bash
ssh steve@little-fluffy.cloud -oForwardAgent=yes -t tmux -2CC new-session -A -s main
```

# Complete the install to apply my configuration.nix
```bash
#curl https://raw.githubusercontent.com/horkhork/nixos-home/master/install.sh | bash
cd /etc/nixos
sudo bash install.sh
```

Follow <https://gitlab.com/simple-nixos-mailserver/nixos-mailserver/-/wikis/A-Complete-Setup-Guide>
to get simplemail setup and working
