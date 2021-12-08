---
title: Notmuch Tricks
description: ""
lead: ""
date: "2021-12-08T14:47:54-0500"
tags:
  - notmuch
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Run queries to build a Notmuch tree similar to what is in Emacs

```bash
# Message IDs that match the query
notmuch search --format=json --output=summary "date:today" | jq -r '.[] | .query[0]'

# Message IDs that are part of threads with messages that match the query
  (display as greyed out)
notmuch search --format=json --output=summary "date:today" | jq -r '.[] | .query[1]'
```

Dump all messages matching one of the above queries
```bash
notmuch show --format=json $(notmuch search --format=json --output=summary "date:today" | jq -r '.[] | .query[0]') | jq . | less
```

# Build Notmuch with Ruby support to get vim-notmuch working
Following: https://github.com/Homebrew/homebrew-core/issues/30019

```bash
brew install -g --build-from-source notmuch
```

Brew didn't work, so installing notmuch from source
Install zlib
Since this is the only library blocking, go to https://www.zlib.net and download source code. Select the "US (zlib.net)" hyperlink about halfway down the page for the tar.xz version.

Then find the download on your local machine and double click on the file. This will unzip the download and create a new folder in the same directly.

Then in Terminal:

cd into the directory with the download then tar -xvf zlib-1.2.11.tar.xz (Note that zlib-1.2.11.tar.xz may change depending on the latest version you've downloaded. Just run whatever file you're just downloaded.) Change directories cd zlib-1.2.11 ./configure make make install
