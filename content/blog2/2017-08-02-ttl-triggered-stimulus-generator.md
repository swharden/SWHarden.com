---
title: TTL Triggered Stimulus Generator
date: 2017-08-02 21:08:00
tags: ["circuit", "microcontroller"]
---

# TTL Triggered Stimulus Generator

__I was presented with a need to rapidly develop a pulse generator to take a TTL input and output a programmable output (for now 0.1 ms pulses at 20 Hz for as long as the input is high).__ I achieved this with a one-afternoon turnaround and the result looks great! This post documents the design and fabrication of this prototype device, with emphasis placed on design considerations and construction technique. 

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10017.jpg)

</div>

**By stocking large quantities of frequently-used items, inventors can build beautiful and functional prototypes for new ideas at the drop of a hat.** While it's easy to inexpensively accumulate tens of thousands of passive components (resistors, capacitors, etc.), it's the slightly more expensive components that people tend to order only when they need it for a project. However, paying high shipping rates or waiting months for items to arrive from overseas dramatically increases the barrier for initiating new projects. In my own workshop I have noticed that stocking large volumes of slightly more costly items (inductors, microcontrollers, connectors, enclosures, LED bezels, etc.) lowers the barrier for me to start new projects, and has proved to be a good investment! Now I can build a product _on the same day that I have the idea_! Today's idea takes the form of a TTL-controlled pulse generator for physiology applications.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10000.jpg)
![](https://swharden.com/static/2017/08/02/pics-10001.jpg)

</div>

__I designed the enclosure before I designed the circuit.__ Metal enclosures are always expensive compared to their plastic counterparts. Steel enclosures are difficult to drill, and aluminum enclosures are expensive. My most cringe-worthy stocking expenditure is ordering metal enclosures in quantities of 10+. The last I checked this specific one is listed as, "Aluminum Instrument Box Enclosure Case+Screw For Project Electronic 26X71X110MM" and is a little under $4 each. Brass hex stand-off nuts and black steel screws don't exactly match the aluminum, but they're what I had on hand. I knew I would need power and a BNC input and output, so I put those 3 on the back. I wasn't sure about the exact functionality of this device (and it may change after it is initially implemented) but I thought a single button and two LEDs would be a good starting point.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/schem.jpg)

</div>

__The circuit demonstrates the general flow of this device: a microcontroller-controlled project with a buffered output.__ I drew this schematic _after_ I finished the build (I kept adding passives here and there as I tested it out) but before I started I knew the gist of how I would organize the project. Mentally I knew that as long as my microcontroller ([ATTiny2313](http://www.atmel.com/Images/Atmel-2543-AVR-ATtiny2313_Datasheet.pdf)) could sense the TTL input and had control over _all _outputs (LEDs and BNC alike), I had a lot of flexibility to control the operation of this device in software. I used a generic [LM7805](http://ee-classes.usc.edu/ee459/library/datasheets/LM7805.pdf) linear voltage regulator with a few decoupling capacitors to take a who-knows-what input voltage (up to 40V) and turn it into a stable 5V output. Note that both inputs (the BNC TTL input and the push-button) have [decoupling capacitors](https://en.wikipedia.org/wiki/Decoupling_capacitor) near the microcontroller input pin to aid in [debouncing](http://www.labbookpages.co.uk/electronics/debounce.html).

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10004.jpg)
![](https://swharden.com/static/2017/08/02/pics-10003.jpg)

</div>

__I'm leaning on a [74HC541 inverting line driver](http://www.ti.com/lit/ds/symlink/cd74hct540.pdf) to clamp the output voltage firmly at TTL levels.__ The microcontroller (an [ATTiny2313](http://www.atmel.com/Images/Atmel-2543-AVR-ATtiny2313_Datasheet.pdf)) isn't really designed to source of sink much current (I think it's rated to 20 mA max) and I don't know about the input circuitry of the stimulus isolator I intend to control (and [don't forget about the impedance of 50-ohm cable](http://www.electronics-tutorials.ws/inductor/ac-inductors.html)). The line driver helps me take some of the pressure off the microcontroller and help me feel better about reliably driving the output BNC.

__Should I have optically isolated the input?__ Well, probably not... the application at hand is low importance. If I wanted to rely on optical isolation I would probably lean on the [H11B1](https://www.vishay.com/docs/83609/h11b1.pdf) as previously used in my [opto-isolated laser build](https://www.swharden.com/wp/2016-07-28-opto-isolated-laser-controller-build/). In retrospect I kind of wish I had just because it would have been cooler!

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10008.jpg)
![](https://swharden.com/static/2017/08/02/pics-10007.jpg)

</div>

__I added a header to allow me to program the microcontroller with a programmer [configured with test clip grabbers](https://www.ebay.com/sch/i.html?_nkw=test+clip+grabber).__ I have an AVR ISP MKII (clone), and building a programming adapter that uses test clips was one of the best decisions I ever made! It makes programming (and the inevitable re-programming) a breeze.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10010.jpg)
![](https://swharden.com/static/2017/08/02/pics-10009.jpg)

</div>

__The program isn't too complex.__ It uses a polling method to continuously check for the state of the input TTL. When it's high, it starts a new cycle (0.1 ms pulse, 49.9ms delay, yielding 20 Hz). The code is ready to add a "mode select" feature (which uses the front-panel push-button to select different stimulation protocols), but that functionality is not included in the example below. Note that a lot of the millisecond and microsecond delays are empirically determined by picking a value and checking its output on the oscilloscope. I should note that absolute timing isn't critical for my application, as long as it's consistent. For this reason I'm not relying on the internal RC clock (which is temperature sensitive), but instead am using an external 20MHz crystal as a time source. It's still temperature sensitive (and so are the loading capacitors on each side of it), but dramatically less so than the RC option. Note that the crystal wasn't in the original photos, but it was added for later photos.

__Configure the ATTiny2313 to use an external crystal clock source__

```bash
@echo off
avrdude -c usbtiny -p t2313 -U lfuse:w:0xff:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m
pause
```

### The core program: main.c

```c
#define F_CPU 20000000UL
#include <avr/io.h>
#include <util/delay.h>

volatile char state=0;

void output_HIGH(){PORTB|=(1<<PB4);}
void output_LOW(){PORTB&=~(1<<PB4);}
void LED1_ON(){PORTB|=(1<<PB3);}
void LED1_OFF(){PORTB&=~(1<<PB3);}
void LED2_ON(){PORTB|=(1<<PB2);}
void LED2_OFF(){PORTB&=~(1<<PB2);}

void singlePulse_20Hz_100us(){
    output_HIGH();
    _delay_us(100);
    output_LOW();
    _delay_us(900);
    LED2_ON();
    _delay_ms(20);
    LED2_OFF();
    _delay_ms(28);
    _delay_us(920);
}

void poll(){
    if ((PIND&(1<<PD4))){singlePulse_20Hz_100us();}
}

int main(void){
    DDRB=255; // all outputs
    DDRD=0; // all inputs
    PORTD=(1<<PD5); // pull front button high
    LED1_ON();
    for(;;){
        poll();
    }
}
```

### Compile and load the ATTiny2313

```bash
@echo off
del *.elf
del *.hex
avr-gcc -mmcu=attiny2313 -Wall -Os -o main.elf main.c -w
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
pause
avrdude -c usbtiny -p t2313 -U flash:w:"main.hex":a
```

__I didn't think to check my height profile!__ I got lucky, and things fit fine. Socketed ICs can be close calls, and so can vertically-installed electrolytic capacitors. Now that it was programmed and everything fit, it was time to seal it up and make labels.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10014.jpg)
![](https://swharden.com/static/2017/08/02/pics-10015.jpg)

</div>

__The finished product looks great!__ Never underestimate the power of [clear labels and square outlines](http://www.qsl.net/pa2ohh/tlabels.htm). Following deployment, a couple screws will let me open it up and access the programming header in case I need to change the stimulation protocols stored in the microchip. I am pleased with how professional of a result I was able to achieve in one sitting! I look forward to seeing how this device works for my application.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/02/pics-10017.jpg)
![](https://swharden.com/static/2017/08/02/pics-10018.jpg)

</div>

PS: Microcontroller code for this project (and many others) is stored in my ever-growing AVR-Projects GitHub page: [_https://github.com/swharden/AVR-projects_](https://github.com/swharden/AVR-projects)

PPS: I smiled when a Google search revealed the [PulsePal](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4263096/pdf/fneng-07-00043.pdf), "A low-cost programmable pulse generator for physiology and behavior".