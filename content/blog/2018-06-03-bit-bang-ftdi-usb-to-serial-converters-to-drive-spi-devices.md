---
title: Bit-Bang FTDI USB-to-Serial Converters to Drive SPI Devices
date: 2018-06-03 18:51:30
tags: ["csharp", "microcontroller"]
---

# Bit-Bang FTDI USB-to-Serial Converters to Drive SPI Devices

**The FT232 USB-to-serial converter is one of the most commonly-used methods of adding USB functionality to small projects, but recently I found that these chips are capable of sending more than just serial signals. With some creative programming, individual output pins can be big-banged to emulate a clock, data, and chip select line to control SPI devices.** This post shares some of the techniques I use to bit-bang SPI with FTDI devices, and some of the perks (and quirks) of using FTDI chips to bit-bang data from a USB port. Code examples are [available](https://github.com/swharden/AVR-projects/tree/master/FTDI%202018-05-30%20bit%20bang) on GitHub, and links to additional resources are at the bottom of this post. After the final build I created a slightly more polished "ftdiDDS.exe" program to control an AD9850 frequency synthesizer from the command line by bit-banging a FT-232, and code (and binaries) are also [available](https://github.com/swharden/AVR-projects/tree/master/FTDI%202018-06-03%20ftdiDDS) on GitHub.

![](https://www.youtube.com/embed/QkHsryvDZfo)

## Why Bit-Bang FTDI Pins?

The main reason I like using FTDI devices is because when you plug them in to a modern computer, they just start working! You don't have to worry about drivers, driver versions, driver signing, third party drivers - most of the time it just does what it's supposed to do with no complexity. If I'm going to build a prototype device for a client, a FT-232 USB to serial converter is the way to go because I can be confident that when they plug in, their device will start working right away. Yeah, there are third party drivers to get extra open-sourcey functionality from FTDI devices ([libFTDI](https://www.intra2net.com/en/developer/libftdi/)), but I don't want to ask a client (with unknown tech-savviness) to install third-party unsigned drivers before plugging my device in (and heaven forbid the product doesn't work in their hands and I have to ask them to verify the device is actually using the third-party drivers and not defaulting back to the official ones). In this project I seek to use only the generic, default, officially-supported FTDI driver and API access will be provided by [libftd2xx](http://www.ftdichip.com/Drivers/D2XX.htm). Don't forget that USB ports supply 5V and GND, so in most cases you can power your project just from the USB port! All-in-all, the FT-232 is a great way to give a small device USB functionality. This post explores how to use it for more than just sending and receiving serial data...

### FT-232R Breakout Board
<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/232r.png)

</div>

### FT-232H Breakout Board
<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/232h.png)

</div>

### TTL-FT232R Cable
<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/ttl-ft232r-cable.png)

</div>

## Controlling FTDI Devices with C# 

The goal of this post is not to describe every detail about how to control FTDI chips. Instead, the key points of the software are described here (and in the video) so you can get the gist of the main concepts. If you're interested in additional detail, [full code examples are provided on the GitHub folder for this project](https://github.com/swharden/AVR-projects/tree/master/FTDI%202018-05-30%20bit%20bang). All code examples were tested with Visual Studio Community 2017, are written in C#, and uses the FTD2XX_NET library installed with NuGet. Also, see the list of resources (including official FTDI datasheets and application notes) at the bottom of this post.

