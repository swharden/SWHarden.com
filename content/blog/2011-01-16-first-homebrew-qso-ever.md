---
title: First Homebrew QSO Ever!
date: 2011-01-16 18:39:32
tags: ["amateur radio", "circuit", "old"]
---

# First Homebrew QSO Ever!

__Today is a very special day,__ as it's the day I first made a contact with a radio transmitter I built completely on my own! The plans were copied from no where (although the concepts were obviously learned elsewhere), so it's somewhat of a unique design (likely because it's not very good!). I'll be the first to admit there is MUCH room for improvement, but my goal was to design and build a multi-band transmitter which would produce RF (not necessarily efficiently) at multiple bands by dropping in crystals of different frequencies.

![](https://www.youtube.com/embed/u4nI0cwSP0Q)

__My first QSO was with Bob, KC8MFF in West Virginia at 5pm today on 7MHz.__ He heard me calling CQ and replied! He gave me a 559 which made my happy. I was sending about 8 watts at the time into a Mosley Pro 67 Yagi at 180FT and receiving from a 40m dipole at 150FT at the W4DFU Gator Amateur Radio Club station in Gainesville, FL.  Although he's was about 650 miles away, I hope to make a more significant contact as the band opens up later tonight. It's such an exciting feeling! The aluminum plate gets very hot (even with the fan) and there's a slight smell of smoke whenever I transmit, but it adds to the fun I guess!  Here's some information about the build, though I'm confident it's less than optimal.

<div class="text-center img-border">

[![](https://swharden.com/static/2011/01/16/IMG_4946_thumb.jpg)](https://swharden.com/static/2011/01/16/IMG_4946.jpg)

</div>

__I'll preface this by stating__ that my goal was to produce an _experimental platform_ which I could use to _investigate_ construction techniques of small moderate-power transmitters. This is by no means a finished product! Much work (and some math) must be done to calculate the best number of turns on each coil for each band, including the RF choke on the power (resulting in class C amplifier behavior), the RF transformer, and the inductor/capacitor values of the low pass filter - all of which were determined empirically (watching output on an oscilloscope while adding/removing turns on a toroid). At 10W, it's not QRP, but it's easy to tone down to QRP (5W levels). 

<div class="text-center">

[![](https://swharden.com/static/2011/01/16/30m_40m_80m_transmitter_10watt_aj4vd_thumb.jpg)](https://swharden.com/static/2011/01/16/30m_40m_80m_transmitter_10watt_aj4vd.jpg)

</div>

One of my desires was to create a transmitter which could be built at minimal cost (total value of this is probably about $10). The microcontroller (ATTiny2313) was what I had on hand ($2), the buffer chip acts as a small amplifier ($0.50), and the power amplifiers are IRF510 MOSFETs ($1). The rest of the components are junkbox, and their values aren't really significant! The power supply is a 19V 3.6A power supply from an old laptop - small, convenient, awesome! Hopefully with some tweaking I'll have a nice transmitter which I'm proud to share and have replicated...

<div class="text-center img-border">

[![](https://swharden.com/static/2011/01/16/IMG_4928_thumb.jpg)](https://swharden.com/static/2011/01/16/IMG_4928.jpg)

</div>

__The overall schematic__ represents a crystal clocking a microcontroller at the transmit frequency, where the CKOUT fuse has been set, producing 5PPV square waves. These trigger an inverting buffer which (a) amplifies the current of the signal and (b) provides an easy source of inverted signal. The two (inverse) signals then fire a pair of IRF510s in tandem, each acting as a Class C amplifier producing about 60PPV waves (not quite as square-ish). The output is low-pass filtered with a Pi filter (3 pole Chebyschev), then sent to an antenna. Nothing special has been done to match the output to the antenna, so SWR with a 50ohm load is currently a bit high, but I imagine a variable capacitor on the output LPF would give me something to adjust to improve this. I should probably go back to square 1 and re-do the math from start to finish and follow my impedance values more closely.

<div class="text-center img-border">

[![](https://swharden.com/static/2011/01/16/IMG_4939_thumb.jpg)](https://swharden.com/static/2011/01/16/IMG_4939.jpg)

</div>

__Future work will be invested into__ adding an iambic keyer property to the microcontroller, as well as a button to send CQ at various speeds. It may be interesting to clock this from a Si570 digital synthesizer, allowing me to transmit on any frequency and no longer be crystal-bound. Additionally, using the same oscillator source to power a direct conversion receiver would yield obvious benefit, allowing transmit/receive from a home-brew device at minimal cost. Currently, I'm locked into using a commercial rig as a receiver. We'll see how it goes... 

<div class="text-center img-border">

[![](https://swharden.com/static/2011/01/16/IMG_4940_thumb.jpg)](https://swharden.com/static/2011/01/16/IMG_4940.jpg)

</div>

__Anyhow,__ that's that. I wanted to document this because I know I'll look back in the future and laugh at how poorly designed this project is. I'm just amazed it works, and for now this represents a gigantic step step in my learning and growth as an engineer. As poorly designed as it may be, it's something I'm very, very proud of!

__Great inspiration__ has come from Wes Hayward's [Experimental Methods in RF Design](http://www.amazon.com/Experimental-Methods-Design-Wes-Hayward/dp/087259923X/ref=sr_1_1?ie=UTF8&s=books&qid=1295289709&sr=8-1) text. I've been checking it out from the library every few weeks (Interlibrary Loan, from Vanderbilt University to the University of Florida) but I finally got my own copy for Christmas. It's such a great resource! The IRF510 push-pull idea came from figure 2.101.

__PS:__ The image below is of a MOSFET I exploded in the development process. Too much current... oops!

<div class="text-center img-border">

[![](https://swharden.com/static/2011/01/16/mosfet_die_thumb.jpg)](https://swharden.com/static/2011/01/16/mosfet_die.jpg)

</div>