---
title: Hacking a Cheap Ammeter / Voltmeter to Provide a Bluetooth PC Interface
date: 2016-09-19 11:46:11
tags: ["circuit"]
---

# Hacking a Cheap Ammeter / Voltmeter to Provide a Bluetooth PC Interface

__I love analyzing data, so any time I work with a device that _measures_ something, I usually want to save its output.__ I've lately come to enjoy the cheap panel-mount volt meters and current meters on eBay, and figured it would be cool to hack one to provide PC logging capability. After getting a few of these devices for [~$8 each on eBay](http://www.ebay.com/sch/i.html?_nkw=ammeter+voltage+current+mA+LED) and probing around, I realized they didn't output measurement data on any of the pins (not that I really expected they would), so I coded a microcontroller to watch the lines of the [multiplexed](https://en.wikipedia.org/wiki/Multiplexed_display) 7-segment display and figure out what the screen is displaying (an odd technique I've done [once](https://www.swharden.com/wp/2011-07-11-aj4vd-arsenal-recently-expanded/) or [twice](https://www.swharden.com/wp/2013-06-22-adding-usb-to-a-cheap-frequency-counter-again/) before), then send its value to a computer using the microcontroller's UART capabilities. Rather than interfacing a traditional serial port (using a [MAX232](https://www.swharden.com/wp/2009-05-14-simple-case-avrpc-serial-communication-via-max232/) level converter, or even a [TTL-level USB serial adapter](http://www.ebay.com/sch/i.html?_nkw=TTL+USB+serial+adapter)) I decided to go full-scale-cool and make it wireless! I succeeded using a [HC-06](https://www.olimex.com/Products/Components/RF/BLUETOOTH-SERIAL-HC-06/resources/hc06.pdf) Bluetooth serial adapter which you can find [on eBay for ~$3](http://www.ebay.com/sch/i.html?_nkw=hc-06). Although I have [previously used custom software to hack the output of a TENMA multimeter](https://www.swharden.com/wp/2016-08-24-tenma-multimeter-serial-hack/) to let me log voltage or current displayed on the multimeter, _now I can measure current and voltage at the same time _(wirelessly no less) and this is a far less expensive option than dedicating a multimeter to the task! The result is pretty cool, so I took pictures and am sharing the build log with the world.

![](https://www.youtube.com/embed/fp7uuyBCSvI)

**The video summarizes the project,** and the rest of this page details the build log. All of the code used to program the microcontroller (AVR-GCC), interface the device with the Bluetooth serial adapter, and plot the data (Python) is <a href="https://github.com/swharden/AVR-projects/tree/master/ATMega328%202016-09-15%20CVM">available as part of a GitHub project</a>.

<div class="text-center img-border">

[![](IMG_8436_thumb.jpg)](IMG_8436.jpg)

</div>

__This is what one of these modules looks like, and how it is intended to be used.__ One of the connectors has 3 wires (black = ground, red = power to run the display (anything up to 30V), and yellow = voltage sense wire). The other connector is thicker and is the current sense circuit. The black wire is essentially short-circuited to ground, so unfortunately this can only be used for low-side current sensing.

<div class="text-center img-border">

[![](IMG_8134_thumb.jpg)](IMG_8134.jpg)

</div>

__The side of the display indicates which model it is.__ Note that if you wish to buy your own panel mount meters, look carefully at their current measuring range. Most of them measure dozens of amps with 0.1 A resolution. There are a few which only measure <1 A, but down to 0.1 mA resolution. This is what I prefer, since I rarely build equipment which draws more than 1 A.

<div class="text-center img-border">

[![](IMG_8138_thumb.jpg)](IMG_8138.jpg)

</div>

__On the back you can see all of the important components.__ There's a large current shunt resistor on the right, solder globs where the through-hole 4 character [7-segment displays](https://en.wikipedia.org/wiki/Seven-segment_display) fits in, and the microcontroller embedded in this device is a [STM8S003 8-Bit MCU](http://www.kosmodrom.com.ua/pdf/STM8S003.pdf). This chip has UART, SPI, and I2C built-in, so it may be technically possible to have the chip output voltage and current digitally without the need for a man-in-the-middle chip like I'm building for this project. However, I don't feel like reverse-engineering the hardware and software which takes measurements of voltage and current (which is an art in itself) and also figure out how to drive the display, so I'm happy continuing on developing my device as planned! I did probe all the pins just to be sure, and nothing looked like it was outputting data I could intercept. That would have been too easy!

<div class="text-center img-border">

[![](IMG_8142_thumb.jpg)](IMG_8142.jpg)

</div>

__I snapped the device out of its plastic frame__ to be able to access the pins more easily.

<div class="text-center img-border">

[![](IMG_8154_thumb.jpg)](IMG_8154.jpg)

</div>

__I then soldered-on headers to help with reverse-engineering the signals.__ Note that this was part of my investigation phase, and that these header pins were not needed for the end product. I have multiple panel mount ammeter / voltmeter modules on hand, so I left this one permanently "pinned" like this so I could access the pins if I needed to. A quick check with the continuity tester confirmed that every segment of every character (of both displays) is continuous (wired together).

<div class="text-center img-border">

[![](IMG_8443_thumb.jpg)](IMG_8443.jpg)

</div>

__These headers made it easy to attach my 16-channel logic analyzer.__ I'm using an off-brand [Saleae compatible](https://www.saleae.com/) logic analyzer. Their software is open source and very simple and easy to use. Saleae sells their official logic analyzers (which are well made and company supported) on their website, but they are expensive (although probably worth it). I purchased an eBay knock-off logic analyzer ($40) which "looks" like a Saleae device to the computer and works with the same open source software. If I were really serious about building professional products, I would certainly invest in an official Saleae product. For now, this is a good option for me and my hobby-level needs. An 8-channel version if as low as [$10 on eBay](http://www.ebay.com/sch/i.html?_nkw=saleae+8+channel), and [$149 from Saleae](https://www.saleae.com/originallogic).

<div class="text-center img-border">

[![](IMG_8447_thumb.jpg)](IMG_8447.jpg)

</div>

__Connections are straightforward.__ I began probing only a single display. This is a good time to mention that an understanding of display multiplexing is critical to understanding how I'm reading this display! If you don't know what a multiplexed display is, [read up on the subject](https://en.wikipedia.org/wiki/Multiplexed_display) then come back here. It's an important concept. While you're at it, do you know what [charlieplexing](https://en.wikipedia.org/wiki/Charlieplexing) is?

<div class="text-center img-border">

[![](IMG_8460_thumb.jpg)](IMG_8460.jpg)

</div>

__After gazing at the screen of squiggly lines,__ I was able to piece together which signals represented characters (due to their regularity) and which represented segments (which changed faster, and were more sporadic).

<div class="text-center img-border">

[![](IMG_8463_thumb.jpg)](IMG_8463.jpg)

</div>

__I'll be honest and say that I cheated a bit,__ using a very high value current limiting resistor and applying current (backwards) into the pins when the device was unplugged. I manged to illuminate individual segments of specific characters in the LCD. This supported what I recorded from the logic analyzer, and in reality could have been used to entirely determine which pins went to which characters/segments.

<div class="text-center img-border img-small">

[![](IMG_8594_thumb.jpg)](IMG_8594.jpg)

</div>

__Here's what I came up with!__ It's not that complicated: 16 pins control all the signals. The microcontroller raises all lines "high" to only one character at a time, then selectively grounds the segments (A-H) to pass current through only the LEDs intended to be illuminated. Characters are numbers and segments are letters. Note that "A" of the top display (voltage) is connected to the "A" of the second display (current), so both rows of 4 characters make 8 characters as far as the logic is concerned. The transistor isn't really a discrete transistor, it's probably the microcontroller sinking current. I used this diagram to conceptualize the directionality of the signals. The sample site of letters is _high_ when a letter is illuminated, and the sample site of a segment is _low_ when that segment is illuminated (the sample site of the segment is the base of the imaginary transistor).

<div class="text-center img-border">

[![](logic_thumb.jpg)](logic.png)

</div>

__Knowing this,__ I can intentionally probe a few segments of a single character. Here is the logic analyzer output probing the second character (top), and two representative segments of that character (bottom). You can see the segments go nuts (flipping up and down) as other segments are illuminated (not shown). If you look closely at the blue annotations, you can see that each character is illuminated for about 1 ms and repeats every 13 ms.

<div class="text-center img-border">

[![](IMG_8471_thumb.jpg)](IMG_8471.jpg)

</div>

__Now it was time to make my device! I started with a new panel meter and an empty project box.__ By this point I had reverse-engineered the device and concluded it would take 16 inputs of a microcontroller to read. I chose an [ATMega328](http://www.atmel.com/images/Atmel-8271-8-bit-AVR-Microcontroller-ATmega48A-48PA-88A-88PA-168A-168PA-328-328P_datasheet_Complete.pdf) which was perfect for the job (plenty of IO) although I could have used a much less powerful microcontroller if I wanted to interface an IO expander. The [MCP23017 16-bit IO expander](http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf) may have been perfect for the job! Anyway, I drilled a few circular holes in the back with a step-bit and cut-away a large square hole in the front with a nibbler so everything would snap-in nicely.

<div class="text-center img-border">

[![](IMG_8482_thumb.jpg)](IMG_8482.jpg)

</div>

__I soldered wires to intercept the signal__ as it left the device's microcontroller and went into the LED display.

<div class="text-center img-border">

[![](IMG_8517_thumb.jpg)](IMG_8517.jpg)

</div>

__I then soldered the wires directly to my microcontroller.__ I also have an extra header available for programming (seen at the bottom) which I was able to remove once the software was complete. The red clip is clamping the serial Tx pin of the microcontroller and capturing the output into a USB serial adapter. Initially I debugged this circuit using the microcontroller's on-board RC oscillator (1MHz) transmitting at 600 baud. I later realized that the serial bluetooth module requires 9600 baud. Although I could hack this with the internal RC clock, it was very unstable and garbage characters kept coming through. Luckily I designed around the potential of using an external crystal (pins 9 and 10 were unused) so it was an easy fix to later drop in a 11.0592 MHz crystal to allow stable transmission at 9600 baud.

<div class="text-center img-border">

[![](IMG_8548_thumb.jpg)](IMG_8548.jpg)

</div>

__Now you can see__ the power regulation (LM7805) providing power to the MCU and wireless bluetooth module. Here's the [HC-06 datasheet](https://www.olimex.com/Products/Components/RF/BLUETOOTH-SERIAL-HC-06/resources/hc06.pdf) (which is similar to HC-05) and [another web page demonstrating how to use the breakout board](https://mcuoneclipse.com/2013/06/19/using-the-hc-06-bluetooth-module/). Also, I added a switch on the back which switches the voltage sense wire between the power supply and a sense connector which is on the back of the project box (red plastic banana jack).

<div class="text-center img-border">

[![](IMG_8554_thumb.jpg)](IMG_8554.jpg)

</div>

__The bluetooth adapter expects 3.3V signals,__ so I added a quick and easy zener diode shunt regulator. I could have accomplished this by running my MCU on 3.3V (I didn't have 3.3V regulators on hand though, and even so the module wants >3.6V to power the wireless transmitter) or perhaps a voltage divider on the output. On second thought, why did I use a zener ($!) over a resistor? Maybe my brain is stuck thinking about [USB protocol standards](http://vusb.wikidot.com/hardware).

<div class="text-center img-border">

[![](IMG_8557_thumb.jpg)](IMG_8557.jpg)

</div>

__Since the chip was unstable__ transmitting 9600 baud, I tightened it up using a 11.0592 MHz crystal. The advantage of making your entire circuit look sketchy is that bodge jobs like this blend in perfectly and are unrecognizable!

<div class="text-center img-border">

[![](IMG_8563_thumb.jpg)](IMG_8563.jpg)

</div>

__A quick reprogram__ to set the AVR fuses to switch from internal clock to external full-swing crystal was easy thanks to the female header I was able to pop out. I only recently started soldering-on headers like this with ribbon cable, but it's my new favorite thing! It makes programming so easy.

<div class="text-center img-border">

[![](IMG_8559_thumb.jpg)](IMG_8559.jpg)

</div>

__I packed it all in__ then added hot glue around the primary components (not shown). Again, if this were a production product I would have designed the hardware very differently. Since it's a one-off job, I'm happy with it exactly like it is! It works, and it withstands bumps and shakes, so it's good enough for me.

<div class="text-center img-border">

[![](IMG_8581_thumb.jpg)](IMG_8581.jpg)

</div>

__I tested on a big piece of electrical equipent I'm building on the other side of the room.__ This device has its own 13.8V regulated power supply (and its own shelf!), so the wireless capability is fantastic to have. I just dropped this device between the power supply and the device under test. Rather than record the power supply voltage (which would always be a boring 13.8V) I decided to record a voltage test point of interest: the point just downstream of an LM7809 voltage regulator. I expected this voltage to swing wildly as current draw was high, and was very interested to know the voltage of this test point with respect to current draw. Although I have [previously used custom software to hack the output of a TENMA multimeter](https://www.swharden.com/wp/2016-08-24-tenma-multimeter-serial-hack/) to let me log voltage or current of this exact circuit, now I can measure both at the same time! Additionally, this is a far less expensive option than dedicating a multimeter to the task.

<div class="text-center img-border img-small">

[![](IMG_8584_thumb.jpg)](IMG_8584.jpg)

</div>

__I'm using [RealTerm](http://realterm.sourceforge.net/)__ to access the serial port and log its output to a text file.

<div class="text-center img-border img-small">

[![](IMG_8590_thumb.jpg)](IMG_8590.jpg)

</div>

__A quick python script__ lets me graph the voltage/current relationship with respect to time. The (short) code to do this is [on the GitHub page](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202016-09-15%20CVM), and is demonstrated in the YouTube video.

<div class="text-center">

[![](demo_thumb.jpg)](demo.png)

</div>

__Here's some data__ which shows the relationship between voltage (red trace) probed just downstream of an LM7809 voltage regulator and the total current draw of the system (blue trace). This data was recorded in real time, wirelessly, from across the room! This is exactly the type of interesting reading I was hoping to see.

<div class="text-center img-border">

[![](IMG_8599_thumb.jpg)](IMG_8599.jpg)

</div>

__Now that it's all together, I'm very happy with the result!__ This little device is happy serving as a simple voltage/current display (which is convenient in itself), but has the added benefit of continuously being available as a Bluetooth device. If I ever want to run an experiment to log/graph data, I just wirelessly connect to it and start recording the data. This build was a one-off device and is quite a hack (coding and construction wise). If I were interested in making a product out of this design, construction would greatly benefit from surface mount components and a PCB, and perhaps not necessitate super glue. For what it is, I'm happy how it came out, pleased to see it as a Bluetooth device I can connect to whenever I want, and I won't tell anyone there's super glue inside if you don't.
>  Code used for this project is available at [GitHub](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202016-09-15%20CVM)