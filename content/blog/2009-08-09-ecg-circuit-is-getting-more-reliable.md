---
title: Improving ECG Reliability
date: 2009-08-09 12:25:50
tags: ["diyECG"]
---

# Improving ECG Reliability

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__Although I made a functional ECG circuit__, it was extremely finicky. If you attached the electrodes too weakly (not a good enough connection), you would get no signal. If you attached the electrodes too tightly (too good of a connection), you wouldn't get a signal either. You had to have just the right resistance between the electrodes and the body for them to work. I tried some things and finally discovered that a resistor between the circuit and me (on the ground lead) significantly improved the situation, but requires a really good body connection. My leads (2) were made from wires (non-shielded) with gator clips at the end clamping onto pennies. I added a dab of moisturizer to the pennies to get a really good connection and used electrical tape to attach them to my chest (+) and leg (GND). I recorded heart data in 10 minute blocks, and it worked amazingly well! Here is a video if me recording my ECG while playing [Counter-Strike](http://en.wikipedia.org/wiki/Counter-Strike).

{{<youtube izet7cgtMjU>}}

__If you look closely you can see my heartbeat__ as the two leftmost bars on the display of the laptop. I'm continuing to work on this circuit, and will release details when it's a little more complete. My plan is to write it up formally, provide a ton of examples/documentation, and really dive into the analysis aspect of it (RRI calculations, variability analysis, etc) and post it to Hackaday. DIY ECGs are nothing new, but no one who's made one has really gone deep into its interpretation. My goal is to have this complete by next week! For now, enjoy the pretty videos.