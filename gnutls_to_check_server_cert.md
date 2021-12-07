---
title: gnutls to check server cert
description: ""
lead: ""
date: "2021-10-28T16:14:16-04:00"
lastmod: "2021-10-28T16:14:16-04:00"
categories:
- cli
- cloud-deployment
tags:
  - tls
  - gnutls
  - little-fluffy.cloud
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
╰─ gnutls-cli -p 443 mail.little-fluffy.cloud
Processed 197 CA certificate(s).
Resolving 'mail.little-fluffy.cloud:443'...
Connecting to '173.199.118.68:443'...
- Certificate type: X.509
- Got a certificate list of 3 certificates.
- Certificate[0] info:
 - subject `CN=mail.little-fluffy.cloud', issuer `CN=R3,O=Let's Encrypt,C=US', serial 0x043afb0e3bcd5937832601e3671f95fd0a45, EC/ECDSA key 256 bits, signed using RSA-SHA256, activated `2021-10-13 12:51:15 UTC', expires `2022-01-11 12:51:14 UTC', pin-sha256="+JLC1VAZwksoVH3kFYbXSpHwhvKtR3K3P3JwgwqZ5kE="
	Public Key ID:
		sha1:7889fefb1677af7d2a7a1f354fef2e9608cea41e
		sha256:f892c2d55019c24b28547de41586d74a91f086f2ad4772b73f7270830a99e641
	Public Key PIN:
		pin-sha256:+JLC1VAZwksoVH3kFYbXSpHwhvKtR3K3P3JwgwqZ5kE=

- Certificate[1] info:
 - subject `CN=R3,O=Let's Encrypt,C=US', issuer `CN=ISRG Root X1,O=Internet Security Research Group,C=US', serial 0x00912b084acf0c18a753f6d62e25a75f5a, RSA key 2048 bits, signed using RSA-SHA256, activated `2020-09-04 00:00:00 UTC', expires `2025-09-15 16:00:00 UTC', pin-sha256="jQJTbIh0grw0/1TkHSumWb+Fs0Ggogr621gT3PvPKG0="
- Certificate[2] info:
 - subject `CN=ISRG Root X1,O=Internet Security Research Group,C=US', issuer `CN=DST Root CA X3,O=Digital Signature Trust Co.', serial 0x4001772137d4e942b8ee76aa3c640ab7, RSA key 4096 bits, signed using RSA-SHA256, activated `2021-01-20 19:14:03 UTC', expires `2024-09-30 18:14:03 UTC', pin-sha256="C5+lpZ7tcVwmwQIMcRtPbsQtWLABXhQzejna0wHFr8M="
- Status: The certificate is trusted.
- Description: (TLS1.3-X.509)-(ECDHE-SECP256R1)-(ECDSA-SECP256R1-SHA256)-(AES-256-GCM)
- Options: OCSP status request,
- Handshake was completed

- Simple Client Mode:

```
