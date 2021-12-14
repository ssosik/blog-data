---
title: GPG Keys and OfflineIMAP
lead: ""
date: "2019-06-20T09:59:04-04:00"
tags:
  - gpg
  - vim
  - offlineimap
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Rotating a password stored in GPG


```sh
vi ~/.password-store/<store>.gpg
```

# Rotating an expired GPG Key

Error messages like:
```
gpg: Note: secret key 7230D8B62C5A7295 expired at Tue Dec  7 08:26:59 2021 EST
```

Followed this reference:
<https://danielpecos.com/2019/03/30/how-to-rotate-your-openpgp-gnupg-keys/>


Follow prompts and set password:
```bash
gpg --full-generate-key
```

Make this new password the default
```bash
gpg --edit-key A95D02EB8F5C51E135CF0E9796AE07FD46851D70
uid 1
primary
save
```
