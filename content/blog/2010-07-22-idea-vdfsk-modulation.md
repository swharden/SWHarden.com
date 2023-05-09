---
title: vdFSK Modulation
date: 2010-07-22 12:39:54
tags: ["python", "qrss", "obsolete"]
---



<blockquote class="wp-block-quote"><p>My goal is to create a QRPP (extremely low power) transmitter and modulation method to send QRSS (extremely slow, frequency shifting data) efficiently, able to be decoded visually or with automated image analysis software. This evolving post will document the thought process and development behind AJ4VD's Frequency Shift Keying method, <b>vdFSK</b>.</p></blockquote>

__Briefly, this is what my idea is.__ Rather than standard 2-frequencies (low for space, high for tone) QRSS3 (3 seconds per dot), I eliminate the need for pauses between dots by using 3 frequencies (low for a space between letters, medium for dot, high for dash). The following images compare my call sign (AJ4VD) being sent with the old method, and the vdFSK method.

<div class="text-center img-border">

![](https://swharden.com/static/2010/07/22/traditional.png)

</div>

__Again,__ both of these images say the same thing: AJ4VD, `.- .--- ....- ...- -..` However, note that the above image has greater than a 3 second dot, so it's unfairly long if you look at the time scale. Until I get a more fairly representative image, just appreciate it graphically. It's obviously faster to send 3 frequencies rather than two. In my case, it's over 200% faster.

<div class="text-center img-border">

![](https://swharden.com/static/2010/07/22/modulation.png)

</div>

__This is the code to generate audio files__ converting a string of text into vdFSK audio, saving the output as a WAV file. Spectrographs can be created from these WAV files.

### generate_audio.py

```python
# converts a string into vdFSK audio saved as a WAV file

import numpy
import wave
from morse import *


def makeTone(freq, duration=1, samplerate=5000, shape=True):
    signal = numpy.arange(duration*samplerate) / \
        float(samplerate)*float(freq)*3.14*2
    signal = numpy.sin(signal)*16384
    if shape == True:  # soften edges
        for i in range(100):
            signal[i] = signal[i]*(i/100.0)
            signal[-i] = signal[-i]*(i/100.0)
    ssignal = ''
    for i in range(len(signal)):  # make it binary
        ssignal += wave.struct.pack('h', signal[i])
    return ssignal


def text2tone(msg, base=800, sep=5):
    audio = ''
    mult = 3  # secs per beep
    msg = " "+msg+" "
    for char in msg.lower():
        morse = lookup[char]
        print char, morse
        audio += makeTone(base, mult)
        for step in lookup[char]:
            if step[0] == ".":
                audio += makeTone(base+sep, int(step[1])*mult)
            if step[0] == "-":
                audio += makeTone(base+sep*2, int(step[1])*mult)
            if step[0] == "|":
                audio += makeTone(base, 3*mult)
    return audio


msg = "aj4vd"
file = wave.open('test.wav', 'wb')
file.setparams((1, 2, 5000, 5000*4, 'NONE', 'noncompressed'))
file.writeframes(text2tone(msg))
file.close()

print 'file written'
```

### morse.py

```python
# library for converting between text and Morse code
raw_lookup="""
a.- b-... c-.-. d-.. e. f..-. g--. h.... i.. j.--- k-- l.-.. m--
n-. o--- p.--. q--.- r.-. s... t- u.- v...- w.-- x-..- y-.-- z--..
0----- 1.---- 2..--- 3...-- 4....- 5..... 6-.... 7--... 8---.. 9----.
..-.-.- =-...- :---... ,--..-- /-..-. --....-
""".replace("n","").split(" ")

lookup={}
lookup[" "]=["|1"]
for char in raw_lookup:
    """This is a silly way to do it, but it works."""
    char,code=char[0],char[1:]
    code=code.replace("-----","x15 ")
    code=code.replace("----","x14 ")
    code=code.replace("---","x13 ")
    code=code.replace("--","x12 ")
    code=code.replace("-","x11 ")
    code=code.replace(".....","x05 ")
    code=code.replace("....","x04 ")
    code=code.replace("...","x03 ")
    code=code.replace("..","x02 ")
    code=code.replace(".","x01 ")
    code=code.replace("x0",'.')
    code=code.replace("x1",'-')
    code=code.split(" ")[:-1]
    #print char,code
    lookup[char]=code

```

<div class="text-center img-border">

![](https://swharden.com/static/2010/07/22/produced.png)

</div>

__Automated decoding__ is trivial. The image above was analyzed, turned into the image below, and the string (AJ4VD) was extracted:

### decode.py

```python
# given an image, it finds peaks and pulls data out
from PIL import Image
from PIL import ImageDraw
import pylab
import numpy

pixelSeek = 10
pixelShift = 15


def findPeak(data):
    maxVal = 0
    maxX = 0
    for x in range(len(data)):
        if data[x] > maxVal:
            maxVal, maxX = data[x], x
    return maxX


def peaks2morse(peaks):
    baseFreq = peaks[0]
    lastSignal = peaks[0]
    lastChange = 0
    directions = []
    for i in range(len(peaks)):
        if abs(peaks[i]-baseFreq) < pixelSeek:
            baseFreq = peaks[i]
        if abs(peaks[i]-lastSignal) < pixelSeek and i < len(peaks)-1:
            lastChange += 1
        else:
            if abs(baseFreq-lastSignal) < pixelSeek:
                c = " "
            if abs(baseFreq-lastSignal) < pixelSeek:
                c = " "
            if abs(baseFreq-lastSignal) < pixelSeek:
                c = " "
            directions.append(
                [lastSignal, lastChange, baseFreq, baseFreq-lastSignal])
            lastChange = 0
        lastSignal = peaks[i]
    return directions


def morse2image(directions):
    im = Image.new("L", (300, 100), 0)
    draw = ImageDraw.Draw(im)
    lastx = 0
    for d in directions:
        print d
        draw.line((lastx, d[0], lastx+d[1], d[0]), width=5, fill=255)
        lastx = lastx+d[1]
    im.show()


im = Image.open('raw.png')
pix = im.load()
data = numpy.zeros(im.size)
for x in range(im.size[0]):
    for y in range(im.size[1]):
        data[x][y] = pix[x, y]

peaks = []
for i in range(im.size[0]):
    peaks.append(findPeak(data[i]))

morse = peaks2morse(peaks)
morse2image(morse)
print morse
```

