---
title: Directly Driving 7-Segment Display with AVR IO Pins
date: 2014-02-27 16:19:53
tags: ["circuit", "obsolete"]
---



__I came across the need for a quick and dirty display to show a 4 digit number from a microcontroller.__ The _right_ way to do this would be to use a microcontroller in combination with a collection of transistors and current limiting resistors, or even a dedicated 7-segment LED driver IC. The _wrong_ way to do this is to wire LEDs directly to microcontroller IO pins to source and sink current way out of spec of the microcontroller... and that's <span style="text-decoration: underline;">exactly</span> what I did! With no current limiting resistors, the AVR is sourcing and sinking current potentially far out of spec for the chip. But, heck, it works! With 2 components (just a microcontroller and a 4 digit, 7-segment LED display) and a piece of ribbon cable, I made something that used to be a nightmare to construct (check out this post from 3 years ago when I accomplished the same thing [with a rats nest of wires](http://www.swharden.com/blog/2011-03-14-frequency-counter-finished/) - it was so much work that I never built one again!) The hacked-together method I show today might not be up to spec for medical grade equipment, but it sure works for my test rig application, and it's easy and cheap to accomplish... as long as you don't mind breaking some electrical engineering rules. Consider how important it is to know how to hack projects like this together: Although I needed this device, if it were any harder, more expensive, or less convenient to build, I simply wouldn't have built it! Sometimes hacking equipment together the wrong way is worth it.

<div class="text-center img-border">

