---
title: Realtime image pixelmap from Numpy array data in Qt
date: 2013-06-03 22:40:56
tags: ["python", "old"]
---

# Realtime image pixelmap from Numpy array data in Qt

Consider realtime spectrograph software like [QRSS VD](http://www.swharden.com/blog/qrss_vd/#screenshots).  It's primary function is to scroll a potentially huge data-rich image across the screen. In Python, this is often easier said than done.__ If you're not careful, you can tackle this problem inefficiently and get terrible frame rates (<5FPS) or eat a huge amount of system resources (I get complaints often that QRSS VD takes up a lot of processor resources, and 99% of it is drawing the images).  In the past, I've done it at least 4 different ways ([one](http://www.swharden.com/blog/2010-03-05-animated-realtime-spectrograph-with-scrolling-waterfall-display-in-python/), [two](http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/), [three](http://www.swharden.com/blog/qrss_vd/#screenshots), [four](http://www.swharden.com/blog/2010-06-24-fast-tk-pixelmap-generation-from-2d-numpy-arrays-in-python/), [five](http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/)). Note that "four" seems to be the absolute fastest option so far. I've been keeping an eye out for a while now contemplating the best way to rapidly draw color-mapped 8-bit data in a python program. Now that I'm doing a majority of my graphical development with PyQt and QtDesigner (packaged with [PythonXY](https://code.google.com/p/pythonxy/)), I ended-up with a solution that looks like this (plotting random data with a colormap):


<div class="text-center img-border">

![](qt-scrolling-spectrograph.gif)

</div>

1.) in QtDesigner, create a form with a **scrollAreaWidget**

2.) in QtDesigner, add a **label** inside the **scrollAreaWidget**

3.) in code, resize **label** and also **scrollAreaWidgetContents **to fit data (disable "widgetResizable")

4.) in code, create a **QImage** from a 2D numpy array (dtype=uint8)

5.) in code, set **label** pixmap to QtGui.QPixmap.fromImage(**QImage**)

That's pretty much it! Here are some highlights of my program. Note that the code for the GUI is in a separate file, and must be downloaded from the ZIP provided at the bottom. Hope it helps someone else out there who might want to do something similar!

```python
import ui_main
import sys
from PyQt4 import QtCore, QtGui

import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PIL import Image
import numpy
import time

spectroWidth=1000
spectroHeight=1000

a=numpy.random.random(spectroHeight*spectroWidth)*255
a=numpy.reshape(a,(spectroHeight,spectroWidth))
a=numpy.require(a, numpy.uint8, 'C')

COLORTABLE=[]
for i in range(256): COLORTABLE.append(QtGui.qRgb(i/4,i,i/2))

def updateData():
    global a
    a=numpy.roll(a,-5)
    QI=QtGui.QImage(a.data, spectroWidth, spectroHeight, QtGui.QImage.Format_Indexed8)
    QI.setColorTable(COLORTABLE)
    uimain.label.setPixmap(QtGui.QPixmap.fromImage(QI))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win_main = ui_main.QtGui.QWidget()
    uimain = ui_main.Ui_win_main()
    uimain.setupUi(win_main)

    # SET UP IMAGE
    uimain.IM = QtGui.QImage(spectroWidth, spectroHeight, QtGui.QImage.Format_Indexed8)
    uimain.label.setGeometry(QtCore.QRect(0,0,spectroWidth,spectroHeight))
    uimain.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0,0,spectroWidth,spectroHeight))

    # SET UP RECURRING EVENTS
    uimain.timer = QtCore.QTimer()
    uimain.timer.start(.1)
    win_main.connect(uimain.timer, QtCore.SIGNAL('timeout()'), updateData)

    ### DISPLAY WINDOWS
    win_main.show()
    sys.exit(app.exec_())
```
