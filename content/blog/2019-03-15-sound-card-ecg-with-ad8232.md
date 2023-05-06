---
title: Sound Card ECG with AD8232
date: 2019-03-15 23:50:34
tags: ["diyECG", "csharp"]
---

# Sound Card ECG with AD8232

**Every few years I revisit the idea of building an ECG machine.** This time I was very impressed with how easy it is to achieve using the [AD8232](https://www.analog.com/media/en/technical-documentation/data-sheets/ad8232.pdf), a single-lead ECG front-end on a chip. The AD8232 is small (LFCSP package) but breakout boards are easy to obtain online. Many [vendors on eBay](https://www.ebay.com/sch/ad8232+module) sell kits that come with electrode cables and pads for under $20. Sparkfun [sells a breakout board](https://www.sparkfun.com/products/12650) but you have to buy the [cable](https://www.sparkfun.com/products/12970) and [electrodes](https://www.sparkfun.com/products/12969) separately. I highly recommend buying bags of electrodes inexpensively on eBay because having plenty will make life much easier as you experiment with this circuit. The signal that comes out of this ECG device (unlike [other ECG machines I've built](https://www.swharden.com/wp/2016-08-08-diy-ecg-with-1-op-amp/)) is remarkably clean! It doesn't require any special spectral filtering (all that is accomplished on the chip), and it can be hooked right up to an oscilloscope or sampled with analog-to-digital converter.

![](https://www.youtube.com/embed/sP_-f5nsOEo)

**The breakout board is easy to use:** Just supply 3.3V, hook-up the chest leads, and a great looking ECG signal appears on the output pin. I prefer using a [LD33V](https://www.sparkfun.com/datasheets/Components/LD1117V33.pdf) to drop arbitrary DC voltages to 3.3V. While using a 9V battery isn't the most power efficient option, it's certainly an easy one. Since the AD8232 claims to only draw 170 µA, inefficient use of a linear voltage regulator probably isn't too much of a concern for desktop experimenters. The low power consumption of this chip raises some interesting possibilities for wireless ECG analysis!

<div class="text-center img-medium">

![](https://swharden.com/static/2019/03/15/CIRCUIT.png)

</div>

**I like inspecting the output of this circuit using my computer sound card.** Probing the output pin on an oscilloscope reveals a beautiful ECG signal, but not everybody has an oscilloscope. I've seen some project webpages out there which encourage people to use the ADC of a microcontroller (usually an Arduino) to perform continuous measurements of voltage and transmit them over the USART pins, which then get transferred to a PC via a USB-to-serial USART adapter (often built around a FTDI FT-232 breakout board or similar), only to get graphed using Java software. That sequence certainly works, and if you already have an Arduino, know its sketch language, and are happy writing software in Processing, that's a great solution for you! However I found the sound card option convenient because everyone has one, and with a click-to-run computer program you can visualize your ECG right away. Note that I added a potentiometer to drop the voltage of the ECG output to make it more suitable for my microphone jack. Ideally you'll find a resistance that uses a lot of your sound card's dynamic range without clipping.

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2019/03/15/screenshot.png)

</div>

**The[ SoundCardECG project](https://github.com/swharden/SoundCardECG) on GitHub** is a click-to-run Windows program I wrote to display and analyze ECG signals coming into the computer sound card. The screenshot above shows my heart rate as I watched a promotional video for a documentary about free-climbing. You can see where my heart-rate elevated for a couple minutes in the middle as I watched a guy free-climb a cliff a thousand feet in the air without safety gear. This software is written in C# and fully open source. It certainly works, but has many avenues for improvement (such as enhanced QRS detection). Interactive graphing is provided by the [ScottPlot](https://github.com/swharden/ScottPlot) library.

**Most of the project details** are in the video, so I won't type them all out here. However, this is an excellent first step for a variety of projects that could emerge from having an easy way to measure an ECG signal. Immediate ideas are (1) heart rate detection in circuitry (not using a PC), (2) data-logging ECG signals, and (3) adding wireless functionality. I may come back and revisit one or more of these ideas in the future, but if you're interested and inspired to make something yourself I'd love to see what you come up with! Send me an email with a link to your project page and I can share it here.

<div class="text-center img-border">

![](https://swharden.com/static/2019/03/15/DSC_0015_lzn-1.jpg)

</div>

**I built this AD8232 breakout board into a nice enclosure** to make it easier to experiment with it in the future. The circuity isn't anything special: a linear voltage regulator with capacitive decoupling on the input and output, and an op-amp serving as a unity gain amplifier to buffer the output accessible through a SMA connector, and a current-limited output attached to a female 1/8" audio for easy connection to my computer sound card.

<div class="text-center img-border">

![](https://swharden.com/static/2019/03/15/AD8232-ECG-output.gif)

</div>

**Personal update:** My website posts (and YouTube videos) have slowed dramatically as I've been dealing with some complicated medical issues. I don't intend on posting medical updates on this web page, but anyone interested in following my medical treatments can do so at http://swharden.com/med/