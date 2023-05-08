---
title: Microcontroller Action Potential Generator
date: 2017-08-20 15:12:33
tags: ["science", "circuit", "microcontroller", "python"]
---



__Here I demonstrate how to use a _single_ microcontroller pin to generate action-potential-like waveforms. __The output is similar [my fully analog action potential generator circuit](https://www.swharden.com/wp/2017-08-12-analog-action-potential-generator-circuit/), but the waveform here is created in an entirely different way. A microcontroller is at the core of this project and determines when to fire action potentials. Taking advantage of the pseudo-random number generator ([rand() in AVR-GCC's stdlib.h](http://www.nongnu.org/avr-libc/user-manual/group__avr__stdlib.html#gae23144bcbb8e3742b00eb687c36654d1)), I am able to easily produce unevenly-spaced action potentials which more accurately reflect those observed in nature. This circuit has a potentiometer to adjust the action potential frequency (probability) and another to adjust the amount of overshoot (afterhyperpolarization, AHP). I created this project because I wanted to practice designing various types of action potential _measurement_ circuits, so creating an action potential _generating_ circuit was an obvious perquisite.

{{<youtube 2s8t3UsONFs>}}

__The core of this circuit is a capacitor which is charged and discharged by toggling a microcontroller pin between high, low, and high-Z states.__ In the high state (pin configured as output, clamped at 5V) the capacitor charges through a series resistor as the pin sources current. In the low state (pin configured as output, clamped at 0V) the capacitor discharges through a series resistor as the pin sinks current. In the high-Z / high impedance state (pin configured as an _input_ and little current flows through it), the capacitor rests. By spending most of the time in high-Z then rapidly cycling through high/low states, triangular waveforms can be created with rapid rise/fall times. Amplifying this transient and applying a low-pass filter using a single operational amplifier stage of an [LM-358](http://www.ti.com/lit/ds/symlink/lm158-n.pdf) shapes this transient into something which resembles an action potential. Wikipedia has a section describing how to [use an op-amp to design an active low-pass filter](https://en.wikipedia.org/wiki/Low-pass_filter#Active_electronic_realization) like the one used here.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/20/action-potential-generator-circuit.jpg)

</div>

__The code to generate the digital waveform is very straightforward.__ I'm using PB4 to charge/discharge the capacitor, so the code which actually fires an action potential is as follows:

```c
// rising part = charging the capacitor
DDRB|=(1<<PB4); // make output (low Z)
PORTB|=(1<<PB4); // make high (5v, source current)
_delay_ms(2); // 2ms rise time

// falling part
DDRB|=(1<<PB4); // make output (low Z)
PORTB&=~(1<<PB4); // make low (0V, sink current)
_delay_ms(2); // 2ms fall time
_delay_us(150); // extra fall time for AHP

// return to rest state
DDRB&=~(1<<PB4); // make input (high Z)
```

__Programming the microcontroller__ was accomplished after it was soldered into the device using test clips attached to my ICSP ([USBtinyISP](https://www.ebay.com/sch/i.html?&_nkw=USBtinyISP)). I only recently started using test clips, and for one-off projects like this it's so much easier than adding header sockets or even wiring up header pins.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/20/ap-generator-programmer.jpg)
![](https://swharden.com/static/2017/08/20/ap-generator-programmer-close.jpg)

</div>

__I am very pleased with how well this project turned out!__ I now have an easy way to make irregularly-spaced action potentials, and have a great starting point for future projects aimed at _measuring_ action potential features using analog circuitry.


<div class="text-center img-border">

![](https://swharden.com/static/2017/08/20/ap-generator-running.jpg)
![](https://swharden.com/static/2017/08/20/ap-generator-running-2.jpg)

</div>

### Notes

*   Action potential half-width (relating to the speed of the action potential) could be adjusted _in software_ by reducing the time to charge and discharge the capacitor. A user control was not built in to the circuit shown here, however it would be very easy to allow a user to switch between regular and fast-spiking action potential waveforms.
*   I am happy that using the 1n4148 diode on the positive input of the op-amp works, but using two 100k resistors (forming a voltage divider floating around 2.5V) at the input and reducing the gain of this stage may have produced a more reliable result.
*   Action potential frequency (probability) is currently detected by sensing the analog voltage output by a rail-to-rail potentiometer. However, if you sensed a noisy line (simulating random excitatory and inhibitory synaptic input), you could easily make an integrate-and-fire model neuron which fires in response to excitatory input.
*   Discussion related to the nature of this "model neuron" with respect to other models (i.e., Hodgkin–Huxley) are on the [previous post](https://www.swharden.com/wp/2017-08-12-analog-action-potential-generator-circuit/).
*   Something like this would make an interesting science fair project

### Source Code on GitHub

*   <https://github.com/swharden/AVR-projects/>

*   <https://github.com/swharden/AVR-projects/tree/master/ATTiny85%202017-08-19%20action%20potential%20generator>
