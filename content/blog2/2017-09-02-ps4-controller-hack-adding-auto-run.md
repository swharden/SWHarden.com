---
title: PS4 Controller Hack - Adding Auto-Run
date: 2017-09-02 15:48:22
tags: ["circuit"]
---



**After a long day** it can be really nice to have a relaxing hobby to clear your head, and few activities shut down your brain as effectively as video games. However, a newly released video game is physically hurting me as my impulse to move quickly causes me to perpetually click the run button. After a few days of game-play and a really sore left thumb, I decided to do something about it: hack-in a microchip to automatically click the button for me.

**Modifying game controllers to do things like automatically rapid fire is nothing new.** I once modified a USB computer mouse to add an extra "rapid fire" button ([link](https://www.swharden.com/wp/2010-12-28-full-auto-rapidfire-mouse-modification/)). Hackaday ran a story about a guy who[ hacked a PS4 controller to add mouse and keyboard functionality](https://hackaday.com/2013/12/12/modifying-a-ps4-dualshock4-controller-to-use-a-mouse-and-keyboard/). Today's hack isn't quite as elaborate, but it's very effective. Here I show how I modified a PlayStation 4 controller to automatically click the L3 button so I am always running. This auto-run functionality mimics the auto-run feature built into many games (like [Titanfall 2](https://www.youtube.com/watch?v=EXwdWuSuiYA) which spoiled me to expect this), but I built the circuit so it can be toggled on and off by clicking the L3 button. After playing Titanfall 2 for the last few months, the recent release of the [Call of Duty WWII](https://www.youtube.com/watch?v=D4Q_XYVescc) beta is driving me crazy as it requires me to click the run button over and over (every two seconds) which, after an afternoon of playing, is actually painful.

{{<youtube v-164sv21Tw>}}

## Assessing the PS4 Controller

**I started out by looking online to see what the PS4 controller looked like inside.** Imgur has a [great PS4 dualshock controller teardown photo collection](http://imgur.com/a/ytRW5) which was an excellent starting place. From these photos I realized this hack would be pretty easy since the L3 "click" action is achieved by a [through-hole SPDT tactile switch](https://learn.sparkfun.com/tutorials/switch-basics) placed under the joystick.

<div class="text-center">

![](https://swharden.com/static/2017/09/02/teardown.jpg)

</div>

**I was surprised to find** my PS4 controller (below) was a little different (green for starters), but the overall layout was the same. I quickly identified the 4 pins of the L3 tactile switch and got to work...

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/069.jpg)

</div>

**After probing around** **with a multimeter and an oscilloscope,** **I was able to determine which pins do what.** Just from looking at the trace it's pretty obvious that two of the pins are the positive voltage rail. In this controller the positive voltage (VCC) is about 3 volts, so keep that in mind and don't hook-up a 5V power supply if you decide to debug this thing.

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/095.jpg)

</div>

**To test my idea I attached 3 wires to VCC, GND, and SENSE and ran into the other room where my PS4 was.** As I held the left joystick up in a game, shorting the SENSE and GND wires (by tapping them together) resulted in running! At this point I knew this hack would work, and proceeded to have a microcontroller control voltage of the L3 sense line.

## Simulating L3 Presses with a Microcontroller

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/145.jpg)

</div>

**I glued a microcontroller ([ATTiny85](http://www.atmel.com/images/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf)) to the circuit board, then ran some wires to the points of interest.** Visual inspection (and a double check with a multimeter when the battery was in) provided easy points for positive and ground which could power my microcontroller. The "L3 sense" pin (which toggles between two voltages when you press the L3 button) was run to pin 3 (PB4) of the microcontroller. In a production environment current limiting resistors and debounce capacitors would make sense, but in the spirit of the hack I keep things minimalistic.

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/158.jpg)

</div>

**The device could be easily reassembled,** and there was plenty of room for the battery pack and its plastic holder to snap in place over the wires. Excellent!

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/161.jpg)

</div>

**While I was in the controller,** I removed the light-pipe that carries light to the diffuser on the back. The PS4 has an embarrassingly poor design (IMO) where the far side of the controller emits light depending on the state of the controller (blue for in use, black for off, orange for charging, etc). This is a terrible design in my opinion because if you have a glossy and reflective TV screen like I do, you see a blue light reflect back in the screen and bobble up and down as you hold the controller. Dumb! Removing the light pipe dramatically reduced the intensity, but still retains the original functionality.

<div class="text-center img-border">

![](https://swharden.com/static/2017/09/02/166.jpg)

</div>

**Programming the microcontroller** was achieved with an in circuit serial programmer ([USBtinyISP](https://www.ebay.com/sch/i.html?&_nkw=USBtinyISP)) with test clips. This is my new favorite way to program microcontrollers for one-off projects. If the pins of the microcontroller aren't directly accessable, breaking them out on 0.1" headers is simple enough and they make great points of attachment for test clips. The simplest code to continuously auto-run is achieved by just swinging the sense line between 5V and 0V. This is the code to do that:

```c
for(;;){ // do this forever
    // simulate a button press
    PORTB|=(1<<PB4); // pull high
    _delay_ms(50); // hold it there
    // simulate a button release
    PORTB&=~(1<<PB4); // pull low
    _delay_ms(50); // hold it there
}

```

## Sensing Actual Button Presses to Toggle Auto-Run On/Off

**Simulating L3 presses was as simple as toggling the sense line between VCC and GND, but _sensing_ manual L3 presses wasn't quite as easy.** After probing the output on the scope (see video) I realized that manual button presses toggle between voltages of about 2V and 3V, and the line never really goes down to zero (or below VCC/2) so it's never read as "off" by the digital input pin. Therefore, I changed my strategy a bit. Instead of clamping between 5V and 0V, I toggled between low impedance and high impedance states. This seemed like it would be gentler on the controller circuit, as well as allow me to use the ADC (analog-to-digital controller) of the microcontroller to read voltage on the line. If voltage is above a certain amount, the microcontroller detects a manual button press is happening and toggles the auto-run functionality on/off. The new code is this:

```c
for(;;){ // do this forever

    // simulate a button press
    PORTB|=(1<<PB4); // pull high
    DDRB|=(1<<PB4); // make output
    _delay_ms(50); // hold it there

    // simulate a button release
    DDRB&=~(1<<PB4); // make input
    PORTB&=~(1<<PB4); // pull low
    _delay_ms(50); // hold it there

    // check if the button is actually pressed to togggle auto press
    if (ADC>200) { // if the button is manually pressed
        _delay_ms(100); // wait a bit
        while (ADC>200) {} // wait until it depresses
        while (ADC<200) {} // then wait for it to be pressed again
    }
}
```

**It works!** After giving it a spin on the Call of Duty WWII Beta, I'm happy to report that this circuit is holding up well and I'm running forever effortlessly. I still suck at aiming, shooting, and not dying though.

## Follow-Up Notes

Follow-up #1: After playing the fast-paced and highly dynamic Titanfall 2 for so long, I rapidly became disenchanted with the Call of Duty WWII game-play which now feels slow and monotonous in comparison. Although this auto-sprint controller hack works, I don't really use it because I barely play the game I made it for! I'm going back to exclusively playing Titanfall 2 for now, and if you get the chance I highly recommend giving it a spin!

{{<youtube ktw2k3m7Qko>}}

Follow-up #1: Call of DUty WWII added auto-sprint a few months after this post was made