---
title: Minimal Radio Project Continues...
date: 2011-02-09 00:18:26
tags: ["circuit", "amateur radio", "obsolete"]
---

# Minimal Radio Project Continues...

__I got a big bag of fresh, new, copper clad PC board__ and I now wish I purchased a big pack months ago! Don't laugh at me, but I was buying 4''x6'' sheets of it at Radio Shack for about $5 a pop - ouch! I probably purchased 3 boards in my lifetime, but at that price you can imagine how careful I was not to use them. I soldered minimally to them, and only used them for the most important, established projects.  Wake up Scott! If your _experimental platform_ actually _inhibits_ experimentation, there's something fundamentally wrong.  Anyway, I got a stack of the stuff and I no longer hesitate to grab a fresh board and start working. I made some progress today simplifying my ultra-minimalist functional radio project. Here's what I came up with!

{{<youtube KTQZzNkMuC8>}}

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5278.jpg)

</div>

As you can see, it's running on 9V batteries! The frequency counter has its own 9V battery and a spiffy new hand-me-down case (originally used for a power supply I think, before which it was a watch case!). The IC is a SA602, SA612, or NE602 (all about the same) direct conversion receiver (Gilbert cell mixer). 

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5275.jpg)

</div>

I now have a small battery powered handheld frequency counter. SWEET! I need to contrive a spectacular case for it. I can't wait! It's probably the most impressive thing I've ever made with respect to the "cool factor". Does it look like a bomb? That probably makes it cooler! It just needs a big red on/off switch labeled "MISSILE LAUNCH", then it'll be the coolest thing on the planet! ... moving on ... <a <a="" href="http://www.SWHarden.com/blog/images/IMG_5261.JPG">

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5261.jpg)

</div>

This is the receiver component. It's about as simple as it gets. No antenna or headphone connector is attached, but doing this is trivial! A resonant front-end filter might make it more sensitive, and add some complexity, so comparisons are needed to get a feel for how much better it really is with one attached. 

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5263.jpg)

</div>

For this board, I added a buffer chip (74HC240) to take the pretty sine wave and turn it into a higher-power square wave...

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5284.jpg)

</div>

The quality of the oscillator is reflected in the smoothness of the sine wave (purity?) and its amplitude (indicating high Q?), though more investigation/research is required to fully understand what makes a good oscillator circuit for this chip. My strategy has been to throw components in the air, let them fall randomly, and eventually something happens and the thing starts oscillating...

<div class="text-center img-border">

![](https://swharden.com/static/2011/02/09/IMG_5282.jpg)

</div>