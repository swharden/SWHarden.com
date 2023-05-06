---
title: 1 Rotary Encoder, 3 Pins, 6 Inputs
date: 2017-02-02 22:48:53
tags: ["microcontroller", "circuit"]
---

# 1 Rotary Encoder, 3 Pins, 6 Inputs

__Rotary encoders are a convenient way to add complex input functionality to small hardware projects with a single component. __Rotary encoders (sometimes called shaft encoders, or rotary shaft encoders) can spin infinitely in both directions and many of them can be pressed like a button. The volume knob on your car radio is probably a rotary encoder.

> With a single component and 3 microcontroller pins I can get six types of user input: turn right, turn left, press-and-turn right, press-and-turn left, press and release, and press and hold.

__A few years ago I [made a video](https://www.youtube.com/watch?v=DREGVc00FY8) discussing how rotary shaft encoders work and how to interface them with microcontrollers.__ Although I'm happy it has over 13,000 views, I'm disappointed I never posted the code or schematics on my website (despite the fact I said on the video I would). A few years later I couldn't find the original code anymore, and now that I'm working on a project using these devices I decided to document a simple case usage of this component.

![](https://www.youtube.com/embed/ZGIQm1tDnRw)

This post is intended to be a resource for future me just as much as it is anyone who finds it via Google or YouTube. This project will permanently live in a "rotary encoder" folder of my AVR projects GitHub page: [AVR-projects](https://github.com/swharden/AVR-projects). For good measure, I made a follow-up YouTube video which describes a more simple rotary encoder example and that has working links to this code.

__At about $.50 each,__ rotary encoders are certainly more expensive than other switches (such as momentary switches). A [quick eBay search](http://www.ebay.com/sch/?_nkw=rotary+encoder+10pcs) reveals these components can be purchased from china in packs of 10 for $3.99 with free shipping. [On Mouser similar components](http://www.mouser.com/ProductDetail/BI-Technologies-TT-Electronics/EN12-HN22AF25) are about $0.80 individually, cut below $0.50 in quantities of 200. The depressible kind have two pins which are shorted when the button is pressed. The rotary part has 3 pins, which are all open in the normal state. Assuming the center pin is grounded, spinning the knob in one direction or the other will temporarily short both of the other pins to ground, but slightly staggered from each other. The order of this stagger indicates which direction the encoder was rotated.

<div class="text-center">

[![](https://swharden.com/static/2017/02/02/schematic_thumb.jpg)](https://swharden.com/static/2017/02/02/schematic.png)

</div>

I typically pull these all high through 10k series resistors ([debounced](http://www.labbookpages.co.uk/electronics/debounce.html) with a 0.1uF capacitor to ground to reduce accidental readings) and sense their state directly with a microcontroller. Although capacitors were placed where they are to facilitate a rapid fall time and slower rise time, their ultimate goal is high-speed integration of voltage on the line as a decoupling capacitor for potential RF noise which may otherwise get into the line. Extra hardware debouching could be achieved by adding an additional series resistor immediately before the rotary encoder switch. For my simple application, I feel okay omitting these. If you want to be really thorough, you may benefit from adding a Schmidt trigger between the output and the microcontroller as well. Note that I can easily applying time-dependent debouncing via software as well.

<div class="text-center img-border">

[![](https://swharden.com/static/2017/02/02/scope_thumb.jpg)](https://swharden.com/static/2017/02/02/scope.jpeg)
[![](https://swharden.com/static/2017/02/02/704_thumb.jpg)](https://swharden.com/static/2017/02/02/704.jpg)

</div>

### Single Click Left and Right

<div class="text-center img-border img-small">

[![](https://swharden.com/static/2017/02/02/left_thumb.jpg)](https://swharden.com/static/2017/02/02/left.png)
[![](https://swharden.com/static/2017/02/02/right_thumb.jpg)](https://swharden.com/static/2017/02/02/right.png)

</div>

### Spin Left and Right

<div class="text-center img-border img-small">

[![](https://swharden.com/static/2017/02/02/fastLeft_thumb.jpg)](https://swharden.com/static/2017/02/02/fastLeft.png)
[![](https://swharden.com/static/2017/02/02/fastRight_thumb.jpg)](https://swharden.com/static/2017/02/02/fastRight.png)

</div>

## Code Notes

### Setting-up PWM on ATTiny2313

I chose to use the 16-bit Timer/Counter to generate the PWM. 16-bits of duty control feels excessive for controlling an LED brightness, but my ultimate application will use a rotary encoder to finely and coarsely adjust a radio frequency, so there is some advantage to having this fine level of control. To round things out to a simple value, I'm capping the duty at 10,000 rather than the full 65,535. This way I can set the duty to 50% easily by setting OCR1A to 5,000. Similarly, spinning left/right can adjust duty by 100, and push-and-turn can adjust by 1,000.

```c
void setupPWM_16bit(){
    DDRB|=(1<<PB3); // enable 16-bit PWM output on PB3
    TCCR1A|=(1<<COM1A1); // Clear OC1A/OC1B on Compare Match
    TCCR1B|=(1<<WGM13); // enable "PWM, phase and frequency correct"
    TCCR1B|=(1<<CS10); // enable output with the fastest clock (no prescaling)
    ICR1=10000; // set the top value (could be up to 2^16)
    OCR1A=5000; // set PWM pulse width (starts at 50% duty)
}
```

### Simple (spin only) Rotary Encoder Polling

```c
void poll_encoder_v1(){
    // polls for turns only
    if (~PINB&(1<<PB2)) {
        if (~PINB&(1<<PB1)){
            // left turn
            duty_decrease(100);
        } else {
            // right turn
            duty_increase(100);
        }
        _delay_ms(2); // force a little down time before continuing
        while (~PINB&(1<<PB2)){} // wait until R1 comes back high
    }
}
```

### Simple (spin only) Rotary Encoder Polling

```c
void poll_encoder_v2(){
    // polls for turns as well as push+turns
    if (~PINB&(1<<PB2)) {
        if (~PINB&(1<<PB1)){
            if (PINB&(1<<PB0)){
                // left turn
                duty_decrease(100);
            } else {
                // left press and turn
                duty_decrease(1000);
            }
        } else {
            if (PINB&(1<<PB0)){
                // right turn
                duty_increase(100);
            } else {
                // right press and turn
                duty_increase(1000);
            }
        }
        _delay_ms(2); // force a little down time before continuing
        while (~PINB&(1<<PB2)){} // wait until R1 comes back high
    }
}
```

### What about an interrupt-based method?

A good compromise between continuous polling and reading pins only when we need to is to take advantage of the pin change interrupts. Briefly, we import avr/interrupt.h, set GIMSK, EIFR, and PCMSK (definitely read the datasheet) to trigger a hardware interrupt when a pin state change is detected on any of the 3 inputs. Then we run sei(); to enable global interrupts, and our functionality is identical without having to continuously call our polling function!

```c
// run this only when pin state changes
ISR(PCINT_vect){poll_encoder_v2();}

int main(void){
    setupPWM_16bit();

    // set up pin change interrupts
    GIMSK=(1<<PCIE); // Pin Change Interrupt Enable
    EIFR=(1<<PCIF); // Pin Change Interrupt Flag
    PCMSK=(1<<PCINT1)|(1<<PCINT2)|(1<<PCINT3); // watch these pins
    sei(); // enable global interrupts

    for(;;){} //forever
}
```

Code for this project is available on the GitHub: https://github.com/swharden/AVR-projects