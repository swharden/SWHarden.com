---
title: Frequency Counter Gen2
date: 2011-07-24 17:07:24
tags: ["microcontroller", "circuit", "old"]
---

# Frequency Counter Gen2

__I'm working to further simplify my frequency counter design.__ This one is simpler than [my previous design](http://www.swharden.com/blog/2011-03-14-frequency-counter-finished/) both in hardware and software! Here's a video to demonstrate the device in its current state:

![](https://www.youtube.com/embed/FUdxwntNh1c)

**I utilize the ATMega48's hardware counter which is synchronous with the system clock, so it can only measure frequency less than half of its clock speed.** I solve this issue by dividing the input frequency by 8 and clocking the chip at 12mhz. This allows me to measure frequencies up to about 48MHz, but can be easily adapted to measure over 700MHz (really?) by dividing the input by 128. Division occurs by a 74HC590 8-bit counter (not a 74HC595 as I accidentally said in the video, which is actually a common shift register), allowing easy selection of input divided by 1, 2, 4, 8, 16, 32, 64, or 128. The following image shows the o-scope showing the original signal (bottom) and the divided-by-8 result (top)

<div class="text-center img-border">

[![](https://swharden.com/static/2011/07/24/DSCN1630_thumb.jpg)](https://swharden.com/static/2011/07/24/DSCN1630.jpg)

</div>

__The device outputs__ graphically to a LCD simply enough. That LCD is from eBay and is only $3.88 shipped! I'm considering buying a big box of them and implementing them in many more of my projects. They're convenient and sure do look nice!

<div class="text-center img-border">

[![](https://swharden.com/static/2011/07/24/DSCN1634_thumb.jpg)](https://swharden.com/static/2011/07/24/DSCN1634.jpg)

</div>

__The signal I test with__ comes from an oscillator I built several months ago.  It's actually a SA612 style receiver whose oscillator is tapped, amplified, and output through a wire. It's tunable over almost all of 40m with a varactor diode configuration. It was the start of a transceiver, but I got so much good use out of it as a function generator that I decided to leave it like it is!

<div class="text-center img-border">

[![](https://swharden.com/static/2011/07/24/DSCN1637_thumb.jpg)](https://swharden.com/static/2011/07/24/DSCN1637.jpg)

</div>

__THIS IS HOW THE PROGRAM WORKS:__ I don't supply a schematic because it's simple as could be. Divide the input frequency to something relatively slow, <1MHz at least.  Configure the 16-bit counter to accept an external pin as the counter source (not a prescaled clock, as I often use in other applications). Then set the timer value to 0, _delay_ms() a certainly amount of time (1/10th second), and read the counter value. Multiply it by 10 to account for the 1/10th second, then multiply it by 8 to account for the divider, and it's done! It will update 10 times a second, with a resolution down to 10*8 = 80 Hz. It's well within the range of amateur radio uses! If you're considering replicating this, read up on how to use hardware counters with ATMEL AVR microcontrollers. That should be enough to get you started! Here's the code I used...

For the LCD, this code requires [LCD library](http://homepage.hispeed.ch/peterfleury/avr-lcd44780.html).

```c
#include <stdlib.h>
#include <avr/io.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
#include "lcd.h"
#include "lcd.c"

int main(void)
{
    TCCR1B=0b00000111; // rising edge trigger
    char buffer[8];
    long toshow=0;
    char mhz=0;
    int khz=0;
    int hz=0;
    lcd_init(LCD_DISP_ON);
    for(;;){
        lcd_clrscr();

        lcd_gotoxy(0,0);
        itoa(mhz , buffer, 10);
        lcd_puts(buffer);
        lcd_puts(".");

        if (khz<100){lcd_puts("0");}
        itoa(khz , buffer, 10);
        lcd_puts(buffer);

        itoa(hz/100 , buffer, 10);
        lcd_puts(buffer);

        lcd_puts(" MHz");

        TCNT1=0;
        _delay_ms(99);
        _delay_us(312);
        toshow=TCNT1;
        toshow=(long)toshow*16*10; // tenth second period
        mhz=toshow/1000000;
        toshow=toshow-mhz*1000000;
        khz=toshow/1000;
        toshow=toshow-khz*1000;
        hz=toshow;
    }
}

```
