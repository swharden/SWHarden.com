---
title: DIY ECG with 1 op-amp
date: 2016-08-08 01:49:24
tags: ["diyECG", "python", "circuit"]
---

# DIY ECG with 1 op-amp

> **⚠️ Check out my newer ECG design:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)

__I made surprisingly good ECG from a single op-amp and 5 resistors! __An ECG (electrocardiograph, sometimes called EKG) is a graph of the electrical potential your heart produces as it beats. Seven years ago I posted _[DIY ECG Machine on the Cheap](https://www.swharden.com/wp/2009-08-14-diy-ecg-machine-on-the-cheap/)_ which showed a discernible ECG I obtained using an op-amp, two resistors, and a capacitor outputting to a PC sound card's microphone input. It didn't work well, but the fact that it worked at all was impressive! It has been one of the most popular posts of my website ever since, and I get 1-2 emails a month from people trying to recreate these results (some of them are during the last week of a college design course and sound pretty desperate). Sometimes people get good results with that old circuit, but more often than not the output isn't what people expected. I decided to revisit this project (with more patience and experience under my belt) and see if I could improve it. My goal was not to create the highest quality ECG machine I could, but rather to create the _simplest_ one I could with emphasis on predictable and reproducible results. The finished project is a blend of improved hardware and custom cross-platform open-source software (which runs on Windows, Linux, and MacOS), and an impressively good ECG considering the circuit is so simple and runs on a breadboard! Furthermore, the schematics and custom software are all [open-sourced on my github](https://github.com/swharden/diyECG-1opAmp/)!

![](https://www.youtube.com/embed/AfirWls9Sys)

__Here's a video demonstrating how the output is shown in real time with custom Python software.__ The video is quite long, but you can see the device in action immediately, so even if you only watch the first few seconds you will see this circuit in action with the custom software. In short, the amplifier circuit (described in detail below) outputs to the computer's microphone and a Python script I wrote analyzes the audio data, performs low-pass filtering, and graphs the output in real time. The result is a live electrocardiograph!

<div class="text-center">

![](https://swharden.com/static/2016/08/08/ECG_1470609065.png)

</div>

### ECG Circuit

<div class="text-center">

![](https://swharden.com/static/2016/08/08/circuit.jpg)

</div>

__The circuit is simple, but a lot of time and thought and experimentation went into it.__ I settled on this design because it produced the best and most reliable results, and it has a few nuances which might not be obvious at first. Although I discuss it in detail in the video, here are the highlights:

*   The output goes to the microphone jack of your computer.
*   There's nothing special about the op-amp I used ([LM741](http://www.ti.com/lit/ds/symlink/lm741.pdf)). A single unit of an [LM324](http://www.ti.com.cn/cn/lit/ds/symlink/lm2902-n.pdf) (or any general purpose op-amp) should work just as well.
*   Resistor values were chosen because I had them on hand. You can probably change them a lot as long as they're in the same ballpark of the values shown here. Just make sure R1 and R2 are matched, and R3 should be at least 10MOhm.
*   <span style="color: #ff0000;">Do not use a bench power supply!</span> "BAT+" and "BAT-" are the leads of a single 9V battery.
*   Note that the leg electrode is ground (same ground as the computer's microphone ground)
*   R5 and R4 form a traditional voltage divider like you'd expect for an op-amp with a gain of about 50.

    *   You'd expect R4 to connect to ground, but since your body is grounded, chest 2 is essentially the same

    *   R3 must be extremely high value, but it pulls your body potential near the optimal input voltage for amplification by the op-amp.

    *   R1 and R2 split the 9V battery's voltage in half and center it at ground, creating -4.5V and +4.5V.

*   altogether, your body stays grounded, and the op-amp becomes powered by -4.5V and +4.5V, and your body is conveniently near the middle and ready to have small signals from CHEST1 amplified. Amplification is with respect to CHEST2 (roughly ground), rather than actual ground, so that a lot of noise (with respect to ground) is eliminated.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/08/IMG_7574.jpg)

</div>

__For those of you who would rather see a picture than a schematic__, here's a diagram of how to assemble it graphically. This should be very easy to reproduce. Although breadboards are typically not recommended for small signal amplification projects, there is so much noise already in these signals that it doesn't really matter much either way. Check out how good the signals look in my video, and consider that I use a breadboard the entire time.

<div class="text-center">

![](https://swharden.com/static/2016/08/08/design.jpg)

</div>

__The most comfortable electrodes I used were made for muscle simulators.__ A friend of mine showed me some muscle stimulator pads he got for a back pain relief device he uses. As soon as I saw those pads, I immediately thought they would be perfect for building an ECG! They're a little bit expensive, but very comfortable, reusable, last a long time, and produce brilliant results. They also have 3.5 mm (headphone jack) connectors which is perfect for DIY projects. On Amazon.com you can get 16 pads for $11 with free shipping. I decided not to include links, because sometimes the pads and cords are sold separately, and sometimes they have barrel connectors and sometimes they have snap connectors. Just get any adhesive reusable electrodes intended for [transcutaneous electrical nerve stimulation (TENS)](https://en.wikipedia.org/wiki/Transcutaneous_electrical_nerve_stimulation) that you can find! They should all work fine.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/08/IMG_7576.jpg)

</div>

### Pennies as Electrodes

__You can make your own electrodes for $0.03!__ Okay that's a terrible joke, but it's true. I made not-awful electrodes by soldering wires to copper pennies, adding strength by super-gluing the wire to the penny, and using electrical tape to attach them to my chest. Unless you want a tattoo of an old guy's face on your torso, wait until they cool sufficiently after soldering before proceeding to the adhesion step. I suspect that super gluing the penny to your chest would also work, but please do not do this. Ironically, because the adhesive pads of the TENS electrodes wear away over time, the penny solution is probably "more reusable" than the commercial electrode option.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/08/08/IMG_7527.jpg)
![](https://swharden.com/static/2016/08/08/IMG_7570-1.jpg)

</div>

This ECG was recorded using pennies as electrodes:

<div class="text-center">

![](https://swharden.com/static/2016/08/08/ECG_1470611901.png)

</div>

__Notes on filtering:__ Why didn't I just use a [hardware low-pass filter](https://en.wikipedia.org/wiki/Low-pass_filter)?

1.   It would have required extra components, which goes against the theme of this project
2.   It would require _specific value_ components, which is also undesirable for a junkbox project
3.   I'm partial to the [Chebyshev filter](https://en.wikipedia.org/wiki/Chebyshev_filter), but getting an extremely sharp roll-off a few Hz shy of 50Hz would take multiple poles (of closely matched passive components) and [not be as trivial as it sounds](http://www.analog.com/library/analogDialogue/archives/43-09/EDCh%208%20filter.pdf?doc=ADA4661-2.pdf).

__Notes on software:__ This a really cool use of Python! I lean on some of my favorite packages [numpy](http://www.numpy.org/), [scipy](https://www.scipy.org/), [matplotlib](http://matplotlib.org/), [pyqrgraph](http://www.pyqtgraph.org/), and [PyQt4](https://wiki.python.org/moin/PyQt4). I've recently made posts describing how to perform real-time data graphing in Python using these libraries, so I won't go into that here. If you're interested, check out my [real-time audio monitor](https://www.swharden.com/wp/2016-07-31-real-time-audio-monitor-with-pyqt/), notes on using [PlotWidget](https://www.swharden.com/wp/2016-07-31-live-data-in-pyqt4-with-plotwidget/), and notes on using [MatPlotLib widget](https://www.swharden.com/wp/2016-07-30-live-data-in-pyqt4-with-matplotlibwidget/). I tried using [PyInstaller](http://www.pyinstaller.org/) to package this project into a single .EXE for all my windows readers who might want to recreate this project, but the resulting EXE was over 160MB! That's crazy! It makes sense considering packagers like PyInstaller and Py2EXE work by building your entire python interpreter and all imported libraries. With all those fun libraries I listed above, it's no wonder it came out so huge. It may be convenient for local quick-fixes, but not a good way to distribute code over the internet. To use this software, just run it in Python. It was tested to work with out-of-the-box [WinPython-64bit-3.5.2.1](https://sourceforge.net/projects/winpython/files/) (not the Qt5 version), so if you want to run it yourself start there.

__Notes on safety.__ How safe is this project? I'm conflicted on this subject. I want to be as conservative as I can (leaning on the side of caution), but I also want to be as realistic as possible. I'm going to play it safe and say "this may not be safe, so don't build or use it". As an exercise, let's consider the pros and cons:

*   __PROS:__

    *   It's powered from a 9V battery which is safer than a bench power supply (but see the matching con).
    *   The only connections to your body are:

        *   leg - ground. you ground yourself all the time. using a wrist grounding strap is the same thing.
        *   chest 1 - extremely high impedance. You're attaching your chest to the high impedance input of an op-amp (which I feel fine with), and also to a floating battery through a 10MOhm resistor (which also I feel fine with)
        *   chest 2 - raises an eyebrow. In addition to a high impedance input, you're connected to an op-amp through a 100k resistor. Even if the op-amp were putting out a full 4.5V, that's 0.045mA (which doesn't concern me a whole lot).

    *   I don't know where to stick this, but I wonder what type of voltages / currents [TENS](https://en.wikipedia.org/wiki/Transcutaneous_electrical_nerve_stimulation) actually provide.

*   __CONS / WARNINGS:__

    *   It's powered from a 9V battery. So are many stun guns.
    *   If the op-amp oscillates, oscillations may enter your body. Personally I feel this may be the most concerning issue.
    *   Small currents can kill. I found a [curiously colored website](https://www.physics.ohio-state.edu/~p616/safety/fatal_current.html) that describes this. It seems like the most dangerous potential effect is induction of cardiac fibrillation, which can occur around 100mA.

__Improving safety through optical isolation:__ The safety of this device may be improved (albeit with increased complexity) through the implementation of [opto-isolators](https://en.wikipedia.org/wiki/Opto-isolator). I may consider a follow-up post demonstrating how I do this. Unlike digital signals which I've [optically isolated before](https://www.swharden.com/wp/2016-07-28-opto-isolated-laser-controller-build/), I've never personally isolated analog signals. Although I'm sure there are fully analog means to do this, I suspect I'd accomplish it by turning it into a digital signal (with a voltage-to-frequency converter), pulsing the output across the optoisolator, and turning it back into voltage with a frequency-to-voltage converter or perhaps even a passive low-pass filter. Analog Devices has a good write-up about [optical isolation techniques](http://www.analog.com/media/en/training-seminars/tutorials/MT-071.pdf).

__Do you have comments regarding the safety of this device?__ Write your thoughts concisely and send them to me in an email! I'd be happy to share your knowledge with everyone by posting it here.

__Did you build this or a device similar to it?__ Send me some pictures! I'll post them here.

__Source code and project files:__ <https://github.com/swharden/diyECG-1opAmp/>

___LEGAL__: This website is for educational purposes only. Do not build or use any electrical devices shown. Attaching non-compliant electronic devices to your body may be dangerous. Consult a physician regarding proper usage of medical equipment._