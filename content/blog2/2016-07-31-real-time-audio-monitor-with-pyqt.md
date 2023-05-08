---
title: Python Real-time Audio Frequency Monitor
date: 2016-07-31 15:21:11
tags: ["python", "obsolete"]
---



__A new project I'm working on requires real-time analysis of soundcard input data, and I made a minimal case example of how to do this in a cross-platform way using python 3, numpy, and PyQt.__ Previous posts compared performance of the [matplotlib widget](https://www.swharden.com/wp/2016-07-30-live-data-in-pyqt4-with-matplotlibwidget/) vs [PyQtGraph plotwidget](https://www.swharden.com/wp/2016-07-31-live-data-in-pyqt4-with-plotwidget/) and I've been working with [PyQtGraph](http://www.pyqtgraph.org/) ever since. For static figures matplotlib is wonderful, but for fast responsive applications I'm leaning toward PyQtGraph. The [full source for this project is on a github page](https://github.com/swharden/Python-GUI-examples/tree/master/2016-07-37_qt_audio_monitor), but here's a summary of the project.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/07/31/demo-1.gif)

</div>

{{<youtube lDS9rI0o6mM>}}

__I made the UI with QT Designer.__ The graphs are _QGraphicsView_ widgets promoted to a pyqtgraph_ PlotWidget_. I describe how to do this [in my previous post](https://www.swharden.com/wp/2016-07-31-live-data-in-pyqt4-with-plotwidget/). Here's the content of the primary program:

```python
from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))
                self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
            self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax,self.ear.data,
                            pen=pen,clear=True)
            pen=pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx[:500],self.ear.fft[:500],
                            pen=pen,clear=True)
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")

```

This project uses a gutted version of the SWHEar class which I still haven't released on githib yet. It will likely have its own project folder. For now, take this project with a grain of salt. The primary advantage of this class is that it makes it easy to use PyAudio to automatically detect input sound cards, channels, and sample rates which are likely to succeed without requiring the user to enter any information.

All files used for this project are [in a GitHub folder](https://github.com/swharden/Python-GUI-examples/tree/master/2016-07-37_qt_audio_monitor)

### Audio Visualizer Screenlet

2016-09-05: Okko adapted this project into a screenlet (cross platform) which also includes an installer for Windows: https://github.com/ninlith/audio-visualizer-screenlet

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/31/widget.png)

</div>