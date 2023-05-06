---
title: A Foot in the QRSS Door
date: 2009-04-30 09:26:40
tags: ["qrss", "microcontroller", "amateur radio", "old"]
---

# A Foot in the QRSS Door

__I've been very busy over the past couple weeks.__ Last Thursday my boss approached me and asked if I could work over the weekend. He wanted to complete and submit a grant by the deadline (Monday at 5 pm). To make a long story short I worked really hard (really long days) on Friday, Saturday, Sunday, and Monday to accomplish this. Monday afternoon when it was done (at about 4 pm), after which I went home and collapsed from exhaustion. I don't know how my boss does it! He worked on it far more than I did, and over that weekend he didn't sleep much. Anyway, in exchange for my over-weekend work I got Tuesday and Wednesday off.

<div class="text-center">

![](https://swharden.com/static/2009/04/30/attiny2313.jpg)

</div>

__I knew in advance that I'd have two days off to do whatever I wanted.__ I prepared ahead of time by ordering a small handful (I think 4?) of [ATMEL AVR](http://en.wikipedia.org/wiki/Atmel_AVR) type [ATTiny2313 chips from Digi-Key](http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&amp;name=ATTINY2313-20PU-ND) at $2.26 per chip. They arrived in the mail on Monday. Unlike the simple [PICAXE](http://en.wikipedia.org/wiki/PICAXE) chips which can be programmed a form of BASIC cod from 2 wires of a serial port, the AVR series of chips are usually programmed from assembly-level code. Thankfully, C code can be converted to assembly (thanks to AVR-GCC) and loaded onto these chips. The result is a much faster and more powerful coding platform than the PICAXE chips can delivery. PICAXE seems useful for rapid development (especially if you already know BASIC) but I feel that I'm ready to tackle something new.

__I built a straight-through parallel programmer__ for my ATTiny2313 chips. It was based upon the [dapa configuration](https://wikis.mit.edu/confluence/download/attachments/20512/dapa.png) and connects to the appropriate pins. To be safe I recommend that you protect your parallel port and microcontrollers by installing the proper resisters (~1k?) between the devices, but I didn't do this.

<div class="text-center img-border">

[![](https://swharden.com/static/2009/04/30/img_1555_thumb.jpg)](https://swharden.com/static/2009/04/30/img_1555.jpg)

</div>

__I decided to dive right in to the world of digital RF transmission__ and should probably go to jail for it. I blatantly violated FCC regulations and simply wired my microcontroller to change the power level given to a 3.579545 MHz oscillator. The antenna is the copper wire sticking vertically out of the breadboard.

__These crystals release wide bands of RF__ not only near the primary frequency (F), but also on the harmonic frequencies (F\*n where n=1,2,3...). I was able to pick up the signal on my scanner at its 9th harmonic (32.215905 MHz). I think the harmonic output power is inversely proportional to n. Therefore the frequency I'm listening to represents only a fraction of the RF power the crystal is putting out at its primary frequency. Unfortunately the only listening device I have (currently) is the old scanner, which can only listen above 30 MHz.

<div class="text-center img-border">

[![](https://swharden.com/static/2009/04/30/img_1550_thumb.jpg)](https://swharden.com/static/2009/04/30/img_1550.jpg)

</div>

__Remember when I talked about the illegal part?__ Yeah, I detected harmonic signals being emitted way up into the high 100s of MHz. I don't think it's a big deal because it's low power and I doubt the signal is getting very far, but I'm always concerned about irritating people (Are people trying to use Morse code at one of the frequencies? Am I jamming my neighbors' TV reception?) so I don't keep it on long. Once I get some more time, I'll build the appropriate receiver circuits (I have another matched crystal) and install a low-pass filter (to eliminate harmonics) and maybe even get a more appropriate radio license (I'm still only technician). But for now, this is a proof-of-concept, and it works. Check out the output of the scanner.

<div class="text-center img-border">

[![](https://swharden.com/static/2009/04/30/ss_thumb.jpg)](https://swharden.com/static/2009/04/30/ss.png)

</div>

__Something I struggled with for half an hour__ was how to produce a tone with a microcontroller and the oscillator. Simply supplying power to the oscillator produces a strong RF signal, but there is no sound to it. It's just full quieting when it's on, and static noise when it's off. To produce an AM tone, I needed amplitude modulation. I activated the oscillator by supplying power from the microcontroller with one pin (to get it oscillating), and fed it extra juice in the form of timer output from another pin. The fluctuation in power to the oscillator (without power-loss) produced a very strong, loud, clear signal (horizontal lines). I wrote code to make it beep. Frequency can be adjusted by modifying the timer output properties. The code in the screenshot is very primitive, and not current (doesn't use timers to control AM frequency), but it worked. I'm sure I'll write more about it later.

<blockquote class="wp-block-quote"><p><strong>Thoughts from Future Scott (August 2019, 10 years later):</strong></p><p>What a good start! But what a bad design =P</p><p>Driving a can oscillator's power pin with two microcontroller pins is not a good idea. Also, you were SO CLOSE to getting frequency shift keying to work! Rather than turning the can oscillator on/off with the microcontroller, just leave it on continuously and send a microcontroller pin to the can oscillator's VCO pin. I'm sure I didn't know what that 4th pin does when did when I originally wrote this (and most diagrams of can oscillators online leave that pin disconnected).</p><p>Either way, I'm happy this day happened - this was the start of years of hobby radio frequency circuit design!</p></blockquote>

