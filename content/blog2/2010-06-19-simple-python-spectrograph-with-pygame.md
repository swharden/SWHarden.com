---
title: Simple Python Spectrograph with PyGame
date: 2010-06-19 21:53:25
tags: ["python", "old"]
---

# Simple Python Spectrograph with PyGame

<b style="font-size: inherit;">While thinking of ways to improve my QRSS VD high-definitions spectrograph software,</b><span style="font-size: inherit;"> I often wish I had a better way to display large spectrographs. Currently I'm using PIL (the Python Imaging Library) with TK and it's slow as heck. I looked into the </span><a href="http://www.pygame.org" style="font-size: inherit;">PyGame</a><span style="font-size: inherit;"> project, and it seems to be designed with speed in mind. I whipped-up this quick demo, and it's a simple case audio spectrograph which takes in audio from your sound card and graphs it time vs. frequency. This method is far superior to the method I was using previously to display the data, because while QRSS VD can only update the entire GUI (500px by 8,000 px) every 3 seconds, early tests with PyGame suggests it can do it about 20 times a second (wow!). With less time/CPU going into the GUI, the program can be more responsivle and my software can be less of a drain.</span>

<div class="text-center img-border">

![](https://swharden.com/static/2010/06/19/simple-spectrograph.png)

</div>

</div>

```python
import pygame
import numpy
import threading
import pyaudio
import scipy
import scipy.fftpack
import scipy.io.wavfile
import wave
rate = 12000  # try 5000 for HD data, 48000 for realtime
soundcard = 2
windowWidth = 500
fftsize = 512
currentCol = 0
scooter = []
overlap = 5  # 1 for raw, realtime - 8 or 16 for high-definition


def graphFFT(pcm):
    global currentCol, data
    ffty = scipy.fftpack.fft(pcm)  # convert WAV to FFT
    ffty = abs(ffty[0:len(ffty)/2])/500  # FFT is mirror-imaged
    # ffty=(scipy.log(ffty))*30-50 # if you want uniform data
    print "MIN:t%stMAX:t%s" % (min(ffty), max(ffty))
    for i in range(len(ffty)):
        if ffty[i] < 0:
            ffty[i] = 0
        if ffty[i] > 255:
            ffty[i] = 255
    scooter.append(ffty)
    if len(scooter) < 6:
        return
    scooter.pop(0)
    ffty = (scooter[0]+scooter[1]*2+scooter[2]*3+scooter[3]*2+scooter[4])/9
    data = numpy.roll(data, -1, 0)
    data[-1] = ffty[::-1]
    currentCol += 1
    if currentCol == windowWidth:
        currentCol = 0


def record():
    p = pyaudio.PyAudio()
    inStream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                      input_device_index=soundcard, input=True)
    linear = [0]*fftsize
    while True:
        linear = linear[fftsize/overlap:]
        pcm = numpy.fromstring(inStream.read(
            fftsize/overlap), dtype=numpy.int16)
        linear = numpy.append(linear, pcm)
        graphFFT(linear)


pal = [(max((x-128)*2, 0), x, min(x*2, 255)) for x in xrange(256)]
print max(pal), min(pal)
data = numpy.array(numpy.zeros((windowWidth, fftsize/2)), dtype=int)
# data=Numeric.array(data) # for older PyGame that requires Numeric
pygame.init()  # crank up PyGame
pygame.display.set_caption("Simple Spectrograph")
screen = pygame.display.set_mode((windowWidth, fftsize/2))
world = pygame.Surface((windowWidth, fftsize/2), depth=8)  # MAIN SURFACE
world.set_palette(pal)
t_rec = threading.Thread(target=record)  # make thread for record()
t_rec.daemon = True  # daemon mode forces thread to quit with program
t_rec.start()  # launch thread
clk = pygame.time.Clock()
while 1:
    for event in pygame.event.get():  # check if we need to exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.surfarray.blit_array(world, data)  # place data in window
    screen.blit(world, (0, 0))
    pygame.display.flip()  # RENDER WINDOW
    clk.tick(30)  # limit to 30FPS
```

