---
title: Debut of the AJ4VD QRSS Gator
date: 2010-05-22 18:41:54
tags: ["qrss", "obsolete"]
---

# Debut of the AJ4VD QRSS Gator

__I re-wrote the code__ from the previous entry to do several things. Once of which was to make a gator rather than a fish. It's more appropriate since I'm planning on housing the transmitter at the University of Florida. To do it, I drew a gator in paint and wrote a python script to convert the image into a series of points. I'll post it later. One thing to note was that size was a SERIOUS issue. I only have two thousand bytes of code, and every point of that gator was a byte, so it was a memory hog. I helped it dramatically by using repeating segments wherever possible, and some creative math to help out the best I could (i.e., the spines on the back) Here's what it looks like, and the code below it...

<div class="text-center img-border">

![](https://swharden.com/static/2010/05/22/aj4vd_gator.png)

</div>

```c
#include <avr/io.h>
#include <util/delay.h>

// front top LED - PA0
// inside top LED - PA1
// inside bot LED - PA2
// front bot LED - PA3

unsigned long int t_unit; // units of time
const int tDit = 100;     //units for a dit
const int tDah = 255;     //units for a dah
char fsk;                 // degree of frequency shift to use for CW
char fsk2;                // degree of frequency shift to use for HELL

char light = 0; // which lights are on/off

void delay()
{
    _delay_loop_2(t_unit);
}

void blink()
{
    return;
    if (light == 0)
    {
        PORTA |= (1 << PA0);  //on
        PORTA |= (1 << PA1);  //on
        PORTA &= ~(1 << PA2); //off
        PORTA &= ~(1 << PA3); //off
        light = 1;
    }
    else
    {
        PORTA |= (1 << PA2);  //on
        PORTA |= (1 << PA3);  //on
        PORTA &= ~(1 << PA0); //off
        PORTA &= ~(1 << PA1); //off
        light = 0;
    }
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
    char mult = 3;

    char f2[] = {2, 3, 4, 5, 6, 7, 4, 3, 7, 4, 7, 7, 6, 5, 4, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 4, 5, 6, 7, 8, 4, 9, 5, 9, 6, 9, 6, 9, 6, 9, 8, 8, 7, 7, 6, 5, 4, 3, 3, 3, 4, 5, 5};

    for (int i = 0; i < sizeof(f2); i++)
    {
        OCR1A = f2[i] * mult;
        blink();
        tick(20);
        OCR1A = 1 * mult;
        blink();
        tick(20);
    }

    char f3[] = {1, 2, 3, 4, 3, 2};

    char offset = 0;
    while (offset < 9)
    {
        for (char j = 0; j < 3; j++)
        {
            for (char i = 0; i < sizeof(f3); i++)
            {
                char val = (f3[i] + 5 - offset) * mult;
                if (val < mult || val > 10 * mult)
                {
                    val = mult;
                }
                OCR1A = val;
                blink();
                tick(20);
                OCR1A = 1 * mult;
                blink();
                tick(20);
            }
        }
        offset++;
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
            OCR1A = 0;
            tick(tDah);
        }
        if (f[i] == 1)
        {
            OCR1A = fsk;
            tick(tDit);
        }
        if (f[i] == 2)
        {
            OCR1A = fsk;
            tick(tDah);
        }
        blink();
        OCR1A = 0;
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
    blink();
    pwm_init();
    t_unit = 1000;
    fsk = 10;
    id(); // set to fast and ID once
          //fsk=50;//t_unit = 65536; // set to slow for QRSS
    t_unit = 60000;

    while (1)
    {
        ;
        fish();
        id();
    }

    return 1;
}
```

