---
title: 40m Junkbox QRP Transmitter
date: 2011-01-10 09:01:20
tags: ["qrss", "amateur radio", "circuit", "obsolete"]
---



__I decided to sit down and build something last night__, and I'm surprised by how functional it is!  Nothing about it is extraordinarily complex, and it's extremely flexible, accommodating almost any crystal you want to drop in.  Although I doubt I'll use this exact design for a permanent transmitter, it was fun to build and I'll post photos hoping to inspire others to tinker with RF circuitry as well! The final device worked on 7.000MHz and had 3 components: power supply, oscillator/amplifier (making 20mW), and amplifier (making 1.5W). 

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4916.jpg)

</div>

__First, I needed an oscillator.__ I had an easy source of one because I had a pile of ATTiny25 microcontrollers.  Often I run a microcontroller at my transmit frequency with a crystal (applied to XTAL1 and XTAL2 pins) and collect the convenient 5V square wave on the CKOUT pin (after the appropriate fuse setting is applied).  However, although the ATTiny25 has both XTAL and CKOUT pins, they overlap! This means that CKOUT cannot be obtained when using a crystal. This complicates things slightly... 

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4906.jpg)

</div>

__I ended-up getting a nice sine wave from the XTAL1 pin__, although it was less than 1PPV.  I tried having this signal directly switch an N-channel MOSFET as an amplifier, but it didn't work that well (a transformer might help increase PPV, but that complicates things).  I instead used a 74HC240 (8 inverting buffers on one chip) to help boost the signal. However, 1PPV wasn't enough to get the buffer oscillating.  I therefore added a 2 resisters and a capacitor to the first inverting output, such that a persistent low would slowly raise the voltage of a wire, and I attached that wire to the input of the buffer chip.  This way, although 1ppv wasn't enough to start oscillations, a few milliseconds of time allowed the inverting output (high when the input is low) to raise voltage of the input until it was enough to fire the buffers.  Once it starts, it starts!  I'm trilled, because a voltage divider or a potentiometer would have been a pain, and required specific parts. 

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4908.jpg)

</div>

__The result is about 20mW of power with no tuned circuit!__ This means it will work on pretty much any crystal you can pop in the micro-controller. This may be suitable for a QRSS transmitter, and since we're not pushing any of the components very little heat is produced, should it should be thermostable and easy to regulate.  Modulation is achieved by a reverse-biased LED varactor diode varying crystal capacitance to ground, discussed elsewhere on my site so I won't go there again. 

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4910.jpg)

</div>

__Power supply__ is one I built a while back and had available.  5V for the microcontroller, and 12V for the amplifier.  Simple!

__Amplifying the signal was pretty easy as well.__ The 5V signal output of the buffer goes from 0V to 5V, which was enough to trigger an IRF510 N-channel MOSFET with a convenient packaging that I screwed into a huge heatsink. I push the MOSFET a lot, and a lot of heat is produced, but as long as I keep it separate from the oscillator the heat shouldn't affect frequency too much. Although on my workbench I use exposed wires connecting components, this is prone to getting RFI so obviously use shielded cable of some sort, or use extremely short leads. The MOSFET is arranged as a class C amplifier, with a RFC inductor at the drain.

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4911.jpg)

</div>

__In retrospect__ I'm doubting that 5V is enough to fully activate the IRF510. I should probably use some method to bring voltage just below firing threshold, so the 5V can more fully open the gate. I'll try that later!  The output is filtered with a PI lowpass filter. I use two 1nF capacitors and a coil which I wind until the output on the scope looks acceptable.  I know there are more exacting ways.  Anyhow, I had fun, so I thought I'd post. I'm just tinkering at this point!

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/IMG_4917.jpg)

</div>

It's putting out about a watt and a half into 50 ohms. How cool? Adding a code key is trivial, as the 74hc240 has "gate enable" pins for easy on/off control - even from a microcontroller! Food for thought... 73!

`` UPDATE `` - I decided to slap a 10.140MHz (QRSS window) crystal in there and see what happened. I saw my signal locally (AJ4VD/W4DFU grabber), but not elsewhere, so I left it up for about a day. [Vince Adams, N9VN](https://swharden.com/static/2011/01/10/) spotted it in IL (about 1,000 miles away) and made a post on a mailing list asking who it was. Awesome! Note that for QRSS I used a lower-current power supply, so I don't actually know what power output was, but I'd estimate it to be about 500mW.

<div class="text-center img-border">

![](https://swharden.com/static/2011/01/10/n9vn.jpg)

</div>

(It's the "V-shape" at the bottom)