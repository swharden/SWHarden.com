---
title: AVR Programming in Linux
date: 2013-01-06 14:51:19
tags: ["microcontroller", "obsolete"]
---



__It is not difficult to program ATMEL AVR microcontrollers with linux, and I almost exclusively do this because various unofficial (inexpensive) USB AVR programmers are incompatible with modern versions of windows (namely Windows Vista and Windows 7).__ I am just now setting-up a new computer station in my electronics room (running Ubuntu Linux 12.04), and to make it easy for myself in the future I will document everything I do when I set-up a Linux computer to program microcontrollers.

<div class="text-center img-border">

![](https://swharden.com/static/2013/01/06/mcu-programmer-far.jpg)

</div>

### Install necessary software

```bash
sudo apt-get install gcc-avr avr-libc uisp avrdude
```

### Connect the AVR programmer

This should be intuitive for anyone who has programmed AVRs before. Visit the datasheet of your MCU, identify pins for VCC (+), GND (-), MOSI, MISO, SCK, and RESET, then connect them to the appropriate pins of your programmer.

### Write a simple program in C

I made a file "main.c" and put the following inside. It's the simplest-case code necessary to make every pin on PORTD (PD0, PD1, ..., PD7) turn on and off repeatedly, sufficient to blink an LED.

```c
#include <avr/io.h>
#include <util/delay.h>

int main (void)
{
 DDRD = 255; // MAKE ALL PORT D PINS OUTPUTS

 while(1) {
  PORTD = 255;_delay_ms(100); // LED ON
  PORTD = 0;  _delay_ms(100); // LED OFF
 }

 return 0;
}
```

### Compile the code (generate a HEX file)

```bash
avr-gcc -w -Os -DF_CPU=2000000UL -mmcu=atmega8 -c -o main.o main.c
avr-gcc -w -mmcu=atmega8 main.o -o main
avr-objcopy -O ihex -R .eeprom main main.hex
```

_note that the arguments define CPU speed and chip model - this will need to be customized for your application_

### Program the HEX firmware onto the AVR

```bash
sudo avrdude -F -V -c avrispmkII -p ATmega8 -P usb -U flash:w:main.hex
```

_note that this line us customized based on my connection (-P flag, USB in my case) and programmer type (-c flag, AVR ISP mkII in my case)_

When this is run, you will see something like this:

```
avrdude: AVR device initialized and ready to accept instructions

Reading | ################################################## | 100% 0.01s

avrdude: Device signature = 0x1e9307
avrdude: NOTE: FLASH memory has been specified, an erase cycle will be performed
         To disable this feature, specify the -D option.
avrdude: erasing chip
avrdude: reading input file "main.hex"
avrdude: input file main.hex auto detected as Intel Hex
avrdude: writing flash (94 bytes):

Writing | ################################################## | 100% 0.04s

avrdude: 94 bytes of flash written
```

### Your Program should now be loaded!

Sit back and watch your LED blink.

<div class="text-center img-border">

![](https://swharden.com/static/2013/01/06/mcu-programmer-close.jpg)

</div>

* __TIP 1:__ I'm using a clone AVRISP mkII from [Fun4DIY.com](http://fun4diy.com/AVRISP_mkII.htm) which is only $11 (shipped!). I glued it to a perf-board with a socket so I can jumper its control pins to any DIP AVR (80 pins or less). I also glued a breadboard for my convenience, and added LEDs (with ground on one of their pins) for easy jumpering to test programs. You can also build your own USB AVR ISP (free schematics and source code) from the [USBtinyISP](http://www.ladyada.net/make/usbtinyisp/) project website.

* __TIP 2:__ Make a shell script to run your compiling / flashing commands with a single command. Name them according to architecture. i.e., "build-m8" or "build-t2313". Make the first line delete all .hex files in the directory, so it stalls before it loads old .hex files if the compile is unsuccessful.  Make similar shell scripts to program fuses. i.e., "fuse-m8-IntClock-8mhz", "fuse-m8-IntClock-1mhz", "fuse-m8-ExtCrystal".

* __TIP 3:__ Use a nice text editor well suited for programming. I love [Geany](http://www.geany.org/).