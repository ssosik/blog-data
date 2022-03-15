---
title: Vim tricks and Notes
description: ""
lead: ""
date: "2019-05-06T14:12:23-04:00"
lastmod: "2019-05-06T14:12:23-04:00"
categories:
  - vim
tags:
  - vim
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Vim-Python interface documentation

I always have trouble googling this, so saving it here:
`http://vimdoc.sourceforge.net/htmldoc/if_pyth.html`

`:help if_pyth.txt` provides the same info

# Opening files

## MacVim open file from command line in existing window

```bash
mvim --remote <filename>
```

## Vim edit remote file

From: <https://vim.fandom.com/wiki/Editing_remote_files_via_scp_in_vim>

`:e scp://remoteuser@server.tld//absolute/path/to/document`

```bash
scp://<username>@<host>/<relative path> or scp://<username>@<host>//<absolute path>
scp://ssosik@72.246.96.12/kmi-760-script-dev.py
```

## macvim open tmp file in already open window

To p4 print a file locally and open it in mvim set FILE to the filepath
```bash
F=$(basename $FILE) \
  && TMP=$(mktemp $HOME/tmp/$F.XXXX) \
  && p4 print -q $FILE > $TMP \
  && mvim -R --remote $TMP
```

## How to display color and/or control characters in an open file

When opening a file that contains control characters to indicate terminal
color, you'll see something like

```
Planning for vkms0-stable...
^[[0m^[[1mRefreshing Terraform state in-memory prior to plan...^[[0m
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.
^[[0m
^[[0m^[[1mdata.external.get_tf_compver: Refreshing state...^[[0m
^[[0m^[[1mdata.external.get_applied_ts: Refreshing state...^[[0m
^[[0m^[[1mdata.external.get_platform_ca_ttl["1"]: Refreshing state...^[[0m
```

Run `:term cat %` to pipe the current file through a terminal. This will open a
new temporary buffer but with all the colors/control characters properly shown.

# Buffer and region tricks

## VIM how to format XML region in file

Select region: `shift-v`

Then pass the selection through xmllint: `:'<,'>!xmllint --encode UTF-8 --format -`

## Run selections in a shell

### Run select lines in a bash subprocess

From <https://stackoverflow.com/questions/19883917/execute-current-line-in-bash-from-vim>

Select region then run `:w !bash`

### Set environment variables following

From <https://vim.fandom.com/wiki/Environment_variables>

`:let $PATH = '/foo:/bar'`

### Repeat last colon command following

From <https://vim.fandom.com/wiki/Repeat_last_colon_command>

`@:` and `@@`

### Run the current buffer (assuming it can be executed)

`:!%`

### By itself, runs the last external command (from your shell history) 

`:!`

### Repeats the last command

`:!!`

### Eliminates the need to hit enter after the command is done

`:silent !{cmd}`

### Puts the output of $cmd into the current buffer.

`:r !{cmd}`

### Fix nasty control characters in a buffer

`:term cat %`

# Window Operations

## Grep open buffers and open results in quickfix

```
:bufdo vimgrepadd [search] % | copen
```

## To enable/disable vertical scroll binding between two buffers:

```vim
:set scb!
```

from https://vim.fandom.com/wiki/Scrolling_synchronously

## Use ctrl-w v to create a vertical split

Instead of `:vs` use `ctrl-w v`

## Use ctrl-w o to show only the current buffer

Instead of `:only` use `ctrl-w o`

# Vim and Powerline stuff

## Powerline fonts on Mac

```sh
brew install coreutils
```

Install powerline fonts: https://github.com/powerline/fonts

Add a patched font to work for the above:
https://github.com/ryanoasis/nerd-fonts#font-installation

Install vim-airline:
https://github.com/vim-airline/vim-airline/blob/master/README.md

DevIcons: https://github.com/ryanoasis/vim-devicons

Install iTerm2 Shell integration: iTerm2 -> Install Shell Integration

## Install oh my zsh on Mac

```sh
xcode-select --install brew tap sambadevi/powerlevel9k brew install
powerlevel9k sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

# Insert timestamp of current file into the current buffer

I'm doing a bunch of processing Org files into my Markdown format. I haven't
gotten bored enough yet to automate the entire thing, but I did just realize I
can read the timestamp off the current file and insert it into the current
buffer:

```sh
r!ls -l --time-style=+'\%Y-\%m-\%dT\%H:\%M:\%S\%z' % | cut -d\  -f6
```

# Pretty prettify json in Vim

From <https://pascalprecht.github.io/posts/pretty-print-json-in-vim>

```bash
:%!python -m json.tool
```

# Mail a buffer from vim command prompt

```
:!mail --to me@little-fluffy.cloud --subject test123 <%
```

# Open previously opened files in vim

`:browse oldfiles`

# Quick vim tips - re-wrap lines and spell checking

## To re-wrap a long line use `gq`

Use either on a line or in Visual mode

`:help gq`

```
gq{motion}		Format the lines that {motion} moves over.
			Formatting is done with one of three methods:
			1. If 'formatexpr' is not empty the expression is
			   evaluated.  This can differ for each buffer.
			2. If 'formatprg' is not empty an external program
			   is used.
			3. Otherwise formatting is done internally.
```

## To enable spell checking

`:set spell`

`:help spell`

useful keys:

```
]s			Move to next misspelled word after the cursor.
			A count before the command can be used to repeat.
			'wrapscan' applies.

							*[s*
[s			Like "]s" but search backwards, find the misspelled
			word before the cursor.  Doesn't recognize words
			split over two lines, thus may stop at words that are
			not highlighted as bad.  Does not stop at word with
			missing capital at the start of a line.

...

zg			Add word under the cursor as a good word to the first
			name in 'spellfile'.  A count may precede the command
			to indicate the entry in 'spellfile' to be used.  A
			count of two uses the second entry.

			In Visual mode the selected characters are added as a
			word (including white space!).
...

Finding suggestions for bad words:
							*z=*
z=			For the word under/after the cursor suggest correctly
			spelled words.  This also works to find alternatives
			for a word that is not highlighted as a bad word,
			e.g., when the word after it is bad.
			In Visual mode the highlighted text is taken as the
			word to be replaced.
			The results are sorted on similarity to the word being
			replaced.
			This may take a long time.  Hit CTRL-C when you get
			bored.
```

# Build and deploy from within vim

```sh
let logjob = job_start("cd <path> && <command>", {'out_io': 'buffer', 'out_name': 'dummy2'})
```
