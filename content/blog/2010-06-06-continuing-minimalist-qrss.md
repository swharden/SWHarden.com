---
title: QRSS DNA
date: 2010-06-06 19:15:58
tags: ["microcontroller", "circuit", "qrss", "old"]
---

# QRSS DNA

__I'm still working on this project,__ and although progress is slow I'm learning a lot and the circuit is getting better with time. I'm still not yet ready to post the schematics, but you can get an idea of what's going on from the picture. It can handle 255 levels of frequency shift and has the ability to turn the tone on and off. 6 capacitors, 3 resistors, 4 transistors, a single inductor, and a micro-controller.

<div class="text-center img-border">

![](https://swharden.com/static/2010/06/06/DSCN0776.jpg)
![](https://swharden.com/static/2010/06/06/OnOffDNA.png)
![](https://swharden.com/static/2010/06/06/dnareport.jpg)

</div>

__UPDATE__ I spotted myself on [W4BHK's Grabber](http://www.qsl.net/w4hbk/W4HBKgrabber.html) about 300 miles away...

```c
#include <avr /io.h>
#include <util /delay.h>

char dotlen = 5;                              // ultimately the speeed of transmission
char call[] = {0, 1, 1, 1, 2, 0, 2, 1, 1, 0}; // 0 for space, 1 for dit, 2 for dah

void setfor(char freq, char ticks)
{
    OCR1A = freq;
    while (ticks > 0)
    {
        sleep();
        ticks--;
    }
}

void sleep()
{
    for (char i = 0; i < dotlen; i++)
    {
        _delay_loop_2(65000);
    }
}

void slideto(char freq, char ticks)
{
    freq = freq + 30;
    char step = 1;
    if (OCR1A > freq)
    {
        step = -1;
    }
    while (OCR1A != freq)
    {
        OCR1A += step;
        setfor(OCR1A, 1);
    }
    setfor(freq, ticks);
}

void DNA()
{
    char a[] = {4, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 5, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3};
    char b[] = {1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 5, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0};
    for (char i = 0; i < sizeof(a); i++)
    {
        //slideto(a[i]*4,2);
        //slideto(b[i]*4,2);
        setfor(a[i] * 2 + 5, 10);
        setfor(b[i] * 2 + 5, 10);
    }
}

void ID()
{
    for (char i = 0; i < sizeof(call); i++)
    {
        setfor(10, 50);
        if (call[i] == 0)
        {
            setfor(10, 100);
        }
        if (call[i] == 1)
        {
            setfor(15, 100);
        }
        if (call[i] == 2)
        {
            setfor(15, 250);
        }
        setfor(10, 50);
    }
}

void ID2()
{
    for (char i = 0; i < sizeof(call); i++)
    {
        if (call[i] == 0)
        {
            ampOFF();
            setfor(10, 50);
        }
        if (call[i] == 1)
        {
            ampON();
            setfor(10, 100);
        }
        if (call[i] == 2)
        {
            ampON();
            setfor(13, 100);
        }
        ampOFF();
        setfor(OCR1A, 30);
    }
    ampON();
}

void ampON()
{
    PORTA |= (1 << PA7);
    PORTA |= (1 << PA0);
    PORTA &= ~(1 << PA1);
    _delay_loop_2(10000);
}
void ampOFF()
{
    PORTA &= ~(1 << PA7);
    PORTA |= (1 << PA1);
    PORTA &= ~(1 << PA0);
    _delay_loop_2(10000);
}

int main(void)
{
    DDRA = 255;
    OCR1A = 75;
    TCCR1A = 0x81;
    TCCR1B = 1;
    while (1)
    {
        ID2();
        ID();
        for (char i = 0; i < 3; i++)
        {
            DNA();
        }
    }
}
```

