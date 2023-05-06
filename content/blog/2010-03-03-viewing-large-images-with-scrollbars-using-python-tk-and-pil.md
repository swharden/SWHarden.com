---
title: Display large Images with Scrollbars with Python, Tk, and PIL
date: 2010-03-03 19:56:55
tags: ["python", "old"]
---

# Display large Images with Scrollbars with Python, Tk, and PIL

__I wrote a program to display extremely large images in Python using TK. __It's interesting how simple this program is, yet frustrating how long it took me to figure out.

<div class="text-center img-border">

[![](https://swharden.com/static/2010/03/03/specview_thumb.jpg)](https://swharden.com/static/2010/03/03/specview.png)

</div>

__This little Python program__ will load an image (pretty much any format) using the Python Imaging Library (PIL, which must be installed) and allows you to see it on a scrollable canvas (in two directions) with Tkinter and ImageTk. The above screenshot is of the program viewing the image below:

<div class="text-center img-border large">

[![](https://swharden.com/static/2010/03/03/1hr_original_thumb.jpg)](https://swharden.com/static/2010/03/03/1hr_original.jpg)

</div>

__What is that image?__ I won't get ahead of myself, but it's about 5kHz of audio from 10.140mHz which includes a popular QRSS calling frequency. The image displays an hour of data. My ultimate goal is to have it scroll in the TK window, with slide-adjustable brightness/contrast/etc.

```python
from Tkinter import *
import Image, ImageTk

class ScrolledCanvas(Frame):
     def __init__(self, parent=None):
          Frame.__init__(self, parent)
          self.master.title("Spectrogram Viewer")
          self.pack(expand=YES, fill=BOTH)
          canv = Canvas(self, relief=SUNKEN)
          canv.config(width=400, height=200)
          canv.config(highlightthickness=0)

          sbarV = Scrollbar(self, orient=VERTICAL)
          sbarH = Scrollbar(self, orient=HORIZONTAL)

          sbarV.config(command=canv.yview)
          sbarH.config(command=canv.xview)

          canv.config(yscrollcommand=sbarV.set)
          canv.config(xscrollcommand=sbarH.set)

          sbarV.pack(side=RIGHT, fill=Y)
          sbarH.pack(side=BOTTOM, fill=X)

          canv.pack(side=LEFT, expand=YES, fill=BOTH)
          self.im=Image.open("./1hr_original.jpg")
          width,height=self.im.size
          canv.config(scrollregion=(0,0,width,height))
          self.im2=ImageTk.PhotoImage(self.im)
          self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

ScrolledCanvas().mainloop()
```