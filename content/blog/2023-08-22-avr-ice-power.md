---
title: Hack an Atmel ICE to Deliver Power
description: How I broke out VCC and programming lines so my Atmel ICE can power devices and program them without requiring the programming cable
Date: 2023-08-22 19:45:00
tags: ["circuit", "microcontroller"]
---

**The Atmel ICE is a development tool for programming and debugging Atmel microcontrollers, but it does not have the ability to power devices under test.** Older AVR series microcontrollers could be programmed with inexpensive ICSP programmers that carried a VCC line, but the newest series of AVR microcontrollers cannot be programmed with ICSP. See my [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming) article for information about options for programming these chips using inexpensive gear. Although the Atmel ICE has a VCC _sense_ line, it does not come with the ability to _deliver_ power. This page describes how I modified my Atmel ICE to break-out 5V and 3.3V lines, and also V<sub>SENSE</sub> and UPDI pins to make it easier to program microcontrollers without needed the ribbon cable.

<a href="https://swharden.com/static/2023/08/22/wires-labeled.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/wires-labeled.jpg">
</a>

## Locating the Power Rails

**I found that the Atmel ICE was very easy to open** by inserting a large flat-head screwdriver into the grooves on the side and twisting (without applying any inward force).

<a href="https://swharden.com/static/2023/08/22/case.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/case.jpg">
</a>

<a href="https://swharden.com/static/2023/08/22/open-case.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/open-case.jpg">
</a>

**After probing around I found convenient locations for soldering wires to break-out key lines.** Ground can be difficult to solder because of how thermally connected it is to the ground planes in the multi-layer board, but soldering to the through-hole thermal vias made this easier. A 3.3V line was easy to locate, but I would hesitate* to use this for significant power draw. I'm not sure how this board is regulated or how close it runs to its current limit when it's performing power-intensive operations. Also I'm not sure how easy it is to damage the programmer if the 3.3V line is exposed to higher voltage or shorted directly to ground. On the other hand, the 5V USB power rail was easy to locate and I'm much less concerned about loading that down.

_*Follow-up: I ended up removing the 3.3V wire after these photographs because it doesn't offer that much benefit, and the risk of accidentally touching a 5V rail or ground and potentially damaging the programmer's internal voltage regulator or power protection circuitry was higher than I was comfortable with.*_

<a href="https://swharden.com/static/2023/08/22/avr-ice-pcb.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/avr-ice-pcb.jpg">
</a>

## Avoiding the Stupid Ribbon Cable

**Did I mention how frustrating the Atmel ICE's ribbon cable is?** The device itself has a reversed connector, so it can only work with a reversing cable! The headers on the Atmel ICE use teeny 1.27 mm pin spacing which prevents manually inserting wires with 2.54 mm female headers. The pins are unnecessarily small considering the other end of the reversing cable has standard 2.54 mm pin spacing! I'm [not](https://www.bigmessowires.com/2018/06/13/atmel-ice-wiring-horror/) the only [person](https://www.avrfreaks.net/s/topic/a5C3l000000UbCNEA0/t156783) who [noticed](https://www.eevblog.com/forum/projects/atmel-ice-cable-stupidity/) how frustrating this cable is. If you lose or break your reversing cable, new ones are available from the major electronics distributors but they seem exorbitantly expensive for what they are.

<a href="https://swharden.com/static/2023/08/22/gears.jpg">
<img src="https://swharden.com/static/2023/08/22/gears.jpg">
</a>

**After breaking out V<sub>SENSE</sub> and UPDI lines** I tossed the ribbon cable into my junk box where it belongs.

<a href="https://swharden.com/static/2023/08/22/cable.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/cable.jpg">
</a>

## Reassembling the Programmer

**I used a nibbler to cut rectangular notches in the white plastic beneath the blue plastic ring and ran the breakout wires through the hole.** When reassembled, these gaps left just enough space for the wires to easily pass through. I didn't attempt to secure the wires to the case, but users concerned about damage from pulling may achieve enhanced protection by using a small zip tie around the wires inside the case next to the hole. Hot glue or epoxy could further secure the wires at the expensive of making the device more difficult to service in the future.

<a href="https://swharden.com/static/2023/08/22/partial-reassemble.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/partial-reassemble.jpg">
</a>

## Conclusion

**My Atmel ICE can now power a device and program it without requiring the ribbon cable or an external power supply.** After using this for a few days, I'm very satisfied with the result! This modification doesn't disable any of the original functionality, so users always have the option to plug in the ribbon cable if they want to program a device that way.

<a href="https://swharden.com/static/2023/08/22/programming.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/22/programming.jpg">
</a>

## Additional Resources

* [Atmel ICE User Guide](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-ICE_UserGuide.pdf)

* [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming)

* [Atmel ICE Wiring Horror](https://www.bigmessowires.com/2018/06/13/atmel-ice-wiring-horror/) 

* [ATtiny816 programming via ATMEL-ICE fails](https://www.avrfreaks.net/s/topic/a5C3l000000UbCNEA0/t156783) 

* [Atmel ICE cable stupidity](https://www.eevblog.com/forum/projects/atmel-ice-cable-stupidity/) 