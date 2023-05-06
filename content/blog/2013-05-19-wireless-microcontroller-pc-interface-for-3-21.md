---
title: Wireless Microcontroller / PC Interface for $3.21
date: 2013-05-19 01:32:46
tags: ["microcontroller", "old", "python"]
---

# Wireless Microcontroller / PC Interface for $3.21

__Here I demonstrate a dirt-cheap method of transmitting data from any microchip to any PC using $3.21 in parts.  __I've had this idea for a while, but finally got it working tonight. On the transmit side, I'm having a an ATMEL AVR microcontroller (ATMega48) transmit data (every number from 0 to 200 over and over) wirelessly using 433mhz wireless modules. The PC receives the data through the microphone port of a sound card, and a cross-platform Python script I wrote decodes the data from the audio and graphs it on the screen. I [did something similar back in 2011](http://www.swharden.com/blog/2011-07-09-sound-card-microcontrollerpc-communication/), but it wasn't wireless, and the software wasn't nearly as robust as it is now.

__This is a proof-of-concept demonstration, and part of a larger project.__ I think there's a need for this type of thing though! It's unnecessarily hard to transfer data from a MCU to a PC as it is. There's USB (For AVR [V-USB](http://www.obdev.at/products/vusb/index.html) is a nightmare and requires a precise, specific clock speed, DIP chips don't have native USB, and some PIC DIP chips do but then you have to go through driver hell), [USART RS-232 over serial port](http://www.swharden.com/blog/2009-05-14-simple-case-avrpc-serial-communication-via-max232/) works (but who has serial ports these days?), or USART over USB RS-232 interface chips (like [FTDI FT-232](http://www.ftdichip.com/Products/ICs/FT232R.htm), but surface mount only), but both also require precise, specific clock speeds. Pretend I want to just measure temperature once a minute. Do I _really_ want to etch circuit boards and solder SMT components? Well, kinda, but I don't like feeling forced to. Some times you just want a no-nonsense way to get some numbers from your microchip to your computer. This project is a funky out-of-the-box alternative to traditional methods, and one that I hope will raise a few eyebrows.

<div class="text-center img-border">

![](https://swharden.com/static/2013/05/19/c31.jpg)

</div>

__Ultimately, I designed this project to eventually allow multiple "bursting" data transmitters to transmit on the same frequency__ __routinely__, thanks to syncing and forced-sync-loss (read on). It's part of what I'm tongue-in-cheek calling the _Scott Harden RF Protocol_ (SH-RFP). In my goal application, I wish to have about 5 wireless temperature sensors all transmitting data to my PC.  The receive side has some error checking in that it makes sure pulse sizes are intelligent and symmetrical (unlike random noise), and since each number is sent twice (with the second time being in reverse), there's another layer of error-detection.  This is \*NOT\* a robust and accurate method to send critical data. It's a cheap way to send data. It is very range limited, and only is intended to work over a distance of ten or twenty feet. First, let's see it in action!

![](https://www.youtube.com/embed/GJHFldPwZvM)

__The RF modules are pretty simple. [At 1.56 on ebay](http://www.ebay.com/itm/KDQ11-NEW-1PCS-433MHZ-RF-TRANSMITTER-AND-RECEIVER-LINK-KIT-FOR-ARDUINO-SCA-1710-/350797631746?pt=LH_DefaultDomain_0&hash=item51ad2b1102) (with free shipping), they're cheap too!__ I won't go into detail documenting the ins and out of these things (that's done well elsewhere). Briefly, you give them +5V (VCC), 0V (GND), and flip their data pin (ATAD) on and off on the transmitter module, and the receiver module's DATA pin reflects the same state. The receiver uses a gain circuit which continuously increases gain until signal is detected, so if you're not transmitting it WILL decode noise and start flipping its output pin. Note that persistent high or low states are prone to noise too, so any protocol you use these things for should have rapid state transitions. It's also suggested that you maintain an average 50% duty cycle. These modules utilize [amplitude shift keying](http://en.wikipedia.org/wiki/Amplitude-shift_keying) (ASK) to transmit data wirelessly. The graphic below shows what that looks like at the RF level. Transmit and receive is improved by adding a quarter-wavelength vertical antenna to the "ANT" solder pad. At 433MHz, that is about 17cm, so I'm using a 17cm copper wire as an antenna.

__Transmitting from the microcontroller is easy as pie!__ It’s just a matter of copying-in a few lines of C.  It doesn’t rely on USART, SPI, I2C, or any other protocol. Part of why I developed this method is because I often use ATTiny44A which doesn’t have USART for serial interfacing. The “SH-RFP” is easy to implement just by adding a few lines of code. I can handle that.  How does it work? I can define it simply by a few rules:

*   Pulses can be one of 3 lengths: A (0), B (1), or C (break).
*   Each pulse represents high, then low of that length.

To send a packet:

*   prime synchronization by sending ten ABCs
*   indicate we’re starting data by sending C.
*   for each number you want to send:
  *   send your number bit by bit (A=0, B=1)
  *   send your number bit by bit (A=1, B=0)
  *   indicate number end by sending C.
*   tell PC to release the signal by sending ten Cs.

Decoding is the same thing in reverse. I use an [eBay sound card at $1.29](https://swharden.com/static/2013/05/19/search.ebay.com/usb-sound-card) (with free shipping) to get the signal into the PC. </span> Synchronization is required to allow the PC to know that real data (not noise) is starting. Sending the same number twice (once with reversed bit polarity) is a proof-checking mechanisms that lets us throw-out data that isn’t accurate.

__From a software side,__ I’m using PyAudio to collect data from the sound card, and the PythonXY distribution to handle analysis with numpy, scipy, and plotting with QwtPlot, and general GUI functionality with PyQt. I think that’s about everything.

<div class="text-center img-border">

![](https://swharden.com/static/2013/05/19/SHRFP.png)

</div>

__The demonstration interface is pretty self-explanatory.__ The top-right shows a sample piece of data. The top left is a histogram of the number of samples of each pulse width. A clean signal should have 3 pulses (A=0, B=1, C=break). Note that you’re supposed to look at the peaks to determine the best lengths to tell the software to use to distinguish A, B, and C. This was intentionally not hard-coded because I want to rapidly switch from one microcontroller platform to another which may be operating at a different clock speed, and if all the sudden it’s running 3 times slower it will be no problem to decide on the PC side. Slick, huh? The bottom-left shows data values coming in. The bottom-right graphs those values. Rate reporting lets us know that I'm receiving over 700 good data points a second. That's pretty cool, especially considering I'm recording at 44,100 Hz.

All source code (C files for an ATMega48 and Python scripts for the GUI) can be viewed here: [SHRFP project on GitHub](https://github.com/swharden/AVR-projects/tree/master/ATMega48%202013-05-14%20SHRFP%20monitor)

If you use these concepts, hardware, or ideas in your project, let me know about it! Send me an email showing me your project – I’d love to see it. Good luck!

