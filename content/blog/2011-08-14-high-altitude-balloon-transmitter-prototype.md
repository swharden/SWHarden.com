---
title: High Altitude Balloon Transmitter Prototype
date: 2011-08-14 18:42:59
tags: ["amateur radio", "circuit", "old"]
---

# High Altitude Balloon Transmitter Prototype

__It's been my goal for quite some time__ to design a simple, easy-to-replicate transmitter for high altitude balloon telemetry transmission. I'm quite satisfied by what I came up with because it's very simple, cheap, easy to code for, and easy to change frequency.  I'd say the most common alternative is a handheld amateur radio transmitter which starts around $60, requires an amateur radio license, and typically output 5W of FM on 144MHz (2m) or 440MHz (70cm). Fancier handheld radios are capable of transmitting [APRS](http://en.wikipedia.org/wiki/Automatic_Packet_Reporting_System) packets, and use established base station repeaters to listen to these frequencies, decode the packets, and update an internet database about current location information. Although it's quite fancy, elegant, and technical (and expensive), I desire a much simpler, cheaper, disposable option! If my balloon lands in the Atlantic ocean, I don't want to be out $100+ of radio equipment! This alternative is about $7.

<div class="text-center img-border">

[![](https://swharden.com/static/2011/08/14/DSCN1718_thumb.jpg)](https://swharden.com/static/2011/08/14/DSCN1718.jpg)

</div>

__Here's my solution.__ I don't normally build things on perf-board (I prefer sloppy Manhattan construction), but since this might go near the edge of space and be jerked around in turbulent winds, I figured it would be a nice and strong way to assemble it.  Anyhow, it uses a can crystal oscillator as the frequency source. These things are pretty cool, because they're very frequency stable, even with changing temperatures.

<div class="text-center img-border">

[![](https://swharden.com/static/2011/08/14/DSCN1701_thumb.jpg)](https://swharden.com/static/2011/08/14/DSCN1701.jpg)

</div>

__The can oscillator (28.704MHz, selected to be in a rarely-used region of the 10m amatuer radio allocation which I'm licensed to use, call sign AJ4VD) outputs 5V square waves which I use to drive two successive class C amplifiers.__ The signal can be shunted to ground between the two stages by a third "control" transistor, which allows micro-controller control over the final amplifier. Although it may have seemed logical to simply supply/cut power from the oscillator to key the transmitter, I decided against it because that can oscillator takes 20ms to stabilize, and I didn't think that was fast enough for some encoding methods I wish to employ!

<div class="text-center img-border">

[![](https://swharden.com/static/2011/08/14/DSCN1717_thumb.jpg)](https://swharden.com/static/2011/08/14/DSCN1717.jpg)

</div>

__Although during my tests I power the device from my bench-top power supply__ (just a few LM3805 and LM3812 regulators in a fancy case), it's designed to be run off 3xAAA batteries (for logic) and a 9V battery (for the transmitter). I could have probably used a regulator to drop the 9V to 5V for the MCU and eliminated some extra weight, but I wonder how low the 9V will dip when I draw a heavy RF load? The 3xAAAs seemed like a sure bet, but quite at the expense of weight. I should consider the regulator option further... [ponders]

![](https://www.youtube.com/embed/rRatJBAMgdg)

__There's the device in action while it was in a breadboard.__ I've since wired it up in a perf board (pictured) and left it to transmit into a small string of wire inside my apartment as an antenna as I went to the UF Gator Amateur Radio Club (a few miles away) and tried to tune into it. It produced a stunningly beautiful signal! I can't wait for its first test on a high altitude balloon!  Here it's transmitting CW Morse code the words "scott rocks", separated by appropriate call sign identification every 10 minutes, AJ4VD, my amateur radio license... of course!

* [cw.mp3](http://www.SWHarden.com/blog/images/cw.mp3)

* [usb.mp3](http://www.SWHarden.com/blog/images/usb.mp3)

__Above is what the audio sounded like__ with a narrow CW filter (awesome, right?), and a 3KHz wide USB configuration. I think this should be more than enough to carry us through a mission, and aid in direction finding of a landed payload!

__Notes about filtering:__ The output of this transmitter is quite harmonic-rich. The oscillator produces square waves for goodness' sake! The class C amplifier smooths a bit of that out, but you still need some low-pass filtering, not shown on the schematic. I think for my purposes a 3-pole [Chebyshev filter](http://en.wikipedia.org/wiki/Chebyshev_filter) will suffice, but just keep this in mind in case you replicate my design. You certainly don't want to be transmitting out of band! Below is the output of the transmitter viewed on my scope. It's suspiciously smooth, which leads me to wonder about the accuracy of my scope! I really should get a spectrum analyzer.

<div class="text-center img-border">

[![](https://swharden.com/static/2011/08/14/DSCN1707_thumb.jpg)](https://swharden.com/static/2011/08/14/DSCN1707.jpg)

</div>