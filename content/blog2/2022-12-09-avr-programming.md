---
title: Programming Modern AVR Microcontrollers
description: Blink a LED on a modern series AVR using Atmel-ICS or MPLAB Snap UPDI programmers.
Date: 2022-12-09 23:45:00
tags: ["circuit", "microcontroller"]
---

**This page describes how to program Microchip's newest series of AVR microcontrollers using official programming gear and software.** I spent many years programming the traditional series of Atmel chips, but now several years after Microchip acquired Atmel I am interested in exploring the capabilities of the latest series of AVR microcontrollers (especially the new AVR DD family). Currently the global chip shortage makes it difficult to source traditional ATMega and STM32 chips, but the newest series of AVR microcontrollers feature an impressive set of peripherals for the price and are available from all the major vendors.
pressive set of peripherals for the price and are available from all the major vendors.

{{<youtube M-myqg-2c5s>}}

## TLDR

* Older AVR microcontrollers are programmed using _in-circuit serial programming_ (ICSP) through the `RESET`, `SCK`, `MISO`, and `MOSI` pins using cheap programmers like [USBtiny](https://learn.adafruit.com/usbtinyisp). However, serial programming is not supported on newer AVR microcontrollers.

* New AVR microcontrollers are programmed using the _unified program and debug interface_ (UDPI) exclusively through the `UDPI` pin. UDPI is a Microchip proprietary interface requiring a UDPI-capable programmer.

* Official UDPI programmers include [Atmel-ICE](https://www.digikey.com/en/products/detail/microchip-technology/ATATMEL-ICE-BASIC/4753381) ($129) and [MPLAB Snap](https://www.digikey.com/en/products/detail/microchip-technology/PG164100/9562532) ($35). The Atmel-ICE is expensive but it is very well supported. The MPLAB Snap is hacky, requires re-flashing, and has a physical design flaw requiring a hardware modification before it can program AVR series chips.

* There are notable attempts to create alternative programmers (e.g., [jtag2updi](https://github.com/ElTangas/jtag2updi) and [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog)), but this journey into the land of unofficial programmer designs is fraught with abandoned GitHub repositories and a lot of added complexity and brittleness (e.g., [SpenceKonde/AVR-Guidance](https://github.com/SpenceKonde/AVR-Guidance/blob/master/UPDI/jtag2updi.md)), so to save yourself frustration in the future I highly recommend just buying an officially supported programmer. It's also nice when you can program and debug your microcontroller from within your IDE.

* UDPI programmers have a `Vcc` pin that is used to _sense_ supply voltage (but not provide it), so you must power your board yourself while using one of these new programmers.

## ATTiny826 LED Blink

**Blinking a LED is the "Hello, World" of microcontroller programming.** Let's take a look at the code necessary to blink a LED on pin 2 of an [ATTiny286](https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny424-426-427-824-826-827-DataSheet-DS40002311A.pdf). It is compiled and programmed onto the chip using [Microchip Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio).

```c
#define F_CPU 3333333UL
#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
	PORTA.DIR = 0xFF;
	while (1)
	{
		PORTA.OUT = 255;
		_delay_ms(500);
		PORTA.OUT = 0;
		_delay_ms(500);
	}
}
```

* `PORTA.DIR` sets the direction of pins on port A (`0xFF` means all outputs)
* `PORTA.OUT` sets output voltage on pins of port A (`0xFF` means all high)
* Using `_delay_ms()` requires including `delay.h`
* Including `delay.h` requires defining `F_CPU` (the CPU frequency)
* The [ATTiny286 datasheet section 11.3.3](https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny424-426-427-824-826-827-DataSheet-DS40002311A.pdf) indicates the default clock is 20 MHz with a /6 prescaler, so the default clock is `3333333 Hz` (3.3 MHz). This behavior can be customized using the Oscillator Configuration Fuse (FUSE.OSCCFG).

## ATTiny826 Pinout

From page 14 of the [ATTiny826 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny424-426-427-824-826-827-DataSheet-DS40002311A.pdf)

<img src="https://swharden.com/static/2022/12/09/attiny826-pinout.png" class="mx-auto d-block w-75" />

## SMT ATTiny Breakout Board

**Many of the newer AVR series microcontrollers are not available in breadboard-friendly DIP packages.** I find SOIC-to-DIP breakout boards (available on Amazon and eBay) to be useful for experimenting with chips in SOIC packages. Here I added extra power and PA4 (pin 2) LEDs and 10 kΩ current limiting resistors.

<a href="https://swharden.com/static/2022/12/09/leds2.jpg">
<img src="https://swharden.com/static/2022/12/09/leds2.jpg"/>
</a>

<a href="https://swharden.com/static/2022/12/09/scope1.jpg">
<img src="https://swharden.com/static/2022/12/09/scope1.jpg"/>
</a>

**I power the device from the 3.3V or 5V pins on a FT232 USB breakout board.** Although the topic is out of scope for this article, I find it convenient to use FTDI chips to exchange small amounts of data or debug messages between a microcontroller and a modern PC over USB without requiring special drivers.

<img src="https://swharden.com/static/2022/12/09/ft232-breadboard.jpg" class="mx-auto d-block w-50" />

## Why is programming modern AVRs so difficult?

**I'm surprised how little information there is online about how to _reliably_ program modern AVR series microcontrollers.** In late 2022 there is a surprisingly large amount of "advice" on this topic which leads to dead ends and broken or abandoned projects. After looking into it for a while, here is my opinionated assessment. Mouser and Digikey have links to expensive programmers, and Amazon has links to similar items but reviews are littered with comments like "arrived bricked" and "can not program AVR series chips". DIY options typically involve abandoned (or soon-to-be abandoned?) GitHub repositories, or instructions for Arduino-related programming. I seek to consolidate and distill the most useful information onto this page, and I hope others will find it useful.

## Atmel-ICE: Expensive but Effective

**After using $5 ICSP programmers for the last decade I almost fell out of my chair when I saw Microchip's recommended entry-level programmer is over $180!** Digikey sells a "basic" version without cables for $130, but that still seems crazy to me. Also, $50 for a ribbon cable?

<a href="https://swharden.com/static/2022/12/09/avr-ice.webp">
<img src="https://swharden.com/static/2022/12/09/avr-ice.webp" class="w-50 d-block mx-auto" />
</a>

**I found a kit on Amazon that sells the programmer with a cable for $126.** It was hard for me to press that buy button, but I figured the time I would save by having access to modern and exotic chips during the present global chip shortage would make it worth it. After a couple days of free Prime shipping, it arrived. It was smaller than I thought it would be from the product photos.

<a href="https://swharden.com/static/2022/12/09/atmel-ice-1.jpg">
<img src="https://swharden.com/static/2022/12/09/atmel-ice-1.jpg" />
</a>

**The cable that came with the device seemed a bit hacky at first, but I'm happy to have it.** The female 2.54 mm socket is easy to insert breadboard jumpers into.

<a href="https://swharden.com/static/2022/12/09/atmel-ice-2.jpg">
<img src="https://swharden.com/static/2022/12/09/atmel-ice-2.jpg"/>
</a>

**I'm glad this thing is idiot proof.** The very first thing I did after unboxing this programmer was hook it up to my power supply rails using reverse polarity. I misread the pin diagram and confused the _socket_ with the _connector_ (they are mirror images of one another). This is an easy mistake to make though, so here's a picture of the correct orientation. Note the location of the tab on the side of the connector.

Atmel ICE Pinout | Programming Connection
---|---
<a href="https://swharden.com/static/2022/12/09/atmel-ice-pinout.png"><img src="https://swharden.com/static/2022/12/09/atmel-ice-pinout.png" class="img-fluid"></a>|<a href="https://swharden.com/static/2022/12/09/atmel-ice-3.jpg"><img src="https://swharden.com/static/2022/12/09/atmel-ice-3.jpg" class="img-fluid"></a>

* Black: `GND`
* Red: `Vcc` - This line is used to _sense_ power and not _deliver_ it, so you are responsible for externally powering your board.
* Blue: `UPDI` pin - Although a pull-up resistor on the UPDI pin is recommended, I did not find it was required to program my chip on the breadboard in this configuration.

**The AVR Ice was easy to use with Microchip Studio.** My programmer was detected immediately, a window popped-up and walked me through updating the firmware, and my LED was blinking in no time.

<a href="https://swharden.com/static/2022/12/09/atmel-ice-4.jpg">
<img src="https://swharden.com/static/2022/12/09/atmel-ice-4.jpg"/>
</a>

## MPLAB Snap: Cheap and Convoluted

**Did I really need to spend $126 for an AVR programmer? Amazon carries the MPLAB Snap for $34, but lots of reviews say it doesn't work.** After easily getting the Atmel-ICE programmer up and running I thought it would be a similarly easy experience setting-up the MPLAB Snap for AVR UPDI programming, but boy was I wrong. Now that I know the steps to get this thing working it's not so bad, but the information here was only gathered after hours of frustration. 

<a href="https://swharden.com/static/2022/12/09/mplab-snap.webp">
<img src="https://swharden.com/static/2022/12/09/mplab-snap.webp" class="d-block mx-auto w-75" />
</a>

<a href="https://swharden.com/static/2022/12/09/mplab-snap-1.jpg">
<img src="https://swharden.com/static/2022/12/09/mplab-snap-1.jpg" />
</a>

Here are the steps you can take to program modern AVR microcontrollers with UPDI using a MPLAB Snap:

### Step 1: Setup MPLAB

* The MPLAB Snap ships with obsolete firmware and must be re-flashed immediately upon receipt.

* Microchip Studio's firmware upgrade tool does not actually work with the MPLAB Snap. It shows the board with version 0.00 software and it hangs (with several USB disconnect/reconnect sounds) if you try to upgrade it.

* You can only re-flash the MPLAB Snap using the MPLAB X IDE. Download the 1.10 GB [MPLAB setup](https://www.microchip.com/en-us/tools-resources/develop/mplab-x-ide) executable and install the MPLAB IDE software which occupies a cool 9.83 GB.

### Step 2: Re-Flash the Programmer

* In the MPLAB IDE select `Tools` and select `Hardware Tool Emergency Boot Firmware Recovery`. At least this tool is helpful. It walks you through how to reset the device and program the latest firmware.

### Step 3: Acknowledge Your Programmer is Defective

Defective may be a strong word, but let's just say the hardware was not designed to enable programming AVR chips using UPDI. Microchip Studio will detect the programmer but if you try to program an AVR you'll get a pop-up error message that provides surprisingly little useful information.

<img src="https://swharden.com/static/2022/12/09/verify.png" class="mx-auto d-block img-fluid" />

> Atmel Studio was unable to start your debug session. Please verify device selection, interface settings, target power and connections to the target device. Look in the details section for more information.
> StatusCode:	131107
> ModuleName:	TCF (TCF command: Processes:launch failed.)
> An illegal configuration parameter was used. Debugger command Activate physical failed.

### Step 4: Fix Your Programmer

**The reason MPLAB Snap cannot program AVR microcontrollers is because the UPDI pin should be pulled _high_, but the MPLAB Snap comes from the factory with its UPDI pin pulled _low_ with a 4.7 kΩ resistor to ground.** You can try to overpower this resistor by adding a low value pull-up resistor to Vcc (1 kΩ worked for me on a breadboard), but the actual fix is to fire-up the soldering iron and remove that tiny surface-mount pull-down resistor labeled `R48`.

Have your glasses? R48 is here:

<a href="https://swharden.com/static/2022/12/09/mplab-snap-fix.jpg">
<img src="https://swharden.com/static/2022/12/09/mplab-snap-fix.jpg" />
</a>


**These photos were taken after I removed the resistor.** I didn't use hot air. I just touched it a for a few seconds with a soldering iron and wiped it off then threw it away.

<a href="https://swharden.com/static/2022/12/09/scope2.jpg">
<img src="https://swharden.com/static/2022/12/09/scope2.jpg" />
</a>

You don't need a microscope, but I'm glad I had one.

### Step 5: Reflect

You can now program AVR microcontrollers using UPDI with your MPLAB Snap! Blink, LED, blink.

<a href="https://swharden.com/static/2022/12/09/mplab-snap-2.jpg">
<img src="https://swharden.com/static/2022/12/09/mplab-snap-2.jpg" />
</a>

**Can you believe this is the officially recommended action?** According to the official Microchip Engineering Technical Note [ETN #36](http://ww1.microchip.com/downloads/en/DeviceDoc/ETN36_MPLAB%20Snap%20AVR%20Interface%20Modification.pdf): MPLAB Snap AVR Interface Modification

* **Symptom:** Programming and debugging fails with AVR microcontroller devices that use the UPDI/PDI/TPI interfaces. MPLAB SNAP, Assembly #02-10381-R1 requires an external pull-up resistor for AVR microcontroller
devices that use these interfaces.

* **Problem:** AVR microcontroller devices that use the UPDI/PDI/TPI interfaces require the idle state of inactivity to be at a logic high level. Internally, the AVR devices have a weak (50-100K) pull-up resistor that attempts to keep the line high. An external and stronger pull-up resistor may be enough to mitigate this issue and bring voltages to acceptable VDD levels. In some cases, this may not be enough and the pull-down resistor that is part of the ICSP protocol can be removed for these AVR microcontroller applications.

* **Solution:** If most of the applications are AVR-centric, consider removing the R48 resistor as shown below. This completely isolates any loading on the programming data line. Additionally, a pull-up resistor to VDD in the range of 1K to 10K should be used for robustness. Pin 4 of J4 is the TPGD data line used for ICSP interfaces and it also doubles as the DAT signal for UPDI/PDI and TPI interfaces. The pull-up resistor can be mounted directly from TVDD (J4-2) to TPGD/DAT (J4-4). Alternatively, the resistor can be mounted on the application side of the circuit
for convenience.

**I feel genuinely sorry for the Amazon sellers who are getting poor reviews because they sell this product.** It really isn't their fault. I hope Google directs people here so that they can get their boards working and leave positive reviews that point more people to this issue.

## UPDI Programming with a Serial Adapter

There is no official support for UPDI programming using a serial adapter, but it seems some people have figured out how to do it in some capacity. There was a promising [pyupdi](https://github.com/mraardvark/pyupdi) project, but it is now deprecated. At the time of writing the leading project aiming to enable UPDI programming without official hardware is [pymcuprog](https://github.com/microchip-pic-avr-tools/pymcuprog), but its repository has a single commit dated two months ago and no activity since. Interestingly, [that commit](https://github.com/microchip-pic-avr-tools/pymcuprog/commit/593afdc8e089e39a4fed9f4fb19ae81f5f51e9a5.patch) was made by buildmaster@microchip.com (an unverified email address), so it may not be fair to refer to it as an "unofficial" solution. The long term support of the pymcuprog project remains uncertain, but regardless let's take a closer look at how it works.

![](https://swharden.com/static/2022/12/09/updi-ftdi-serial-programmer.png)

To build a programmer you just need a TTL USB serial adapter and a 1kΩ resistor. These are the steps I used to program a LED blink program using this strategy:

* Use a generic [FT232 breakout board](https://www.amazon.com/s?k=ft232+breakout) to achieve a USB-controlled serial port on my breadboard.

* Connect the programmer as shown with the RX pin directly to the UPDI pin of the microcontroller and the resistor between the RX and TX pins.

* Ensure a [modern version of Python](https://www.python.org/) is installed on your system

* `pip install pymcuprog`

* Use the device manager to identify the name of the COM port representing your programmer. In my case it's `COM12`.

* I then interacted with the microcontroller by running `pymcuprog` from a terminal

### Ping the Microcontroller

This command returns the device ID (1E9328 for my ATtiny826) indicating the UPDI connection is working successfully

```bash
pymcuprog ping -d attiny826 -t uart -u com12
```

```
Connecting to SerialUPDI
Pinging device...
Ping response: 1E9328
```

### Write a Hex File

I used Microchip Studio to compile my C code and generate the hex file. Now I can use `pymcuprog` to load those hex files onto the chip. It's slower to program and inconvenient to drop to a terminal whenever I want to program a chip, but it works.

```
pymcuprog write -f LedBlink.hex -d attiny826 -t uart -u com12
```

```
Connecting to SerialUPDI
Pinging device...
Ping response: 1E9328
Writing from hex file...
Writing flash...
```

## Conclusions

* The new AVR series microcontrollers have lots of cool peripherals for the price and are available during a chip shortage that threatens availability of the more common traditional microcontrollers.

* The Atmel-ICE is expensive, but the most convenient and reliable way to program modern AVR microcontrollers using UPDI.

* The MPLAB Snap can program modern AVRs using UPDI after a software flash and a hardware modification, but its support for AVRs seems like an afterthought rather than its design priority.

* You can create a makeshift unofficial UPDI programmer from a USB serial adapter, but the added complexity, lack of debugging capabilities, increased friction during the development loop, and large number of abandoned projects in this space make this an unappealing long term solution in my opinion.

## Resources

* Atmel-ICE
  * [Atmel-ICE on Mouser](https://www.mouser.com/ProductDetail/Microchip-Technology-Atmel/ATATMEL-ICE?qs=sGAEpiMZZMuRZxwUfDU0miN4udwF8GpUanrVt%252BDSn9Q4SZQ5wSGB4Q%3D%3D) (currently $180.64)
  * [Atmel-ICE on DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/ATATMEL-ICE/4753379) (currently $180.62)
  * [Atmel-ICE on Amazon](https://www.amazon.com/s?k=atmel+ice) (currently $126.49)
  * [Atmel-ICE on eBay](https://www.ebay.com/sch/i.html?_nkw=atmel-ice) (currently $135.00)
  * [Atmel-ICE datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-ICE_UserGuide.pdf)
* MPLAB Snap
  * [MPLAB Snap on Mouser](https://www.mouser.com/ProductDetail/Microchip-Technology-Atmel/PG164100?qs=w%2Fv1CP2dgqoaLDDBjfzhMQ%3D%3D) (currently $34.77)
  * [MPLAB Snap on DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/PG164100/9562532) (currently $34.76)
  * [MPLAB Snap on Amazon](https://www.amazon.com/s?k=mplab+snap) (currently $34.09)
  * [MPLAB Snap datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/50002787C.pdf)
  * [MPLAB Snap AVR UPDI modification](http://ww1.microchip.com/downloads/en/DeviceDoc/ETN36_MPLAB%20Snap%20AVR%20Interface%20Modification.pdf)
* [ATTiny826 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny424-426-427-824-826-827-DataSheet-DS40002311A.pdf)
* [UPDI Physical Interface](https://onlinedocs.microchip.com/pr/GUID-DDB0017E-84E3-4E77-AAE9-7AC4290E5E8B-en-US-4/index.html)
* [Contact me](https://swharden.com/about/) if you have suggestions or updated information