---
title: Multichannel USB Analog Sensor with ATMega48
date: 2012-06-14 10:42:00
tags: ["microcontroller", "circuit", "obsolete"]
---



__Sometimes it's tempting to re-invent the wheel to make a device function exactly the way you want.__ I am re-visiting the field of homemade electrophysiology equipment, and although I've [already published](https://swharden.com/blog/2009-08-14-diy-ecg-machine-on-the-cheap/) a home made [electocardiograph](http://en.wikipedia.org/wiki/Electrocardiography) (ECG), I wish to revisit that project and make it much more elegant, while also planning for a [pulse oximeter](http://en.wikipedia.org/wiki/Pulse_oximeter), an [electroencephalograph](http://en.wikipedia.org/wiki/Electroencephalography) (EEG), and an [electrogastrogram](http://en.wikipedia.org/wiki/Electrogastrogram) (EGG). This project is divided into 3 major components: the low-noise microvoltage amplifier, a digital analog to digital converter with PC connectivity, and software to display and analyze the traces. My first challenge is to create that middle step, a device to read voltage (from 0-5V) and send this data to a computer.

> This project demonstrates a simple solution for the frustrating problem of sending data from a microcontroller to a PC with a USB connection. My solution utilizes a [USB FTDI serial-to-usb cable](http://www.ftdichip.com/Products/Cables/USBTTLSerial.htm), allowing me to simply put header pins on my device which I can plug into providing the microcontroller-computer link. This avoids the need for soldering [surface-mount FTDI chips](http://en.wikipedia.org/wiki/File:Arduino_ftdi_chip-1.jpg) (which gets expensive if you put one in every project). [FTDI cables are inexpensive](http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=ftdi+cable&_sacat=0) (about $11 shipped on eBay) and I've gotten a lot of mileage out of mine and know I will continue to use it for future projects. If you are interested in MCU/PC communication, consider one of these cables as a rapid development prototyping tool. I'm certainly enjoying mine!

__It is important to me that my design is minimalistic, inexpensive, and functions natively on Linux and Windows without installing special driver-related software__, and can be visualized in real-time using native Python libraries, such that the same code can be executed identically on all operating systems with minimal computer-side configuration. I'd say I succeeded in this effort, and while the project could use some small touches to polish it up, it's already solid and proven in its usefulness and functionality.

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/011.jpg)

</div>

__This is my final device.__ It's reading voltage on a single pin, sending this data to a computer through a USB connection, and custom software (written entirely in Python, designed to be a cross-platform solution) displays the signal in real time. Although it's capable of recording and displaying 5 channels at the same time, it's demonstrated displaying only one. Let's check-out a video of it in action:

{{<youtube zPAx4JTCFAc>}}

>  This 5-channel realtime USB analog sensor, coupled with custom cross-platform open-source software, will serve as the foundation for a slew of electrophysiological experiments, but can also be easily expanded to serve as an inexpensive multichannel digital oscilloscope. While more advanced solutions exist, this has the advantage of being minimally complex (consisting of a single microchip), inexpensive, and easy to build.


__Below is a simplified description of the circuit__ that is employed in this project. Note that there are 6 ADC (analog to digital converter) inputs on the [ATMega48](http://www.atmel.com/devices/atmega48.aspx) IC, but for whatever reason I ended-up only hard-coding 5 into the software. Eventually I'll go back and re-declare this project a 6-channel sensor, but since I don't have six things to measure at the moment I'm fine keeping it the way it is. RST, SCK, MISO, and MOSI are used to program the microcontroller and do not need to be connected to anything for operation. The [max232](http://en.wikipedia.org/wiki/MAX232) was initially used as a level converter to allow the micro-controller to communicate with a PC via the serial port. However, shortly after this project was devised an upgrade was used to allow it to connect via USB. 


<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/031.jpg)

</div>

**Below you can see the circuit breadboarded.** The potentiometer (small blue box) simulated an analog input signal.

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/041.jpg)

</div>

**The lower board is my AVR programmer**, and is connected to RST, SCK, MISO, MOSI, and GND to allow me to write code on my laptop and program the board. It's a <a href="http://fun4diy.com/AVRISP_mkII.htm">Fun4DIY.com AVR programmer</a> which can be yours for $11 shipped! I'm not affiliated with their company, but I love that little board. It's a clone of the AVR ISP MK-II.

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/051.jpg)

</div>

<p style="text-align: left;"><strong>As you can see, the USB AVR programmer I'm using is supported in Linux.</strong> I did all of my development in Ubuntu Linux, writing AVR-GCC (C) code in my favorite Linux code editor <a href="http://www.geany.org/">Geany</a>, then loaded the code onto the chip with <a href="http://www.nongnu.org/avrdude/">AVRDude</a>.</p>

