---
title: Launch with Zoom
date: 2018-04-14 12:49:18
thumbnail: automator.png
usePageBundles: true
---

Simple Automator Workflow to Get rid of "Open zoom.us.app" on Mac

<!--more-->

![](automator.png)

## How to Install

1. Download workflow file and extract
1. Double click on "Launch with Zoom.workflow"
1. Click "Install" on Dialog

## How to Use

1. On and zoom link, just Right click > Services > Launch with Zoom
   ![](menu.png)

   **OR**

1. Select zoom link
1. On Mac Touch bar > Quick Action > "Launch with Zoom"

[Click here to get Mac Automator Workflow](workflow.zip)

## How to create it yourself

1. Open Automator
1. Create a new workflow ( File > New > Quick Action)
1. Add a "Run Shell Script" action ( filter second column to find the action )
1. Configure workflow
   - Workflow receives current **URLs** in **any application**
   - Input is **only URLs**
   - Image **Video**
   - Color **Blue**
1. In "Run Shell Script"
   - Shell: **/bin/bash**
   - Pass input: **as arguments**
1. Put following script in the text box

   ```bash
   open $(echo $1 | sed -E 's#https://[a-zA-Z0-9]+.zoom.us/j/#zoommtg://zoom.us/join?confno=#g;s/\?pwd/\&pwd/')
   ```

1. Save workflow (File > Save)
1. Save quick action as: **Launch with Zoom**
1. Quit Automator
