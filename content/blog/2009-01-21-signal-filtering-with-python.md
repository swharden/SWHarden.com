---
title: Signal Filtering with Python
date: 2009-01-21 16:25:04
tags: ["diyECG", "python", "obsolete"]
---



> **⚠️ SEE UPDATED POST:** [**Signal Filtering in Python**](https://swharden.com/blog/2020-09-23-signal-filtering-in-python/)

I've been spending a lot of time creating a [DIY ECGs](https://swharden.com/blog/tags/#diyecg) which produce fairly noisy signals. I have researched the ways to clean-up these signals, and the results are very useful! I document some of these findings here.

<div class="text-center">

![](https://swharden.com/static/2009/01/21/filtering.png)

</div>

__This example shows how I take__ __a noisy recording and turn it into a smooth trace. __This is achieved by eliminating excess high-frequency components which are in the original recording due to electromagnetic noise. A major source of noise can be from the AC passing through wires traveling through the walls of my apartment. My [original ECG circuit](https://swharden.com/static/2009/01/14/opampecg.gif) was highly susceptible to this kind of interference, but my [improved ECG circuit](https://swharden.com/static/2009/01/13/bigsch.gif) eliminates much of this noise. However, noise is still in the trace and it needs to be removed.

__One method of reducing noise uses the FFT (Fast Fourier Transformation) and its inverse (iFFT) algorithm__. Let's say you have a trace with repeating sine-wave noise. The output of the FFT is the breakdown of the signal by frequency. Check out [this FFT trace of a noisy signal](https://swharden.com/static/2009/01/15/diy_ecg4.png) from a few posts ago. High peaks represent frequencies which are common. See the enormous peak around 60 Hz? That's noise from AC power lines. Other peaks (shown in colored bands) are other electromagnetic noise sources, such as wireless networks, TVs, telephones, and maybe my computer. The heart produces changes in electricity that are very slow (a heartbeat is about 1 Hz), so if we can eliminate higher-frequency sine waves we can get a pretty clear trace. This is called a band-stop filter (we block-out certain bands of frequencies). A band-pass filter is the opposite, where we only allow frequencies which are below (low-pass) or above (high-pass) a given frequency. By eliminating each of the peaks in the colored regions (setting each value to 0), then performing an inverse fast Fourier transformation (going backwards from frequency back to time), the result is the signal trace (seen as light gray on the bottom graph) with those high-frequency sine waves removed! (the gray trace on the bottom graph). A little touch-up smoothing makes a great trace (black trace on the bottom graph).

__Here's some Python code you may find useful.__ The image below is the output of the Python code at the bottom of this entry. This python file requires that [ecg.wav](https://swharden.com/static/2009/01/21/ecg.wav) (an actual ECG recording of my heartbeat) exist in the same folder.

![](https://swharden.com/static/2009/01/21/sig.png)

*   (A) The original signal we want to isolate. (IE: our actual heart signal)
*   (B) Some electrical noise. (3 sine waves of different amplitudes and periods)
*   (C) Electrical noise (what happens when you add those 3 sine waves together)
*   (D) Static (random noise generated by a random number generator)
*   (E) Signal (A) plus static (D)
*   (F) Signal (A) plus static (D) plus electrical noise (C)
*   (G) Total FFT trace of (F). Note the low frequency peak due to the signal and electrical noise (near 0) and the high frequency peak due to static (near 10,000)
*   (H) This is a zoomed-in region of (F) showing 4 peaks (one for the original signal and 3 for high frequency noise). By blocking-out (set it to 0) everything above 10Hz (red), we isolate the peak we want (signal). This is a low-pass filter.
*   (I) Performing an inverse FFT (iFFT) on the low-pass iFFT, we get a nice trace which is our original signal!
*   (J) Comparison of our iFFT with our original signal shows that the amplitude is kinda messed up. If we normalize each of these (set minimum to 0, maximum to 1) they line up. Awesome!
*   (K) How close were we? Graphing the difference of iFFT and the original signal shows that usually we're not far off. The ends are a problem though, but if our data analysis trims off these ends then our center looks great.

*   _Note: these ends can be fixed by applying a windowing function to the original data. The FFT works best if the input data starts and ends at zero._

```python
import numpy, scipy, pylab, random

# This script demonstrates how to use band-pass (low-pass)
# filtering to eliminate electrical noise and static
# from signal data!

##################
### PROCESSING ###
##################

xs=numpy.arange(1,100,.01) #generate Xs (0.00,0.01,0.02,0.03,...,100.0)
signal = sin1=numpy.sin(xs*.3) #(A)
sin1=numpy.sin(xs) # (B) sin1
sin2=numpy.sin(xs*2.33)*.333 # (B) sin2
sin3=numpy.sin(xs*2.77)*.777 # (B) sin3
noise=sin1+sin2+sin3 # (C)
static = (numpy.random.random_sample((len(xs)))-.5)*.2 # (D)
sigstat=static+signal # (E)
rawsignal=sigstat+noise # (F)
fft=scipy.fft(rawsignal) # (G) and (H)
bp=fft[:]
for i in range(len(bp)): # (H-red)
    if i&gt;=10:bp[i]=0
ibp=scipy.ifft(bp) # (I), (J), (K) and (L)

################
### GRAPHING ###
################

h,w=6,2
pylab.figure(figsize=(12,9))
pylab.subplots_adjust(hspace=.7)

pylab.subplot(h,w,1);pylab.title("(A) Original Signal")
pylab.plot(xs,signal)

pylab.subplot(h,w,3);pylab.title("(B) Electrical Noise Sources (3 Sine Waves)")
pylab.plot(xs,sin1,label="sin1")
pylab.plot(xs,sin2,label="sin2")
pylab.plot(xs,sin3,label="sin3")
pylab.legend()

pylab.subplot(h,w,5);pylab.title("(C) Electrical Noise (3 sine waves added together)")
pylab.plot(xs,noise)

pylab.subplot(h,w,7);pylab.title("(D) Static (random noise)")
pylab.plot(xs,static)
pylab.axis([None,None,-1,1])

pylab.subplot(h,w,9);pylab.title("(E) Signal + Static")
pylab.plot(xs,sigstat)

pylab.subplot(h,w,11);pylab.title("(F) Recording (Signal + Static + Electrical Noise)")
pylab.plot(xs,rawsignal)

pylab.subplot(h,w,2);pylab.title("(G) FFT of Recording")
fft=scipy.fft(rawsignal)
pylab.plot(abs(fft))
pylab.text(200,3000,"signals",verticalalignment='top')
pylab.text(9500,3000,"static",verticalalignment='top',
        horizontalalignment='right')

pylab.subplot(h,w,4);pylab.title("(H) Low-Pass FFT")
pylab.plot(abs(fft))
pylab.text(17,3000,"sin1",verticalalignment='top',horizontalalignment='left')
pylab.text(37,2000,"sin2",verticalalignment='top',horizontalalignment='center')
pylab.text(45,3000,"sin3",verticalalignment='top',horizontalalignment='left')
pylab.text(6,3000,"signal",verticalalignment='top',horizontalalignment='left')
pylab.axvspan(10,10000,fc='r',alpha='.5')
pylab.axis([0,60,None,None])

pylab.subplot(h,w,6);pylab.title("(I) Inverse FFT")
pylab.plot(ibp)

pylab.subplot(h,w,8);pylab.title("(J) Signal vs. iFFT")
pylab.plot(signal,'k',label="signal",alpha=.5)
pylab.plot(ibp,'b',label="ifft",alpha=.5)

pylab.subplot(h,w,10);pylab.title("(K) Normalized Signal vs. iFFT")
pylab.plot(signal/max(signal),'k',label="signal",alpha=.5)
pylab.plot(ibp/max(ibp),'b',label="ifft",alpha=.5)

pylab.subplot(h,w,12);pylab.title("(L) Difference / Error")
pylab.plot(signal/max(signal)-ibp/max(ibp),'k')

pylab.savefig("SIG.png",dpi=200)
pylab.show()
```

