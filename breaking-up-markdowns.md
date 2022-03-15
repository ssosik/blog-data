---
title: Breaking down my monolithic repo of Markdowns into Public/Private, Work/Personal
date: "2022-03-11T11:17:35-0500"
tags:
  - markdown
  - cli
  - git
draft: false
weight: 50
images: []
---

Use this to move files/directories from one git repo into another, removing the
item from the former repo.

# Set up
```bash
git remote add origin https://github.com/ssosik/work-notes-public.git
git remote add gitsource ssh://git@git.source:7999/~ssosik/notes.git

git checkout -b new origin/main
git checkout -b old gitsource/main
```

# Script
{{< include title="breaking-up-markdowns.sh" file="breaking-up-markdowns.sh" lang="bash" open=true highlight={linenos=table} >}}

Then run this loop to move files from the `old` branch into the `new`
branch, deleting the file from the `old` branch.

# Make the changes
```bash
# Look for files/directories to move over
git diff old

# e.g.
moveit APC-1067_Mount_Aliasing_stress_test_notes.md
```
