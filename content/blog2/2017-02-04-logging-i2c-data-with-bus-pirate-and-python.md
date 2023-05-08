---
title: Logging I2C Data with Bus Pirate and Python
date: 2017-02-04 13:13:44
tags: ["microcontroller", "circuit"]
---

# Logging I2C Data with Bus Pirate and Python

__I'm working on a project which requires I measure temperature via a computer, and I accomplished this with minimal complexity using a BusPirate and LM75A I2C temperature sensor.__ I already had some LM75A breakout boards I got on eBay (from China) a while back. A [current eBay search reveals](http://www.ebay.com/sch/?_nkw=LM75A) these boards are a couple dollars with free shipping. The IC itself is [available on Mouser](http://www.mouser.com/ProductDetail/NXP-Semiconductors/LM75AD118) for $0.61 each. The [LM75A datasheet](http://www.mouser.com/ds/2/302/LM75A-841329.pdf) reveals it can be powered from 2.8V-5.5V and has a resolution of 1/8 ºC (about 1/4 ºF). I attached the device to the Bus Pirate according to the [Bus Pirate I/O Pin Descriptions](http://dangerousprototypes.com/docs/Bus_Pirate_I/O_Pin_Descriptions) page (SCL->CLOCK and SDA->MOSI) and started interacting with it according to the [Bus Pirate I2C page](http://dangerousprototypes.com/docs/I2C). Since Phillips developed the [I2C protocol,](https://en.wikipedia.org/wiki/I%C2%B2C) a lot of manufacturers avoid legal trouble and call it TWI (two-wire interface).

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2017/02/04/busPirate_LM75A.jpeg)

</div>

__Here I show how to pull data from this I2C device directly via a serial terminal, then show my way of automating the process with Python.__ Note that there are multiple python packages out there that claim to make this easy, but in my experience they are either OS-specific or no longer supported or too confusing to figure out rapidly. For these reasons, I ended up just writing a script that uses common Python libraries so nothing special has to be installed.

### Read data directly from a serial terminal

