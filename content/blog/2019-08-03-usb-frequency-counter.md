---
title: USB Frequency Counter
date: 2019-08-03 21:15:00
tags: ["circuit"]
---

# USB Frequency Counter

**I built a frequency counter with a USB interface** based around a [74LV8154](https://www.ti.com/lit/ds/symlink/sn74lv8154.pdf) 32-bit counter, FTDI [FT230XS](https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT230X.pdf) (USB serial adapter), and an [ATMega328](https://www.microchip.com/wwwproducts/en/ATmega328) microcontroller. I've used this same counter IC in some old projects ([1](https://swharden.com/blog/2011-03-14-frequency-counter-finished/), [2](https://swharden.com/blog/2011-02-12-wideband-receiver-works/), [3](https://swharden.com/blog/2011-02-09-minimal-radio-project-continues/), [4](https://swharden.com/blog/2011-02-04-frequency-counter-working/), [5](https://swharden.com/blog/2011-01-28-home-brew-transceiver-taking-shape/)) this time I decided to I design the circuit a little more carefully, make a PCB, and use all surface-mount technology (SMT).

<div class="text-center img-medium">

[![](https://swharden.com/static/2019/08/03/curved2_thumb.jpg)](https://swharden.com/static/2019/08/03/curved2.jpg)

</div>

**The micro USB port provides power and PC connectivity,** and when running the device sends frequency to the computer every second. All the parameters can be customized in software, and source code is on the [USB-Counter GitHub page](https://github.com/swharden/USB-Counter). 

<div class="text-center">

[![](https://swharden.com/static/2019/08/03/DSC_0132_thumb.jpg)](https://swharden.com/static/2019/08/03/DSC_0132.jpg)

</div>

**I also added support for a 7-segment LED display.** The counter works fine without the screen attached, but using the screen lets this device serve as a frequency counter without requiring a computer. This display is a MAX7219-driven display module which currently runs for [$2 each on Amazon](https://www.amazon.com/s?k=max7219+segment) when ordered in packs of 5.

### Precision Frequency Measurement

**One advantage of this counter is that it is never reset.** Since this circuit uses 32-bit counter IC, and every gate cycle transmits the current count to the computer over USB. Because every input cycle is measured high precision measurements of frequency over long periods of time are possible. For example, 1000 repeated measurements with a 1Hz gate allows frequency measurement to a precision of 0.01 Hz.

<div class="text-center img-border img-medium">

[![](https://swharden.com/static/2019/08/03/2019-08-04-output_thumb.jpg)](https://swharden.com/static/2019/08/03/2019-08-04-output.png)

</div>

### Internal or External Gating

**An optional external 1PPS gate can be used for precise timing.** The microcontroller is capable of generating gate cycles in software. Precision is limited to that of the TCXO used to clock the microcontroller (2.5 PPM). For higher-precision gating a resistor may be lifted and an external gate applied (e.g., 1PPS GPS signal).

### TCXO Driving a Gate in Software

**By clocking the microcontroller at 14.7456 MHz with a temperature-compensated crystal oscillator (TCXO)** I'm able to communicate with the PC easily at [115200 baud](http://ruemohr.org/~ircjunk/avr/baudcalc/avrbaudcalc-1.0.8.php), and with some [clever timer settings](https://eleccelerator.com/avr-timer-calculator/) and interrupts I'm able to toggle an output pin every 14,745,600 cycles to produce a fairly accurate 1PPS signal.

### Maximum Counting Frequency

**According to the SN74LV8154 datasheet** the minimum expected maximum input frequency (f<sub>MAX</sub>) is 40 MHz. To count higher frequencies, a high-speed prescaler could be added to the input to divide-down the input signal to a frequency this counter can range. This was [discussed](https://swharden.com/static/2019/08/03/) in the original issue that kicked-off this project, and [Onno Hoekstra (PA2OHH)](https://www.qsl.net/pa2ohh/) recommended the [SAB6456](https://doc.lagout.org/electronics/doc/ic_various/SAB6456.PDF) divide-by-64/divide-by-256 prescaler which supports up to 1 GHz input frequency. However, present availability seems to be limited. A similar chip, or even a pair of octal flip-flops that work in the GHZ range could achieve this functionality.

## Design

**By populating one of two input paths** with components this device can serve as a sensitive frequency counter (with a small-signal amplifier front-end) or a pulse counter (with a simple 50 ohm load at the front-end).

<div class="text-center">

[![](https://swharden.com/static/2019/08/03/schematic_thumb.jpg)](https://swharden.com/static/2019/08/03/schematic.png)

</div>

### Optional RF Amplifier Front-End

**An optional amplifier front-end** has been added to turn weak input into strong square waves suitable for driving the TTL counter IC. It is designed for continuously running input, and will likely self-oscillate if it is not actively driven.

<div class="text-center img-border">

![](https://swharden.com/static/2019/08/03/front-end.jpg)

</div>

> ⚠️ **WARNING: There is an error in this schematic.** The protection diodes should be the other way around.

**This simulation** shows a small 1 MHz signal fed into a high impedance front-end being amplified to easily satisfy TTL levels. The 1k resistor (R3) could be swapped-out for a 50 Ohm resistor for a more traditional input impedance if desired. LTSpice source files are in the GitHub repository in case you want to refine the simulation.

<div class="text-center img-border">

![](https://swharden.com/static/2019/08/03/front-end-wave.jpg)

</div>

### Components
* all passives are 0805 (~$1)
* [SBAV99WT1G SC-70 dual diode](https://www.mouser.com/ProductDetail/ON-Semiconductor/SBAV99WT1G?qs=%2Fha2pyFaduhs9dhfVWP8oT%252BsAj5t0ZSYddkb6PuTtd0%3D) 215 mA ($0.29)
* [14.7456MHz TCXO](https://www.mouser.com/ProductDetail/Fox/FOX924B-147456?qs=sGAEpiMZZMt8oz%2FHeiymADfzZKRiEXclvcmWd5jLzoM%3D) 2.5 PPM, 14.7456MHz ($2.36)
* [SN74LV8154](https://www.mouser.com/ProductDetail/Texas-Instruments/SN74LV8154PWR?qs=sGAEpiMZZMtdY2G%252BSI3N4aQvQNXOTGN6Ghdjz%252BkScFE%3D) ($0.99) TSSOP-20
* [FT230XS-R](https://www.mouser.com/ProductDetail/FTDI/FT230XS-R?qs=sGAEpiMZZMtv%252Bwxsgy%2FhiIaF6qCroMVR1i2pEQA5UpU%3D) ($2.04) SSOP-16
* [ATMega328](https://www.mouser.com/ProductDetail/Microchip-Technology-Atmel/ATMEGA328PB-AU?qs=sGAEpiMZZMvc81WFyF5EdrSRAEYMYvHlMc95YQj%2FArE%3D) ($1.38)
* [mini-USB jack](https://www.mouser.com/ProductDetail/CUI/UJ2-MBH-1-SMT-TR?qs=sGAEpiMZZMu3xu3GWjvQiLfiCTO8RP%252Bk%252BIiwpoT5qew%3D) ($0.49)
* [micro-USB jack](https://www.mouser.com/ProductDetail/Hirose-Connector/ZX62D-B-5PA830?qs=sGAEpiMZZMulM8LPOQ%252Byk6r3VmhUEyMLT8hu1C1GYL85FtczwhvFwQ%3D%3D) ($0.70)
* [SMA connector](https://www.mouser.com/ProductDetail/LPRS/SMA-CONNECTOR?qs=sGAEpiMZZMuLQf%252BEuFsOrkd7M7rmHNHidLMZ%2Ftb%252B0T1YCJLScw0qLA%3D%3D) ($1.08)
* [SPI-driven 8-digit 7-segment display module](https://www.amazon.com/dp/B07CL2YNJQ) ($13 for 4)


### PCB

<div class="text-center img-border">

[![](https://swharden.com/static/2019/08/03/pcb-dsn_thumb.jpg)](https://swharden.com/static/2019/08/03/pcb-dsn.png)

</div>

<div class="text-center">

[![](https://swharden.com/static/2019/08/03/pcb-rndr_thumb.jpg)](https://swharden.com/static/2019/08/03/pcb-rndr.png)

</div>

<div class="text-center img-border">

[![](https://swharden.com/static/2019/08/03/DSC_0128_thumb.jpg)](https://swharden.com/static/2019/08/03/DSC_0128.jpg)

</div>

### Changes from rev 1.0
* improved RF amplifier design
* alternate path to bypass RF amplifier
* corrected counter pin connections
* free a MCU pin by making the status LED the gate
* add a header for the serial LED display
* run MCU at 14.7456 MHz
  * allows much faster serial transmission
  * no longer accepts external 10MHz reference
  * may still accept external gate
* added screw holes
  * they're floating (not grounded) - should they be grounded?
* switched to micro USB (from mini USB)

### Build Notes
* didnt have 27 ohm resistors. used 22 ohm.
* I used a 500mW rated R15
* I used a 500mW rated R13
* make hand solder version of usb
* make oscillator fit less awkwardly
* Add a 7805 so 12V can be applied or USB. Use a 78L33 (not the reg on the FTDI chip) to power everything else.
* This device doesn't work when plugged into a wall USB cord (power only, no data). It seems an active USB connection is required to cause the 3.3V regulator (built into the FTDI chip) to deliver power. The next revision should use a discrete 3.3V regulator.
* For a standalone (LED) device no USB connection is needed. Make a version that accepts 12V and displays the result on the LED. Make the optional external gate easy to access. Break-out the TX pin so PC logging is still very easy.

## Resources
* [USB-Counter](https://github.com/swharden/USB-Counter) on GitHub
* [Revision 1.0 build notes](https://github.com/swharden/USB-Counter/tree/master/builds/1.0)
* [Revision 1.1 build notes](https://github.com/swharden/USB-Counter/tree/master/builds/1.1)
* [GitHub issue](https://github.com/swharden/AVR-projects/issues/1) where this topic was first discussed