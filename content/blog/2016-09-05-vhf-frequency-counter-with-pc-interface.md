---
title: VHF Frequency Counter with PC Interface
date: 2016-09-05 17:34:44
tags: ["amateur radio", "circuit", "python", "old"]
---

# VHF Frequency Counter with PC Interface

**Projects I build often involve frequency synthesis, and one of the most useful tools to have around is a good frequency counter.** I love the idea of being able to access / log / analyze frequency readings on my computer. Commercial frequency counters can be large, expensive, and their calibration is a chicken-and-egg problem (you need a calibrated frequency counter to calibrate a frequency reference you use to calibrate a frequency counter!). **For about the cost of a latte I made a surprisingly good frequency frequency counter (which directly counts >100 MHz without dividing-down the input signal)** by blending a SN74LV8154 dual 16-bit counter (which can double as a 32-bit counter, [$1.04 on mouser](http://www.mouser.com/Search/Refine.aspx?Keyword=sn74lv8154&Ns=Pricing%7c0&FS=True)) and an ATMega328 microcontroller ([$3.37 on Mouser](http://www.mouser.com/Semiconductors/Integrated-Circuits-ICs/Embedded-Processors-Controllers/Microcontrollers-MCU/8-bit-Microcontrollers-MCU/_/N-a86lo?P=1z0y33r&Keyword=atmega328p&Ns=Pricing%7c0&FS=True)). 

**Although these two chips are all you need to count something, the accuracy of your counts depend on your gate.** If you can generate a signal of 1 pulse per second (1PPS), you can count anything, but your accuracy depends on the accuracy of your 1PPS signal. To eliminate the need for calibration (and to provide the 1PPS signal with the accuracy of an atomic clock) I'm utilizing the 1PPS signal originating from a GPS unit which I already had distributed throughout my shack ([using a 74HC240 IC as a line driver](https://www.swharden.com/wp/2016-08-20-breadboard-line-driver-module/)). If you don't have a GPS unit, consider getting one! I'm using a NEO-6M module ([$17.66 on Amazon](https://www.amazon.com/Andoer-AeroQuad-Multirotor-Quadcopter-Aircraft/dp/B00RCP9MLY)) to generate the 1PPS gate, and if you include its cost we're up to $22.07. Also,** all of the code for this project (schematics, C that runs on the microcontroller, and a Python to interact with the serial port) is [shared on GitHub](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202016-09-04%20SN74LV8154)!** You may be wondering, "why do GPS units have incredibly accurate 1PPS signals?" It's a good question, but a subject for another day. For now, trust me when I say they're fantastically accurate (but slightly less precise due to jitter) if you're interested in learning more read up on [GPS timing](https://www.u-blox.com/sites/default/files/products/documents/Timing_AppNote_%28GPS.G6-X-11007%29.pdf).

<div class="text-center">

[![](pc-frequency-counter-schem_thumb.jpg)](pc-frequency-counter-schem.png)

</div>

**This is the general idea behind how this frequency counter works.** It's so simple! It's entirely digital, and needs very few passive components. sn74lv8154 is configured in 32-bit mode (by chaining together its two 16-bit counters, [see the datasheet for details](http://www.ti.com/lit/ds/symlink/sn74lv8154.pdf)) and acts as the front-end directly taking in the measured frequency. This chip is "rare" in the sense I find very few internet projects using it, and they're not available on ebay. However they're cheap and plentiful on mouser, so I highly encourage others to look into using it! The datasheet isn’t very clear about its maximum frequency, but in my own tests I was able to measure in excess of 100 MHz from a breadboarded circuit! This utilized [two cascaded ICS501 PLL frequency multiplier ICs to multiply a signal](https://www.swharden.com/wp/2016-08-31-ics501-simple-frequency-multiplier/) I had available (the 11.0592 MHz crystal the MCU was running from) by ten, yielding 110 MHz, which it was able to measure (screenshot is down on the page).

<div class="text-center">

[![](neo-60-gps-1pps_thumb.jpg)](neo-60-gps-1pps.jpg)

</div>

**The 1PPS gate signal is generated from an inexpensive GPS module [available on Amazon](https://www.amazon.com/Andoer-AeroQuad-Multirotor-Quadcopter-Aircraft/dp/B00RCP9MLY).** I've hinted at the construction of this device before and [made a post](https://www.swharden.com/wp/2016-08-20-breadboard-line-driver-module/) about how to send output signals like the 1PPS signal generated here throughout your shack via coax using a line driver, so I won't re-hash all of those details here. I will say that this module has only VCC, GND, and TX/RX pins, so to get access to the 1PPS signal you have to desolder the SMT LED and solder a wire to its pad. It requires a bit of finesse. If you look closely, [you can see it in this picture](https://www.swharden.com/wp/2016-08-20-breadboard-line-driver-module/#jp-carousel-5918) (purple wire).

<div class="text-center img-border">

[![](IMG_8207_thumb.jpg)](IMG_8207.jpg)

</div>

**I first built this device on a breadboard, and despite the rats nest of wires it worked great!** Look closely and you can see the ICS501 frequency multiplier ICs [I wrote about before](https://www.swharden.com/wp/2016-08-31-ics501-simple-frequency-multiplier/). In this case it's measuring the 10x multiplied crystal frequency clocking the MCU (11 MHz -> 110 MHz) and reporting these readings every 1 second to the computer via a serial interface.

<div class="text-center img-border">

[![](ss_thumb.jpg)](ss.png)

</div>

**Frequency measurements of the VHF signal are reported once per second. Measurements are transmitted through a USB serial adapter, and captured by a Python script.** Note that I'm calling this signal [VHF](https://en.wikipedia.org/wiki/Very_high_frequency) because it's >30 MHz. I am unsure if this device will work up to 300 MHz (the border between VHF and UHF), but I look forward to testing that out! Each line contains two numbers: the actual count of the counter (which is configured to simply count continuously and overflow at 2^32=4,294,967,296), and the gated count (calculated by the microcontroller) which is the actual frequency in Hz.

>  This screenshot shows that my ~11.05 MHz crystal is actually running at 11,061,669.4 Hz. See how I capture the 0.4 Hz unit at the end? That level of precision is the advantage of using this VHF-capable counter in conjunction with a 10x frequency multiplier!

**Once I confirmed everything was working, I built this device in a nice enclosure.** I definitely splurge every few months and buy extruded split body aluminum enclosures in bulk ([ebay](http://www.ebay.com/sch/i.html?_nkw=extruded+split+body+aluminum+enclosure)), but they're great to have on hand because they make projects look so nice. I added some rubber feet (cabinet bumpers from Walmart), drilled holes for all the connectors with a continuous step drill bit, made a square hole for the serial port using a [nibbler](https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtools&field-keywords=Nickel+Plated+Nibbling+Tool), and the rest is pretty self-evident. Labels are made with a DYMO LetraTag (Target) and clear labels (Target, Amazon) using a style [inspired by PA2OHH](http://www.qsl.net/pa2ohh/tlabels.htm). I tend to build one-off projects like this dead-bug / Manhattan style.

<div class="text-center img-border">

[![](IMG_8277_thumb.jpg)](IMG_8277.jpg)
[![](IMG_8282_thumb.jpg)](IMG_8282.jpg)

</div>

**I super-glued a female header to the aluminum frame to make in-circuit serial programming (ICSP) easy.** I can't believe I never thought to do this before! Programming (and reprogramming) was so convenient. I'm going to start doing this with every enclosed project I build from now on. FYI I'm using a USBTiny ISP ([$10.99, Amazon](https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=usbtiny+isp)) to do the programming (no longer the BusPirate, it's too slow) [like I describe here for 64-bit Windows 7](https://www.swharden.com/wp/2013-05-07-avr-programming-in-64-bit-windows-7/) (although I'm now using Windows 10 and it works the same).

<div class="text-center img-border">

[![](IMG_8330_thumb.jpg)](IMG_8330.jpg)

</div>

**The front of the device** has LEDs indicating power, serial transmission, and gating. Without a 1PPS gate, the device is set to send a count (of 0) every 5 seconds. In this case, the TX light will illuminate. If a gate is detected, the TX and GATE LEDs will illuminate simultaneously. In reality I just drilled 3 holes when I really needed two, so I had to make-up a function for the third LED (d'oh!)

<div class="text-center img-border">

[![](IMG_8286_thumb.jpg)](IMG_8286.jpg)

</div>

**The back of the device** has serial output, frequency input, gate input, and power. Inside is a LM7805 voltage regulator, and careful attention was paid to decoupling and keeping ripple out of the power supply (mostly so our gate input wouldn't be affected). I'm starting to get in the habit of labeling all serial output ports with the level (TTL vs CMOS, which makes a HUGE difference as MAX232 level converter may be needed, or a USB serial adapter which is capable of reading TTL voltages), as well as the baud rate (119200), byte size (8), parity (N), and stop bit (1). _I just realized there's a typo! The label should read 8N1. I don't feel like fixing it, so I'll use a marker to turn the 2 into an 8. _I guess I'm only human after all.

<div class="text-center img-border">

[![](IMG_8297_thumb.jpg)](IMG_8297.jpg)

</div>

**I should have tried connecting all these things before I drilled the holes.** I got _so_ lucky that everything fit, with about 2mm to spare between those BNC jacks. Phew!

<div class="text-center img-border">

[![](IMG_8316_thumb.jpg)](IMG_8316.jpg)

</div>

**This is an easy test frequency source.** I have a dozen [canned oscillators](https://en.wikipedia.org/wiki/Crystal_oscillator) of various frequencies. This is actually actually a voltage controlled oscillator ([VCO](https://en.wikipedia.org/wiki/Voltage-controlled_oscillator)) with adjustment pin (not connected), and it won't be exactly 50 MHz without adjustment. It's close enough to test with though! As this is >30 MHz, we can call the signal [VHF](https://en.wikipedia.org/wiki/Very_high_frequency).

<div class="text-center img-border">

[![](IMG_8318_thumb.jpg)](IMG_8318.jpg)

</div>

**You can see on the screen it's having no trouble reading the ~50 MHz frequency.** You'll notice I'm using [RealTerm](http://realterm.sourceforge.net/) (with a [good write-up on sparkfun](https://learn.sparkfun.com/tutorials/terminal-basics/real-term-windows)) which is my go-to terminal program instead of HyperTerminal (which really needs to go away forever). In reviewing this photo, I'm appreciating how much unpopulated room I have on the main board. I'm half tempted to build-in a frequency multiplier circuit, and place it under control of the microcontroller such that if an input frequency from 1-20MHz is received, it will engage the 10x multiplier. That's a mod for another day though! Actually, since those chips are SMT, if I really wanted to do this I would make this whole thing a really small SMT PCB and greatly simplify construction. That sounds like a project for another day though...[None](https://www.swharden.com/wp/wp-content/uploads/2016/09/IMG_8316.jpg)

<div class="text-center img-border">

[![](IMG_8335_thumb.jpg)](IMG_8335.jpg)

</div>

**Before closing it up I added some extra ripple protection on the primary counter chip.** There's a 560 uH series inductor with the power supply, followed by a 100 nF capacitor parallel with ground. I also added [ferrite beads](https://en.wikipedia.org/wiki/Ferrite_bead) to the MCU power line and gate input line. I appreciate how the beads are unsecured and that this is a potential weakness in the construction of this device (they're heavy, so consider what would happen if you shook this enclosure). However, anything that would yank-away cables in the event of shaking the device would probably also break half the other stuff in this thing, so I think it's on par with the less-than-rugged construction used for all the other components in this device. It will live a peaceful life on my shelf. I am not concerned.

<div class="text-center img-border">

[![](IMG_8335_thumb.jpg)](IMG_8335.jpg)

</div>

**This is the final device counting frequency and continuously outputting the result to my computer.** In the background you can see the 12V power supply (yellow) indicating it is drawing only 20 mA, and also the GPS unit is in a separate enclosure on the bottom right. [Click here to peek inside](https://www.swharden.com/wp/2016-08-20-breadboard-line-driver-module/#jp-carousel-5918) the GPS 1PPS enclosure.

<div class="text-center img-border">

[![](IMG_8344_thumb.jpg)](IMG_8344.jpg)

</div>

**I'm already loving this new frequency counter!** It's small, light, and nicely enclosed (meaning it's safe from me screwing with it too much!). I think this will prove to be a valuable piece of test equipment in my shack for years to come. I hope this build log encourages other people to consider building their own equipment. I learned a lot from this build, saved a lot of money not buying something commercial, had a great time making this device, and I have a beautiful piece of custom test equipment that does _exactly_ what I want.

## Source Code

Microcontroller code (AVR-GCC), schematics, and a Python script to interface with the serial port are all available on [this project's GitHub page](https://github.com/swharden/AVR-projects/blob/master/ATMega328%202016-09-04%20SN74LV8154/main.c)

## Afterthought: Using without GPS

One of the great advantages of this project is that it uses GPS for an extremely accurate 1 PPS signal, but what options exist to adapt this project to not rely on GPS? The GPS unit is expensive (though still <$20) and GPS lock is not always feasible (underground, in a Faraday cage, etc). Barring fancy things like dividing-down rubidium frequency standards or oven controlled oscillators, consider having your microcontroller handle the gating using either [interrupts and timers precisely configured to count seconds](https://www.swharden.com/wp/2011-06-19-using-timers-and-counters-to-clock-seconds/). Since this project uses a serial port with a 11.0592 MHz crystal, your 1PPS stability will depend on the stability of your oscillator (which is pretty good!). Perhaps more elegantly you could use a 32.768 kHz crystal oscillator to create a 1 PPS signal. This frequency can be divided by 2 over and over to yield 1 Hz perfectly. This is what most modern wristwatches do. Many AVRs have a separate oscillator which can accomodate a 32 kHz crystal and throw interrupts every 1 second without messing with the system clock. Alternatively, the [74GC4060](http://www.nxp.com/documents/data_sheet/74HC_HCT4060_Q100.pdf) (a 14 stage ripple counter) can divide 32k into 1 Hz and even can be arranged as an oscillator (check the datasheet). It would be possible to have both options enabled (local clock and GPS) and only engage the local clock if the GPS signal is absent. If anyone likes the idea of this simple VHF frequency counter with PC interface but doesn't want to bother with the GPS, there are plenty of options to have something _almost_ as accurate. That really would cut the cost of the final device down too, keeping it under the $5 mark.

## Update: Integrating Counter Serial Output with GPS Serial Output

The NEO-M8 GPS module is [capable of outputting serial data](https://www.u-blox.com/sites/default/files/NEO-M8_DataSheet_(UBX-13003366).pdf) at 9600 baud and continuously dumps [NEMA formatted](http://www.gpsinformation.org/dale/nmea.htm) GPS data. While this isn't really useful for location information (whose frequency counter requires knowing latitude and longitude?) it's great for tracking things like signal strength, fix quality, and number of satellites. After using this system to automatically log frequency of my frequency reference, I realized that sometimes I'd get 1-2 hours of really odd data (off by kHz, not just a few Hz). Power cycling the GPS receiver fixes the problem, so my guess it that it's a satellite issue. If I combine the GPS RX and counter in 1 box, I could detect this automatically and have the microcontroller power cycle the GPS receiver (or at the least illuminate a red error LED). I don't feel like running 2 USB serial adapters continuously. I don't feel like programming my AVR to listen to the output from the GPS device (although that's probably the _correct_ way to do things).  Instead I had a simpler idea that worked really well, allowing me to simultaneously log serial data from my GPS unit and microcontroller (frequency counter) using 1 USB serial adapter.

<div class="text-center img-border">

[![](IMG_8401_thumb.jpg)](IMG_8401.jpg)

</div>

**The first thing I did was open up the frequency counter and reconnect my microcontroller programmer.** This is exactly what I promised myself I wouldn't do, and why I have a nice enclosure in the first place! Scott, stop fidgeting with things! The last time I screwed this enclosure together I considered adding super glue to the screw threads to make sure I didn't open it again. I'll keep my modifications brief! For now, this is a test of a concept. When it's done, I'll revert the circuitry to how it was and close it up again. I'll take what I learn and build it into future projects.

<div class="text-center img-border">

[![](IMG_8402_thumb.jpg)](IMG_8402.jpg)

</div>

**I peeked at the serial signals of both the frequency counter (yellow) and the GPS unit output (blue).** To my delight, there was enough dead space that I thought I could stick both in the same signal. After a code modification, I was able to tighten it up a lot, so the frequency counter never conflicts with the GPS unit by sending data at the same time.

<div class="text-center img-border">

[![](IMG_8403_thumb.jpg)](IMG_8403.jpg)

</div>

**I had to slow the baud rate to 9600, but I programmed it to send fewer characters.** This leaves an easy ~50ms padding between my frequency counter signal and the GPS signal. Time to mix the two! This takes a little thought, as I can't just connect the two wires together. Serial protocol means the lines are usually high, and only pulled down when data is being sent. I had to implement an active circuit.

<div class="text-center img-border img-small">

[![](FullSizeRender-2_thumb.jpg)](FullSizeRender-2.jpg)

</div>

**Using a few components, I built an AND gate to combine signals from the two serial lines.** For some reason it took some thought before I realized an AND gate was what I needed here, but it makes sense. The output is high (meaning no serial signal) only when both inputs are high (no serial signals on the input). When either signal drops low, the output drops low. This is perfect. My first thought was that I'd need a NOR gate, but an inverted AND gate _is_ a NOR gate.

<div class="text-center img-border">

[![](IMG_8404_thumb.jpg)](IMG_8404.jpg)

</div>

**Here's my quick and dirty implementation.** A reminder again is that this will be removed after this test. For now, it's good enough.

<div class="text-center img-border">

[![](IMG_8405_thumb.jpg)](IMG_8405.jpg)

</div>

**After connecting** the GPS serial output and frequency counter serial output to the AND gate (which outputs to the computer), I instantly got the result I wanted!

<div class="text-center img-border">

![](serial-combine.jpg)

</div>

**RealTerm shows that both inputs are being received.** It's a mess though. If you want to know what everything is, read up on [NEMA formatted](http://www.gpsinformation.org/dale/nmea.htm) GPS data.

<div class="text-center img-border">

[![](combined-python_thumb.jpg)](combined-python.png)

</div>

**I whipped-up a python program to parse, display, and log key information.** This display updates every 1 second. The bottom line is what is appended to the log file on ever read. It's clunky, but again this is just for testing and debugging. I am eager to let this run for as long as I can (days?) so I can track how changes in satellite signal / number / fix quality influence measured frequency.