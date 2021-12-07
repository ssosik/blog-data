---
title: Bash Tricks
description: ""
lead: ""
date: "2019-03-21T14:51:11-04:00"
lastmod: "2019-03-21T14:51:11-04:00"
categories:
  - cli
tags:
  - bash
  - cli
draft: false
weight: 50
images: []
contributors:
  - steve
---

# Strict Mode

Set this at the top of a bash script for saner behavior when expected things
aren't set properly

```sh
#!/bin/bash
set -euo pipefail
```

From <http://redsymbol.net/articles/unofficial-bash-strict-mode/>

immediately exit if any command has a non-zero exit status

a reference to any variable you haven't previously defined - with the
exceptions of $* and $@ - is an error

If any command in a pipeline fails, that return code will be used as
the return code of the whole pipeline

# OpenSSL

## openssl one-liner to create self-signed cert

From: <https://stackoverflow.com/a/10176685>

```bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650
openssl req -nodes -newkey rsa:2048 -keyout example.key -out example.csr -subj "/C=US/ST=Connecticut/L=Granby/O=ORG/OU=Platform/CN=foo.com"
```

## use openssl to split pem into private key

Convert pem to cert

From: <https://serverfault.com/questions/391396/how-to-split-a-pem-file>

Read in a pem and pull out just the parts
```sh
# private key
openssl pkey -in edgemon-client.pem -out edgemon-client.key

# cert + chain
openssl crl2pkcs7 -nocrl -certfile edgemon-client.pem | openssl pkcs7 -print_certs -out edgemon-client.crt
```

## Split concatenated SSL PEM cert into individual certs

From <https://serverfault.com/questions/391396/how-to-split-a-pem-file/765943#765943>

```bash
csplit -n1 -z -f part-  edgemon-client.crt '/-----BEGIN CERTIFICATE-----/' '{*}'
```

As a piped command
```bash
vault read platform-ca/cert/ca_chain -format=json | jq -r '.data.certificate' | csplit -n1 -z -f crtpart -  '/-----BEGIN CERTIFICATE-----/' '{*}'
for PART in $(ls crtpart*) ; do openssl x509 -noout -text -in $PART ; rm $PART ; done
```

# find files written in the past 24 hours

```bash
find . -type f -amin +1 -amin -1440 | xargs zless
```

# find broken symlinks

```bash
find . -xtype l
```

# grep multiline

From <https://stackoverflow.com/questions/3717772/regex-grep-for-multi-line-search-needed>

`(?s)` enables `.` characters to match newline characters

-P activate perl-regexp for grep (a powerful extension of regular expressions)

-z suppress newline at the end of line, subtituting it for null character. That is, grep knows where end of line is, but sees the input as one big line.

-o print only matching. Because we're using -z, the whole file is like a single big line, so if there is a match, the entire file would be printed; this way it won't do that.

In regexp:

(?s) activate PCRE_DOTALL, which means that . finds any character or newline

```bash
grep -Pzo -- "(?s)(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)"
grep -Pzo -- "(?s)-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----"
```

# Use linux find to find files under matching subdirectory nested find

Find files under matching subdirectory, across symlinks, and limiting maxdepth
to avoid filesystem loops

```sh
find -L /path/ -maxdepth 3 -type d -name '<file name pattern>*' \
    -exec find -L '{}' -maxdepth 4 -type f -name "ssl_cert.certificate" \;
```

# Using fzf

## Interactively select git branch
```sh
git checkout $(git branch | fzf-tmux -d 15)
```

## Open files in vim
```vim
:Files <optional path root to start>
```

## Open git-controlled files in vim
```vim
:GFiles <optional path root to start>

# Or untracked files
:GFiles? <optional path root to start>
```

## Vim buffer completion
```vim
:Buffers
```

## Vim lines matching in open buffers
```vim
:Lines
```

# Advanced tar usage

## List contents of a compressed tarball
```bash
tar -ztf file.tgz
```

## Extract a single file from the compressed tarball
```bash
tar -zvf file.tgz --get ./run-telegraf
```

## Extract a single file from a tarball and put it into another location
```bash
tar -zvf file.tgz -C $HOME/.terraform.d/plugins/ --get ./terraform-provider-vault
```

## Grep the contents of a single file from a compressed tarball
```bash
tar -zvf file.tgz --get ./run-telegraf --to-command=strings | grep PATTERN
```

# Creating iterm vim screen recordings

Install <https://asciinema.org/>
```sh
brew install asciinema
asciinema rec -i 2.5 -t "Using Vim to execute Vault Commands" vim-vault.cast
```

Use <https://github.com/asciinema/asciicast2gif> to convert to gif
```sh
docker pull asciinema/asciicast2gif
docker run --rm -v $PWD:/data asciinema/asciicast2gif -t solarized-dark vim-vault.cast vim-vault.gif
```

# Shell script to move each markdown note into it's own directory

```sh
#cat move.sh

#!/bin/bash
set -euo pipefail

for F in $(find . -type f -name '*.md' | sort) ; do
    echo -n "$F "
    T=$(basename -s .md $F)
    D=$(date --date="$(echo $T | tr '_' ' ')" --iso=seconds)
    mkdir $D
    git mv $F $D/index.md
    echo $T
done
```

# 'timeout' CLI tool to run a command for a set amount of time

Use `timeout` to run a command for set amount of time. I'm using it to
temporarily swap out a running service for a spoofed service to see how
this disruption effects a consumer of this service:

    while true ; do
       sleep $(echo "$RANDOM / 1000" | bc)
       date
       <stop real service>
       timeout 60 <spoof service binary>
       <restart real service>
    done

I can let this test bake for a long time, then come back later and
scrape the logs to verify the consumer of this service handled the
errors correctly.

