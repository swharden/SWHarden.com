---
title: Generating Analog Voltage with Raspberry Pi
date: 2016-09-28 22:26:29
---

# Generating Analog Voltage with Raspberry Pi

__I recently had the need to generate analog voltages from the Raspberry PI, which has rich GPIO digital outputs but no analog outputs.__ I looked into the [RPi.GPIO project](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/) which can create PWM (which I wanted to smooth using a low pass filter to create the analog voltage), but its output on the oscilloscope looked terrible! It stuttered all over the place, likely because the duty is continuously under software control. I ended up solving my problem with a [MCP4921 12-bit DAC](http://ww1.microchip.com/downloads/en/DeviceDoc/21897a.pdf) chip ([about $1.50 on eBay](http://www.ebay.com/sch/i.html?_nkw=MCP4921)). It's controlled via [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus), and although I could have written a python program to bit-bang its protocol with [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/) I realized I could write directly to the Raspberry Pi SPI device using the `` echo `` command. Dividing 3.3V into 12-bits (4096) means that I can control voltage in steps of less than 1mV each, right from the bash console!

<div class="text-center img-border">

[![](IMG_8696_thumb.jpg)](IMG_8696.jpg)

</div>

### Video: The Problem (RPi PWM jitters)

![](https://www.youtube.com/embed/AtW2DouoyOg)

### Video: My Solution (SPI DAC)

![](https://www.youtube.com/embed/iwzXh2V1SP4)

### Hardware Connection

There's very little magic in how the microchip is connected to the Pi. It's a straight shot to its SPI bus! Here's a quick drawing showing which pins to connect. Check your device against the Raspberry Pi [GPIO pinout diagram](http://www.hobbytronics.co.uk/raspberry-pi-gpio-pinout) for different devices.

<div class="text-center img-border">

![](IMG_8701.jpg)

</div>

### Controlling the DAC with a Bus Pirate

Before I used a Raspberry Pi to control the DAC chip, I tested it out with a [Bus Pirate](http://dangerousprototypes.com/docs/Bus_Pirate). I don't have a lot of pictures of the project, but I have a screenshot of a serial console used to send commands to the chip. One advantage of the Bus Pirate is that I can type bytes in binary, which helps to see the individual bits. I don't have this ability when I'm working in the [bash console](https://en.wikipedia.org/wiki/Bash_(Unix_shell)).

<div class="text-center img-border img-small">

[![](serial_thumb.jpg)](serial.png)

</div>

I'm less familiar with the Bus Pirate, but this was a good opportunity to get to know it a little better. It look me a long time (requiring I pull out the logic analyzer) to realize that I had to manually enable/disable the chip-select line, using the "[" and "]" [commands](http://dangerousprototypes.com/docs/Bus_Pirate_menu_options_guide). When I set up the SPI mode (command m5) I told it to use active low, but I wasn't sure how to reverse the active level of the chip-select commands, so I just did ]this[ instead of [this] and it worked great.

<div class="text-center img-border">

[![](fromPi_thumb.jpg)](fromPi.png)

</div>

This is the signal probed when it was controlled by the Raspberry Pi, but it looked essentially identical when values were sent via the Bus Pirate. The only difference is there was an appreciable delay between the "]" commands and each of the bytes. It worked fine though.

### Controlling the DAC with Console Commands

Once the hardware was configured, the software was trivial. I could control analog voltages by sending two properly-formatted bytes to the SPI hardware device. Importantly, you must use [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) to enable SPI.

```bash
# set analog voltage to minimum value (about 0V)
echo -ne "\x30\x00" > /dev/spidev0.0 # minimum

# set analog voltage to something a little higher
echo -ne "\x30\xAB" > /dev/spidev0.0

# set analog voltage to maximum value (about 3.3V)
echo -ne "\x3F\xFF" > /dev/spidev0.0
```

### Helpful Links:

*   Useful Raspberry Pi [GPIO pinout information](http://www.hobbytronics.co.uk/raspberry-pi-gpio-pinout) for different devices
*   The [RPi.GPIO project](https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/) is a gray way to access Pi hardware from Python
*   Official Raspberry Pi page showing [different methods](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md) to send SPI commands
*   Bus Pirate [SPI Guide](http://dangerousprototypes.com/docs/SPI)

