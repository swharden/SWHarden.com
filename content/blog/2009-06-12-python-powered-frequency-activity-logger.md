---
title: Python-Powered Frequency Activity Logger
date: 2009-06-12 17:42:32
---

# Python-Powered Frequency Activity Logger

__I'm often drawn toward projects involving data analysis with Python. __When I found out a fellow ham in Orlando was using his computer to stream a popular local repeater frequency over the internet I got excited because of the potential for generating data from the setup. Since this guy already has his radio connected to his PC's microphone jack, I figured I could write a Python app to check the microphone input to determine if anyone is using the frequency. By recording when people start and stop talking, I can create a log of frequency activity. Later I can write software to visualize this data. I'll talk about that in a later post. For now, here's how I used Python and a Linux box (Ubuntu, with the python-alsaaudio package installed) to generate such logs.

![](https://www.youtube.com/embed/wnqsv03hu3U)

__We can visualize this data__ using some more simple Python code. Long term it would be useful to visualize frequency activity similarly to [how I graphed computer usage at work over the last year](2009-05-20-graphing-computer-usage/) but for now since I don't have any large amount of data to work with. I'll just write cote to visualize a QSO (conversation) with respect to time. It should be self-explanatory. This data came from data points displayed in the video (provided at the end of this post too).

<div class="text-center">

[![](qsographpng_thumb.jpg)](qsographpng.png)

</div>

__And, of course, the code I used to generate the log files (seen running in video above):__ Briefly, this program checks the microphone many times every second to determine if its state has changed (talking/no talking) and records this data in a text file (which it updates every 10 seconds). Matplotlib can EASILY be used to graph data from such a text file.

```python
import alsaaudio, time, audioop, datetime
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(1)
inp.setrate(4000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(1)

squelch = False
lastLog = 0
dataToLog = ""

def logIt(nowSquelch):
 global dataToLog, lastLog
 timeNow = datetime.datetime.now()
 epoch = time.mktime(timeNow.timetuple())
 if nowSquelch==True: nowSquelch=1
 else: nowSquelch=0
 logLine="%s %dn"%(timeNow, nowSquelch)
 print timeNow, nowSquelch
 dataToLog+=logLine
 if epoch-lastLog&gt;10:
 #print "LOGGING..."
 f=open('squelch.txt','a')
 f.write(dataToLog)
 f.close()
 lastLog = epoch
 dataToLog=""

while True:
 l,data = inp.read()
 if l:
 vol = audioop.max(data,2)
 #print vol #USED FOR CALIBRATION
 if vol&gt;800: nowSquelch = True
 else: nowSquelch = False
 if not nowSquelch == squelch:
 logIt(nowSquelch)
 squelch = nowSquelch
 time.sleep(.01)

```

__To use this code__ make sure that you've properly calibrated it. See the "vol&gt;800" line? That means that if the volume in the microphone is at least 800, it's counted as talking, and less than it's silence. Hopefully you can find a value that counts as silence when the squelch is active, but as talking when the squelch is broken (even if there's silence). This is probably best achieved with the radio outputting at maximum volume. You'll have to run the program live with that line un-commented to view the data values live. Find which values occur for squelch on/off, and pick your threshold accordingly.

__After that you can visualize__ the data with the following code. Note that this is SEVERELY LIMITED and is only useful when graphing a few minutes of data. I don't have hours/days of data to work with right now, so I won't bother writing code to graph it. This code produced the graph seen earlier in this page. Make sure matplotlib is installed on your box.

```python
import pylab

def loadData():
 #returns Xs
 import time, datetime, pylab
 f=open('good.txt')
 raw=f.readlines()
 f.close()
 onTimes=[]
 timeStart=None
 lastOn=False
 for line in raw:
 if len(line)&lt;10: continue
 line = line.strip('n').split(" ")
 t=line[0]+" "+line[1]
 t=t.split('.')
 thisDay=time.strptime(t[0], "%Y-%m-%d %H:%M:%S")
 e=time.mktime(thisDay)+float("."+t[1])
 if timeStart==None: timeStart=e
 if line[-1]==1: stat=True
 else: stat=False
 if not lastOn and line[-1]=="1":
 lastOn=e
 else:
 onTimes.append([(lastOn-timeStart)/60.0,
 (e-timeStart)/60.0])
 lastOn=False
 return onTimes

times = loadData()
pylab.figure(figsize=(8,3))
for t in times:
 pylab.fill([t[0],t[0],t[1],t[1]],[0,1,1,0],'k',lw=0,alpha=.5)
pylab.axis([None,None,-3,4])
pylab.title("A little QSO")
pylab.xlabel("Time (minutes)")
pylab.show()
```