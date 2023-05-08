---
title: Ridiculously Simple AVR AM Radio Transmitter
date: 2011-08-06 19:32:44
tags: ["amateur radio", "circuit", "obsolete"]
---

# Ridiculously Simple AVR AM Radio Transmitter

__I was brainstorming some RF circuits today__ and I had the desire to create a rapid transmitter/receiver pair that anyone would have around their house. I decided that AM or FM radio would be good since everyone can receive that, and pondered how best to generate the necessary radio signal and modulate it appropriately.  After a few LC oscillator designs, I thought about the RC oscillators built into most micro-controllers. I grabbed an ATMEL AVR I had on hand (an ATTiny44A) and checked the datasheet. It had an 8MHz RC oscillator, which could be divided-down to 1MHz, and output on a CKOUT pin - all configurable with a few hardware fuses! Note that commercial AM radio stations are between 0.52 and 1.61 MHz, so a 1MHz signal would be smack-dab in the middle of our radio dial! I had to build a prototype to see how well it would work. Once concern was that the RC  oscillator wouldn't be stable enough to produce reliable audio - boy was I wrong!

<div class="text-center img-medium">

![](https://swharden.com/static/2011/08/06/schem.jpg)

</div>
__The circuitry is textbook simple.__ Appropriately configured, the AVR generates 5V square waves from its CKOUT pin. Although a pretty shape, they're not powerful enough on their own to be heard across a room, so I needed an amplifier stage. A class C amplifier provided by a 2n7000 is commonly done in the low power amateur radio (QRP) community, so I went with it. A 2n7000 N-channel MOSFET with a 220-ohm resistor on the drain and the CKOUT directly into the gate did a fine job (I've used this design for 10MHz QRSS transmitters before), and I was able to modulate its amplitude by feeding the voltage from a MCU pin (turned on/off rapidly) through a decoupling capacitor into the drain of the MOSFET. I couldn't have asked for a simpler result!

{{<youtube 1VCkhPTAHjY>}}

__This code sends a message in Morse code.__ It seems too easy!  Applications are endless, as this is one heck of an easy way to send audio from a micro-controller to a radio, and possibly to a computer. Morse code is easy, and since we have the ability to dynamically generate different audio frequencies and tones, data exchange is easy too!  Nothing's stopping you from adding the code to turn this into a RTTY (or [Hellschreiber?](http://www.swharden.com/blog/2011-08-05-i-before-e-except-after-hellschreiber/)) transmitter.


<div class="text-center img-border">

![](https://swharden.com/static/2011/08/06/DSCN1670.jpg)

</div>

__Again, this transmitter can be heard on a standard AM radio tuned to about 1000 kHz.__ This is the setup I used with great success:

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/06/schem2.jpg)

</div>

__Here's the code on the chip!__ Nothing complicated:

```c

// designed for and tested with ATTiny44A
#include <avr/io.h>
#define F_CPU 1000000UL
#include <avr/delay.h>
#include <avr/interrupt.h>

void beep(){
    for(char i=50;i;i--){
        DDRA|=_BV(PA7);_delay_ms(1);
        DDRA&=~_BV(PA7);_delay_ms(1);
    }
}

void rest(){_delay_ms(100);}

void dot(){beep();rest();}
void dash(){beep();beep();beep();rest();}
void space(){rest();rest();}
void space2(){space();space();}

int main(){
    DDRA|=_BV(PA7);
    for(;;){
        dot();dot();dot();space();             // S
        dash();dot();dash();dot();space();     // C
        dash();dash();dash();space();          // O
        dash();space();                        // T
        dash();space();                        // T
        space2();
        dot();dash();dot();space();            // R
        dash();dash();dash();space();          // O
        dash();dot();dash();dot();space();     // C
        dash();dot();dash();space();           // K
        dot();dot();dot();space();             // S
        _delay_ms(1000); // silence
    }
    return 0;
}
```

___THIS IS ILLEGAL__ to do if you exceed a certain amount of power because you're stepping on legitimate commercial broadcasters and will have to deal with the FCC. Additionally, you are transmitting on more frequencies than the primary frequency because the signal is heavy in odd harmonics. This means a 1 MHz transmitter, producing square waves, will generate tones on 1, 3, 5, 7 MHz, etc. Don't do this with much power! Heck, you probably shouldn't do it at all ;-)_