__This block of code attaches to FTDI device 0 (the first FTDI device it sees) and sends the letter "a" using a traditional serial protocol.__ Since this code connects to the first FTDI device it finds, this could be a problem if you have more than 1 FTDI device attached. Alternatively you could have your program connect to a specific FTDI device (e.g., by its serial number). To see what FTDI devices are attached to your computer (and see or set their serial numbers), use the FT_Prog application [provided by FTDI](http://www.ftdichip.com/Support/Utilities.htm). Also, [see the code I use to list FTDI devices](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-06-03%20ftdiDDS/source/FTDI-video-demo/Program.cs#L87-L107) from inside a C# program ftdiDDS program.

_Full code is [on GitHub](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-05-30%20bit%20bang/00-serial.cs)_

```cs
public static FTDI ftdi = new FTDI();
public static FTDI.FT_STATUS ft_status = FTDI.FT_STATUS.FT_OK;
public static UInt32 bytesWritten = 0;

static void Main(string[] args)
{
    ft_status = ftdi.OpenByIndex(0);
    ft_status = ftdi.SetBaudRate(9600);
    string data = "a";
    ft_status = ftdi.Write(data, data.Length, ref bytesWritten);
}

```

# LED Blink by Bit-Banging FTDI Pins

__Here is a minimal complexity LED blink example. This code block alternates between writing 0 (all pins off) and 1 (TX pin high) over and over forever. __Note that `` ftdi.SetBitMode `` is what frees the FTDI chip from sending serial data when `` ftdi.Write() `` gets called. The 255 is a byte mask which tells all 8 pins to be outputs (by setting all 8 bits in the byte to 1, hence 255). Setting bit mode to 1 means we are using asynchronous bit bang bode (sufficient if we don't intend to read any pin states). For full details about these (and other) bit-bang settings, check out the [Bit Bang Modes for the FT232R](http://www.ftdichip.com/Support/Documents/AppNotes/AN_232R-01_Bit_Bang_Mode_Available_For_FT232R_and_Ft245R.pdf) application note.

_Full code is [on GitHub](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-05-30%20bit%20bang/03-state-LEDblink.cs)_

```cs
ft_status = ftdi.OpenByIndex(0);
ft_status = ftdi.SetBitMode(255, 1);
ft_status = ftdi.SetBaudRate(9600);
int count = 0;

while (true)
{
    byte[] data = { (byte)(count++%2) };
    ft_status = ftdi.Write(data, data.Length, ref bytesWritten);
    System.Threading.Thread.Sleep(100);
}

```

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/DSC_0023.jpg)

</div>

# Bit-Bang SPI with a FT232

In reality all we want to send to SPI devices are a series of numbers which we can place in a byte array. These numbers are transmitted by pulling-low a clip select/enable line, setting a data line (high or low, one bit at a time) and sliding the clock line from low to high. At a high level we want a function to just take a byte array and bit-bang all the necessary SPI signals. At a low level, we need to set the state for every clock cycle, bit by bit, in every byte of the array. For simplify, I use a `` List<byte> `` object to collect all my pin states. Then I convert it to an array right before sending it with `` ftdi.Write() ``.

_Full code is [on GitHub](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-05-30%20bit%20bang/06-bit-bang-spi.cs)_

```cs
List<byte> bytesToSend = new List<byte>();
bytesToSend.Add(123); // just
bytesToSend.Add(111); // some
bytesToSend.Add(222); // test
bytesToSend.Add(012); // data

BitBangBytes(bytesToSend.ToArray());

// given a byte, return a List<byte> of pin states
public static List<byte> StatesFromByte(byte b)
{
    List<byte> states = new List<byte>();
    for (int i=0; i<8; i++)
    {
        byte dataState = (byte)((b >> (7-i)) & 1); // 1 if this bit is high
        states.Add((byte)(pin_data * dataState)); // set data pin with clock low
        states.Add((byte)(pin_data * dataState | pin_clock)); // pull clock high
    }
    return states;
}

// given a byte array, return a List<byte> of pin states
public static List<byte> StatesFromByte(byte[] b)
{
    List<byte> states = new List<byte>();
    foreach (byte singleByte in b)
        states.AddRange(StatesFromByte(singleByte));
    return states;
}

// bit-bang a byte array of pin states to the opened FTDI device
public static void BitBangBytes(byte[] bytesToSend)
{
    List<byte> states = StatesFromByte(bytesToSend);

    // pulse enable to clear what was there before
    states.Insert(0, pin_enable);
    states.Insert(0, 0);

    // pulse enable to apply configuration
    states.Add(pin_enable);
    states.Add(0);
    ft_status = ftdi.Write(states.ToArray(), states.Count, ref bytesWritten);
}

```

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/DSC_0046.jpg)

</div>

# Bit-Bang Control of an RF Synthesizer

__The AD9850 is a SPI-controlled DDS (Direct Digital Synthesizer) capable of generating sine waves up to 65 MHz and is available on breakout boards for around $20__ on eBay and Amazon. It can be programmed with SPI by sending 40 bits (5 bytes), with the first 4 bytes being a frequency code (LSB first) and the last byte controls phase.

__To calculate the code required for a specific frequency,__ multiply your frequency by 4,294,967,296 (2^32 - 1) then divide that number by the clock frequency (125,000,000). Using this formula, the code for 10 MHz is the integer 343,597,383. In binary it's 10100011110101110000101000111, and since it has to be shifted in LSB first (with a total of 40 bits) that means we would send 11100010100001110101111000101000 followed by the control byte which can be all zeros. In C# using the functions we made above, this looks like the following.

