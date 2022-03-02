---
title: Git Tricks and Cheatsheet
description: ""
lead: ""
date: "2021-09-01T19:31:58-04:00"
tags:
  - git
  - cli
  - cheatsheet
  - tricks
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Remotes

## Fetch everything from remotes

```bash
git fetch --all --tags --prune
```

# Tags

## List tags

```bash
git tag --list
```

## Tag delete

How to delete a tag locally and on a remote
https://www.manikrathee.com/how-to-delete-a-tag-in-git.html

Delete the tag locally, in this case the tag was confusingly named `refs/heads/main`
```bash
git tag -d refs/heads/main
```

Delete it from the remote, in this case the tag was confusingly named `refs/heads/main`
```bash
git push origin :refs/tags/refs/heads/main
```

# Submodules

## Submodule sync and changes through .gitmodules

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

# Diffing, merging, cherry-picking, and adding code chunks

## Interactively select chunks of code from a different branch

```bash
git checkout -p origin/master
```

## Git log/diff excluding subdirectories

Golang is messy, especially when trying to view git diffs when dependencies have
changed. Exclude vendored dependencies when view commits/diffs

```bash
# Exclude 'vendor' subdirectory
git diff add-akamake feature/KMI-913-development  ':!vendor'

# Or                   <go.mod/go.sum>  <all vendored files>
git diff origin/master ':(exclude)go.*' ':(exclude)vendor/*'
```

# Committing

## Show staged diff while editing the commit message

```bash
git commit -v
```

Or while amending the last commit
```bash
git commit -v --amend
```

# Rebasing

## Interactively reorder/squash/edit a range of commits

This is really useful alongside the fugitive.vim plugin to see the contents of
individual commits. Use actions like "pick", "reword", "edit", "squash",
"fixup", "drop", and "break" to curate a history. You can do things like:
- merge related commits into one and edit the commit message
- break apart single commits into smaller pieces, adding just the code you want
    per commit
- reorder commits
- reword a commit message
- keep a commit just as it is

### Break up a commit into smaller pieces

```bash
git rebase -i HEAD~4 # Edit the history far enough back

# Mark the commit I want to pull apart as "e" (edit)

# Use this command to see the current patch
git rebase --show-current-patch

# Reset the current commit
git reset HEAD^

# Edit the index
git add -p
git commit

# Add other parts of the original commit that you want to break into separate commits
git add -p
git commit ...

# Resume the rebase
git rebase --continue
```

# Show contents of file from another branch

```bash
git show origin/dev-branch:Dockerfile
```

# Get current branch name

```bash
git rev-parse --abbrev-ref HEAD
```
