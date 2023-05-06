---
title: Microcontroller Clocking a Transmitter?
date: 2010-04-03 23:19:37
tags: ["qrss", "circuit"]
---

# Microcontroller Clocking a Transmitter?

__I shouldn't claim this idea as novel. __After googling around, I found another person who's doing the same thing, and now that I read his page I remember reading his page before, which is likely where I got the idea in the first place. I want to give him credit and hope that my project can turn out successfully like his! [http://clayton.isnotcrazy.com/mept\_v1](http://clayton.isnotcrazy.com/mept_v1).

__Here's my idea: __ The core of any transmitter is an oscillator, and in simple transmitters (like QRSS devices), it's often a crystal. Frequency adjustment is accomplished by adjusting capacitance to ground on one of the crystal legs. Simple oscillators such as the Colpitts design (based on an NPN transistor) are often used (pictured).

<div class="text-center">

[![](https://swharden.com/static/2010/04/03/NPN_Colpitts_oscillator_collector_coil_thumb.jpg)](https://swharden.com/static/2010/04/03/NPN_Colpitts_oscillator_collector_coil.png)

</div>

__See how pins 4 and 5 allow for a crystal, and pin 6 has a "CKOUT" feature?"__ I'm still not sure exactly what the waveform of its output looks like. The datasheet is almost intentionally cryptic. About the only thing I've been able to discover from the Internet is that it's sufficient to clock another microcontroller. However, if it's an amplified sine wave output, how cool is it that it might be able to produce RF at the same frequency at which it's clocked?

__However in my quest to design a minimal-case long-distance transmitter,__ I'm trying to think outside the box. Although it's relatively simple, that's still several parts just to make an oscillating sine wave from a crystal. The result still has to be pre-amplified before sending the signal to an antenna. I'm starting to wonder about the oscillator circuitry inside a microcontroller which has the ability to be clocked by an external crystal. For example, take the pinout diagram from an Atmel ATTiny2313 AVR:

<div class="text-center">

![](https://swharden.com/static/2010/04/03/attiny-2313.gif)

</div>

__Taking it a step further,__ I wonder if I could write code for the microcontroller to allow it to adjust its own clock speed / frequency output by adjusting capacitance on one of the legs of the crystal. A reverse-biased LED with variable voltage pressed against it from an output pin of the microcontroller might accomplish this. How cool would this be - a single chip transmitter and frequency-shifting keyer all in one? Just drop in a crystal of your choice and BAM, ready to go. Believe it or not I've tested this mildly and it's producing enough RF to be able to be picked up easily by a receiver in the same room, but I'm still unsure of the power output or the waveform. If the waveform is an amplified sine wave I'm going to pass out. More likely it's a weak sine wave needing a preamplifier still, or perhaps even amplified square waves in need of lowpass filtering...

<div class="text-center img-border">

[![](https://swharden.com/static/2010/04/03/IMG_3206_thumb.jpg)](https://swharden.com/static/2010/04/03/IMG_3206.png)

</div>

My wife snapped a photo of me working! It's a funny pic - I'm in my own little world sometimes…

<div class="text-center img-border">

[![](https://swharden.com/static/2010/04/03/IMG_3241_thumb.jpg)](https://swharden.com/static/2010/04/03/IMG_3241.jpg)

[![](https://swharden.com/static/2010/04/03/IMG_3245_thumb.jpg)](https://swharden.com/static/2010/04/03/IMG_3245.jpg)

[![](https://swharden.com/static/2010/04/03/IMG_3250_thumb.jpg)](https://swharden.com/static/2010/04/03/IMG_3250.jpg)

[![](https://swharden.com/static/2010/04/03/IMG_3257_thumb.jpg)](https://swharden.com/static/2010/04/03/IMG_3257.jpg)

</div>