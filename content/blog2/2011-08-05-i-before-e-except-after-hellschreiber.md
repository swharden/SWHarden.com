---
title: I before E except after Hellschreiber
date: 2011-08-05 18:52:40
tags: ["microcontroller", "circuit", "obsolete", "amateur radio"]
---

# I before E except after Hellschreiber

**This post describes a project I designed which transmits strings of data from a microcontroller to a PC's screen using audio beeping in a special mode called [Hellschreiber](http://en.wikipedia.org/wiki/Hellschreiber).** Although these days it's almost exclusively used by amateur radio operators, I thought it would make a cool microcontroller project! The result can be accomplished with a microcontroller and a speaker as a transmitter and a PC with a microphone as a receiver and decoder, or with actual radio equipment (even toy walkie talkies) by transmitting the tones over modulated radio frequencies for long distance communication! [Ideas anyone?](http://www.amazon.com/Midland-GXT760VP4-36-Mile-42-Channel-Two-Way/dp/B0039YON6Q/ref=sr_1_1?ie=UTF8&qid=1312588647&sr=8-1)

___SPECIAL THANKS:__ I'd like to think [Mike Seese](http://www.mikeseese.com) for his brainstorming help in making this project a reality. [Mike](http://www.mikeseese.com) and I are working on a high altitude balloon project together, and a creative inexpensive radio link is one of our goals. Thanks [Mike](http://www.mikeseese.com)!_

__As a professional dental student by day and amateur electrical/RF engineer by night, I'm having a very strange summer.__ I'm developing rapidly in my experience and skills in both arenas. I finally feel like I have a working knowledge of most fundamental electrical and radio frequency concepts, and I'm starting to see patients and do procedures on humans (no more mannequins) in the student dental clinic. For legal and ethical reasons I do not write specifics about what I do with my patients, but I certainly make up for it by documenting the electronic projects I work on! My goals of doing this are to (a) inspire potential electronics tinkerers to come up with new ideas and attack new projects, and (b) receive feedback and insight from those more experienced than me to help me grow in my knowledge. My eye caught [a comment](http://www.swharden.com/blog/2011-07-24-frequency-counter-gen2/comment-page-1/#comment-16485) a few posts ago that made me smile: _You have been blessed with talent and the drive to attempt things not been tried before, keep it up, great job. --David S_  While I can't claim that everything I do is truly novel or never tried before, I appreciate the encouraging words. Thank you David S!

__Today's project is a fun one involving vintage wartime radio equipment, amateur radio computer software, and a healthy dose of microcontrollers!__ My goal is to design a single chip Hellschreiber (technically Feldhellschreiber) transmitter. "Hellschreiber" translates into English as "Light Writer" and is a pun on the name of its inventor, Rudolf Hell, who built the first device in 1920. It was intended to allow messages to be transferred over poor radio links too noisy for intelligible voice or [radioteletype (RTTY)](http://en.wikipedia.org/wiki/Radioteletype) communication. Its cool factor is upped by the fact that it was sometimes used by the German military in conjunction with the [Enigma encryption system](http://en.wikipedia.org/wiki/Enigma_machine) during World War 2! [As an aside, RTTY is still pretty sweet and dates back to the mid 1800s! Check out hardware receivers in [video 1](http://www.youtube.com/watch?v=mN8pkJoDDfI) and [video 2](http://www.youtube.com/watch?v=Ml00ngVwrcU)]

{{<youtube nXLPUbGYDp4>}}

__Seeing a battlefield-ready Hellschreiber receiver gives you a good idea of how it works.__ (The video isn't mine, I found it on youtube.) The concept is relatively simple (shown above), and the receiver has only 2 moving parts. A spinning corkscrew presses a ticker tape into ink when it receives a radio signal. As the radio signal beeps on and off, the corkscrew contacts at different positions at different times, and letters are written on the ticker tape! 

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/05/anaglyph-hell-GL-11.jpg)

</div>

The [designers of these things were extraordinarily creative](http://www.nonstopsystems.com/radio/hellschreiber-fonts.htm)! The picture on the right shows a Hellschreiber transmitter - basically a typewriter with mechanical wizardry that turns key presses into a series of radio tones corresponding to the pixelated shape of a character.

__Almost a century later, people are still sending messages around the world using Hellschreiber!__ With an [amateur radio license](http://en.wikipedia.org/wiki/Amateur_radio) and an amateur radio transceiver you can tune around special [Hellschreiber calling frequencies](http://www.nonstopsystems.com/radio/frank-radio-dig-mode-freqs.htm) and engage in conversations with other people who enjoy using this unique mode. Computers have modernized the process, allowing you to send Hellschreiber text by typing on your keyboard and receive it by just looking at your screen. My favorite program (free) to do this is Digital Master 780, part of [Ham Radio Deluxe](http://www.ham-radio-deluxe.com/Downloads.aspx).

{{<youtube _MJYwXvwTvY>}}

__This is the project I just completed.__ It takes strings of text stored (or dynamically generated) in an array on a microcontroller (I'm using an ATMega48, but the code is almost identical for any ATMEL AVR microcontroller, and easy adapted for other architectures) and turns it into an audio tone using PWM. This audio tone could be fed into a speaker and a microphone across the room could receive it and use the software to show the received data, or the audio could be fed into a radio transmitter and a PC hooked to the receiver could decode the audio.  Either way, the text in the microcontroller is converted to Hellschreiber audio tones ready to be used however you see fit!  Although I designed it as a resilient way to transmit GPS/altitude data from a high altitude balloon using a small, cheap, low-power radio transmitter, this project is just the foundation of a plethora of potential projects!

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/05/DSCN1663.jpg)

</div>

__Here's the circuit I'm using.__ It's actually less complicated than shown - all those yellow wires are going to my AVR programmer! The chip just receives +5V and GND, and the audio is generated automatically and output on the OC0A pin, which happens to be pin 12 on my ATMega48. The output (audio level square waves) is fed to a crystal oscillator [like this one](http://www.taydaelectronics.com/servlet/the-709/OSC-dsh-40M-dsh-MEC-dsh-LF-CRYSTAL-OSCILLATOR-40.00/Detail), which generates square waves with an amplitude equal that to the input. Thus, by audio-frequency AC from the microchip, decoupled through a series capacitor, added to the power supply of the oscillator (provided by the 5V rail through a 1.8k resistor), we effectively produce an amplitude modulated (AM) radio signal!

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/05/DSCN1667.jpg)

</div>

__This is the receiver I'm using.__ I'm lucky enough to have an all-mode, general-coverage, 100W amateur radio transceiver! It's a [Yaesu 857-D](http://www.eham.net/reviews/detail/3046) and I'm completely in love with it. It's quite pricey though! You can find wide coverage receive-only radios called [radio scanners](http://en.wikipedia.org/wiki/Scanner_(radio)) (or police scanners), often for $20 or so on eBay which would do just as good a job of receiving all sorts of radio signals! Whatever you use, after tuning into the audio with the ham radio delux software, you'll be able to decode Hellschreiber like this:

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/05/hell.png)

</div>

__A few notes about the code:__ Each letter is sent twice vertically and I don't think I should have done that. It's easy enough to correct by eliminating the second FOR loop in the sendChar() function, and doubling the height of the pixels transmitted by changing on(1) and off(1) to on(2) and off(2). Then again, I could be mistaken - I don't use this mode much.  Also, horizontal width of characters (increase this and horizontally compress the received image to reduce the effects of noise) is controlled by a single variable, dynamically adjustable in software. Characters are created from a 3x5 grid (15 bits) and stored as an integer (16 bits, 2 bytes in AVR-GCC). Custom characters are certainly possible! This program takes 16.1% of program space (658 bytes) and 25.4% of data space (130 bytes) and certainly leaves room for optimization.

```c
// designed for and tested with ATMega48
#include <avr/io.h>
#define F_CPU 8000000UL
#include <avr/delay.h>
#include <avr/interrupt.h>

/*
character format (3x5):
    KFA
    LGB
    MHC
    NID
    OJE

variable format:
    2-byte, 16-bit int 0b0ABCDEFGHIJKLMNO
    (note that the most significant bit is not used)
*/
#define A    0b0111111010011111
#define B    0b0010101010111111
#define C    0b0100011000101110
#define D    0b0011101000111111
#define E    0b0100011010111111
#define F    0b0100001010011111
#define G    0b0100111000101110
#define H    0b0111110010011111
#define I    0b0100011111110001
#define J    0b0111110000100011
#define K    0b0110110010011111
#define L    0b0000010000111111
#define M    0b0111110110011111
#define N    0b0011111000001111
#define O    0b0011101000101110
#define P    0b0010001010011111
#define Q    0b0111011001011110
#define R    0b0010111010011111
#define S    0b0100101010101001
#define T    0b0100001111110000
#define U    0b0111110000111111
#define V    0b0111100000111110
#define W    0b0111110001111111
#define X    0b0110110010011011
#define Y    0b0110000011111000
#define Z    0b0110011010110011
#define n0    0b0111111000111111
#define n1    0b0000011111101001
#define n2    0b0111011010110111
#define n3    0b0111111010110001
#define n4    0b0111110010011100
#define n5    0b0101111010111101
#define n6    0b0101111010111111
#define n7    0b0110001011110000
#define n8    0b0111111010111111
#define n9    0b0111111010111101
#define SP    0b0000000000000000
#define BK    0b0111111111111111
#define SQ    0b0001000111000100
#define PR    0b0000110001100011
#define AR    0b0001000111011111

volatile char width=1; // width of characters, widen to slow speed

#define spd 8300 // synchronization, incr to make it slant upward

void rest(char times){while (times){times--;_delay_us(spd);}}

void on(char restfor){OCR0A=110;rest(restfor);}
void off(char restfor){OCR0A=0;rest(restfor);}

void sendChar(int tosend){
    char w;
    char bit;
    for(w=0;w<width*2;w++){ // left column
        off(1);
        for (bit=0;bit<5;bit++){
                if ((tosend>>bit)&1) {on(1);}
                else {off(1);}
            }
        off(1);
        }
    for(w=0;w<width*2;w++){ // middle column
        off(1);
        for (bit=5;bit<10;bit++){
                if ((tosend>>bit)&1) {on(1);}
                else {off(1);}
            }
        off(1);
        }
    for(w=0;w<width*2;w++){ // right column
        off(1);
        for (bit=10;bit<15;bit++){
                if ((tosend>>bit)&1) {on(1);}
                else {off(1);}
            }
        off(1);
        }
    off(14); // letter space (1 column)
}

// CUSTOMIZE THE MESSAGE, OR GENERATE IT DYNAMICALLY!
int message[]={AR,AR,AR,S,W,H,A,R,D,E,N,PR,C,O,M,SP,R,O,C,K,S,
    SP,AR,AR,AR,SP,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,
    V,W,X,Y,Z,n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,BK,SP};

void sendMessage(){
    char i;
    for(i=0;i<sizeof(message)/2;i++){
        sendChar(message[i]);
    }
}

int main(){ // ### PROGRAM STARTS HERE ###

    // this sets up CPWM in CTC mode,
    // it may be slightly different for other chips
    DDRD|=255; // OC0A is now an output
    TCCR0A=0b01000010; // toggle on match, CTC mode
    TCCR0B=0B00000011; // set prescalar

    for(;;){
        width=1; // fast mode
        sendMessage();
        width=3; // slow mode
        sendMessage();
    }

    return 0;
}

```
