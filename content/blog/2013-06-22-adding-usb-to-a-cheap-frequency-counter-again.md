---
title: Adding USB to a Cheap Frequency Counter (Again)
date: 2013-06-22 20:07:22
tags: ["circuit"]
---

# Adding USB to a Cheap Frequency Counter (Again)

__Today I rigineered my frequency counter to output frequency to a computer via a USB interface.__ You might remember that[ I did this exact same thing two years ago](http://www.swharden.com/blog/2011-07-11-aj4vd-arsenal-recently-expanded/), but unfortunately I fell victim to accidental closed source. When I rigged it the first time, I stupidly tried to get fancy and add USB interface with [V-USB](http://www.obdev.at/products/vusb/index.html) requiring special drivers and special software code to retrieve the data. The advantage was that the microcontroller spoke directly to the PC USB port via 2 pins requiring no extra hardware. The stinky part is that I've since lost the software I wrote necessary to decode the data. Reading my old post, I see I wrote_ "Although it’s hard for me, I really don’t think I can release this \[microchip code\] right now. I’m working on an idiot’s guide to USB connectivity with ATMEL microcontrollers, and it would cause quite a stir to post that code too early."_  Obviously I never got around to finishing it, and I've since lost the code. Crap! I have this fancy USB "enabled" frequency counter, but no ability to use it. NOTE TO SELF: NEVER POST PROJECTS ONLINE WITHOUT INCLUDING THE CODE! I guess I have to crack this open again and see if I can reprogram it...

<div class="text-center img-border">

[![](IMG_0285_thumb.jpg)](IMG_0285.jpg)

</div>

__My original intention was just to reprogram the IC and add serial USART support, then use a little FTDI adapter module to serve as a USB serial port.__ That will be supported by every OS on the planet out of the box.  Upon closer inspection, I realized I previously used an ATMega48 which has trouble being programmed by AVRDUDE, so I whipped up a new perf-board based around an ATMega8. I copied the wires exactly (which was stupid, because I didn't have it written down which did what, and they were in random order), and started attacking the problem in software.

<div class="text-center img-border">

[![](IMG_0283_thumb.jpg)](IMG_0283.jpg)

</div>

__The way the microcontroller reads frequency is via the display itself.__ There are multiplexed digits, so some close watching should reveal the frequency. I noticed that there were fewer connections to the microcontroller than expected - a total of 12. How could that be possible? 8 seven-segment displays should be at least 7+8=15 wires. What the heck? I had to take apart the display to remind myself how it worked. It used a pair of[ ULN2006A darlington transistor arrays](http://www.ti.com/lit/ds/symlink/uln2003a.pdf) to do the multiplexing (as expected), but I also noticed it was using a [CD4511BE BCD-to-7-segment driver to drive the digits](http://www.play.com.br/datasheet/CD4511.pdf). I guess that makes sense. That way 4 wires can drive 7 segments. 8+4=12 wires, which matches up. Now I feel stupid for not realizing it in the first place. Time to screw things back together.

<div class="text-center img-border">

[![](IMG_0288_thumb.jpg)](IMG_0288.jpg)

</div>

__Here's the board I made. 3 wires go to the FTDI USB module (GND, VCC 5V drawn from USB, and RX data), black wires go to the display, and the headers are to aid programming.__ I added an 11.0592MHz crystal to [allow maximum serial transfer speed](http://www.wormfood.net/avrbaudcalc.php) (230,400 baud), but stupidly forgot to enable it in code. It's all boxed up now, running at 8MHz and 38,400 baud with the internal RC clock. Oh well, no loss I guess.

<div class="text-center img-border">

[![](IMG_0291_thumb.jpg)](IMG_0291.jpg)
[![](IMG_0293_thumb.jpg)](IMG_0293.jpg)

</div>

__I wasted literally all day on this.__ It was so stupid. The whole time I was kicking myself for not posting the code online. I couldn't figure out which wires were for the digit selection, and which were for the BCD control. I had to tease it apart by putting random numbers on the screen (by sticking my finger in the frequency input hole) and looking at the data flowing out on the oscilloscope to figure out what was what. I wish I still had my [DIY logic analyzer](http://www.swharden.com/blog/2011-07-16-half-hearted-diy-logic-analyzer-works-a-little/). I guess this project was what I built it for in the first place! A few hours of frustrating brute force programming and adult beverages later, I had all the lines figured out and was sending data to the computer.

<div class="text-center img-border">

[![](IMG_0289_thumb.jpg)](IMG_0289.jpg)
[![](IMG_0287_thumb.jpg)](IMG_0287.jpg)
[![](IMG_0290_thumb.jpg)](IMG_0290.jpg)
[![](IMG_0288_thumb.jpg)](IMG_0288.jpg)

</div>

__With everything back together,__ I put the frequency counter back in my workstation and I'm ready to begin my frequency measurement experiments. Now it's 9PM and I don't have the energy to start a whole line of experiments. Gotta save it for another day. At least I got the counter working again!

<div class="text-center img-border">

[![](IMG_0296_thumb.jpg)](IMG_0296.jpg)

</div>

__Here's the code that goes on the microcontroller __(it sends the value on the screen as well as a crude checksum, which is just the sum of all the digits)

```c
#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define USART_BAUDRATE 38400
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

void USART_Init(void){
    UBRRL = BAUD_PRESCALE;
    UBRRH = (BAUD_PRESCALE >> 8);
    UCSRB = (1<<TXEN);
    UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0); // 9N1
}

void USART_Transmit( unsigned char data ){
    while ( !( UCSRA & (1<<UDRE)) );
    UDR = data;
}

void sendNum(int byte){
    if (byte==0){
        USART_Transmit(48);
    }
    while (byte){
        USART_Transmit(byte%10+48);
        byte-=byte%10;
        byte/=10;
    }
}

void sendBin(int byte){
    char i;
    for (i=0;i<8;i++){
        USART_Transmit(48+((byte>>i)&1));
    }
}

volatile char digits[]={0,0,0,0,0,0,0,0};
volatile char freq=123;

char getDigit(){
    char digit=0;
    if (PINC&0b00000100) {digit+=1;}
    if (PINC&0b00001000) {digit+=8;}
    if (PINC&0b00010000) {digit+=4;}
    if (PINC&0b00100000) {digit+=2;}
    if (digit==15) {digit=0;} // blank
    return digit;
}

void updateNumbers(){
    while ((PINB&0b00000001)==0){} digits[7]=getDigit();
    while ((PINB&0b00001000)==0){} digits[6]=getDigit();
    while ((PINB&0b00010000)==0){} digits[5]=getDigit();
    while ((PINB&0b00000010)==0){} digits[4]=getDigit();
    while ((PINB&0b00000100)==0){} digits[3]=getDigit();
    while ((PINB&0b00100000)==0){} digits[2]=getDigit();
    while ((PINC&0b00000001)==0){} digits[1]=getDigit();
    while ((PINC&0b00000010)==0){} digits[0]=getDigit();
}

int main(void){
    USART_Init();
    char checksum;
    char i=0;
    char digit=0;

    for(;;){
        updateNumbers();
        checksum=0;
        for (i=0;i<8;i++){
            checksum+=digits[i];
            sendNum(digits[i]);
        }
        USART_Transmit(',');
        sendNum(checksum);
        USART_Transmit('n');
        _delay_ms(100);
    }
}
```

__Here's the Python code to listen to the serial port, though you could use any program __(note that the checksum is just shown and not verified):

```python
import serial, time
import numpy
ser = serial.Serial("COM15", 38400, timeout=100)

line=ser.readline()[:-1]
t1=time.time()
lines=0

data=[]

def adc2R(adc):
    Vo=adc*5.0/1024.0
    Vi=5.0
    R2=10000.0
    R1=R2*(Vi-Vo)/Vo
    return R1

while True:
    line=ser.readline()[:-1]
    print line
```

__This is super preliminary,__ but I've gone ahead and tested heating/cooling an oscillator (a microcontroller clocked with an external crystal and outputting its signal with CKOUT). By measuring temperature and frequency at the same time, I can start to plot their relationship...

<div class="text-center img-border">

[![](photo-1-1_thumb.jpg)](photo-1-1.jpg)

</div>

<div class="text-center">

[![](tf_thumb.jpg)](tf.png)

</div>