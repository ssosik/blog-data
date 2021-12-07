---
title: Nixos bootstrapping
description: ""
lead: ""
date: "2020-04-26T13:45:02-04:00"
lastmod: "2020-04-26T13:45:02-04:00"
categories:
- nixos
- cli
tags:
  - nixos
  - nix
  - home-network
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Now that I've played around with Nixos, let's try reinstalling everything to see
if I can pull in my configs and channel from Git.

# Follow Boot From USB

<https://nixos.org/nixos/manual/index.html#sec-booting-from-usb>

Boot from the stick and get networking working.
```bash
ip a
```

<https://nixos.org/nixos/manual/index.html#sec-installation-booting>

## Enable ssh and set root passwd
```bash
sudo systemctl start sshd
sudo su root
passwd
```

Follow UEFI partitioning

<https://nixos.org/nixos/manual/index.html#sec-installation-partitioning-UEFI>

```bash
parted /dev/sda -- mklabel gpt
parted /dev/sda -- mkpart primary 512MiB -8GiB
parted /dev/sda -- mkpart primary linux-swap -8GiB 100%
parted /dev/sda -- mkpart ESP fat32 1MiB 512MiB
parted /dev/sda -- set 3 boot on

parted /dev/sda -- print
# Model: ATA TS64GMTS400S (scsi)
# Disk /dev/sda: 64.0GB
# Sector size (logical/physical): 512B/512B
# Partition Table: gpt
# Disk Flags:
# 
# Number  Start   End     Size    File system     Name     Flags
#  3      1049kB  537MB   536MB   fat32           ESP      boot, esp
#  1      537MB   55.4GB  54.9GB  ext4            primary
#  2      55.4GB  64.0GB  8590MB  linux-swap(v1)  primary  swap
```

Partition Formatting

<https://nixos.org/nixos/manual/index.html#sec-installation-partitioning-formatting>

```bash
mkfs.ext4 -L nixos /dev/sda1
mkswap -L swap /dev/sda2
mkfs.fat -F 32 -n boot /dev/sda3
```

Start the install

<https://nixos.org/nixos/manual/index.html#sec-installation-installing>


```bash
mount /dev/disk/by-label/nixos /mnt

mkdir -p /mnt/boot
mount /dev/disk/by-label/boot /mnt/boot

swapon /dev/sda2

```

Run nixos-generate-config

```bash
nixos-generate-config --root /mnt

vi /mnt/etc/nixos/configuration.nix
# Make these tweaks:
#  environment.systemPackages = with pkgs; [
#    wget vim git
#  ];
#  services.openssh.enable = true;
#  services.openssh.permitRootLogin = "yes";
#  services.openssh.passwordAuthentication = true;
```

# Run the install
```bash
nixos-install
```

# Boot into the fresh OS
reboot and remove USB stick

# Update the system
nixos-rebuild switch --upgrade


# Swap in my configuration.nix WITHOUT home-manager enabled
Install git and pull down my committed configs:
```bash
# Add my channel and update it
nix-channel --add https://horkhork.github.io/nixpkgs-ssosik/
nix-channel --update

cd /etc
mv nixos nixos.install

git clone https://github.com/horkhork/nixos-home.git nixos
cp nixos.install/hardware-configuration.nix nixos/.
cd nixos

# Write hostname.nix
#{...}:
#
#{
#  networking.hostName = "scooby.little-fluffy.cloud";
#}

# Make any other tweaks to the configs. Temporarily comment out
# dnscrypt-proxy-blacklist-updater

# Build everything -j1 to limit parallel workers to avoid a hang/race
nixos-rebuild build --show-trace -vvv -j 1

# Stub out the dnscrypt proxy blacklist file
touch /var/lib/dnscrypt-proxy2/dnscrypt-proxy-blacklist.txt
mkdir /nix/var/nix/profiles/per-user/steve  # Why is this needed?

# Still seeing a hang, temporarily comment out home-manager in configuration.nix

# Switch
nixos-rebuild switch --show-trace -vvv -j 1

# uncomment home-manager
nixos-rebuild switch --upgrade
```

TODO rename `nixos-home` git repo to something slightly more indicative of being
system nixos configs. `nix-cfgs`

~TODO update dnscrypt-proxy2-blacklist-updater to write the blacklist.txt file
immediately if it doesn't exist, to make dnscrypt-proxy happy.~

TODO update configuration.nix to import dnscrypt-proxy2-blacklist-updater
similar to how it's being done for home-manager

~TODO systemd hook to restart dnscrypt-proxy2 when
dnscrypt-proxy-blacklist-updater is enabled~
