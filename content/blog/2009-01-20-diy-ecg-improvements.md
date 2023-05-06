---
title: DIY ECG Improvements
date: 2009-01-20 00:53:00
tags: ["diyECG"]
---

# DIY ECG Improvements

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

Instead of using a [single op-amp circuit](http://www.swharden.com/blog/images/opampecg.gif) like the previous entries which gave me [decent but staticky](http://www.swharden.com/blog/images/diy_ecg4.png) traces, I decided to build [a more advanced ECG circuit](http://www.eng.utah.edu/~jnguyen/ecg/bigsch.gif) documented by [Jason Nguyen](http://www.eng.utah.edu/~jnguyen/ecg/ecg_index.html) which used 6 op amps! (I'd only been using one). Luckily I got a few couple LM324 quad op-amps from radioshack ($1.40 each), so I had everything I needed.

<div class="text-center img-border">

[![](https://swharden.com/static/2009/01/20/08-01-19-410_thumb.jpg)](https://swharden.com/static/2009/01/20/08-01-19-410.jpg)

</div>

The results look great! Noise is almost zero, so true details of the trace are visible. I can now clearly see the [PQRST](http://www.vanth.org/vibes/images/normalECG2.PNG) features in the wave. I'll detail how I did this in a later entry. For now, here are some photos of the little device.

<div class="text-center">

[![](https://swharden.com/static/2009/01/20/nicetwopng_thumb.jpg)](https://swharden.com/static/2009/01/20/nicetwopng.png)

</div>

__UPDATE:__ After analyzing ~20 minutes of heartbeat data I found a peculiarity. Technically this could be some kind of noise (a 'pop' in the microphone signal), but because this peculiarity happened only once in 20 minutes I'm not ruling out the possibility that this is the first irregular heartbeat I captured with my DIY ECG. Note that single-beat irregularities are common in healthy people, and that this does not alarm me so much as fascinate me.

<div class="text-center">

[![](https://swharden.com/static/2009/01/20/murm2_thumb.jpg)](https://swharden.com/static/2009/01/20/murm2.png)

</div>

