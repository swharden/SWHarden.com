---
title: Insights Into FFTs, Imaginary Numbers, and Accurate Spectrographs
date: 2010-06-23 22:21:00
tags: ["qrss", "python", "old"]
---

# Insights Into FFTs, Imaginary Numbers, and Accurate Spectrographs

__I'm attempting to thoroughly re-write the data assessment__ portions of my QRSS VD software, and rather than rushing to code it (like I did last time) I'm working hard on every step trying to optimize the code. I came across some notes I made about Fast Fourier Transformations from the first time I coded the software, and though I'd post some code I found helpful. Of particular satisfaction is an email I received from Alberto, I2PHD, the creator of Argo (the "gold standard" QRSS spectrograph software for Windows). In it he notes:

<blockquote class="wp-block-quote"><p>I think that [it is a mistake to] throw away the imaginary part of the FFT. What I do in Argo, in Spectran, in Winrad, in SDRadio and in all of my other programs is compute the magnitude of the [FFT] signal, then compute the logarithm of it, and only then I do a mapping of the colors on the screen with the result of this last computation.</p><cite> Alberto, I2PHD (the creator of Argo)</cite></blockquote>

> __UPDATE IN SEPTEMBER, 2020 (10 years later):__ I now understand that `magnitude = sqrt(real^2 + imag^2)` and this post is a bit embarrassing to read! Check out my .NET FFT library [FftSharp](https://github.com/swharden/FftSharp) for a more advanced discussion on this topic.

__These concepts are simple__ to visualize when graphed. Here I've written a short Python script to listen to the microphone (which is being fed a 2kHz sine wave), perform the FFT, and graph the real FFT component, imaginary FFT component, and their sum. The output is:

<div class="text-center">

![](https://swharden.com/static/2010/06/23/real_imaginary_fft_pcm.png)

</div>

__Of particular interest__ to me is the beautiful complementary of the two curves. It makes me wonder what types of data can be extracted by the individual curves (or perhaps their difference?) down the road. I wonder if phase measurements would be useful in extracting weak carries from beneath the noise floor?

<div class="text-center">

![](https://swharden.com/static/2010/06/23/fft_base2.png)

</div>

__Here's the code I used to generate the image above.__ Note that my microphone device was set to listen to my stereo output, and I generated a 2kHz sine wave using the command `` speaker-test -t sine -f 2000 `` on a PC running Linux. I hope you find it useful!

```python
import numpy
import pyaudio
import pylab
import numpy

### RECORD AUDIO FROM MICROPHONE ###
rate = 44100
soundcard = 1  # CUSTOMIZE THIS!!!
p = pyaudio.PyAudio()
strm = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
              input_device_index=soundcard, input=True)
strm.read(1024)  # prime the sound card this way
pcm = numpy.fromstring(strm.read(1024), dtype=numpy.int16)

### DO THE FFT ANALYSIS ###
fft = numpy.fft.fft(pcm)
fftr = 10*numpy.log10(abs(fft.real))[:len(pcm)/2]
ffti = 10*numpy.log10(abs(fft.imag))[:len(pcm)/2]
fftb = 10*numpy.log10(numpy.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2]
freq = numpy.fft.fftfreq(numpy.arange(len(pcm)).shape[-1])[:len(pcm)/2]
freq = freq*rate/1000  # make the frequency scale

### GRAPH THIS STUFF ###
pylab.subplot(411)
pylab.title("Original Data")
pylab.grid()
pylab.plot(numpy.arange(len(pcm))/float(rate)*1000, pcm, 'r-', alpha=1)
pylab.xlabel("Time (milliseconds)")
pylab.ylabel("Amplitude")
pylab.subplot(412)
pylab.title("Real FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq, fftr, 'b-', alpha=1)
pylab.subplot(413)
pylab.title("Imaginary FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq, ffti, 'g-', alpha=1)
pylab.subplot(414)
pylab.title("Real+Imaginary FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq, fftb, 'k-', alpha=1)
pylab.show()
```

__After fighting for a while long with__ a "shifty baseline" of the FFT, I came to another understanding. Let me first address the problem. Taking the FFT of different regions of the 2kHz wave I got traces with the peak in the identical location, but the "baselines" completely different.

<div class="text-center">

![](https://swharden.com/static/2010/06/23/fft_base3.png)

</div>

__Like many things, I re-invented the wheel.__ Since I knew the PCM values weren't changing, the only variable was the starting/stopping point of the linear sample. "Hard edges", I imagined, must be the problem. I then wrote the following function to shape the PCM audio like a triangle, silencing the edges and sweeping the volume up toward the middle of the sample:

```python
def shapeTriangle(data):
    triangle=numpy.array(range(len(data)/2)+range(len(data)/2)[::-1])+1
    return data*triangle
```

__After shaping the data BEFORE I applied the FFT,__ I made the subsequent traces MUCH more acceptable. Observe:

__Now that I've done all this experimentation/thinking,__ I remembered that this is nothing new! Everyone talks about shaping the wave to minimize hard edges before taking the FFT. They call it _windowing._ Another case of me re-inventing the wheel because I'm too lazy to read others' work. However, in my defense, I learned a lot by trying all this stuff -- far more than I would have learned simply by copying someone else's code into my script. Experimentation is the key to discovery!
