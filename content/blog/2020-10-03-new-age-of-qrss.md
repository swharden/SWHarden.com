---
title: The New Age of QRSS
date: 2020-10-03 22:08:00
tags: ["qrss", "amateur radio"]
---

# The New Age of QRSS

**QRSS is an experimental radio mode that uses frequency-shift-keyed (FSK) continuous wave (CW) Morse code to transmit messages that can be decoded visually by inspecting the radio frequency spectrogram.** The name "QRSS" is a derivation of the [Q code](https://en.wikipedia.org/wiki/Q_code) "QRS", a phrase Morse code operators send to indicate the transmitter needs to slow down. The extra "S" means slow way, _way_ down, and at the typical speed of 6 second dots and 18 second dashes most QRSS operators have just enough time to send their call sign once every ten minutes (as required by federal law). These slow Morse code messages can be decoded by visual inspection of spectrograms created by computer software processing the received audio. A QRSS grabber is a radio/computer setup configured to upload the latest radio spectrogram to the internet every 10 minutes. [QRSS Plus](https://swharden.com/qrss/plus/) is an automatically-updating list of active QRSS grabbers around the world, allowing the QRSS community to see QRSS transmitters being detected all over the world. 

> **TLDR: Get Started with QRSS**
> * Tune your radio to 10.140 MHz (10.1387 MHz USB)
> * Install spectrogram software like [FSKview](https://swharden.com/software/FSKview)
> * Inspect the spectrogram to decode callsigns visually
> * Join the [QRSS Knights](https://groups.io/g/qrssknights) mailing list to learn what's new
> * Go to [QRSS Plus](https://swharden.com/qrss/plus/) to see QRSS signals around the world
> * Design and build a circuit (or [buy a kit](https://www.qrp-labs.com/)) to transmit QRSS

## What is QRSS?

**QRSS allows miniscule amounts of power to send messages enormous distances.** For example, 200 mW QRSS transmitters are routinely spotted on QRSS grabbers thousands of miles away. The key to this resilience lies in the fact that spectrograms can be designed which average several seconds of audio into each pixel. By averaging audio in this way, the level of the noise (which is random and averages toward zero) falls below the level of the signal, allowing visualization of signals on the spectrogram which are too deep in the noise to be heard by ear.

<div class="text-center img-border">

![](https://swharden.com/static/2020/10/03/lopora-signals2.jpg)

</div>

**If you have a radio and a computer, you can view QRSS!** Connect your radio to your computer's microphone, then run a spectrogram like [FSKview](https://swharden.com/software/FSKview/) to visualize that audio as a spectrogram. The most QRSS activity is on 30m within 100 Hz of 10.140 MHz, so set your radio to upper sideband (USB) mode and tune to 10.1387 MHz so QRSS audio will be captured as 1.4 kHz audio tones. 

**[FSKview](https://swharden.com/software/FSKview/) is radio frequency spectrogram software for viewing QRSS and WSPR simultaneously.** I wrote [FSKview](https://swharden.com/software/FSKview/) to be simple and easy to use, but it's worth noting that [Spectrum Lab](https://www.qsl.net/dl4yhf/spectra1.html),  [Argo](https://digilander.libero.it/i2phd/argo/), [LOPORA](https://www.qsl.net/pa2ohh/11lop.htm), and [QRSSpig](https://gitlab.com/hb9fxx/qrsspig) are also popular spectrogram software projects used for QRSS, with the last two supporting Linux and suitable for use on the Raspberry Pi.

<div class="text-center">

![](https://swharden.com/static/2020/10/03/fskview.png)

</div>

## QRSS Transmitter Design

**QRSS transmitters can be extraordinarily simple because they just transmit a single tone which shifts between two frequencies.** The simplicity of QRSS transmitters makes them easy to assemble as a kits, or inexpensively designed and built by those first learning about RF circuit design. The simplest designs use a crystal oscillator (typically a [Colpitts](https://en.wikipedia.org/wiki/Colpitts_oscillator) configuration) followed by a buffer stage and a final amplifier (often [Class C](https://en.wikipedia.org/wiki/Power_amplifier_classes#Class_C) configuration using a 2N7000 N-channel MOSFET or 2N2222 NPN transistor). Manual frequency adjustments are achieved using a variable capacitor, supplemented in this case with twisted wire to act as a simple but effective variable capacitor for fine frequency tuning within the 100 Hz QRSS band. Frequency shift keying to transmit call signs is typically achieved using a microcontroller to adjust voltage on a reverse-biased diode (acting as a [varactor](https://en.wikipedia.org/wiki/Varicap)) to modulate capacitance and shift resonant frequency of the oscillator. Following a low-pass filter (typically a 3-pole [Chebyshev](https://en.wikipedia.org/wiki/Chebyshev_filter) design) the signal is then sent to an antenna.

<div class="text-center img-medium">

![](https://swharden.com/static/2020/10/03/qrp-labs-kit-schematic.jpg)

</div>

**[QRP Labs](https://www.qrp-labs.com/) is a great source for QRSS kits.** The kit pictured above and below is one of their earliest kits (the 30/40/80/160m QRSS Kit), but they have created many impressive new products in the last several years. Some of their more advanced QRSS kits leverage things like direct digital synthesis (DDS), GPS time synchronization, and the ability to transmit additional digital modes like Hellschreiber and WSPR.

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2020/10/03/qrp-labs-kit-photo.jpg)

</div>

## Radio Frequency Spectral Phenomena

**Atmospheric phenomena and other special conditions can often be spotted in QRSS spectrograms**. One of the most common special cases are radio frequency reflections off of airplanes resulting in the radio waves arriving at the receiver simultaneously via two different paths (a form of [multipath propagation](https://en.wikipedia.org/wiki/Multipath_propagation)). Due to the Doppler shift from the airplane approaching the receiver the signal from the reflected path appears higher frequency than the direct path, and as the airplane flies over and begins heading away the signal from the reflected path decreases in frequency relative to the signal of the direct path. The image below is one of my favorites, captured by [Andy (G0FTD)](https://sites.google.com/view/andy-g0ftd/the-qrss-gallery) in the 10m QRSS band. [QRSS de W4HBK](http://pensacolasnapper.blogspot.com/) is a website that has many blog posts about rare and special grabs, demonstrating effects of meteors and coronal mass ejections on QRSS signals.

<div class="text-center img-medium">

![](https://swharden.com/static/2020/10/03/rf-reflection-airplane.png)

</div>

<div class="text-center img-medium img-border">

![](https://swharden.com/static/2020/10/03/rf-reflection-airplane.jpg)

</div>

## QRSS Transmitters are Not Beacons

Radio beacons send continuous, automated, unattended, one-way transmissions without specific reception targets. In contrast, QRSS transmitters are only intended to be transmitting when the control operator is available to control them, and the recipients are known QRSS grabbers around the world. To highlight the distinction from radio beacons, QRSS transmitters are termed ***Manned Experimental Propagation Transmitters (MEPTs)***. Users in the United States will recall that the FCC (in Part 97.203) confines operation of radio beacons to specific regions of the radio spectrum and disallows operation of beacons below 28 MHz. Note that amateur radio beacons typically operate up to 100 W which is a power level multiple orders of magnitude greater than QRSS transmitters. MEPTs, in contrast, can transmit in any portion of the radio frequency spectrum where CW operation is permitted.

## The New Age of QRSS
**QRSS was first mentioned in epsisode 28 of [The Soldersmoke Podcast](http://www.soldersmoke.com/) on July 30, 2006.** It was discussed in several episodes over the next few years, and a 2009 [post about QRSS](https://hackaday.com/2009/02/22/qrss-radio-amateurs-slow-speed-narrowband/) on Hack-A-Day brought it to my attention. In the early days of QRSS the only way to transmit QRSS was to design and build your own transmitter. [David Hassall (WA5DJJ)](http://www.zianet.com/dhassall/QRSS_A.html), [Bill Houghton (W4HBK)](http://pensacolasnapper.blogspot.com/), [Hans Summers (G0UPL)](http://www.hanssummers.com/), and others would post their designs on their personal websites along with notes about where their transmitters had been spotted. In the following years the act of creating QRSS grabbers became streamlined, and websites like I2NDT's [QRSS Grabber Compendium](https://digilander.libero.it/i2ndt/grabber/grabber-compendium.htm) and [QRSS Plus](https://swharden.com/qrss/plus/) made it easier to see QRSS signals around the world. [Hans Summers](http://www.hanssummers.com/) (G0UPL) began selling QRSS transmitter kits at amateur radio conventions, then later through the [QRP Labs website](https://www.qrp-labs.com/). As more people started selling and buying kits (and documenting their experiences) it became easier and easier to get started with QRSS. Before QRSS kits were easy to obtain the only way to participate in the hobby was to design and build a transmitter from scratch, representing a high barrier to entry for those potentially interested in this fascinating hobby. Now with the availability of high quality QRSS transmitter kits and the ubiquity of internet tools and software to facilitate QRSS reception, it's easier than ever to get involved in this exciting field! For these reasons I believe we have entered into a _New Age of QRSS_.

## QRSS Frequency Bands

**To receive QRSS, configure your radio for uper sideband using a dial frequency from the table below and QRSS will be audible as 1-2 kHz audio tones.** This radio configuration is identical to the recommendation by [WSPRnet](https://www.wsprnet.org) for receiving WSPR using WSJT-X software, allowing QRSS and WSPR to be monitored simultaneously.

**The entire QRSS band is approximately 200 Hz wide** centered on the QRSS frequencies listed in the table below. Testing and experimentation is encouraged in the 100 Hz below the listed frequency, and the upper portion is typically used for more stable transmitters. An exception is the 10m band where the QRSS band is 400 Hz wide, extending ±200 Hz from the center frequency listed below.

<div class="text-center">
<div class="d-inline-block mx-auto text-start">


Band | QRSS Frequency (±100 Hz)     | USB Dial Frequency (Hz)   | Audio Frequency (Hz)
-----|------------------------------|---------------------------|-----------------------
600m | 476,100						| 474,200					| 1,900
160m | 1,837,900					| 1,836,600					| 1,300
80m  | 3,569,900 ⭐ _popular_		| 3,568,600					| 1,300
60m  | 5,288,550					| 5,287,200					| 1,350
40m  | 7,039,900 ⭐ _popular_		| 7,038,600					| 1,300
30m  | 10,140,000 🌟 _most popular_	| 10,138,700				| 1,300
22m  | 13,555,400					| 13,553,900				| 1,300
20m  | 14,096,900 ⭐ _popular_		| 14,095,600				| 1,300
17m  | 18,105,900					| 18,104,600				| 1,300
15m  | 21,095,900					| 21,094,600				| 1,300
12m  | 24,925,900					| 24,924,600				| 1,300
10m  | 28,125,700					| 28,124,600				| 1,100
6m   | 50,294,300					| 50,293,000				| 1,300


</div>
</div>

Similar QRSS frequency tables:

* [WSPR and QRSS frequencies](https://g6nhu.co.uk/frequencies.html) by Keith (G6NHU)

* [QRSS Watering Holes](https://sites.google.com/view/andy-g0ftd/qrss-freqs) by Andy (G0FTD)

> **⚠️ WARNING:** It may not be legal for you to transmit on these frequencies. Check license requirements and regulations for your region before transmitting QRSS.

> **⚠️ WARNING:** These frequencies sometimes change based upon community discussion. Frequency tables can be found on the [Knights QRSS Wiki](https://groups.io/g/qrssknights/wiki/3964). Outdated or alternate frequencies include 160m (1,843,200 Hz), 80m (3,593,900 Hz), 12m (24,890,800 Hz), 10m (28,000,800 Hz and 28,322,000 ±500 Hz), and 6m (50,000,900 Hz). Experimentation on 10m is encouraged in the 100Hz above the band.

**When tuning your radio your dial frequency may be lower than the QRSS frequency.** If you are using upper-sideband (USB) mode, you have to tune your radio dial 1.4 kHz _below_ the QRSS band to hear QRSS signals as a 1.4 kHz tone. Recommended dial frequencies in the table above are suitable for receiving QRSS and WSPR.

## QRSS Knights

**The [QRSS Knights](https://groups.io/g/qrssknights) is a group of QRSS enthusiasts** who coordinate events and discuss experiments over email. The group is kind and welcoming to newcomers, and those interested in learning more about QRSS are encouraged to join the mailing list.

## Resources

* This page can be found at http://swharden.com/qrss

* [QRSS Plus](https://swharden.com/qrss/plus/) is an automatically-updating active QRSS grabber list

* [What is QRSS](https://www.qsl.net/m0ayf/What-is-QRSS.html) by M0AYF is a classic summary of QRSS, with many links to detailed schematics and design consideration notes. Notably the sections for [receiving QRSS](https://www.qsl.net/m0ayf/Receiving-QRSS.html) and [transmitting QRSS](https://www.qsl.net/m0ayf/Transmitting-QRSS.html) are great places to learn more.

* [QRSS and You](http://www.ka7oei.com/qrss1.html) by KA7OEI is another classic summary of QRSS.

* Weak Signal Propagation Reporter (WSPR) is a low power radio protocol that typically operates adjacent to the QRSS bands and provides automated decoding of callsign, power, and location information. Read more at http://wsprnet.org

* [The QRSS Adventure](http://www.zianet.com/dhassall/QRSS_A.html) by Dave Hassall (WA5DJJ) has circuit designs and commentary spanning far back into the early days of QRSS. His [ 1,164,000,000 Miles per Watt Test](http://www.zianet.com/dhassall/BILLIONMPW.html) is extraordinary!

* [QRSS de W4HBK](http://pensacolasnapper.blogspot.com/) website by Bill Houghton (W4HBK) contains many useful blog posts about advanced QRSS topics. The website also has many examples of special grabs depicting rare events and atmospheric phenomena.

* [Hans Summers' website](http://www.hanssummers.com/) (the founder of [QRP Labs](https://www.qrp-labs.com/)) has many excellent resources related to RF design and early work in the QRSS space.

* [Simple QRP Equipment](https://www.qsl.net/pa2ohh/) by Onno  (PA2OHH) is a collection of fantastic resources related to QRSS transmission, reception, and software design.

* [Electronics & HAM Radio Blog](http://wa0uwh.blogspot.com/) by Eldon Brown (WA0UWH) has many fantastic articles about QRSS. Eldon's SMT band-edge transmitter inspired me to make a SMT QRSS transmitter many years later.

* [Dave Richards, AA7EE](https://aa7ee.wordpress.com/) has a fantastic website documenting many amateur radio topics including QRSS. This website has the prettiest pictures of circuit boards you'll ever see.

* [Andy, G0FTD](https://sites.google.com/view/andy-g0ftd/home) has an excellent website with many pages about radio transmitters and QRSS including a [gallery of interesting QRSS grabs](https://sites.google.com/view/andy-g0ftd/the-qrss-gallery)

* My [QRSS Hardware](https://github.com/swharden/QRSS-hardware) GitHub page collects notes and resources related to QRSS transmitter and receiver design.

<div class="text-center img-border">

![](https://swharden.com/static/2020/10/03/smt-qrss.jpg)

</div>