---
title: TENMA Multimeter Serial Hack
date: 2016-08-24 03:08:28
tags: ["python", "obsolete"]
---

# TENMA Multimeter Serial Hack

__I just spent the afternoon reverse-engineering the 72 series TENMA multimeter serial interface,__ and can now access all of its readings from a standalone Python script. This lets me send all measurements made with the multimeter to my computer in real time (using an optically isolated connection), and eliminates the need for the TENMA PC interface software. In addition to allowing the development of custom software to use measurements from TENMA multimeters in real time, this project also lets allows TENMA multimeters to interface with Linux computers (such as the raspberry pi). 

**I have owned a [TENMA 72-7750](http://www.farnell.com/datasheets/1955368.pdf?_ga=1.217276502.1323514874.1471841353) multimeter for several years, and over all I've been happy with it!** To be honest, 90% of my multimeter needs are just using a continuity tester or checking to see if there is voltage on a line. For _checking_ electrical signals, I love my no-name (actually it's branded "KOMEC") $15 eBay special multimeter. The screen updates about 4 times a second, and I don't care if it's off by 10%, it's cheap and light and fast and easy for simple tasks. However, when I'm going to use a multimeter to actually _measure_ something, I reach for a higher quality meter like my TENMA 72-7750. Although [similar TENMA models may be more popular](http://www.newark.com/MarketingProductList?storeId=10194&catalogId=15003&langId=-1&orderCode=02J5540,02J5541,02J5542,02J5543,02J5546), I went with this particular one because it could measure frequency which is convenient when building RF circuits. While big fancy frequency counters are nice to have on your workbench, I liked the idea of having that functionality built into my multimeter. I believe my particular model is discontinued, but it looks like the 72-7745 is a similar product, and there are [many TENMA multimeters on Amazon](https://www.amazon.com/s/field-keywords=tenma+multimeter). Back in April of 2013 I mentioned on my website that I'd consider writing interface software in Python. Now that I'm [finally] out of school and have a little more free time, I decided to pick up the project again. I ran into a few tangles along the way, but I'm happy to report this project is now working beautifully! The [pyTENMA project](https://github.com/swharden/pyTENMA) is open-sourced on my GitHub. I'm excited to see what kind of data I can get out of this thing!

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/24/IMG_7956.jpg)

</div>

**This is my multimeter taking a measurement (resistance) and sending the data to my computer using the optically-isolated serial connector (which ships with the multimeter).** In this picture, it's interacting with the official TENMA software. To try to figure out what was going on, I probed pins of the serial port while data was being exchanged. The yellow trace is the data signal. 

