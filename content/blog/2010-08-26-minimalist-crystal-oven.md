---
title: Minimalist Crystal Oven
date: 2010-08-26 10:40:16
tags: ["circuit", "qrss", "old", "microcontroller"]
---

# Minimalist Crystal Oven

__So I'm working on building a crystal oven__ to keep my QRSS MEPT (radio transmitter) at an extremely stable frequency. Even inside a thick Styrofoam box, slight changes in my apartment temperature caused by the AC turning on and off is enough to change the crystal temperature of the transmitter, slightly modifying its oscillation frequency. For a device that vibrates exactly 10,140,070 times a second, even 3 to many or too few vibrations per second is too much. Keeping in the spirit of hacking things together with a minimum of parts, this is what I came up with!

{{<youtube P3tmFMWZn90>}}

__It uses a thermistor, potentiometer, and comparator of a microcontroller (ATTiny44a)__ to tightly sense and regulate temperature. The heater element is a junk MOSFET I found in an old battery backup system. I simply have pass a ton of current (turned on/off by the gate) to generate heat, transferred into a piece of steel for smooth regulation. One of the unexpected advantages is that the light flickers rapidly near equilibrium, which is great because it has the ability to turn the heater on a little or a lot based upon the averaging effect of the flicker. Here is the code I wrote on the microcontroller to handle the comparator. It couldn't be simpler!

```c
#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
    DDRA = 0;   // all inputs
    DDRB = 255; // all outputs

    while (1)
    {
        if (ACSR & _BV(ACO))
        {
            /* AIN0 is more positive than AIN1 right now */
            PORTB |= (1 << PB0);
            PORTB &= ~(1 << PB1);
        }
        else
        {
            /* AIN0 is more negative than AIN1 */
            PORTB |= (1 << PB1);
            PORTB &= ~(1 << PB0);
        }
    }
}
```