Before automating anything, I figured out what I2C address this chip was using and got some sample temperature readings directly from the serial terminal. I used [RealTerm ](https://sourceforge.net/projects/realterm/)to connect to the Bus Pirate. The sequence of keystrokes I used are:

*   __\#__ - to reset the device
*   __m__ - to enter the mode selection screen

    *   __4__ - to select I2C mode
    *   __3__ - to select 100KHz

*   __W__ - to turn the power on
*   __P__ - to enable pull-up resistors
*   __(1)__ - to scan I2C devices

    *   _this showed the device listening on 0x91_

*   __\[0x91 r:2\]__ - to read 2 bytes from I2C address 0x91

    *   _this showed bytes like 0x1D and 0x20_
    *   _0x1D20 in decimal is 7456_
    *   _according to datasheet, must divide by 2^8 (256)_
    *   _7456/256 = 29.125 C = 84.425 F_

<div class="text-center img-border img-small">

![](https://swharden.com/static/2017/02/04/BusPirate_i2c_read.png)
![](https://swharden.com/static/2017/02/04/BusPirate_i2c_scan.png)

</div>

### __Automating Temperature Reads with Python__

__There should be an easy way to capture this data from Python.__ The Bus Pirate website even [has a page](http://dangerousprototypes.com/blog/2014/11/05/bus-pirate-v3-and-lm75-temperature-sensors/) showing how to read data from LM75, but it uses a pyBusPirateLite python package which has to be manually installed (it doesn't seem to be listed in pypi). Furthermore, they only have a screenshot of a partial code example (nothing I can copy or paste) and their link to the original article is broken. I found a cool pypy-indexed python module _[pyElectronics](https://github.com/MartijnBraam/pyElectronics)_ which should allow easy reading/writing from I2C devices via BusPirate and Raspberry Pi. However, it crashed immediately on my windows system due to attempting to load Linux-only python modules. I improved the code and issued a pull request, but I can't encourage use of this package at this time if you intend to log data in Windows. Therefore, I'm keeping it simple and using a self-contained script to interact with the Bus Pirate, make temperature reads, and graph the data over time. You can code-in more advanced features as needed.__ The graphical output__ of my script shows what happens when I breathe on the sensor (raising the temperature), then what happens when I cool it (by placing a TV dinner on top of it for a minute). 

<div class="text-center">

![](https://swharden.com/static/2017/02/04/demo.png)

</div>

__Below is the code__ used to set up the Bus Pirate to log and graph temperature data. It's not fast, but for temperature readings it doesn't have to be! It captures about 10 reads a second, and the rate-limiting step is the timeout value which is currently set to 0.1 sec.

__NOTE:__ The Bus Pirate has a convenient [_binary scripting mode_](http://dangerousprototypes.com/docs/Bus_Pirate#Binary_scripting_mode) which can speed all this up. I'm not using that mode in this script, simply because I'm trying to closely mirror the functionality of directly typing things into the serial console.

```python
import serial
import matplotlib.pyplot as plt

BUSPIRATE_PORT = 'com3' #customize this! Find it in device manager.

def send(ser,cmd,silent=False):
    """
    send the command and listen to the response.
    returns a list of the returned lines.
    The first item is always the command sent.
    """
    ser.write(str(cmd+'\n').encode('ascii')) # send our command
    lines=[]
    for line in ser.readlines(): # while there's a response
        lines.append(line.decode('utf-8').strip())
    if not silent:
        print("\n".join(lines))
        print('-'*60)
    return lines

def getTemp(ser,address='0x91',silent=True,fahrenheit=False):
    """return the temperature read from an LM75"""
    unit=" F" if fahrenheit else " C"
    lines=send(ser,'[%s r:2]'%address,silent=silent) # read two bytes
    for line in lines:
        if line.startswith("READ:"):
            line=line.split(" ",1)[1].replace("ACK",'')
            while "  " in line:
                line=" "+line.strip().replace("  "," ")
            line=line.split(" 0x")
            val=int("".join(line),16)
            # conversion to C according to the datasheet
            if val < 2**15:
                val = val/2**8
            else:
                val =  (val-2**16)/2**8
            if fahrenheit:
                val=val*9/5+32
            print("%.03f"%val+unit)
            return val

# the speed of sequential commands is determined by this timeout
ser=serial.Serial(BUSPIRATE_PORT, 115200, timeout=.1)

# have a clean starting point
send(ser,'#',silent=True) # reset bus pirate (slow, maybe not needed)
#send(ser,'v') # show current voltages

# set mode to I2C
send(ser,'m',silent=True) # change mode (goal is to get away from HiZ)
send(ser,'4',silent=True) # mode 4 is I2C
send(ser,'3',silent=True) # 100KHz
send(ser,'W',silent=True) # turn power supply to ON. Lowercase w for OFF.
send(ser,'P',silent=True) # enable pull-up resistors
send(ser,'(1)') # scan I2C devices. Returns "0x90(0x48 W) 0x91(0x48 R)"

data=[]
try:
    print("reading data until CTRL+C is pressed...")
    while True:
        data.append(getTemp(ser,fahrenheit=True))
except:
    print("exception broke continuous reading.")
    print("read %d data points"%len(data))

ser.close() # disconnect so we can access it from another app

plt.figure(figsize=(6,4))
plt.grid()
plt.plot(data,'.-',alpha=.5)
plt.title("LM75 data from Bus Pirate")
plt.ylabel("temperature")
plt.xlabel("number of reads")
plt.show()

print("disconnected!") # let the user know we're done.

```

### __Experiment: Measuring Heater Efficacy__

This project now now ready for an actual application test. I made a simple heater circuit which could be driven by an analog input, PWM, or digital ON/OFF. Powered from 12V it can pass 80 mA to produce up to 1W of heat. This may dissipate up to 250 mW of heat in the transistor if partially driven, so keep this in mind if an analog signal drive is used (i.e., thermistor / op-amp circuit). Anyhow, I soldered this up with SMT components on a copper-clad PCB with slots drilled on it and decided to give it a go. It's screwed tightly to the temperature sensor board, but nothing special was done to ensure additional thermal conductivity. This is a pretty crude test.

### Drilled Slots Facilitate SMT Placement
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_000.jpeg)

</div>

### All Components Soldered
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_001.jpeg)

</div>

### Heater Mates with Sensor Board
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_003.jpeg)

</div>

### Headers are Easily Accessible
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_002.jpeg)

</div>

### LED Indicates Heater Current
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_004.jpeg)

</div>

### Styrofoam Igloo
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_005.jpeg)
![](https://swharden.com/static/2017/02/04/File_006.jpeg)

</div>

### Temperature Control Circuit
<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/File_007.jpeg)

