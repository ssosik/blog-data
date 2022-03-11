---
title: Google Sheets Dynamic Tab Names
description: ""
lead: ""
date: "2020-03-06T14:26:11-05:00"
lastmod: "2020-03-06T14:26:11-05:00"
tags:
  - google-sheets
  - spreadsheet
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Column of computed tab names

I wanted to create a summary table with aggregated data based on tables in other
tabs.

Following things like:
<https://stackoverflow.com/questions/26319026/using-a-cell-to-reference-the-name-of-sheet-in-a-formula-for-google-sheets>
<https://www.youtube.com/watch?v=W6DhIM53eIM>
<https://www.prolificoaktree.com/google-sheets-insert-sheet-names-into-cells/>
<https://support.google.com/docs/answer/3093290?hl=en>

With the spreadsheet open, Tools -> Script Editor and add these functions
```javascript
//Return the current sheet name.
function SheetName() {
  return SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getName();
}

//Return all current sheet names.
function SheetNames() {
  var out = new Array()
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  for (var i=0 ; i<sheets.length ; i++) out.push( [ sheets[i].getName() ] )
  return out
}

//Return specified sheet name
function SheetNumber(idx) {
  if (!idx)
    return SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getName();
  else {
    var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
    var idx = parseInt(idx);
    if (isNaN(idx) || idx < 1 || sheets.length < idx)
      throw "Invalid parameter (it should be a number from 0 to "+sheets.length+")";
    return sheets[idx-1].getName();
  }
}
```

Save the code.

Go back to the spreadsheet and enter `=sheetnames()`. This should add a columns
of the open Tab names after processing for a second. To Recalculate the tabs,
delete the computed cells and then hit *enter* with the formula cell selected.

# Dynamically compute data based on other cells

Use the ISBLANK and INDIRECT functions. Add this formula to a cell:
```
=IF(ISBLANK(B3),,MIN(INDIRECT("'"&B3&"'!G:G")))
```

If the cell `B3` is **not** blank, load the entire dataset of column `G` from
the sheet tab named in the cell at `B3`.
