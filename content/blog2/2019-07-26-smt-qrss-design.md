---
title: SMT QRSS Design
date: 2019-07-26 21:00:00
tags: ["qrss", "circuit"]
---

# SMT QRSS Design

This page documents development of a voltage-controlled oscillator suitable for QRSS. Source code and PCB files are on https://github.com/swharden/QRSS-hardware

**For QRSS it's convenient to have 2 frequency shift adjustments: a coarse one to set frequency (~200 Hz), and a fine one for FSK (5 Hz).** I began with the design below allowing manual adjustment of coarse tuning, then an external input for fine tuning. Eventually I switched to a design where a single voltage controls tuning (coarse and fine). Many QRSS TX designs use a variable capacitor to set the coarse adjustment, but I don't like that design because it means you have to open your enclosure every time you want to shift frequency. If this is going to be ovenized, I'd love to close the box and do all the tuning electronically.

<div class="text-center">

![](https://swharden.com/static/2019/07/26/varactor-tuning-aj4vd-v1.png)

</div>

**This design worked pretty well.** Fixed capacitors (optionally populated) set the frequency so the crystal oscillates in the QRSS band. The coarse adjustment moves the signal around the QRSS band (100Hz). The fine adjustment is pulled high through a divider. Adjust R4 to control how wide the FSK can be.

**Real varicap diodes definitely work better than reverse-biased LEDs.** A reverse-biasd blue LED measured 60 Hz swing (with a lot of additional fixed capacitance in place to get near center frequency). Replacing this with a BB132 (I had to remove a 5pF cap to compensate) I got a swing of 159 Hz. That's more than double, and that's just one varicap. You can stack them in parallel. Real varicaps dont mind low voltage* I found out, so don't worry about avoiding that super low region like with the LED.

**Eventually I stopped trying to separate fine and coarse frequency adjustments** and just went with a single voltage for tuning. I can control voltage coarsely and finely using potentiometers, so I was happy to simplify the oscillator design by moving that complexity to the keyer/control system. This is the QRSS oscillator I came up with. It's just a [Colpitts oscillator](https://en.wikipedia.org/wiki/Colpitts_oscillator) with an output buffer. Note that the buffer will self-oscillate if the oscillator stops, so on-off-keying should be achieved downstream of this circuit. These decisions are made with maximal frequency stability in mind.

<div class="text-center">

![](https://swharden.com/static/2019/07/26/qrss-oscillator.png)

</div>

<div class="text-center img-border">

![](https://swharden.com/static/2019/07/26/pcb-design.png)

</div>

<div class="text-center">

![](https://swharden.com/static/2019/07/26/pcb-3d.png)

</div>

I'm glad I used a SMA connector, but in hindsight I should have laid it out sideways because I couldn't close the lid.

## Build Notes
* I used BB132 for the varicap
* I used 33P for C6
* For C9 I used 33p (should be NP0)
* For C11 I used 100p
* For C10 and C12 I used NP0 120p caps

<div class="text-center img-border">

![](https://swharden.com/static/2019/07/26/2019-07-26-a.jpg)
![](https://swharden.com/static/2019/07/26/2019-07-26-b.jpg)
![](https://swharden.com/static/2019/07/26/2019-07-26-c.jpg)

</div>

## Ovenization

**Ovenization is achieved using two power-resistors fixed to the metal enclosure.** A thermistor fastened to the chassis provides temperature feedback. This _chassis heater_ seems to be a winning design, as it is slow but stable. Having loose coupling between the PCB and the chassis is intentional. The whole thing is enclosed in a modestly insulative plastic enclosure. I'm very happy with this design!

## Ovenization

### QRSS Oscillators Need Ovens
My oscillator looks stable on time scales of minutes, but on time scales of hours it is obvious that it wobbles as my central air conditioning turns on and off. I could go nuts with Styrofoam, but a crystal oven (or chassis heater) is warranted.

### Why I want a chassis heater (not a oven heater)
Some DIY QRSS ovens use resistors as the heater element and package the heater and temperature sensor against the crystal. While temperature stability of the crystal is good, I prefer to thermo-stabilize all frequency-determining components (capacitors and varactors) of the oscillator circuit. For this reason, I prefer a chassis heater.

### Eventually I want a SMT PCB heater
When I get an oscillator I like using SMT parts, I'll try adding the temperature sensor and heater directly on the board. This is ideal for small PCBs. It would be cool if the board could thermo-regulate itself, then the oscillator would just need insulation, and the heater would require very low power.

### Chassis Heater Design

This section documents my thoughts and experiments related to development of a chassis heater. Since I'll build the chassis heater inside an insulated container, I'll refer to it as a chassis oven.

### Design

After running the numbers for a bunch of different power/resistor combinations, I decided to work with 50-Ohm power resistors. I'd love to have more 50-Ohm power resistors on hand to use for making dummy loads.

I settled on this part: [50 Ohm (+/- 1%) 12.5 watt resistor](https://www.mouser.com/ProductDetail/Vishay-Dale/RH01050R00FE02?qs=sGAEpiMZZMtbXrIkmrvidDNaDpN5VXc5nhpgDg1t8QQ%3D) ($2.64)

Running 12V through a single resistor would burn 2.88W of power as heat. If we wanted more heat we could add additional resistors in parallel, but this should be okay.

### Circuit
After the above considerations, this is what I came up with. I made it on a breadboard and it works well.

<div class="text-center">

![](https://swharden.com/static/2019/07/26/oven-aj4vd-resistor-heater.png)

</div>

* You can add multiple R4s in parallel for faster heating
* I ended-up replacing the TIP122 (Darlington transistor) with an IRF510 (N-channel MOSEFET) for better linear operation (since the TIP122 has such high gain)
  * This works great and the IRF510 rests partially on once stabalized
  * The IRF510 gets hot! Maybe you can mount that to the chassis too?
* You can supply it with dirty power and it doesn't seem to affect oscillator performance
* I use a multi-turn potentiometer for RV1
* R6 sets hysteresis
  * Large values promote squishy temperature control. 
  * Small values will faster responses but may oscillate
  * Remove R6 for bang-bang operation
* I suspect this design could be used as a _crystal_ oven
  * Replace Q1 with a 2N2222
  * Replace R4 with a 680 Ohm 1/4-watt resistor (~17 mA, ~200 mW)
  
### Photos

<div class="text-center img-border">

![](https://swharden.com/static/2019/07/26/2019-07-26-d.jpg)
![](https://swharden.com/static/2019/07/26/2019-07-26-e.jpg)

</div>

### More Notes
I experimented more on 2019-08-31:

* Switched to an LM335 (not a thermistor) super-glued to the chassis
* I target 3.10 mV (310 Kelvin = 37C or 100F)
* Can use LM7805 for op-amp and divider since we are using low voltages
* A tip122 is cheaper than the IRF510 and works fine


### Calculating power dissipation of a transistor heating a resistor

Consider a NPN with a collector tied to VCC (`Vcc`) and emitter dumping into a resistor (`R`) to ground. Let's say I'm driving a 50 Ohm resistor as a heater. How hot will the transistor get? Is my transistor beefy enough? To answer this I need to ***determine the peak power dissipation through a transistor into a resistive load.***

We should assume the current flowing through the resistor (`I`) will be the same as the current flowing through the transistor.

```c
// Ve is a function of R and I
Ve = R * I

// transistor voltage drop
Vce = Vcc - Ve

// power through the transistor
Pnpn = I * Vce

// substitute 
Pnpn = I * Vce
Pnpn = I * (Vcc - Ve)
Pnpn = I * (Vcc - (R * I))
Pnpn = (I * Vcc) - (I^2 * R)

// at peak power the first derivative of current is zero
Pnpn = (I * Vcc) - (I^2 * R)
d(Pnpn) = Vcc - (2 * I * R) = 0

// find the current through the resistor (= transistor) at peak power
Vcc - (2 * I * R) = 0
2 * I * R = VCC
Ipeak = VCC / (2 * R)

// substitute back into original equation
Pnpn = (Ipeak * Vcc) - (Ipeak^2 * R)
Pnpn = ((Vcc / (2 * R)) * Vcc) - ((Vcc / (2 * R))^2 * R)
Pnpn = (Vcc^2) / (2 * R) - (Vcc^2 * R) / (4 * R^2)
4 * R * Pnpn = 2 * Vcc^2 - Vcc^2
Pnpn = Vcc ^ 2 / (4 * R)
Pnpn = Vcc * Vcc / (4 * R)
Pnpn = Vcc * (I * R) / (4 * R)
Pnpn = Vcc * I / 4

// since the power through the resistor is
Pr = Vcc * I

// peak power through the NPN is 1/4 that through the resistor
Pnpn = Vcc * I / 4
```

* If I drop 12V through a 330 Ohm resistor it passes 36.4 mA of current and dissipates 436.4 mW of power. This means the transistor will dissipate 109 mW of power at its max. 
  * A 2n7000 can handle this.
  * A [0.5W 0805 300 Ohm resistor](https://www.mouser.com/ProductDetail/Panasonic/ERJ-P06J331V?qs=sGAEpiMZZMu61qfTUdNhG4N%252BbAgO2H57MCL338q%2F2SU%3D) can handle this (Mouser # 667-ERJ-P06J331V)