![](https://swharden.com/static/2014/02/27/IMG_2316.jpg)

</div>

Segments are both current sourced and sunk directly from AVR IO pins. Digits are multiplexed with 1ms illumination duration. I don't really have a part number for the component because it was a China eBay special. The display was $6.50 for 4 (free shipping). That's ~$1.65 each. The microcontroller is ~$1.[/caption]

__SCHEMATIC?__ If you want it, read this. It's so simple I don't feel like making it. Refer to an [ATMega48 pin diagram](http://www.swharden.com/blog/images/atmega48pinout.png). The LCD is common anode (not common cathode), and here's the schematic on the right. I got it from eBay ([link](http://www.ebay.com/itm/4Pcs-7seg-4digit-LED-Display-work-with-arm7-MCU-Arduino-/280533977596?ssPageName=ADME:L:OC:US:3160)) for <$2.  The connections are as follows:


<div class="text-center ">

![](https://swharden.com/static/2014/02/27/common-cathode-7-segment-display-lcd.jpg)

</div>

*   Segments (-) A...H are directly wired to PD0...PD7 
  * I call the decimal point (dp) segment "H" - I don't use current limiting resistors. I'm not making a consumer product. It works fine, especially multiplexed. Yeah I could use transistors and CLRs to drive the segments to have them bright and within current specifications, but I'm not building an airplane or designing a pacemaker, I'm making a test device at minimum cost! Direct LED wiring to my microcontroller is fine for my purposes.
  * I am multiplexing the characters of my display. I could have used a driver IC to simplify my code and eliminate the current / wiring issues described above. 
  * A [MAX7219 or MAX7221](http://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf) would have been easy choices for this (note common anode vs. common cathode drivers / displays). It adds an extra $5 to my project cost though, so I didn't go with a driver. I drove the segments right out of my IO pins.

*   Characters (+) 1...4 are PC0...PC3

*   Obviously I apply +5V and GND to the appropriate AVR pins

__Here it all is together in my microcontroller programming set up.__ I'll place this device in a little enclosure and an an appropriate BNC connector and either plan on giving it USB power or run it from 3xAA batteries. For now, it works pretty darn well on the breadboard.

<div class="text-center img-border">

![](https://swharden.com/static/2014/02/27/IMG_2320.jpg)

</div>

Here is my entire programming setup. On the top left is my eBay special USB AVR programmer. On the right is a little adapter board I made to accomodate a 6 pin ISP cable and provide a small breadboard for adding programming jumpers into a bigger breadboard. The breadboard at the bottom houses the microcontroller and the display. No other components! Well, okay, a 0.1uF decoupling capacitor to provide mild debouncing for the TTL input.

__Let's talk about the code.__ Briefly, I use an infinite loop which continuously displays the value of the volatile long integer "numba". In the display function, I set all of my segments to (+) then momentarily provide a current sink (-) on the appropriate digit anode for 1ms. I do this for each of the four characters, then repeat. How is the time (the value of "numba") incremented? Using a hardware timer and its overflow interrupt! It's all in the ATMega48 datasheet, but virtually every microcontroller has some type of timer you can use to an equivalent effect. See my earlier article "[_Using Timers and Counters to Clock Seconds_](http://www.swharden.com/blog/2011-06-19-using-timers-and-counters-to-clock-seconds/)" for details. I guess that's pretty much it! I document my code well enough below that anyone should be able to figure it out. The microcontroller is an [ATMega48](http://www.atmel.com/images/doc2545.pdf) (clocked 8MHz with an internal RC clock, close enough for my purposes).

```c
#define F_CPU 8000000UL // 8mhz
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// for simplicity, define pins as segments
#define A (1<<PD0)
#define B (1<<PD1)
#define C (1<<PD2)
#define D (1<<PD3)
#define E (1<<PD4)
#define F (1<<PD5)
#define G (1<<PD6)
#define H (1<<PD7)

void setDigit(char dig){ // set the digit starting at 0
    PORTC=(1<<dig)|(1<<PC4); // always keep the PC4 pin high
}

void setChar(char c){
    // given a number, set the appropraite segments
    switch(c){
        case 0:    DDRD=A|B|C|D|E|F;    break;
        case 1:    DDRD=B|C;            break;
        case 2:    DDRD=A|B|G|E|D;        break;
        case 3: DDRD=A|B|G|C|D;        break;
        case 4: DDRD=F|G|B|C;        break;
        case 5: DDRD=A|F|G|C|D;        break;
        case 6: DDRD=A|F|G|E|C|D;    break;
        case 7: DDRD=A|B|C;            break;
        case 8: DDRD=A|B|C|D|E|F|G;    break;
        case 9: DDRD=A|F|G|B|C;        break;
        case 31: DDRD=H;            break;
        default: DDRD=0;             break;
    }
}

void flashNumber(long num){
    char i;

    for (i=0;i<4;i++){
        setChar(num%10);
        if (i==2){DDRD|=H;} // H is the decimal point
        setDigit(3-i);
        num=num/10;
        _delay_ms(1); // time to leave the letter illuminated
    }
}

volatile long numba = 0;
volatile long addBy = 1;

ISR(PCINT1_vect){ // state change on PC4
    if ((PINC&(1<<PC4))==0) {addBy=0;} // pause
    else {numba=0;addBy=1;} // reset to 0 and resume
}

ISR(TIMER1_OVF_vect){
    TCNT1=65536-1250; // the next overflow in 1/100th of a second
    numba+=addBy;      // add 1 to the secound counter
}

int main(void)
{
    DDRC=(1<<PC0)|(1<<PC1)|(1<<PC2)|(1<<PC3); // set all characters as outputs
    DDRD=255;PORTD=0;     // set all segments as outputs, but keep them low

    TCCR1B|=(1<<CS11)|(1<<CS10); // prescaler 64
    TIMSK1|=(1<<TOIE1); //Enable Overflow Interrupt Enable
    TCNT1=65536-1250;   // the next overflow in 1/100th of a second

    // note that PC4 (PCINT12) is an input, held high, and interrupts when grounded
    PCICR |= (1<<PCIE1); // enable interrupts on PCING13..8 -> PCI1 vector
    PCMSK1 |= (1<<PCINT12); // enable PCINT12 state change to be an interrupt
    sei(); // enable global interrupts

    for(;;){flashNumber(numba);} // just show the current number repeatedly forever
}
```

I edit my code in [Notepad++](http://notepad-plus-plus.org/) by the way. To program the chip, I use a bash script...

```bash
avr-gcc -mmcu=atmega48 -Wall -Os -o main.elf main.c -w
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
avrdude -c usbtiny -p m48 -F -U flash:w:"main.hex":a -U lfuse:w:0xe2:m -U hfuse:w:0xdf:m
```

__Nothing here is groundbreaking.__ It's simple, and convenient as heck. Hopefully someone will be inspired enough by this write-up that, even if they don't recreate _this_ project, they'll jump at the opportunity to make something quick and dirty in the future. It's another example that goes to show that you don't have to draw schematics, run simulations, do calculations and etch boards to make quick projects. Just hack it together and use it.

__Update a two days later... __I found a similarly quick and dirty way to package this project in an enclosure. I had on hand some 85x50x21mm project boxes (eBay, 10 for $14.85, free shipping, about $1.50 each) so I used a [nibbler](http://www.amazon.com/Hand-Sheet-Metal-Nibbler-Cutter/dp/B000T5FV4Q) to hack out a square to accomodate the display. After a little super glue, ribbon cable, and solder, we're good to go!

<div class="text-center img-border">

![](https://swharden.com/static/2014/02/27/IMG_2336.jpg)
![](https://swharden.com/static/2014/02/27/IMG_2351.jpg)
![](https://swharden.com/static/2014/02/27/IMG_2355.jpg)
![](https://swharden.com/static/2014/02/27/IMG_2356.jpg)
![](https://swharden.com/static/2014/02/27/IMG_2362.jpg)
![](https://swharden.com/static/2014/02/27/IMG_2380.jpg)

</div>

__Related reading for the technically inclined:__

*   [Interfacing LEDs with the AVR microcontroller](http://www.avr-tutorials.com/interfacing/interfacing-leds-avr-microcontroller) (the right way)
*   [Driving LEDS with vs. without a current limiting resistor](http://tinkerlog.com/2009/04/05/driving-an-led-with-or-without-a-resistor/) (nice write-up!)
*   Official datasheet for [driving LCDs with AVR](http://www.atmel.com/Images/doc2569.pdf) (not LEDs)
*   Official datasheet for [using AVR timers](http://www.atmel.com/Images/doc2505.pdf)

