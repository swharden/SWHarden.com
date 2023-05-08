---
title: $10 Frequency Counter Finished!
date: 2011-03-14 10:29:21
tags: ["amateur radio", "circuit", "microcontroller", "obsolete"]
---

# $10 Frequency Counter Finished!

__Wow, what a cool project start to finish.__ Simple, cheap, and absolutely useful! ... and not to mention big green numbers which make it look more impressive than it actually is! This is my super-simple frequency counter designed to be used for amateur radio, all for about $10.  It was a project I developed over the last few months and documented all along the way. It's finished I guess, so this will probably be the last post about it! Now for some vids and pics:

{{<youtube KduEGjvXaeY>}}

__Sure there's room for improvement,__but that's the fun part! This is a solid start and it's cheap as can be. Simply improving software would greatly improve its accuracy. This doesn't use any time-averaging at all! If you had it average 20 readings, it'd probably be much smoother, update every second, and have a higher precision. Also, there's ample room left in the case to build in a transmitter or receiver!

<dev class="center border">

![](https://swharden.com/static/2011/03/14/IMG_5452.jpg)

</dev>

__There's the finished project!__ It looks pretty good, considering it was built mostly out of junk box components, and everything it's made from can be purchased cheaply online. I'm happy with it! I could improve my metal cutting, but that was the first time I ever cut a square window in aluminum so I'm still proud of myself.

<dev class="center border">

![](https://swharden.com/static/2011/03/14/IMG_5429.jpg)

</dev>

__As you can see the enclosure is made from sheet metal__ bent and cut into 2 pieces. The enclosure was from RadioShack, and was $2.99! Yeah it might be cheaper online, but when you add shipping it's pretty convenient to get it locally. My local RadioShack didn't carry these metal ones (they have stupid plastic ones), but I found these in Orlando and after asking the workers I learned that anyone can find any product online (such as [the case I used](http://www.radioshack.com/product/index.jsp?productId=2062217)) and request that their local store order them. When they arrive, you can buy them with no extra charge!

<dev class="center border">

![](https://swharden.com/static/2011/03/14/IMG_5425.jpg)

</dev>

__Here are some of the internals after being mounted.__ Heck, these are ALL the internals! You can tell I could have gotten away with a case one third this size if I had one available. Oh well, it's still cool.

<dev class="center border">

![](https://swharden.com/static/2011/03/14/IMG_5209.jpg)
![](https://swharden.com/static/2011/03/14/IMG_5222.jpg)
![](https://swharden.com/static/2011/03/14/IMG_5221.jpg)

</dev>

__There are a few random photos of the build.__ It's just a microcontroller reading (and resetting) a counter a bunch of times a second and displaying the result on the multiplexed display. That's it! It was a lot of work, but a truly simple concept. The micro-controller is an ATMEL Atmega 16 AVR which is a little costly (around $5) but I had it on hand. I imagine you could accomplish the same thing with a far less intricate microcontroller! I'll bet you could pull it off with an ATTiny2313, especially if you had a LCD display rather than a multiplexed LED like mine. The counter is a 74lv8154 chip, a 32-bit (dual 16-bit) counter IC at a bargain $0.50 - why when I google for home made frequency counters do I not see people using these? They daisy-chain multiple 8-bit counters! What a shortcut I stumbled upon...

__Thinking of making your own?__ Go for it! Here are some of my other posts which describe the development of this thing (including stuff I tried that didn't work). Everything I ordered should be stocked at mouser.com.

* [this post demonstrates it in action](http://www.swharden.com/blog/2011-02-12-wideband-receiver-works/)

* [this post shows it being used too](http://www.swharden.com/blog/2011-02-09-minimal-radio-project-continues/)

* [this post shows the first time I really got it working](http://www.swharden.com/blog/2011-02-04-frequency-counter-working/)

* [this post has the SCHEMATIC for the counter!](http://www.swharden.com/blog/2011-01-28-home-brew-transceiver-taking-shape/)

__I guess that sums it up!__ What a fun hack. If you have any questions feel free to contact me (link in the menu on the right), and if you make one of these of your own I'd LOVE to see it! I'll even slap a photo of yours on my site to share with everyone. I had fun working on this project. If you're at all into radio, I recommend you try attacking a project like this too! It's more efficient at determining frequency than turning on a commercial radio receiver and spinning the dial until you hear your transmitter ^_^

## SUPPLEMENTAL VIDEO

{{<youtube B0pj717UJPo>}}

__Upon request here's the code!__ It's nothing special, and certainly not very efficient, but it's quite functional. If you re-create this project, I recommend writing your own code rather than flat copying mine. You'll learn a heck of a lot more... and my code for this is really crap XD

```c
#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

#define A PC5
#define B PC0
#define C PC6
#define D PC7
#define E PC2
#define F PC4
#define G PC1
#define P PC3

char sendDigit(char row, char num, char dot){
    char val=0;
    if (num==0) {val|=(1<<A)|(1<<B)|(1<<C)|(1<<D)|(1<<E)|(1<<F);}
    if (num==1) {val|=(1<<B)|(1<<C);}
    if (num==2) {val|=(1<<A)|(1<<B)|(1<<D)|(1<<E)|(1<<G);}
    if (num==3) {val|=(1<<A)|(1<<B)|(1<<C)|(1<<D)|(1<<G);}
    if (num==4) {val|=(1<<B)|(1<<C)|(1<<F)|(1<<G);}
    if (num==5) {val|=(1<<A)|(1<<C)|(1<<D)|(1<<F)|(1<<G);}
    if (num==6) {val|=(1<<A)|(1<<C)|(1<<D)|(1<<E)|(1<<F)|(1<<G);}
    if (num==7) {val|=(1<<A)|(1<<B)|(1<<C);}
    if (num==8) {val|=(1<<A)|(1<<B)|(1<<C)|(1<<D)|(1<<E)|(1<<F)|(1<<G);}
    if (num==9) {val|=(1<<A)|(1<<B)|(1<<C)|(1<<F)|(1<<G);}
    if (dot==1) {val|=(1<<P);}
    PORTC=val;
    PORTD=(0b10000000>>row);
    _delay_ms(1);
}

void showNumber(unsigned long val){
    if (val==0) {return;}
    int i;
    int array[6]={10,0,0,0,0,0}; // NUMBER OF DIGITS
    int dly=10;
    i=6-1;
    while (val>0){
      array[i--]=val%10;
      val /= 10;
    }
    sendDigit(1,array[0],0);
    sendDigit(2,array[1],1);
    sendDigit(3,array[2],0);
    sendDigit(4,array[3],0);
    sendDigit(5,array[4],0);
    sendDigit(6,array[5],0);
    sendDigit(0,0,0);
}

#define byte1 PB4
#define byte2 PB3
#define byte3 PB2
#define byte4 PB1

unsigned long val=123456;
void readFreq(){
    unsigned long b4,b3,b2,b1;
    PORTB=255-(1<<byte1);b1=PINA;
    PORTB=255-(1<<byte2);b2=PINA;
    PORTB=255-(1<<byte3);b3=PINA;
    PORTB=255-(1<<byte4);b4=PINA;
    PORTB=0;PORTB=255;//RESET
    val=b1+b2*256+b3*65536+b4*16777216;
    val=val/3355;
}

int cnt=0;
ISR(TIMER1_OVF_vect)
{
   cnt++;
   readFreq();
}

int main(){
    DDRA=0;
    DDRB=255;
    DDRC=255;
    DDRD=255;

    TIMSK|= (1 << TOIE1); // Enable overflow interrupt
    sei(); // Enable global interrupts
       TCCR1B|=(1<<CS11); // Set up timer at Fcpu/8

    while(1){showNumber(val);}
}
```

__... and I know it's unrelated, but:__

{{<youtube _0NIDVJWo0U>}}

(I watched this four times - it's so random I love it!)

## Update

This project was featured on a couple of my favorite sites, [Hack-A-Day](http://hackaday.com/2011/03/14/frequency-counter-for-10-worth-of-parts/) and [Electronics-Lab](http://www.electronics-lab.com/blog/?p=10093)!

<dev class="center border">

![](https://swharden.com/static/2011/03/14/counter_EL.jpg)
![](https://swharden.com/static/2011/03/14/counter_HAD.jpg)

</dev>