---
title: Taskserver set up on NixOS 21.05
description: ""
lead: ""
date: "2021-10-13T10:39:43-04:00"
lastmod: "2021-10-13T10:39:43-04:00"
categories:
- home-network
- nixos
tags:
  - nixos
  - home-network
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Reference: [Taskserver NixOS Manual entry](https://nixos.org/manual/nixos/stable/index.html#module-taskserver)


# Initial Setup

Added to configuration.nix
```nix
     taskserver = {
       enable = true;
       fqdn = "mail.little-fluffy.cloud";
       listenHost = "::";
       organisations.little-fluffy-cloud.users = [ "steve" ];
     };
```

Followed by a `sudo nixos-rebuild switch --upgrade`

NOTE needed the `sudo` here for this to work correctly

```bash
sudo nixos-taskserver user export little-fluffy-cloud steve
```

To set the taskserver stuff from my mac via ssh
```bash
ssh -F /dev/null -i ~/.ssh/linode_rsa steve@mail.little-fluffy.cloud -p 64122 "sudo nixos-taskserver user export little-fluffy-cloud steve" | sh
```
Actually needed to run the above manually in pieces due to prompts, and then
manually tweak settings in ~/.taskrc
```
taskd.certificate=/Users/ssosik/.task/keys/public.cert
taskd.key=/Users/ssosik/.task/keys/private.key
taskd.ca=/Users/ssosik/.task/keys/ca.cert
taskd.credentials=little-fluffy-cloud/steve/8bbc8572-770c-4924-b9d9-069613351201
taskd.server=mail.little-fluffy.cloud:53589
```

NOTE don't forget to update the firewall on VULTR!!!!!

# Try to use LetsEncrypt certs

Links:
- [Write-up on using LetsEncrypt certs with TaskWarrior](https://mrwonko.de/blog/2017/using-letsencrypt-certificates-with-a-taskwarrior-server.html)
- [Another Write-up on setting TaskWarrior up with LetsEncrypt certs](https://gist.github.com/polettix/e8007a7f2064e7f133d93e060032a880)
- [Setting up a TaskWarrior server](https://blog.polettix.it/setup-a-taskwarrior-server/)
- [TaskWarrior FAQ](https://taskwarrior.org/support/faq.html)

Point server cert and key at the cert/key delivered for the hostname via ACME;
actually because of group permissions I needed to copy the certs:

cp /var/lib/acme/mail.little-fluffy.cloud/cert.pem /var/lib/taskserver/keys/server.cert
cp /var/lib/acme/mail.little-fluffy.cloud/key.pem /var/lib/taskserver/keys/server.key

ca.cert: these are the root Certificate Authorities accepted by the server. They
are used to verify the identity of the clients. Apparently the file can contain
multiple root certificates, but I only use one: The self-signed one whose
generation is described in the guide, created using pki/generate.ca.

╰─ nix-store -q $(nix-instantiate '<nixpkgs>' -A taskserver)
warning: you did not specify '--add-root'; the result might be removed by the garbage collector
/nix/store/ig3shc40c4ws3c2spx6hzg3r51v9if59-taskserver-1.1.0

/nix/store/ig3shc40c4ws3c2spx6hzg3r51v9if59-taskserver-1.1.0/bin/generate.ca

╰─ mkdir taskserver-lets-encrypt-dev
╰─ cd taskserver-lets-encrypt-dev
╰─ cp /nix/store/ig3shc40c4ws3c2spx6hzg3r51v9if59-taskserver-1.1.0/share/taskd/pki/vars .
╰─ /nix/store/ig3shc40c4ws3c2spx6hzg3r51v9if59-taskserver-1.1.0/bin/taskd-pki-generate.ca
╰─ sudo cp *.pem /var/lib/taskserver/keys/.


TaskServer service config tweaks:
```nix
    taskserver = {
      enable = true;
      debug = false;
      ipLog = false;
      fqdn = "mail.little-fluffy.cloud";
      listenHost = "mail.little-fluffy.cloud";
      organisations.Public.users = [ "steve" ];
      #config = {
      #  debug.tls = 3;
      #};
+      config = {
+        debug.tls = 3;
+      };
+      pki.manual = {
+        #server.cert = "/var/lib/acme/mail.little-fluffy.cloud/cert.pem";
+        #server.key = "/var/lib/acme/mail.little-fluffy.cloud/key.pem";
+        server.cert = "/var/lib/taskserver/keys/server.cert";
+        server.key = "/var/lib/taskserver/keys/server.key";
+        ca.cert = "/var/lib/taskserver/keys/ca.cert.pem";
+      };
    };
```

Restart the server and then make sure it's trusted
```bash
╰─   nix-shell -p gnutls

[nix-shell:~]$ gnutls-cli --print-cert -p 53589 mail.little-fluffy.cloud
```

Generate client certs
```bash
╰─ /nix/store/ig3shc40c4ws3c2spx6hzg3r51v9if59-taskserver-1.1.0/bin/taskd-pki-generate.client
And copy them into place
cp client.cert.pem .task/keys/public.cert
cp client.key.pem .task/keys/private.key

.task/keys/ca.cert is the root CA, copy it out of the last cert output from
gnutls-cli above
```

# Handle a rotation
The server cert provided via LetsEncrypt will expire periodically. Clients will
see errors like:

## Task CLI error with expired server cert
```bash
╰─ task sy
Syncing with mail.little-fluffy.cloud:53589

Handshake failed. The certificate is NOT trusted. The certificate chain uses expired certificate.
Sync failed.  Could not connect to the Taskserver.
```
## Foreground Android App error with expired server cert
```bash
Sync Failed
javax.net ssl.SSLHandshakeException:
java.security.cert.CertPathValidatorException: Trust anchor for certification
path not found.
```
## Use openssl to inspect the expiry on the server cert
```bash
nix-shell -p gnutls --command 'gnutls-cli --print-cert -p 53589 mail.little-fluffy.cloud'
...
- Certificate[0] info:
 - subject `CN=mail.little-fluffy.cloud', issuer `CN=R3,O=Let's Encrypt,C=US', serial 0x040f1d6b69104a448eecccf6123e4d6efacb, EC/ECDSA key 256 bits, signed using RSA-SHA256, activated `2021-12-12 06:12:58 UTC', expires `2022-03-12 06:12:57 UTC', pin-sha256="fDOvEHS6p64t92NIh6xCaMY4iUfq6RxBtkXAbkbmVMA="
...
```

## Rotate the server cert on the taskwarrior server
```bash
# Replace the expired Let's Encrypt server cert
sudo cp /var/lib/acme/mail.little-fluffy.cloud/cert.pem /var/lib/taskserver/keys/server.cert
sudo cp /var/lib/acme/mail.little-fluffy.cloud/key.pem /var/lib/taskserver/keys/server.key

cd /home/steve
mkdir -p taskserver-lets-encrypt-dev
cd taskserver-lets-encrypt-dev

TIMESTAMP=$(date --iso-8601)
STOREPATH=$(nix-store -q $(nix-instantiate '<nixpkgs>' -A taskserver))

# Create the TaskD PKI CA
cp $STOREPATH/share/taskd/pki/vars .
$STOREPATH/bin/taskd-pki-generate.ca

sudo cp ca.cert.pem /var/lib/taskserver/keys/ca.cert.pem.$TIMESTAMP
sudo cp ca.key.pem /var/lib/taskserver/keys/ca.key.pem.$TIMESTAMP
sudo unlink /var/lib/taskserver/keys/ca.cert.pem
sudo unlink /var/lib/taskserver/keys/ca.key.pem
sudo ln -s /var/lib/taskserver/keys/ca.cert.pem.$TIMESTAMP /var/lib/taskserver/keys/ca.cert.pem
sudo ln -s /var/lib/taskserver/keys/ca.key.pem.$TIMESTAMP /var/lib/taskserver/keys/ca.key.pem
sudo chown taskd:taskd /var/lib/taskserver/keys/ca.cert.pem.$TIMESTAMP
sudo chown taskd:taskd /var/lib/taskserver/keys/ca.key.pem.$TIMESTAMP
sudo chown -h taskd:taskd /var/lib/taskserver/keys/ca.cert.pem
sudo chown -h taskd:taskd /var/lib/taskserver/keys/ca.key.pem

sudo ls -latr /var/lib/taskserver/keys

sudo systemctl restart taskserver
sudo journalctl -fn200 -u taskserver
```

## At this point, the taskserver should be using the new cert, double check
```bash
# Ensure the cert is no longer expired
nix-shell -p gnutls --command 'gnutls-cli --print-cert -p 53589 mail.little-fluffy.cloud'
```

## Generate client certs
Now, we need to regenerate the client certs since these are issued from the
server cert.
```bash
$STOREPATH/bin/taskd-pki-generate.client

# On the taskserver itself, copy over the new client certs and verify they work
cp client.cert.pem $HOME/.task/keys/public.cert
cp client.key.pem $HOME/.task/keys/private.key

cd
# This is currently not working because the taskwarrior client on the
# taskserver isn't on the right version:
task sync
```

## Rotate client secrets

### On my mac, fetch the new taskserver client cert

```bash
scp mail.little-fluffy.cloud:.task/keys/public.cert .task/keys/.
scp mail.little-fluffy.cloud:.task/keys/private.key .task/keys/.

task sync
# Sync successful.  4 changes downloaded.
```
### On my Android phone, For Foreground app

Need to do the same on my phone in Foreground App. Connect using Android File
Transfer. Copy `ca.cert`, `public.cert`, and `private.key` to Documents folder
on the phone. Then open the Foreground App and re-select the CA, Public, and
Private certs used under Settings. Might need to disable and reenable sync.
