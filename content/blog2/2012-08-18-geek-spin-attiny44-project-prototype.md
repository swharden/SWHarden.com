---
title: Geek Spin - ATTiny44 Project Prototype
date: 2012-08-18 15:28:38
tags: ["microcontroller", "obsolete"]
---

# Geek Spin - ATTiny44 Project Prototype

__Some days you feel like working on projects to benefit humanity. The day I made this clearly wasn't one of those days.__ A little over a year ago, I got into a troll war with my friend [Mike Seese](http://www.mikeseese.com/). The joke, similar to that of [rick rolling](http://www.youtube.com/watch?v=oHg5SJYRHA0), was to get each other to unexpectedly click a link to the [Hatsune Miku version of the leekspin song](http://www.youtube.com/watch?v=kbbA9BhCTko&feature=player_embedded). After several weeks of becoming beyond annoying, I decided to make an _actual_ Hatsune Miku which would spin her leek and bobble her head to the techno version of the [Levan Polka](http://www.youtube.com/watch?v=1ygdAiDxKfI) for his birthday.

<div class="text-center img-border">

![](https://swharden.com/static/2012/08/18/leek-spin.gif)

</div>

__The goal was to create a minature Miku which would perform perfectly in sync with audio coming from a portable music player (iPod or something) and _NOT_ require a computer connection.__ I accomplished it by sending some creative control beeps out of the left channel of the stereo signal. Although I didn't finish the project, I got pretty far with the prototype, so I decided to dig it out of the archives and share it with the world because it's pretty entertaining!

{{<youtube RzqdL5gqaHM>}}

(look how close I came to replicating the original:

{{<youtube 6ZWwqTnqxdk>}}

__How did I do it?__ First off, I used servos. If you're not familiar with them, I suggest you look up [how servos work](http://www.servocity.com/html/how_do_servos_work_.html). Perhaps check out [how to control servos with AVR microcontrollers](http://www.engineersgarage.com/embedded/avr-microcontroller-projects/atmega16-servo-motor-circuit). Basically, their position along a rotational axis is determined by the width of a pulse on a 20ms time window. Anyhow, if I only had 1 servo to control (i.e., leek only), I'd have controlled the servo directly with PWM signals in the left channel - no microcontroller needed, easy as pie, problem solved. However, since I needed to control two servos, I had to come up with something a bit more creative. Although I could have probably done this ten different ways, the way I chose to do it was using a series of pre-encoded leek spin and head bobble motions, triggered by control beeps in the left channel of the audio cable. (The right channel was patched through to the speakers.)  Below is a diagram of what I believe I did, although I didn't thoroughly document it at the time, so you might have to use your imagination if you decide to re-create this project.

<div class="text-center img-border">

![](https://swharden.com/static/2012/08/18/2012-08-18-15.21.34-525x289.jpg)

</div>

__The idea is that by sending bursts of sine waves,__ the circuit can rectify them and smooth them out to have them look to a microcontroller like a brief "high" signal. Each signal would tell the microcontroller to proceed to the next pre-programmed (and carefully timed) routine.  With enough practice listening, watching, and tweaking the code, I was able to make a final version which worked pretty darn well!


<div class="text-center img-border">

![](https://swharden.com/static/2012/08/18/geek_spin.gif)

</div>

__LISTEN__ to the [music with control beeps](http://www.SWHarden.com/blog/images/2012/08/GOLEEKGO.mp3) (it's a surprisingly fun listen)

__A few technical details__ are that I used an ATTiny44a microcontroller (it may have been an ATTiny2313, I can't remember for sure, but they're so similar it's virtually negligable).  The servos I used were cheap (maybe $4?) from eBay. They looked like the one pictured below. The servo position was controlled by PWM, but I manually sent the pulses and didn't actually use the integrated PWM in the microcontroller.  I can't remember why I did it this way - perhaps because it was so simple to use the _delay_us() and _delay_ms() functions? I also used an operational amplifier (if I remember, it was a LM741) to boost the left channel control signals rather than rectifying/assessing the left channel directly.

<div class="text-center img-border img-micro">

![](https://swharden.com/static/2012/08/18/01_findpic.png)
![](https://swharden.com/static/2012/08/18/02_dropbg.jpg)
![](https://swharden.com/static/2012/08/18/08_hairtop.jpg)
![](https://swharden.com/static/2012/08/18/06_blockskirt.jpg)
![](https://swharden.com/static/2012/08/18/body.png)
![](https://swharden.com/static/2012/08/18/hairtop.png)

</div>

[This is the video](https://www.youtube.com/embed/kbbA9BhCTko) which I mimiced to create my prototype (note how the leek in her arm and her head move exactly the same as the prototype I made - score!)

__And how did I find out about this song?__ I actually saw it on the video below which was hosted on wimp.com. I thought the song was catchy, looked it up, and the rest was history. It's worth noting that (perhaps to avoid copyright issues?) the key was shifted two half-steps up. I get a kick out of the way the girl waves her arm in the beginning, mimicking the leek :)

{{<youtube Pk1CTYszDFU>}}

__Here are some of the images I made__ which I printed, glued to foam board, and cut out with a razor blade. I'm not sure how useful they are, but they're provided just in case.

... but sometimes Japan takes it a bit too far and things get awkward ...

__Below is the code I used.__ Note that PWM that controls the servos isn't the integrated PWM, but rather a couple pins I manually pulse on and off to control the arm and head positions. Also notice how, in the main routine, I wait for the control beeps before continuing the next sequences.

```c

// leek spin code - designed for ATTiny
// by Scott Harden, www.SWHarden.com

#include <avr/io.h>
#include <avr/delay.h>

void go_high(){
    // sets the arm to the highest position
    for (char i=0;i<5;i++){
        PORTA|=(1<<PA0);
        _delay_us(1400);
        PORTA&=~(1<<PA0);
        _delay_us(20000-1200);
        }
    }

void go_low(){
    // sets the leek to the middle position
    for (char i=0;i<5;i++){
        PORTA|=(1<<PA0);
        _delay_us(1900);
        PORTA&=~(1<<PA0);
        _delay_us(20000-1900);
        }
    }

void go_lowest(){
    // sets the leek to the lowest position
    for (char i=0;i<5;i++){ // takes 100ms total
        PORTA|=(1<<PA0);
        _delay_us(2300);
        PORTA&=~(1<<PA0);
        _delay_us(20000-2500);
        }
    }

void go_slow(char times){
    // does one slow leek down/up
    // beat is 500ms
    for (char i=0;i<times;i++){
        go_low();
        _delay_ms(10);
        go_high();
        _delay_ms(290);
        PORTA^=(1<<PA2);
        PORTA^=(1<<PA3);
    }
}

void go_fast(char times){
    // does one fast leek down/up
    // beat is 250ms
    for (char i=0;i<times;i++){
        go_low();
        _delay_ms(10);
        go_high();
        _delay_ms(15);
        PORTA^=(1<<PA2);
        PORTA^=(1<<PA3);
    }
}
void head_left(){
    // tilts the head to the left
    for (char i=0;i<5;i++){
        PORTA|=(1<<PA1);
        _delay_us(1330);
        PORTA&=~(1<<PA1);
        _delay_us(20000-1200);
        }
    }

void head_right(){
    // tilts the head to the right
    for (char i=0;i<5;i++){
        PORTA|=(1<<PA1);
        _delay_us(1500);
        PORTA&=~(1<<PA1);
        _delay_us(20000-1200);
        }
    }

void head_center(){
    // centers the head
    for (char i=0;i<5;i++){
        PORTA|=(1<<PA1);
        _delay_us(1400);
        PORTA&=~(1<<PA1);
        _delay_us(20000-1200);
        }
    }

void head_go(char times){
    // rocks the head back and forth once
    for (char i=0;i<(times-1);i++){
        head_left();
        _delay_ms(400);
        PORTA^=(1<<PA2);
        PORTA^=(1<<PA3);
        head_right();
        _delay_ms(400);
        PORTA^=(1<<PA2);
        PORTA^=(1<<PA3);
    }
    head_center(); // returns head to center when done
    _delay_ms(400);
    PORTA^=(1<<PA2);
    PORTA^=(1<<PA3);
}

int main(void) {
    while (1){
        DDRA=255; // set port A (servos) as outputs
        DDRB=0; // set port B (listening pins) as inputs

        go_lowest();head_center();// set starting positions

        while ((PINB & _BV(PB0))){} // wait for beep que
        PORTA=(1<<PA3);
        go_high();_delay_ms(1000);
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_slow(31); // tilt leek slowly 31 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_slow(31); // tilt leek slowly 31 times

        while ((PINB & _BV(PB0))){} // wait for beep que
        _delay_ms(200);
        head_go(16); // rock head 16 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_fast(68); // tilt leek rapidly 68 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_slow(24); // tilt leek slowly 24 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_fast(17); // tilt leek rapidly 17 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_slow(31); // tilt leek slowly 31 times
        while ((PINB & _BV(PB0))){} // wait for beep que
        go_slow(31); // tilt leek slowly 31 times

        while ((PINB & _BV(PB0))){} // wait for beep que
        _delay_ms(200);
        head_go(16); // rock head 16 times
        go_lowest(); // reset position
        PORTA=0;
    }
  return 0;
}

```

__Finally, I'd like to take a moment to indicate one of the reasons this project is special to me.__ My wife, Angelina Harden, died one year ago today. This project was the last one she worked on with me. She died a few days after the video was taken, and in the process of moving out of our apartment I threw away almost everything (including this project). Although I never finished it, I remember working on it with Angelina - we went to wal-mart together to buy the foam board I used to make it, and she told me that I should make her head rock back and forth rather than just move her arm. I remember that, once it was all done, I let her sit in the chair in front of it and played it through, and she laughed nearly the whole time :) I'll always miss her.