---
title: NixOS dnscrypt-proxy2 automating blacklist updates with Cron
description: ""
lead: ""
date: "2020-04-19T14:28:02-04:00"
lastmod: "2020-04-19T14:28:02-04:00"
categories:
- nixos
- cli
tags:
  - nixos
  - dnscrypt-proxy
  - dnscrypt
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

Getting dnscrypt-proxy2 to run in Nixos was fairly straightforward and it
appears to work well.

For blacklisting and adblocking, I currently have a static blacklists file in
`/var/lib/private/dnscrypt-proxy2/dnscrypt-proxy-blacklist.txt`

It would be nice to automatically use the generate-domains-blacklist.py from
https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Public-blacklists to output the
blacklists file.

Manual blacklist generation
```bash
cd ~/git/dnscrypt-proxy/utils/generate-domains-blacklists
nix-shell '<nixpkgs>' -p python
[nix-shell:~/git/dnscrypt-proxy/utils/generate-domains-blacklists]$ ./generate-domains-blacklist.py -i > blacklist.txt
```

Which I then manually copy in place.

# How to use Cron
<https://nixos.wiki/wiki/Cron>

# How to create packages
<https://nixos.wiki/wiki/Nixpkgs/Create_and_debug_packages>
<https://nixos.wiki/wiki/Packaging/Tutorial>

# My fork of nixpkgs
<https://github.com/horkhork/nixpkgs>

## Working with the fork
```zsh
╭─     ~/git ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:26:10
╰─❯ git clone https://github.com/horkhork/nixpkgs.git
Cloning into 'nixpkgs'...
remote: Enumerating objects: 17, done.
remote: Counting objects: 100% (17/17), done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 1911223 (delta 7), reused 8 (delta 0), pack-reused 1911206
Receiving objects: 100% (1911223/1911223), 1.08 GiB | 9.16 MiB/s, done.
Resolving deltas: 100% (1306817/1306817), done.
Updating files: 100% (21514/21514), done.

╭─     ~/git ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────   4m 15s steve@cthulhu   14:30:30
╰─❯ cd nixpkgs

╭─     ~/git/nixpkgs    master ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:35:02
╰─❯ git remote add upstream https://github.com/NixOS/nixpkgs.git

╭─     ~/git/nixpkgs    master ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:35:03
╰─❯ git fetch upstream

╭─     ~/git/nixpkgs    master ──────────────────────────────────────────────────────────────────────────────────────────────────────────────   3s steve@cthulhu   14:35:24
╰─❯ git checkout -b upstream-master upstream/master
Branch 'upstream-master' set up to track remote branch 'master' from 'upstream'.
Switched to a new branch 'upstream-master'

╭─     ~/git/nixpkgs    upstream-master:master ──────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:35:26
╰─❯ git pull
Already up to date.

╭─     ~/git/nixpkgs    upstream-master:master ──────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:36:33
╰─❯ git checkout -b dnscrypt-proxy2-auto-blacklisting
```

### Starting to hack on dnscrypt-proxy2

```bash
╭─     ~/git/nixpkgs    upstream-master:master ──────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   14:45:32
╰─❯ find . -name '*dnscrypt*'
./pkgs/tools/networking/dnscrypt-proxy2
./pkgs/tools/networking/dnscrypt-wrapper
./nixos/tests/dnscrypt-proxy2.nix
./nixos/modules/services/networking/dnscrypt-wrapper.nix
./nixos/modules/services/networking/dnscrypt-proxy2.nix

nix-shell '<nixpkgs>' -A dnscrypt-proxy2

[nix-shell:~/git/nixpkgs]$ genericBuild
unpacking sources
unpacking source archive /nix/store/bfmzf7mq7vfncrg18s9s1zlmkdc7ijwi-source
source root is source
patching sources
configuring
mv: cannot stat 'source': No such file or directory
building
find: ‘github.com/jedisct1/dnscrypt-proxy’: No such file or directory
installing
post-installation fixup

... permissions errors ...

[nix-shell:/run/user/1000]$ ls

# directory is changed and it looks like it built some stuff

╭─     ~/git/nixpkgs    upstream-master:master ?1 ───────────────────────────────────────────────────────────────────────────────────────────   9s steve@cthulhu   14:51:34
╰─❯ ls /nix/store/bfmzf7mq7vfncrg18s9s1zlmkdc7ijwi-source
ChangeLog  dnscrypt-logo.svg  dnscrypt-proxy  go.mod  go.sum  LICENSE  logo.png  logo.svg  README.md  snapcraft.yaml  utils  vendor  windows
```

