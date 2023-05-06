---
title: High Altitude Balloon Transmitter
date: 2010-07-14 08:05:46
tags: ["qrss", "amateur radio", "old"]
---

# High Altitude Balloon Transmitter

<blockquote class="wp-block-quote"><p><b>SUMMARY:</b> A small group of high school students taking an AP class for college credit launched a high-altitude weather balloon with a small payload. In addition to a video transmitter and GPS transmitter, they decided to include a simple transmitter built from scratch. This is the story of the project, with emphasis on the simple transmitter's design, construction, implementation, and reception (which surprised me, being detected ~200 miles away and lasting the entire duration of the flight!) [<a href="http://www.SWHarden.com/blog/images/beeps.ogg">sample.ogg</a>]</p></blockquote>

# 6/16/2010 - TRACKING

__I'm impressed __ how well the transmitter/receiver worked! For only a few milliwatts, I was able to track that thing all the way from takeoff to landing in Gainesville, FL a few hundred miles away.

<div class="text-center img-border">

[![](balloon_track_thumb.jpg)](balloon_track.jpg)

</div>

__ANALYSIS:__ the text on the image describes most if it, but one of the most interesting features is the "multipathing" during the final moments of the descent, where the single carrier signal splits into two. I believe this is due to two Doppler shifts: (1) as the distance between the falling transmitter and the receiver is decreasing, producing a slight in increase in frequency, and (2) a signal reflected off of a layer of the atmosphere above the craft (the ionosphere?) before it gets to the receiver, the distance of which is increasing as the craft falls, producing a decrease in frequency. I'll bet I can mathematically work backwards and determine how high the craft was, how fast it was falling, and/or how high the layer of the reflecting material is - but that's more work than this dental student is prepared to do before his morning coffee!

