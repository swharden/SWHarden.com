---
title: Breadboard Line Driver Module
date: 2016-08-20 19:16:27
tags: ["circuit", "old"]
---

# Breadboard Line Driver Module

__Sometimes I rapidly want to amplify a signal, but building amplifiers, buffers, and line drivers can be a hassle, especially on a breadboard!__ It's important to know how to carefully design build [tuned and untuned amplifier circuits](https://en.wikibooks.org/wiki/Practical_Electronics/Amplifiers#Type_of_load), but sometimes you just want to analyze or work with a signal without modifying it by sinking too much current, so being able to rapidly drop in a buffer stage would be a great help. Sometimes I want to buffer a signal so I can analyze it (with an oscilloscope or frequency counter) or use use it (perhaps to drive or gate something), but the signal source is across the room, so I need a beefy amplifier to drive it into coax as I run it across my ceiling while I'm experimenting. A [MOSFET voltage follower](https://en.wikipedia.org/wiki/Buffer_amplifier#Impedance_transformation_using_the_MOSFET_voltage_follower) or a [Darlington transistor](https://en.wikipedia.org/wiki/Darlington_transistor) may do the job, but I have to worry about input conditioning, biasing, output voltage limiting, class A, B, C, D, etc., RF vs DC, copying this circuit multiple times for multiple signals, and before you know it I'm sinking more time into my task than I need to. 

__Line driver chips are one of my go-tos for quickly amplifying digital signals because they're so fast to drop in a breadboard and they provide a strong output with very high impedance inputs and need no external components.__ Individual buffer of the integrated chip can be paralleled to multiply their current handling capabilities too. One of the common variants is the 74HC240. I don't know why it's so popular (I still find its pinout odd), but because it is popular it is cheap. They're [$0.50 on Mouser.com](http://www.mouser.com/Semiconductors/Integrated-Circuits-ICs/Logic-ICs/Buffers-Line-Drivers/_/N-6j78c?P=1z0z63x&Keyword=74hc240&FS=True) (perhaps cheaper on ebay) and [according to their datasheet](http://www.nxp.com/documents/data_sheet/74HC_HCT240.pdf) they can be run up to 7V to deliver or sink 20mA/pin with a maximum dissipation of 500mW. With propagation, enable, and disable times of tens of nanoseconds, they're not awful for lower-range radio frequencies (HF RF). This specific chip (somewhat comically at the exclusion of almost all others) has been latched onto by amateur radio operators who use it as an amplifier stage of low power (QRP) Morse code radio transmitters often pushing it to achieve ~1 watt of power output. A quick google [reveals](https://www.google.com/search?q=74hc240+transmitter) thousands of web pages discussing this! This [Portuguese site](http://py2ohh.w2c.com.br/trx/digital/rfdigital.htm) is one of the most thorough. Even if not used as the final amplifier, they're a convenient intermediate stage along an amplifier chain as they can directly drive FET final stages very well (probably best for class C operation). If you're interested, definitely check out [The Handiman's Guide to MOSFET "Switched Mode" Amplifiers guide by Paul Harden](http://www.aoc.nrao.edu/~pharden/hobby/_ClassDEF1.pdf) (no relation). Also his [part 2](http://www.aoc.nrao.edu/~pharden/hobby/_ClassDEF2.pdf).

<div class="text-center img-medium">

[![](schematic_thumb.jpg)](schematic.jpg)

</div>

This is the circuit I commonly build. I have one variant on hand for RF (extremely fast oscillations which are continuously fed into the device and often decoupled through a series capacitor), and one for TTL signals (extremely fast). __I find myself paralleling line driver outputs all the time. On a breadboard, this means tons of wires!__ __It becomes repetitive and a pain. I've started pre-packaging highly parallel line drivers into little modules which I find really convenient.__ I have a half dozen of these soldered and ready to go, and I can use them by simply dropping them into a breadboard and applying ground, power (+5V), and input signal, and it amplifies it and returns an output signal. Note that in the "Case 2: RF input" example, the inverted output of the first stage is continuously fed back into the input. This will result in continuous oscillation and undesired output if no input is supplied. In case 2, RF must be continuously applied. The advantage is that the feedback network holds the input near the threshold voltage, so very little voltage swing through the decoupling capacitor is required to generate strong output.

<div class="text-center img-border img-small">

[![](IMG_7890_thumb.jpg)](IMG_7890.jpg)
[![](IMG_7894_thumb.jpg)](IMG_7894.jpg)
[![](IMG_7897_thumb.jpg)](IMG_7897.jpg)

</div>

__Although I have made this entirely floating, I prefer using copper-clad board.__ Not only does it aid heat dissipation and provide better mechanical structure, but it also serves as a partial RF shield to minimize noise in the input and output signals. A Dremel with a diamond wheel does a good job at cutting out notches in the copper-clad board.

<div class="text-center img-border img-small">

[![](IMG_7898_thumb.jpg)](IMG_7898.jpg)
[![](IMG_7900_thumb.jpg)](IMG_7900.jpg)
[![](IMG_7909_thumb.jpg)](IMG_7909.jpg)

</div>

__The best way to replicate this is to look at the picture.__ It's surprisingly difficult to get it right just by looking at the datasheet, because when it's upside down it's mirror-imaged and very easy to make mistakes. I just connect all inputs and all outputs in parallel, for 7 of 8 gates. For one gate, I connect its output to the parallel inputs. I added some passives (including a [ferrite bead](https://en.wikipedia.org/wiki/Ferrite_bead) and decoupling capacitor on the VCC pin) and it's good to go. With only 4 pins (GND, +5V, IN, and OUT) this amplifier is easy to drop in a breadboard:

<div class="text-center img-border">

[![](IMG_7904_thumb.jpg)](IMG_7904.jpg)

</div>

__Although I often use it in a breadboard, it's easy to stick in a project.__ Since the back side is unpopulated, you can use a dot of super glue and stick it anywhere you want. In this example, I had a GPS receiver module which blinked a LED at exactly one pulse per second (1PPS) [[check out why](http://electronics.stackexchange.com/questions/30750/why-do-gps-receivers-have-a-1-pps-output)] and I wanted to do some measurements on its output. I couldn't send this line signal out a coax line because it was so low current (in reality, I didn't know what it could deliver). This is a perfect use for a buffer / line driver. 

<div class="text-center img-border">

[![](IMG_7912_thumb.jpg)](IMG_7912.jpg)

</div>

I glued this board inside my temporary project enclosure (which admittedly looks nicer and more permanent than it's actually intended to be) and set the output to deliver through 50 Ohm coax. It works beautifully!

<div class="text-center img-border img-small">

[![](IMG_7943_thumb.jpg)](IMG_7943.jpg)
[![](IMG_7948_thumb.jpg)](IMG_7948.jpg)

</div>