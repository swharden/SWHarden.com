---
title: Controlling Bus Pirate with Python
date: 2016-07-14 00:15:31
tags: ["microcontroller", "circuit", "obsolete"]
---

# Controlling Bus Pirate with Python

__After using the [AVR-ISP mkII](http://www.atmel.com/Images/Atmel-42093-AVR-ISP-mkII_UserGuide.pdf) for years (actually the [cheap eBay knock-offs](http://www.ebay.com/sch/i.html?_nkw=avr+isp+mkii)) to program [ATMEL AVR microcontrollers](https://en.wikipedia.org/wiki/Atmel_AVR), today I gave the [Bus Pirate ](http://dangerousprototypes.com/docs/Bus_Pirate)a shot.__ Far more than just a microcontroller programmer, this little board is basically a serial interface to basic microcontroller peripherals. In a nutshell, you plug it in via USB and it looks like a serial port which has a command-line interface that lets you do things like turn pins on and off, perform voltage measurements, and it naively supports bidirectional use of common protocols like I2C, SPI, UART, and even HD44780 series LCDs. Note that although you could directly interface with the Bus Pirate using HyperTerminal, I recommend using [TeraTerm](https://ttssh2.osdn.jp/index.html.en). It can supply voltages (3.3V and 5V) to power small circuits, and if current draw is too high (indicating something is hooked-up wrong) it automatically turns the supply off. So clever! At <$30, it's a cool tool to have around. In addition, it's naively supported as an AVR programmer by [AVRDUDE](http://www.nongnu.org/avrdude/). Although I could write assembly to perform tasks, I almost always write in C for the convenience. For my reference (and that of anyone who may want to do something similar), I'm posting the simplest-case method I use to program AVR microcontrollers with the Bus Pirate on Windows (noting that Linux would be nearly identical). ___I also wrote a Python script to connect with the Bus Pirate and run simple commands___ (which turns the power supply on and report the voltage of the VCC line immediately after programming completes).  Yes, there are [fancy packages](http://dangerousprototypes.com/docs/Bus_Pirate_Scripting_in_Python) that allow you to interact with Bus Pirate from Python, but ___the advantage of my method is that it runs from native Python libraries! ___To get this all up and running for yourself, just install [WinAVR ](http://winavr.sourceforge.net/)(which supplies AVRDUDE and AVR-GCC) and Python 3. I assume this code will work just as well on Python 2, but haven't tried.

<div class="text-center img-border">

![](https://swharden.com/static/2016/07/14/IMG_7092-1.jpg)

</div>

__To ensure my Bus Pirate is working properly, I start off by running the Bus Pirate's built-in test routine.__ For full details read the [guide](http://dangerousprototypes.com/docs/Bus_Pirate_self-test_guide). It just involves connecting two pairs of pins together as shown in the picture here, connecting to the Bus Pirate with the serial terminal, and running the command "~". It will output all sorts of useful information. Once I know my hardware is up and running, I'm good to continue.

<div class="text-center">

![](https://swharden.com/static/2016/07/14/Bpv3v2go-pinout.png)

</div>

__Here's the code which runs on the microcontroller to twiddle all the pins (saved as main.c).__ Note that my MCU is an [ATTiny85](http://www.atmel.com/images/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf). I'm using standard clock settings (internal RC clock, 8MHz), but if I wanted to modify fuses to do things like use an external clock source or crystal, I'd calculate them with [engbedded's handy dandy fuse calculator](http://www.engbedded.com/fusecalc/) (which also shows AVRdude arguments needed to make the change!).

```c
#define F_CPU (8000000UL)
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

__To compile the code and program the MCU with it__, I always have a bash script in the same folder that I can double-click on to delete old compiled files (so we don't accidentally re-program our MCU with old code), compile main.c, and load it onto the MCU using the Bus Pirate. You may have to change COM3 to reflect the com port of your Bus Pirate. Note that it is required that you disconnect other terminals from the Bus Pirate before doing this, otherwise you'll get an "access denied" error.

```bash
@echo off
del *.elf
del *.hex
avr-gcc -mmcu=attiny85 -Wall -Os -o main.elf main.c
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
avrdude -c buspirate -p attiny85 -P com3 -e -U flash:w:main.hex
python up.py
```

Although the programmer briefly supplies my MCU with power from the +5V pin, it's cut after programming completes. Rather than manually re-opening my terminal program, re-connecting with the bus pirate, re-setting the mode (command "m") to something random (DIO, command "9"), and re-enableing voltage output (command "W") just to see my LED blink, I want all that to be automated. Thanks python for making this easy. The last line calls "up.py". This fancy script even outputs the voltage of the VCC line after it's turned on!

### Python3 Control of Bus Pirate

```python
import serial

BUSPIRATE_PORT = 'com3' #customize this! Find it in device manager.

def send(ser,cmd):
    """send the command and listen to the response."""
    ser.write(str(cmd+'\n').encode('ascii')) # send our command
    for line in ser.readlines(): # while there's a response
        print(line.decode('utf-8').strip()) # show it

ser=serial.Serial(BUSPIRATE_PORT, 115200, timeout=1) # is com free?
assert ser.isOpen() #throw an exception if we aren't connected
send(ser,'#') # reset bus pirate (slow, maybe not needed)
send(ser,'m') # change mode (goal is to get away from HiZ)
send(ser,'9') # mode 9 is DIO
send(ser,'W') # turn power supply to ON. Lowercase w for OFF.
send(ser,'v') # show current voltages
ser.close() # disconnect so we can access it from another app
print("disconnected!") # let the user know we're done.

```

When "burn.cmd" is run, the code is compiled and loaded, the power supply is turned on (and killed if too much current is drawn!), and the voltage on VCC is reported. The output is:

```
C:\Users\scott\Documents\important\AVR\2016-07-13 ATTiny85 LEDblink>burn.cmd

Detecting BusPirate...
**
**  Bus Pirate v3a
**  Firmware v5.10 (r559)  Bootloader v4.4
**  DEVID:0x0447 REVID:0x3046 (24FJ64GA002 B8)
**  http://dangerousprototypes.com
**
BusPirate: using BINARY mode
avrdude: AVR device initialized and ready to accept instructions

Reading | ################################################## | 100% 0.12s

avrdude: Device signature = 0x1e930b
avrdude: erasing chip
avrdude: reading input file "main.hex"
avrdude: input file main.hex auto detected as Intel Hex
avrdude: writing flash (84 bytes):

Writing | ################################################## | 100% 3.12s

avrdude: 84 bytes of flash written
avrdude: verifying flash memory against main.hex:
avrdude: load data flash data from input file main.hex:
avrdude: input file main.hex auto detected as Intel Hex
avrdude: input file main.hex contains 84 bytes
avrdude: reading on-chip flash data:

Reading | ################################################## | 100% 2.72s

avrdude: verifying ...
avrdude: 84 bytes of flash verified

avrdude: safemode: Fuses OK

avrdude done.  Thank you.
```

```
#
RESET

Bus Pirate v3a
Firmware v5.10 (r559)  Bootloader v4.4
DEVID:0x0447 REVID:0x3046 (24FJ64GA002 B8)
http://dangerousprototypes.com

HiZ>
m
1. HiZ
2. 1-WIRE
3. UART
4. I2C
5. SPI
6. 2WIRE
7. 3WIRE
8. LCD
9. DIO
x. exit(without change)

(1)>
9
Ready
DIO>
W
Power supplies ON
DIO>
v
Pinstates:
1.(BR)  2.(RD)  3.(OR)  4.(YW)  5.(GN)  6.(BL)  7.(PU)  8.(GR)  9.(WT)  0.(Blk)
GND     3.3V    5.0V    ADC     VPU     AUX     CLK     MOSI    CS      MISO
P       P       P       I       I       I       I       I       I       I
GND     3.17V   5.00V   0.00V   0.00V   L       L       L       H       L
DIO>
disconnected!
```

__This is a minimal-case scenario, but can be obviously expanded to perform some complicated tasks!__ For example, all commands could be run from a single python program. Considering the Bus Pirate's ability to communicate with so many different protocols (I2C, 2-write, etc.), being able to naively control it from Python without having to install special additional libraries will certainly prove to be convenient.

_PS: I noted there is a surprising delay when initializing programming the AVR with the bus pirate. The process hangs for about 10 seconds after the bus pirate introduces itself with the welcome message, then seems to resume at full speed writing to the flash of the microchip. After a bit of Googling, I believe the delay is due to the Bus Pirate slowly bit-banging SPI to initialize the programming sequence. The AVR has [rich SPI functionality](http://maxembedded.com/2013/11/the-spi-of-the-avr/), some of which involves its own programming. Satisfied with this answer for now, I'm not going to try to speed it up. It's a little annoying, but not too bad that I won't use this to program my AVRs._