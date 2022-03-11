---
title: Taskwarrior with time tracking hook
description: ""
lead: ""
date: "2019-03-13T10:56:24-04:00"
lastmod: "2019-03-13T10:56:24-04:00"
tags:
  - getting-things-done
  - zero-inbox
  - productivity
draft: true
weight: 50
images: []
contributors:
  - steve
---

I've recently started using Taskwarrior to track tasks as a replacement
for Emacs OrgMode. While it takes some discipline to incorporate it into
my daily and hourly workflow, it's really lightweight and seems like the
right tool for the job.

The one thing that I feel is lacking, however, is the ability to get
time reports based on starting/stopping work on a specific task.

A quick google turned up this:
https://github.com/kostajh/taskwarrior-time-tracking-hook

So let's give it a shot:

```sh
pip3 install taskwarrior-time-tracking-hook

# pip installed the binary to ~/.local/bin/; Needed to add ~/.local/bin to my $PATH

mkdir -p ~/.task/hooks
ln -s `which taskwarrior_time_tracking_hook` ~/.task/hooks/on-modify.timetracking

task config uda.totalactivetime.type duration
task config uda.totalactivetime.label Total active time
task config uda.totalactivetime.values ''

task config report.list.labels 'ID,Active,Age,TimeSpent,D,P,Project,Tags,R,Sch,Due,Until,Description,Urg'
task config report.list.columns 'id,start.age,entry.age,totalactivetime,depends.indicator,priority,project,tags,recur.indicator,scheduled.countdown,due,until.remaining,description.count,urgency'
```
