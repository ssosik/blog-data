---
title: Pandoc Tricks
description: ""
lead: ""
date: "2019-03-29T12:12:57-04:00"
lastmod: "2019-03-29T12:12:57-04:00"
categories:
  - cli
tags:
  - pandoc
  - markdown
draft: false
weight: 50
images: []
contributors:
  - steve
---

# Links
- [Some useful notes on Pandoc tricks](https://github.com/jgm/pandoc/wiki/Pandoc-Tricks)

# Pandoc example to reformat Markdown and add Title

```sh
pandoc --columns=80 --atx-headers -s --toc -f markdown \
    -t markdown rfcs/VKMS-10-Vault-config-and-deployment-rfc.md \
     > rfcs/VKMS-10-Vault-config-and-deployment-rfc.md.pandoc
```

# Pandoc links from markdown

Wrap `http://` prefixed URLs with angle brackets in order for Pandoc to convert
them to clickable links.

From:
<https://stackoverflow.com/questions/35414121/pandoc-automatically-convert-urls-into-hyperlinks>

Bonus how to use vim-surround to wrap string in angle brackets:
`ysWa`

# Pandoc lua filter documentation

https://pandoc.org/lua-filters.html#type-ref-Link

# Use pandoc and some bash scripting to convert P4 scratch file into WIKIs

Since 2013 I've kept a Perforce-controlled "scratch" buffer to keep
track of various debugging notes, bash snippets, and other useful bits
of info. I recently broke that file up by P4 change-number and created
timestamped markdown documents.

In order to enable my markdown-ir.vim Xapian markdown indexer/querier to
load and search these files, I need to put a YAML frontmatter section
into each file. Let's use pandoc and some bash glue to do that.

## Create templates to help parse any existing YAML frontmatter

```sh
pandoc --print-default-template=markdown
> $if(titleblock)$
> $titleblock$
> 
> $endif$
> $for(header-includes)$
> $header-includes$
> 
> $endfor$
> $for(include-before)$
> $include-before$
> 
> $endfor$
> $if(toc)$
> $table-of-contents$
> 
> $endif$
> $body$
> $for(include-after)$
> 
> $include-after$
> $endfor$

# Create the full-body template which will be our final output target
pandoc --print-default-template=markdown > full.pandoc

# Create two template files from above, one for the "titleblock" and one for the
rest of the document:
cat frontmatter.pandoc
> $if(titleblock)$
> $titleblock$
> 
> $endif$

cat body.pandoc
> $for(header-includes)$
> $header-includes$
> 
> $endfor$
> $for(include-before)$
> $include-before$
> 
> $endfor$
> $if(toc)$
> $table-of-contents$
> 
> $endif$
> $body$
> $for(include-after)$
> 
> $include-after$
> $endfor$
```

## Pull the existing markdown data off the document if it exists

    pandoc --standalone --from markdown+yaml_metadata_block --to markdown_strict+yaml_metadata_block --atx-headers --template frontmatter.pandoc diary/2013-03-13_17:13:41.md -o metadata.yaml

### Python code to load the YAML file to create pandoc command line args

```python
'''
Example:
    python3 pandoc-yaml-argifier.py 1980-01-01_01:01.md -title STEVE thing -tags foo1 foo2 foo3
'''

import sys
import yaml
import subprocess
import os.path
import dateutil.parser
import re
from collections import defaultdict
from pdb import set_trace

sys.argv.pop(0) # discard script name
datafile = sys.argv.pop(0) # Original Markdown file

PANDOC = '/usr/bin/pandoc'
METADATA_TMPL = "frontmatter.pandoc"
BODY_TMPL = "body.pandoc"
FULL_TMPL = "full.pandoc"

cmd = [PANDOC, '--standalone', '--from', 'markdown+yaml_metadata_block', '--to',
        'markdown+yaml_metadata_block', '--atx-headers', '--template',
        METADATA_TMPL, datafile]
mdata = subprocess.check_output(cmd)
metadata = yaml.load(mdata.strip().strip(b"---").strip())
if metadata is None:
    metadata = {}

cmd = [PANDOC, '--standalone', '--from', 'gfm+yaml_metadata_block', '--to',
        'gfm+yaml_metadata_block', '--atx-headers', '--template',
        BODY_TMPL, datafile]
body = subprocess.check_output(cmd).decode("unicode_escape")
#print(body)
#set_trace()

overrides = {}
overrides["date"] = dateutil.parser.parse(os.path.splitext(datafile)[0].replace('_', ' ')).isoformat()
m = re.search('.*# (.*)\n', body)
if m is not None:
    overrides["title"] = m.group(1)
#overrides["name"] = datafile

tmp = defaultdict(list)
for token in sys.argv:
    if token.startswith('-'):
        key = token.lstrip('-')
        if key not in tmp:
            tmp[key] = []
    else:
        tmp[key].append(token)

for k, v in tmp.items():
    if len(v) == 1:
        overrides[k] = v[0]
    else:
        overrides[k] = v

overrides.update(metadata)

output = ''
for k, v in overrides.items():
    if isinstance(v, (list, tuple)):
        if len(v) == 0:
            output += '-M {}:" " '.format(k)
        else:
            for vi in v:
                output += '-M {}:"{}" '.format(k,vi)
    else:
        output += '-M {}:"{}" '.format(k,v)

print(output)
```

### Run the above script and use xargs to pipe to pandoc

``` {.bash}
python3 pandoc-yaml-argifier.py metadata.yaml -author steve -category work -cover -excert -date "FOOTIME" -tags -title "FOOTITLE" -subtitle | xargs pandoc --standalone  --to markdown_strict+yaml_metadata_block --atx-headers
python3 pandoc-yaml-argifier.py 1980-01-01_01:01.md -author steve -category work | xargs pandoc --standalone  --to markdown_strict+yaml_metadata_block --atx-headers 1980-01-01_01:01.md
python3 pandoc-yaml-argifier.py 1980-01-01_01:01.md -cover -author steve -category work | xargs pandoc --standalone  --to markdown_strict+yaml_metadata_block --atx-headers 1980-01-01_01:01.md
```

### Bash script to put it all together

```sh
#!/bin/bash

set -e

for F in $(ls *.md) ; do
    echo $F
    python3 pandoc-yaml-argifier.py $F -cover -author steve -category work | xargs pandoc --standalone  --from markdown+yaml_metadata_block --to markdown+yaml_metadata_block --atx-headers -o $F $F
done
```

## Doing it again to remove category and stuff the value under tags

```python
'''
Example:
    python3 pandoc-yaml-argifier.py 1980-01-01_01:01.md -title STEVE thing -tags foo1 foo2 foo3
'''

import sys
import yaml
import subprocess
import os.path
import dateutil.parser
import re
from collections import defaultdict
from pdb import set_trace

sys.argv.pop(0) # discard script name
datafile = sys.argv.pop(0) # Original Markdown file

PANDOC = '/usr/bin/pandoc'
METADATA_TMPL = "frontmatter.pandoc"
BODY_TMPL = "body.pandoc"
FULL_TMPL = "full.pandoc"

cmd = [PANDOC, '--standalone', '--from', 'markdown+yaml_metadata_block', '--to',
        'markdown+yaml_metadata_block', '--atx-headers', '--template',
        METADATA_TMPL, datafile]
mdata = subprocess.check_output(cmd)
metadata = yaml.load(mdata.strip().strip(b"---").strip())
if metadata is None:
    metadata = {}

if 'tags' not in metadata:
    metadata['tags'] = list()

if not isinstance(metadata['tags'], list):
    print("NOT A LIST %s" % metadata['tags'])

if 'category' in metadata:
    metadata['tags'].append(metadata['category'])
    metadata['category'] = ''  # Empty out the category

output = ''
for k, v in metadata.items():
    if isinstance(v, (list, tuple)):
        if len(v) == 0:
            output += '-M {}:" " '.format(k)
        else:
            for vi in v:
                output += '-M {}:"{}" '.format(k,vi)
    else:
        output += '-M {}:"{}" '.format(k,v)

print(output)
```

### And the bash loop

```sh
for F in $(ls *.md) ; do
    echo $F
    python3 markdown-pandoc-scraper-argifier.py $F | xargs pandoc --standalone  --from markdown+yaml_metadata_block --to markdown+yaml_metadata_block --atx-headers -o $F $F
done
```

# how to extract only metadata from a markdown file

Create a custom pandoc template to only output the file metadata.

```sh
pandoc --print-default-template=markdown > md-tmpl.pandoc
cat md-tmpl.pandoc
> $titleblock$

markdown+yaml_metadata_block --to markdown+yaml_metadata_block --atx-headers \
    --template md-tmpl.pandoc diary/2019-03-09_20:49.md
> ---
> author: steve
> cover: '8.jpg'
> subtitle: how to extract only metadata from a markdown file
> tags:
> - pandoc
> - title: More pandoc and markdown wrangling
> - ---
```

# Notes on exporting markdown files to /u4 via pandoc

Useful resources on pandoc and markdown processing:
http://www.flutterbys.com.au/stats/tut/tut17.3.html
https://metacpan.org/pod/Pandoc::Metadata

```bash
pandoc -s -f markdown -t html -o /u4/ssosik/public_html/notes/2019-03-26T14:38:00-04:00/index.html /home/ssosik/workspace/vimdiary/2019-03-26T14:38:00-04:00/index.md
```

# Vim function to publish directly from Vim
```
let g:publish_dir = '/u4/ssosik/public_html/notes'
let g:pandoc_bin = '/usr/bin/pandoc'
" Filter markdown links to html, idea from https://stackoverflow.com/a/49396058
let g:pandoc_args = '-s -f markdown -t html --lua-filter=/home/ssosik/.local/pandoc/lua/links-to-html.lua'
let g:publish_suffix = 'html'

function! PandocPublish()
python3 << EOF
import vim
import os.path
import subprocess

pandoc = vim.eval('g:pandoc_bin')
args = vim.eval('g:pandoc_args')
root = vim.eval('g:publish_dir')
suffix = vim.eval('g:publish_suffix')

filename = vim.current.buffer.name
subdir = os.path.split(os.path.dirname(filename))[1]
fname = os.path.splitext(os.path.basename(filename))[0]
outpath = os.path.join(root, subdir)
outfile = os.path.join(outpath, fname + '.' + suffix)

try:
    os.mkdir(outpath)
except FileExistsError:
    pass
cmd = '{} {} -o {} {}'.format(pandoc, args, outfile, filename)
subprocess.check_output(cmd.split(' '))

EOF
endfunction
command! -nargs=0 PandocPublish call PandocPublish()
```

# Lua Pandoc filter to convert .md links to .html

```lua
function Link(el)
  el.target = string.gsub(el.target, "%.md", ".html")
  return el
end
```

# Use pandoc to convert vimwiki documents to markdown format

When I first started using Vimwiki, I used the default "vimwiki"
document format. After learning a bit about how GatsbyJS and it's data
sourcing works, it would be better if my content were in "markdown"
format.

Let's use **Pandoc** to convert the vimwiki files into markdown. Only
newer versions of Pandoc support the vimwiki file format.

## Download and install the latest version of pandoc

    wget https://github.com/jgm/pandoc/releases/download/2.6/pandoc-2.6-1-amd64.deb
    sudo dpkg -i pandoc-2.6-1-amd64.deb

## Run pandoc to convert all vimwiki files into mardown format

    while read L ; do
        echo $L
        F=$(basename -a -s .wiki "$L")
        P=$(dirname "$L")
        pandoc -f vimwiki -t markdown -o $P/$F.md $L
    done < <(find . -type f -name '*.wiki')

## Document metadata

FIXME - More fiddling with Pandoc to see if I can have it
generate/preserve the "frontmatter" header information on each Markdown
page that the Gatsby remark plugin requires so that it can properly
query the document. It looks like the `yaml_metadata_block` markdown
extension is what should do it.

I'll want to add the header metadata on each Markdown file from within
Vimwiki to include values for:

    - title
    - author
    - date
    - abstract
    - keywords
    - tags

Reference https://pandoc.org/MANUAL.html\#metadata-variables

Then, when running pandoc, see if I can pass in a variable corresponding
to the file path. Or, see if I can get vim to do this. I need the file
path as part of Gatsby when building the site.

Something like this should work:

    pandoc -s -f markdown+yaml_metadata_block -t markdown+yaml_metadata_block --metadata=foo:bar workspace/vimwiki/diary/2019-02-28.md

### Figured out why lists weren't working in pandoc conversion

Need to add a newline between the list and the previous line in order
for lists to be interpreted properly.

## More pandoc digging

This should work:

``` {.bash}
pandoc -s -f markdown+pandoc_title_block -t markdown+yaml_metadata_block --metadata=path:bash-tool-timeout.md -o workspace/node-docker/site/src/markdown/bash-tool-timeout.md workspace/vimwiki/posts/bash-tool-timeout.md
```

But, YAML title info didn't work. Needed to follow:
https://pandoc.org/MANUAL.html\#metadata-blocks

Use pandoc\_title\_block format:

    % (title)
    % (author)
    % (date)

## Even more digging.

Turns out the YAML metadata must conform to YAML syntax! I.e. if the
value contains a ':' colon, then the entire value must be wrapped in
quotes. If not, pandoc barfs on trying to parse the metadata.
