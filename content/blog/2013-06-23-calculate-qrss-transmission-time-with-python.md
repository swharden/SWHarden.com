---
title: Calculate QRSS Transmission Time with Python
date: 2013-06-23 21:19:59
tags: ["qrss", "python", "obsolete"]
---



__How long does a particular bit of Morse code take to transmit at a certain speed?__ This is a simple question, but when sitting down trying to design schemes for 10-minute-window QRSS, it doesn't always have a quick and simple answer. Yeah, you could sit down and draw the pattern on paper and add-up the dots and dashes, but why do on paper what you can do in code? The following speaks for itself. I made the top line say my call sign in Morse code (AJ4VD), and the program does the rest. I now see that it takes 570 seconds to transmit AJ4VD at QRSS 10 speed (ten second dots), giving me 30 seconds of free time to kill.


<div class="text-center">

![](https://swharden.com/static/2013/06/23/qrss-calclator.png)

</div>

Output of the following script, displaying info about "AJ4VD" (my call sign).

__Here's the Python code I whipped-up to generate the results:__

```python
xmit=" .- .--- ....- ...- -..  " #callsign
dot,dash,space,seq="_-","_---","_",""
for c in xmit:
    if c==" ": seq+=space
    elif c==".": seq+=dot
    elif c=="-": seq+=dash
print "QRSS sequence:n",seq,"n"
for sec in [1,3,5,10,20,30,60]:
    tot=len(seq)*sec
    print "QRSS %02d: %d sec (%.01f min)"%(sec,tot,tot/60.0)
```

__How ready am I to implement this in the microchip? __Pretty darn close. I've got a surprisingly stable software-based time keeping solution running continuously executing a "tick()" function thanks to hardware interrupts. It was made easy thanks to [Frank Zhao's AVR Timer Calculator](http://www.frank-zhao.com/cache/avrtimercalc.php). I could get it more exact by using a /1 prescaler instead of a /64, but this well within the range of acceptability so I'm calling it quits!


<div class="text-center img-border">

![](https://swharden.com/static/2013/06/23/photo-11.jpg)

</div>

Output frequency is 1.0000210 Hz. That'll drift 2.59 sec/day. I'm cool with that.