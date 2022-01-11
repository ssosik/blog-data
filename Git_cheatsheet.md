---
title: Git cheatsheet
description: ""
lead: ""
date: "2021-09-01T19:31:58-04:00"
lastmod: "2021-09-01T19:31:58-04:00"
tags:
  - git
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

### Tag delete

How to delete a tag locally and on a remote
https://www.manikrathee.com/how-to-delete-a-tag-in-git.html

Delete the tag locally
    git tag -d refs/heads/main

Delete it from the remote, in this case the tag was confusingly named `refs/heads/main`
    git push origin :refs/tags/refs/heads/main

### Submodule sync and changes through .gitmodules

I had a problem while I was attempting to push to remote in a submodule, git
was attempting to push using the wrong username.

Solution: add the username to the submodule URL **AND** then to a `git submodule
sync`. Without the submodule sync, the incorrect username will continue to be
used.

```toml
cat .gitmodules

[submodule "content/notes"]
	path = content/notes
	url = https://ssosik@github.com/ssosik/blog-data.git
        # Add this    ^^^^^^^
```

Then `git submodule sync`. Git pushes should then use the correct user.
