---
title: Build xapian-query-cli xq in a vanilla ubuntu docker container
description: ""
lead: ""
date: "2021-08-10T09:17:23-04:00"
lastmod: "2021-08-10T09:17:23-04:00"
tags:
  - docker
  - cli
  - xq
  - rust
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
# Start bash in the container
sudo docker run -ti ubuntu /bin/bash

# fetch dependencies, source, and build it
apt-get update  --yes
apt-get upgrade  --yes
apt-get install  --yes aptitude git make tar xz-utils vim g++ curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
rustup install stable
git clone --recurse-submodules https://github.com/ssosik/xapian-query-cli.git
cd xapian-query-cli
make
```
