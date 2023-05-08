---
title: Adding ADC to Microcontrollers without ADC
date: 2016-09-09 03:00:31
tags: ["circuit", "old"]
---

# Adding ADC to Microcontrollers without ADC

__I recently had the need to carefully measure a voltage with a microcontroller which lacks an analog-to-digital converter (ADC), and I hacked together a quick and dirty method to do just this using a comparator, two transistors, and a few passives.__ The purpose of this project is to make a [crystal oven](https://en.wikipedia.org/wiki/Crystal_oven) controller at absolute minimal cost with minimal complexity. Absolute voltage accuracy is not of high concern (i.e., holding temperature to 50.00 C) but precision is the primary goal (i.e., hold it within 0.01 C of an arbitrary target I set somewhere around 50 C). Voltage measurement is usually a balance of a few factors: precision, accuracy, cost, simplicity, and speed. The method I demonstrate here maximizes precision and simplicity while minimizing cost. High speed operation is not of interest (1-2 measurements per second is fine), and as mentioned before accuracy is not a chief concern as long as precision is maximized. I would feel neglectful if I didn't give a shout out to a few alternatives to this method: Using the [10-bit ADC built into most AVR microcontrollers](http://maxembedded.com/2011/06/the-adc-of-the-avr/) (my go-to for ATMega328 at ATTiny85, but the ATTiny2313 doesn't have any) [often combined with an op-amp like this](https://www.swharden.com/wp/2013-06-10-precision-temperature-measurement/), using an IC like the [MCP3208 8-channel 12-bit ADC](http://ww1.microchip.com/downloads/en/DeviceDoc/21298c.pdf) (very expensive at [$3.66 on mouser](http://www.mouser.com/Search/Refine.aspx?Keyword=mcp3208&Ns=Pricing%7c0&FS=True)) are a good option, and fancy alternative dual slope methods as described in this [really good youtube video](https://www.youtube.com/watch?v=pzXZnvEKMXs) and even mentioned nicely in the digital volt meter (DVM) / LCD driver [ICL1706 datasheet](http://www.intersil.com/content/dam/Intersil/documents/icl7/icl7106-07-07s.pdf). Those addressed, my quick and dirty idea uses only a couple cents of components and 3 pins of a microcontroller. There is much room for improvement (see my notes about a 555 timer, voltage reference, and operational amplifiers at the bottom) but this is a good minimal case starting point. This type of measurement is perfect for high precision temperature measuring using things like an [LM335](http://www.ti.com/lit/ds/symlink/lm135.pdf), [LM35](http://www.ti.com/lit/ds/symlink/lm135.pdf), or [thermistor](https://en.wikipedia.org/wiki/Thermistor).

<div class="text-center">

![](https://swharden.com/static/2016/09/09/circuit.png)

</div>

**The concept behind this method is simple:** use a current-limiting circuit to charge a capacitor at a constant rate so voltage rises linearly with time (rather than forming an exponential RC curve), and time how long that voltage takes to cross your test voltage. A circuit which compares two voltages and outputs high when one voltage surpasses the other is called a [comparator](https://en.wikipedia.org/wiki/Comparator), and many microcontrollers (including ATMEL AVRs) have analog comparators built in (which compare AIN0 and AIN1, the result of which accessable by accessing the <code>ACSR&(<span class="pl-c1">1</span><<ACO)</code>) bit value (at least for the ATMega328, according to the [datasheet](http://www.atmel.com/images/Atmel-8271-8-bit-AVR-Microcontroller-ATmega48A-48PA-88A-88PA-168A-168PA-328-328P_datasheet_Complete.pdf)). 

**I can use the AVR's comparator to time how long it takes a capacitor to charge to the test voltage, and output to that to the serial port.** _Note that I designed this entire circuit to use the most common transistor/resistors I could think of. It can be fine-tuned to increase speed or increase precision, but this is a great starting point_. To generate a constant current I need a PNP transistor (I had a 2N2907 on hand) with a voltage divider on the base and a current limiting resistor above the transistor for good measure (in retrospect, with a more carefully chosen set of values this may not be needed). This is all that's needed to charge the capacitor linearly and generate a positive ramp.

<div class="text-center img-border">

![](https://swharden.com/static/2016/09/09/testrig-1.jpg)

</div>

__My test setup is a mess, but it demonstrates this idea works well, and is stable enough to run some experiments.__ In the frame you can see the ATMega328 microcontroller (big microchip), [LM335 temperature sensor](http://www.ti.com/lit/ds/symlink/lm135.pdf) (the TO-92 closest to the MCU), a TTL FTDI serial/USB adapter (red board, top), and my USBTiny AVR programmer (blue board, right), and oscilloscope probes.

<div class="text-center img-border">

![](https://swharden.com/static/2016/09/09/scope.png)

</div>

__To prevent this linear charger from charging forever, I make the microcontroller read the comparator which compares my test voltage with that of the ramp.__ If the test voltage is reached, or if the ramp reaches a cutoff voltage first (meaning the test voltage is too high to be measured), the count (time between last reset and now) is sent to the computer via serial port, and the capacitor is discharged through a PNP resistor. In the schematic, this is the "reset" pin. Note that the "measure" pin is AVR AC0, and AC1 is the test voltage. When all this is assembled, you can see how the linear ramps are created every time the reset transistor shuts off. Note that every 10th ramp is higher than the rest (shown here as the one left from center). This is because every 10th reading the data is summed and sent to the serial port, causing a little extra time before it is reset again. While the _time value_ has been recorded of the comparator match of the test voltage and the ramp voltage, the capacitor is allowed to continue charging until the next cycle.

__Interestingly, this method is largely insensitive to power supply noise.__ I'm using an extremely noisy environment (breadboard, DIP power regulator) but the recordings are rock solid. I suspect this is because the ramps are timed based on constant current, not abbsolute voltage, and that the ramps are fast enough to not be sensitive to slow changes in voltage. In reality, I don't think I can adequately explain why the readings are so good when the supply is so shaky (the positive voltage rail is all over the place). It works, so I'm happy with it, and I'll keep pushing forward.

<div class="text-center img-border">

![](https://swharden.com/static/2016/09/09/miniterm.png)

</div>

__Lately I've been using [RealTerm](http://realterm.sourceforge.net/) as a feature-rich alternative to HyperTerminal__ and a more convenient method than requiring custom python scripts be written every time I want to interact with the serial port in a way that involves debugging or logging or other advanced features. Here you can see the real time output of this device logging time to comparator match as it also logs to disk in a text file. This is great for simultaneously logging data (from RealTerm) and graphing it (from custom python scripts).

<div class="text-center">

![](https://swharden.com/static/2016/09/09/data_touch.png)

</div>

__This is what happens when I touch the temperature sensor for about 30s.__ I'm recording the time to voltage crossing of an LM335, so the number decreases as temperature increases. Also each data point is the average (actually the sum) of 10 points. It would be trivial to create some voltage test points, create a calibration curve, and infer the voltages involved, but this is more than enough already to prove that this method is robust and clean and precise and I couldn't be more satisfied with the results! With a pair or capacitors and a few passives, this is totally implementable virtually anywhere. Considering my room is about 78F and my finger is about 98F, this 20F spread is about 1500 data points. That means each degree F is about 75 points, so I can resolve better 0.02 F (about 0.01 C) with this crude setup.

<div class="text-center">

![](https://swharden.com/static/2016/09/09/data_ac.png)

</div>

__If I let it run for about an hour, I catch my air conditioning coming on and off.__ Warmer temperature is higher voltage which means less time to charge, so the downslopes are my AC cooling my home and the up slope is my home passively warming. The fluctuations are only about 100 units which I (backwards calculate) assume are about 1-2 F.

__These numbers seem so arbitrary! How can we calibrate this?__ This opens up a Pandora's box of possible improvements. I'll close by saying that this project works great exactly how it is to meet my needs. However, some modifications could be made to change the behavior of this device:

*   __Slowing things down: __A larger capacitor value (or higher resistor value) would increase the time or charging, lengthen the time to comparator threshold crossing, and increase precision. The readings would be slower (and more susceptible to noise), but it's an option.
*   __Self-calibration:__ Components (Rs and Cs) are sensitive to temperature and charge time can fluctuate with age, wear, temperature, etc. To self-calibrate with each sweep, add an additional comparator step which compares voltages between a [precision voltage reference](http://www.ti.com/lit/an/slyt183/slyt183.pdf) and your ramp would be a way to self-calibrate your ramp charge rate with each sweep. Optimally do this with two voltage references (3.3V and 1.8V are common) but comparing 0V to a single voltage reference would be a great step.
*   __Don't have the microcontroller gate:__ A 555 is perfectably capable of generating pulses to reset the ramp every so often, and frees up a pin of the microcontroller.
*   __Use an op-amp for constant current charging.__ It seems like a lateral move, but if your deign already has an op-amp chances are there may be some unused amps, so eliminate a transistor for this purpose! Check out the constant current source section from TIs [handbook on operational amplifier applications](http://www.ti.com/lit/an/sboa092a/sboa092a.pdf).
*   __Use an op-amp for the comparator(s).__ The microcontroller's comparator is handy, but if yours doesn't have one (or you don't feel like using one) configuring an unused op-amp stage as a comparator is a good option. The digital output could also trigger an interrupt on the digital input of a MCU pin as well!
*   __Use timer and counters to measure time__ while using an external interrupt to gate the count. Your microcontroller's on-board counter is likely extremely powerful so utilize it! This example doesn't use it actually, but using it would let you count up to the CPU clock's frequency of ticks between ramp starts and the comparator match.
*   __Eliminate the microcontroller.__ Yeah, you heard me. If you use an op-amp keep resetting the ramps, and op-amp comparators to generate digital outputs of threshold crossings, you can use a standard counter (configured to latch then clear when the reset event is engaged by the 555 which induces resetting of the ramp by draining the capacitor), just use a counter IC to capture the value. You can clock it as fast as you want! You could even have it output its value directly to LED or LCD displays. In fact, this is how some digital volt meters work without the need for a microcontroller.

>  All code used in this project is available on [its GitHub page](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202016-09-07%20ramp%20DVM)