# Command-line to iterate over filenames containing spaces

Command line tools are pretty powerful, but there are some edge cases
that take some extra care. For example, using a `for` loop over a set of
files can be really useful, but if those filenames contain a space then
things may not work as expected.

So here's a quick recipe to work around this problem.

What would normally be something like:

``` {.bash}
for F in $(find . -type f -name "*.wiki") ; do
    <do stuff>
done
```

This falls down when the filenames contain one or more spaces, since the
for-loop iterates on whitespace-delimited tokens in the list.

Instead, do something like this:

``` {.bash}
while read F ; do
    <do stuff>
done < <(find . -type f -name '*.wiki')
```

# Complex one-liner to read lines from a JSON file, parse it, and scrape the results

```sh
while read LINE ; do
    echo $LINE | python -mjson.tool
done <<EOF 2>&1 | sed -n 's/"object": "\(.*\)",/\1/p' | sort | uniq -c > outfile
$(grep PATTERN FILE | sed "s/send: b'\(.*\)'/\1/")
EOF
```

# linux find exclude directory

Find files matching pattern but exclude the `vroots` directory
```bash
find . -path ./vroots -prune -o -type f -name '*.swp' -print
#      ^^^^^^^^^^^^^^^^^^^^^^^^
```

# HTTP Post using netcat

Not sure if this will work, here are scratch notes
```sh
# Get the liveness endpoint within the app container
cat <<EOF | nc 127.0.0.1 80
GET /v1/sys/health HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost
Accept: */*

EOF

# login via netcat within the app container
cat <<EOF | nc 127.0.0.1 80
POST /v1/auth/vkms_proxy_auth/login HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost
Accept: */*
X-Ssl-Client-Auth-Cn: foo
Content-Length: 41
Content-Type: application/json

{"method": "cert", "name": "mpulse-user"}

EOF

# This does not work, the newlines are probably not correct
cat <<EOF | openssl s_client -CAfile ~/.certs/nss1-canonical_ca_roots.pem -cert ~/.certs/ssosik-testnet.crt -key ~/.certs/ssosik-testnet.key vkms0-ssosik.default.abattery.appbattery.nss1.tn.akamai.com:443
POST /v1/auth/vkms_proxy_auth/login HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost
Accept: */*
X-Ssl-Client-Auth-Cn: foo
Content-Length: 41
Content-Type: application/json

{"method": "cert", "name": "mpulse-user"}

EOF

# This works - Using openssl s_client to make an HTTP POST request
echo -e 'POST /v1/auth/vkms_proxy_auth/login HTTP/1.1\r\nHost: vkms0-ssosik.default.abattery.appbattery.nss1.tn.akamai.com\r\nUser-Agent: curl/7.58.0\r\nAccept: */*\r\nContent-Length: 41\r\nContent-Type: application/json\r\n\r\n{"method": "cert", "name": "mpulse-user"}\r\n\r\n' | openssl s_client -quiet -CAfile ~/.certs/nss1-canonical_ca_roots.pem -cert ~/.certs/ssosik-testnet.crt -key ~/.certs/ssosik-testnet.key -connect vkms0-ssosik.default.abattery.appbattery.nss1.tn.akamai.com:443
```

# How to assign a heredoc to a variable

From: <https://stackoverflow.com/questions/1167746/how-to-assign-a-heredoc-value-to-a-variable-in-bash>
```sh
read -r -d '' VAR <<'EOF'
abc'asdf"
$(dont-execute-this)
foo"bar"''
EOF
```

# How to grep matching curly braces

From <https://unix.stackexchange.com/questions/147662/grep-upto-matching-brackets>
```
╰─ grep -zPo "ring0_id_namespaces = (\{([^{}]++|(?1))*\})" ../env.tfvars | grep -zPo "\"$APPNAME\" = (\{([^{}]++|(?1))*\})"
"vault-foo" = {
    "admins"           = ["aaa", "bbb"]
    "id_namespaces"    = ["aaa", "bbb"]
    "platform_ca_host" = "<hostname>"
  }
```

# Run Strace on a running process and see what it's blocked on

```sh
strace -fff -p 24056
```

# Network throughput test

    # On one host
    nc -l 12345 -k  # Set up netcat to listen on a TCP port

    # On another host
    pv -i0.5 -r /dev/zero | nc $IP 12345  # use netcat and pv to test throughput

# Bash function to get memory usage of a process name

        vsize() {
            ps -eo vsize,pid,euser,args:100 --sort %mem | grep -v grep | grep -i $@ | awk '{printf $1/1024 "MB"; $1=""; print }'
        }

        rss()
        {
            ps -eo rss,pid,euser,args:100 --sort %mem | grep -v grep | grep -i $@ | awk '{printf $1/1024 "MB"; $1=""; print }'
        }

## Sum memory usage of a process

        mem apache2 | tr -d 'MB' | awk '{print $1}' | paste -s -d + -  | bc
        1679.426106

## Look at random pages from a core dump for anything interesting to indicate a memory leak:

        $CORE=...
        off=$(($RANDOM % ($(stat -c "%s" $CORE)/4096)))
        $ dd if=$CORE bs=4096 skip=$off count=1 | xxd
        via my friend's blog at https://blog.nelhage.com/2013/03/tracking-an-eventmachine-leak/

        CORE=~/core.11301
        off=$(($RANDOM % ($(stat -c "%s" $CORE)/4096))) ; dd if=$CORE  bs=4096 skip=$off count=1 | xxd | less

# Quick tangent: how to check which process is listening on a port

From
https://debian-administration.org/article/184/How\_to\_find\_out\_which\_process\_is\_listening\_upon\_a\_port

`lsof -i :80`
