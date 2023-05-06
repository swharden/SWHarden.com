---
title: Using Timers and Counters to Clock Seconds
date: 2011-06-19 23:06:41
tags: ["circuit", "microcontroller", "old"]
---

# Using Timers and Counters to Clock Seconds

__My current secret project involves cramming a bunch of features into a single microcontroller.__ The chip I chose to use is an [ATMega48](http://www.swharden.com/blog/images/atmega48pinout.png). The ATMega 48 is $1.40 each in small quantities and comes crammed packed with features. The chip will be quite busy performing many functions, but its main loop will be executed at least every 50ms (required for USB, did I mention I'm bit-banging USB?!).  I desire to have a bit of RTC (real time clock) functionality in that I need to precisely measure seconds, although I don't need to actually know the time or date. I desire to execute a function once per second, consuming a minimum of resources. The solution was quite simple, but I'm choosing to document it because it's somewhat convoluted in its explanation elsewhere on the net.

__In summary, the way I accomplished this__ is using the built-in 16-bit timer (most AVRs have such a timer, including the ATTiny series). If I'm clocking the microcontroller at a known rate (determined by my selection of crystal, 12 MHz in my case), I can set the chip to continuously increment a register (timer1) and execute a function every time it overflows. Timer1 overflows at 2^16 (65,536).  I enabled a prescaler value of 256 so that it takes 256 clock pulses to increment the timer. 12MHz/256 = 46,875 Timer1 increments each second. Since Timer1 overflows at 65,536, if I initiate Timer1 at 18,661 (65,536-46,875), it will take 1 second exactly to overflow. Upon overflowing, I do something (maybe flip a LED on or off), and reset the Timer1 back to its starting value 18,661. Done! Without using an external RTC module or even an external crystal or asynchronous timer, we managed to execute a function every second on the second with minimal overhead, allowing the chip to do everything it wants in the rest of the time!

__The following example__ is a little more specific, executing a function exactly 15 times a second, and executing another function (to flash an LED) exactly every 1 second. It should be self explanatory:

```c
// This function is called every second on the second
volatile int count; // this should be global
ISR(TIMER1_OVF_vect){
    TCNT1=62411;//Initialize our varriable (set for 1/15th second)
    count++; //increment 1/15th second counter
    if(count==15){
        statusTOGGLE(); // do your event (flash a LED in my case)
        count=0;//reset global variable
        }
    }
```

```c
// This is for ATMega48, consult datasheet for variations for different chips
// place this just inside main(), before your primary loop
TCCR1B|=(1<<CS12);// prescaler 256
TIMSK1|=(1<<TOIE1); //Enable Overflow Interrupt Enable
TCNT1=62411;//Initialize our varriable (set for 1/15th second)
count=0; //Initialize a global variable
sei(); // enable interrupts
```

__I'm having a lot of fun__ spending time going through the datasheet of this chip. It has a lot of features, and some I didn't really dig deeply into. Without giving away too much of my project, I'll show some photos I'm excited to share. My project interfaces the PC through USB directly attached to 2 pins using no intermediate chips (wow!). The photos demonstrate various steps in the temperature measurement and calibration tests...

<div class="text-center img-border">

[![](https://swharden.com/static/2011/06/19/DSCN1367_thumb.jpg)](https://swharden.com/static/2011/06/19/DSCN1367.jpg)
[![](https://swharden.com/static/2011/06/19/DSCN1372_thumb.jpg)](https://swharden.com/static/2011/06/19/DSCN1372.jpg)

</div>