---
title: Live Data in PyQt4 with PlotWidget
date: 2016-07-31 07:28:28
tags: ["python", "old"]
---

# Live Data in PyQt4 with PlotWidget

__After spending a day comparing performance of MatplotlibWidget with PlotWidget, when it comes to speed PlotWidget wins by a mile!__ Glance over my [last post](https://www.swharden.com/wp/2016-07-30-live-data-in-pyqt4-with-matplotlibwidget/) where I describe how to set up the window with QT Designer and convert the .ui file to a .py file. With only a few changes to the code, I swapped the matplotlib _MatplotlibWidget _with the pyqtgraph _PlotWidget_. I easily got a 20x increase in speed (frame rate), and I'm likely to favor [PyQtGraph](http://www.pyqtgraph.org/) over matpltolib for python applications involving realtime display of data. Just like the [previous example using matplotlib](https://www.swharden.com/wp/2016-07-30-live-data-in-pyqt4-with-matplotlibwidget/), this one uses the system time to control the phase and color of a sine wave in real time. You can grab the full code from [my github folder](https://github.com/swharden/Python-GUI-examples/tree/master/2016-07-31_qt_PyQtGraph_sine_scroll).

<div class="text-center img-border img-small">

![](demo2.gif)
[![](demo2cmd_thumb.jpg)](demo2cmd.png)

</div>

__When designing the GUI with QT Designer, add a QGraphicsView widget then assign it to become a PyQtGraph object.__ To do this, follow the steps found on the [pyqtgraph docs page](http://www.pyqtgraph.org/documentation/how_to_use.html#embedding-widgets-inside-pyqt-applications):

* In Designer, create a QGraphicsView widget
* Right-click on the QGraphicsView and select “Promote To...”
* Set “Promoted class name” to “PlotWidget”
* Under “Header file”, enter “pyqtgraph”
* Click “Add”, then click “Promote”
* _apparently this only needs to be done once per project_

<div class="text-center img-border">

[![](promoted_thumb.jpg)](promoted.png)

</div>

__In addition to faster frame rate, the PyQtGraph method is easy to interact with.__ Clicking and dragging scrolls the data, and right-clicking and dragging zooms on each axis. Here's the program code:

```python
from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pylab
import time
import pyqtgraph

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.update)
        self.grPlot.plotItem.showGrid(True, True, 0.7)

    def update(self):
        t1=time.clock()
        points=100 #number of data points
        X=np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=pyqtgraph.hsvColor(time.time()/5%1,alpha=.5)
        pen=pyqtgraph.mkPen(color=C,width=10)
        self.grPlot.plot(X,Y,pen=pen,clear=True)
        print("update took %.02f ms"%((time.clock()-t1)*1000))
        if self.chkMore.isChecked():
            QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
```

This project is available on GitHub: https://github.com/swharden/Python-GUI-examples/tree/master/2016-07-31_qt_PyQtGraph_sine_scroll