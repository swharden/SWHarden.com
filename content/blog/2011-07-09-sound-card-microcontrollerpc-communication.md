---
title: Sound Card Microcontroller/PC Communication
date: 2011-07-09 23:30:44
tags: ["microcontroller", "circuit", "old"]
---

# Sound Card Microcontroller/PC Communication

_This page describes a method of sending data from a microchip to a PC using pulses of data. It's an alternative to more traditional serial or USB methods of connectivity. It's not intended as a solution for consumer products, but rather an easy hack for hobbyists to employ if they don't have the equipment for other methods. This method doesn't require any circuitry, just a sound card. The one built in your computer is fine, but I'm using a $1.30 USB sound card for simplicity. It boils down to just a single microcontroller pin connected to a PC sound card microphone jack!

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/09/DSCN1532.jpg)

</div>

__MY PROBLEM:__ I want to send data from a simple microcontroller to a PC. While USART and a serial port is the common solution [like I've done before](http://www.swharden.com/blog/2009-05-14-simple-case-avrpc-serial-communication-via-max232/), it's not convenient because it requires a level converter (like a MAX232, about $4), crystal (specific values based on bit and error rate, if you're lucky you might have a right value in your junk box), and an archaic PC which actually has a serial port. A usb serial port adapter sounds clever, but many aren't supported on Linux, Windows Vista, or Windows 7. Also, many small chips (most of the ATTiny series) don't have built in serial capabilities, so it has to be bit-banged in software! Yuk! The second choice would be USB. This requires a crystal too, zener diodes, and bit-banging the USB protocol with something like [V-USB](http://www.obdev.at/products/vusb/index.html) since most of the AVR series don't have built in USB (do they even make breadbordable DIP chips with USB?). Even so, it requires drivers, custom software, cross-platform frustrations, etc. I know PIC has some 18f series chips with USB, but I don't feel like switching architectures just to send a few bytes of data to a PC. FDTI has a [FT232R](http://www.ftdichip.com/Products/ICs/FT232R.htm) chip which is a USB serial port adapter, but it's expensive (about $5) and doesn't come in dip, so no breadboarding! Sure there are adapter boards, but that just adds the cost. I'm not excited about a $5 solution for a $1 microcontroller. I even did [a bit of trolling on AVR Freaks](http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&t=109298) to see if anyone could help me out - just more of the same!

![](https://www.youtube.com/embed/I0UEooQH2bw)

__MY SOLUTION:__ Send data through the sound card! USB sound cards are $1.30 (shipped) on eBay! It couldn't be simpler. Send pulses, measure distance between pulses. Short pulses are a zero, longer ones are a 1, and very long pulses are number separators. __A Python solution with PyAudio allows 1 script which will work on Mac, Linux, Windows, etc, and because it calibrates itself, this will work on any chip at any clock rate.__ Data is initiated with calibration pulses so timing is not critical - the PC figures out how fast the data is coming in. Check it out! (scroll way down for a bidirectional communication solution)

![](https://www.youtube.com/embed/WKp0P43uhzY)

Here is a sound card I used for bidirectional communication:

<div class="text-center img-border">

![](https://swharden.com/static/2011/07/09/DSCN1466.jpg)
![](https://swharden.com/static/2011/07/09/DSCN1470.jpg)

</div>

Output graph (python and excel) of temperature when I put a soldering iron near the sensor: 

<div class="text-center img-border">

[![](https://swharden.com/static/2011/07/09/python1_thumb.jpg)](https://swharden.com/static/2011/07/09/python1.png)
[![](https://swharden.com/static/2011/07/09/excel_thumb.jpg)](https://swharden.com/static/2011/07/09/excel.jpg)

</div>

## UNIDIRECTIONAL SOLUTION

__The following code is designed to have a chip send data to your PC automatically.__ This can be run on any micro-controller (PIC or AVR I guess, the concept is the same) at any clock rate. Just make sure the sound card is recording fast enough to differentiate pulses. (keep scrolling down for a bidirectional solution)

__A NOTE ABOUT MY CODE:__ This is just the code I used for my demonstration. It might be more logical for you to write your own since the concept is so simple. I'm a dental student, not a programmer, so I'm sure it's not coded very elegantly. I didn't work hard to make this code easy to read or easy to share. With that being said, help yourself!

```c
/*The following code is written in AVR-GCC for an ATTiny44a.
It reads ADC values on 3 pins and reports it each second along
 with a number which increments each time data is sent.
It's designed as a starting point, allowing anyone to
customize it from here!*/

#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

// bytes we want to send to the PC
volatile int data1=0;
volatile int data2=0;
volatile int data3=0;
volatile int data4=0;

void solid(){  // dont touch
    _delay_ms(1);
    pulse(1);pulse(1);pulse(1);pulse(3);pulse(3);
    pulse(3);pulse(5);pulse(5);// CALIBRATION PULSES
}
void pulse(char size){ // dont touch
    PORTA|=_BV(PA3);
    _delay_us(100);
    PORTA&=~_BV(PA3);
    while (size){size--;_delay_us(100);}
}
void sendVal(unsigned long tosend){ // dont touch
    pulse(5); // send a space
    while (tosend){
        if (tosend&1){pulse(3);} // send ONE
        else {pulse(1);} // send ZERO
        tosend=tosend>>1;
    }
}

int readADC(char adcNum){
    _delay_ms(1);
    ADMUX=adcNum; // select which ADC to read, VCC as ref.
    ADCSRA=0b11000111; // enable, start, 128 prescale
    while (ADCSRA&( 1<<ADSC)) {}; // wait for measurement
    return ADC;
}

void takeReadings(){
        data1=readADC(0); // ADC0
        data2=readADC(1); // ADC1
        data3=readADC(2); // ADC2
        data4++; // incriment just because we want to
}

void sendStuff(){ // EDIT to send what you want
    solid(); //required
    sendVal(12345); //required
    sendVal(12345); //required
    sendVal(54321); //required

    sendVal(data1);
    sendVal(data2);
    sendVal(data3);
    sendVal(data4);

    pulse(1); //required
}

int main(){
    DDRA|=_BV(PA2)|_BV(PA3);
    for (;;){
        _delay_ms(1000);
        takeReadings();
        sendStuff();
    }
    return 0;
}
```

```python
"""
file name: listenOnly.py

This is the PC code to listen to the microphone and display
and log the data. It probably does NOT need adjustment!
 Make sure the correct sound card is selected (in the code)
 and make sure microphone input is turned up in volume control.

This code is what was used on my PC for the demonstration
video. This is the listenOnly.py file which will turn any audio
 detected from a sound card into data, optionally logging it
(if the last few lines are uncommented). This also works to
capture data for the bidirectional communication method,
described below on this website.

If this is running but no data is coming through, make sure the
microphone is selected as a recording device, the correct sound
card is selected, and the microphone volume is turned to high.

REQUIRED: To run this, you need to have the following installed:
-- Python 2.6
-- numpy for python 2.6
-- matplotlib for python 2.6
-- pyaudio for python 2.6
(other versions may work, but this is what I'm using)
"""
import numpy
import pyaudio
import matplotlib.pyplot as plt
import wave
import time

def listCards(dontAsk=True):
    p=pyaudio.PyAudio()
    print "SOUND CARDS:"
    for i in range(p.get_default_host_api_info()["deviceCount"]):
        if p.get_device_info_by_index(i)["maxInputChannels"]>0:
                cardName = p.get_device_info_by_index(i)["name"]
                cardIndex = p.get_device_info_by_index(i)["index"]
                print "[%d] %s"%(cardIndex,cardName)
    if dontAsk: return
    return int(raw_input("CARD NUMBER TO USE:"))

cardID=1
listCards()
print "USING CARD:",cardID

rate=44100.0
sampleSize=1024

def data2vals(data):
    vals=numpy.array([])
    lastPeak=0
    for i in range(1,len(data)):
        if data[i]==True and data[i-1]==False:
            if lastPeak>0: vals=numpy.append(vals,i-lastPeak)
            lastPeak=i
    return vals

def binary2dec(binary):
    binary=binary[:-1]
    dec=0
    s=""
    for i in range(len(binary)):
        dec=dec*2
        dec+=binary[i]
        s="%d"%binary[i]+s
    #print s,"=",dec #11111100101100000 = 3391
    return dec

def readVals(vals):
    if len(vals)<7: return False
    vals2=[]
    aLow = min(vals[0:3])
    aMed = min(vals[3:6])
    aHigh = vals[6]
    thresh1=sum([aLow,aMed])/2+2
    thresh2=sum([aMed,aHigh])/2+2
    #print "tresholds:",thresh1,thresh2
    #print vals
    vals=vals[8:]
    binary=[]
    for i in range(len(vals)):
        if vals[i]>thresh2:
            vals2.append(binary2dec(binary))
            binary=[]
        if vals[i]>thresh1:binary=[1]+binary
        else:binary=[0]+binary
    vals2.append(binary2dec(binary))
    for i in range(len(vals2)):
        if vals2[i]==54321: return vals2[i+1:]
    return False

def playFile():
    chunk = 1024
    wf = wave.open("short_onenum.wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()

def captureData():
    pyaud = pyaudio.PyAudio()
    stream = pyaud.open(format=pyaudio.paInt16,channels=1,
        rate = 44100,input_device_index=cardID,input=True,output=True)
    sample=numpy.array([])
    while True:
        sampleNew=numpy.fromstring(stream.read(sampleSize),dtype=numpy.int16)
        sampleNew=(sampleNew<-25000)*1
        if True in sampleNew: sample=numpy.append(sample,sampleNew)
        else:
            if len(sample):
                stream.close()
                return sample
    stream.close()

tone_quiet=0

def buildNumber(num=123):

    if num>255: print "NUMBER TOO HIGH!!!"
    #print num,'=',
    num+=1
    for i in [7,6,5,4,3,2,1,0]:
        if num>2**i:one();num=num-2**i;#print"1",
        else: zero();#print"0",
    #print
    space()

def pulse():
    global data
    data+=[-30000]*10

def space():
    global data
    data+=[tone_quiet]*900
    pulse()

def one():
    global data
    data+=[tone_quiet]*600
    pulse()

def zero():
    global data
    data+=[tone_quiet]*300
    pulse()

def silence(msec=1000):
    global data
    data+=[tone_quiet]*int(41.1*msec)

data=[]
def sendAudio(numbers=[11,66,77]):
    global data
    data=[]
    silence(100)
    buildNumber(250)
    print "SENDING",
    for numba in numbers:
        buildNumber(numba)
        print numba,
    buildNumber(250)
    silence(100)
    data=numpy.array(data)
    data=-data
    data=data.tostring()
    print

    p = pyaudio.PyAudio()
    stream = p.open(rate=44100, channels=1, format=pyaudio.paInt16,
                    input_device_index=cardID, output=True)
    stream.write(data)
    stream.close()
    p.terminate()

i=0
while True:
    i+=1
    val=readVals(data2vals(captureData()))
    if val == False: continue
    line=""
    for item in val: line+=str(item)+","
    print i,line
    #f=open('log.csv','a')
    #f.write("%sn"%line)
    #f.close()
```

## BIDIRECTIONAL SOLUTION

__What if we want to send data TO the microcontroller?__ The solution is a little more complex, but quite doable. Just add an extra wire to the sound card's speaker output and attach it to PCINT0 (the highest level internal interrupt). This is intended for advanced users, and if you're doing this you probably are better off with USB or serial anyway! ... but heck, why not do it as a proof of concept!

![](https://www.youtube.com/embed/fhsYGRdwIaw)

Note that the USB sound card speaker output was not powerful enough to trigger the digital input pin of the AVR, so an inverting buffer was made from a single NPN transistor (2n3904). The hardware interrupt was attacked to the collector, and the collector was attached through +5V through a 220 ohm resistor. The emitter was grounded. The base was attached directly to the sound card output. I also tried running the sound card output through a small series capacitor (0.1uF) and biasing the base to ground through a 1Mohm resistor and it worked the same. Hardware, simple. Chip-side software... a little more complex.

```python
"""
This code is what was used on my PC for the
 demonstration video. The listenonly.py file
 (above on site) was also used without modification.
"""
import pyaudio
from struct import pack
from math import sin, pi
import wave
import random
import numpy
import time

RATE=44100
maxVol=2**15-1.0 #maximum amplitude
p = pyaudio.PyAudio()
stream = p.open(rate=44100, channels=1, format=pyaudio.paInt16,
        input_device_index=1, output=True)

def pulseZero():
    global wvData
    wvData+=pack('h', 0)*30
    wvData+=pack('h', maxVol)

def pulseOne():
    global wvData
    wvData+=pack('h', 0)*40
    wvData+=pack('h', maxVol)

def pulseSpace():
    global wvData
    wvData+=pack('h', 0)*50
    wvData+=pack('h', maxVol)

def buildNumber(num=123):
    if num>255: print "NUMBER TOO HIGH!!!"
    num+=1
    for i in [7,6,5,4,3,2,1,0]:
        if num>2**i:
            pulseOne()
            num=num-2**i
        else:
            pulseZero()

wvData=""
wvData+=pack('h', 0)*2000
pulseOne() #required before sending data

buildNumber(55)
buildNumber(66)
buildNumber(77)
buildNumber(123)

wvData+=pack('h', 0)*2000

while True:
    print "SENDING",
    stream.write(wvData)
    raw_input()
```

```c
/*
This code is what was used on my AVR
microcontroller for the demonstration video
*/
#include <avr/io.h>
#include <avr/delay.h>
#include <avr/interrupt.h>

volatile long commandIncoming=0;
volatile char command1=0;
volatile char command2=0;
volatile char command3=0;
volatile char command4=0;
volatile char bitsGotten=0;

// timing thresholds are critical! Send pulses to the chip
// and have it report the time between them. Use this to
// determine the best threshold value for your application.
// The ones here must be changed if you run at a speed other
// than 1mhz or if you use different timings in PC software
#define thresh_low 100 // between this and the next
#define thresh_high 130 // is the range for a logical 'one'

// ######## OUTGOING AUDIO DATA #########
void solid(){
    _delay_ms(1); //LONG LOW
    pulse(1);pulse(1);pulse(1);pulse(3);pulse(3);
    pulse(3);pulse(5);pulse(5);// CALIBRATION PULSES
}
void pulse(char size){
    PORTA|=_BV(PA3);
    _delay_us(100);
    PORTA&=~_BV(PA3);
    while (size){size--;_delay_us(100);}
}
void sendVal(unsigned long tosend){
    pulse(5); // send a space
    while (tosend){
        if (tosend&1){pulse(3);} // send ONE
        else {pulse(1);} // send ZERO
        tosend=tosend>>1;
    }
}

// ######## INCOMING AUDIO DATA #########
// NOTE THAT INPUTS ARE NORMALLY *HIGH* AND DROP *LOW* FOR SIGNAL
SIGNAL (PCINT0_vect) { // audio input trigger
    TIMSK0|=(1<<TOIE1); //Overflow Interrupt Enable
    if (TCNT0<10){return;} // seem too fast? ignore it!
    // Enable the following line to test custom timings
    //command1=command2;command2=command3;
    //command3=command4;command4=TCNT0;
    bitsGotten++;
    commandIncoming=commandIncoming*2; // shift left
    if (TCNT0>thresh_low){commandIncoming++;} // make 1
    TCNT0=0;
}

ISR(TIM0_OVF_vect){ // TIMER OVERFLOW
    if (bitsGotten){sendStuff();}
}

void fillCommands(){
    command1=(char*)(commandIncoming>>24);
    command2=(char*)(commandIncoming>>16);
    command3=(char*)(commandIncoming>>8);
    command4=(char*)(commandIncoming);
}

void sendStuff(){
    TIMSK0=0; //Overflow Interrupt
    cli(); // disable interrupts!
    fillCommands();
    solid(); // start data transmissions with this
    sendVal(12345);
    sendVal(12345);
    sendVal(54321);
    sendVal(command1);
    sendVal(command2);
    sendVal(command3);
    sendVal(command4);
    sendVal(1234567890);
    pulse(1);
    bitsGotten=0;
    sei(); // enable interrupts again!
    TIMSK0|=(1<<TOIE1); //Overflow Interrupt
}

// ######## MAIN PROGRAM #########
int main(){

    DDRA|=_BV(PA2)|_BV(PA3);

    // SET UP FOR SOUND CARD INTERRUPT
    MCUCR = 0b00000010; // trigger interrupt on falling edge
    GIMSK = 0b00010000; // pin change interrupt enable 0
    GIFR =  0b00010000; // flag register, same as above
    PCMSK0 = (1<<PCINT0); // Set Pin to use (PCINT0)
    sei(); // enable global interrupts

    // SET UP 8-bit COUNTER
    TCCR0B|=0b00000010;
    //TCCR1B|=(1<<CS12)|(1<<CS10); // prescaler 1024
    TIMSK0|=(1<<TOIE1); //Enable Overflow Interrupt Enable
    TCNT0=0;//Initialize our varriable (set for 1/15th second?)

    // MAIN PROGRAM
    for (;;){}
    return 0;

}
```

__In closing__, I'm tickled this works so well. It's funny to me that no one's really done this before in the hobby field. I'm sure I'm not the only one who wished there were an easy way to do this. I'm sure the process could be greatly improved, but this is a fun start. Wow, it's late, I should get to bed. I have to treat patients tomorrow morning!

__PS:__ If you replicate this concept, let me know about it! I'd love to see your project!

__UPDATE: This story was featured on [this post of HackADay.com](http://hackaday.com/2011/07/10/sound-card-microcontrollerpc-communication/)!__