#### Cleaning the build
```bash
nix-collect-garbage -d

sudo nix-shell '<nixpkgs>' -A dnscrypt-proxy2
```

a `source` directory containing build artifacts might be lying around as well,
`rm -rf` that.

#### Exploring dev
In the nix-shell, the build process invokes a series of shell functions
```bash
# View the shell code for genericBuild
typeset -f genericBuild | less


unpackPhase
#unpacking source archive /nix/store/bfmzf7mq7vfncrg18s9s1zlmkdc7ijwi-source
#source root is source
```

#### Building locally-edited nixpkg
```bash
export NIXPKGS=$HOME/git/nixpkgs
# Build it
nix-build $NIXPKGS -A dnscrypt-proxy2
# Run environment to build it
nix-build $NIXPKGS --run-env -A dnscrypt-proxy2
```

Repl
```bash
nix repl -I $NIXPKGS
╭─     ~/git/dnscrypt-proxy-blup ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   15:32:08
╰─❯ nix repl -I $NIXPKGS
Welcome to Nix version 2.3.4. Type :? for help.

nix-repl> :l <nixpkgs>
Added 11489 variables.

nix-repl> "${pkgs.dnscrypt-proxy2}" # Tab completion works in here

nix-repl> "${pkgs.dnscrypt-proxy2}"
"/nix/store/jq6hcxkwj6i50d3aljjvg1xq0fp8n6sz-dnscrypt-proxy2-2.0.39-bin"

nix-repl>
```

##### Add pkgs/tools/networking/dnscrypt-proxy2-blacklist-updater/default.nix

Following <https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md>

created a default.nix for dnscrypt-proxy2-blacklist-updater using the `buildPythonApplication` function.

and added this line to `pkgs/top-level/all-packages.nix`:
```nix
dnscrypt-proxy2-blacklist-updater = callPackage ../tools/networking/dnscrypt-proxy2-blacklist-updater { };
```

This does something:
```bash
╭─     ~/git/nixpkgs    upstream-master:master ⇡1 ?1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── ✘ INT steve@cthulhu   08:54:49
╰─❯ export NIXPKGS=$HOME/git/nixpkgs

╭─     ~/git/nixpkgs    upstream-master:master ⇡1 ?1 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   08:55:32
╰─❯ nix-build $NIXPKGS --run-env -A dnscrypt-proxy2-blacklist-updater
these paths will be fetched (16.00 MiB download, 84.62 MiB unpacked):
  /nix/store/00iijl9s12z2qy8gjggdn72d3l3vipbi-python3.7-setuptools-45.2.0
  /nix/store/06d2850apsqa603cxngsrsxf8mra0v47-openssl-1.1.1f
  ...
Sourcing python-remove-tests-dir-hook
Sourcing python-catch-conflicts-hook.sh
Sourcing python-remove-bin-bytecode-hook.sh
Sourcing setuptools-build-hook
Using setuptoolsBuildPhase
Using setuptoolsShellHook
Sourcing pip-install-hook
Using pipInstallPhase
Sourcing python-imports-check-hook.sh
Using pythonImportsCheckPhase
Sourcing python-namespaces-hook
Sourcing setuptools-check-hook
Using setuptoolsCheckPhase
Executing setuptoolsShellHook
Finished executing setuptoolsShellHook

[nix-shell:~/git/nixpkgs]$
```