<p style="text-align: left;"><strong>I found a simple way to add USB functionality in a standard, reproducible way</strong> that works without requiring the soldering of a <a href="http://en.wikipedia.org/wiki/File:Arduino_ftdi_chip-1.jpg">SMT FTDI chip</a>, and avoids custom libraries like <a href="http://www.obdev.at/products/vusb/index.html">V-USB</a> which don't easily have drivers that are supported by major operating systems (Windows) without special software. I understand that the simplest long-term and commercially-logical solution would be to use that SMT chip, but I didn't feel like dealing with it. Instead, I added header pins which allow me to snap-on <a href="http://www.ftdichip.com/Products/Cables/USBTTLSerial.htm">a pre-made FTDI USB cable</a>. <em><strong>They're a bit expensive ($12 on ebay) but all I need is 1 and I can use it in all my projects since it's a sinch to connect and disconnect.</strong></em> Beside, it supplies power to the target board! It's supported in Linux and in Windows with established drivers that are shipped with the operating system. It's a bit of a shortcut, but I like this solution. It also eliminates the need for the max232 chip, since it can sense the voltages outputted by the microcontroller directly.</p>

<blockquote><p style="text-align: left;">The system works by individually reading the 10-bit <a href="http://en.wikipedia.org/wiki/Analog-to-digital_converter">ADC</a> pins on the microcontroller (providing values from 0-1024 to represent voltage from 0-5V or 0-1.1V depending on how the code is written), converting these values to text, and sending them as a string via the serial protocol. The <a href="http://www.ftdichip.com/Products/Cables/USBTTLSerial.htm">FTDI cable</a> reads these values and transmits them to the PC through a USB connection, which looks like "COM5" on my Windows computer. Values can be seen in any serial terminal program (i.e., hyperterminal), or accessed through Python with the <a href="http://pyserial.sourceforge.net/">PySerial</a> module.</p></blockquote>

**As you can see, I'm getting quite good at home-brewn PCBs.** While it would be fantastic to design a board and have it made professionally, this is expensive and takes some time. In my case, I only have a few hours here or there to work on projects. If I have time to design a board, I want it made immediately! I can make this start to finish in about an hour. I use a classic toner transfer method with ferric chloride, and a dremel drill press to create the holes. I haven't attacked single-layer SMT designs yet, but I can see its convenience, and look forward to giving it a shot before too long.</p>

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/091.jpg)

</div>

**Here's the final board ready for digitally reporting analog voltages.** You can see 3 small headers on the far left and 2 at the top of the chip. These are for RST, SCK, MISO, MOSI, and GND for programming the chip. Once it's programmed, it doesn't need to be programmed again. Although I wrote the code for an <a href="http://www.atmel.com/devices/atmega48.aspx">ATMega48</a>, it works fine on a pin-compatible <a href="http://www.atmel.com/devices/atmega8.aspx">ATMega8</a> which is pictured here. The connector at the top is that FTDI USB cable, and it supplies power and USB serial connectivity to the board.</p>

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/101.jpg)

</div>

<p style="text-align: left;"><strong>If you look closely, you can see that modified code has been loaded</strong> on this board with a Linux laptop. This thing is an exciting little board, because it has so many possibilities. It could read voltages of a single channel in extremely high speed and send that data continuously, or it could read from many channels and send it at any rate,<strong><em> or even cooler would be to add some bidirectional serial communication capabilities to allow the computer to tell the microcontroller which channels to read and how often to report the values back</em></strong>. There is a lot of potential for this little design, and I'm glad I have it working.</p>

<div class="text-center img-border">

