---
title: Single Wavelength Pulse Oximeter
date: 2012-12-06 08:13:41
tags: ["circuit", "diyECG", "obsolete"]
---



> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__I want to create a microcontroller application__ which will utilize information obtained from a home-brew pulse oximeter. Everybody and their cousin seems to have their own slant how to make DIY pulse detectors, but I might as well share my experience. Traditionally, pulse oximeters calculate blood oxygen saturation by comparing absorbance of blood to different wavelengths of light. In the graph below (from [Dildy et al., 1996](http://www.ncbi.nlm.nih.gov/pubmed/8694032) that deoxygenated blood (dark line) absorbs light differently than oxygenated blood (thin line), especially at 660nm (red) and 920nm (infrared). Therefore, the ratio of the difference of absorption at 660nm vs 920nm is an indication of blood oxygenation. Fancy (or at least well-designed) pulse oximeters continuously look at the ratio of these two wavelengths. Analog devices has a [nice pulse oximeter design using an ADuC7024 microconverter](http://www.analog.com/library/analogDialogue/archives/41-01/pulse_oximeter.html). A more hackerish version was made and described [on this non-english forum](http://www.elektroda.pl/rtvforum/viewtopic.php?p=8025042). A fail-at-the-end page of a simpler project is also shown [here](http://blog.energymicro.com/2012/11/21/create-a-simple-pulse-oximeter-with-tiny-gecko/), but not well documented IMO.

<div class="text-center">

![](https://swharden.com/static/2012/12/06/pulse-oximeter-wavelength.jpg)

</div>

That's not how mine works. I only use a single illumination source (~660nm) and watch it change with respect to time. Variability is due to a recombination effect of blood volume changes and blood oxygen saturation changes as blood pulses through my finger. Although it's not quite as good, it's a bit simpler, and it definitely works. [Embedded-lab has a similar project](http://embedded-lab.com/blog/?p=5508) but the output is only a pulsing LED (not what I want) and a voltage output that only varies by a few mV (not what I want).

__Here's what the device looks like assembled in a breadboard:__


<div class="text-center img-border">

![](https://swharden.com/static/2012/12/06/IMG_5919.jpg)

</div>

__I made a sensor__ by drilling appropriately-sized holes in a clothespin for the emitter (LED) and sensor (phototransistor). I had to bend the metal spring to make it more comfortable to wear. Light pressure is better than firm pressure, not only because it doesn't hurt as much, but because a firm pinch restricts blood flow considerably.

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/06/IMG_5920.jpg)
![](https://swharden.com/static/2012/12/06/IMG_5924.jpg)

</div>

__An obvious next step__ is microcontroller + LCD (or computer) digitization, but for now all you can do is check it out on my old-school analog oscilloscope. Vertical squares represent 1V (nice!). You can see the pulse provides a solid 2V spike.

<div class="text-center img-border">

![](https://swharden.com/static/2012/12/06/pulse-scope.jpg)

</div>

__Here's some video of it in action:__

{{<youtube MwkR_Vv0wMA>}}

I'm holding-back the circuit diagram until I work through it a little more. I don't want to mislead people by having them re-create ill-conceived ideas on how to create analog amplifiers. I'll post more as I develop it.