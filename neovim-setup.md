---
title: Switching from MacVim to Neovim and Neovide
date: "2022-03-23T09:17:15-0400"
tags:
- vim
weight: 50
---

# Nvim links

https://nvim-awesome.vercel.app/

This looks neat: https://github.com/iamcco/markdown-preview.nvim

https://medium.com/geekculture/neovim-configuration-for-beginners-b2116dbbde84

https://vonheikemen.github.io/devlog/tools/configuring-neovim-using-lua/


# Neovide UI to Neovim

https://github.com/neovide/neovide

Install instructions: https://github.com/neovide/neovide#mac-from-source

Seems pretty cool so far, the only problem I have is that the UI Window doesn't
appear to be recognized by Amythest tiling window manager.

## Fix UI window

Use [cargo-bundle](https://github.com/burtonageo/cargo-bundle) to package the
Neovide binary so I can make it a Mac Application:
```bash
rustup update
cargo install cargo-bundle
cargo bundle --release
cp -r /Users/ssosik/workspace/neovide/target/release/bundle/osx/Neovide.app ~/Applications
open ~/Applications/Neovide.app
open ~/Applications/Neovide.app -- --args --frame ButtonLess
open ~/Applications/Neovide.app -- --args --frame ButtonLess --remote-tcp=localhost:6666
```



## Remote Nvim session

Connect to remote nvim over SSH tunnel

On remote machine:
`nvim --headless --listen localhost:6666 &`

Set up SSH Port Forwarding.

Instruct Neovide to connect to local tunneled port:
`./target/release/neovide --remote-tcp=localhost:6666`

Now I can open files and they seem local even though they are remote.
