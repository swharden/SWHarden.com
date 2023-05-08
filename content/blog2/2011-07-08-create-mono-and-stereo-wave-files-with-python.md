---
title: Create Mono and Stereo Wave Files with Python
date: 2011-07-08 09:22:04
tags: ["python", "old"]
---

# Create Mono and Stereo Wave Files with Python

__My current project involves needing to create stereo audio in real time__ with Python. I'm using PyAudio to send the audio data to the sound card, but in this simple example I demonstrate how to create mono and stereo sounds with Python. I'm disappointed there aren't good simple case examples on the internet, so I'm sharing my own. It doesn't get much easier than this!

### Python 2

```python
from struct import pack
from math import sin, pi
import wave
import random

RATE=44100

## GENERATE MONO FILE ##
wv = wave.open('test_mono.wav', 'w')
wv.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=2**15-1.0 #maximum amplitude
wvData=""
for i in range(0, RATE*3):
    wvData+=pack('h', maxVol*sin(i*500.0/RATE)) #500Hz
wv.writeframes(wvData)
wv.close()

## GENERATE STERIO FILE ##
wv = wave.open('test_stereo.wav', 'w')
wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=2**15-1.0 #maximum amplitude
wvData=""
for i in range(0, RATE*3):
    wvData+=pack('h', maxVol*sin(i*500.0/RATE)) #500Hz left
    wvData+=pack('h', maxVol*sin(i*200.0/RATE)) #200Hz right
wv.writeframes(wvData)
wv.close()
```

__The output__ is two sound files which look like this:

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/08/mono.png)

![](https://swharden.com/static/2011/07/08/stereo.png)

</div>

### Python 3

```python
from struct import pack
from math import sin, pi
import wave
import random
from os.path import abspath

# create a bytestring containing "short" (2-byte) sine values
SAMPLE_RATE = 44100
waveData = b''
maxVol = 2**15-1.0
frequencyHz = 500.0
fileLengthSeconds = 3
for i in range(0, SAMPLE_RATE * fileLengthSeconds):
    pcmValue = sin(i*frequencyHz/SAMPLE_RATE * pi * 2)
    pcmValue = int(maxVol*pcmValue)
    waveData += pack('h', pcmValue)

# save the bytestring as a wave file
outputFileName = 'output.wav'
wv = wave.open(outputFileName, 'w')
wv.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
wv.writeframes(waveData)
wv.close()
print(f"saved {abspath(outputFileName)}")
```

