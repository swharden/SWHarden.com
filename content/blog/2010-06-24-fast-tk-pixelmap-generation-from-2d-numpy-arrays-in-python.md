---
title: Fast TK Pixelmap generation from 2D Numpy Arrays in Python
date: 2010-06-24 21:29:29
tags: ["python", "old"]
---

# Fast TK Pixelmap generation from 2D Numpy Arrays in Python

__I had TKinter all wrong!__ While my initial tests with PyGame's rapid ability to render Numpy arrays in the form of pixel maps proved impressive, it was only because I was comparing it to poor TK code. I don't know what I was doing wrong, but when I decided to give TKinter one more shot I was blown away -- it's as smooth or smoother as PyGame. Forget PyGame! I'm rendering everything in raw TK from now on. This utilizes the Python Imaging Library (PIL) so it's EXTREMELY flexible (supports fancy operations, alpha channels, etc).

<div class="text-center img-border">

[![](https://swharden.com/static/2010/06/24/glade_python_improving_thumb.jpg)](https://swharden.com/static/2010/06/24/glade_python_improving.png)

</div>

__The screenshot shows__ me running the script (below) generating random noise and "scrolling" it horizontally (like my spectrograph software does) at a fast rate smoothly (almost 90 FPS!). Basically, it launches a window, creates a canvas widget (which I'm told is faster to update than a label and reduces flickering that's often associated with rapid redraws because it uses double-buffering). Also, it uses threading to handle the calculations/redraws without lagging the GUI. The code speaks for itself.

```python
import Tkinter
from PIL import Image, ImageTk
import numpy
import time


class mainWindow():
    times = 1
    timestart = time.clock()
    data = numpy.array(numpy.random.random((400, 500))*100, dtype=int)

    def __init__(self):
        self.root = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.root, width=500, height=400)
        self.frame.pack()
        self.canvas = Tkinter.Canvas(self.frame, width=500, height=400)
        self.canvas.place(x=-2, y=-2)
        self.root.after(0, self.start)  # INCREASE THE 0 TO SLOW IT DOWN
        self.root.mainloop()

    def start(self):
        global data
        self.im = Image.fromstring('L', (self.data.shape[1],
                                         self.data.shape[0]), self.data.astype('b').tostring())
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=Tkinter.NW)
        self.root.update()
        self.times += 1
        if self.times % 33 == 0:
            print "%.02f FPS" % (self.times/(time.clock()-self.timestart))
        self.root.after(10, self.start)
        self.data = numpy.roll(self.data, -1, 1)


if __name__ == '__main__':
    x = mainWindow()
```

