---
title: Frequency Counter Hacked to add USB Functionality
date: 2011-07-11 17:02:33
tags: ["amateur radio", "qrss", "circuit", "microcontroller", "old"]
---

# Frequency Counter Hacked to add USB Functionality

This is a multi-part blog entry added over 2 days of time documenting the progress of the addition of USB to a simple frequency counter. The final result lets me graph frequency over time on the computer, automatically, over days of time if desired. I'm quite pleased at the result, especially considering so little circuitry was required! 

__It looks like this will be a multi-part blog entry.__ I'm in the process of figuring out how to add USB functionality to this simple device, which will be a fun way for me to express my creativity and think a bit outside the box while gaining some simple electrical engineering experience! Here's the jist of what I'm planning...

{{<youtube L5ZWWcXklHs>}}

__After a brief trip__ to Orlando to visit family, I decided to stop by the house of one of my neighbors who worked at the same small engineering company I did when I was first starting college (about the time I decided to peruse biology rather than engineering).  I hadn't seen him in a while and we talked about various electronics things (he's working on an impressive project currently), and before I left he offered me a brown box. "Do you have any use for a function generator?" I got excited and said "sure!" On closer inspection, it was actually a frequency counter, and he said "oh well I don't need one of those anyway" and gave it to me. I was ecstatic! Between [this post](http://www.swharden.com/blog/2011-01-28-home-brew-transceiver-taking-shape/), [this post](http://www.swharden.com/blog/2011-02-04-frequency-counter-working/), [this post](http://www.swharden.com/blog/2011-02-09-minimal-radio-project-continues/), [this post](http://www.swharden.com/blog/2011-02-12-wideband-receiver-works/), and [this final project post](http://www.swharden.com/blog/2011-03-14-frequency-counter-finished/) you can tell that building a frequency counter was really important to me, and that I was never truly satisfied with the result - it wasn't stable to the Hz! I'm excited to finally have a real counter at my workstation. (It's an instek GFC-8010H, 1-120 MHz range.) Now onto figuring out how to build a spectrum analyzer... X_x

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/after1.jpg)

</div>

### Update (2 days later)

__I never can leave things alone can I?__ While basking in happiness over this new acquisition I pondered how easy it would be to interface this to a PC. I would like to graph frequency drift over time directly (not using a radio receiver outputting audio which I graph, since the radio is sensitive to drift). Plus this counter allows sample sizes of 10 seconds! That's some serious resolution (compared to what I'm used to at least).  First step to PC interfacing is to see what I've got to work with. I unscrewed the box and snapped some photos of the surprisingly simple device... I can't believe [this costs over $175 (as listed on Amazon.com)](http://www.amazon.com/Instek-GFC8010H-Frequency-Counter/dp/B000I3VS0A) - it's so simple!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1540.jpg)

</div>

__I guess it all makes sense.__ AC transformer and rectifier diodes with a smoothing capacitor on the bottom left, fed into a 7805 linear voltage regulator, no doubt powering the micro-controller (big IC), logic buffer (small IC), and whatever analog circuitry is under the panel.

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1541.jpg)

</div>

__I'm not going to lift the panel__ because it's obvious what's under there. Likely some high gain, high distortion amplifier stages to provide a lot of buffering, eventually the input shape is fed to the chip for counting.

__After posting and thinking about it,__ the curiosity got to me! I lifted the panel and this is what I found...

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1552.jpg)

</div>

__There's our buffer and wave shaper!__ The [full datasheet](http://www.onsemi.com/pub_link/Collateral/MC10H116-D.PDF) shows it's a (triple) line driver.

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1544.jpg)

</div>

__Come to think of it,__ I'm not entirely sure about that smaller IC.  It's a 74HC00N, quad NAND gate. Knee-jerk was to say it was used for dividing-down the frequency, but that's silly since it takes 2 NAND gates to make a flip flop, and that chip would be only 2 flip flops (/4), and there are flip flip chips for all that.  Perhaps this has something to do with the buttons on the front panel? Perhaps something to do with square-shaping the oscillator with the 10mhz crystal? The big GFC 9701-1 IC seems to be a custom counter chip used in many Instek products. Here's a blurb from a page of their manual for a function generator they make:

>  The most important function of the internal counter is to show the main frequency on the display. So we take a square signal from the square shaper and change the level to TTL compatible level with a TTL shaper block (is this the role of that NAND gate?) then the signal will connect with the counter GFC-9701. Because the counter directly connects with the MPU system, the MPU can get correct frequency and show it on the display.
__So, it seems__ that chip is already outputting data ready to go into a CPU. I wonder if it's outputting some type of data on an unused pin, ripe for the picking? I can't find more ICs in this device, so it's possible no other MCU is driving the display, and this counter IC is doing that all on its own. Bah, again curiosity is getting the best of me... [unscrews front panel]

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1560.jpg)

</div>

__More ICs!__ I couldn't see them well before so I'm glad I opened up the display. The ULN2003A is a 7 channel darlington array, x2 = 14 darlingtons. The CD4511 is a common 7-segment driver - BINGO! If I'm going to interface this device by intercepting the display, this is the way to do it!  The darlingtons tell me which character is selected, and the input of this chip tells me the value to be displayed. Pow!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/xray_circuit.jpg)

</div>

