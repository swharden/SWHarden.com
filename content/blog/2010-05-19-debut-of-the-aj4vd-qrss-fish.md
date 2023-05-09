---
title: Debut of the AJ4VD QRSS Fish
date: 2010-05-19 19:58:16
tags: ["python", "qrss", "obsolete"]
---



__Finally!__ After a few years tumbling around in my head, a few months of reading-up on the subject, a few weeks of coding, a few days of bread-boarding, a few hours of building, a few minutes of soldering, and a few seconds of testing I've finally done it - I've created my first QRSS transmitter! I'll describe it in more detail once I finalize the design, but for now an awesome working model. It's all digital, consisting of 2 ICs (an ATTiny44a for the PWM-controlled frequency modulation, and an octal buffer for the pre-amplifier) followed by a simple pi low-pass filter.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/19/qrss-desk.jpg)

</div>

__My desk is a little messy.__ I'm hard at work! Actually, I'm thinking of building another desk. I love the glass because I don't have to worry (as much) about fires. That sounds scary, I know.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/19/qrss-transmitter.jpg)

</div>

__This is the transmitter.__ The box is mostly empty space, but it consists of the circuit, an antenna connection, a variable capacitor for center frequency tuning, and a potentiometer for setting the degree of frequency shift modulation.

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/19/qrss-fish.png)

</div>

__Yeah, that's a fishy. __Specifically a goldfish (the cracker). It's made with a single tone, shifting rapidly (0.5 sec) between tones. So cool. Anyway, I'm outta here for now - getting back to the code! I think I'll try to make a gator next...

__Here's the code that makes the fish.__ It sends my ID quickly, some fish, then my ID in QRSS speed using PWM.

```c
#include <avr/io.h>
#include <util/delay.h>

const int tDit = 270 / 3;
const int tDah = 270;

char fsk;
unsigned long int t_unit;

void delay()
{
    _delay_loop_2(t_unit);
}

void blink()
{
    PORTA ^= (1 << 0);
    PORTA ^= (1 << 1);
    PORTA ^= (1 << 2);
    PORTA ^= (1 << 3);
}

void tick(unsigned long ticks)
{
    while (ticks > 0)
    {
        delay();
        delay();
        ticks--;
    }
}

void pwm_init()
{
    //Output on PA6, OC1A pin (ATTiny44a)
    OCR1A = 0x00;  //enter the pulse width. We will use 0x00 for now, which is 0 power.
    TCCR1A = 0x81; //8-bit, non inverted PWM
    TCCR1B = 1;    //start PWM
}

void set(int freq, int dly)
{
    OCR1A = freq;
    tick(dly);
}

void fish()
{
    char f[] = {0, 0, 0, 4, 5, 3, 6, 2, 7, 1, 5, 6, 8, 1, 8, 1, 8, 1, 8, 1, 8, 2, 7, 3, 6, 2, 7, 1, 8, 1, 8, 4, 5, 2, 3, 6, 7, 0, 0, 0};
    char i = 0;
    while (i < sizeof(f))
    {
        i++;
        OCR1A = 255 - f[i] * 15;
        blink();
        tick(20);
    }
}

void id()
{
    char f[] = {0, 0, 1, 2, 0, 1, 2, 2, 2, 0, 1, 1, 1, 1, 2, 0, 1, 1, 1, 2, 0, 2, 1, 1, 0, 0};
    char i = 0;
    while (i < sizeof(f))
    {
        blink();
        if (f[i] == 0)
        {
            OCR1A = 255;
            tick(tDah);
        }
        if (f[i] == 1)
        {
            OCR1A = 255 - fsk;
            tick(tDit);
        }
        if (f[i] == 2)
        {
            OCR1A = 255 - fsk;
            tick(tDah);
        }
        blink();
        OCR1A = 255;
        tick(tDit);
        i++;
    }
}

void slope()
{
    char i = 0;
    while (i < 25)
    {
        OCR1A = 255 - i;
        i++;
    }
    while (i > 0)
    {
        i--;
        OCR1A = 255 - i;
    }
}

int main(void)
{
    DDRA = 255;
    PORTA ^= (1 << 0);
    PORTA ^= (1 << 1);
    pwm_init();

    t_unit = 2300;
    fsk = 50;
    id(); // set to fast and ID once

    fsk = 50;
    t_unit = 65536; // set to slow for QRSS

    while (1)
    {
        id();
        for (char i = 0; i < 3; i++)
        {
            fish();
        }
    }

    return 1;
}
```