_Full code is [on GitHub](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-05-30%20bit%20bang/07-AD9850-single-frequency.cs)_

```cs
int freqTarget = 12_345_678; // 12.345678 MHz
ulong freqCode = (ulong)freqTarget * (ulong)4_294_967_296;
ulong freqCrystal = 125_000_000;
freqCode = freqCode / freqCrystal;
bytesToSend.Add(ReverseBits((byte)((freqCode >> 00) & 0xFF))); // 1 LSB
bytesToSend.Add(ReverseBits((byte)((freqCode >> 08) & 0xFF))); // 2
bytesToSend.Add(ReverseBits((byte)((freqCode >> 16) & 0xFF))); // 3
bytesToSend.Add(ReverseBits((byte)((freqCode >> 24) & 0xFF))); // 4 MSB
bytesToSend.Add(0); // control byte
BitBangBytes(bytesToSend.ToArray());

```

<div class="text-center img-border img-small">

![](https://swharden.com/static/2018/06/03/ad9850-SPI-DDS.png)
![](https://swharden.com/static/2018/06/03/scope-output.png)

</div>

If somebody wants to get fancy and create a quadrature sine wave synthesizer, one could do so with two AD9850 boards if they shared the same 125 MHz clock. The two crystals could be programmed to the same frequency, but separated in phase by 90º. This could be used for quadrature encoding/decoding of single sideband (SSB) radio signals. This method may be used to build a direct conversion radio receiver ideal for receiving CW signals while eliminating the undesired sideband. This technique is described [here](https://www.eetimes.com/document.asp?doc_id=1224754), [here](https://pdfs.semanticscholar.org/9ca4/d7b29b33ff47bde4945af854416ff0f0a9db.pdf), and [here](http://www.cs.tut.fi/kurssit/TLT-5806/RecArch.pdf).

# Polishing the Software

Rather than hard-coding a frequency into the code, I allowed it to accept this information from command line arguments. I did the same for FTDI devices, allowing the program to scan/list all devices connected to the system. Now you can command a particular frequency right from the command line. I didn't add additional arguments to control frequency sweep or phase control functionality, but it would be very straightforward if I ever decided to. __I called this program "ftdiDDS.exe" and it is tested/working with the FT-232R and FT-232H, and likely supports other FTDI chips as well.__

### Download ftdiDDS

*   64-bit Windows binary: [ftdiDDS.exe](https://github.com/swharden/AVR-projects/blob/master/FTDI%202018-06-03%20ftdiDDS/ftdiDDS.zip)
*   Source code: [ftdiDDS on GitHub](https://github.com/swharden/AVR-projects/tree/master/FTDI%202018-06-03%20ftdiDDS)

### Command Line Usage:

*   `` ftdiDDS -list `` _lists all available FTDI devices_
*   `` ftdiDDS -mhz 12.34 `` _sets frequency to 12.34 MHz_
*   `` ftdiDDS -device 2 -mhz 12.34 `` _specifically control device 2_
*   `` ftdiDDS -sweep `` _sweep 0-50 MHz over 5 seconds_
*   `` ftdiDDS -help `` _shows all options including a wiring diagram_

<div class="text-center">

![](https://swharden.com/static/2018/06/03/console.jpg)

</div>

# Building an Enclosure

Although my initial goal for this project was simply to figure out how to bit-bang FTDI pins (the AD9850 was a SPI device I just wanted to test the concept on), now that I have a command-line-controlled RF synthesizer I feel like it's worth keeping! I threw it into an enclosure using my standard methods. I have to admit, the final build looks really nice. I'm still amused how simple it is.

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/enclosed.png)
![](https://swharden.com/static/2018/06/03/dds-desk.jpg)

</div>

# Beware of the FT232R Bit Bang Bug

__There is a serious problem with the FT-232R that affects its bit-bang functionality, and it isn't mentioned in the datasheet.__ I didn't know about this problem, and it set me back _years_! I tried bit-banging a FT-232R several years ago and concluded it just didn't work because the signal looked so bad. This week I learned it's just a bug (present in every FT-232R) that almost nobody talks about!

__Consider trying to blink a LED with { 0, 1, 0, 1, 0 }__ sent using `` ftdi.Write() `` to the FT-232R. You would expect to see two pulses with a 50% duty. Bit-banging two pins like this { 0, 1, 2, 1, 2, 0 } one would expect the output to look like two square waves at 50% duty with opposite phase. This just... isn't what we see on the FT-232R. The shifts are technically correct, but the timing is all over the place. The identical code, when run on a FT-232H, presents no timing problems - the output is a beautiful

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/232h-scope.jpg)

</div>

__The best way to demonstrate how "bad" the phase problem is when bit-banging the FT232R is seen when trying to send 50% duty square waves.__ In the photograph of my oscilloscope below, the yellow trace is supposed to be a "square wave with 50% duty" (ha!) and the lower trace is supposed to be a 50% duty square wave with half the frequency of the top (essentially what the output of the top trace would be if it were run through a flip-flop). The variability in pulse width is so crazy that initially I mistook this as 9600 baud serial data! Although the timing looks wacky, the actual shifts are technically correct, and the FT-232R can still be used to bit-bang SPI.

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/232r-scope2.jpg)

</div>

**Unfortunately this unexpected behavior is not documented in the datasheet,** but it is referenced in section 3.1.2 of the [TN\_120 FT232R Errate Technical Note](http://www.ftdichip.com/Support/Documents/TechnicalNotes/TN_120_FT232R%20Errata%20Technical%20Note.pdf) where it says "_The output may be clocked out at different speeds ... and can result in the pulse widths varying unexpectedly on the output._" Their suggested solution (I'll let you read it yourself) is a bit comical. It's essentially says "to get a 50% duty square wave, send a 0 a bunch of times then a 1 the same number of times". I actually tried this, and it is only square-like when you send each state about 1000 times. The data gets shifted out 1000 times slower, but if you're in a pinch (demanding squarer waves and don't mind the decreased speed) I guess it could work. Alternatively, just use an FT-232H.

__Update (2018-10-05):__ YouTube user Frederic Torres said this issue goes away when externally clocking the FT232R chip. It's not easy to do on the breakout boards, but if you're spinning your own PCB it's an option to try!

# Alternatives to this Method

Bit-banging pin states on FTDI chips is a cool hack, but it isn't necessarily the best solution for every problem. This section lists some alternative methods which may achieve similar goals, and touches on some of their pros and cons.

*   [LibFTDI](https://www.intra2net.com/en/developer/libftdi/) - an alternative, open-source, third party driver for FTDI devices. Using this driver instead of the default FTDI driver gives you options to more powerful commands to interact with FTDI chips. One interesting option is the simple ability to interact with the chip from Python with [pyLibFTDI](https://pylibftdi.readthedocs.io/en/0.15.0/).While this is a good took for hackers and makers, if I want to build a device to send to a lay client I won't want to expect them to fumble with installing custom drivers or ensure they are being used over the default ones FTDI supplies. I chose not to pursue utilizing this project because I value the "plug it in and it just works" functionality that comes from simply using FTDI's API and drivers (which are automatically supplied by Windows)

*   [Raspberry PI can bit-bang SPI](https://raspberrypi-aa.github.io/session3/spi.html) - While perhaps not ideal for making small USB devices to send to clients, if your primary goal is just to control a SPI device from a computer then definitely consider using a Raspberry Pi! A few of the pins on its header are capable of SPI and can even be driven directly from the bash console. I've [used this technique](https://www.swharden.com/wp/2016-09-28-generating-analog-voltages-with-the-raspberry-pi/) to generate analog voltages from a command line using a Raspberry PI to send SPI commands to a MCP4921 12-bit DAC.

*   [Multi-Protocol Synchronous Serial Engine (MPSSE)](http://www.ftdichip.com/Support/Documents/AppNotes/AN_135_MPSSE_Basics.pdf) - Some FTDI chips support MPSSE, which can send SPI (or I2C or other) protocols without you having to worry about bit-banging pins. I chose not to pursue this option because I wanted to use my FT232R (one of the most common and inexpensive FTDI chips), which doesn't support MPSSE. ALthough I do have a FT232H which does support MPSSE ([example project](http://www.ftdichip.com/Support/Documents/AppNotes/AN_180_FT232H%20MPSSE%20Example%20-%20USB%20Current%20Meter%20using%20the%20SPI%20interface.pdf)), I chose not to use that feature for this project, favoring a single code/program to control all FTDI devices.

*   [Bus Pirate](http://dangerousprototypes.com/docs/Bus_Pirate) - If you don't have a Bus Pirate already, [get one!](https://www.seeedstudio.com/s/bus%20pirate.html) It's one of the most convenient ways to get a new peripheral up and running. It's a USB device you can interact with through a serial terminal (supplied using a FTDI usb-to-serial converter, go fig) and you can tell it to send/receive commands to SPI or I2C devices. It does a lot more, and is worth checking out.

# Resources

*   [Saleae logic analyzers](https://www.saleae.com) - The official Saleae hardware (not what was shown in my video, which was a cheap eBay knock-off) can do a lot of great things. Their free software is _really _simple to use, and they haven't gone out of their way to block the use of third-party logic analyzers with their free software. If you are in a place where you can afford to support this company financially, I suggest browsing their products and purchasing their official hardware.

*   [DYMO Letra-Tag LT100-H label maker](https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=Dymo+LetraTag+LT100-H&rh=i%3Aaps%2Ck%3ADymo+LetraTag+LT100-H) and [clear tape](https://www.amazon.com/Genuine-Polyester-LetraTAG-LetraTag-LT100H/dp/B01M9CPJGK/) - When labels are printed with black boxes around them (a tip I learned from [Onno](http://www.qsl.net/pa2ohh/)) they look fantastic when placed on project boxes! Don't buy the knock-off clear labels, as they aren't truly clear. The clear tape you need to purchase has the brand name "DYMO" written on the tape dispenser.

*   [FT232H breakout board](https://www.adafruit.com/product/2264) (adafruit) - This is where I got the FT232H board used in this video. You can find additional [similar FT232H breakout boards on Amazon](https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=ft232h).

*   [FT232R breakout board](https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=ft232r&rh=i%3Aaps%2Ck%3Aft232r) - Everyone sells these. I got some lately on Amazon, but I've gotten them before on eBay too.

*   [TTL-232R cable](http://www.ftdichip.com/Support/Documents/DataSheets/Cables/DS_TTL-232R_CABLES.pdf) - If you're making a device which you want to appear a bit more professional, this cable has the FT232R built-in and it just has several pins (in a female header) you can snap onto your board.

*   [Bit Bang Modes for the FT232R](http://www.ftdichip.com/Support/Documents/AppNotes/AN_232R-01_Bit_Bang_Mode_Available_For_FT232R_and_Ft245R.pdf) - FTDI datasheet detailing how to Bit-Bang the FT232R chip. In practice, the terms, language, and code examples in this datasheet seem similar enough to the FT232H that it probably is all you need to get started, since it's the large-scale concepts which are most important.

*   [Introduction to the FTDI BitBang mode](https://hackaday.com/2009/09/22/introduction-to-ftdi-bitbang-mode/) - A Hack-A-Day article from 2009 mentions FTDI chips can be used to bit-bang pin states and they have their own LED blink examples. Their article does hint at using this method to bit-bang SPI, but it fails entirely to note the FT232R bug that surely has confused multiple people in the past...

*   [FT232R BitBang SPI example](http://jdelfes.blogspot.com/2014/02/spi-bitbang-ft232r.html) - This code uses [libftdi](https://www.intra2net.com/en/developer/libftdi/), not the default driver supplied by FTDI ([libftd2xx](http://www.ftdichip.com/Drivers/D2XX.htm)).

*   [FT232R BitBang mode is broken](http://blog.bitheap.net/2012/03/ft232r-bitbang-mode-is-broken.html) - an article from 2012 detailing how bad the timing is when bit-banging pin states on the FT232R.

*   Official acknowledgement of the FT232R timing problem is described in the [TN\_120 FT232R Errate Technical Note](http://www.ftdichip.com/Support/Documents/TechnicalNotes/TN_120_FT232R%20Errata%20Technical%20Note.pdf) in section 3.1.2 where they state the problem as: "_The output may be clocked out at different speeds to allow for different pulse widths. However this clocking stage is not synchronized with the incoming data and can result in the pulse widths varying unexpectedly on the output._"

*   [AD9850 Complete DDS Synthesizer Datasheet](http://www.analog.com/media/en/technical-documentation/data-sheets/AD9850.pdf)

# Conclusion

**Bit-banging pin states on FTDI devices is relatively simple, even using the standard drivers and API.** The FTD2XX_NET library on NuGet provides a simple way to do this. The output of the FT232H is much more accurate in the time domain than the FT232R. Although there are crazy timing issues with the FT232R, it works fine when driving most SPI devices. Here we used this technique to write a console application to control an AD9850 DDS directly from an FT232R using command line arguments. When given a formal enclosure, this project looks (and works) great!

<div class="text-center img-border">

![](https://swharden.com/static/2018/06/03/scope-dds.png)

</div>

If you make something cool by bit-banging a FTDI device, let me know about it!