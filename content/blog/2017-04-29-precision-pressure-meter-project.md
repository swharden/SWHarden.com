---
title: Precision Pressure Meter Project
date: 2017-04-29 13:15:07
tags: ["microcontroller", "circuit"]
---



__I just completed building a device capable of measuring temperature to one hundredth of a degree Celsius and pressure to one ten-thousandth of a PSI!__ This project is centered around a [MS5611 temperature sensor breakout board](http://www.icstation.com/ms5611-pressure-altitude-sensor-module-24bit-converter-p-10426.html) which was small enough to fit inside of a [plastic syringe](https://swharden.com/static/2017/04/29/#links). The result is a small and inexpensive pressure sensor in a convenient form factor with a twist connector (a [Luer-Lok](https://en.wikipedia.org/wiki/Luer_taper) fitting) that can be rapidly attached to existing tubing setups. Although the screw attachment would work well for industrial or scientific applications, I found that the inner connector (the non-threaded plastic nub with 6% taper) made a snug and air-tight connection with my [CO2-impermanent aquarium tubing](http://www.ebay.com/sch/i.html?_nkw=CO2+aquarium+tubing). The MS5611 breakout board is small enough to fit inside a 10 mL syringe!

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170423_171551.jpg)

</div>

__I documented this project thoroughly so others can learn about the design process__ that goes into making one-off prototypes like this. The video is quite long considering how simple the task seems (read a number from a sensor and display it on a screen), but it gives a lot of tips and insights into rapidly making professional looking one-off projects like this. Reading datasheets can be intimidating for newcomers too, and this video walks through how to figure out how to bang out I2C commands to a new sensor using a [Bus Pirate](http://dangerousprototypes.com/docs/Bus_Pirate) - a _really_ convenient tool to have for electrical engineering hobbyists like me! After it's working well with the sensor/computer interface you can move to the microcontroller level with confidence. Since no one has posted code for how to interface this sensor directly with the microcontroller platform I intended to use (AVR-GCC, notably _not_ Arduino), my build process started by poking around with a [Bus Pirate](https://swharden.com/static/2017/04/29/#tools) to learn how to interact with the device using  I2C commands. Once I was able to initiate temperature and pressure readings and pull its values by hand using the Bus Pirate, I wrote a Python script to automate the process (using PySerial to interact with the Bus Pirate) and allow recording and graphing of real-time pressure and temperature information. I then used a [logic analyzer](https://swharden.com/static/2017/04/29/#tools) to glance at the data exchanged between the Bus Pirate and the pressure sensor (mostly for my own satisfaction, and to help with debugging in the future). Finally, I ditched the computer and had an ATMega328 microcontroller pull temperature/pressure readings and display them on a [16x2 HD44780 character LCD display](https://swharden.com/static/2017/04/29/#components) beautifully framed with a [laser-cut LCD bezel](https://swharden.com/static/2017/04/29/#components) (from Tindie user [widgeneering](https://www.tindie.com/stores/WIDGENEERING/)). I used a USB connector to give the device power (though there's no reason it couldn't run off of 3xAA batteries) and CAT5 cable as a convenient connector between the display and the sensor. After assembling everything and [making some labels](https://swharden.com/static/2017/04/29/#tools), the final product looks quite professional!

## Project Summary Video

This video is quite extensive. It explores the design process for one-off projects like this, with extra time spent on the difficult parts that often pose the greatest challenges to newcomers (exploring datasheets, banging out I2C commands with a new sensor). I don't see this part of the design process discussed too often in engineering videos, so I hope it will be an insightful and inspiring resource to people just starting to work with custom electronics and prototype design. Another group of people who benefit from watching the video are those who don't know much about the design process of embedded devices, but will quickly realize that building a prototype device to do something as simple as reading a number from a sensor and displaying it on a screen can take an immense amount of insight, work, troubleshooting, and effort to create.

{{<youtube T3ma1n_jhbQ>}}

## About the MS5611 Temperature and Pressure Sensor

__The breakout board I'm using provides 5V access to the I2C interface of the MS5611.__ This is convenient because the MS5611 requires 3.3V and many microcontroller applications run at 5V. The MS5611 itself is the small (5mm by 3mm) silver rectangle on the side of the board. The [MS5611 datasheet](http://www.hpinfotech.ro/MS5611-01BA03.pdf) has all the information we need to know to get started poking around its I2C bus! The general idea is that it has an imperfect pressure sensor on board. During production the pressure sensors are produced with slightly different offsets and gains. Further, the pressure sensor varies its output as a function of temperature. They included a temperature sensor on there too, but that also varies by offset and gain due to production! To yield highly precise absolute pressure readings, the factory calibrates every device individually by storing six 16-bit calibration values in a program memory. They represent the sensitivities and offsets of these sensors.

When run through an algorithm (given a whole page in the datasheet), the 6 factory-programmed calibration values (16-bit integers) can be combined with the raw temperature and pressure readings (24-bit integers) to yield incredibly accurate and precise temperature and pressure readings down to 0.01 degree Celsius and 0.012 millibar (0.00017 PSI). This accuracy is enough to be able to measure changes in altitude of 10 centimeters!

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/10426_1_4531.jpg)
![](https://swharden.com/static/2017/04/29/10426_3_5984.jpg)
![](https://swharden.com/static/2017/04/29/WIN_20170312_21_36_07_Pro.jpg)
![](https://swharden.com/static/2017/04/29/WIN_20170312_21_32_56_Pro.jpg)

</div>

__These are some photos of the break-out board__ from the [company's product page](http://icstation.com/ms5611-pressure-altitude-sensor-module-24bit-converter-p-10426.html) and a few more taken from my USB microscope zoomed in on the sensor itself. If I feel inspired, I may use my hot air tool to lift the sensor off the board and incorporate into a future, smaller design. I'll save that project for another day!

## Using a Bus Pirate to Communicate with the Sensor

__After reading the datasheet I learned the general flow of how to read data from this sensor.__ It was a three step command process for both temperature and pressure:

*   **Tell the device what to measure and with what precision** by sending 1 byte. This is in the commands section (page 9/20) of the [datasheet](http://www.hpinfotech.ro/MS5611-01BA03.pdf). Command __0x48__ will tell it to use maximum oversampling ratio (OSR) to convert D1 (the digital pressure value). Highest OSR (4096) means the most precise reading but a slightly slower reading (9.04 ms) with higher current draw (12.5 µA at 1 Hz) as compared to the lowest OSR (256, 0.6 ms, 0.9 µA).

*   **Tell the device you are ready to perform an ADC read** by sending 1 byte. The byte you send to read the ADC is always `0x00`. Don't proceed to this step until the conversion has been given time to complete or your reading will be zero.

*   **Read the ADC result** by reading 3 bytes. The ADC result will always be an 18-bit integer.

__This was a great use for my Bus Pirate! __Without the [Bus Pirate](http://dangerousprototypes.com/docs/Bus_Pirate) in order to debug this device I would have needed to make a circuit board, wire-up a microcontroller, figure out how to program that microcontroller to interact with the sensor (with very limited hardware debug tools), and send readings (and debug messages) to a computer via a USB serial port. Also, I'd have to add bidirectional serial communication code if I wanted it to be interactive. What a nightmare! Recently I started really valuing my Bus Pirate as a way to immediately hook up to a new sensor out of the box and interactively pull data from it within a few seconds. To hack this to my Bus Pirate I soldered-on female headers (instead of soldering on the pins that came with the breakout board). The [Bus Pirate pin descriptions page](http://dangerousprototypes.com/docs/Bus_Pirate_I/O_Pin_Descriptions) shows how to hook up an I2C device. It's important to note that the sensor board will not receive power (and its LED won't light up) until you send the "W" command to the Bus Pirate.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/270.jpg)

</div>

__Here are the commands I use with the Bus Pirate to connect with the sensor.__ If you can't get this part to work, I don't recommend challenging using a microcontroller to pull I2C data from this part! This is kind of fool proof, so this stage not working means you've read the datasheet incorrectly and don't know how to interact with the sensor as well as you thought you did, or that there is a hardware or connectivity issue with the circuit. All of this is in the video posted above, so watching that part of the video may help you get an idea of what it looks like interacting with circuits like this with a Bus Pirate. Also, be sure to review the [Bus Pirate I2C guide](http://dangerousprototypes.com/blog/bus-pirate-manual/i2c-guide/).

*   Open [RealTerm](https://swharden.com/static/2017/04/29/#software) and connect to the Bus Pirate

    *   change display mode to Ansi
    *   set baud to 115200 baud (no parity, 8 bits, 1 stop bit)

*   __\#__ to reset the Bus Pirate (optional)
*   __m__ to set mode
*   __4__ to select I2C
*   __3__ to select 100 KHz
*   __W__ to enable power (the red LED on the sensor should light up)
*   __P__ to enable pull-up resistors (no errors should be displayed)
*   __(1)__ scan for I2C devices (the sensor should be displayed, likely as oxEE)
*   Let's make a read! This is how to read raw pressure:

    *   __\[0xEE 0x48\]__ _to do the 4096 OCR D1 read_
    *   __\[0xEE 0x00\]__ _to prepare to read the ADC_
    *   __\[0xEF r:3\]__ _to read 3 bytes_


<div class="text-center">

![](https://swharden.com/static/2017/04/29/realterm3.png)

</div>

__For the most accurate readings__, use the algorithms on [page 7/20 of the datasheet](http://www.hpinfotech.ro/MS5611-01BA03.pdf) to use the calibration variables (C1-C6) in combination with pressure (D1) and temperature (D2) to produce an accurate temperature and pressure measurement.

## Enclosing the Pressure Sensor

__My application requires me to sense pressure in air-tight tubing.__ My solution was to insert this sensor inside a 10 mL syringe and seal it up with epoxy such that the only opening would be the twist connector I could attach to the air line. I accomplished this by cutting the syringe with a rotary tool, removing the rubber stopper from the plunger and puncturing it so I could pass the wires through, then sealing it up as tightly as I could. I crossed my fingers and hoped it wouldn't leak as I mixed-up some epoxy and poured it in. After an hour of setting time, I was delighted to learn that it sealed air tight! I could now attach needles and tubes with the screw connector, or leave it disconnected to measure atmospheric pressure.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/310.jpg)
![](https://swharden.com/static/2017/04/29/316.jpg)
![](https://swharden.com/static/2017/04/29/327.jpg)

</div>

## Sniffing I2C with a Logic Analyzer

__Right off the bat my Bus Pirate could pull sensor data but the C code I wrote running on a microcontroller could not.__ What gives? Was the sensor hooked up wrong? Was the microcontroller sending the wrong commands? Were the commands not being read by the microcontroller properly? Were the messages not being transmitted to the LCD display properly? There are so many points for failure and such limited hardware debugging (I'm not using [JTAG](https://en.wikipedia.org/wiki/JTAG)) that my first go-to was my [logic analyzer](https://swharden.com/static/2017/04/29/#tools). As you can probably tell by the video I don't use this thing too often, but good gosh when I do it usually saves me hours of head scratching.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170423_210831.jpg)

</div>

__In this case, I immediately saw__ that the I2C lines were always low (!) and realized that the problem was my reliance on microcontroller pull-up resistors to keep those lines continuously high. That was a rookie mistake. I guess I could have seen this with an oscilloscope, but at the time I hooked it up I thought it was a _protocol issue_ and not a _dumb hardware issue_. I slapped on a few 10K resistors to the VCC line and it worked immediately. Regardless, it was nice to have the capability. See the video for details.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/saleae.jpg)

</div>

## Building the Enclosure

__I still can't get over how good the silver aluminium looks against the black laser-cut display bezel in combination with the dark backbit LCD display.__ I couldn't have done this without the [LCD bezels I just found being sold on Tindie](https://www.tindie.com/stores/WIDGENEERING/)! Mounting character LCD displays on metal or plastic enclosures is a chore and usually looks awful. I cringe at [some of my old projects](https://www.swharden.com/wp/2011-03-14-frequency-counter-finished/) which have displays loosely meshed with square cut-outs. My square holes look nicer now that I use a hand nibbler tool, but there's just no way that I know of to make an LCD display look good in a square cut-out without a good bezel. Another advantage of a large bezel is you don't have to make a perfectly square cut-out, since it will all get covered-up anyway!

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170408_120421.jpg)
![](https://swharden.com/static/2017/04/29/20170408_120633.jpg)
![](https://swharden.com/static/2017/04/29/342.jpg)
![](https://swharden.com/static/2017/04/29/20170408_124012.jpg)

</div>

__I then proceeded to epoxy the connectors__ I wanted (USB and Ethernet) and drill holes for the PCB mount. I added the microcontroller ([ATMega328](http://www.microchip.com/wwwproducts/en/ATmega328)) and the circuit is so simple I'm not even going to display it here. If you're really interested, check out the video. My logic is that a 5V noisy power supply is fine since all we are doing is simple, slow, digital signaling, and that the sensitive stuff (analog pressure/temperature sensing) is done on a board which already has a linear regulator on it presumably filtering-out almost all of the supply line noise. Plus, my application is such that 0.1 PSI is good enough and measuring it to a ten-thousandth of a PSI is quite overkill and I didn't even end-up displaying the last digit of precision.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170409_132514_HDR.jpg)

</div>

__I used CAT5 to carry I2C, which I understand is a bit iffy.__ I2C is designed to be sent over small distances (like across a circuit board), and not really for long distance transmission. That's not to say long distance I2C isn't possible; it just requires a few extra design considerations. The basic idea is that a long line has a lot of capacitance, so it would take a lot of current (sinking and sourcing) to rapidly pull that line fully high and fully low at the high speeds that I2C could use. The longer the cable, the greater the capacitance, and the lower speed I2C you have to use and/or higher current you need to drive it. I2C drivers exist to help with this purpose, and although I have some I found I didn't actually need to use them. For more information, google on the topic of sending I2C over twisted pair. This [Hackaday article on sending I2C over long distances](http://hackaday.com/2017/02/08/taking-the-leap-off-board-an-introduction-to-i2c-over-long-wires/) is also quite nice. For the purposes of this prototype, it's working with straight-through wiring (sensor-to-microcontroller) so let's call it good and move on.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170420_212832.jpg)

</div>

__I had to use a slightly larger aluminum enclosure__ than I initially wanted because there was limited vertical space with the LCD risers as well as the risers I used for my own board. It was a tight squeeze when all was said and done, but it worked great!

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170422_172610.jpg)

</div>

## Programming the Microcontroller

__Let's just say I programmed the microchip to do exactly what we did with the Bus Pirate.__ The code is messy as heck (and even is using two different I2C libraries to signal on the same I2C line!) but it works and the prototype is done and sealed so I don't really have a lot of reason to fine-tune the software. The full project can be [found on the GitHub page](https://swharden.com/static/2017/04/29/#links), and a few relevant lines of code are below.

__Here are a few key points about the microcontroller software:__

*   I added a "baseline reset" which resets the current pressure to 0.000 PSI.
*   I'm intentionally not showing full precision because I don't need it for my application.
*   I hard-coded the calibration values in C rather than look them up each time. This is fine since this code will only run on this one microchip with this one sensor. If this were a production device, obviously they would be read on startup.
*   I am not using the formula provided in the datasheet to integrate the calibration values with temperature to calculate pressure. Instead, I came up with my own formula (essentially just Y=mX+b) which was fit to an ADC/PSI curve I plotted myself using the calibration values for this one sensor and the temperature (72F) where I know the device will be held.
*   Since I'm controlling for temperature and hard-coded my calibration values, I can get good enough precision without the need for floating point math. Adding floating point libraries to an 8-bit AVR [consumes a lot of memory](https://electronics.stackexchange.com/questions/16400/excessive-avr-static-ram-usage-with-mixed-type-math-operations) and can be slow. However, in a production unit this would probably be a must.
*   Adding logging / PC connectivity would be really easy since there's already a USB connection there! In this circuit I'm just using it for the +5V power, but there's no reason we couldn't attach to the data lines and send our temperature and pressure readings via USB. The easiest way to do this would be by adding an FTDI TTL serial USB adapter such as the [FT232](http://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT232R.pdf) or its [breakout board](https://www.sparkfun.com/products/12731). The microcontroller already has TTL USART capability so it would only be a few extra lines of code.

__Code to pull 16-bit calibration values from program memory:__

```c
volatile unsigned int prog[8]; // holds calibration values
uint8_t data[2];
char i,j;
for (i=0;i<8;i++){
    data[0]=160+i*2; // addresses from datasheet
    i2c2_transmit(0xEE,data,1);
    i2c2_receive(0xEF,data,2);
    prog[i]=data[0];
    prog[i]*=256;
    prog[i]+=data[1]; // prog[1] will be C1
}
```

__Code to pull a 24-bit pressure sensor reading:__

```c
uint8_t data[3];
data[0]=72; // command 72 is "set register to pressure"
i2c2_transmit(0xEE,data,1);
_delay_ms(10); // time for conversion to complete
data[0]=0; // command 0 is "ADC read"
i2c2_transmit(0xEE,data,1);
i2c2_receive(0xEF,data,3);
pressure=0;
pressure+=data[0]; // pull in a byte
pressure=pressure<<8; // and shift its significance
pressure+=data[1]; // pull in another byte
pressure=pressure<<8; // shit it all again
pressure+=data[2]; // add the last byte

```

## Example Application

__It's great to have an inexpensive precision temperature and pressure sensor design ready to go__ for any application I want to use it for in the future. This is a project I've been wanting to build for a long time for an aquarium purpose involving monitoring the rate of CO2 injection through the intake valve of an aquarium filter (which I am aware is discouraged because bubbles can be rough on the impeller) as part of a DIY yeast reactor, all to encourage aquatic plant growth. Botany in a sentence: plants use light to grow and metabolize carbon dioxide (CO2) while producing oxygen (O2). By supplementing (but not saturating) the water with CO2, I get better plants. 

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170329_232145.jpg)

</div>

**There's also potential for an application to monitor the positive pressure** (rather than negative pressure / suction) of a microcontroller-pressure-controlled reaction chamber this way. If I code it wrong, and the pressure isn't released, 1 gallon of sugary yeasty water will end up bursting over my living room floor. (I guess this means the _pressure_ _is on_ to get the design right?) Alternatively this prototype may serve a role as a pressure sensor for scientific applications monitoring incubator pressure and temperature. Most importantly, this project encouraged me to check out some new hardware I am really glad I found (laser-cut character LCD bezels), read-up on I2C transmission lines and power drivers, and get experience with a new type of sensor that a lot of the Internet has not seen before.

<div class="text-center img-border">

![](https://swharden.com/static/2017/04/29/20170423_214443.jpg)

</div>

## Resources

### Components

*   __Pressure sensor__ \[$7.79\] [MS5611 break-out board](http://www.icstation.com/ms5611-pressure-altitude-sensor-module-24bit-converter-p-10426.html) from [ICStation](http://www.ICStation.com) (15% discount code: haics)
*   __LCD Bezel__ \[$4.99\] [16x2 LCD Bezel](https://www.tindie.com/products/WIDGENEERING/16x2-lcd-bezel/) from Tindie user [Widgeneering](https://www.tindie.com/stores/WIDGENEERING/)
*   __LCD Display__ \[$1.50 in bulk\] 16x2 hd44780 character LCD with backlight [via eBay search](http://www.ebay.com/sch/i.html?_nkw=hd44780)
*   __LCD I2C adapter__ \[$3\] 1602-based [via eBay search](http://www.ebay.com/sch/i.html?_nkw=hd44780) (not really needed)
*   __Aluminum enclosure__ \[$11.50\] 4.32" x 3.14" x 1.43" size found [via eBay search](http://www.ebay.com/sch/i.html?_nkw=split+body+aluminum+enclosure)
*   __ATMega328 8-bit microcontroller__ \[~$1.50 each in bulk\] [via eBay search](http://www.ebay.com/sch/i.html?_nkw=atmega328)
*   __Plastic syringes__ and blunt needles \[cheap\] from [Amazon](https://www.amazon.com/Pack-Refilling-Measuring-E-Liquids-Adhesives/dp/B01CFJ51X4/)
*   __USB and Ethernet sockets and cables__ \[salvaged\]

### Tools

*   __Bus Pirate__ (v3) \[$27.15\] from [DangerousPrototypes.com](http://dangerousprototypes.com/docs/Bus_Pirate)
*   __AVR programmer__ (USBtinyISP) \[$4.99\] [via eBay search](http://www.ebay.com/sch/i.html?_nkw=usbtinyisp)\]
*   __Saleae Logic Analyzer__

    *   Saleae software (free) at [saleae.com/downloads](https://www.saleae.com/downloads)
    *   Official Logic Pro 8 \[$109\] or Logic Pro 16 \[$599\] from [saleae.com](https://www.saleae.com/)
    *   Knock-off 8 channel logic analyzer \[$6.93\] [via eBay search](http://www.ebay.com/sch/i.html?_nkw=saleae+logic+8)
    *   Knock-off 16 channel logic analyzer \[$39.50\] [via eBay search](http://www.ebay.com/sch/i.html?_nkw=saleae+logic+16)
    *   [Review of Knock-off hardware](https://iamzxlee.wordpress.com/2015/09/15/usb-logic-analyzer-review/) by iamzxlee
    *   [Review of Official hardware](http://hackaday.com/2015/05/26/review-dslogic-logic-analyzer/) on Hack-A-Day
    *   [Saleae's comments on counterfeit devices](https://www.saleae.com/counterfeit)

*   __Labels__ made with a [LetraTag LT-100T](https://www.amazon.com/DYMO-LetraTag-Personal-Hand-Held-1733013/dp/B001B1FIW2/) and [clear tape](https://www.amazon.com/DYMO-Labeling-LetraTag-Labelers-Black/dp/B00006B8FA) (tricks [learned from Onno](http://www.qsl.net/pa2ohh/tlabels.htm))

### Software

*   All code used for this project is on my [AVR-Projects GitHub page](https://github.com/swharden/AVR-projects)

    *   [Python code](https://github.com/swharden/AVR-projects/tree/master/BusPirate%202017-02-04%20i2c%20ms5661%20pressure) to interact with Bus Pirate
    *   [ATMega328 code](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202017-03-19%20i2c%20LCD%20pressure%20sensor) to control the sensor and LCD with the microcontroller

*   [RealTerm on SourceForge](https://sourceforge.net/projects/realterm/) (serial console program I use to communicate with Bus Pirate)
*   [Saleae software](https://www.saleae.com/downloads) is free and works (for now) on clone hardware

### Additional Resources

*   [Bus Pirate I2C guide](http://dangerousprototypes.com/blog/bus-pirate-manual/i2c-guide/)
*   Hackaday article: [Sending I2C over long wires](http://hackaday.com/2017/02/08/taking-the-leap-off-board-an-introduction-to-i2c-over-long-wires/)
*   Application note: [Driving I2C bus signals over twisted pair cables with PCA9605](http://www.nxp.com/documents/application_note/AN11075.pdf)
*   My [AVR-Projects GitHub page](https://github.com/swharden/AVR-projects) has notes about AVR programmers and software