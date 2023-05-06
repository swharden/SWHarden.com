---
title: IoT Festivus Pole
date: 2017-12-19 22:11:17
tags: ["circuit", "microcontroller"]
---

# IoT Festivus Pole

The <em>Internet of Things</em> now includes Festivus poles! **Festivus is a holiday celebrated on December 23rd, and its [customary practices](https://en.wikipedia.org/wiki/Festivus) include a Festivus pole, Festivus dinner, airing of grievances, feats of strength, and Festivus miracles. The internet contains a few nods to the holiday, including [what happens when you Google for the word Festivus](https://www.google.com/search?q=festivus) (a Festivus pole is displayed at the bottom of the page). In 2015 I had the honor of gifting the world with the first [Festivus pole video game](https://www.swharden.com/wp/2015-12-23-festivus-pole-video-game/), and today I am happy to unveil the world's first internet-enabled Festivus pole. Every time somebody tweets #Festivus or #FestivusMiracle, the light at the top of the pole illuminates! All in the room then excitedly exclaim, "it's a Festivus miracle!"

<div class="text-center img-border img-small">

![](https://swharden.com/static/2017/12/19/723.jpg)

</div>

__The IoT Festivus Pole is powered by a Raspberry Pi__ (a Pi 2 Model B, although any Pi would work) running a Python script which occasionally checks for tweets using the [twitter API](https://developer.twitter.com/en/docs) (via [twython](https://github.com/ryanmcgrath/twython), a pure-python twitter API wrapper) and controls the GPIO pin 12 with [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) ([extra docs](https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api)). After writing the Python script (which should work identically in Python 2 or Python 3), I got it to run automatically every time the system boots by adding a line to /etc/rc.local (surrounding it with parentheses and terminating the line with & to allow it to run without blocking the startup sequence). The LED was added to the end of a long wire (with a series 220-ohm resistor) and connected across the [Raspberry Pi header](https://pinout.xyz) pins 12 (PWM) and 14 (GND). I set PWM frequency to 100 Hz, but this is easily configurable in software.

<div class="text-center img-small">

![](https://swharden.com/static/2017/12/19/festivus_miracle.gif)
![](https://swharden.com/static/2017/12/19/729.jpeg)

</div>

__To build the Festivus pole__ I got a piece of wood and a steel conduit pipe from Lowe's (total <$5). Festivus purists will argue that Festivus poles should be made from aluminum (with its very high strength to weight ratio). I live in an apartment and don't have a garage, so my tool selection is limited. I cut the wood a few times with a jigsaw and glued it together to make an impressive stand similar to those of [traditional Festivus poles](https://en.wikipedia.org/wiki/Festivus). I have a few hole saw drill bits, but none of them perfectly matched the size of the pipe. I traced the outline of the pipe on the wood and cut-out a circular piece with a Dremel drill press in combination with a side-cutting bit. The hole was slightly larger than required for the pipe, so I used a few layers of electrical tape on the bottom of the pipe to "seal" the base of the pipe into the hole, then poured acrylic epoxy into the empty space. Clamping it against a desk allowed the epoxy to set such that the pole was rigidly upright, and the result was a fantastic-looking Festivus pole! It's a bit smaller in size than the famous one featured in Seinfeld, but I think it is appropriately sized for my apartment.

<div class="text-center img-border">

![](https://swharden.com/static/2017/12/19/725.jpg)
![](https://swharden.com/static/2017/12/19/726.jpg)

</div>

__Adding the computer was easy!__ Internet capability was provided via a USB WiFi card. Code is at the bottom of this page. The LED was connected to [Raspberry Pi header](https://pinout.xyz) pins 12 and 14. The wiring was snaked through the conduit.

<div class="text-center img-border">

![](https://swharden.com/static/2017/12/19/728.jpg)
![](https://swharden.com/static/2017/12/19/719.jpg)
![](https://swharden.com/static/2017/12/19/726.jpg)

</div>

__The code will work on Python 2 and Python 3.__
Pip can be used to install RPi.GPIO and twython: `` pip install python-dev python-rpi.gpio twython ``

```python
import RPi.GPIO as GPIO
import time
from twython import Twython

APP_KEY = 'zSNYBNWHmXhU3CX765HnoQEbm'
APP_SECRET = 'getYourOwnApiKeyFromTwitterWebsite'
twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 100)
p.start(0)

if __name__=="__main__":
    tweetLast=0
    checkLast=0
    duty=100

    while True:
        if (checkLast+5)<time.time():
            checkLast=time.time()
            print("checking twitter...")
            tweetLatest=twitter.search(q='festivus')["statuses"][0]["created_at"]
            if tweetLatest!=tweetLast:
                print("IT'S A FESTIVUS MIRACLE!")
                tweetLast=tweetLatest
                duty=100
            else:
                print('nothing')

        if duty>=0:
            p.ChangeDutyCycle(duty)

        time.sleep(.3)
        duty-=1

```

__This Festivus pole has been up and running for the last few days__ and I'm excited to see how much joy it has brought into my household! Admittedly the Raspberry Pi seems to be overkill, but at the time I was considering having it also output audio every time a tweet is made but I never decided on the clip to use so I omitted the feature. An [ESP8266 WiFi module](https://www.sparkfun.com/products/13678) interfaced with a microntroller can do the same job with more elegance and lower cost, so I may consider improving it next year. Until then, Happy Festivus!

![](https://www.youtube.com/embed/HX55AzGku5Y)