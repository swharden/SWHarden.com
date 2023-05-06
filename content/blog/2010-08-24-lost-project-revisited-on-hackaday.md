---
title: Lost Project Revisited on HackADay
date: 2010-08-24 21:22:37
tags: ["circuit", "old"]
---

# Lost Project Revisited on HackADay

__I somehow forgot about a cool project I made over a year ago!__ I guess dental school got in the way of my productivity. It's a little ironic how the last post was about something I made a year ago screwing up, and this one is about something I made a year ago turning out well!  Anyhow, the world's only battery powered microcontroller based handheld prime number generator I made last year (documented [here](http://www.swharden.com/blog/2009-06-10-primary-prototype-complete/), [here](http://www.swharden.com/blog/2009-06-04-prime-prototype-construction/), and [here](http://www.swharden.com/blog/2009-06-07-mcppng-nearing-completion/)) got some new exposure this morning when it was posted on [HackADay.com](http://www.HackADay.com)! 

<div class="text-center img-border img-small">

![](https://swharden.com/static/2010/08/24/hackaday_swharden_primes.jpg)

</div>

__I'm absolutely amazed by how much I learned__ back in the days when I was working with electronics in the weeks before I began dental school.  Perhaps it's also ironic that my learning decreased dramatically once I resumed graduate school... To give you an idea of how early in my electronics exploration this project was, look at the wires... they're made from phone cord! I had no wire at my apartment, so I had to scavenge it from whatever I could find, and I ended-up buying a 50ft phone cord at Wall-Mart (super-cheap I'd imagine) and harvesting the colored wires inside.

<div class="text-center img-border">

![](https://swharden.com/static/2010/08/24/img_2098.jpg)
![](https://swharden.com/static/2010/08/24/img_2119.jpg)
![](https://swharden.com/static/2010/08/24/img_2137.jpg)

</div>

__The code is a joke.__ There's no reason for this thing to generate numbers rapidly, so I used the absolute-slowest method for detecting primes possible. The schematic is a joke too.  There's hardly enough current to ignite those LEDs! Notice how the video had to be filmed in a dark room.  Ironically enough also, the crystal isn't even being used! It's just for show! I'm confident I never changed the ATTiny2313's fuse bits to rely on th external crystal, so it's probably running on the 4MHz internal RC oscillator (perhaps with the /8 fuse set by default, so 500kHz?)

{{<youtube k4Req0I7lbY>}}
