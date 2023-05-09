---
title: "PySquelch: A Python-Based Frequency Audio Activity Monitor"
date: 2009-07-26 00:22:12
tags: ["python", "obsolete"]
---



__I'm pretty much done with this project so it's time to formally document it.__  This project is a collaboration between Fred, [KJ4LFJ](http://www.qrz.com/kj4lfj) who supplied the hardware and myself, Scott, [KJ4LDF](http://www.qrz.com/kj4ldf) who supplied the software.  Briefly, a scanner is set to a single frequency (147.120 MHz, the output of an [active repeater ](http://www.147120.com/) in Orlando, FL) and the audio output is fed into the microphone hole of a PC sound card.  The scripts below (run in the order they appear) detect audio activity, log the data, and display such data graphically.  

Here is some sample output:

<div class="text-center">

![](https://swharden.com/static/2009/07/26/test_24hr-1.png)
![](https://swharden.com/static/2009/07/26/test_average.png)
![](https://swharden.com/static/2009/07/26/test_alltime-1.png)
![](https://swharden.com/static/2009/07/26/test_60min.png)

</div>

__Live-running software is current available at: [Fred's Site](http://kj4lfj.dyndns.org/147120/stream-data/pySquelch.html)__. The most current code can be found in its working directory.  For archival purposes, I'll provide [the code for pySquelch in ZIP format](http://www.SWHarden.com/blog/images/pysquelch.zip).  Now, onto other things...