---
title: Festivus Pole Video Game
date: 2015-12-23 18:24:11
tags: ["obsolete"]
---



__December 23 is Festivus! To commemorate the occasion, I have built a traditional Festivus pole with a couple added features.__ To my knowledge, this is the first _electronic_ Festivus pole on the internet. <a href="https://swharden.com/blog/images/2015/12/full.gif" rel="attachment wp-att-3921">

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/full.gif)

</div>

**[Festivus](https://en.wikipedia.org/wiki/Festivus) is a holiday comically celebrated as an alternative to the pressures of commercialism commonly associated with other winter holidays.** Originating from the 1997 Seinfeld episode "The Strike", the traditions of Festivus include demonstrating feats of strength, declaring common occurrences as Festivus miracles, airing of grievances, and of course the fabrication of a _Festivus pole_. 

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/strike.jpg)

</div>

**Over the years** various Festivus poles (often made of beer cans) have been erected in government buildings alongside the nativity scene and menorah, [including this year in my home state Florida](http://www.fox35orlando.com/home/60908334-story) (the video is a good laugh). Here, I show a Festivus pole I made made from individually illuminated diet coke cans which performs as a simple video game, controlled by a single button. The illuminated can scrolls up and down, and the goal is to push the button when the top can is lit. If successful, the speed increases, and the game continues! It's _hours_ of jolly good fun.

{{<youtube TviqZgyZNnk>}}

__After playing at my workbench for a while, I figured out a way I could light-up individual coke cans.__ I drilled a dozen holes in each can (with a big one in the back), stuck 3 blue LEDs (wired in parallel with a 220-ohm current limiting resistor in series) in the can, and hooked it up to 12V. This was the motivation I needed to continue...

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/a.jpg)
![](https://swharden.com/static/2015/12/23/b.jpg)
![](https://swharden.com/static/2015/12/23/c.jpg)
![](https://swharden.com/static/2015/12/23/d.jpg)
![](https://swharden.com/static/2015/12/23/e.jpg)
![](https://swharden.com/static/2015/12/23/f.jpg)

</div>

__Now for the design.__ I found a junk box 12V DC wall-wart power supply which I decided to commandeer for this project. Obviously a microcontroller would be the simplest way to implement this "game", and I chose to keep things as minimal as possible. I used a single 8-pin [ATMEL ATTiny85 microcontroller](http://www.mouser.com/ProductDetail/Atmel/ATtiny85-20PU/?qs=sGAEpiMZZMu9ReDVvI6ax7XpNAHo%252bKm8HQZQZgS5360%3d) ($1.67) which takes input from 1 push-button and sends data through two daisy-chained[ 74hc595 shift-registers](http://www.mouser.com/ProductDetail/Texas-Instruments/SN74HC595N/?qs=sGAEpiMZZMtsbn1GaJysl80qBaGZ8bjzTAKqk4DYcpY%3d) ($0.57) to control base current of [2n3904 transistors](http://www.mouser.com/search/ProductDetail.aspx?R=0virtualkey0virtualkey2N3904BU) ($.019) to illuminate LEDs which I had on hand (ebay, 1000 3mm blue LEDs, $7.50 free shipping). A [LM7805 linear voltage regulator](http://www.mouser.com/ProductDetail/Fairchild-Semiconductor/LM7805CT/?qs=sGAEpiMZZMtUqDgmOWBjgPJMQlYvsHAW%252bBbwCYnQla0%3d) ($0.68) was used to bring the 12V to 5V, palatable for the microcontroller. Note that all prices are for individual units, and that I often buy in bulk from cheap (shady) vendors, so actual cost of construction was less.

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/festivus-pole-video-game-schematic.png)

</div>

__To build the circuit,__ I used perf-board and all through-hole components. It's a little messy, but it gets the job done! Admire the creative resistor hops connecting shift registers and microcontroller pins. A purist would shriek at such construction, but I argue its acceptability is demonstrated in its functionality.

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/IMG_4350.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4352.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4362.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4364.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4366.jpg)

</div>

__The installation had to be classy.__ To stabilize the fixture, I used epoxy resin to cement a single coke can to an upside-down Pyrex dish (previously used for [etching circuit boards in ferric chloride](http://hackaday.com/2008/07/28/how-to-etch-a-single-sided-pcb/)). I then used clear packaging tape to hold each successive illuminated can in place. All wires were kept on the back side of the installment with electrical tape. Once complete, the circuit board was placed beneath the Pyrex container, and the controller (a single button in a plastic enclosure connected with a telephone cord) was placed beside it.

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/IMG_4402.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4403.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4404.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4406.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4396.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4375.jpg)

</div>

__It's ready to play!__ Sit back, relax, and challenge your friends to see who can be the Festivus pole video game master!

<div class="text-center img-border">

![](https://swharden.com/static/2015/12/23/IMG_4401.jpg)
![](https://swharden.com/static/2015/12/23/IMG_4408.jpg)

</div>

__A few notes about the code...__ The microcontroller ran the following C code ([AVR-GCC](http://www.nongnu.org/avr-libc/)) and is extremely simple. I manually clocked the [shift registers](https://en.wikipedia.org/wiki/Shift_register) (without using the chip's serial settings) and also manually polled for the button press (didn't even use interrupts). It's about as minimal as it gets! What improvements could be made to this Festivus hacking tradition? We will have to wait and see what the Internet comes up with next year...

```c
#define F_CPU 1000000UL
#include <avr/io.h>
#include <avr/delay.h>

// PB2 data
// PB1 latch
// PB0 clock
// PB4 LED

// PB3 input button

volatile int speed=400;
volatile char canlit=0;
volatile char levelsWon=0;

char buttonPressed(){
    char state;
    state = (PINB>>PB3)&1;
    if (state==0) {
        PORTB|=(1<<PB4);
        return 1;
    }
    else {
        PORTB&=~(1<<PB4);
        return 0;
    }
}

void shiftBit(char newval){
    // set data value
    if (newval==0){PORTB&=~(1<<PB2);}
    else {PORTB|=(1<<PB2);}
    // flip clock
    PORTB|=(1<<PB0);
    PORTB&=~(1<<PB0);
}

void allOff(){
    char i=0;
    for(i=0;i<16;i++){
        shiftBit(0);
    }
    updateDisplay();
}

void allOn(){
    char i=0;
    for(i=0;i<14;i++){
        shiftBit(1);
    }
    updateDisplay();
}

void onlyOne(char pos){
    if (pos>=8) {pos++;}
    char i;
    allOff();
    shiftBit(1);
    for (i=0;i<pos;i++){shiftBit(0);}
    //if (pos>8) {shiftBit(0);} // because we skip a shift pin
    updateDisplay();
    }

void updateDisplay(){PORTB|=(1<<PB1);PORTB&=~(1<<PB1);}

void ledON(){PORTB|=(1<<PB4);}
void ledOFF(){PORTB&=~(1<<PB4);}

char giveChance(){
    int count=0;
    for(count=0;count<speed;count++){
        _delay_ms(1);
        if (buttonPressed()){return 1;}
    }
    return 0;
}

void strobe(){
    char i;
    for(i=0;i<50;i++){
        allOn();_delay_ms(50);
        allOff();_delay_ms(50);
    }
}

char game(){
    for(;;){
        for(canlit=1;canlit<15;canlit++){
            onlyOne(canlit);
            if (giveChance()) {return;}
        }
        for(canlit=13;canlit>1;canlit--){
            onlyOne(canlit);
            if (giveChance()) {return;}
        }
    }
}

void levelWin(){
    char i;
    for(i=0;i<levelsWon;i++){
        allOn();
        _delay_ms(200);
        allOff();
        _delay_ms(200);
    }
}
void levelLose(){
    char i;
    for(i=0;i<20;i++){
        for(canlit=13;canlit>1;canlit--){
            onlyOne(canlit);
            _delay_ms(10);
        }
    }
}

void showSelected(){
    char i;
    for(i=0;i<20;i++){
        onlyOne(canlit);
        _delay_ms(50);
        allOff();
        _delay_ms(50);
    }
}

void nextLevel(){
    // we just pushed the button.
    showSelected();
    levelsWon++;
    if (canlit==14) {
        levelWin();
        speed-=speed/5;
        }
    else {
        levelLose();
        speed=400;
        levelsWon=0;
    }
}

int main(void){
    DDRB=(1<<PB0)|(1<<PB1)|(1<<PB2)|(1<<PB4);
    char i;
    for(;;){
        game();
        nextLevel();
    }
}
```

__Programming:__ note that the code was compiled and programmed onto the AVR from a linux terminal using [AvrDude](http://www.nongnu.org/avrdude/). The shell script I used for that is here:

```bash
rm main
rm *.hex
rm *.o
echo "MAKING O"
avr-gcc -w -Os -DF_CPU=1000000UL -mmcu=attiny85 -c -o main.o main.c
echo "MAKING BINARY"
avr-gcc -w -mmcu=attiny85 main.o -o main
echo "COPYING"
avr-objcopy -O ihex -R .eeprom main main.hex
echo "PROGRAMMING"
avrdude -c usbtiny -p t85 -F -U flash:w:"main.hex":a -U lfuse:w:0x62:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m
echo "DONE"
```
