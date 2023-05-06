---
title: Pushing and Pulling
date: 2010-05-26 07:42:39
tags: ["circuit", "amateur radio", "old"]
---

# Pushing and Pulling

__I found a way__ to quadruple the output power of my QRSS transmitter without changing its input parameters. Thanks to a bunch of people (most of whom are on the Knights QRSS mailing list) I decided to go with a push-pull configuration using 2 pairs of 4 gates (8 total) of a 74HC240. I'll post circuit diagrams when I perfect it, but for now check out these waveforms!

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/26/qrss_amplified1.jpg)

</div>

First of all, this is the waveform before and after amplification with the 74HC240. I artificially weakened the input signal (top) with a resistor and fed it to the 74HC240. For the rest of the images, the input is 5v p-p and the output is similar, so amplification won't be observed. The wave I'm starting with is the output of a microcontroller which is non-sinusoidal, but this can be fixed later with lowpass filtering.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/26/qrss_74hc2401.jpg)

</div>

Here you can see the test circuit I'm using. It should be self-explanatory.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/26/qrss_inPhase1.jpg)

</div>

Here's the output of the microcontroller compared to the in-phase output of the 74HC240

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/26/qrss_out_of_phase1.jpg)

</div>

Here are the two outputs of the 74HC240. 4 of the gates are used to create output in-phase with the input, and the other four are used to create out-of-phase wave. Here are the two side by side. The top is 0 to 5v, the bottom is 0 to -5v, so we have a push-pull thing going on... woo hoo!

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/26/qrss_out_of_phase_overlap1.jpg)

</div>

The waves, when overlapped, look similar (which I guess is a good thing) with a slight (and I mean VERY slight) offset of the out-of-phase signal. I wonder if this is caused by the delay in the time it takes to trigger the 74HC240 to make the out-of-phase signal? The signal I'm working with is 1MHz.

__Okay, that's it for now.__ I'm just documenting my progress. 73