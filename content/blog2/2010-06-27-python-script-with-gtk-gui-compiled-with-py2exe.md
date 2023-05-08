---
title: Python Script with GTK GUI Compiled with Py2EXE
date: 2010-06-27 23:16:05
---

# Python Script with GTK GUI Compiled with Py2EXE

__This is a total hack, but it works.__ I spent all night jumping through hoops to get this thing to run on Windows. The problem is that I designed my previous UI in a version of GLADE which is newer than that supported by Windows. It looks like it's not backward-compatible, so I have to re-design the GUI from scratch using an earlier version of GLADE. I'll probably stick to GTK version 2.12 and Python version 2.6 because they play nicely on Windows. It's a quick and dirty script, but I was able to make the following run on Windows as a single EXE file!

<div class="text-center">

![](https://swharden.com/static/2010/06/27/glade_windows_python.png)

</div>

> Scott from the future (10 years later): Where's the source code for this? Weird post.