---
title: High School Students' High Altitude Balloon #2
date: 2011-08-14 18:36:12
tags: ["amateur radio"]
---



__Last year a group of high school students,__ in collaboration with a seminar course on Space Systems sponsored by the University of Florida's [Student Science Training Program (SSTP)](http://www.cpet.ufl.edu/sstp/default.html), gained some real-world experience planning, building, and launching a research payload to the edge of space – all in a couple weeks!  Last year's high altitude balloon launch was [covered on my website](http://www.swharden.com/blog/2010-07-14-high-altitude-balloon-transmitter/), and the radio transmitter I built for it was featured on [this Hack-A-Day post](http://hackaday.com/2010/07/27/200-mile-rf-transmitter-and-high-altitude-balloon/). Unlike last year's payload, whose only homebrew device was the radio transmitter, this year's payload had equipment we assembled ourselves, and instead of launching from NASA we launched from the UF football stadium! There were a couple problems along the way, and the payload hasn't been recovered (yet), but it was a fun project and we all learned a lot along the way!

**Update:** [project video](http://vimeo.com/27447092)

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/group.jpg)

</div>

Below is a panoramic photo right before the launch - see our balloon on the right? So cool!

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/pan.jpg)

</div>

__Our goal was to take photos from the edge of space, and log temperature, pressure, humidity, and GPS coordinates along the way.__ On-board were a radio transmitter, an Arduino with a GPS shield, and an Android phone to take pictures every few seconds.

__Android details:__ Most of the Android development was handled by UF student Richard along with high school students Benji, Tyler, Michael, and Kevin. Their GitHub project is here:<https://github.com/rich90usa/AndroidSensorLogger>. Also note that the automatic photo capture utilized [Photo Log Lite](http://www.appbrain.com/app/photo-log-lite/com.keepknocking.PhotoLogLite). We also used [GPSLogger](http://mendhak.github.com/gpslogger/") to handle logging GPS to SD. _"Both of these programs were chosen for their ability to run in the background - and do so reliably by using the 'correct' Android supported methods of doing so." -- Richard_

>  Our code used the phone's text-to-speech engine to speak out an encoded version of every 90th new GPS coordinate. The data was encoded by connecting every number (0-9) to a word the [NATO phonetic alphabet](http://en.wikipedia.org/wiki/NATO_phonetic_alphabet). The code also used text-to-speech to have the phone speak out the phone's altitude data. --Benji

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/DSC_6013.jpg)
![](https://swharden.com/static/2011/08/14/IMG_2095.jpg)

</div>

__The device consisted of 4 main components:__ a payload (the styrofoam box in which all of the electrical equipment was housed), a radar reflector (hanging off the bottom of the payload, to help make this object visible to aircraft), a parachute (at the top, made of bio-degradable plastic), and the balloon itself which measured about 6 feet wide when inflated at ground level (supposedly it reaches approximately 30 feet wide at high altitudes before it bursts).  Once the balloon bursts, the parachute fills with air and the device floats back to earth.

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/DSC_6009.jpg)

</div>

__Kunal demonstrates the__ effectiveness of our parachute with a scientific "run test"!

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/DSC_6015.jpg)

</div>

__The radio communication system we used this year__ were a little more commercial than last year. Due to my limited time availability (I had an oral surgery rotation all week the week before launch), I chose to get something pre-packaged. My intent was to use FRS (those little 500mW family radio service radios) to send GPS data back to earth, but I later (after launch) did a little more research and realized that it probably wasn't the most legal way to do it. However, it was extremely cost effective (amateur radio transmitters and RF transmitter modules are quite pricey). For about the cost of a pizza, we were able to interface a FRS radio to the android phone, and the phone ran a program which polled its GPS, turned coordinates into NATO letter abbreviations, and spoke them through the speaker line. The FRS radio with VOX (voice operated transmit) sensed audio and transmitted accordingly. Although it worked very well, I later learned that this may not have been legal in the US because, although FRS doesn't require a user license and is legal to use anywhere as long as you use its stock antenna, I violated the rule that it cannot be operated above a certain height (20m I think?). Note that this should not be replicated, and probably shouldn't have been done in the first place. I know I'll take a lot of heat over this, but it's in the past now and will be done differently in the future.

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/DSC_6016.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6042.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6049.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6071.jpg)

</div>

__Here are some photos right before the launch.__ It was a sunny day at the UF football stadium! The Android phone is taped the the outside of the box and takes pictures every few seconds, storing them on a micro SD card. Inside the box is an Arduino with GPS shield, and the FRS radio transmitter.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2011/08/14/DSC_6079.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6119.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6132.jpg)
![](https://swharden.com/static/2011/08/14/pan.jpg)
![](https://swharden.com/static/2011/08/14/panZoomed.jpg)
![](https://swharden.com/static/2011/08/14/DSC_6145.jpg)

</div>

{{<youtube BozzCpdTJUk>}}

__After launch the balloon ascended at a rate of about 500ft/min.__ It spat out GPS data often, and altitude (not encoded with NATO abbreviations) was the easiest to hear as I walked from the UF football stadium to the UF [Gator Amateur Radio Club](http://gatorradio.org) to use their equipment (namely an AZEL-rotor-controlled 70cm yagi antenna attached to an I-Com 706) to listen in as the balloon ascended... but not before a group photo!

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/DSC_6151.jpg)

</div>

__Here we are in the station... let's get to work!__

{{<youtube 98SHxyvsGB4>}}

<div class="text-center img-border">

![](https://swharden.com/static/2011/08/14/IMG_2118.jpg)

</div>

__The results were a bit disappointing,__ as we believe the Android phone froze/crashed about 10,000 feet in the air! Since that was the device which generated the audio fed into the transmitter, when that phone died, the transmitter stopped transmitting, and we didn't hear anything else from the transmitter ever again!  We included contact information in the payload and it's possible it will be found one day and we will be contacted about it. If this is the case, we'll view the SD cards and see the full GPS log and pictures from the edge of space! Until then, we can only cross our fingers and hope for the best. Either way we had a blast, and learned a lot along the way. Next time we can be better prepared for a solid recovery!

__Here's audio of the device's last words__ when it was about 10,000 feet in the air: [lastwords.mp3](https://swharden.com/static/2011/08/14/lastwords.mp3)

__Overall we had an awesome time!__ I'd like to thank everyone who helped with this project, especially UF students Richard, Kunal, Dante, and all of the SSTP high school students!