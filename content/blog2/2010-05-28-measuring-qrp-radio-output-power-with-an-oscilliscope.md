---
title: Measuring QRP Radio Output Power with an Oscilloscope
date: 2010-05-28 19:54:39
tags: ["amateur radio", "circuit", "obsolete"]
---

# Measure QRP Radio Output Power with an Oscilloscope

__I added a backlight to my oscilloscope!__ My o-scope's backlight hasn't worked since I got it (for $10), so I soldered-up a row of 9 orange LEDs (I had them in a big bag) and hooked them directly up to a 3v wall wart. In retrospect I wish I had a bunch of blue LEDs... but for now I can't get over how well this worked! Compare it to the images a few posts back - you can really see the grid lines now!

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/28/oscilliscope_leds.jpg)
![](https://swharden.com/static/2010/05/28/qrss_qrp_circuit_scope.jpg)

</div>

__I know this is super-basic stuff__ for a lot of you all, but I haven't found a place online which CLEARLY documents this process, so I figured I'd toss-up a no-nonsense post which documents how I calculate the power output (in watts) of my QRP devices (i.e., QRSS MEPT) using an oscilloscope.

__I think I have increased power output__ because I'm now powering my 74HC240 from this power supply (5v, 200A) rather than USB power (which still powers the microcontroller). Let's see!

__There's the signal, and I haven't calibrated__ the grid squares (this thing shifts wildly) so I have to measure PPV (peak-to-peak voltage) in "squares". The PPV of this is about 5.3 squares.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/28/qrss_qrp_signal.jpg)
![](https://swharden.com/static/2010/05/28/10vSquare.jpg)

</div>

__I now use a function generator__ to create square waves at a convenient height. Using the same oscilloscope settings, I noticed that 10v square waves are about 7 squares high. My function generator isn't extremely accurate as you can see (very fuzzy) but this is a good approximation. I now know that my signal is 5.3/7\*10 volts. The rest of the math is pictured here:

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/28/powerCalcs.jpg)

</div>

__140mW - cool!__ It's not huge... but it's pretty good for what it is (a 2-chip transmitter). I'd like to take it up to a full watt... we'll see how it goes. My 74HC240 is totally mutilated. I accidentally broke off one of the legs, couldn't solder to it anymore, and thought I destroyed the chip. After getting distraught about a $0.51 component, I ripped ALL the legs off. Later I realized I was running out of these chips, and decided to try to revive it. I used a Dremel with an extremely small bit (similar to a quarter-round burr in dentistry) and drilled into the black casing of the microchip just above the metal contacts, allowing me enough surface area for solder to adhere to. I'm amazed it works! Now, to get more milliwatts and perhaps even watts...

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/28/testcircuit.jpg)

</div>

