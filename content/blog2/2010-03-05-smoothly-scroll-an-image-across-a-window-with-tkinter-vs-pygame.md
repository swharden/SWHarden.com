---
title: Smoothly Scroll an Image Across a Window with Tkinter vs. PyGame
date: 2010-03-05 08:49:00
tags: ["python", "obsolete"]
---

# Smoothly Scroll an Image Across a Window with Tkinter vs. PyGame

<div class="text-center img-border">

![](https://swharden.com/static/2010/03/05/tk-scrolling.png)

</div>

__The goal is simple: have a very large image (larger than the window) automatically scroll across a Python-generated GUI window.__ I already have the code created to generate spectrograph images in real time, now I just need a way to have them displayed in real time. At first I tried moving the coordinates of my images and even generating new images with create\_image(), but everything I did resulted in a tacky "flickering" effect (not to mention it was slow). Thankfully I found that `` self.canv.move(self.imgtag,-1,0) `` can move a specific item (self.imgtag) by a specified amount and it does it smoothly (without flickering). Here's some sample code. Make sure "snip.bmp" is a big image in the same folder as this script

```python
from Tkinter import *
import Image
import ImageTk


class scrollingImage(Frame):

    def go(self):
        self.canv.move(self.imgtag, -1, 0)
        self.canv.update()
        self.after(100, self.go)

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.master.title("Spectrogram Viewer")
        self.pack(expand=YES, fill=BOTH)
        self.canv = Canvas(self, relief=SUNKEN)
        self.canv.config(width=200, height=200)
        self.canv.config(highlightthickness=0)

        sbarV = Scrollbar(self, orient=VERTICAL)
        sbarH = Scrollbar(self, orient=HORIZONTAL)

        sbarV.config(command=self.canv.yview)
        sbarH.config(command=self.canv.xview)

        self.canv.config(yscrollcommand=sbarV.set)
        self.canv.config(xscrollcommand=sbarH.set)

        sbarV.pack(side=RIGHT, fill=Y)
        sbarH.pack(side=BOTTOM, fill=X)

        self.canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.im = Image.open("./snip.bmp")
        width, height = self.im.size
        # self.canv.config(scrollregion=(0,0,width,height))
        self.canv.config(scrollregion=(0, 0, 300, 300))
        self.im2 = ImageTk.PhotoImage(self.im)
        x, y = 0, 0
        self.imgtag = self.canv.create_image(x, y,
                                             anchor="nw", image=self.im2)
        self.go()

scrollingImage().mainloop()
```

__Alternatively, I found a way to accomplish a similar thing with PyGame.__ I've decided not to use PyGame for my software package however, because it's too specific and can't be run well alongside Tk windows, and it would be insanely hard to add scrollbars to the window. However it's extremely effective at scrolling images smoothly. Anyhow, here's the code:

```python
import pygame
from PIL import Image

im = Image.open("1hr_original.jpg")
graphic = pygame.image.fromstring(im.tostring(), im.size, im.mode)
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = 1
x, y = 0, 0
while running:
    clock.tick(30)
    for event in pygame.event.get():  # get user input
        if event.type == pygame.QUIT:  # if user clicks the close X
            running = 0  # make running 0 to break out of loop
    screen.blit(graphic, (x, y))
    pygame.display.flip()  # Update screen
    x -= 1
```

