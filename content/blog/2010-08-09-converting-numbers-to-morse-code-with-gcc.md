---
title: Converting Numbers to Morse Code with GCC
date: 2010-08-09 07:55:47
tags: ["python", "qrss", "old"]
---

# Converting Numbers to Morse Code with GCC

__One of my microcontroller projects__ requires me to measure values and transmit then in Morse code. There may be code out there to do this already, but I couldn't find it. I'm sure there are more elegant and efficient ways to handle the conversion, but this works for me. Hopefully someone will find it useful!

<div class="text-center img-border">

[![](https://swharden.com/static/2010/08/09/binary_to_Morse_thumb.jpg)](https://swharden.com/static/2010/08/09/binary_to_Morse.png)

</div>

```c
#include <stdio.h>

//Morse code numbers from 0 to 9
char *array[10] = {"-----", ".----", "..---", "...--", "....-",
                   ".....", "-....", "--...", "---..", "----."};

void beep(char v)
{
    // beep (or print) Morse code as necessary
    printf("%s ", array[v]);
}

void send(int l)
{
    // convert a number into Morse code
    char d = 0;
    int t = 0;
    int val = 0;
    for (t = 100000; t > 0; t = t / 10)
    { //number of digits here
        if (l > t)
        {
            d = l / t;
            beep(d);
            l -= d * t;
        }
        else
        {
            beep(0);
        }
    }
    printf("n");
}

void main()
{
    // program starts here
    int l = 0b1111111111; //sample number (maximum 10-bit)
    printf("%d ", l);
    send(l);
    l = 0b11010001100101100011; //larger sample number
    printf("%d ", l);
    send(l);
}
```

