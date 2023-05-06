---
title: "DIY ECG Attempt 1: Failure"
date: 2009-01-14 11:27:37
tags: ["diyECG"]
---

# DIY ECG Attempt 1: Failure

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__I followed-through on yesterday's post__ and actually tried to build an ECG machine. I had a very small amount of time to work on it, so instead of building the fancy circuit (with 6 band-pass filtered op-amps and diodes posted in the previous entry) I built the most crude circuit that would theoretically work.

<div class="text-center img-border">

![](opampecg.gif)

</div>

__I used just one of the 4 available op-amps from a LM324.__ I built this, hooked it up to my sound card, and made electrodes by soldering wires to pennies. After a good lick, I attached the pennies to my chest with tape and tried recording. Every time the pennies made contact with my skin, I would see noise on the trace, but I couldn't seem to isolate a strong heartbeat signal. This is what I saw and the circuit I build to see it:

<div class="text-center img-border">

[![](noise_thumb.jpg)](noise.png)

</div>

__Perhaps this project will be working soon.__ Many techno-savvy people have made these DIY ECG machines, but not many describe how to interpret the data. Since I'm planning on building it, testing it, recording ECG data, and processing/analyzing it, I'll may have something unique on the internet.

