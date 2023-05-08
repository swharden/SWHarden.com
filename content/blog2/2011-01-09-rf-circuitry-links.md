---
title: RF Circuitry Links
date: 2009-01-09 15:30:00
tags: ["circuit", "amateur radio"]
---



<a href="http://www.nutsvolts.com/media-files/A_Universal_Direct_Conversion_Receiver_For_PSK-31.pdf">PSK-31 receiver</a> - sports a crystal filter front-end and active receiver

<a href="http://www.arrl.org/files/file/Technology/tis/info/pdf/28814.pdf">Neophyte Receiver</a> - old article based around an NE602 / SA602 / SA612.

<a href="http://techdoc.kvindesland.no/radio/b1/20051213190607573.pdf">602 Primer</a> - old document but very good about SA602, includes method to estimate capacitor values for Colpitts oscillator mode.

<a href="http://www.hanssummers.com/30m.html">Hans' 30m receiver</a> where he used an inverting gate buffer oscillator to generate 5v square waves which he fed into a SA602

<a href="http://frrl.wordpress.com/2008/11/15/direct-conversion-receiver-making-friends-with-the-signetics-sa602/">Making Friends with the SA602</a> - an attempt at a write-up of the circuitry behind the <a href="http://www.ramseyelectronics.com/cgi-bin/commerce.exe?preadd=action&amp;key=HR-SERIES">Ramsey receiver kits</a> (which only do 1 band each), although the manuals (<a href="http://www.ramseyelectronics.com/downloads/manuals/HR40.pdf">example for 40m</a>) may be useful

<a href="http://www.seekic.com/forum/22_circuit_diagram/25644_35_TO_10_MHz_SIMPLE_SUPERHETERODYNE_RECEIVER.html">3.5-10MHz receiver</a> - around a few SA602s, uses IF transformers too

<a href="http://www.gqrp.com/suddenbuildingyourkitbooklet30m.pdf">30m receiver design</a> - "The Limerick Sudden 30m Receiver Kit" based around a SA602/LM386 very simple and pretty

<a href="http://www.qrpme.com/docs/ORIGINAL%20SS%20Instructions.pdf">Sudden Storm Receiver</a> - tuna tun style, check out schem a few pages in... sa602 + LM386 + crystal

<a href="http://www.stephenhobley.com/blog/2011/03/02/still-messing-with-forces-i-dont-understand-the-formula/">Etching PCBs</a> with hydrogen peroxide, vinegar, and table salt (wow!)

<a href="http://swharden.com/qrssvd/files/morse.exe">Morse.exe</a> - A good way to learn Morse code!

## High Altitude Balloon

<a href="http://www.ve7zsa.net/technical/advsgtxt/c7oscillator_r00.htm ">Oscillator page</a> which has a section mentioning that the 7th overtone can be used in an oscillator. The 7th overtone of 18mhz (17m) is 144mhz (2m) smack dab in the CW region. Nice!

<a href="http://habhub.org/predict/#!/uuid=6f0e725b992a00555d7b2e65b0bae1ade0d38fae">Path prediction</a> - note that UF is 29.642276 latitude and -82.344949 longitude

<a href="http://www.robertharrison.org/icarus/wordpress/">Icarus</a> - a HAB project run on advertising revenue that seems successful and has launched many balloons with some awesome photos. <a href="http://www.robertharrison.org/index.php?option=com_content&amp;task=view&amp;id=25&amp;Itemid=78">Robert Harrison</a> knows his stuff!

<a href="http://projectspaceplanes.com/">Project Space Planes</a> - launches paper airplanes from 30km above the earth which glide down and land all over the world!

<a href="http://natrium42.com/halo/flight2/">HALO project</a> - very well documented HAB with pictures/video

<a href="http://www.phonestack.com/farhan/jbot.html">JBOT</a> - An SSB linear amplifier made from Just a Bunch of Transistors. It's pretty straightforward, cheap, and converts 1mW input to 5W output.

<a href="http://oz2oe.dk/radio/interference/xtalgen/xtalgen.html">harmonic oscillator</a>

<a href="http://www.radiosparks.com/images_d/OSBA1078.jpg">tuned oscillator example</a>

<a href="http://www.radiosparks.com/images_d/OSCR941.jpg">overtone oscillator</a>

<a href="http://my.integritynet.com.au/purdic/rf-amplifier-with-feedback.htm">amplifier design walk-through</a>

