---
title: AVR Programming in 64-bit Windows 7
date: 2013-05-07 18:14:58
tags: ["microcontroller", "obsolete"]
---



__A majority of the microcontroller programming I do these days involves writing C for the ATMEL AVR series of microcontrollers.__ I respect PIC, but I find the open/free atmosphere around AVR to be a little more supportive to individual, non-commercial cross-platform programmers like myself. With that being said, I've had a few bumps along the way getting unofficial AVR programmers to work in Windows 7. Previously, I had great success with a $11 (shipped) [clone AVRISP-mkII programmer](http://fun4diy.com/AVRISP_mkII.htm)  from fun4diy.com. It was the heart of a little AVR development board I made and grew to love (which had a drop-in chip slot and also a little breadboard all in one) seen in a [few](https://swharden.com/blog/2010-12-28-full-auto-rapidfire-mouse-modification/) random blog [posts](https://swharden.com/blog/2010-05-24-solar-powered-qrss-beacon/) over the years. Recently it began giving me trouble because, despite downloading and installing various drivers and packages, I couldn't get it to work with Windows Vista or windows 7. I needed to find another option. I decided against the official programmer/software because the programmer is expensive (for a college student) and the software (AVR studio 6) is terribly bloated for LED-blink type applications. "AStudio61.exe" is 582.17 Mb. Are you kidding me? Half a gig to program a microchip with 2kb of memory? Rediculous.  I don't use [arduino](http://en.wikipedia.org/wiki/Arduino) because I'm comfortable working in C and happy reading datasheets. Furthermore, I like programming chips hot off the press, without requiring a special boot loader.

<div class="text-center img-border">

![](https://swharden.com/static/2013/05/07/2013-05-05-22.57.01.jpg)

</div>

I got everything running on Windows 7 x64 with the following:

* **Programmer:** USBTinyISP (eBay, $8.50 free shipping)___It's a branch of an unofficial AvrISP-mkII project. [Ladyada.net provides](http://www.ladyada.net/make/usbtinyisp/) code, [schematics](http://www.ladyada.net/make/usbtinyisp/make.html), and even an option to buy a [built-it-yourself kit](http://www.adafruit.com/category/16) for $~22 (+shipping) through adafruit. However I found them [pre-assembled with SMT components for $8.48 shipped on eBay](http://www.ebay.com/sch/usbtiny). _

* **Drivers:** Find them on the[ Ladyada page](http://www.ladyada.net/make/usbtinyisp/download.html). (Free)___There are links at the top for 32-bit and 64-bit windows._

* **Compiler Software:** [WinAvr](http://winavr.sourceforge.net/index.html) (Free)___This is windows software. Linux users want a different flavor of AVR-GCC and should see my previous post on [programming AVR in Ubuntu Linux](https://swharden.com/blog/2013-01-06-avr-programming-in-linux/)_

* **Programming Software:** [AVRDudess](http://blog.zakkemble.co.uk/avrdudess-a-gui-for-avrdude/) (Free)___This is actually a GUI for [AVRDude](http://www.ladyada.net/make/usbtinyisp/avrdude.html), a command line driven programmer. It has a [great tutorial](http://www.ladyada.net/learn/avr/avrdude.html) though. I accidentally keep thinking (and searching) for this program by the incorrect title AVRDudette._


__Here's the "hello world" of microchip programs (it simply blinks an LED).__ I'll assume the audience of this page knows the basics of microcontroller programming, so I won't go into the details. Just note that I'm using an ATMega48 and the LED is on pin 9 (PB6). This file is named "blink.c".

```c
#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>

int main (void)
{
    DDRB = 255;
    while(1)
    {
        PORTB ^= 255;
        _delay_ms(500);
    }
}
```

__Here's how I compiled the code:__

```bash
avr-gcc -mmcu=atmega48 -Wall -Os -o blink.elf blink.c
avr-objcopy -j .text -j .data -O ihex blink.elf blink.hex
```

_In reality, it is useful to put these commands in a text file and call them "compile.bat"_
__Here's how I program the AVR.__ I used [AVRDudess](http://blog.zakkemble.co.uk/avrdudess-a-gui-for-avrdude/)! I've been using raw AVRDude for years. It's a little rough around the edges, but this GUI interface is pretty convenient. I don't even feel the need to include the command to program it from the command line! If I encourage nothing else by this post, I encourage (a) people to use and support AVRDudess, and (b) AVRDudess to continue developing itself as a product nearly all hobby AVR programmers will use. Thank you 21-year-old Zak Kemble.

<div class="text-center img-border">

![](https://swharden.com/static/2013/05/07/2013-05-05-22.56.20.jpg)

</div>

__And finally, the result.__ A blinking LED. Up and running programming AVR microcontrollers in 64-bit Windows 7 with an unofficial programmer, and never needing to install bloated AVR Studio software.

<div class="text-center img-border">

![](https://swharden.com/static/2013/05/07/2013-05-05-23.05.53.jpg)

</div>