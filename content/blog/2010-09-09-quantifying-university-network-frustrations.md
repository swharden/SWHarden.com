---
title: Quantifying University Network Frustrations
date: 2010-09-09 08:06:39
tags: ["python", "old"]
---

# Quantifying University Network Frustrations

__I'm sitting in class frustrated as could be.__ The Internet in this room is unbelievably annoying.  For some reason, everything runs fine, then functionality drops to unusable levels.  Downloading files (i.e., PDFs of lectures) occurs at about 0.5kb/s (wow), and Internet browsing is hopeless.  At most, I can connect to IRC and enjoy myself in #electronics, #python, and #linux. I decided to channel my frustration into productivity, and wrote a quick Python script to let me visualize the problem.

<div class="text-center img-medium">

[![](https://swharden.com/static/2010/09/09/out_thumb.jpg)](https://swharden.com/static/2010/09/09/out.png)

</div>

__Notice the massive lag spikes__ around the time class begins. I think it's caused by the retarded behavior of windows update and anti-virus software updates being downloaded on a gazillion computers all at the same time which are required to connect to the network on Windows machines. Class start times were 8:30am, 9:35am, and 10:40am.  Let's view it on a logarithmic scale:

<div class="text-center img-medium">

[![](https://swharden.com/static/2010/09/09/out2_thumb.jpg)](https://swharden.com/static/2010/09/09/out2.png)

</div>

__Finally, the code.__ It's two scripts:

This script pings a website (kernel.org) every few seconds and records the ping time to "pings.txt":

```python
import socket
import time
import os
import sys
import re


def getping():
    pingaling = os.popen("ping -q -c2 kernel.org")
    sys.stdout.flush()
    while 1:
        line = pingaling.readline()
        if not line:
            break
        line = line.split("n")
        for part in line:
            if "rtt" in part:
                part = part.split(" = ")[1]
                part = part.split('/')[1]
                print part+"ms"
                return part


def add2log(stuff):
    f = open("pings.txt", 'a')
    f.write(stuff+",")
    f.close()


while 1:
    print "pinging...",
    stuff = "[%s,%s]" % (time.time(), getping())
    print stuff
    add2log(stuff)
    time.sleep(1)
```

This script graphs the results:

```python
import pylab
import time
import datetime
import numpy


def smoothTriangle(data, degree, dropVals=False):
    triangle = numpy.array(range(degree)+[degree]+range(degree)[::-1])+1
    smoothed = []
    for i in range(degree, len(data)-degree*2):
        point = data[i:i+len(triangle)]*triangle
        smoothed.append(sum(point)/sum(triangle))
    if dropVals:
        print "smoothlen:", len(smoothed)
        return smoothed
    while len(smoothed) < len(data):
        smoothed = [None]+smoothed+[None]
    if len(smoothed) > len(data):
        smoothed.pop(-1)
    return smoothed


print "reading"
f = open("pings.txt")
raw = eval("[%s]" % f.read())
f.close()

xs, ys, big = [], [], []
for item in raw:
    t = datetime.datetime.fromtimestamp(item[0])
    maxping = 20000
    if item[1] > maxping or item[1] == None:
        item[1] = maxping
        big.append(t)
    ys.append(float(item[1]))
    xs.append(t)

print "plotting"
fig = pylab.figure(figsize=(10, 7))
pylab.plot(xs, ys, 'k.', alpha=.1)
pylab.plot(xs, ys, 'k-', alpha=.1)
pylab.plot(xs, smoothTriangle(ys, 15), 'b-')
pylab.grid(alpha=.3)
pylab.axis([None, None, None, 2000])
pylab.ylabel("latency (ping kernel.org, ms)")
pylab.title("D3-3 Network Responsiveness")
fig.autofmt_xdate()
pylab.savefig('out.png')
pylab.semilogy()
pylab.savefig('out2.png')
fig.autofmt_xdate()
print "done"
```