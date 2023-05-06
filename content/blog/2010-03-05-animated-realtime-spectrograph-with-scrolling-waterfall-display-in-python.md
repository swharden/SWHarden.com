---
title: Animated Realtime Spectrograph with Scrolling Waterfall Display in Python
date: 2010-03-05 22:51:21
tags: ["python", "old"]
---

# Animated Realtime Spectrograph with Scrolling Waterfall Display in Python

__My project is coming along nicely.__ This isn't an incredibly robust spectrograph program, but it sure gets the job done quickly and easily. The code below will produce a real time scrolling spectrograph entirely with Python! It polls the microphone (or default recording device), should work on any OS, and can be adjusted for vertical resolution / FFT frequency discretion resolution. It has some simple functions for filtering (check out the de-trend filter!) and might serve as a good start to a spectrograph / frequency analysis project. It took my a long time to reach this point! I've worked with Python before, and dabbled with the Python Imaging Library (PIL), but this is my first experience with real time linear data analysis and high-demand multi-threading. I hope it helps you. Below are screenshots of the program (two running at the same time) listening to the same radio signals (mostly Morse code) with standard output and with the "de-trending filter" activated.

<div class="text-center img-border">

[![](spectrogram-scrollbars_thumb.jpg)](spectrogram-scrollbars.png)

</div>

<div class="text-center img-border img-small">

[![](nofilter_thumb.jpg)](nofilter.png)
[![](filter_thumb.jpg)](filter.png)

</div>

```python
import pyaudio
import scipy
import struct
import scipy.fftpack

from Tkinter import *
import threading
import time
import datetime
import wckgraph
import math

import Image
import ImageTk
from PIL import ImageOps
from PIL import ImageChops
import time
import random
import threading
import scipy

# ADJUST RESOLUTION OF VERTICAL FFT
bufferSize = 2**11
# bufferSize=2**8

# ADJUSTS AVERAGING SPEED NOT VERTICAL RESOLUTION
# REDUCE HERE IF YOUR PC CANT KEEP UP
sampleRate = 24000
# sampleRate=64000

p = pyaudio.PyAudio()
chunks = []
ffts = []


def stream():
    global chunks, inStream, bufferSize
    while True:
        chunks.append(inStream.read(bufferSize))


def record():
    global w, inStream, p, bufferSize
    inStream = p.open(format=pyaudio.paInt16, channels=1,
                      rate=sampleRate, input=True, frames_per_buffer=bufferSize)
    threading.Thread(target=stream).start()
    # stream()


def downSample(fftx, ffty, degree=10):
    x, y = [], []
    for i in range(len(ffty)/degree-1):
        x.append(fftx[i*degree+degree/2])
        y.append(sum(ffty[i*degree:(i+1)*degree])/degree)
    return [x, y]


def smoothWindow(fftx, ffty, degree=10):
    lx, ly = fftx[degree:-degree], []
    for i in range(degree, len(ffty)-degree):
        ly.append(sum(ffty[i-degree:i+degree]))
    return [lx, ly]


def smoothMemory(ffty, degree=3):
    global ffts
    ffts = ffts+[ffty]
    if len(ffts) < =degree:
        # ly.append(fft[i]-(ffty[i-degree]+ffty[i+degree])/2) return [lx,ly] def graph(): global chunks, bufferSize, fftx,ffty, w if len(chunks)>0:
        return ffty ffts = ffts[1:] return scipy.average(scipy.array(ffts), 0) def detrend(fftx, ffty, degree=10): lx, ly = fftx[degree:-degree], [] for i in range(degree, len(ffty)-degree): ly.append((ffty[i]-sum(ffty[i-degree:i+degree])/(degree*2)) * 2+128)
        data = chunks.pop(0)
        data = scipy.array(struct.unpack("%dB" % (bufferSize*2), data))
        ffty = scipy.fftpack.fft(data)
        fftx = scipy.fftpack.rfftfreq(bufferSize*2, 1.0/sampleRate)
        fftx = fftx[0:len(fftx)/4]
        ffty = abs(ffty[0:len(ffty)/2])/1000
        ffty1 = ffty[:len(ffty)/2]
        ffty2 = ffty[len(ffty)/2::]+2
        ffty2 = ffty2[::-1]
        ffty = ffty1+ffty2
        ffty = (scipy.log(ffty)-1)*120
        fftx, ffty = downSample(fftx, ffty, 2)
        updatePic(fftx, ffty)
        reloadPic()

    if len(chunks) > 20:
        print "falling behind...", len(chunks)


def go(x=None):
    global w, fftx, ffty
    print "STARTING!"
    threading.Thread(target=record).start()
    while True:
        # record()
        graph()


def updatePic(datax, data):
    global im, iwidth, iheight
    strip = Image.new("L", (1, iheight))
    if len(data) > iheight:
        data = data[:iheight-1]
    # print "MAX FREQ:",datax[-1]
    strip.putdata(data)
    # print "%03d, %03d" % (max(data[-100:]), min(data[-100:]))
    im.paste(strip, (iwidth-1, 0))
    im = im.offset(-1, 0)
    root.update()


def reloadPic():
    global im, lab
    lab.image = ImageTk.PhotoImage(im)
    lab.config(image=lab.image)


root = Tk()
im = Image.open('./ramp.tif')
im = im.convert("L")
iwidth, iheight = im.size
im = im.crop((0, 0, 500, 480))
# im=Image.new("L",(100,1024))
iwidth, iheight = im.size
root.geometry('%dx%d' % (iwidth, iheight))
lab = Label(root)
lab.place(x=0, y=0, width=iwidth, height=iheight)
go()
```

__UPDATE: I'm not going to post the code for this yet__ (it's very messy) but I got this thing to display a spectrograph on a canvas. What's the advantage of that? Huge, massive spectrographs (thousands of pixels in all directions) can now be browsed in real time using scrollbars, and when you scroll it doesn't stop recording, and you don't lose any data! Super cool.