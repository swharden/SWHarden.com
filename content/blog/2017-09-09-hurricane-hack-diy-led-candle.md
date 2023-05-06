---
title: Hurricane Hack - DIY LED Candle
date: 2017-09-09 11:27:43
tags: ["circuit"]
---

# Hurricane Hack - DIY LED Candle

**Florida is about to get hit by a massive hurricane, and my home town is in the direct path!** I am well prepared with lots of food, water, and communications equipment. While the storm itself is dangerous, part of getting ready for it means preparing for the potential to be out of power for weeks. A staple go-to for light when the power is out is candles. Instinctively people tend to reach for candles and kerosene lamps (in Florida they're called hurricane lanterns). However, these sources of light can be extremely dangerous!

<div class="text-center img-border img-small">

[![](https://swharden.com/static/2017/09/09/livehere_thumb.jpg)](https://swharden.com/static/2017/09/09/livehere.jpg)

</div>

**With the storm one day away, my roommates and I began pooling our emergency supplies in the living room and I grew uneasy about how many matches and candles were accumulating.** With severe weather, wind, falling trees, tornadoes, and projectiles blowing around there is an appreciable risk of knocking-over a flame and starting a fire. This risk multiplies when you consider that people often fall asleep with flames running, perhaps even in another room! 

**I thought how great it would be to have a bunch of [LED candles](https://en.wikipedia.org/wiki/Flameless_candles), but there is absolutely no way I can buy one now.** Although I could just leave a flashlight on shining at the ceiling, it would produce too much light and the batteries would die before long. With the storm one day away, every store in this town is out of water, most groceries are out of canned foods, and most of the gas stations are out of gas and have locked up. Flashlights, radios, and LED candles are surely gone from all the stores as well. I decided to hack-together several LED candles to use around the house over the next several days, and the result came out great!

<div class="text-center">

[![](https://swharden.com/static/2017/09/09/hurricaine-diy-led-candle_thumb.jpg)](https://swharden.com/static/2017/09/09/hurricaine-diy-led-candle.jpg)

</div>

**I taped together 2 AA batteries and soldered a resistor and a white LED in series with jumper to serve as an on/off switch.** It's not yellow and doesn't flicker like fancy LED candles, but who cares? This is perfectly functional, and for lighting a room I would say it's a superior alternative to fire-based candles when the power is out for long periods of time. The batteries will last _much_ longer than they would if we just turned on a flashlight and aimed it at the ceiling too. My white LEDs (generic low current clear 5mm LEDs) have about a 20º light emission angle. To improve its function as a room light I taped a sheet of paper around a glass cup and set it over the top to act as a light diffuser. This couldn't be simpler!

<div class="text-center img-border img-medium">

[![](https://swharden.com/static/2017/09/09/063_thumb.jpg)](https://swharden.com/static/2017/09/09/063.jpg)

</div>

**If the light diffuser is removed this thing works pretty well as a flashlight.** I practiced walking around a dark closet and pointing it around and was impressed at how much it is able to illuminate a relatively narrow area. _This is a good time to add a basic warning reminding people that soldering directly to batteries is potentially dangerous for the person (and may be destructive to the battery) and it should be avoided. Battery holders are superior, and batteries with solder tabs already on them are a superior alternative to generic batteries._

# 3xAAA Version

**I found a box of battery holders and decided to make a second version of this device.** I felt better about this one since I didn't need to solder directly to any batteries. A dot of super glue is all it took to secure the LED to the enclosure, and it even stands upright!

<div class="text-center img-border img-small">

[![](https://swharden.com/static/2017/09/09/081_thumb.jpg)](https://swharden.com/static/2017/09/09/081.jpg)
[![](https://swharden.com/static/2017/09/09/078_thumb.jpg)](https://swharden.com/static/2017/09/09/078.jpg)

</div>

# How long will it last?

I'll use some scratch match to predict how long this device will stay lit. I'll run the math first for the 2xAA version. Placing an ammeter in the circuit while the LED was on revealed it consumes **1.8 mA** of current.  [PowerStream has a great website showing battery discharge curves](https://www.powerstream.com/AA-tests.htm) for various consumer grade batteries. Eyeballing the graph it looks like most batteries doesn't start to drop voltage significantly until near the end of their life. To make calculations simple, let's just use the mAH (milliamp hour) rating that the manufacturer provides... except I can't find where Amazon specs their "Amazon basics" battery. A consumer review indicates 997 mAh at 100 mA discharge rate. I'm sure our duration would be far beyond this since we are drawing less than 1/50 of that much current, but let's just say 1000 mAh to be conservative. We can double that since we are using two AA batteries in this circuit, so 2000 mAh / 1.8 mA = **46 days**. Interestingly, the 3xAAA battery presents a larger voltage to the led/resistor so it draws more current (6.3 mA) and 3000 mAh / 6.3 mA it is expected to last only about 19 days. I could increase the value of the resistor to compensate, but it's already built and it's fine enough for my needs.

<div class="text-center img-border img-small">

[![](https://swharden.com/static/2017/09/09/088_thumb.jpg)](https://swharden.com/static/2017/09/09/088.jpg)
[![](https://swharden.com/static/2017/09/09/091_thumb.jpg)](https://swharden.com/static/2017/09/09/091.jpg)

</div>

**When the storm has passed and things return to normal, I'll consider making a few different designs** and testing how long they actually last. Many battery tests use relatively high current challenges so their discharge finishes in days rather than weeks or months... but with a sensitive voltmeter circuit attached to a logging raspberry pi or something, I'd be interested to see the battery discharge curve of a DIY LED candle on a weeks/months timescale! For now I feel prepared for the upcoming storm, and with several DIY LED candles to light my home instead of actual candles, I'll feel safer as well.

## UPDATE

**Two months later (Nov 11, 2017) this thing is still going strong!** I've left it on continuously since it was built, and I'm truly surprised by how long this has lasted... I'm going it continue leaving it running to see how much longer it goes. For future builds I will add more LEDs and not be so concerned about longevity. It may be work noting that a build like this would have been great for residents of Puerto Rico, because much of that island is _still_ without power. This is a photograph in a dimly-lit room after more than 2 months continuous use:

<div class="text-center img-border">

[![](https://swharden.com/static/2017/09/09/IMG_0303_thumb.jpg)](https://swharden.com/static/2017/09/09/IMG_0303.jpg)

</div>