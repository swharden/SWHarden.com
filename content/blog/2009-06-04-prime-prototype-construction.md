---
title: Prime Prototype Construction
date: 2009-06-04 12:46:18
tags: ["circuit", "microcontroller"]
---

# Prime Prototype Construction

__Now that I've worked-out the software side of the microcontroller-powered prime number generator, it's time to start working on the hardware.__ I want to make a prototype which is far smaller and simpler than the final version but lets me practice driving lots of LEDs (30). I expect the final version to have around 80. Also, the heart of this project is an ATTiny2313 microcontroller, and for the full version I'd like to use an ATMEega8. I picked up an unfinished wooden box with a magnetic latch from Michaels. It's delicate and tends to chip when you drill it, but moving slowly I'm able to make nice evenly-spaced holes.

<div class="img-border img-micro">

[![](https://swharden.com/static/2009/06/04/img_2028_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2028.jpg)
[![](https://swharden.com/static/2009/06/04/img_2041_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2041.jpg)
[![](https://swharden.com/static/2009/06/04/img_2043_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2043.jpg)
[![](https://swharden.com/static/2009/06/04/img_2047_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2047.jpg)
[![](https://swharden.com/static/2009/06/04/img_2054_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2054.jpg)
[![](https://swharden.com/static/2009/06/04/img_2056_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2056.jpg)
[![](https://swharden.com/static/2009/06/04/img_2057_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2057.jpg)
[![](https://swharden.com/static/2009/06/04/img_2058_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2058.jpg)
[![](https://swharden.com/static/2009/06/04/img_2062_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2062.jpg)
[![](https://swharden.com/static/2009/06/04/img_2025_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2025.jpg)

</div>

__This is the circuit concept. __The chip is an ATTiny2313, sourced with 5V, where the left pins control the columns (by providing current) and the right pins control the rows (by providing ground). The "holes" at the top of the circuit represent where I hook up my PC and external power for testing purposes.

<div class="text-center">

[![](https://swharden.com/static/2009/06/04/prime-number-broken-circuit_thumb.jpg)](https://swharden.com/static/2009/06/04/prime-number-broken-circuit.png)

</div>

<blockquote class="wp-block-quote"><p><strong>Thoughts from Future Scott (10 years later, August, 2019)</strong></p><p>A+ for enthusiasm and construction but your design is... just no!</p><p>Why are you using an external crystal? </p><p>The schematic for the crystal is wrong: those capacitors should be to ground not in series!</p><p>You made the circuit diagram in InkScape!</p><p>You shouldn't drive current directly out of the microcontroller pins.</p><p>The majority of the microcontroller CPU cycles will go into managing multiplexing of the display (not calculating primes).</p></blockquote>

__After a little more work I have a functional device__ and it looks better than I expected. There are a few more features I want to add, and I want to work on the code some more, but I hope to be done tomorrow. The coolest part is that I've included an internal button which drives a pause/resume and speed-controller menu based upon the length of button presses! There's a lot of awesome stuff I want to write, but once again, I'll save it for the completed project page.

<div class="img-border img-micro">

[![](https://swharden.com/static/2009/06/04/img_2066_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2066.jpg)
[![](https://swharden.com/static/2009/06/04/img_2076_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2076.jpg)
[![](https://swharden.com/static/2009/06/04/img_2085_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2085.jpg)
[![](https://swharden.com/static/2009/06/04/img_2089_thumb.jpg)](https://swharden.com/static/2009/06/04/img_2089.jpg)

</div>

__I rendered the cover sticker wrong and all the LEDs are mislabled.__ The first LED should be 2^0 (1), and the second should be 2^1 (2), etc. Also, 2^22 and 2^23 are mislabeled - oops! But the thing really does generate, differentiate, and display \[only\[ prime numbers. Once again, videos (including demonstration of the menus and the programming options) and source code will be posted soon.