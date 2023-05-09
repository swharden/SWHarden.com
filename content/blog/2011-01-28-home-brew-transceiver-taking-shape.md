---
title: Home-Brew Transceiver Taking Shape!
date: 2011-01-28 14:13:33
tags: ["circuit", "microcontroller", "obsolete", "amateur radio"]
---



__In the spirit of furthering my knowledge of AC circuity,__ I'm trying to build a 100% homebrew transceiver.  Yeah, QRSS and ultra-weak signal, ultra-narrowband communications is still fun, but it's not the same thrill as actually engaging in real time communication with somebody!  My goal is a transmitter / receiver in a box. The basic features I desire are (1) multiple bands (at least 40m, 30m, 20m), (2) FULL-band coverage, (3) direct conversion receiver, (4) 10W transmitter, (5) digital frequency display, (6) common standard components (nothing mechanical, no air variable capacitors, everything must be easily obtainable on sites like Mouser and DigiKey), (7) SMT capability, (8) inexpensive ($20 is my goal, but that's a tough goal!). My designs are changing daily, so I'm not going to waste time posting schematics every time I write on this blog, but here are some photos and videos of the product in its current state.

{{<youtube LACpR1vIwWM>}}

{{<youtube Cq-lnMONUe4>}}

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/28/IMG_4994.jpg)
![](https://swharden.com/static/2011/01/28/IMG_5013.jpg)

</div>

{{<youtube B-klfgb125o>}}

(I just found that last video - it was one of my favorite songs as a teenager, performed live!)

__UPDATE:__ I got a cool dual 16-bit counter IC made by TI, a SN74LV8154N - very cheap, and can be configured as a 32-bit counter. It seemed like a better option than multiple 8-bit counters, and this chip is about $0.60 so if I can make it work I'll be happy! I breadboarded it up (see circuit diagram) and it seemed to work. I started wiring it on the perf board, but haven't written software for it yet...

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/28/IMG_5042.jpg)
![](https://swharden.com/static/2011/01/28/IMG_5039.jpg)
![](https://swharden.com/static/2011/01/28/IMG_5041.jpg)

</div>

__UPDATE__ - I just found this video on youtube I never posted on my blog, so this seems like an appropriate location for it:

{{<youtube w2MJQakqI0M>}}