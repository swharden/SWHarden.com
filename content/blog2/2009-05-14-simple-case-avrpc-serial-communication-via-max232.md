---
title: Simple Case AVR/PC Serial Communication via MAX232
date: 2009-05-14 11:00:19
tags: ["microcontroller", "circuit", "obsolete"]
---

# Simple Case AVR/PC Serial Communication via MAX232

__I recently had the desire__ to be able to see data from an ATMEL AVR microcontroller (the [ATTiny2313](http://www.SWHarden.com/blog/images/attiny-2313.gif)) for development and debugging purposes.  I wanted an easy way to have my microcontroller talk to my PC (and vise versa) with a minimum number of parts.  The easiest way to do this was to utilize the [UART](http://en.wikipedia.org/wiki/UART) capabilities of the [ATTiny2313](http://www.SWHarden.com/blog/images/attiny-2313.gif) to talk to my PC through the serial port. One problem is that the [ATTiny2313](http://www.SWHarden.com/blog/images/attiny-2313.gif)(as with most microcontrollers) puts out 5V for "high" (on) and 0V for "low" (off).  The RS-232 standard (which PC serial ports use) required -15V for high and +15v for low!  Obviously the microcontroller needs some help to achieve this.  The easiest way was to use the [MAX232 serial level converter](http://en.wikipedia.org/wiki/MAX232) which [costs about 3 bucks at DigiKey](http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&amp;name=MAX232CPE%2B-ND). Note that it requires a few 10uF capacitors to function properly.

<div class="text-center img-border">

![](https://swharden.com/static/2009/05/14/serialcircuit.png)

</div>

__Here's a more general schematic:__


<div class="text-center">

![](https://swharden.com/static/2009/05/14/max232_serial_microcontroller.gif)

</div>

__I connected my ATTiny2313 to the MAX232__ in a very standard way. (photo)   MAX232 pins 13 and 14 go to the serial port, and the ATTiny2313 pins 2 and 3 go to the MAX232 pins 12 and 11 respectively.  I will note that they used a oscillator value (3.6864MHz) different than mine (9.216MHz).

__Determining the speed of serial communication__ is important.  This is dependent on your oscillator frequency!  I said I used a 9.216Mhz oscillator.  First, a crystal or ceramic oscillator is required over the internal RC oscillator because the internal RC oscillator is not accurate enough for serial communication.  The oscillator you select should be a perfect multiple of 1.8432MHz. Mine is 5x this value.  Many people use 2x this value (3.6864Mhz) and that's okay!  You just have to make sure your microchip knows (1) to use the external oscillator (google around for how to burn the fuses on your chip to do this) and (2) what the frequency of your oscillator is and how fast it should be sending data.  This is done by setting the UBRRL value.  The formula to do this is here:

<div class="text-center">

![](https://swharden.com/static/2009/05/14/ubrrformula.gif)

</div>

__The datasheet of your microcontroller__ may list a lot of common crystal frequencies, bandwidths, and their appropriate UBRR values.  However my datasheet lacked an entry for a 9.216MHz crystal, so I had to do the math myself.  I Googled around and no "table" is available!  Why not make one? (picture, below).  Anyway, for my case I determined that if I set the UBRR value to 239, I could transmit data at 2800 baud (bits/second).  This is slow enough to ensure accuracy, but fast enough to quickly dump a large amount of text to a PC terminal.

<div class="text-center">

![](https://swharden.com/static/2009/05/14/ubrr-table.gif)

</div>

## AVR Baud Calculator

This will make your life easier. The page <a href="http://www.wormfood.net/avrbaudcalc.php">wormfood.net/avrbaudcalc.php</a> has a chart of common crystals and the baud rates they work best with! Try to pick a combination that provides the least error possible...

__This is the bare-minimum code__ to test out my setup. Just load the code (written in C, compiled with avr-gcc) onto your chip and it's ready to go.  Be sure you set your fuses to use an external oscillator and that you set your UBRRL value correctly.

```c
#include <avr/io.h>  
#include <avr/interrupt.h>  
#include <util/delay.h>  

int main (void)  
{  
  unsigned char data=0;  
  UBRRL = 239;  
  UCSRB = (1 < < RXEN) | (1 << TXEN);  
  UCSRC = (1 < < UCSZ1) | (1 << UCSZ0);  

  for (;;)  
  {  
    if (data>'Z'||data< 'A')  
    {  
      UDR = 10; UDR = 13; data='A';_delay_ms(100);  
    }  
    
    UDR = data;  
    data += 1;  
    _delay_ms(100);  
  }  
}  
```

__Once you load it, it's ready to roll!__  It continuously dumps letters to the serial port.  To receive them, open HyperTerminal (on windows, under accessories) or minicom (on Linux, look it up!).  Set your baud rate to 2800 (or whatever you selected) and you're in business.  This (picture below) is the output of the microcontroller to HyperTerminal on my PC.  Forgive the image quality, I photographed the LCD screen instead of taking a screenshot.

<div class="text-center img-border">

![](https://swharden.com/static/2009/05/14/avr_serial_console.jpg)

</div>

__This is the circuit__ which generates the output of the previous image.  I have a few extra components.  I have an LED which I used for debugging purposes, and also a switch (labeled "R").  The switch (when pressed) grounds pin 1 of the ATTiny2313 which resets it.  If I want to program the chip, I hold "R" down and the PC can program it with the inline programmer ["parallel port, straight-through, DAPA style](https://wikis.mit.edu/confluence/download/attachments/20512/dapa.png)).  One cable going into the circuit is for the parallel port programmer, one cable is for the serial port (data transfer), and one is for power (5v which I stole from a USB port).

<div class="text-center img-border">

![](https://swharden.com/static/2009/05/14/avr_max232.jpg)

</div>

__I hope you found this__ information useful.  Feel free to [contact me](http://www.swharden.com/blog/send-scott-a-message/) with any questions you may have, but realize that I'm no expert, and I'm merely documenting my successes chronologically on this website.