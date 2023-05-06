---
title: Tenma 72-7750 Multimeter for RF Engineering
date: 2013-04-17 22:20:55
tags: ["old"]
---

# Tenma 72-7750 Multimeter for RF Engineering

> **Update:** This page reviews my initial impressions of the Tenma 72-7750. In a later article ([TENMA Multimeter Serial Hack](https://swharden.com/blog/2016-08-24-tenma-multimeter-serial-hack/)) I use Python to interface this multimeter to make it easier to log data and create plots of measurements without using the official (Windows-only) software.

__I recently got my hands on a Tenma 72-7750 multimeter.__ Tenma has a [pretty large collection of test equipment and measurement products](http://www.newark.com/jsp/search/results.jsp?N=422+2203+200023&Ntk=gensearch&Ntt=tenma&Ntx=mode+matchallpartial&isNotify=true), including [several varieties of hand-held multimeters](http://www.newark.com/jsp/search/productListing.jsp?SKUS=02J5540,02J5541,02J5542,02J5543,02J5546). The 72-7750 multimeter has the standard measurement modes you'd expect (voltage, current capacitance, resistance, conductivity), but stood out to me because it also measures frequency, temperature, and has RS232 PC connectivity. Currently it's [sale from Newark for under fifty bucks](http://www.newark.com/tenma/72-7750/multimeter-digital-handheld-3-3/dp/02J5543)! This is what mine arrived with:

<div class="text-center img-small">

[![](2013-04-06-11.09.44_thumb.jpg)](2013-04-06-11.09.44.jpg)
[![](2013-04-06-11.11.35_thumb.jpg)](2013-04-06-11.11.35.jpg)

</div>

__The obvious stuff worked as expected.__ Auto ranging, (5 ranges of voltage and resistance, 3 of current, 7 of capacitance), accurate measurement, etc. I was, however, impressed with the extra set of test leads they provided - little short ones with gator clips! These are perfect for measuring capacitance, or for clipping onto wires coming out of a breadboard. So many times with my current multimeters I end-up gator-clipping wires to my probes and taking them to what I'm measuring. I'm already in love with the gator clip leads, and know I'll have a set of these at my bench for the rest of my life.

__I was impressed by the frequency measuring ability of this little multimeter!__ When I read that it could measure up to 60MHz, I was impressed, but also suspected it might be a little flakey. This was not at all the case - the frequency measurement was dead-on at several ranges! With so many of the projects I work on being RF-involved (radio transmitters, radio receivers, modulators, mixers, you name it), I sided with this meter because unlike some of its siblings this one is rated beyond 50Mz. I hooked it up to the frequency synthesizer I built based around an [ad9850](http://www.analog.com/static/imported-files/data_sheets/AD9850.pdf) direct digital synthesizer and played around. When the synthesizer was set to various frequencies, the multimeter followed it to the digit! Check out the pics of it in action, comparing the LCD screen frequency with that being displayed on the meter:

<div class="text-center img-small img-border">

[![](2013-04-17-21.01.57_thumb.jpg)](2013-04-17-21.01.57.jpg)
[![](2013-04-17-21.02.50_thumb.jpg)](2013-04-17-21.02.50.jpg)

</div>

<div class="text-center img-border">

[![](2013-04-17-20.58.47_thumb.jpg)](2013-04-17-20.58.47.jpg)

</div>


__I also took a closer look at the PC interface.__ When I looked closely, I noticed it wasn't an electrical connection - it was an optical one! It has a phototransistor on one end, and a serial connection on the other. I'm no stranger to tossing data around with light (I made something that did this [here](http://www.swharden.com/blog/2011-07-26-pcmicrocontroller-wireless-data-transfer/), which was later featured on Hack-A-Day [here](http://hackaday.com/2011/07/28/microcontroller-communications-using-flashing-lights/)). I wondered what the format of the data was, when to my surprise I saw it spelled out in the product manual! (Go Tenma!)  It specifically says "Baud Rate 19230, Start Bit 1 (always 0), Stop bit 1 (always 1), Data bits (7), Parity 1 (odd)". Although they have their own windows-only software to display/graph readings over time, I'd consider writing Python-based logging software. It should be trivial with python, pySerial, numpy, and matplotlib. Clearly [I'm no stranger to graphing things in python](http://www.swharden.com/blog/category/python/) :)

<div class="text-center img-small">

[![](2013-04-17-21.04.28_thumb.jpg)](2013-04-17-21.04.28.jpg)
[![](2013-04-17-21.04.46_thumb.jpg)](2013-04-17-21.04.46.jpg)

</div>

__How does the photo-transistor work without power?__ I attached my o-scope to the pins and saw nothing when RS232 mode was activated on the multimeter. Presumably, the phototransistor requires a voltage source (albeit low current) to operate. With a little digging on the internet, I realized that the serial port can source power. I probably previously overlooked this because serial devices were a little before my time, but consider serial mice: they must have been supplied power! [Joseph Sullivan](http://www.clansullivan.com/joseph/index.html) has a [cool write-up](http://www.clansullivan.com/joseph/projects/laser.htm) on a project which allowed him to achieve bidirectional optical (laser) communication over (and completely powered by) a serial port. With a little testing, I applied 0V to pin 5 (GND), +5V to pin 6 (DSR, data set ready), and looked at the output on pin 3 (PC RX). Sure enough, there were bursts of easy-to-decode RS232 data. Here's the scheme Joseph came up with to power his laser communication system, which presumably is similar to the one in the multi-meter. (Note, that the cable is missing its "TX" light, but the meter has an "RX" phototransistor. I wonder if this would allow optically-loaded firmware?)

<div class="text-center img-border">

![](rs232-phototransistor-communication.jpg)

</div>

__There were a couple other things I found useful.__ Although I didn't appreciate it at first, after a few days the backlight grew on me. I've been doing experiments with photosensors which require me to turn out the lights in the room, and the backlight saved the day! Also, the meter came with a thermocouple for temperature measurement. It has it's own "ºC" setting on the dial, and displays human-readable temperature right on the screen. I used to do this with LM334-type thermosensitive current sources but it was always a pain (especially if I had one which output temperature in Kelvin!) I'm not sure exactly what's inside the one that came with this meter, but the datasheet suggests it can measure -40 through 1,000 C, which certainly will do for my experiments!

__All in all, I'm happy with this little guy,__ and am looking forward to hacking into it a little bit. There may be enough room in the case to add a hacked-together high frequency divider (a decade counter would be fantastic, divided by ten would allow measurement through 500MHz), but I might be over-reaching a bit. Alternatively, a high gain preamplifier would be a neat way to allow the sort probe to serve as an antenna to measure frequency wirelessly, rater than requiring contact. Finally, I'm looking forward to writing software to interface the RS232 output. The ability to measure, record, and display changes in voltage or temperature over time is an important part of designing controller systems. For example, an improved crystal oven is on my list of projects to make. What a perfect way to monitor the temperature and stability of the completed project! Straight out of the box, this multimeter is an excellent tool.