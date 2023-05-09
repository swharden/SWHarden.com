---
title: WSPR Code Generator
description: An online resource for generating encoded WSPR messages
Date: 2021-03-27 20:00:00
tags: ["blazor", "amateur radio", "qrss"]
---



**[WSPR](https://en.wikipedia.org/wiki/WSPR_(amateur_radio_software)) (Weak Signal Propagation Reporter) is a protocol for weak-signal radio communication.** Transmissions encode a station's callsign, location (grid square), and transmitter power into a frequency-shift-keyed (FSK) signal that hops between 4 frequencies to send 162 tones in just under two minutes. Signals can be decoded with S/N as low as −34 dB! [WSJT-X](https://physics.princeton.edu/pulsar/k1jt/wsjtx.html), the most commonly-used decoding software, reports decoded signals to [wsprnet.org](https://wsprnet.org/) so propagation can be assessed all over the world.

**[WsprSharp](https://github.com/swharden/WsprSharp) is a WSPR encoding library implemented in C#.** I created this library learn more about the WSPR protocol. I also made a web application (using Blazor WebAssembly) to make it easy to generate WSPR transmissions online: [WSPR Code Generator](https://swharden.com/software/wspr-code-generator)

<a href="https://swharden.com/software/wspr-code-generator">
<img src="https://swharden.com/static/2021/03/27/wspr-code-generator.png">
</a>


### WSPR Transmission Information

![](https://swharden.com/static/2021/03/27/wspr-spectrogram.png)

* One packet is 110.6 sec continuous wave
* Frequency shifts between 4 tones 
* Each tone keys for 0.683 sec
* Tones are separated by 1.4648 Hz
* Total bandwidth is about 6 Hz
* 50 bits of information are packaged into a 162 bit message with [FEC](https://en.wikipedia.org/wiki/Error_correction_code)
* Transmissions always begin 1 sec after even minutes (UTC)

### Resources
* [WSPR Code Generator](https://swharden.com/software/wspr-code-generator) - encode WSPR messages from your browser
* [WsprSharp](https://github.com/swharden/WsprSharp) - a .NET library for encoding and decoding WSPR transmissions using C#
* [FSKview](https://swharden.com/software/FSKview/) - spectrogram for viewing frequency-shift keyed (FSK) signals in real time
* [Anatomy of a WSPR transmission](https://swharden.com/software/FSKview/wspr/)
* [WSPR](https://en.wikipedia.org/wiki/WSPR_(amateur_radio_software)) on Wikipedia
* [K1JT Program](http://physics.princeton.edu/pulsar/K1JT/devel.html)
* [Grid square lookup](http://www.levinecentral.com/ham/grid_square.php?Grid=FN20)
* [WSJT](https://sourceforge.net/projects/wsjt/) on SourceForge
* [WSPR Mode in WSJT-X](https://wsprnet.org/drupal/node/5563)