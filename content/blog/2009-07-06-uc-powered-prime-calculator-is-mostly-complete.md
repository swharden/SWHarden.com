---
title: Microcontroller-Powered Prime Number Generator
date: 2009-07-06 10:07:56
tags: ["microcontroller"]
---

# Microcontroller-Powered Prime Number Generator

__My microcontroller-powered prime number calculator is complete!__ Although I'm planning on improving the software (better menus, the addition of sound, and implementation of a more efficient algorithm) and hardware (a better enclosure would be nice, battery/DC wall power, and a few LEDs on the bottom row are incorrectly wired), this device is currently functional therefore I met my goal!

<div class="text-center img-border">

[![](primepic1_thumb.jpg)](primepic1.jpg)

</div>

__This device generates large prime numbers (v) while keeping track of how many prime numbers have been identified (N).__ For example, the 5th prime number is 11. Therefore, at one time this device displayed N=5 and V=11. N and V are displayed on the LCD. In the photo the numbers mean the 16,521,486th prime is 305,257,039 ([see for yourself!](http://primes.utm.edu/nthprime/index.php#nth)). The LCD had some history. [In December, 2003 (6 years ago) I worked with this SAME display](http://www.swharden.com/blog/2003/12/), and I even located the [blog entry on November 25'th, 2003](http://www.swharden.com/blog/2003-11-25-doh/) where I mentioned I was thinking of buying the LCD (it was $19 at the time). Funny stuff. Okay, fast forward to today. Primes (Ns and Vs) are displayed on the LCD.

<div class="text-center img-border">

[![](primepic2_thumb.jpg)](primepic2.jpg)

</div>

__In addition to the LCD, numbers are displayed in binary:__ __Each row of LEDs represents a number. __Each row of 30 LEDs allows me to represent numbers up to 2^31-1 (2,147,483,647, about 2.15 billion) in [the binary numeral system](http://en.wikipedia.org/wiki/Binary_numeral_system). Since there's no algorithm to simply generate prime numbers (especially the Nth prime), the only way to generate large Nth primes is to start small (2) and work up (to 2 billion) testing every number along the way for primeness. The number being tested is displayed on the middle row (N_test_). The last two digits of N_test_ are shown on the top left. To test a number (N_test_) for primeness, it is divided by every number from 2 to the square root of N_test_. If any divisor divides evenly (with a remainder of zero) it's assumed not to be prime, and N_test_ is incremented. If it can't be evenly divided by any number, it's assumed to be prime and loaded into the top row. In the photo (with the last prime found over 305 million) the device is generating new primes every ~10 seconds.

__I'd like to emphasize that__ this device is not so much technologically innovative as it is creative in its oddness and uniqueness. I made it because no one's ever made one before. It's not realistic, practical, or particularly useful. It's just unique. The brain behind it is an [ATMEL ATMega8 AVR microcontroller](http://thinklabs.in/shop/images/mega8.jpg) (_[What is a microcontroller?](http://en.wikipedia.org/wiki/Microcontroller)_), the big 28-pin microchip near the center of the board. (Note: I usually work with ATTiny2313 chips, but for this project I went with the ATMega8 in case I wanted to do analog-to-digital conversions. The fact that the ATMega8 is the heart of the [Arduino](http://en.wikipedia.org/wiki/Arduino) is coincidental, as I'm not a fan of Arduino for purposes I won't go into here).

___I'd like to thank my grandmother's brother and his wife (my great uncle and aunt I guess)__ for getting me interested in microcontrollers almost 10 years ago when they gave me BASIC Stamp kit ([similar to this one](http://www.colinfahey.com/ps2_mouse_and_basic_stamp_computer/2002june03_basicstamp_mousecircuit01_adj.jpg)) for Christmas. I didn't fully understand it or grasp its significance at the time, but every few years I broke it out and started working with it, until a few months ago when my working knowledge of circuitry let me plunge way into it. I quickly outgrew it and ventured into directly programming cheaper microcontrollers which were nearly disposable (at $2 a pop, compared to $70 for a BASIC stamp), but that stamp kit was instrumental in my transition from computer programming to microchip programming._

__The microcontroller is currently running at 1 MHz__, but can be clocked to run faster. The PC I'm writing this entry on is about 2,100 MHz (2.1 GHz) to put it in perspective. This microchip is on par with computers of the 70s that filled up entire rooms. I program it with [the C language](http://en.wikipedia.org/wiki/C_(programming_language)) (a language designed in the 70s with those room-sized computers in mind, perfectly suited for these microchips) and load software onto it through the labeled wires two pictures up. The microcontroller uses my software to [bit-bang](http://en.wikipedia.org/wiki/Bit-banging) data through a slew of daisy-chained [shift registers](http://en.wikipedia.org/wiki/Shift_register) (74hc595s, most of the 16-pin microchips), allowing me to control over 100 pin states (on/off) using only 3 pins of the microcontroller. There are also 2 4511-type CMOS chips which convert data from 4 pins (a binary number) into the appropriate signals to illuminate a 7-segment display. Add in a couple switches, buttons, and a speaker, and you're ready to go!

__I'll post more__ pictures, videos, and the code behind this device when it's a little more polished. For now it's technically complete and functional, and I'm very pleased. I worked on it a little bit every day after work. From its conception on May 27th to completion July 5th (under a month and a half) I learned a heck of a lot, challenged my fine motor skills to complete an impressive and confusing soldering job, and had a lot of fun in the process.

<div class="text-center img-border">

[![](primepic3_thumb.jpg)](primepic3.jpg)

</div>