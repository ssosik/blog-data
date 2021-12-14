---
title: Gnu Wiggle manpage
description: ""
lead: ""
date: "2020-12-15T15:11:15-05:00"
lastmod: "2020-12-15T15:11:15-05:00"
tags:
  - work
  - wiggle
  - diff
  - git
  - gnu
  - manpage
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

This view shows the merge of the patch with the
original file.  It is like a full-context diff showing
removed lines with a '-' prefix and added lines with a
'+' prefix.
In cases where a patch chunk could not be successfully
applied, the original text is prefixed with a '|', and
the text that the patch wanted to add is prefixed with
a '+'.
When the cursor is over such a conflict, or over a chunk
which required wiggling to apply (i.e. there was unmatched
text in the original, or extraneous unchanged text in
the patch), the terminal is split and the bottom pane is
use to display the part of the patch that applied to
this section of the original.  This allows you to confirm
that a wiggled patch applied correctly, and to see
why there was a conflict

Highlight Colours and Keystroke commands

In all different views of a merge, highlight colours
are used to show which parts of lines were added,
removed, already changed, unchanged or in conflict.
Colours and their use are:
 normal              unchanged text
 red                 text that was removed or changed
 green               text that was added or the result
                     of a change
 yellow background   used in side-by-side for a line
                     which has no match on the other
                     side
 blue                text in the original which did not
                     match anything in the patch
 cyan                text in the patch which did not
                     match anything in the original
 cyan background     already changed text: the result
                     of the patch matches the original
 underline           remove or added text can also be
                     underlined indicating that it
                     was involved in a conflict

While viewing a merge various keystroke commands can
be used to move around and change the view.  Basic
movement commands from both 'vi' and 'emacs' are
available:

 p control-p k UP    Move to previous line
 n control-n j DOWN  Move to next line
 l LEFT              Move one char to right
 h RIGHT             Move one char to left
 / control-s         Enter incremental search mode
 control-r           Enter reverse-search mode
 control-g           Search again
 ?                   Display help message
 ESC-<  0-G          Go to start of file
 ESC->  G            Go to end of file
 q                   Return to list of files or exit
 S                   Arrange for merge to be saved on exit
 control-C           Disable auto-save-on-exit
 control-L           recenter current line
 control-V SPACE     page down
 ESC-v   BACKSPC     page up
 N                   go to next patch chunk
 P                   go to previous patch chunk
 C                   go to next conflicted chunk
 C-X-o   O           move cursor to alternate pane
 ^ control-A         go to start of line
 $ control-E         go to end of line

 a                   display 'after' view
 b                   display 'before' view
 o                   display 'original' view
 r                   display 'result' view
 d                   display 'diff' or 'patch' view
 m                   display 'merge' view
 |                   display side-by-side view

 I                   toggle whether spaces are ignored
                     when matching text.
 x                   toggle ignoring of current Changed,
                     Conflict, or Unmatched item
 c                   toggle accepting of result of conflict
 X                   Revert 'c' and 'x' changes on this line
 v                   Save the current merge and run the
                     default editor on the file.

