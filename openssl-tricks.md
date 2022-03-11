---
title: OpenSSL tricks
date: "2022-03-11T12:58:21-0500"
tags:
  - cli
  - openssl
draft: false
weight: 50
images: []
---

# Convert p12 into client cert and private key

```bash
PASS=1234
openssl pkcs12 -in incert.p12 -passin pass:$PASS -out out.crt
openssl pkcs12 -in incert.p12 -passin pass:$PASS -out out.key -nocerts -clcerts -passout pass: -nodes
```
