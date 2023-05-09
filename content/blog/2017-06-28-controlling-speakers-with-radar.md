---
title: Controlling Speakers with RADAR
date: 2017-06-28 21:56:24
tags: ["circuit"]
---



__I just finished building a device that uses RADAR to toggle power to my speakers when it detects my hand waiving near them!__ I have some crummy old monitor speakers screwed to a shelf, and although their sound is decent the volume control knob (which also controls power) is small and far back on my work bench and inconvenient to keep reaching for. I decided to make a device which would easily let me turn the speakers on and off without having to touch anything. You could built a device to detect a hand waive in several different ways, but RADAR (RAdio Detection And Ranging) has got to be the coolest!

{{<youtube EIuYRhChw60>}}

__This project centers around a 5.8 GHz microwave radar sensor module__ ([HFS-DC06](http://www.icstation.com/microwave-radar-sensor-module-58ghz-waveband-392211mm-p-9551.html), $5.22 from [icstation.com](http://www.icstation.com/microwave-radar-sensor-module-58ghz-waveband-392211mm-p-9551.html), + 15% discount code _haics_) which senses distance (sensitivity is adjustable with a potentiometer) and in response to crossing a threshold it outputs a TTL pulse (the duration of with is adjustable with another potentiometer). I ran the output of the module through [divide-by-two circuit](http://www.electronics-tutorials.ws/counter/count_1.html) (essentially a [flip-flop](https://en.wikipedia.org/wiki/Flip-flop_(electronics))) so that an object-detect event would _toggle_ a line rather than pull the line high for each detection. I didn't have a cheap flip-flop IC on hand (the [74HC374](http://www.ti.com/lit/ds/symlink/cd74hct574.pdf) comes to mind, [$0.54 on Mouser](http://www.mouser.com/ProductDetail/Texas-Instruments/SN74HC374N/)) but I did have a [74HC590 8-bit binary counter](https://assets.nexperia.com/documents/data-sheet/74HC590.pdf) on hand ([$0.61 on Mouser](http://www.mouser.com/ProductDetail/Texas-Instruments/SN74HC590AN/)) which has a divide-by-two output. I used the radar sensor and this IC to produce a proximity-toggled TTL signal which enabled/disabled current flowing through a [power n-channel MOSFET](https://en.wikipedia.org/wiki/MOSFET). All together this let met create a device with two DC barrel jacks (an input and an output), and current delivery on the output could be toggled with proximity sensing.

The RADAR antenna is built into the front PCB. The back side of the module reveals the simplistic connections: VCC (5V), OUT, and GND.

<div class="text-center img-border">

![](https://swharden.com/static/2017/06/28/03module.jpg)
![](https://swharden.com/static/2017/06/28/04module.jpg)

</div>

## __Design__

__I wanted this device to be extremely simple, with a single input DC jack and single output jack and no buttons or knobs.__ It's a funny feeling making a user input device with no drill holes in the enclosure! The design is so simple it's not worth reviewing in detail. The 15V line (which in reality could be almost anything) is brought to 5V with a [LM7805 linear voltage regulator](https://www.sparkfun.com/datasheets/Components/LM7805.pdf). Decoupling capacitors are commonly placed on the input and output of the regulator, but since the function is to toggle a switch I didn't find it necessary (there is no downstream signal I wish to preserve the integrity of). The radar module has only 3 connectors: +5v, GND, and OUT. Out produces a high pulse when it detects something close. The output of the OUT signal is fed into a divide-by-two stage which is really just a [74HC590 8-bit binary counter](https://assets.nexperia.com/documents/data-sheet/74HC590.pdf) taking output of the div/2 pin. That output is fed into an [IRF510 N-channel MOSFET](http://www.vishay.com/docs/91015/sihf510.pdf) to switch current flow on the "DC output" on and off. A [Darlington transistor](https://en.wikipedia.org/wiki/Darlington_transistor) (i.e., [TIP122](http://www.mouser.com/ds/2/149/TIP122-890116.pdf)) would probably work fine too, but there would be a slightly greater voltage drop across it. Any power MOSFET would have worked, but I had a box of IRF510s on hand so I used one although they are more expensive ([$0.82 on Mouser](http://www.mouser.com/ProductDetail/Vishay-Semiconductors/IRF510PBF/)). Not shown is a status LED which is also on the output of the divide-by-2 chip (with a current limiting series resistor).

<div class="text-center img-medium">

![](https://swharden.com/static/2017/06/28/schematic3.png)
![](https://swharden.com/static/2017/06/28/75hc590_divide_by_2.png)
![](https://swharden.com/static/2017/06/28/75hc590_pinout.png)

</div>

## __Construction__

__I _glued_ the radar module to the wall of a plastic enclosure.__ Isn't radar messed-up by glue and plastic? Yes! But I'm not sensing things 50 feet away. I'm sensing a hand moving a few inches away. To this end, I experimented with how much glue and how thick plastic I needed to distort the signal enough so that it would only activate when I put my hand near it (as opposed to sitting down at my desk, which could also trigger the sensor without these attenuating structures). I found that aluminum tape further dampened the response, but luckily for the aesthetics of the build I didn't have to use it. Also, rather than take time making a PCB (or even using perfboard), I found point-to-point construction quite sufficient. I hot glued the counter IC to the radar module, wired it all together, and it was done! A little black plastic LED bezel was a nice touch with the diffuse blue LED.

<div class="text-center img-border">

![](https://swharden.com/static/2017/06/28/1083.jpg)

</div>

## __Alternative Designs__

RADAR was a cool way to accomplish this task, but there certainly are additional methods which could achieve a similar result:

*   __IR (infrared)__ - By pulsing IR and sensing the reflected signal intensity with an IR-filtered photo-transistor, you could invisibly detect presence of an object in front of the sensor. Adjusting the amplification of the photo-transistor (and/or diffusion of its lens or enclosure) could adjust for distance. In fact, many companies make [paired IR-LED / IR-phototransistor modules](https://www.adafruit.com/product/164) specifically for this task. However, if you have a TV remote control or other device which uses IR to communicate, it could screw with this signal.

*   __Sonar__ - Instead of light, pressure waves (sound) could be used to sense distance due to the time delay between an audio emission and detection of its reflection. Presumably an _ultrasonic _transducer would be used to prevent perpetual annoyance of those living in the area. [Ultrasonic distance sensor modules](https://www.sparkfun.com/products/13959) can also be found online for this purpose. These technologies are what is commonly used by vehicles to detect objects in their path while backing-up, alerting the driver with a beep. The downside of this method is that it would not work inside an enclosure. Aesthetically, I didn't want to have two silver screen-covered cans staring at me.

## __Radar Module Teardown__

__I had two of these modules on hand, so after I got this project working with one I used the other to conduct a destructive teardown.__ What I found inside was interesting! If someone were really interested, there may be some potential for hackability here. Aside from the microwave PCB goodness I found two primary ICs: the [LM2904](http://www.ti.com/lit/ds/symlink/lm2904.pdf) dual op-amp and an [ATTiny13](http://www.atmel.com/Images/2535S.pdf) 8-bit microcontroller. I was really surprised to find a microcontroller in here! With so much analog on these boards, it seemed that a timed pulse could be accomplished by a [555](https://en.wikipedia.org/wiki/555_timer_IC) or similar. A single-quantity ATTiny13 is [$0.58 on Mouser](http://www.mouser.com/ProductDetail/Microchip-Technology-Atmel/ATTINY13A-SSU) (as compared to [$0.36 for a 555](http://www.mouser.com/Semiconductors/Integrated-Circuits-ICs/_/N-6j73k?Keyword=555&FS=True&Ns=Pricing|0)) but maybe when you add the extra discrete components (plus cost of board space) it makes sense. Also, I'm not entirely sure _how_ this circuit is sensing distance and translating it into pulses so perhaps there is some more serious computation than I'm giving it credit for.

<div class="text-center img-border">

![](https://swharden.com/static/2017/06/28/teardown-3.jpg)

</div>

__The presence of an ATMEL AVR in this RADAR module is a potential site for future hacks.__ I'd be interested to solder some wires to it and see if I could extract the firmware. In any large scale commercial products the read/write access would be disabled, but with small run modules like this one seems to be there's a chance I could reprogram it as-is. If I _really_ wanted to use this layout but write a custom program for the micro I could desolder it and lay my own chip on the board. For now though, I'm really happy with how this project came out!