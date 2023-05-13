---
title: Reading PCM Audio with Python
date: 2009-06-19 09:08:33
tags: ["python", "obsolete"]
---



__When I figured this out__ I figured it was simply way too easy and way to helpful to keep to myself.  Here I post (for the benefit of friends, family, and random Googlers alike) two examples of super-simplistic ways to read [PCM](http://en.wikipedia.org/wiki/Pulse-code_modulation) data from Python using [Numpy](http://numpy.scipy.org/) to handle the data and [Matplotlib](http://matplotlib.sourceforge.net/) to display it.  First, get some junk audio in PCM format (test.pcm).

```python
import numpy
data = numpy.memmap("test.pcm", dtype='h', mode='r')
print "VALUES:",data
```

__This code prints the values of the PCM file.__ Output is similar to:

```
VALUES: [-115 -129 -130 ...,  -72  -72  -72]
```

__To graph this data, use matplotlib like so:__

```python
import numpy, pylab
data = numpy.memmap("test.pcm", dtype='h', mode='r')
print data
pylab.plot(data)
pylab.show()
```

__This will produce a graph that looks like this:__

<div class="text-center">

![](https://swharden.com/static/2009/06/19/audiograph.png)

</div>

__Could it have been ANY easier?__ I'm so in love with python I could cry right now.  With the powerful tools Numpy provides to rapidly and efficiently analyze large arrays (PCM potential values) combined with the easy-to-use graphing tools Matplotlib provides, I'd say you can get well on your way to analyzing PCM audio for your project in no time.  Good luck!

__FOR MORE INFORMATION AND CODE__ check out:
* [Linear Data Smoothing In Python](https://swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/)
* [Signal Filtering With Python](https://swharden.com/blog/2009-01-21-signal-filtering-with-python/)
* [Circuits Vs. Software](https://swharden.com/blog/2009-01-15-circuits-vs-software/)
* [DIY ECG](https://swharden.com/blog/category/diy-ecg-home-made-electrocardiogram/) of entries.

__Let's get fancy and use this concept to determine the number of seconds in a 1-minute PCM file in which a radio transmission occurs.__  I was given a 1-minute PCM file with a ~45 second transmission in the middle.  Here's the graph of the result of the code posted below it.  (Detailed descriptions are at the bottom)

<div class="text-center">

![](https://swharden.com/static/2009/06/19/secpermin.png)

</div>

__Figure description:__ The top trace (light blue) is the absolute value of the raw sound trace from the PCM file.  The solid black line is the average (per second) of the raw audio trace.  The horizontal dotted line represents the _threshold_, a value I selected.  If the average volume for a second is above the threshold, that second is considered as "transmission" (1), if it's below the threshold it's "silent" (0).  By graphing these 60 values in bar graph form (bottom window) we get a good idea of when the transmission starts and ends.  Note that the ENTIRE graphing steps are for demonstration purposes only, and all the math can be done in the 1st half of the code.  Graphing may be useful when determining the optimal threshold though.  Even when the radio is silent, the microphone is a little noisy.  The optimal threshold is one which would consider microphone noise as silent, but consider a silent radio transmission as a transmission.

```python
### THIS CODE DETERMINES THE NUMBER OF SECONDS OF TRANSMISSION
### FROM A 60 SECOND PCM FILE (MAKE SURE PCM IS 60 SEC LONG!)
import numpy
threshold=80 # set this to suit your audio levels
dataY=numpy.memmap("test.pcm", dtype='h', mode='r') #read PCM
dataY=dataY-numpy.average(dataY) #adjust the sound vertically the avg is at 0
dataY=numpy.absolute(dataY) #no negative values
valsPerSec=float(len(dataY)/60) #assume audio is 60 seconds long
dataX=numpy.arange(len(dataY))/(valsPerSec) #time axis from 0 to 60
secY,secX,secA=[],[],[]
for sec in xrange(60):
    secData=dataY[valsPerSec*sec:valsPerSec*(sec+1)]
    val=numpy.average(secData)
    secY.append(val)
    secX.append(sec)
    if val>threshold: secA.append(1)
    else: secA.append(0)
print "%d sec of 60 used = %0.02f"%(sum(secA),sum(secA)/60.0)
raw_input("press ENTER to graph this junk...")

### CODE FROM HERE IS ONLY USED TO GRAPH THE DATA
### IT MAY BE USEFUL FOR DETERMINING OPTIMAL THRESHOLD
import pylab
ax=pylab.subplot(211)
pylab.title("PCM Data Fitted to 60 Sec")
pylab.plot(dataX,dataY,'b',alpha=.5,label="sound")
pylab.axhline(threshold,color='k',ls=":",label="threshold")
pylab.plot(secX,secY,'k',label="average/sec",alpha=.5)
pylab.legend()
pylab.grid(alpha=.2)
pylab.axis([None,None,-1000,10000])
pylab.subplot(212,sharex=ax)
pylab.title("Activity (Yes/No) per Second")
pylab.grid(alpha=.2)
pylab.bar(secX,secA,width=1,linewidth=0,alpha=.8)
pylab.axis([None,None,-0.5,1.5])
pylab.show()
```

__The output of this code:__

```46 sec of 60 used = 0.77```