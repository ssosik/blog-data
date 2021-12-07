---
title: rsync.net and borg setup
description: ""
lead: ""
date: "2021-10-20T14:21:43-04:00"
lastmod: "2021-10-20T14:21:43-04:00"
categories:
- home-network
- nixos
tags:
  - borg
  - rsync
  - home-network
  - nixos
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Links
- [Generate SSH Keys for Rsync.net](https://www.rsync.net/resources/howto/ssh_keys.html)
- [BorgBackup NixOS docs](https://nixos.wiki/wiki/Borg_backup)
- [Example BorgBackup NixOS config](https://github.com/Xe/nixos-configs/blob/master/common/services/backup.nix)
- [Remote Commands Over SSH](https://www.rsync.net/resources/howto/remote_commands.html)

# Create key
```bash
ssh-keygen -t ed25519 -b 4096 -f .ssh/rsync.net
```

# Update local .ssh/config
```bash
Host de1576.rsync.net rsync.net
  ForwardAgent no
  User de1576
  PubkeyAuthentication yes
  IdentityFile ~/.ssh/rsync.net
```

# Test password-based log in
```bash
ssh de1576@de1576.rsync.net ls
```

# Push the ssh key fingerprint
```bash
scp .ssh/rsync.net.pub de1576@de1576.rsync.net:.ssh/authorized_keys
```

# Make the backup directories
```bash
ssh de1576@de1576.rsync.net mkdir mail.little-fluffy.cloud
ssh de1576@de1576.rsync.net mkdir mail.little-fluffy.cloud/mail
ssh de1576@de1576.rsync.net mkdir mail.little-fluffy.cloud/nixos
ssh de1576@de1576.rsync.net mkdir mail.little-fluffy.cloud/taskserver
```

# Change the password

```bash
ssh -t de1576@de1576.rsync.net passwd
```

# Nix config

```nix
   services = {
+     borgbackup.jobs = {
+       mailBackup = {
+         paths = [ "/var/vmail" "/var/dkim" ];
+         doInit = true;
+         repo = "de1576@de1576.rsync.net:mail.little-fluffy.cloud/mail";
+         encryption.mode = "none";
+         environment.BORG_RSH = "ssh -i /root/.ssh/rsync.net";
+         compression = "auto,lzma";
+         startAt = "daily";
+         extraArgs = "--remote-path=borg1";
+       };
+       etcNixos = {
+         paths = [ "/etc/nixos" ];
+         doInit = true;
+         repo = "de1576@de1576.rsync.net:mail.little-fluffy.cloud/nixos";
+         encryption.mode = "none";
+         environment.BORG_RSH = "ssh -i /root/.ssh/rsync.net";
+         compression = "auto,lzma";
+         startAt = "weekly";
+         extraArgs = "--remote-path=borg1";
+       };
+       taskServer = {
+         paths = [ "/var/lib/taskserver" ];
+         doInit = true;
+         repo = "de1576@de1576.rsync.net:mail.little-fluffy.cloud/taskserver";
+         encryption.mode = "none";
+         environment.BORG_RSH = "ssh -i /root/.ssh/rsync.net";
+         compression = "auto,lzma";
+         startAt = "daily";
+         extraArgs = "--remote-path=borg1";
+       };
+     };
```

# Copy ssh keys to root location
```bash
sudo cp .ssh/rsync.net* /root/.ssh/.
```

*NOTE*: I needed to add remote server key to known_hosts
