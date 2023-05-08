---
title: Full-Auto Rapidfire Mouse Modification
date: 2010-12-28 01:52:09
tags: ["circuit", "microcontroller", "obsolete"]
---



__I did this purely for the fun of it, and am aware there are many ways to accomplish the same thing.__ I was playing [Counter Strike Source](http://store.steampowered.com/css) (you should buy it and play with me, name "swharden") and my fingers are really cold from the winter weather, and wondered if I could have a button help with the rapid firing of pistols.  I mentioned it on the microphone, and one of the players ("{Ẋpli¢it} shadow") said I should go for it.  Because it was a fun little project, I documented it so I could share it. Check out the cool photos and video!

{{<youtube pxHLXyPt6N8>}}

__There's a summary of the project in video form.__ Some details of the project are below...

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-1.jpg)

</div>

__Here you can see the original circuit board in the mouse. __The microchip on the bottom right of the image seems to do the data processing, so I investigated it a bit and found the pin that the left-click button goes to.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-2.jpg)

</div>

__Here's the underside.__ It helped me identify good locations to grab +5V and GND solder points.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-3.jpg)

</div>

__This is the microcontroller I decided to use for the project.__ It's an ATTiny25, $1.33 USD (10+ quantity from Mouser), and has a built in 8MHz oscillator (which can run at 1MHz thanks to the DIV/8 clock prescaler.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-4.jpg)

</div>

__I slap the chip in the homebrew development board__ (a glorified AVR-ISP mkII) and it's ready for programming. Code and schematics are at the bottom.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-5.jpg)

</div>

__After programming, I glued the microchip__ upside-down in the mouse case and soldered wires directly to the pins. I used small (about 28AWG) magnet wire because it's a lot easier than stripping wires. Just heat the tip with a soldering iron, the coating melts away, and you can stick it wherever you need to with a dab of solder. Not too many people use this method, but I recommend you try it at least once! It can be very useful at times, and is about as cheap as you can get. (eBay has good prices)

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-6.jpg)

</div>

__BIG PROBLEM!__ It didn't work *AT ALL*. Why? Didn't know... I checked the o-scope and saw everything seemed to be working fine.  It turns out that 50 clicks per second was too fast to register, and when I reduced the speed to 25 clicks per second it worked fine. Unfortunately I had to add extra wires to allow myself to program the chip while it was in the mouse - a major pain that complicated the project more than I wished!

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-7.jpg)

</div>

__Here's a good view of the transistor. __ Simply put, when the microcontroller sends power to the "base" pin of the 2n2222 transistor, the "collector" is drained through the "emitter", and the transistor acts like a switch. It's shorting the pin, just like would happen if you physically pressed the left click mouse button. When the mouse microchip is positive (+5V), it's "no click", but when it goes to ground (shorted by the click button), a click is detected. I biased the "base" pin toward ground by connecting it to GND through a high value resistor. This makes sure it doesn't accidentally fire when it's not supposed to.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-8.jpg)

</div>

__Here you can clearly see the programmer pins I added.__ This lets me quickly access the chip and reprogram it if I decide to add/modify functionality.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-9.jpg)

</div>

__When it's all said and done, it's surprisingly slick and functional. __ I'm using it right now to write my blog, and the button isn't really in the way. I think it's one of those el-cheapo buttons you get in a pack of 10 from RadioShack, but I would highly recommend eBay as RadioShack is ridiculously overpriced on components.

<div class="text-center img-border">

![](https://swharden.com/static/2010/12/28/rapidfire_mouse_mod-10.jpg)

</div>

__There's the schematic.__  Grabbing 5v and GND from a usb mouse is trivial. Heck, most of the circuity/code is trivial!  Now that I think about it, this represents are really great starter project for anyone interested in microcontrollers.

<div class="text-center">

![](https://swharden.com/static/2010/12/28/ATtiny25-45-85V.jpg)

</div>

__Use this diagram of the pin functions for reference.__

__Remember there's more than one way to skin a cat!__ For example, if you don't want to program a microcontroller, a 555 timer is a simple method and there are tutorials out there demonstrating how to do this.  I chose a microcontroller because I can precisely control the rate of firing and the duration. If you decide to do something similar, send me photos and I'd be happy to share them on the site!  I love doing tangible projects, however silly they are.

__And finally, the code!__

```c
#define F_CPU 1000000UL // frequency (20MHz)
#include <avr/io.h>
#include <util/delay.h>

void on()
{
    PORTB |= 1 << PB3; //led
    PORTB |= 1 << PB2; //heater
}
void off()
{
    PORTB &= ~(1 << PB3); //led
    PORTB &= ~(1 << PB2); //heater
}

void main()
{
    DDRB |= (1 << PB3) | (1 << PB2);
    int ticks;

    for (;;)
    { //FOREVER
        while ((PINB & _BV(PB4)) == 0)
        {
        }                                     // NOT PRESSED, DO NOTHING
        for (ticks = 0; ticks < 125; ticks++) // CLICK FOR 5 seconds
        {
            on();
            _delay_ms(20);
            off();
            _delay_ms(20);
        } // CLICK TAKES 1/50'th second
    }
}
```
