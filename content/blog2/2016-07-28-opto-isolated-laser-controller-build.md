---
title: Opto-Isolated Laser Controller Build
date: 2016-07-28 02:33:12
tags: ["microcontroller", "circuit", "obsolete"]
---



**This page documents the design and build of a small device to interface a [modern fiber-coupled DPSS laser](http://www.lasercentury.com/product.asp?id=612) with [old scientific hardware](http://www.coulbourn.com/product_p/h02-08.htm) designed to control mechanical relays.** This project involves analog and digital circuitry, microcontrollers, and lasers, and it turned out to be a pretty cool build so I'm sharing the design and construction process online in case it will be helpful for others or even my future self.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/28/IMG_7304.jpg)

</div>

**The existing hardware I must interface is made by [Coulbourn Instruments](http://www.coulbourn.com/) and is essentially just a large multi-channel computer-controlled DAC/ADC**. It does its job well (turning lights on and off, recording button presses, etc.), but this new task requires millisecond resolution and modulation patterns which lies outside the specs of this system and software. **My goal is to interface a free output line of this old hardware and use it to signal to a new device I build to activate the laser to produce a pulsed pattern.** This way there would be no modification to any existing equipment, and no software to install. Further, since this hardware isn't mine, I don't like the idea of permanently modifying it (or even risking breaking it by designing something which could damage it by connecting to it). The specific goal is to allow the existing software to cause the laser to fire 20 ms pulses at 15 Hz for a few dozen cycles of 5s on, 5s off. **It's also important to have some flexibility to reprogram the high speed laser stimulation pattern in the future.** Experiments are already underway and I need this device to be complete within a couple of days! As much as I'd love to go to the internet and order the perfect cheap components, make a proper PCB, and have a beautiful build completed in a month, my goal is to build this over a weekend using only using parts I already have at my home.

<div class="text-center img-micro">

![](https://swharden.com/static/2016/07/28/hardware-stack.jpg)
![](https://swharden.com/static/2016/07/28/hardware-stack2.jpg)
![](https://swharden.com/static/2016/07/28/hardware-pci.jpg)

</div>

**Probing the existing hardware revealed many surprises.** After inspecting the existing hardware setup I found an auxiliary output which could be controlled by software. This AUX port has a [frustratingly rare connector 1mm dual keyhole touchproof connector](http://shop.cephalon.eu/Braebon,-Keyhole-to-two-touchproof-(1,5mm)-connect/ItemDetails.aspx?9=GB&5=0574&11=1531) which I couldn't buy in bulk on eBay or Amazon, and couldn't figure out the part numbers of on Mouser or Digikey. The manual even says "_you may find it convenient to fit them with CI-type connectors_" which makes me wonder why it wasn't designed this way in the first place! Luckily the laboratory had an old (broken) device with that connector on it they said I could use for this build. After plugging in the connector, I used a volt meter to measure the output. To my surprise, it wasn't a [TTL signal](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic)! I expected to see my volt meter read 5V, but it read 28V! [After consulting the manual](http://www.coulbourn.com/v/vspfiles/assets/manuals/GraphicStateNotation2-101SoftwareUserGuide.pdf) I found mention of this: "_Graphic State Notation software is designed for use with our Habitest animal-behavior-analysis environments or any other animal-behavior-testing apparatus that operates on the industry-standard 28-Volt control voltage._" I was surprised that 28V signals is a standard for any industry. 

**Control voltages are negative!** Elsewhere in the manual I found the phrase "_The power base is capable of delivering 8 Amps of -28 VDC_" which made me question the voltage reading I took earlier. The voltmeter showed 28V, but that's the difference between one keyhole connector output and the other. It became apparent that it really may be 0V (GND) and -28mV (an even more curious "industry standard"). I wondered if connecting the negative terminal to ground would destroy the unit (think about how easy this would be to do! If it were a TTL signal, the first thing you would do is connect the negative terminal to ground and start sampling the positive terminal). There was even talk of me interfacing with a different output port (which I hadn't probed, so I didn't know the voltage). _Moving forward, I realized I had to tread very carefully. Doing something like connecting two grounds together could permanently damage this system!_ 

**Optical isolation should be used as a caution.** Not really knowing if I should design to expect a TTL signal, a +28V signal, or a -28V signal, I decided to design a circuit to accommodate all of the above, while achieving _total electrical discontinuity_ from whatever circuit I develop. I'm going to accomplish this using an [opto-isolator on the input](https://en.wikipedia.org/wiki/Opto-isolator). I drew the schematic using [KiCad](http://kicad-pcb.org/) as I built the board manually using through-hole construction. I considered laying-out a PCB (I have most of these components in SMT form factors too) but I knew I wouldn't manage a one-weekend turnaround if I went that direction.

<div class="text-center">

![](https://swharden.com/static/2016/07/28/schematic-4.png)

</div>

### Design Notes

*   The input should be able to accomodate any signal (TTL, CMOS, 28V, etc)
*   The input is _totally_ isolated electrically, so this should be very safe on the hardware
*   The microcontroller is a socketed [ATTiny85](http://www.atmel.com/images/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf) which I programmed with a [Bus Pirate](https://www.swharden.com/wp/2016-07-14-controlling-bus-pirate-with-python/).
*   I decided to rely on a [crystal rather than the internal RC clock](http://www.electroschematics.com/9481/avr-clock-source-fuse-bits/) to improve temporal precision of the output signal. A 11.0592 MHz crystal was chosen because I already had an abundance of them (they're [perfect for serial communication at all common baud rates](http://wormfood.net/avrbaudcalc.php)). Any crystal could be used, as long as its frequency is defined in software.
*   Capacitors were added more to ensure oscillation initiates than to bring down the oscillation frequency. (I'm told that omitting them may cause a case where the crystal doesn't resonate as well, but I've never found this in my personal experience.) A good note on microcontroller clocks is in a [Microchip PIC application note](http://ww1.microchip.com/downloads/en/appnotes/00826a.pdf).
*   I included a "test" button (momentary switch) to simulate having an input signal.
*   Note that R1 must be able to handle the current applied to it. It was mistakenly designed as 1k, and later replaced with 10k. See the bodge note at the bottom of this post for details.

### Potential Improvements

*   Forward protection diodes on the input could protect accidental reverse polarity
*   Adding an [ICSP](http://www.ladyada.net/learn/avr/programming.html) header would prevent de-socketing of the MCU if reprogramming is desired
*   The BNC output is directly from a MCU pin. A [transistor-buffered](https://en.wikipedia.org/wiki/Buffer_amplifier#Single-transistor_circuits) output design could be considered to deliver higher current for more confident control of the laser input.

**Because there is a possibility that a different output (laser control) pattern may be desired in the future, I considered whether or not I should make the output pattern user-configurable.** Adding buttons, a display, and designing a menu system in software would be a lot of work and it's unclear if a protocol change will ever actually be required, so I concluded that I'm going to build this device to the specific task at hand and extended it later if/when needed. If the end user eventually wants the ability to modulate the pattern on their own, the device they ask for would be a very different one than the one I was tasked to create. Since the current pattern is burned into a microchip, a compromise is that I could have new patterns burned into new microchips, and the end-user could change the chip (as long as it's an infrequent occurrence).

_EDIT: About a year later a modification was indeed required (something like changing 15 Hz to 40 Hz), and the solution was to burn these two patterns into two microchips. Since they're socketed, they're swappable (albiet a limited number of times). This design worked-out well._

**Is a microcontroller/crystal overkill for a system which could be accomplished using an analog circuit?** Generating 20 ms pulses at 15 Hz sounds like an easy task for a [555 timer](https://en.wikipedia.org/wiki/555_timer_IC) without the need for digital circuitry. I considered this for a while, but concluded that the advantage of the MCU (crystal-disciplined time precision) outweighed the convenience of  a purely analog circuit. A 555 timer in [astable / multi-vibrator configuration](http://www.circuitbasics.com/555-timer-basics-astable-mode/) would mostly get the job done, but you would either (1) only allow one output pattern and rely on precision passive components (which I don't have on hand), or (2) allow the end-user to adjust duty/frequency with potentiometers (which would require the output to be quantitatively monitored on an oscilloscope). There's also the issue where RC oscillators can be highly temperature sensitive, so the microcontroller/crystal design seemed like a more robust solution for reliable and defined behavior.

**I started the build** by measuring/marking drill points. I used a Dremel drill press to make the holes, then smoothed them with a deburring tool. I also drilled holes in the base of the enclosure.

<div class="text-center img-small img-border">

![](https://swharden.com/static/2016/07/28/IMG_7186.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7188.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7191.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7192.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7203.jpg)

</div>

**I had an enclosure ready to go.** I always buy enclosures in bulk, and even though nice ones tend to be expensive, having them on hand encourages me to build devices as I think of them, rather than making flaky hardware which I [have a history of doing](https://www.swharden.com/wp/2011-01-16-first-homebrew-qso-ever/) which sometimes [borders on ridiculousness](https://www.swharden.com/wp/2010-06-03-aj4vd-qrss-vd-mept/). I usually stock [unfinished Hammond diecast aluminum enclosures](http://www.alliedelec.com/hammond-manufacturing-1590g/70165610/) for making quick RF projects, and [boxes with feet and side vents](https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=aluminum+electronic+project+enclosure+box) for fancier projects, but for this task I decided to enclose everything inside a typical (but a little more costly) aluminum enclosure ordered in bulk from eBay. I love using low current LEDs, and I started going with frosted instead of clear LEDs because they're easier on the eyes. Also, I switched to mostly 3mm LEDs instead of 5MM because they look a little nicer in these small enclosures with small black bezels.

<div class="text-center img-small img-border">

![](https://swharden.com/static/2016/07/28/IMG_7191.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7206.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7204.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7208.jpg)

</div>

**I used nicer perfboard with plated holes to build this circuit.** Normally I use [cheap perfboard](https://www.circuitspecialists.com/solderable-perf-boards) with little copper rings glued to one side because it's faster to solder (the copper is so thin it heats quickly), but it's not always a good long-term solution because the copper pads have a tendency to un-stick. I rarely use this nicer perfboard (it is more expensive), but it's nice to have for more reliable builds.

<div class="text-center img-small img-border">

![](https://swharden.com/static/2016/07/28/IMG_7258.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7215.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7216.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7252.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7259.jpg)

</div>

**I marked areas of optical isolation with a black marker.** This makes it obvious where the potentially dangerous, potentially high-voltage (well, higher than TTL), potentially negative input comes in. No wires or connections should invade this space on the board. The special connector which will connect this device to the scientific hardware is on-site, and I'll have to solder it at the time of delivery/installation. I left an extra hole in the back to accommodate this wire. I didn't have any [rubber grommets](http://www.ebay.com/sch/i.html?_from=R40&_trksid=p2050601.m570.l1313.TR0.TRC0.H0.Xrubber+grommets.TRS0&_nkw=rubber+grommets&_sacat=0), but I suspect this build may have benefitted from one.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/28/IMG_7232.jpg)

</div>

**Once it was all together, the device seemed to perform well.** The test button on the back made it easy to inspect the output. I build so many RF circuits that I instinctively reached for a 50-ohm terminator, but the square wave quickly transformed into shark fins (RC curves) reminding me that and I realized 50 ohms is far too low impedance. If it's a TTL signal, let's assume it's virtually infinite impedance. I was uncertain whether or not I should drive the output directly with a microcontroller pin. There may be a need for a buffered output. The microcontroller's datasheet suggests limiting its current to 20 mA per pin (requiring termination of no less than 250 Ohms at 5V), and I'm going to move forward assuming the laser TTL input doesn't sink much current.

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2016/07/28/IMG_7284.jpg)
![](https://swharden.com/static/2016/07/28/scope.jpg)

</div>

**How should TTL timing be controlled in software?** I want this device to perform identically over long periods of time, favoring reliability and consistency over microsecond time precision. To achieve 15 Hz of 20ms pulses I need 20ms on and 46.666667 ms off. I could probably get pretty close if I wanted to, but I rounded it to 20 ms on and 46 ms off. This gives time for the instruction cycles toggling the output pins to occur (although it's on an order of magnitude faster time scale), which slightly biases the time in the right direction. I considered adding a _delay_us(666) after the _delay_ms(46) but I'm satisfied with it this knowing it's within 1% accuracy of 15 Hz and that precision is locked to that of the crystal (around 10 ppm, or 0.001%).

**Hard-coded \_delay\_ms() is somewhat inelegant.** The use of [AVR timers](http://www.atmel.com/Images/Atmel-2505-Setup-and-Use-of-AVR-Timers_ApplicationNote_AVR130.pdf) should probably be considered as an alternative strategy. Here's an [awesome guide on the topic](http://maxembedded.com/2011/06/introduction-to-avr-timers/), and [here's another](http://www.avrfreaks.net/forum/tut-c-newbies-guide-avr-timers?page=all). Timers would be preferred if I wanted the program code of the microcontroller to be free to do other things like drive menus or multiplex a display. Since this task is simply required generation of a TTL output pattern (and nothing more), the hard-coded delay method met this need, but I found it useful to consider the asynchronous strategies:

*   **Timers**: [Set the timer](http://eleccelerator.com/avr-timer-calculator/) to overflow every 1 ms. On overflow, a counting variable would be incremented and a function would be called to determine what to do. At pre-programmed time points (with respect to the counting variable), the output pin would be toggled, or the counting variable would be reset.

*   **Output compare registers:** Utilize the built-in OCR (output compare register) to turn the output signal on and off. [Set the timer](http://eleccelerator.com/avr-timer-calculator/) to overflow at 15 Hz, turning the output on. Set the OCR (to the fractional point between 0 and the maximum timer value) such that when it is passed, the output is turned off. This way 15 Hz, 20 ms pulses _would be continuously running without any code being executed_. Input sensing could simply enable and disable the timer.

*   **Input interrupts:** Why stop at timers? Polling the input pin for a TTL signal puts the chip in an infinite loop. Relying on the AVR's external (pin change) hardware interrupts could eliminate this as well. I always [rely heavily on the datasheet](http://www.atmel.com/images/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf) when setting these interrupts.

**These alternative implementations will be useful in the future** if a more accurate time source is desired, an advanced display is added, or menus are implemented which would benefit from letting the pulsing output operate in the background while accepting user input. For now, I'm happy with the blocking delay strategy.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/07/28/IMG_7265.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7262.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7301.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7300.jpg)

</div>

**After I was satisfied with construction, I started labeling the enclosure.** I want to tip my hat to [Onno Hoekstra](http://www.qsl.net/pa2ohh/) on this one, as [his webpage](http://www.qsl.net/pa2ohh/tlabels.htm) and some email correspondence helped me realize how good clear labels look when outlined and applied to aluminum enclosures. I'm using a [DYMO LetraTag LT-100T Plus](https://www.amazon.com/DYMO-LetraTag-Personal-Hand-Held-1733013/dp/B001B1FIW2/) label maker and [clear tape](https://www.amazon.com/DYMO-Labeling-LetraTag-Labelers-Black/dp/B00006B8FA). It's important to enable the black outline around the text, then I cut carefully slightly outside the outline with regular scissors, and apply the labels with a hobby knife or razor blade.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/07/28/IMG_7310.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7308.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7307.jpg)
![](https://swharden.com/static/2016/07/28/IMG_7305.jpg)

</div>

**The morning I delivered the product** and added the final proprietary connector which I didn't have at home. It's an inelegant knot-retained configuration, but I think it'll get the job done! It was a [surprisingly rare, fully shielded, keyhole-shaped touchproof connector](http://shop.cephalon.eu/Braebon,-Keyhole-to-two-touchproof-(1,5mm)-connect/ItemDetails.aspx?9=GB&5=0574&11=1531) apparently used only in medical applications. At this point, I'm thinking this connector was chosen to (A) protect the user from accidentally shorting a 28V 8A power source (that's over 200 watts!), (B) to prevent you from damaging the equipment by plugging in something that doesn't belong (could you imagine what would happen if this -28V high current source had a BNC connector and you plugged this into something expecting a 5V TTL input?), and (C) prevent you from plugging in anything that wasn't made by this company. The last option is most likely a well-intentioned attempt by the manufacturer to prevent customers from damaging their product rather than the company trying to maintain its status as a sole distributor of accessories, but it makes me wonder. I would have preferred power pole sockets, molded power connectors like those on motherboards, or even barrel connectors! Surely there's a more standard touchproof connector for moderate voltage/currents than this bizarre keyhole connector.

**I plugged the device in to the computer, attached the laser, and it worked immediately!** I wasn't really surprised that it worked (I tested it extensively at home), but it still felt good to watch the blue laser trigger as it was supposed to. Another interesting one-off project is complete, and have some interesting photos and notes about the build to share on this website. I hope this little device continues to do its job well for many years in its new laboratory home.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/28/IMG_7316.jpg)

</div>

### Microcontroller Code

```c
#define F_CPU 11059200UL
#include <avr/io.h>
#include <util/delay.h>

int main (void){
    DDRB=(1<<PB0); // set port B pin 0 as an output
    PORTB=0;       // pull all pins low
    while(1){
        while((PINB&(1<<PB2))==0){} // do nothing while the input is low
        PORTB=(1<<PB0);   // TTL ON
        _delay_ms(20);    // stay on for 20ms
        PORTB&=~(1<<PB0); // TTL OFF
        _delay_ms(46);    // stay off for 46ms
    }
}
```

**Here's the batch script I used to compile and load the code onto the microcontroller.** I compiled the code with AVR-GCC and copied it onto the microcontroller with a [Bus Pirate](https://www.swharden.com/wp/2016-07-14-controlling-bus-pirate-with-python/). Note also that I'm [setting the fuses to respect an external oscillator](http://www.engbedded.com/fusecalc/).

```bash
@echo off
del *.elf
del *.hex
avr-gcc -mmcu=attiny85 -Wall -Os -o main.elf main.c
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
avrdude -c buspirate -p attiny85 -P com3 -e -U flash:w:main.hex
avrdude -c buspirate -p attiny85 -P com3 -U lfuse:w:0xff:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m
pause
```

### Final Design

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/28/IMG_7304.jpg)

</div>

### Update: Improve Current Handling

**After a few days I got an email from someone concerned about the current handling capability of the front-end of the circuit.** It was noted that a standard 1/4 watt resistor may not be suitable for R1, as a 28V potential would stress it beyond its specs. With 28V applied, R1 (a quarter-watt resistor) would experience P=IE=28mA*28V=784mW of current! It might last (especially if pulsed), but it also might fail with time. The advantage of the R1/D1/R2 system is that the output current will be identical across a wide range of input voltages. The disadvantage is that it's hard to predict how much current R1 needs to be expected to tolerate. I could have placed five 4.7k resistors in parallel to replace R1 (this would let me handle over 1 watt of input power), but I instead simply upped it from 1kOhm to 10kOhm. This further reduced the current that the opto-isolator sees (now only about 0.2 mA) but it seems to work still. I'm satisfied with this modification, but a little disappointed I didn't catch it sooner. Note that the new input resistor (a 10k R1) should now only have to dissipate about 80mW, well within its specs.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/28/IMG_7368.jpg)

</div>

### Update: H11B1 minimum current and AC noise

**What is the minimum current required to confidently activate the optoisolator?** I considered that a 10K input resistor on 28V would only allow 2.8 mA to pass, and I was unsure if this would reliably activate the optocoupler. Considering only 3.3V will persist after the zener (a ~11.7% current retaining ratio, if that's valid), I figured that a best 330µA were passing through the opto-isolator. That seems outside of the specs of the device, because their datasheet graphs always start at 1mA. I decided to run some tests at my home to see how this device performed with lower input currents. I determined that a 10k resistor still works with 5V (500 µA into the device), but checking the output on the oscilloscope I realized that the device operates only partially, and slowly at that low voltage/current. The darlington transistor configuration is very high gain, which is the only reason this works at all, but such low currents are sensitive to parasitic capacitance and infiltrating RF currents. Because of this it seems the chip takes a few ms to activate and deactivate. Since this application only uses 5s on and 5s off inputs, it's fine for this application, but I wouldn't expect high speed pulsing of the input signal to work well. Furthermore, in my breadboard I realized I was getting funny output currents oscillating around 60Hz, which made me suspicious that the device was picking up AC somehow. I realized it was from pin 6 (the exposed darlington base). Normally the LED is so strong is blasts the device fully on or off, but hovering on the edge like this, that pin is picking up signals that influence the open state of the transistor inside. Since it's not connected to anything anyway, I cut the pin off as close to the microchip as I could, and noticed an instant improvement in 60Hz rejection. In conclusion, I wouldn't try to reliably drive an opto-isolator with a complex pattern using less than 1 mA, but it seems to work well for simple on/off control.

This is the output of the unmodified H11B1:

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/07/28/IMG_7495.jpg)
![](https://swharden.com/static/2016/07/28/SDS00008.bmp)

</div>

This is the output of the H11B1 with the base pin removed:

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/07/28/IMG_7497.jpg)
![](https://swharden.com/static/2016/07/28/SDS00010.bmp)

</div>

**Conclusion:** This was an interesting build! I'm satisfied with the use of optical isolation here to adapt two incompatible systems with unknown/unspecified input/output properties, and the lack of electrical connections between the inputs and outputs gave me high confidence to experiment along the way.