---
title: QRSS and Life in Dental School
date: 2010-01-01 18:33:50
tags: ["qrss", "amateur radio"]
---



__QRSS uses extremely simple radio transmitters at extremely low power to send an extremely slow Morse code message over an extremely large distance to extremely sensitive receivers which are extremely dependent on computers to decode.__ While you might be able to send a voice message across the ocean with ~100 watts of power, there are people sending messages with _milliwatts_! The main idea is that if you send the signals slow enough, and average the audio data ([fast Fourier transformation](http://en.wikipedia.org/wiki/Fast_Fourier_transform)) over a long enough time, weak signals below the noise threshold will stand out enough to be copied visually.

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/qrss_kj4ldf.png)

</div>

__Without going into more detail than that, this is the kind of stuff I've been copying the last couple days.__ The image is a slow time-averaged waterfall-type [FFT](http://en.wikipedia.org/wiki/Fast_Fourier_transform) display of 10.140 MHz copied from a [Mosley-pro 67 yagi](http://www.mosley-electronics.com/newspage/pd2ba%20PRO-67-B%205-29-07.jpg) mounted ~180 ft in the air connected to a [Kenwood TS-940S transceiver](http://www.universal-radio.com/USED/UP52lrg.jpg). Red ticks represent 10 seconds. Therefore the frame above is ~10 minutes of audio. The trace on the image is from two different transmitters. The upper trace is from [VA3STL](http://www.qrz.com/callsign?callsign=VA3STL)'s QRSS quarter-watt transmitter from Canada [described here](http://va3stl.wordpress.com/2009/03/09/homebrew-qrss-beacon-working/) and pictured below. The lower trace is from [WA5DJJ](http://www.qrz.com/callsign?callsign=WA5DJJ)'s QRSS quarter-watt transmitter in New Hampshire, [described and pictured here](http://www.zianet.com/dhassall/QRSS.html).

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/qrss_transmitter.jpg)

</div>

__I don't know why I'm drawn to QRSS so much.__ Perhaps it's the fact that it's a hobby which only a handful of people have ever participated in. It uses computers and software, but unlike [software-defined radio](http://en.wikipedia.org/wiki/Software-defined_radio) they don't require complicated equipment, and a QRSS transmitter or receiver can be built from simple and cheap components.

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/10_01_01_00009.bmp)

</div>

__Argo: __There's a popular QRSS "grabber" software for Windows called [Argo](http://www.sdrham.com/argo/index.html). It dumps out screenshots of itself every few minutes which is nice, but it doesn't assemble them together (which is annoying). I wrote a script to assemble Argo screen captures together as a single image. It's a script for ImageJ.

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/long.jpg)

</div>

```c
makeRectangle(13, 94, 560, 320);
run("Crop");
rename("source");
frames = nSlices();
newImage("long", "RGB White", (frames - 1) * 560, 320, 1);
for (i = 0; i < frames; i++)
{
    selectWindow("source");
    setSlice(i + 1);
    run("Select All");
    run("Cut");
    selectWindow("long");
    run("Paste");
    makeRectangle(i * 560, 0, 560, 320);
}
selectWindow("source");
close();
```

__As far as life goes,__ I'm discovering that it's not the attainment of a goal that gives me pleasure; it's the pursuit of the goal. Perhaps that's why I peruse hobbies which are difficult, and further challenge myself by doing things in weird, quirky ways. I'd love to experiment more with radio, but I don't have much money to spend. Yeah, an all-band 100-watt HF/VHF/UHF rig would be nice, but I don't want to spend hundreds of dollars on that kind of equipment... Maybe when I have a "real" job and stop being a student I'll be in a better place to buy stuff like that. I built a cheap but surprisingly functional base-loaded vertical HF antenna for my apartment balcony (don't worry neighbors, it's taken inside after every use). It's mainly for receive, but I don't see any reason why it couldn't be used for QRP transmitting.

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/ant_1.jpg)

</div>

__Yes, that's an antenna made from copper pipe, wire, and toilet paper rolls. __I wound the wire around the base and created various tap points so it serves as a variable inductor depending on where I gator-clip the radio. Not pictured are 33' radials running inside my apartment serving as grounding. The antenna feeds into a [Pixie II direct conversion receiver / QRP transmitter](http://www.swharden.com/blog/images/pixie2transceiver.gif) which dumps its output to a laptop computer. I copied some [PSK-31](http://en.wikipedia.org/wiki/PSK31) transmissions from Canada with this setup. It works way better than a long / random wire antenna because it dramatically boosts signal-to-noise when tuned to the proper frequency.

<div class="text-center img-border">

![](https://swharden.com/static/2010/01/01/ant_2.jpg)

</div>

__UPDATE:__ VA3STL [mentioned me on his site](http://va3stl.wordpress.com/2010/01/01/qrss-signal-reaches-florida/)