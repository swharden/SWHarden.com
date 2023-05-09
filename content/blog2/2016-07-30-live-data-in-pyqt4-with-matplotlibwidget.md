---
title: Live Data in PyQt4 with MatplotlibWidget
date: 2016-07-30 23:15:23
tags: ["python", "obsolete"]
---



__I keep getting involved in projects which require live data to be graphed in real time.__ Since most of my back-end is written in Python, it makes sense to have a Pythonic front-end. Cross-platform GUI programming in Python is frustratingly non-trivial, as there multiple window frameworks available (TK, GTK, and QT) and their respective graphical designers ([torture](https://wiki.python.org/moin/Intro%20to%20programming%20with%20Python%20and%20Tkinter), [Glade](https://glade.gnome.org/), and [QT Designer](http://doc.qt.io/qt-4.8/designer-manual.html)) and each has its own way of doing things. Add different ways to plot data in the mix ([gnuplot](http://www.gnuplot.info/), [matplotlib](http://matplotlib.org/), and [custom widgets](http://qcustomplot.com/)) and it can become a complicated mess. Different framework combinations favor different features (with unique speed / simplicity / elegance), so my goal is to slowly test out a few combinations most likely to work for my needs, and add my findings to a [growing github repository](https://github.com/swharden/Python-GUI-examples). The first stab is using PyQt4 and matplotlib's widget (MatplotlibWidget). Rather than capture data from the sound card (my ultimate goal), I'm going to generate a sine wave whose phase and color is related to the system time. Matplotlib plotting is a bit slow, but the output is beautiful, and their framework is so robust. Here's the output of my first test showing the sine wave generated as well as the console output (showing that each call to the plotting function takes about 40 ms. At this rate, I can expect a maximum update rate of ~25 Hz.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/30/demo.gif)
![](https://swharden.com/static/2016/07/30/qt4.png)

</div>

__Designing this project was easy, but it was surprisingly hard to figure out how to do this based on examples I found on the internet.__ This is part of why I wanted to place this example here. The downside of many internet examples is that they did not use Qt Designer to make the window, so their code to create a window and insert the MatplotlibWidget wasn't copy/paste compatible with my goals, and often more complex than I needed. Some internet examples _did_ use Qt Designer to make the window, but left a frame empty which they later manually filled with a widget and attached to a matplotlib canvas. This is fine, but more complex than I need to get started.

__First, I designed a GUI with Qt Designer__. I dropped a MatplotlibWidget somewhere, and used its default name. I saved this file as [ui\_main.ui](https://github.com/swharden/Python-GUI-examples/blob/master/2016-07-30_qt_matplotlib_sine_scroll/ui_main.ui) (which is an XML file, ready to be used for [multiple programming languages](http://doc.qt.io/qt-4.8/designer-using-a-ui-file.html)).

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/30/pyqt4-designer.png)

</div>

__Next, I converted the UI file into a .py file__ with a standalone python script that's an alternative to using pyuic from the command line. The script to do this is [ui\_convert.py](https://github.com/swharden/Python-GUI-examples/blob/master/2016-07-30_qt_matplotlib_sine_scroll/ui_convert.py) and it calls PyQt4.uic.compileUi():

```python
from PyQt4 import uic
fin = open('ui_main.ui','r')
fout = open('ui_main.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()
```

__I then created my main program file which populates the matplotlib widget with data.__ I called it [go.py](https://github.com/swharden/Python-GUI-examples/blob/master/2016-07-30_qt_matplotlib_sine_scroll/go.py) and running it will launch the app. The code explains it all, and there's not much more to say! It produces the output at the top of this post.

```python
from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pylab
import time

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.update)
        self.matplotlibwidget.axes.hold(False) #clear on plot()

    def update(self):
        t1=time.time()
        points=100 #number of data points
        X=np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=pylab.cm.jet(time.time()%10/10) # random color
        self.matplotlibwidget.axes.plot(X,Y,ms=100,color=C,lw=10,alpha=.8)
        self.matplotlibwidget.axes.grid()
        self.matplotlibwidget.axes.get_figure().tight_layout() # fill space
        self.matplotlibwidget.draw() # required to update the window
        print("update took %.02f ms"%((time.time()-t1)*1000))
        if self.chkMore.isChecked():
            QtCore.QTimer.singleShot(10, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
```

This project is on GitHub: https://github.com/swharden/Python-GUI-examples/tree/master/2016-07-30_qt_matplotlib_sine_scroll