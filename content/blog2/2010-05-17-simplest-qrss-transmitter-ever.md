---
title: Minimal QRSS Transmitter
date: 2010-05-17 11:13:52
tags: ["circuit", "qrss", "obsolete"]
---

# Minimal QRSS Transmitter

__Success!__ Amid a bunch of academic exams, psycho-motor tests, and other crazy shenanigans my dental school is putting me through, I managed to do something truly productive! I built a simple QRSS transmitter with an ATTiny44A microcontroller clocked by a 7.04 MHz crystal which generates FSK signals and modulates its own frequency by applying potential to a reverse-biased diode at the base of the crystal, the output (CKOUT) of which is amplified by an octal buffer and sent out through an antenna. As it is, no lowpass filtering is implemented, so noisy harmonics are expected. However for ~2$ of parts this is an effective QRSS transmitter!

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/17/simple_qrss_transmitter.jpg)

</div>

__I was able to detect__ these signals VERY strongly at a station ~10 miles from my house. I haven't yet dropped in a 10.140 MHz crystal and tried to get this thing to transmit in the QRSS band, but when I do I hope to get reports from all over the world! This is what it looks like:

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/17/aj4vd.jpg)

</div>

__The cool thing__ about this transmitter (aside from the fact that it's so cheap to build) is that it will work with almost any crystal (I think below 20 MHz-ish) - just drop it in the slot and go!