![](https://swharden.com/static/2012/06/14/111.jpg)

</div>

<p style="text-align: left;"><strong>Unfortunately I lost the schematics</strong> to this device because I formatted the computer that had the Eagle files on it. It should be simple and intuitive enough to be able to design again. The code for the microcontroller and code for the real-time visualization software will be posted below shortly. Below are some videos of this board in use in one form or another:</p>

{{<youtube GJcrXoIC7Q8>}}
{{<youtube HsV-LK3KO1U>}}
{{<youtube tdf0wzS-H-8>}}
{{<youtube VZkWUR-gAZk>}}

__Here is the code that is loaded onto the microcontroller:__

```c

#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>

void readADC(char adcn){
        //ADMUX = 0b0100000+adcn; // AVCC ref on ADCn
        ADMUX = 0b1100000+adcn; // AVCC ref on ADCn
        ADCSRA |= (1<<ADSC); // reset value
        while (ADCSRA & (1<<ADSC)) {}; // wait for measurement
}

int main (void){
    DDRD=255;
    init_usart();
    ADCSRA = 0b10000111; //ADC Enable, Manual Trigger, Prescaler
    ADCSRB = 0;

    int adcs[8]={0,0,0,0,0,0,0,0};

    char i=0;
    for(;;){
        for (i=0;i<8;i++){readADC(i);adcs[i]=ADC>>6;}
        for (i=0;i<5;i++){sendNum(adcs[i]);send(44);}
        readADC(0);
        send(10);// LINE BREAK
        send(13); //return
        _delay_ms(3);_delay_ms(5);
    }
}

void sendNum(unsigned int num){
    char theIntAsString[7];
    int i;
    sprintf(theIntAsString, "%u", num);
    for (i=0; i < strlen(theIntAsString); i++){
        send(theIntAsString[i]);
    }
}

void send (unsigned char c){
    while((UCSR0A & (1<<UDRE0)) == 0) {}
    UDR0 = c;
}

void init_usart () {
    // ATMEGA48 SETTINGS
    int BAUD_PRESCALE = 12;
    UBRR0L = BAUD_PRESCALE; // Load lower 8-bits
    UBRR0H = (BAUD_PRESCALE >> 8); // Load upper 8-bits
    UCSR0A = 0;
    UCSR0B = (1<<RXEN0)|(1<<TXEN0); //rx and tx
    UCSR0C = (1<<UCSZ01) | (1<<UCSZ00); //We want 8 data bits
}

```

__Here is the code that runs on the computer, allowing reading and real-time graphing of the serial data.__ It's written in Python and has been tested in both Linux and Windows. It requires *NO* non-standard python libraries, making it very easy to distribute. Graphs are drawn (somewhat inefficiently) using lines in TK. Subsequent development went into improving the visualization, and drastic improvements have been made since this code was written, and updated code will be shared shortly. This is functional, so it's worth sharing.

```python
import Tkinter, random, time
import socket, sys, serial

class App:

    def white(self):
        self.lines=[]
        self.lastpos=0

        self.c.create_rectangle(0, 0, 800, 512, fill="black")
        for y in range(0,512,50):
            self.c.create_line(0, y, 800, y, fill="#333333",dash=(4, 4))
            self.c.create_text(5, y-10, fill="#999999", text=str(y*2), anchor="w")
        for x in range(100,800,100):
            self.c.create_line(x, 0, x, 512, fill="#333333",dash=(4, 4))
            self.c.create_text(x+3, 500-10, fill="#999999", text=str(x/100)+"s", anchor="w")

        self.lineRedraw=self.c.create_line(0, 800, 0, 0, fill="red")

        self.lines1text=self.c.create_text(800-3, 10, fill="#00FF00", text=str("TEST"), anchor="e")
        for x in range(800):
            self.lines.append(self.c.create_line(x, 0, x, 0, fill="#00FF00"))

    def addPoint(self,val):
        self.data[self.xpos]=val
        self.line1avg+=val
        if self.xpos%10==0:
            self.c.itemconfig(self.lines1text,text=str(self.line1avg/10.0))
            self.line1avg=0
        if self.xpos>0:self.c.coords(self.lines[self.xpos],(self.xpos-1,self.lastpos,self.xpos,val))
        if self.xpos<800:self.c.coords(self.lineRedraw,(self.xpos+1,0,self.xpos+1,800))
        self.lastpos=val
        self.xpos+=1
        if self.xpos==800:
            self.xpos=0
            self.totalPoints+=800
            print "FPS:",self.totalPoints/(time.time()-self.timeStart)
        t.update()

    def __init__(self, t):
        self.xpos=0
        self.line1avg=0
        self.data=[0]*800
        self.c = Tkinter.Canvas(t, width=800, height=512)
        self.c.pack()
        self.totalPoints=0
        self.white()
        self.timeStart=time.time()

t = Tkinter.Tk()
a = App(t)

#ser = serial.Serial('COM1', 19200, timeout=1)
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    while True: #try to get a reading
        #print "LISTENING"
        raw=str(ser.readline())
        #print raw
        raw=raw.replace("n","").replace("r","")
        raw=raw.split(",")
        #print raw
        try:
            point=(int(raw[0])-200)*2
            break
        except:
            print "FAIL"
            pass
    point=point/2
    a.addPoint(point)
```

__If you re-create this device of a portion of it, let me know!__ I'd love to share it on my website. Good luck!