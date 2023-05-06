---
title: A Prime Idea
date: 2009-05-27 10:28:19
tags: ["old", "circuit"]
---

# A Prime Idea

__I'm completely drained of energy.__ I visited my wife's family in Tennessee last week. I left Thursday and came back Tuesday (yesterday). I drove a total of 2,180 miles. The drive to Humboldt, TN (the destination) and back is only 1,658 miles. That means that I drove over 520 miles over the 3 days _while_ at my destination. That's about 174 miles a day. At 50 MPH average speed that's about 4 hours in the car. So, 13 hour drive (each way) to get there, then 4 hours in the car every day I was there. That's a lot of car time!

__While speaking with my brother-in-law__ (who just got a BS in computer science with a minor in mathematics) I learned that a faculty member at the university challenged him to write a computer program which could find the N'th prime number (up to 10^15) for a graduate school project. I was fascinated by the idea project and the various techniques, and workarounds related to it. After working on the theory behind the software (which I tested in Python) for a few hours, I had the idea to attempt to perform a similar task at the microcontroller level.

<div class="text-center">

[![](prime_binary_thumb.jpg)](prime_binary.png)

</div>

__Here's the project I want to begin:__ I want to build a microcontroller-powered prime number generator which displays results in binary. The binary-encoded output is similar to the [binary clocks](http://www.thinkgeek.com/interests/giftsforhim/59e0/) which are nothing new. My project will calculate prime numbers up to 2^25 (33,554,432) and display the results in binary using long strips of 20 LEDs. There will be 3 rows of LEDs. The middle row (red) will simply count from 0 to 2^25. Every time it gets to a new number, the bottom row (blue) counts from 0 to the square root of the middle row. For every number on the bottom row, the remainder (modulus) of the middle/bottom is calculated. If the remainder is 0, the middle (red) number is divisible by the bottom (blue) therefore it is not prime. If the bottom number gets all the way to the square root of the middle number, the middle number is assumed to be prime and it is copied to the top row (green). The top row displays the most recent number determined to be prime.

__Technical details of the project__ further reveal its dual simplicity/complexity nature. I'll add some buttons/switches for extra features. For example, I want to be able to start the program at a number of my choosing rather than forcing it to start at 0. Also, I want to be able to adjust the speed at which it runs (I don't want the blue row to just flicker forever). The ATTiny2313 (my microcontroller of choice because I have a few extra of them) has 18 IO pins. If I get creative with my [multiplexing techniques](http://en.wikipedia.org/wiki/Multiplexed_display), I can probably run 81 LEDs from 18 pins (9 rows of 9 LEDs). I've specifically chosen against [charlieplexing](http://en.wikipedia.org/wiki/Charlieplexing) because I will be lighting many LEDs "simultaneously" and I think the degree of flicker would be far too great to satisfy my sensitive eyes, even though I could do it all with only 10 pins.

__I've decided to transistorize__ the entire project to provide a greater and more constant current to the LEDs. I'll use a set of 9 transistors to set the row that gets power (when the microcontroller powers the base, the row gets power) and another set of 9 transistors to set the LEDs in each row that light up (when the microcontroller powers the base, the LED gets grounded and lights up). To have consistently-bright, non-flickering LEDs which don't dim as more LEDs illuminate, I will add a resistor to every LED. Maybe I can get creative and utilize [10-pin resistor networks](http://www.gino-midi.nl/Electr_pagina_afbeeldingen/!SIL10_9.jpg) (one for each row) immediately after the row-selecting transistor! That will save me so much time. (I just came up with that idea - just now!) Anyway, that's my project idea.

__I'd love to make this project look nice.__ All of my other projects were housed in junky plastic or cardboard boxes (if they were housed at all!) and this is something I want to keep. I start dental school soon, and I've love to have a fancy-looking piece of artsy/geeky/electrical memorabilia so I'll never forget who I am, my roots, and my true interests. Plus, it will give me something groovy to stare at when I come home after a long day cleaning the teeth of manikins and wondering why I went to dental school \[sigh\].

__Update (nextday):__ I've been toying over some various layouts for the LEDs. I most like the rectangle and hex-rectangle configurations, and am already working on assembly of the "mini" (prototype). Here are some random images of my thinking process.

<div class="text-center">

[![](prime_layout_2_thumb.jpg)](prime_layout_2.png)
[![](g12684_thumb.jpg)](g12684.png)
[![](rect7887_thumb.jpg)](rect7887.png)

</div>