---
title: systemd how to get path to service file
description: ""
lead: ""
date: "2021-10-22T09:47:02-04:00"
lastmod: "2021-10-22T09:47:02-04:00"
categories:
- cli
- meilisearch
tags:
  - systemd
  - linux
  - meilisearch
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
╰─ systemctl show -p FragmentPath  meilisearch.service
FragmentPath=/etc/systemd/system/meilisearch.service

╰─ cat /etc/systemd/system/meilisearch.service
[Unit]
After=network.target
Description=MeiliSearch daemon

[Service]
Environment="LOCALE_ARCHIVE=/nix/store/ccxz84hrxlvrmwy1sw7klzg90q5v9k1w-glibc-locales-2.33-50/lib/locale/locale-archive"
Environment="MEILI_DB_PATH=/var/lib/meilisearch"
Environment="MEILI_DUMPS_DIR=/var/lib/meilisearch/dumps"
Environment="MEILI_ENV=production"
Environment="MEILI_HTTP_ADDR=127.0.0.1:7700"
Environment="MEILI_LOG_LEVEL=INFO"
Environment="MEILI_MAX_INDEX_SIZE=107374182400"
Environment="MEILI_NO_ANALYTICS=1"
Environment="PATH=/nix/store/xyn0240zrpprnspg3n0fi8c8aw5bq0mr-coreutils-8.32/bin:/nix/store/1nq62klcc9n2jv2ixaf77makkzdcghrh-findutils-4.8.0/bin:/nix/store/xxgddhdi57bbgd1yxza44plq6krjmiz1-gnugrep-3.6/bin:/nix/store/dy4ylp9439la4lq35ah2mj80fi87pk4w-gnused-4.8/bin:/nix/store/27855idyr8dkmh0xrzg7jln7a3fa7viy-systemd-249.4/bin:/nix/store/xyn0240zrpprnspg3n0fi8c8aw5bq0mr-coreutils-8.32/sbin:/nix/store/1nq62klcc9n2jv2ixaf77makkzdcghrh-findutils-4.8.0/sbin:/nix/store/xxgddhdi57bbgd1yxza44plq6krjmiz1-gnugrep-3.6/sbin:/nix/store/dy4ylp9439la4lq35ah2mj80fi87pk4w-gnused-4.8/sbin:/nix/store/27855idyr8dkmh0xrzg7jln7a3fa7viy-systemd-249.4/sbin"
Environment="TZDIR=/nix/store/x629s2442r2qfa3834rl4iqrai24fym6-tzdata-2021a/share/zoneinfo"

DynamicUser=true
EnvironmentFile=/root/meili_master_key
ExecStart=/nix/store/49212v5ckk1fr8fyvxgya8vdqgdj5qbz-meilisearch-0.21.1/bin/meilisearch
StateDirectory=meilisearch
```
