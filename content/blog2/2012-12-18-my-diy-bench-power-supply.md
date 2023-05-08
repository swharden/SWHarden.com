---
title: My DIY Bench Power Supply
date: 2012-12-18 11:30:27
tags: ["circuit"]
---



__Another thing everybody needs (and has probably built) is a simple laboratory bench power supply.__ A lot of people use things like [modified PC power supplies](http://web2.murraystate.edu/andy.batts/ps/powersupply.htm) but I wasn't in favor of this because I wanted something smaller, lower current, and cleaner (from an RF perspective).  My needs are nothing particularly high power, just something to provide a few common voltages for digital logic and small RF circuits.  This is what I came up with!

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/18/5.jpg)

</div>

In the image above you can see an ordinary LED being powered directly from the a 5V hook-up.  There is no current limiting resistor, so a lot of current is travelling through the LED, burning it up as I photographed it. The ammeter (blue number) shows it's drawing 410 mA - whoa!  The layout is pretty simple. Each red banana plug hook-up supplies a voltage (5, 5, 12, and variable respectively). Black hook-ups are ground. The black hook-up on the top left is a current-sensing ground, and current travelling through it will be displayed on the blue dial.  The right dial shows the voltage of the variable voltage supply, and can go from about 3.5 - 30.5 V depending on where the potentiometer is set. All voltage outputs are designed to put-out approximately 1A of current.

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/18/1.jpg)

</div>

__I built this using a lot of (eBay) components I had on hand.__ I often save money where I can by stocking my workbench with components I buy in bulk. Here's what I used:

*   4.5-3.0V DC volt meter - $2.08 (shipped) eBay
*   0-9.99 A ampere meter - $4.44 (shipped) eBay
*   L7805 5V voltage regulator - 10 for $3.51 ($.35 ea) (shipped) eBay
*   L7812 12V voltage regulator - 20 for $3.87 ($.19 ea) (shipped) eBay
*   LM317 variable voltage regulator - 20 for $6.15 ($0.30 ea) (shipped) eBay
*   10k linear potentiometer - 10 for 4.00 ($.40 ea) (shipped) eBay
*   banana plug hook-ups - 20 for $3.98 ($.20 ea) (shipped) eBay
*   aluminum enclosure - $3.49 (radioshack)

TOTAL: $13.60

<div class="text-center">

![](https://swharden.com/static/2012/12/18/LM317.gif)

</div>

Does the variable voltage actually work? Is the voltmeter accurate? Let's check it out.

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/18/4.jpg)

</div>

I'd say it's working nicely!  I now have a new took on my workbench.

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/18/6.jpg)

</div>

__A note about the yellow color:__ The enclosure I got was originally silver aluminum. I sanded it (to roughen the surface), then sprayed it with a yellow rustoleum spray paint. I figured it was intended to go on metal, so I might as well give it a shot. I sprayed it once, then gave it a second coat 20 minutes later, then let it dry overnight. In the future I think I would try a lacquer finish, because it's a bit easy to scratch off.  However, it looks pretty cool, and I'm going to have to start spray-painting more of my enclosures in the future.

<div class="text-center">

![](https://swharden.com/static/2012/12/18/rust.jpg)

</div>

__A note about smoothing capacitors.__ Virtually all diagrams of linear voltage regulators like the LM7805 show decoupling capacitors before and after the regulator. I added a few different values of capacitors on the input (you can see them in the circuit), but I intentionally did _not_ include smoothing capacitors on the output. The reason was that I always put smoothing capacitors in my breadboards and in my projects, closer to the actual circuitry. If I included (and relied) on output capacitors at the level of the power supply, I would be picking-up 60Hz (and other garbage) RF noise in the cables coming from the power supply to my board. In short, no capacitors on the output, so good design must always be employed and decoupling capacitors added to whatever circuits are being built.

__The input__ of this circuit is a 48V printer power supply from an archaic inkjet printer. It's been attached to an RCA jack to allow easy plugging and unplugging.