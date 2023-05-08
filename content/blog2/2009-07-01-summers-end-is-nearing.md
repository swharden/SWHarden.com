---
title: Summer's End is Nearing
date: 2009-07-01 09:40:43
tags: ["microcontroller"]
---

# Summer's End is Nearing

<div class="text-center img-border">

![](https://swharden.com/static/2009/07/01/scott_working.png)

</div>

__My favorite summer yet is reaching its end.__ With about a month and a half before I begin dental school, I pause to reflect on what I've done, and what I still plan to do. Unlike previous summers where my time was devoted to academic requirements, this summer involved a 9-5 job with time to do whatever I wanted after. I made great progress in the realm of microcontroller programming, and am nearing the completion of my prime number calculator. I'm very happy with its progress.

<div class="text-center img-border">

![](https://swharden.com/static/2009/07/01/wiremess.jpg)
![](https://swharden.com/static/2009/07/01/lightson.jpg)

</div>

__Most of the LEDs are working__ but I'm still missing a few shift registers. It's not that they're missing, so much as I broke them. (D'oh!) I have to wait for a dozen more to come in the mail so I can continue this project. Shift registers are also responsible for powering the binary-to-7-segment chips on the upper left, whose sockets are currently empty.

Since this project is on pause, I began work hacking a [VFD](http://en.wikipedia.org/wiki/Vacuum_fluorescent_display) I heard about at Skycraft. It's a 20x2 character display (forgot to photograph the front) and if I can make it light up, it will be gorgeous.

<div class="text-center">

![](https://swharden.com/static/2009/07/01/vfd.jpg)

</div>

__Here's a high resolution photo of the back panel of the VFD__. I believe it used to belong to an old cash register, and it has some digital interfacing circuitry between the driver chips (the big OKI ones) and the 9-pin input connector. I think my best bet for being able to control this guy as much as I want is to attack those driver chips, with help from the Oki C1162A datasheet. It looks fairly straightforward. As long as I don't screw up my surface-mount soldering, and assuming that I come up with 65 volts to power the thing (!) I think it's a doable project.