__HERE IS SOME AUDIO__ of some of the strongest signals I received. Pretty good for a few milliwatts a hundred miles away! \[[beeps.ogg](http://www.SWHarden.com/blog/images/beeps.ogg)\]

# 6/16/2010 - THE FLIGHT

![](https://www.youtube.com/embed/qjLrytsDPjw)

The design team:

<div class="text-center img-border">

[![](DSC_7127_thumb.jpg)](DSC_7127.jpg)

</div>

<strong>Walking the balloon</strong> to its launch destination at NASA with an awesome rocket (Saturn 1B - identified by Lee, KU4OS) in the background.

<div class="text-center img-border">

[![](DSC_7210_thumb.jpg)](DSC_7210.jpg)

</div>

<strong>The team</strong> again, getting ready for launch. I've been informed that the reason their hands are up is to prevent the balloon from tilting over too much. I'd imagine that a brush with a grass blade could be bad news for the project!

<div class="text-center img-border">

[![](DSC_7232_thumb.jpg)](DSC_7232.jpg)

</div>

<strong>Last minute checks</strong> - you can see the transmitter and battery holders for it taped to the Styrofoam. 

<div class="text-center img-border">

[![](DSC_7248_thumb.jpg)](DSC_7248.jpg)

</div>

The transmitter in its final position:

<div class="text-center img-border">

[![](DSC_7250_thumb.jpg)](DSC_7250.jpg)

</div>

Note the coil of yellow wire. That serves as a rudimentary "ground" for the antenna's signal to push off of. I wasn't very clear on my instructions on how to make it. I meant that it should be a huge coil wrapped around the entire payload (as large as it can be), which would have probably produced a better signal, but since I was able to capture the signal during the whole flight it turned out to be a non-issue.

<strong>The antenna</strong> can be seen dropping down as a yellow wire beneath the payload. (arrow)

<div class="text-center img-border">

[![](DSC_7253_thumb.jpg)](DSC_7253.jpg)

[![](DSC_7279_thumb.jpg)](DSC_7279.jpg)

</div>

<strong>Launch!</strong> Look how fast that balloon is rising!

<div class="text-center img-border">

[![](DSC_7294_thumb.jpg)](DSC_7294.jpg)

</div>

<strong>It's out of our hands</strong> now. When I got the text message that it launched, I held my breath. I was skeptical that the transmitter would even work!  

<div class="text-center img-border">

[![](DSC_7297_thumb.jpg)](DSC_7297.jpg)

</div>

<strong>One of the students</strong> listening to my transmitter with QRSS VD software (score!)

<div class="text-center img-border">

[![](DSC_7365_thumb.jpg)](DSC_7365.jpg)

</div>

<strong>Video capture</strong> from an on-board camera was also attempted (900MHz), but from what I hear it didn't function well for very long.

<div class="text-center img-border">

[![](DSC_7334_thumb.jpg)](DSC_7334.jpg)

</div>

# 6/15/2010 - IMPROVED BUILD

__Here you can see me__ (center arrow) showing the students how to receive the Morse code signal sent from the small transmitter (left arrow) using a laptop running [QRSS VD (my software)](http://www.swharden.com/blog/qrss_vd/) analyzing audio from and an Icom706 mkII radio receiver attached to a dipole (right arrow).

<div class="text-center img-border">

[![](DSC_7082_thumb.jpg)](DSC_7082.jpg)
[![](72hc240_qrp_amplifier_thumb.jpg)](72hc240_qrp_amplifier.jpg)

</div>

__I amped-up the output of the oscillator__ using an octal buffer chip (74HC240) with some decent results. I'm pleased! It's not perfect (it's noisy as heck) but it should be functional for a 2 hour flight.

<div class="text-center img-border">

[![](01_closeup_thumb.jpg)](01_closeup.jpg)

</div>

Closeup of the transmitter showing the oscillator at 29.4912 MHz, the Atmel ATTiny44a AVR microcontroller (left chip), octal buffer 74HC240 (right chip), and some status lights which blink as the code is executed.

<div class="text-center img-border">

[![](02_workstation_thumb.jpg)](02_workstation.jpg)

</div>

__This is my desk__ where I work from home. Note the styrofoam box in the background - that's where my low-power transmitter lives (the one that's spotted around the world). All I needed to build this device was a soldering iron.

<div class="text-center img-border">

[![](03_room_thumb.jpg)](03_room.jpg)

</div>

__Although I had a radio,__ it is not capable of receiving 29MHz so I was unable to test the transmitter from home. I had to take it to the university to assess its transmitting capabilities.

__I connected the leads to the output of the transmitter, shorted by a 39ohm resistor.__ By measuring the peak-to-peak voltage of the signal going into a resistor, we can measure its power.

__Here's the test setup.__ The transmitter is on the blue pad on the right, and the waveform can be seen on the oscilloscope on the upper left.

<div class="text-center img-border">

[![](06_scope_thumb.jpg)](06_scope.jpg)

</div>

__With the amplifier off__, the output power is just that of the oscillator. Although the wave should look like a sine wave, it's noisy, and simply does not. While this is unacceptable if our goal is a clean radio signal with maximum efficiency, this is good enough to be heard at our target frequency. The PPV (peak-to-peak voltage) as seen on the screen is about 100mV. Since I'm using a x10 probe, this value should be multiplied by 10 = 1V. 1V PPV into 39 ohms is about __3 milliwatts!__ ((1/(2\*2^.5))^2/39\*1000=3.2). For the math, see [this post](http://www.swharden.com/blog/2010-05-28-measuring-qrp-radio-output-power-with-an-oscilliscope/)

__With the amplifier,__ the output is much more powerful. At 600mV peak-to-peak with a 10x probe (actually 6V peak-to-peak, expected because that's the voltage of the 4xAAA battery supply we're using) into 39 ohms we get __115 millivolts!__ (6/(2\*2^.5))^2/39\*1000=115.38.

__Notes about power:__ First of all, the actual power output isn't 115mW. The reason is that the math equations I used work only for pure sine waves. Since our transmitter has multiple waves in it, less than that power is going to produce our primary signal. It's possible that only 50mW are going to our 29MHz signal, so the power output assessment is somewhat qualitative. Something significant however is the difference between the measured power with and without the amplifier. The 6x increase in peak-to-peak voltage results in a 36x (6^2) increase in power, which is very beneficial. I'm glad I added this amplifier! A 36 times increase in power will certainly help.

<div class="text-center img-border">

[![](balloon_transmitter_final_thumb.jpg)](balloon_transmitter_final.png)

</div>

# 6/14/2010 - THE BUILD

__Last week I spoke with a student in the UF aerospace engineering department who told me he was working with a group of high school students to add a payload to a high-altitude balloon being launched at (and tracked by) NASA.__ We tossed around a few ideas about what to put on it, and we decided it was worth a try to add a transmitter. I'll slowly add to this post as the project unfolds, but with only 2 days to prepare (wow!) I picked a simplistic design which should be extremely easy to understand by everyone. Here's the schematic:

<div class="text-center img-border">

[![](balloon_transmitter_thumb.jpg)](balloon_transmitter.png)

</div>

__The code is as simple as it gets.__ It sends some Morse code ("go gators"), then a long tone (about 15 seconds) which I hope can be measured QRSS style. I commented virtually every line so it should be easy to understand how the program works.

```c
#include <avr/io.h>
#include <util/delay.h>

char call[] = {2, 2, 1, 0, 2, 2, 2, 0, 0, 2, 2, 1, 0, 1, 2, 0, 2, 0, 2, 2, 2, 0, 1, 2, 1, 0, 1, 1, 1, 0, 0};
// 0 for space, 1 for dit, 2 for dah

void sleep()
{
    _delay_ms(100);      // sleep for a while
    PORTA ^= (1 << PA1); // "flip" the state of the TICK light
}

void ON()
{
    PORTB = 255;          // turn on transmitter
    PORTA |= (1 << PA3);  // turn on the ON light
    PORTA &= ~(1 << PA2); // turn off the ON light
}

void OFF()
{
    PORTB = 0;            // turn off transmitter
    PORTA |= (1 << PA2);  // turn on the OFF light
    PORTA &= ~(1 << PA3); // turn off the OFF light
}

void ID()
{
    for (char i = 0; i < sizeof(call); i++)
    {
        if (call[i] == 0)
        {
            OFF();
        } // space
        if (call[i] == 1)
        {
            ON();
        } // dot
        if (call[i] == 2)
        {
            ON();
            sleep();
            sleep();
        } // dash
        sleep();
        OFF();
        sleep();
        sleep(); // between letters
    }
}

void tone()
{
    ON(); // turn on the transmitter
    for (char i = 0; i < 200; i++)
    { // do this a lot of times
        sleep();
    }
    OFF();
    sleep();
    sleep();
    sleep(); // a little pause
}

int main(void) // PROGRAM STARTS HERE
{
    DDRB = 255; // set all of port B to output
    DDRA = 255; // set all of port A to output
    PORTA = 1;  // turn on POWER light

    while (1)
    {           // loop forever
        ID();   // send morse code ID
        tone(); // send a long beep
    }
}
```

__I'm now wondering if I should further amplify this signal's output power.__ Perhaps a 74HC240 can handle 9V? ... or maybe it would be better to use 4 AAA batteries in series to give me about 6V. \[ponders\] [this](http://www.SWHarden.com/blog/images/balloon_transmitter_amplified.png) is the schematic I'm thinking of building.

**UPDATE:** This story was featured on [Hack-A-Day](http://hackaday.com/2010/07/27/200-mile-rf-transmitter-and-high-altitude-balloon/)! Way to go everyone!

<div class="text-center img-border">

[![](hackaday_swharden_thumb.jpg)](hackaday_swharden.png)

</div>