<a href="http://openbookproject.net/electricCircuits/">Lessons in Electric Circuits</a> - A very good (free) textbook. Anyone starting to learn about electronics should start by skimming over relevant chapters of this text!

<a href="http://www.genesisradio.com.au/Q5/">1W CW transmitter kit</a> - Although I don't own one, I appreciate the kit and love the <a href="http://genesisradio.com.au/Q5/q5_20.gif">schematic</a>. This guy uses a buffer chip (a 74HC04n, similar to a 74HC240 often used in QRP too) to act as an oscillator and small amplifier. The output is then further amplified by a 2n3866 transistor.

<a href="http://clayton.isnotcrazy.com/mept_v1">30M Solar QRSS transmitter</a> - such an inspiring project! This guy uses a buffer chip (74hc245) to amplify the output of CKOUT of a microcontroller clocked at the transmit frequency. The thing is solar powered, and has a unique temperature compensation mechanism which uses the chip's built-in thermosensor to adjust its offset. I haven't seen this technique used anywhere else in a QRP transmitter!

<a href="http://www.hanssummers.com/">HansSummers.com</a> - Everything this man does is impressive! His QRSS section is wonderful, and I won't detract from it by trying to describe it here. He also has a simple QRSS receiver circuit based upon a SA602, <a href="http://www.swharden.com/blog/2010-06-09-minimalist-radio-receiver/">something I replicated</a> (tuned front-end not shown) to operate my <a href="http://ham.w4dfu.ufl.edu:8080/">W4DFU QRSS Grabber</a> at the University of Florida.

<a href="http://www.aoc.nrao.edu/~pharden/hobby/_ClassDEF1.pdf">MOSFET "Switched Mode" Amplifiers</a> - a wonderful document, read it multiple times! Transistors are traditionally used in many QRP circuits as amplifiers, but MOSFETs have some unique qualities which in many ways makes them easier to work with in simple circuits. I found this guide EXTREMELY helpful!

<a href="http://my.integritynet.com.au/purdic/rf-amplifier-with-feedback.htm">Amplifier design</a> - a cool walk-through of the design of an amplifier with the math described every step of the way

<a href="http://www.ham.se/en/27939-post26.html">IRF-510 QRP transmitter</a> design which looks pretty interesting... Note that increasing efficiency lets the MOSFET run cool!

<a href="http://www.rason.org/Projects/transmit/transmit.htm">Similar IRF-510 transmitter</a> I like as well....

<a href="http://www.pan-tex.net/usr/r/receivers/svfo.htm">SA602 as an oscillator</a> - clever, clock with tank, mix with nothing, output (mixed?) is clock only!

<a href="http://en.wikipedia.org/wiki/User:Rainglasz/Colpitts-Oscillator">JFET Rainglasz/Colpitts Oscillator Design</a> which looks interesting

## Misc

<a href="http://www.gizmology.net/batteries.htm">Battery info</a> - useful for calculating life of batteries under load

<a href="http://www.powerstream.com/AA-tests.htm">Battery tests</a> - tests common batteries at different loads to determine real (not optimal) amp hour ratings!

<a href="http://www.aade.com/filter32/download.htm">Filter design software</a> I use for low pass filter design

<a href="http://www.dl5swb.de/html/mini_ring_core_calculator.htm">Mini ring and core calculator</a> very convenient for designing inductors with toroids or calculating resonance of LC networks

<a href="http://digilander.libero.it/i2ndt/grabber/grabber-compendium.htm">Knights QRSS Compendium</a> - Live image feeds of QRSS grabbers all around the world, often situated at the QRSS watering hole of 10.140MHz

<a href="http://cnts.be/mailman/listinfo/knightsqrss_cnts.be">Knights QRSS Mailing List</a> - Sign up for this mailing list to see who's transmitting what on which frequency. People also often post photos of their transmitters, and interesting captures from grabbers that you may have missed!

<a href="http://www.amazon.com/Experimental-Methods-Design-Amateurs-Library/dp/0872598799">Experimental Methods in RF Design</a> - Only $32 on Amazon.com right now, this book is an amazing resource for anyone interested in building RF circuits. It goes from extremely simple transmitters, receivers, and amplifiers all the way through advanced topics, modulation methods, etc. It even describes how to build your own test equipment, and even how to use an oscilloscope and assess various stages of your transmitter designs. Flipping through the pages of this book gives me new ideas every time! I requested it many times from my university library (interlibrary loan, often came from Vanderbilt University) before I broke down and got it. I highly recommend this book!