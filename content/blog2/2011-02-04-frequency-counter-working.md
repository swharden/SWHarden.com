---
title: Frequency Counter Working!
date: 2011-02-04 21:26:26
tags: ["microcontroller", "circuit", "old"]
---

# Frequency Counter Working!

__I'm ecstatic!__ Finally I built something that worked the first time.  Well... on the 3rd attempt! The goal was to develop a minimal-cost, minimal complexity frequency counter suitable for amateur radio. Although I think I can still cut cost by eliminating components and downgrading the microcontroller, I'm happy with my first working prototype.

{{<youtube heIkWcM9n0Q>}}

{{<youtube EVZcyYnUipQ>}}

__I haven't tested it rigorously __ with anything other than square waves, but I imagine that anything over 1PPV is sufficient (the input is through a bypass capacitor, internally biased right at the trigger threshold).  Counting is accomplished by a 74LV8154N  (dual 16-bit counter configured as 32-bit) which displays the count as four selectable bytes presented on 8 parallel pins. The heart of the device is an ATMega16 which handles [multiplexing of the display](http://en.wikipedia.org/wiki/Multiplexed_display) and has a continuously-running 16-bit timer which, upon overflowing, triggers a reset of the counter and measurement of the output.  Software isn't perfect (you can see the timing isn't accurate) but I imagine its inaccuracy can be measured and is a function of frequency such that it can be corrected via software.  Here are some photos...

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/04/IMG_5209.jpg)
![](https://swharden.com/static/2011/02/04/IMG_5222.jpg)
![](https://swharden.com/static/2011/02/04/IMG_5221.jpg)

</div>

__A PCB is DESPERATELY needed.__ I'll probably make one soon. Once it's a PCB, the components are pretty much drop-in and go! No wires! It'll be a breeze to assemble in 5 minutes. I wonder if it would make a fun kit? It would run on a 9V battery of course, but a calculator-like LCD (rather than LED) display would be ultra-low-current and might make a good counter for field operation (3xAAA batteries would last for months!)

_UPDATE: I found out that the ATMega16 donation was from my friend Obulpathi, a fellow Gator Amateur Radio Club member! He also gave me a pair of ATMega32 chips. Thanks Obul!_