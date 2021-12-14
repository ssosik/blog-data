---
title: How to use distinct SSH keys for clones of github repos
description: ""
lead: ""
date: "2021-08-09T08:54:15-04:00"
lastmod: "2021-08-09T08:54:15-04:00"
tags:
  - git
  - github
  - ssh
  - cli
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Following the hint here:
https://gist.github.com/jexchan/2351996

Add a dedicated ssh key and upload it to https://github.com/settings/keys
```
ssh-keygen -t rsa -b 2048 -C "ssosik github" -f ~/.ssh/ssosik-github
```

Update ~/.ssh/config for a specific github entry for this key
```
Host github.com-ssosik
	HostName github.com
	User git
	IdentityFile ~/.ssh/ssosik-github
```

Then in the local clone for the repo update the config to refer to this SSH
config entry:
```
git config user.name steve
git config user.email "steve@little-fluffy.cloud"
git config remote.origin.url "git@github.com-ssosik:ssosik/xapian-query-cli.git"
```

