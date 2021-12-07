---
title: meilisearch on nixos little-fluffy.cloud
description: ""
lead: ""
date: "2021-10-22T09:40:19-04:00"
lastmod: "2021-10-22T09:40:19-04:00"
categories:
- cli
- nixos
- cloud-deployment
- meilisearch
tags:
  - meilisearch
  - little-fluffy.cloud
  - vultr
  - nixos
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Get meiliesearch running on NixOS

- [Meilisearch guide on running meilisearch in a production environment](https://docs.meilisearch.com/create/how_to/running_production.html)
- [Nixos documentation (not much right now)](https://nixos.org/manual/nixos/unstable/index.html#module-services-meilisearch)
- [Nixos options](https://github.com/NixOS/nixpkgs/blob/nixos-unstable/nixos/modules/services/search/meilisearch.nix)

## Needed to upgrade to unstable

```bash
╰─ sudo nix-channel --add https://nixos.org/channels/nixos-unstable nixos

╰─ sudo nix-channel --list
nixos https://nixos.org/channels/nixos-unstable
nixpkgs-ssosik https://horkhork.github.io/nixpkgs-ssosik

╰─ sudo nix-channel --update
```

## Set the master key, NOTE this must have the 'MEILI_MASTER_KEY=' prefix
```bash
╰─ sudo vi /root/meili_master_key
MEILI_MASTER_KEY=XXXXXXXXX (in 1password)
```

*NOTE* The environment variable name in the master key line above

## Nixos configs to enable meilisearch

```bash
╰─ vi /etc/nixos/full-configuration-mail.nix
```
```nix
+     meilisearch = {
+       enable = true;
+       listenAddress = "127.0.0.1"; # Default, only listen on localhost
+       listenPort = 7700; # Default
+       environment = "production";
+       # File contains `MEILI_MASTER_KEY=XXXXXXXXX`, set permissions appropriately
+       masterKeyEnvironmentFile = "/root/meili_master_key";
+       noAnalytics = true; # Default
+     };
```
```bash
╰─ sudo nixos-rebuild switch --upgrade
```

Currently running Meilisearch 0.21.1

## Test the install

```bash
# Server is running
╰─ curl localhost:7700
{"status":"MeiliSearch is running"}

# Use the master key to 
╰─ curl -s localhost:7700/keys --header "X-Meili-API-Key: $(sudo cat /root/meili_master_key | cut -d= -f2)" | jq
{
  "private": "b1d63a569f07e1a22ae48a2f2....",
  "public": "d08fd475dc67bc6ce7c2d2017...."
}
```

Note that changing the master key regenerates the private and public keys. These
keys are used for API interactions: adding new items and querying the db.

## Notes about keys
- https://docs.meilisearch.com/reference/api/keys.html#get-keys
- https://docs.meilisearch.com/reference/features/authentication.html#communicating-with-a-protected-instance
- https://docs.meilisearch.com/reference/features/authentication.html#key-types

# Set up a reverse proxy

Links
- https://nixos.wiki/wiki/Nginx
- https://medium.com/@robin.raymond/websocket-proxys-with-nginx-and-the-beauty-of-nixos-e1b95dff1e04
- https://discourse.nixos.org/t/simple-reverse-proxy/11016
- https://toxicfrog.github.io/reverse-proxying-plex-with-nginx-on-nixos/

This was too easy!!!

```
+    nginx = {
+      enable = true;
+      recommendedGzipSettings = true;
+      recommendedOptimisation = true;
+      recommendedProxySettings = true;
+      recommendedTlsSettings = true;
+
+      # other Nginx options
+      virtualHosts."meilisearch.little-fluffy.cloud" =  {
+        enableACME = true;
+        forceSSL = true;
+        locations."/" = {
+          proxyPass = "http://127.0.0.1:7700";
+          proxyWebsockets = false;
+        };
+      };
+    };
```

Followed by a
```
╰─ sudo nixos-rebuild switch --upgrade
```

Since I already have vultr DNS pointing all requests for little-fluffy.cloud
this now just works. AND since we're matching on virtual hosts
`mail.little-fluffy.cloud` goes to Roundcube and
`meilisearch.little-fluffy.cloud` goes to meilisearch.

# Trying to upgrade Meilisearch is tricker.

## Use prefetch to get a git hash we don't have locally
```bash
nix-shell -p nix-prefetch-scripts
nix-prefetch-git https://github.com/meilisearch/MeiliSearch
Initialized empty Git repository in /run/user/1000/git-checkout-tmp-O7V1UwZh/MeiliSearch/.git/
remote: Enumerating objects: 154, done.
remote: Counting objects: 100% (154/154), done.
remote: Compressing objects: 100% (143/143), done.
remote: Total 154 (delta 12), reused 52 (delta 3), pack-reused 0
Receiving objects: 100% (154/154), 7.00 MiB | 19.92 MiB/s, done.
Resolving deltas: 100% (12/12), done.
From https://github.com/meilisearch/MeiliSearch
 * branch            HEAD       -> FETCH_HEAD
Switched to a new branch 'fetchgit'
removing `.git'...

git revision is 24eef577c52d97586f27a7bd699b79e5a0909c12
path is /nix/store/p8wjnipga0s9izqajlawvsflymj79s25-MeiliSearch
git human-readable version is -- none --
Commit date is 2021-10-19 09:32:27 +0000
hash is 0sfc5c3ys258pccrjrqhsva9xqxqxwddfphbsg7svnw14fb9k0mm
{
  "url": "https://github.com/meilisearch/MeiliSearch",
  "rev": "24eef577c52d97586f27a7bd699b79e5a0909c12",
  "date": "2021-10-19T09:32:27+00:00",
  "path": "/nix/store/p8wjnipga0s9izqajlawvsflymj79s25-MeiliSearch",
  "sha256": "0sfc5c3ys258pccrjrqhsva9xqxqxwddfphbsg7svnw14fb9k0mm",
  "fetchLFS": false,
  "fetchSubmodules": false,
  "deepClone": false,
  "leaveDotGit": false
}`
```


## How to import a local derivation
https://discourse.nixos.org/t/how-to-use-a-nix-derivation-from-a-local-folder/5498/3


## Trying to uplift existing:
https://github.com/NixOS/nixpkgs/tree/a0dbe47318bbab7559ffbfa7c4872a517833409f/pkgs/servers/search/meilisearch

Need to use crate2nix to update the generated Cargo.nix
```
╰─   nix-shell -p crate2nix
these paths will be fetched (1.48 MiB download, 6.47 MiB unpacked):
  /nix/store/x4sbsraq4rkdf6q6qf733bvxm72hwdsv-crate2nix-0.10.0
copying path '/nix/store/x4sbsraq4rkdf6q6qf733bvxm72hwdsv-crate2nix-0.10.0' from 'https://cache.nixos.org'...

[nix-shell:/etc/nixos]$ crate2nix
```

Need to checkout and build meilisearch-0.23.1 and then run crate2nix there

```
nix-shell -p cargo crate2nix
git clone https://github.com/meilisearch/MeiliSearch.git
cd MeiliSearch/
git checkout v0.23.1
cargo build
crate2nix generate
sudo cp crate-hashes.json Cargo.nix /etc/nixos
sudo cp -a meilisearch-lib/ /etc/nixos
```


Took a long time to build but didn't do the right thing, need to update the
service.

https://nixos.wiki/wiki/NixOS:extend_NixOS


