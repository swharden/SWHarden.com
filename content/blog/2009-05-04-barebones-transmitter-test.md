---
title: AM Transmitter Test
date: 2009-05-04 22:09:13
---

# AM Transmitter Test

__I put the transmitter from the previous post to the test.__ I changed the circuitry a bit though. I kept the oscillator (50 MHz) is now continuously powered. I programmed the ATTiny 2313 microcontroller (using PWM output) to send an oscillating signal to the base of a transistor (NPN). In this way the microcontroller PWM output didn't supply power to the oscillator, but rather grounded it. I got a big boost in range this way. Yesterday I couldn't even hear the signal in the parking lot of my apartment, whereas today I heard it loud and clear. I decided to take a drive with my scanner, laptop, and Argo to see how far away I could get and still detect the signal. With this bare bones transmitter setup (using a 2M J-pole antenna) I was able to detect it over 4,000 ft away. The receiving antenna was a 2m ~1ft high antenna magnet-mounted on top of my car.

<div class="text-center img-border">

[![](qrss_fade_thumb.jpg)](qrss_fade.png)

</div>

__In retrospect, I should have run Argo at my apartment and drove the _transmitter _farther and farther away.__ I presume that my transmitter is functioning decently, and that if I attached it to a proper antenna (and had a better receiving antenna) I might be able to get some cross-town distance? I'm still learning - this is the point though, right?

<div class="text-center img-border">

[![](firsttransmap_thumb.jpg)](firsttransmap.png)

</div>

__This is where I was when the signal died.__ The red marker (upper right) is my apartment where the transmitter was, and the signal began to die right as I traveled south on Chickasaw past Lake Underhill (~4000 ft away). This immediate loss may be due to the fact that I passed under power lines which parallel Lake Underhill which interrupted the line-of-sight path between my 3rd story apartment balcony and me. If this were the case, supposedly if I kept driving south the signal may have improved.

