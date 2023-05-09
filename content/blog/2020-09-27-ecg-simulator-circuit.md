---
title: ECG Simulator Circuit
date: 2020-09-27 17:11:00
tags: ["circuit", "diyECG"]
---



**This page describes a simple circuit which produces ECG-like waveform.** The waveform is not very detailed, but it contains a sharp depolarizing (rising) component, a slower hyperpolarizing (falling) component, and a repetition rate of approximately one beat per second making it potentially useful for testing heartbeat detection circuitry.

**In 2019 I released a [YouTube video](https://www.youtube.com/watch?v=sP_-f5nsOEo) and [blog post](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/) showing how to build an ECG machine** using an AD8232 interfaced to a computer's sound card. At the end of the video I discussed how to use a 555 timer to create a waveform roughly like an ECG signal, but I didn't post the circuit at the end of that video. I get questions about it from time to time, so I'll share my best guess at what that circuit was here using LTSpice to simulate it.

<a href='https://swharden.com/static/2020/09/27/ltspice-ecg-simulator.png'>
<img src='https://swharden.com/static/2020/09/27/ltspice-ecg-simulator.png' class='w-75 d-block mx-auto border shadow'>
</a>

## Design Notes

* The 555 timer generates pulses about once per second.

* The diode (D1) causes the 555 to produce very short pulses. The duty of the pulses is controlled by the resistance in series with the diode (R3), with higher resistances resulting in larger duty.

* The main purpose of the first op-amp is to invert polarity of the signal emitted by the 555. The signal is a square wave at about 1Hz, but it is mostly high with brief low pulses.

* The second op-amp serves as a voltage buffer to stabilize the output, and the final series capacitor shifts the voltage so it's centered around zero.

* Unity gain op-amps should have some feedback resistance to improve small-signal stability in production applications, but for messing around here I felt fine omitting them.

## Resources

* LTSpice file for this project: [ecg.asc](https://swharden.com/static/2020/09/27/ecg.asc)

* You will need the LM741 model found on the [Using MOD Files in LTSpice](https://swharden.com/blog/2020-09-26-ltspice-mod-files/) page

* My [Action Potential Generator Circuit](https://swharden.com/blog/2017-08-12-analog-action-potential-generator-circuit/) and [Microcontroller Action Potential Generator](https://swharden.com/blog/2017-08-20-microcontroller-action-potential-generator/) articles describe method to produce a similar waveform (designed to look more like what firing neurons produce) using transistors to charge/discharge a capacitor rather than op-amps.