__Let's take a closer look at that main chip again...__ X-RAY VISION TIME! I used Image-J to extract the red channel of the image and increased contrast, inverted, then used a 10 pixel wide unsharp mask with 0.8 weight to bring-out the leads. I guess I could have just unscrewed it and looked at the bottom, but where's the fun in that? I imagine the top left pin is input of frequency. The bottom left pins go to buttons on the front, so they're for front panel input. The headers on the right go to the front panel display. The pin going to the smaller IC must be the clock input, so that NAND gate DOES do something with shaping the input clock signal. On the top fight of the image you can see the crystal connecting to that gate. The trace going in the center of the chip on top is probably +5V supply for the chip. I'm not sure about much else, and I don't feel like poking around with a continuity meter right now. UPDATE - I tested each pin with an analog o-scope. I found that pin 6 (unconnected) outputs a burst of data every time the display updates - this is my data line! If I had a logic analyzer I'd know how to read it... BAH!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1547.jpg)

</div>

__What's this?!__ The voltage regulator with its hefty heat sink (which obviously gets quite warm) is attached to a 10.000 MHz crystal!  Is this the time base crystal? Doesn't accuracy depend on thermostability of this crystal? It's not just near it - it's physically connected with it through metal! Does this imply that a loaded 7805 voltage regulator produces heat more steadily, and with a final temperature more stable than room air in a plastic enclosure??

__update:__ The following was emailed to me in response to this puzzling issue. It's from my good friend Bill!

>  _It may be an SC-cut crystal which is the best type for precision oscillators because the turn around inflection occurs at a much broader temperature range than the regular AT-cut, el cheapo types we often use. SC types, if carefully selected, can remain within a fraction of a ppm over a temperature range to 10 to 20 C. The turn around point temperature is pretty high, about 90 C, compared to around 25C for the at-cut. So, my guess is that the 7805 provides this really high temperature to the xtal and can be trusted to not vary by more than a few degrees, particularly in a laboratory environment._ --Bill (W4HBK)
_Afterthought: This would make one hell of a huff-and-puff oscillator!_

## PROJECT COMPLETED!

__I'm quite excited__, the end product works wonderfully! It looks pretty spiffy too!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/DSCN1580.jpg)
![](https://swharden.com/static/2011/07/11/DSCN1605.jpg)
![](https://swharden.com/static/2011/07/11/DSCN1609.jpg)

</div>

__Here's some video__ showing the device at work!

{{<youtube c6uFN52LGnc>}}

Of course Python and MatPlotLib can graph it:

<div class="text-center">

![](https://swharden.com/static/2011/07/11/usb-frequency-counter-hack2.png)

</div>

... but so can Excel!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/11/usb-frequency-counter-hack.png)

</div>

__UPDATE__ Oops, I forgot to remove the trailing zero. That's 9.9 MHz, not 99 MHz.  That's easy enough to do later, so I'm not going to fix it and re-post updated images. Don't email me about it, I know ^_^

__UPDATE 2__ Here's some useful data! I hooked up a canned oscillator at 3.57 something MHz (very stable) and watched it as my frequency counter warmed up. The result showed that the counter takes about 2 hours to warm up!!! he shift is only about 15 Hz over 2 hours, but still it's good to know.

<div class="text-center">

![](https://swharden.com/static/2011/07/11/warmup1.png)

</div>

Once it's warm, it's stable!

<div class="text-center">

![](https://swharden.com/static/2011/07/11/warm.png)

</div>

## Schematic

This device is very simple and specialized for my use and I have not designed a custom schematic. USB functionality is as recommended by V-USB, similar to:

<div class="text-center">

![](https://swharden.com/static/2011/07/11/circuit-zoomed.gif)

</div>

For more information on the USB circuitry, view the [hardware considerations page](http://vusb.wikidot.com/hardware) relating to the [V-USB project](http://www.obdev.at/products/vusb/index.html).

## CODE

__Microcontroller code - __ Although it's hard for me, I really don't think I can release this right now. I'm working on an idiot's guide to USB connectivity with ATMEL microcontrollers, and it would cause quite a stir to post that code too early. It'll be shared soon! Here are the python scripts for the logging and for the graphing:

```python

#This code polls the USB device and displays/logs frequency
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

def readVals(c):
    x=dev.ctrl_transfer(0xC0, 3, c,4,4).tolist()
    val=x[0]
    if val>9: val=0
    return val

def readDisp():
    c=[]
    for i in range(1,9):
        val=readVals(i)
        c.append(val)
        #print "char",i,"=",val
    disp="%d%d%d%d%d%d%d%d"%(c[0],c[1],c[2],c[5],c[6],c[3],c[4],c[7])
    return disp

def readFreq():
    i=0
    first=readDisp()
    while True:
        if first==readDisp():
            i+=1
            if i==5: break #we're good!
        else: #FAIL! start over...
            i=0
            first=readDisp()
    return first

### PROGRAM START ##################

start=time.time()
while True:
    line="%.02f,%s"%(time.time()-start,readFreq())
    print line
    f=open("freq.csv",'a')
    f.write(line+"n")
    f.close()
    time.sleep(1)

```

```python

#This code reads the log file and graphs it with matplotlib
import matplotlib.pyplot as plt
import numpy

print "loading"
f=open("freq.csv")
raw=f.readlines()
f.close()

print raw

print "crunching"
times=numpy.array([])
data=numpy.array([])
for line in raw:
    if len(line)<10: continue
    line=line.replace("n",'').split(',')
    times=numpy.append(times,float(line[0]))
    data=numpy.append(data,float(line[1]))

#data=data/1000000.0
print times, data
print "DONE processing",len(data),"linesnn"
print "plotting..."
plt.figure()
plt.grid()
plt.plot(times,data,'-')
plt.plot(times,data,'.')
plt.show()

```
