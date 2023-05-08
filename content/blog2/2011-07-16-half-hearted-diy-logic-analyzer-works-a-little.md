---
title: DIY State Machine
date: 2011-07-16 22:52:17
tags: ["microcontroller", "circuit", "obsolete"]
---



__While trying to attack the problem described in the previous entry,__ it became clear that a logic analyzer would be necessary.  I thought I'd try to build one, and my first attempt was so close to being successful, but not quite there.  It records 19 channels (the maximum pins available on the ATMega48 not being occupied by the status LED or USB connection pins) at a rate just under 1,000 samples per second. The USB connection to the PC is obvious, and it utilizes the V-USB project to bit-bang the USB protocol. I'm posting this in part because some of the comments to my entry two posts ago were disheartening, discouraging, and even down-right viscous!  I made a simple way to send numbers to a PC through the sound card, so what? Don't be nasty about it!  Meh, internet people.  Anyway, here's a marginally more proper way to send data to a PC with USB and an AVR (logging and interface designed in python), but I'll probably still get yelled at for it.

{{<youtube TEHF6b5bqj8>}}

__As you can see from the video__, it's good but not good enough. If I could get samples at 2,000 per second I'd probably be OK, but it's just not quite fast enough with it's current, ultra-simplistic method of sample recording. I'll figure out a fancier way to build a spectrum analyzer - it's obvious the platform is there, it just needs some refinement.

{{<youtube chyJ3Fw0mPc>}}

Images of the output:

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/16/diy-logic-analyzer-1.png)
![](https://swharden.com/static/2011/07/16/diy-logic-analyzer-2.png)

</div>

__UPDATE!__ The more I think about it, the more I think this might be just good enough to work!  Look at the stagger in those peaks near the top - that's probably the lines telling which character to display. Data between the peaks indicates the value to be provided, and I should have enough time to accurately measure that... Maybe this is good enough after all? I'll have to run some more tests tomorrow...

__Where's the code?__ It kills me to do this, but I need to withhold the chip side code. I'm working on an idiot's guide to USB connectivity with AVR microcontrollers, and I'd rather post the simplest-case code first, then share complicated stuff like this.  I'll post the python scripts:

```python

# LOGIC.PY - this script will log (or print) raw data from the USB device
from optparse import OptionParser
import time
import usb.core
import usb.util
import os

while True:
        print "nTrying to communicate with the Gator Keyer ...",
        dev = usb.core.find(find_all=True, idVendor=0x16c0, idProduct=0x5dc)
        if len(dev)==0: print "FAIL"
        dev=dev[0]
        dev.set_configuration()
        print "there it is!"
        break

def readVals():
    x=dev.ctrl_transfer(0xC0, 2, 2, 3, 4).tolist()
    return x

def toBinary(desc):
    bits=[]
    for i in range(7,-1,-1):
        if (2**i>desc):
            bits.append('0')
        else:
            bits.append('1')
            desc=desc-2**i
    return bits

def toStr(lists):
    raw=[]
    for port in lists: raw+=toBinary(port)
    return ''.join(raw)

### PROGRAM START ##################
live=False
#live=True
start=time.time()
if live==True:
    while True:
        a,b,c,d=readVals()
        if not a==123: continue #bad data
        elapsed=time.time()-start
        print "%.010f,%s"%(elapsed,toStr([b,c,d]))
else:
    times=0
    data=''
    f=open("out.txt",'a')
    while True:
        a,b,c,d=readVals()
        if not a==123: continue #bad data
        elapsed=time.time()-start
        data+="%.010f,%sn"%(elapsed,toStr([b,c,d]))
        times+=1
        if times%1000==999:
            print "%d readings / %.02f = %.02f /sec"%(times,elapsed,times/elapsed)
            f.write(data)
            data=""

```

```python

#logicGraph.py - this will show the data in a pretty way
import matplotlib.pyplot as plt
import numpy

c={
0:"",
1:"",
2:"blk sol",
3:"yel str",
4:"yel sol",
5:"pur sol",
6:"pur str",
7:"",
8:"",
9:"",
10:"blu sol",
11:"blu str",
12:"orn sol",
13:"orn str",
14:"pnk sol",
15:"pnk str",
16:"",
17:"",
18:"",
19:"",
20:"",
21:"",
22:"",
23:"",
24:"",
}

print "loading"
f=open("out.txt")
raw=f.readlines()
f.close()

print "crunching"
times=numpy.array([])
data=numpy.array([])
for line in raw:
    if len(line)<10: continue
    line=line.replace("n",'').split(',')
    times=numpy.append(times,float(line[0]))
    bits = []
    for bit in line[1]:
        if bit=="1":bits.append(1)
        else:bits.append(0)
    data=numpy.append(data,bits)

columns=24
rows=len(data)/columns
data=numpy.reshape(data,[rows,columns])
print "DONE processing",len(data),"linesnn"
print "plotting..."
plt.figure()
plt.grid()
for i in range(len(c.keys())):
    if c[i]=="": continue
    plt.plot(times,data[:,i]+i*1.1,'-',label=c[i])
plt.legend()
plt.show()
```