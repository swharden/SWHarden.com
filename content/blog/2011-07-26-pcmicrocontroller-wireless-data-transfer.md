---
title: PC/microcontroller "wireless" data transfer (part 1)
date: 2011-07-26 22:35:16
tags: ["circuit", "microcontroller", "old"]
---

# PC/microcontroller "wireless" data transfer (part 1)

__Several days ago I had a crazy idea.__ I was driving to Orlando to pick my wife up from the airport and it was dark and stormy on the highway and I was thinking about the backlash I got from my [Sound Card Microcontroller/PC Communication](http://www.swharden.com/blog/2011-07-09-sound-card-microcontrollerpc-communication/) project, where I used an embarrassingly simple hardware to accomplish the simple task of exchanging a few bytes of data between a PC and microcontroller (in the face of many people who adamantly prefer more complicated "traditional standard" methods). The car in front of me drove with his emergency flashers on, and at times all I could see were his lights. At that moment the crazy idea popped in my head - I wonder if I could use a PC monitor and phototransistors to send data to a microchip? I can't think of any immediate uses for this capability, but perhaps if I make a working prototype I'll stumble upon some. Either way, it sounds like a fun project!

<div class="text-center img-border">

[![](DSCN1652_thumb.jpg)](DSCN1652.jpg)

</div>

__The circuit is as simple as it gets.__ 

<div class="text-center">

[![](PHOTOTRANSISTOR-MICROCONTROLLER-CIRCUIT_thumb.jpg)](PHOTOTRANSISTOR-MICROCONTROLLER-CIRCUIT.png)

</div>

A phototransistor is exactly what it says, a photo (light-triggered) transistor (uses small current to trigger a large current). It's a [photodiode](http://en.wikipedia.org/wiki/Photodiode) with a small transistor circuit built in. Make sure you give it right polarity when you plug it in! For some reason (likely known to electrical engineers, not dental students) the larger metal piece in the plastic part, which I normally associate as negative for LEDs, should be plugged in the +5V for my photodiode. Again, make sure you hook yours up right. I purchased mine from eBay quite cheaply, but I'll bet you can find some in RadioShack.  Note that the value of the 22k resistor is important, and that your needed value may differ from mine. The resistor relates to sensitivity, the larger the value the more sensitive the device is to light. If it's too sensitive, it will sense light even when aimed at a black portion of the screen.


<div class="text-center">

[![](hardcode_thumb.jpg)](hardcode.jpg)

</div>

__Initial tests were done__ using the pins as digital inputs. This was difficult to achieve because, even as transistorized photo-diodes, it took a large difference in light to go from 5V to 0V (even past the 2.5V threshold). After a few minutes of frustration, I decided to use ADC to measure the light intensity. I use only the most significant 8 bits (ADCH). I found that in ambient light the readings are 255, and that white monitor light is around 200. Therefore my threshold is 250 (4.88V?) and I use this for logic decisions. Here's my setup showing the ADC value of each phototransistor translated into a 1 and 0 for clock (C) and data (D). Both are aimed toward the lamp, so both show a logical 1:

<div class="text-center img-border">

[![](DSCN1651_thumb.jpg)](DSCN1651.jpg)

</div>

__My first test__ involved reading the data from the image above. The clock is on the bottom line, data is on the top. Every time the clock transitions from black to white, the value of the data at that point is read (white=1, black=0) and the number is placed on a screen.  Here's what it looks like in action:

![](https://www.youtube.com/embed/lvVjsMMCx0U)

__Hopefully soon we can get a JavaScript interface going!__ Rather than swiping I'd like to just point this at the screen and let JS flash some squares for my device to read. This will allow virtually unlimited amounts of data to be transferred, albeit slowly, to the micro-controller. Here's a preliminary sketch of how to send strings.


<div class="text-center">

[![](string_thumb.jpg)](string.png)

</div>

__Remember now we're using a time domain, not a 2d barcode.__ I really stink at writing JavaScript, I'm going to have to pull in some help on this one!