</div>

__I ran an experiment to compare open-air heating/cooling vs. igloo conditions, as well as low vs. high heater drive conditions.__ The graph below shows these results. The "heating" ranges are indicated by shaded areas. The exposed condition is when the device is sitting on the desk without any insulation. A 47k resistor is used to drive the base of the transistor (producing less than maximal heating). I then repeated the same thing after the device was moved inside the igloo. I killed the heater power when it reached the same peak temperature as the first time, noticing that it took less time to reach this temperature. Finally, I used a 1k resistor on the base of the transistor and got near-peak heating power (about 1W). This resulted in faster heating and a higher maximum temperature. If I clean this enclosure up a bit, this will be a nice way to test software-based [PID temperature control](https://en.wikipedia.org/wiki/PID_controller) with slow PWM driving the base of the transistor.

<div class="text-center">

![](https://swharden.com/static/2017/02/04/experiment2.png)

</div>

Code to create file logging (csv data with timestamps and temperatures) and produce plots lives in the 'file logging' folder of the Bus Pirate LM75A project on the GitHub page.

### __Experiment: Challenging LM7805 Thermal Shutdown__

The ubiquitous LM7805 linear voltage regulator offers internal current limiting (1.5A) and thermal shutdown. I've wondered for a long time if I could use this element as a heater. It's TO-220 package is quite convenient to mount onto enclosures. To see how quickly it heats up and what temperature it rests at, screwed a LM7805 directly to the LM75A breakout board (with a dab of thermal compound). I soldered the output pin to ground (!!!) and recorded temperature while it was plugged in.

[gallery size="medium" link="file" ids="6449,6450,6451"]

Power (12V) was applied to the LM7805 over the red-shaded region. It looks like it took about 2 minutes to reach maximum temperature, and settled around 225F. After disconnecting power, it settled back to room temperature after about 5 minutes. I'm curious if this type of power dissipation is sustainable long term...

<div class="text-center">

![](https://swharden.com/static/2017/02/04/data.png)

</div>

### Update: Reading LM75A values directly into an AVR

This topic probably doesn't belong inside this post, but it didn't fit anywhere else and I don't want to make it its own post. Now that I have this I2C sensor mounted where I want it, I want a microcontroller to read its value and send it (along with some other data) via serial USART to an FT232 (USB serial adapter). Ultimately I want to take advantage of its comparator thermostat function so I can have a USB-interfaced PC-controllable heater with multiple LM75A ICs providing temperature readings at different sites in my project. To do this, I had to write code to interface my microcontroller to the LM75A. I am using an ATMega328 (ATMega328P) with AVR-GCC (_not_ Arduino). Although there are multiple LM75A senor libraries for Arduino [[link](https://github.com/QuentinCG/Arduino-LM75A-Temperature-Sensor-Library)] [[link](https://github.com/thefekete/LM75)] [[link](https://piandmore.wordpress.com/2016/09/21/arduino-and-lm75a/)] I couldn't find any examples which didn't rely on Arduino libraries. I ended up writing functions around [g4lvanix's L2C-master-lib](https://github.com/g4lvanix/I2C-master-lib).

<div class="text-center">

![](https://swharden.com/static/2017/02/04/circuit2.jpg)

</div>

__Here's a relevant code snippit.__ See the full code (with compile notes) on [this GitHub page](https://github.com/swharden/AVR-projects/tree/master/ATMega328%202017-02-08%20i2c%20LM75A%20thermometer):

```c
uint8_t data[2]; // prepare variable to hold sensor data
uint8_t address=0x91; // this is the i2c address of the sensor
i2c_receive(address,data,2); // read and store two bytes
temperature=(data[0]*256+data[1])/32; // convert two bytes to temperature

```

<div class="text-center img-border">

![](https://swharden.com/static/2017/02/04/circuit.jpg)

![](https://swharden.com/static/2017/02/04/demo-1.png)

</div>

This project is on GitHub: https://github.com/swharden/AVR-projects