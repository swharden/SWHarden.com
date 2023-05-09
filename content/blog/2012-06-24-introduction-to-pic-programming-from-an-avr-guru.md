---
title: Introduction to PIC Programming for AVR users
date: 2012-06-24 20:29:03
tags: ["microcontroller", "obsolete"]
---



__I'm not ashamed to say it: I'm a bit of an ATMEL guy.__ [AVR microcontrollers](http://en.wikipedia.org/wiki/Atmel_AVR) are virtually exclusively what I utilize when creating hobby-level projects. Wile I'd like to claim to be an expert in the field since I live and breathe ATMEL datasheets and have used many intricate features of these microchips, the reality is that I have little experience with other platforms, and have likely been leaning on AVR out of habit and personal convention rather than a tangible reason.

<div class="text-center">

![](https://swharden.com/static/2012/06/24/150-28-DIP1-200x128.jpg)

</div>

**Although I was initially drawn to the AVR line of microcontrollers** because of its open-source nature (The primary compiler is the free AVR-GCC) and longstanding ability to be programmed from non-Windows operating systems (like Linux), [Microchip's PIC](http://en.wikipedia.org/wiki/PIC_microcontroller) has caught my eye over the years because it's often a few cents cheaper, has considerably large professional documentation, and offers advanced integrated peripherals (such as native USB functionality in a DIP package) more so than the current line of ATTiny and ATMega microcontrollers. From a hobby standpoint, I know that ATMEL is popular (think [Arduino](http://en.wikipedia.org/wiki/Arduino)), but from a professional standpoint I usually hear about commercial products utilizing PIC microcontrollers. One potential drawback to PIC (and the primary reason I stayed away from it) is that full-featured C compilers are often not free, and as a student in the medical field learning electrical engineering as a hobby, I'm simply not willing to pay for software at this stage in my life.

__I decided to take the plunge and start gaining some experience with the PIC platform.__ I ordered some PIC chips (a couple bucks a piece), a PIC programmer (a Chinese knock-off clone of the [Pic Kit 2](http://en.wikipedia.org/wiki/PICKit) which is <$20 shipped on eBay), and shelved it for over a year before I got around to figuring it out today. My ultimate goal is to utilize its native USB functionality (something at ATMEL doesn't currently offer in DIP packages). I've previously used bit-banging libraries like [V-USB](http://www.obdev.at/products/vusb/index.html) to hack together a USB interface on AVR microcontrollers, but it felt unnecessarily complex. PIC is commonly used and a bit of an industry standard, so I'm doing myself a disservice by not exploring it. My goal is USB functionality, but I have to start somewhere: blinking a LED.

<div class="text-center">

![](https://swharden.com/static/2012/06/24/2012-06-24-15.57.56-525x393.jpg)

</div>

__Here's my blinking LED__. It's a bit anticlimactic, but it represents a successful program design from circuit to writing the code to programming the microchip.
>  _Based on my limited experience, it seems you need 4 things to program a PIC microcontroller with C:_
>
> *   __[PIC microcontroller](http://en.wikipedia.org/wiki/PIC_microcontroller)__ compatible with your programmer and your software (I'm using [18F2450](http://ww1.microchip.com/downloads/en/DeviceDoc/39760d.pdf))
> *   __PIC programmer__ (I'm using a clone [PicKit 2](http://en.wikipedia.org/wiki/PICKit), [$19.99 shipped on eBay](http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=pic+kit+2&_sacat=0)) - get the PICkit2 installer [here](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en023805)
> *   Install __[MPLAB IDE](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en019469&part=SW007002)__ (programming environment for PIC) - has a free version
> *   Install a __C compiler__: I'm using [PIC18 C Compiler for MPLAB](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en010014) Lite - has a free version
>
>
__The first thing I did was familiarize myself with the pin diagram of my PIC from its datasheet__. I'm playing with an [18F2450](http://ww1.microchip.com/downloads/en/DeviceDoc/39760d.pdf) and the [datasheet is quite complete](http://ww1.microchip.com/downloads/en/DeviceDoc/39760d.pdf). If you look at the pin diagram, you can find pins labeled __MCLR__ (reset), __VDD__ (+5V), __VSS__ (GND), __PGC__ (clock), and __PGD__ (data). These pins should be connected to their respective counterparts on the programmer. To test connectivity, install and run the [PICkit2 installer software](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en023805) and it will let you read/verify the firmware on the chip, letting you know connectivity is solid. Once you're there, you're ready to start coding!

__I wish I were friends with someone who programmed PIC, such that in 5 minutes I could be shown what took a couple hours to figure out.__ There are quite a few tutorials out there - borderline too many, and they all seem to be a bit different. To quickly get acquainted with the PIC programming environment, I followed the ["Hello World" Program in C tutorial](http://www.pic18f.com/18f4550-c-tutorial/2009/11/16/tutorial-4-hello-world-program-in-c/) on [PIC18F.com](http://www.pic18f.com/). Unfortunately, it didn't work as posted, likely because their example code was based on a PIC 18F4550 and mine is an 18F2450, but I still don't understand why such a small difference caused such a big problem. The problem was in their use of LATDbits and TRISDbits (which I tried to replace with LATBbits and TRISBbits). I got around it by manually addressing TRISB and LATB. Anyway, this is what I came up with:

```c
#include <p18f2450.h> // load pin names
#include <delays.h>   // load delay library

#pragma config WDT = OFF // disable watchdog timer
#pragma config FOSC = INTOSCIO_EC // use internal clock

void main() // this is the main program
{
    TRISB=0B00000000; // set all pins on port B as output
    while(1) // execute the following code block forever
    {
        LATB = 0b11111111; // turn all port B pins ON
        Delay10KTCYx(1);   // pause 1 second
        LATB = 0b00000000; // turn all port B pins OFF
        Delay10KTCYx(1);   // pause 1 second
    }
}
```

__A couple notes about the code:__ the WDT=OFF disables the [watchdog timer](http://en.wikipedia.org/wiki/Watchdog_timer), which if left unchecked would continuously reboot the microcontroller. The FOSC=INTOSCIO_EC section tells the microcontroller to use its internal oscillator, allowing it to execute code without necessitating an external crystal or other clock source. As to what TRIS and LAT do, I'll refer you to [basic I/O operations with PIC](http://www.mikroe.com/eng/chapters/view/4/chapter-3-i-o-ports/).

<div class="text-center">

![](https://swharden.com/static/2012/06/24/pic-ledblink.png)

</div>

__Here is what the MPLAB IDE looked like after I successfully loaded the code onto the microcontroller.__ At this time, the LED began blinking about once per second. I guess that about wraps it up! This afternoon I pulled a PIC out of my junk box and, having never programmed a PIC before, successfully loaded the software, got my programmer up and running, and have a little functioning circuit. I know it isn't _that_ big of a deal, but it's a step in the right direction, and I'm glad I've taken it.