```bash
╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ?1 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   09:00:53
╰─❯ sudo rm -rf source

╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   09:00:56
╰─❯ nix-build $NIXPKGS --run-env -A dnscrypt-proxy2-blacklist-updater
Sourcing python-remove-tests-dir-hook
Sourcing python-catch-conflicts-hook.sh
Sourcing python-remove-bin-bytecode-hook.sh
Sourcing setuptools-build-hook
Using setuptoolsBuildPhase
Using setuptoolsShellHook
Sourcing pip-install-hook
Using pipInstallPhase
Sourcing python-imports-check-hook.sh
Using pythonImportsCheckPhase
Sourcing python-namespaces-hook
Sourcing setuptools-check-hook
Using setuptoolsCheckPhase
Executing setuptoolsShellHook
Finished executing setuptoolsShellHook

[nix-shell:~/git/nixpkgs]$ genericBuild
unpacking sources
unpacking source archive /nix/store/hjvi333p81f3dbv4zs8dnxmihzh5d1bf-source
source root is source
setting SOURCE_DATE_EPOCH to timestamp 315637200 of file source/windows/service-uninstall.bat
patching sources
configuring
no configure script, doing nothing
building
Executing setuptoolsBuildPhase
Traceback (most recent call last):
  File "nix_run_setup", line 8, in <module>
    exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\\r\\n', '\\n'), __file__, 'exec'))
  File "/nix/store/lm0w36273v76nnph1518gwbv1g45sl8w-python3-3.7.7/lib/python3.7/tokenize.py", line 447, in open
    buffer = _builtin_open(filename, 'rb')
FileNotFoundError: [Errno 2] No such file or directory: 'setup.py'
Finished executing setuptoolsBuildPhase
installing
Executing pipInstallPhase
mkdir: cannot create directory ‘/nix/store/k9djb7bg1wxrfs6l8yx86fcav88valc3-dnscrypt-proxy2-2.0.42’: Read-only file system
bash: pushd: dist: No such file or directory
post-installation fixup
find: ‘/nix/store/k9djb7bg1wxrfs6l8yx86fcav88valc3-dnscrypt-proxy2-2.0.42’: No such file or directory
strip is /nix/store/p1y0xl8dp4s1x1vvxxb5sn84wj6lsh8s-binutils-2.31.1/bin/strip
mkdir: cannot create directory ‘/nix/store/k9djb7bg1wxrfs6l8yx86fcav88valc3-dnscrypt-proxy2-2.0.42’: Read-only file system
bash: /nix/store/k9djb7bg1wxrfs6l8yx86fcav88valc3-dnscrypt-proxy2-2.0.42/nix-support/propagated-build-inputs: No such file or directory
Executing pythonRemoveTestsDir
Finished executing pythonRemoveTestsDir
running install tests
no Makefile or custom buildPhase, doing nothing
pythonCatchConflictsPhase
pythonRemoveBinBytecodePhase
pythonImportsCheckPhase
Executing pythonImportsCheckPhase
setuptoolsCheckPhase
Executing setuptoolsCheckPhase
Traceback (most recent call last):
  File "nix_run_setup", line 8, in <module>
    exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\\r\\n', '\\n'), __file__, 'exec'))
  File "/nix/store/lm0w36273v76nnph1518gwbv1g45sl8w-python3-3.7.7/lib/python3.7/tokenize.py", line 447, in open
    buffer = _builtin_open(filename, 'rb')
FileNotFoundError: [Errno 2] No such file or directory: 'setup.py'
Finished executing setuptoolsCheckPhase

[nix-shell:~/git/nixpkgs/source]$
```

`setuptoolsBuildPhase` and `setuptoolsCheckPhase` are failing because `setup.py`
isn't found. Examine these bash functions:

```bash
typeset -f setuptoolsBuildPhase | less

setuptoolsBuildPhase ()
{
    echo "Executing setuptoolsBuildPhase";
    local args;
    runHook preBuild;
    cp -f /nix/store/fscd8f71wmpwphcmi5mx8qnif2402x9m-run_setup.py nix_run_setup;
    args="";
    if [ -n "$setupPyGlobalFlags" ]; then
        args+="$setupPyGlobalFlags";
    fi;
    if [ -n "$setupPyBuildFlags" ]; then
        args+="build_ext $setupPyBuildFlags";
    fi;
    eval "/nix/store/lm0w36273v76nnph1518gwbv1g45sl8w-python3-3.7.7/bin/python3.7 nix_run_setup $args bdist_wheel";
    runHook postBuild;
    echo "Finished executing setuptoolsBuildPhase"
}
```

Dead end

