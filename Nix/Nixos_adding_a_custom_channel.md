---
title: Nixos adding a custom channel
description: ""
lead: ""
date: "2020-04-23T12:50:36-04:00"
lastmod: "2020-04-23T12:50:36-04:00"
categories:
- nixos
- cli
tags:
  - nix
  - nixos
  - nixpkgs
  - dnscrypt-proxy2
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Following this writeup: <http://www.lpenz.org/articles/nixchannel/>
And related repo: <https://github.com/lpenz/nixpkgs-lpenz>


Nix docs on channels:
<https://nixos.wiki/wiki/Nix_channels>

Using Travis.ci to build the master branch and write the output into a
`gh-pages` branch.

Related Travis.ci docs:
- <https://docs.travis-ci.com/user/deployment/pages/#setting-the-github-token>
- <https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings>
- <https://docs.travis-ci.com/user/best-practices-security#recommendations-on-how-to-avoid-leaking-secrets-to-build-logs>

My build-page:
<https://travis-ci.com/github/horkhork/nixpkgs-ssosik>

Needed to create a Github Access token, and store it, along with the
`NIX_CACHE_PRIV_KEY` as environment variables as a Travis CI setting.

Github access tokens: <https://github.com/settings/tokens>
And notes on how to create/use one: <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line>

My Repo: <https://github.com/horkhork/nixpkgs-ssosik>
My Github Pages URL (should be just a blank page): <https://horkhork.github.io/nixpkgs-ssosik/>

With the `nixpkgs-ssosik` code committed to master branch and pushed up, and the
secrets stored as environment variables in Travis CI, Travis CI will build the
cache and store it in a separate branch on the repo. Once that is complete, I
can use the channel as:
```bash
# Add the channel on a per-user basis
nix-channel --add https://horkhork.github.io/nixpkgs-ssosik/
nix-channel --update # must do this to fetch the cache and store it locally
# Install my custom thing
nix-env -iA nixpkgs-ssosik.dnscrypt-proxy2-blacklist-updater

# And to remove it:
nix-env --uninstall nixpkgs-ssosik.dnscrypt-proxy2-blacklist-updater

# And double check it's not in the installed list
nix-env --query
```

Since the nixpkg is cached locally, making changes to the remote repo and
re--updating them will not work. Need to remove the repo, garbage collect,
re-add and re-update the repo:
```bash
nix-channel --remove nixpkgs-ssosik
nix-collect-garbage -d
... add ... update ... install
```

# Now, how to add the channel and then refer to the custom nixpkg in configuration.nix?

```bash
# Add the channel to the system-wide configuration
sudo nix-channel --add https://horkhork.github.io/nixpkgs-ssosik/
sudo nix-channel --update
# Ensure the channel is now available in NIX_PATH
nix-instantiate --eval -E '<nixpkgs-ssosik>'
╭─     ~/git/nixpkgs-ssosik    master ───────────────────────────────────────────────────────────────────── steve@cthulhu   13:06:53
╰─❯ ls /nix/var/nix/profiles/per-user/root/channels/
manifest.nix  nixos  nixpkgs-ssosik

sudo nixos-rebuild switch

# Need to fix bugs. Make change, push to master, check Travis CI build
sudo nix-channel --remove nixpkgs-ssosik
sudo nix-collect-garbage -d
```

Adding an import like `<nixpkgs>` is close to working. Need to sort out inputs.
Was hitting an error like:
```bash
error: The option `dnscrypt-proxy2-blacklist-updater' defined in `/nix/var/nix/profiles/per-user/root/channels/nixpkgs-ssosik' does not exist.
(use '--show-trace' to show detailed location information)
building Nix...
```

So there's a problem in the default.nix in `nixpkgs-ssosik`.

Doing an import like the following bypasses the error in `default.nix` but hits
another error
`<nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix>`
```bash
╭─     ~/git/nixpkgs-ssosik    master ───────────────────────────────────────────────────────────────────── steve@cthulhu   13:36:44
╰─❯ sudo nixos-rebuild switch
error: anonymous function at /home/steve/git/nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix:1:1 called with unexpected argument 'config', at /nix/var/nix/profiles/per-user/root/channels/nixos/lib/modules.nix:224:8
(use '--show-trace' to show detailed location information)
building Nix...
```

So, switching the import to a local path to debug and tweak:
`/home/steve/git/nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix`

Needed to fiddle with things.

Now, nix-build is failing:
```bash
╭─     ~/git/nixpkgs-ssosik    master ───────────────────────────────────────────────────────────────────────────────────────────────────   1m 50s steve@cthulhu   19:21:23
╰─❯ nix-build
error: cannot auto-call a function that has an argument without a default value ('config')
```

In order to get things to build in Travis CI, reference this
<https://docs.travis-ci.com/user/languages/nix/>

```yaml
(use '--show-trace' to show detailed location information)
diff --git a/.travis.yml b/.travis.yml
index a906f30..bb3df6d 100644
--- a/.travis.yml
+++ b/.travis.yml
@@ -8,7 +8,7 @@ jobs:
   include:
     - name: build
       language: nix
-      script: nix-build
+      script: nix-build -E 'with import <nixpkgs> {}; callPackage ./dnscrypt-proxy2-blacklist-updater.nix {}'
```

DEADEND

# Starting over again

Building upon the Travis CI setup stuff from <http://www.lpenz.org/articles/nixchannel/>
But following <https://blog.hackeriet.no/packaging-python-script-for-nixos/> for
details on the nix expressions

Test that the default.nix is good:
```bash
nix-instantiate --eval default.nix
```

Test that it builds
```bash
nix-build
```

# SUCCESS

Add this local import:
```
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      /home/steve/git/nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix
    ];
```

And the service is available:
```
  services.dnscrypt-proxy2-blacklist-updater.enable = true;
```

# Now, using the channel:

Push the repo to git and wait for Travis to build it

```bash
╭─     ~/git/nixpkgs-ssosik    master *3 ────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   21:39:12
╰─❯ sudo nix-channel --add https://horkhork.github.io/nixpkgs-ssosik/

╭─     ~/git/nixpkgs-ssosik    master *3 ────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   21:39:20
╰─❯ sudo nix-channel --update

unpacking channels...
created 2 symlinks in user environment

╭─     ~/git/nixpkgs-ssosik    master *3 ────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   21:39:23
╰─❯ sudo nixos-rebuild switch
```

And then update `configuration.nix`
```
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      <nixpkgs-ssosik/dnscrypt-proxy2-blacklist-updater.nix>
    ];
...
  services.dnscrypt-proxy2-blacklist-updater.enable = true;
```

switch again and it's installed