__There was a problem, and this problem took me hours to figure it out,__ but now that I realize what's going on it seems so obvious. The problem was that I could never get the multimeter to send my Python script data, despite the fact that the exact same configuration would send the commercial program data. I used serial port sniffing software to view the data too! I matched the baud rate (19200 / 19230), data bits (7), and parity (odd), and I just couldn't figure out why the heck this thing wouldn't work. I resorted to using an oscilloscope to probe the pins of the serial cable directly. I made a small man-in-the-middle test jig to give me headers I could easily probe or solder wires to. After poking around, I learned two things. (1) I really need a logic analyzer. They're so cheap now, I went ahead and ordered one. (2) The RTS line goes low and the DSR line goes high when data is being sent. I realized that the Python software was disregarding these pins. You wouldn't _think_ you needed them if you're just going to be receiving data with software control... but I immediately realized that those pins may be important for powering the optoelectronics (likely a phototransistor and some passive components) underlying the data exchange. After all, it's not like the multimeter is able to source or sink appreciable current through an optical connection! I'll note that some [sketchy schematics](http://hackaday.com/2014/12/05/fixing-a-multimeters-serial-interface/) are floating around Hackaday (pun intended), but the [web page they link to](http://www.wattnotions.com/tenma-72-7735-serial-interface/) doesn't look very complete so I'm not sure how far that author got toward the same endeavor I'm chasing.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/24/IMG_7961.jpg)

</div>

__Here you can see some of the adjacent (non-data) pins change their voltage state during transmissions. Once I realized replicating these states was also necessary, everything quickly fell into place.__ After manually commanding the RTS pin to lie low (1 line of code), the data starting coming in! I finished writing a basic pyTENMA class (which does a lot of hardware detection, string parsing, etc. to generate simple no-nonsense value/unit pairs to return to the user as well as log values to disk automatically) and tried to make it as simple as possible. Without going into too much detail ([see the note in the top of my source code for more information](https://github.com/swharden/pyTENMA/blob/master/pyTENMA.py)), the multimeter just sends a 9-character ASCII string every second. I refer to this string as ABBBBCDEF. Byte 1 is a multiplier and bytes 2-5 are the value displayed on the screen. The actual value of a read is BBBB*10^A. The units depend on the mode (resistance, capacitance, etc), which is indicated by byte 6. It's a little funny in that "4" means temperature and ";" means voltage, but once I figured out (through trial and error) which symbols match with which mode it was pretty easy to make it work for me. D is the sign (negative, zero, or positive), and I still haven't really figured what E and F are. I thought they might be things like backlight or perhaps indicators of the range setting. I didn't care to figure it out, because I already had access to the data I wanted!

__To use the pyTENMA script, just drop it alongside a Python script you want to work on.__ Import it, tell it a COM port to use (if not, it'll try to guess one) and a log file (optional). This is all the code you need:

```python
import pyTENMA # make sure pyTENMA.py is in the same folder
PT=pyTENMA.pyTenma("COM4","log.txt")
PT.readUntilBroken()
```

__The output is very simple.__ Here it is compared to the commercial TENMA software. [PyroElectro has a good demonstration](http://www.pyroelectro.com/tutorials/tenma_digital_multimeter/software.html) of the PC interface software that ships with this unit. While the TENMA software is functional, it has some serious limitations that motivate me to improve upon it. (1) It's Windows only. (2) It doesn't automatically log data (you have to manually click save to write it to disk). (3) It seems to be limited to COM1-COM4. My USB serial adapter was on COM7 and inaccessible to this program. I had to go in the device manager and change the advanced settings to allow the commercial software to read my device. (4) The graphs are poor, non-interactive, and often broken. (5) Data output format is only an Excel spreadsheet (.xls), and I don't have control to save in other formats like CSV. If I'm going to use this on a raspberry pi, I don't want to fumble around with Microsoft Office! Yeah I know I can get modules (even for Python) to access data in excel spreadsheets, but it seems like an unnecessary complexity just to retrieve some voltage readings. Over all it seems a little unfortunate that a relatively great product is pulled down when its weakest link is its software. It's okay, we are on our way to can fixing this with [pyTENMA](https://github.com/swharden/pyTENMA)!

<div class="text-center img-border img-small">

![](https://swharden.com/static/2016/08/24/screenshot.jpg)
![](https://swharden.com/static/2016/08/24/commercialSoftware.jpg)

</div>

## Measuring Capacitor Leakage

__I set up an experiment to demonstrate how logging data works.__ I charged a 22uF capacitor on a breadboard and let it sit there disconnected, slowly draining through leakage (and perhaps micro current draw from the multimeter). After a while I slowly charged it (using my body as a resistor, touching the +5V line and touching the capacitor lead with my fingers) and watched it discharge again. You can set pyTENMA software to save as little or often as you want. It defaults to every 10 reads, but I adjust it to every 100 reads for longer experiments. Also note that if you break it (with CTRL+C) it gently disconnects the serial device, logs remaining data to disk, then exits gracefully.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/24/IMG_7981.jpg)

</div>

__In this demonstration,__ voltage across the capacitor on the breadboard is being measured by the multimeter, and reported (and logged) in real time by pyTENMA seen on the screen. Here is what that data looks like after about a half hour of run time. The code to read the log file and make graphs from it (using numpy and matplotlib) is in the [logPlot source code](https://github.com/swharden/pyTENMA/blob/master/extras/logPlot.py).

<div class="text-center img-medium">

![](https://swharden.com/static/2016/08/24/logDemo.png)

</div>

## Measuring OCXO Warm-Up

__Now that I know everything is up and running, I can use this device to make some measurements I'm actually interested in!__ In reality, this usage case is the _reason_ I went through all the trouble to write custom data logging software for this multimeter is specifically for this case. I'm working on a large project involving a GPS-disciplined oven controlled crystal oscillator (OCXO) for a 1pps frequency reference, and spoiler alert it involves a raspberry pi to plot and upload live graphs of real-time frequency and accuracy statistics to my website. I don't want to discuss it yet (it's not complete), but I can't avoid mentioning it since I'm showing photos of it. I'll surely make a follow-up post when that project is complete and well documented. For now, the only relevant thing is that the device is an oven which takes a lot of current to heat from room temperature to a high temperature, and a smaller amount of current to maintain it at that temperature. I wanted to know how long it takes the current to stabilize over time (on a scale of hours), determine if its current draw oscillates, and also assess what the voltage at the oscillator reads during warm-up (high current draw) vs. stable conditions.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/24/FullSizeRender-2.jpg)

</div>

__My test setup uses the TENMA multimeter in current measuring configuration.__ Note the configuration of the multimeter test leads as being in series with the power supply.  This meter has two current measurement settings, one for <600 mA and one for up to 10 A. I know that the oscillator draws about 2 A during warm-up (this is because I'm intentionally limiting it to 2A), and stabilizes to somewhere near 200 mA after several minutes. To maximize my sample resolution, I started the recording using the 10 A setting, then after it dropped well below 600 mA I switched to the lower current setting. The data is colored red and blue, respectively:

current stabilizes within 10 minutes:

<div class="text-center">

![](https://swharden.com/static/2016/08/24/ocxo-1.png)

</div>

Current is maxed-out for a few minutes, oscillates then stabilizes. 10 A / 600 mA measuring settings are in red and blue (respectively):

<div class="text-center">

![](https://swharden.com/static/2016/08/24/ocxo-2.png)

</div>

once stable, current draw is stable for hours

<div class="text-center">

![](https://swharden.com/static/2016/08/24/ocxo-3.png)

</div>

__I concluded that this thing stabilizes to within 10% of its final current draw well within 10 minutes.__ From there, it seems really stable, but slowly oscillates on a time scale of tens of minutes. I suspect this correlates with the AC unit of my house turning on and off. A similar recording of temperature of the oscillator (which the TENMA 72-7750 can also do with the thermocouple it was shipped with) may provide more insight as to whether or not the oscillator itself is actually changing temperature during these current oscillations. Now I'm curious what the voltage does during the warm-up period while the current is maxed out. I guess I need to reveal that my current limit is provided by two parallel LM7809 voltage regulators each in series with a 2 Ohm current limiting resistor before connecting to a common +9V rail which is running the oscillator. Since each regulator is current limited to about 1A, it's no surprise my maximum current is about 2A, but I'd be interested to learn what the voltage is doing during that period.

<div class="text-center img-border">

![](https://swharden.com/static/2016/08/24/FullSizeRender-3.jpg)

</div>

I measured voltage just downstream of the voltage regulators:
<div class="text-center">

![](https://swharden.com/static/2016/08/24/mV1.png)

</div>

During current max-out, the voltage is <<9V
<div class="text-center">

![](https://swharden.com/static/2016/08/24/mV2.png)

</div>

Voltage stabilizes after about 10 minutes
<div class="text-center">

![](https://swharden.com/static/2016/08/24/mV3.png)

</div>

__I am interested in seeing what of these measurements (with more such as temperature and OCXO frequency) look like when they are all measured simultaneously.__ The TENMA multimeter I'm using can't measure voltage and current at the same time (which would require a third lead, if you think about it), so this solution will require alternative equipment. Stay tuned, because I have a cool solution for that in the works! For now, I couldn't be happier with my TENMA multimeter's ability to log data to text files using [pyTENMA](https://github.com/swharden/pyTENMA) and the ease in which numpy/matplotlib can read and graph them. A data logging multimeter is a great tool to have in any engineer's toolbox, and I'm glad I now have one that plays nicely with Python.

## Resources

* pyTENMA on GitHub: [github.com/swharden/pyTENMA](https://github.com/swharden/pyTENMA)