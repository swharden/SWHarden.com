---
title: Screwy Oscillator Idea
date: 2011-06-02 21:18:47
tags: ["circuit", "amateur radio", "old"]
---

# Screwy Oscillator Idea

__Can you believe it's been almost 3 months since my last post?__ A lot's been going on since then, namely the national board dental exam. I'm happy to report I prepared for it and performed above and beyond my expectations on the exam, and I'm quite satisfied.  The last few weeks were quite a strain on my life in my aspects, and during that time I realized that I didn't appreciate the little things (such as free time) that I would have loved to experience instead of studying. I guess it's the feeling you have when you're really sick and think to yourself "remember this moment so that when you're well again, you can appreciate feeling well". Now that it's all behind me, what do I do?  I sit at my work station, play some [light music](http://www.youtube.com/watch?v=7nmTRZLLO2M), grab an adult beverage, turn on the soldering iron, and make something special.

__I'm resuming work on my simple transmitter/receiver projects,__ but I'm working at the heart of the device and experimenting with oscillator designs. I built various [Colpitts](http://en.wikipedia.org/wiki/Colpitts_oscillator), [Hartley](http://en.wikipedia.org/wiki/Hartley_oscillator), [Clapp](http://en.wikipedia.org/wiki/Clapp_oscillator), and other oscillator designs, and I think I landed on a design I'm most comfortable with replicating. I'm actually creating a voltage controlled oscillator (VCO or VFO), with a frequency that can be adjusted by rotating a dial or two. It's always a balance between stability and tunability for me. I don't want to use polyvaricon variable capacitors (expensive!), and LED-based varactor diode configurations only give me a swing of about 20pf. What did I come up with?

<div class="text-center img-border">

![](https://swharden.com/static/2011/06/02/DSCN1335.jpg)

</div>

__I had tremendous success__ using a variable _inductor_ for coarse tuning! The inductor is nothing more than a screw entering and exiting the center of an air core inductor. I can't claim all the credit, because I got the idea from [this photo](http://www.vk2zay.net/article/45) on one of the coolest websites on the planet, [Alan Yates' Lab](http://www.vk2zay.net). It looks like Alan got the idea from [this](http://www.wa6otp.com/pto.htm) page... This is so useful! Is this common HAM knowledge? Why am I, someone who's been into RF circuitry for a couple of years now, JUST learning about this? I'm documenting it because I haven't seen it out there on the web, and I feel it should be represented more! Here's a video of it in action:

{{<youtube 5JjF8-hjL9E>}}

This is the circuit I was using: 

<div class="text-center img-border">

![](https://swharden.com/static/2011/06/02/DSCN1334.jpg)

</div>

This is what it looked like before the glue or screw: 

<div class="text-center img-border">

![](https://swharden.com/static/2011/06/02/DSCN1307.jpg)

</div>

Here's the variable inductor enveloped in hot glue before it cooled and turned white: 

<div class="text-center img-border">

![](https://swharden.com/static/2011/06/02/DSCN1316.jpg)

</div>

At the end of the day, it looks nice! 


<div class="text-center img-border">

![](https://swharden.com/static/2011/06/02/DSCN1339.jpg)

</div>

__Band changes can be accomplished by__ swapping the capacitor between the inductor and ground. It couldn't be any easier! I'll see if I can build this in a more compact manner...

**UPDATE (2 days later):** Apparently this is called a "Permeability Tuned Oscillator", or PTO. It's an early design for radios (earlier than variable capacitors) and I guess therefore not described often on the internet. Knowing it's official title, searching yielded a few pages describing this action: [Dave, G7UVW](http://webshed.org/wiki/Mercury_PTO) did some analytical measurements using a mercury core!The [Tin Ear](http://www.amqrp.org/kits/tin_ear/index.html) uses a PTO as its primary tuning method (also McDonalds straw?) [This guy](http://www.geocities.ws/k7hkl_arv/PTO_Simplified_Mechanicals.html) made a PTO out of PVC with a nice screw handle! [This PTO](http://www.wa6otp.com/pto.htm) kit seems to be used in many projects.The [Century 21's VFO](http://www.io.com/~n5fc/c21_pto.htm) is a PTO! I love that rig and had no idea it tuned like that... [This guy](http://kd1jv.qrpradio.com/ARRLHBC/ARRL_MMR40.html) used a PTO in his MMR-40 radio.

Someone on Hackaday recommended [This ARRL Challenge winner](http://www.arrl.org/files/file/QST/Homebrew%20Challenge/HBC%201%20Winner-KD1JV.pdf) with an almost identical design as mine!I guess this bright idea was so bright, it was thought of by many people long ago...