#### Set setuptools.py to local checkout of dnscrypt-proxy2
cat ~/git/dnscrypt-proxy/utils/generate-domains-blacklists/setup.py
```python
# setup.py
from distutils.core import setup

setup(
    name='dnscrypt-proxy2-blacklist-updater',
    version='0.0.1',
    scripts=['generate-domains-blacklist.py',],
)

```
And update `src` field in default.nix to point to local path:
```
src = /home/steve/git/dnscrypt-proxy/utils/generate-domains-blacklists;
```

Build is successful!
```bash
╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   10:23:54
╰─❯ sudo rm -rf source ; nix-build $NIXPKGS -A dnscrypt-proxy2-blacklist-updater
/nix/store/zdljw6fgnzin51kxaahdk65j98wd4dkd-dnscrypt-proxy2-2.0.42

╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   10:23:56
╰─❯ ls /nix/store/zdljw6fgnzin51kxaahdk65j98wd4dkd-dnscrypt-proxy2-2.0.42
bin  lib  nix-support

╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   10:24:00
╰─❯ ls /nix/store/zdljw6fgnzin51kxaahdk65j98wd4dkd-dnscrypt-proxy2-2.0.42/bin
generate-domains-blacklist.py

```

##### Trying again with manual environment
```bash
╭─     ~/git/nixpkgs    upstream-master:master ⇡1 !1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── ✘ INT steve@cthulhu   10:24:43
╰─❯ sudo rm -rf source ; nix-build $NIXPKGS --run-env -A dnscrypt-proxy2-blacklist-updater
these paths will be fetched (47.62 MiB download, 209.09 MiB unpacked):
  /nix/store/00iijl9s12z2qy8gjggdn72d3l3vipbi-python3.7-setuptools-45.2.0
...

Executing setuptoolsShellHook
Finished executing setuptoolsShellHook

[nix-shell:~/git/nixpkgs]$ genericBuild
unpacking sources
unpacking source archive /nix/store/nm120cjp7r5m19cyav1d1971az1jwpcn-generate-domains-blacklists
source root is generate-domains-blacklists
setting SOURCE_DATE_EPOCH to timestamp 315637200 of file generate-domains-blacklists/setup.py
...

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
Finished executing setuptoolsCheckPhase

[nix-shell:~/git/nixpkgs/generate-domains-blacklists]$ ls
build  dist  dnscrypt_proxy2_blacklist_updater.egg-info  domains-blacklist-local-additions.txt  domains-blacklist.conf  domains-time-restricted.txt  domains-whitelist.txt  generate-domains-blacklist.py  nix_run_setup  out  setup.py

[nix-shell:~/git/nixpkgs/generate-domains-blacklists]$ ./generate-domains-blacklist.py
Loading data from [file:domains-blacklist-local-additions.txt]
Loading data from [https://mirror1.malwaredomains.com/files/justdomains]
Loading data from [https://www.malwaredomainlist.com/hostslist/hosts.txt]
Loading data from [https://easylist-downloads.adblockplus.org/antiadblockfilters.txt]
Loading data from [https://easylist-downloads.adblockplus.org/easylist_noelemhide.txt]
...

##### Install the package from local NIXPKGS
```bash
╭─     ~ ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── ✘ INT steve@cthulhu   10:36:34
╰─❯ echo $NIXPKGS
/home/steve/git/nixpkgs

╭─     ~ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── steve@cthulhu   10:36:39
╰─❯ sudo nixos-rebuild switch -I nixpkgs=$NIXPKGS
building Nix...
building the system configuration...
activating the configuration...
setting up /etc...
reloading user units for steve...
setting up tmpfiles

╭─     ~ ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────   15s steve@cthulhu   10:37:01
╰─❯
```
Update `/etx/nixos/configuration.nix`:
```
  services.cron = {
    enable = true;
    systemCronJobs = [
      "*/1 * * * *      root    date >> /tmp/cron.log"
      #"*/1 * * * *      root    . /etc/profile; ${pkgs.dnscrypt-proxy2}/utils/generate-domains-blacklists/generate-domains-blacklist.py > /tmp/blacklist.txt"
      "*/1 * * * *      root    . /etc/profile; ${pkgs.dnscrypt-proxy2-blacklist-updater}/generate-domains-blacklist.py > /tmp/blacklist.txt"
    ];
  };
```

Install it
```bash
sudo nixos-rebuild -I nixpkgs=$NIXPKGS switch
```

