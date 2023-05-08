---
title: ICS501 Simple Frequency Multiplier
date: 2016-08-31 03:57:50
tags: ["circuit", "obsolete"]
---

# ICS501 Simple Frequency Multiplier

**Today I made a high frequency multiplier using a single component: the ICS501 PLL clock multiplier** **IC.** This chip provides 2x, 5x, 8x (and more) clock multiplication using an internal phased-lock loop (PLL). At less [than a dollar on eBay](http://www.ebay.com/sch/i.html?&_nkw=ICS501), [$1.55 on mouser](http://www.mouser.com/Search/Refine.aspx?Keyword=ics501&Ns=Pricing%7c0&FS=True), and [$0.67 on Digikey](http://www.digikey.com/product-search/en/integrated-circuits-ics/clock-timing-clock-generators-plls-frequency-synthesizers/2556421?FV=fff40027%2Cfff80205&mnonly=0&newproducts=0&ColumnSort=1000011&page=1&stock=0&pbfree=0&rohs=0&k=ics501&quantity=&ptm=0&fid=0&pageSize=25), they don't break the bank and I'm glad I have a few in my junk box! I have a 10MHz frequency standard which I want to use to measure some 1Hz (1pps) pulses with higher precision, so my general idea is to use a frequency multiplier circuit to increase the frequency (to 80 MHz) and use this to run a counter IC to measure the number of clock pulses between the PPS pulses. I spent a lot of time working with the [CD4046](http://www.ti.com/lit/ds/symlink/cd4046b.pdf) micro-power phased lock loop IC which has a [phase comparator](https://en.wikipedia.org/wiki/Phase_detector) and a voltage controlled oscillator built in. It seemed this chip was the go-to for many years, but it requires external circuitry (ICs in my case) to divide by N and is intended to adjust a [VCO](https://en.wikipedia.org/wiki/Voltage-controlled_oscillator) output voltage based on the phase difference of two different inputs. Although I made some great progress using this chip, I found a few SMT ICS501 ICs in my junk box and decided to give them a try. I was impressed how easy it was to use! **I just fed it 5V and my clock signal, and it output 8x my clock signal!** Since I don't have my 10MHz reference frequency running at the moment, I tested it with a 1MHz canned oscillator. It worked great, and was so easy! I'll definitely be using this chip to multiply-up crystal oscillator frequencies to improve the precision of frequency counting.

<div class="text-center img-medium">

![](https://swharden.com/static/2016/08/31/datasheet.jpg)

</div>

**The pin connections are straightforward:** +5V and GND to pins 2 and 3, no connection for pins 7 and 8, clock goes in 1 and comes out on 5. Pins 4 and 6 are both set to +5V to yield a x8 multiplier, according to the chart. All of this is in the datasheet for the chip.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8104.jpg)

</div>

**The IC I had on hand was [SOIC](https://en.wikipedia.org/wiki/Small_Outline_Integrated_Circuit).** I don't think they make this IC in [DIP](https://en.wikipedia.org/wiki/Dual_in-line_package). Luckily, I have breadboardable breakout boards on hand. These breakout boards are identical to those sold on [dipmicro](https://www.dipmicro.com/store/PCB-SSOP-DIP28) but I got mine from ebay and they're [all over ebay](http://www.ebay.com/sch/sis.html?_nkw=SMD+SMT+IC+PCB+Adapter)!

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8111.jpg)

</div>

**I didn't feel like changing my soldering iron tip so I gave it a go with a huge wedge,** **and it worked pretty well!** I first melted a little bit of solder on all the rails, waited until it cooled, pressed the IC into the solder, then re-melted it with the iron. It was relatively easy and I had no shorts. I do have a hot air gun (which I also didn't feel like setting up and waiting for to get warm) but this worked fine...

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8113.jpg)

</div>

**Here's the test circuit.** I added a 100nF power [decoupling capacitor](https://en.wikipedia.org/wiki/Decoupling_capacitor) and a SMT LED (with a 1 kOhm current limiting resistor) so I could tell when it was powered. I am using a 1MHz can oscillator at the input of the ICS501, and capturing both outputs through a 0.1uF capacitors terminating in a 50 ohm loads (at the oscilloscope, seen better in the next photo).

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8121.jpg)

</div>

**It worked immediately with no trouble!** The top trace is the original 1MHz clock signal, and the bottom is the 8MHz trace.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/ics501-demo.png)

</div>

The frequency isn't exactly 1MHz because the adjustment pin of the can oscillator has been left floating. Also, I recognize the power supply is noisy which is also getting noise in the signals. **None of that matters, I'm just testing the concept here. The bottom line is that the ICS501 is an extremely easy way to multiply a clock frequency to beyond 100 MHz and it requires no external components!** I will definitely be using this IC in some of my future designs. I'm glad I have it! I had to search my email to see when I ordered it because I had no memory of doing so. It looks like I got them in August 2013 (3 years ago!) and never used them. Regardless, I'm happy to have found them in my junk box, and will definitely be using them from now on.

## Update: Cascading Two ICS501s for 10x Frequency Multiplication

**My ultimate goal is to build a frequency counter using a 10 MHz frequency source, multiplied to a higher value for greater precision.** Although I could achieve 8x frequency multiplication with a single ICS501, I didn't like the idea of frequency steps not being decimal. I decided to try to cascade two ICS501 chips configured to multiply by 2 then by 5 to yield 10. Supposedly this could work on a range of frequencies up through 64x multiplication, but for me generating 100 MHz from a 10 MHz reference is exactly what I need.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/08/31/IMG_8179.jpg)

</div>

**Here's my design.** It's simple. I configure S0 or S1 as floating, grounded, or high to set the multiplication factor (see the chart above).

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8175.jpg)

</div>

**Here's my implementation.** I didn't have enough space on the breakout board to fit the whole chip (I was missing a single row!). Luckily the SMT perf board is spaced perfectly for SOIC. I was surprised how easy this thing was to solder on the SMT perf board. I'm going to have to buy some more and try prototyping with it. It would be cool to get good at it. That's another story for another day though...

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8162.jpg)

</div>

**The breadboard design got way easier!** This thing now just needs power (+5V and GND), an input signal (1 MHz in this demo), and the output signal is 10x the input (10 MHz).

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8161.jpg)

</div>

**This is what the output looks like.** Signals terminate into a 10 ohm load at the level of the oscilloscope.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/SDS00018.jpg)

</div>

I had the USB drive in the thing so I went ahead and pushed the print button. Here's the actual screen capture.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/SDS00005.jpg)

</div>

**Here it is converting 10 MHz into 100 MHz.** The signals are a bit noisy, likely because both ICs are being powered together (behind the same inductor/capacitor). In a production device, each IC should have its own inductor/capacitor to isolate it from ripple on the power rail. Regardless, this works great in cascading arrangement to multiply HF frequencies to VHF frequencies. The 10MHz source is my oven controlled crystal oscillator (OCXO) which I haven't written about yet.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/31/IMG_8166.jpg)

</div>

**All in all, the ICS501 was an easy cheap single-component solution to frequency multiplication**, **and cascading two in series** easily allows me to multiply the frequency of an incoming signal. I look forward to posting details of my frequency counter build soon!