---
title: Crystal Oven Experiments
date: 2010-11-28 17:06:18
tags: ["circuit", "microcontroller", "obsolete"]
---



__Now that I've finished my__ 6-channel data logger (previous post), it's time to put it to the test!  I'm using a handful of LM335 temperature sensors to measure temperature, and a 20 Ohm resistor to act as a heater.  When 1A of current passes through it, it gets quite toasty!  First, I'll make some temperature probes...

<div class="text-center img-border">

![](https://swharden.com/static/2010/11/28/IMG_4581.jpg)
![](https://swharden.com/static/2010/11/28/IMG_4588.jpg)

</div>

__UPDATE:__ Those photos show a partially completed sensor. Obviously the third wire is required between the resistor and the LM335 to allow for measurement! Here's a more completed sensor before the shrink tube was massaged over the electrical elements:

<div class="text-center img-border">

![](https://swharden.com/static/2010/11/28/IMG_4591.jpg)

</div>

__Then I mounted the sensors__ on a block of steel with the heater on one side.  This way I can use one temperature to measure the heater temperature, and the other to measure the temperature of the metal chassis.  I then put the whole thing in a small Styrofoam box. 

<div class="text-center img-border">

![](https://swharden.com/static/2010/11/28/IMG_4606.jpg)
![](https://swharden.com/static/2010/11/28/IMG_4615.jpg)

</div>

__When I fire the heater,__ that sucker gets pretty darn hot. In 40 minutes it got almost 250F (!) at which time I pulled the plug on the heater and watched the whole thing cool. Notice how the metal chassis lags behind the temperature of the heater. I guess it's a bit of a "thermal low-pass filter".  Also, yes, I'm aware I spelled chassis incorrectly in the graphs.

<div class="text-center">

![](https://swharden.com/static/2010/11/28/howhot.png)
![](https://swharden.com/static/2010/11/28/quicktest.png)

</div>

__But how do we use this to build a thermo-stable crystal oven for a MEPT (radio transmitter)?__ I tried a lot of code, simply "if it's too cold, turn heater on / if it's too hot, turn heater off" but because the chassis always swung behind the heater, and even the heater itself had a bit of a delay in heating up, the results were always slowly oscillating temperatures around 10F every 20 min. That's worse than no heater!  My best luck was a program to hold temperature stable at 100F with the following rules:

* `1.) If heater > 155F, turn heater off (prevent fire)`
* `2.) If chassis < 100F, turn heater on`
* `3.) if (heater-target) > (target-chassis), turn heater off`

<div class="text-center">

![](https://swharden.com/static/2010/11/28/heaterworks.png)

</div>

__What a great job!__ That thing is practically stable in 20 minutes. The advantage of this over an analog method is that I can set the temperature in software (or provide an interface to change temperature) and my readings are analytical, such that they can be conveyed in a radio message. Again, my best results came when I implemented rule 3 in the code above. More experiments to come!