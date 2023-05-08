---
title: Precision Temperature Measurement
date: 2013-06-10 22:25:27
tags: ["microcontroller", "old"]
---

# Precision Temperature Measurement

__In an effort to resume previous work \[[A](http://www.swharden.com/blog/2010-11-24-atmega48-lm335-max232-serial-port-multi-channel-temperature-measurement/), [B](http://www.swharden.com/blog/2010-11-28-crystal-oven-experiments/), [C](http://www.swharden.com/blog/2010-08-27-hacking-together-a-crystal-oven-part-2/), [D](http://www.swharden.com/blog/2010-08-26-minimalist-crystal-oven/)\] on developing a crystal oven for radio frequency transmitter / receiver stabilization purposes, the first step for me was to create a device to accurately measure and log temperature.__ I did this with common, cheap components, and the output is saved to the computer (over 1,000 readings a second). Briefly, I use a [LM335 precision temperature sensor](http://www.ti.com/lit/ds/symlink/lm335.pdf) ([$0.70 on mouser](http://www.mouser.com/ProductDetail/STMicroelectronics/LM335Z/?qs=sGAEpiMZZMusbZ2pNxAMx3IjjBanxLGdnwZerf04Dlo%3d)) which outputs voltage with respect to temperature. It acts like a [Zener diode](http://en.wikipedia.org/wiki/Zener_diode) where the breakdown voltage relates to temperature. 2.95V is 295K (Kelvin), which is 22ºC / 71ºF. Note that Kelvin is just ºC + 273.15 (the difference between freezing and [absolute zero](http://en.wikipedia.org/wiki/Absolute_zero)). My goal was to use the [ADC ](http://en.wikipedia.org/wiki/Analog_digital_converter)of a microcontroller to measure the output. The problem is that my [ADC ](http://en.wikipedia.org/wiki/Analog_digital_converter)(one of 6 built into the [ATMEL ATMega8 microcontroller](http://www.atmel.com/Images/Atmel-2486-8-bit-AVR-microcontroller-ATmega8_L_datasheet.pdf)) has 10-bit resolution, reporting steps from 0-5V as values from 0-1024. Thus, each step represents 0.0049V (0.49ºC / 0.882ºF). While ~1ºF resolution might be acceptable for _some_ temperature measurement or control applications, I want to see fractions of a degree because radio frequency crystal temperature stabilization is critical. Here's a video overview.

{{<youtube LTPncC2e3Zo>}}

__This is the circuit came up with.__ My goal was to make it cheaply and what I had on hand. It could certainly be better (more stable, more precise, etc.) but this seems to be working nicely. The idea is that you set the gain (the ratio of R2/R1) to increase your desired resolution (so your 5V of ADC recording spans over just several ºF you're interested in), then set your "base offset" temperature that will produce 0V. In my design, I adjusted so 0V was room temperature, and 5V (maximum) was body temperature. This way when I touched the sensor, I'd watch temperature rise and fall when I let go.  Component values are very non-critical. LM324 is powered 0V GND and +5V Vcc. I chose to keep things simple and use a single rail power supply. It is worth noting that I ended-up using a 3.5V Zener diode for the positive end of the potentiometer rather than 5V.  If your power supply is well regulated 5V will be no problem, but as I was powering this with USB I decided to go for some extra stability by using a Zener reference.

<div class="text-center img-border">

![](https://swharden.com/static/2013/06/10/precision-thermometer-LM335-LM324-microcontroller.jpg)

</div>

__On the microcontroller side, analog-to-digital measurement is summed-up pretty well in the datasheet.__ There is a lot of good documentation on the internet about how to get reliable, stable measurements. Decoupling capacitors, reference voltages, etc etc. That's outside the scope of today's topic. In my case, the output of the ADC went into the ATMega8 ADC5 (PC5, pin 28). Decoupling capacitors were placed at ARef and AVcc, according to the datasheet. Microcontroller code is at the bottom of this post.

<div class="text-center">

![](https://swharden.com/static/2013/06/10/photo-3.jpg)

</div>

__To get the values to the computer, I used the USART capability of my microcontroller and sent ADC readings (at a rate over 1,000 a second) over a USB adapter based on an FTDI FT232 chip.__ I got e-bay knock-off FTDI evaluation boards which come with a USB cable too (they're about $6, free shipping). Yeah, I could have done it cheaper, but this works effortlessly. I don't use a crystal. I set [fuse settings](http://www.engbedded.com/fusecalc) so the MCU runs at 8MHz, and thanks to the [nifty online baud rate](http://www.wormfood.net/avrbaudcalc.php) calculator determined I can use a variety of transfer speeds (up to 38400). At 1MHz (if DIV8 fuse bit is enabled) I'm limited to 4800 baud. Here's the result, it's me touching the sensor with my finger (heating it), then letting go.

<div class="text-center">

![](https://swharden.com/static/2013/06/10/finger-touch.png)

</div>

Touching the temperature sensor with my finger, voltage rose exponentially. When removed, it decayed exponentially - a temperature RC circuit, with capacitance being the specific heat capacity of the sensor itself. Small amounts of jitter are expected because I'm powering the MCU from unregulated USB +5V.[/caption]

__I spent a while considering fancy ways to send the data__ (checksums, frame headers, error correction, etc.) but ended-up just sending it old fashioned ASCII characters. I used to care more about speed, but even sending ASCII it can send over a thousand ADC readings a second, which is plenty for me. I ended-up throttling down the output to 10/second because it was just too much to log comfortable for long recordings (like 24 hours). In retrospect, it would have made sense to catch all those numbers and do averaging on the on the PC side.

<div class="text-center">

![](https://swharden.com/static/2013/06/10/ac2.png)

</div>

I keep my house around 70F at night when I'm there, and you can see the air conditioning kick on and off. In the morning the AC was turned off for the day, temperature rose, and when I got back home I turned the AC on and it started to drop again.[/caption]

__On the receive side, I have nifty Python with [PySerial ](http://pyserial.sourceforge.net/)ready to catch data coming from the microcontroller. __It's decoded, turned to values, and every 1000 receives [saves a numpy array as a NPY binary file](http://docs.scipy.org/doc/numpy/reference/generated/numpy.save.html). I run the project out of my google drive folder, so while I'm at work I can run the plotting program and it loads the NPY file and shows it - today it allowed me to realize that my roommate turned off the air conditioning after I left, because I saw the temperature rising mid-day. The above graph is temperature in my house for the last ~24 hours. That's about it! Here's some of the technical stuff.

AVR ATMega8 microcontroller code:

```c
#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

/*
8MHZ: 300,600,1200,2400,4800,9600,14400,19200,38400
1MHZ: 300,600,1200,2400,4800
*/
#define USART_BAUDRATE 38400
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

/*
ISR(ADC_vect)
{
    PORTD^=255;
}
*/

void USART_Init(void){
    UBRRL = BAUD_PRESCALE;
    UBRRH = (BAUD_PRESCALE >> 8);
    UCSRB = (1<<TXEN);
    UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0); // 9N1
}

void USART_Transmit( unsigned char data ){
    while ( !( UCSRA & (1<<UDRE)) );
    UDR = data;
}

void sendNum(long unsigned int byte){
    if (byte==0){
        USART_Transmit(48);
    }
    while (byte){
        USART_Transmit(byte%10+48);
        byte-=byte%10;
        byte/=10;
    }

}

unsigned int readADC(char adcn){
    ADMUX = 0b0100000+adcn;
    ADCSRA |= (1<<ADSC); // reset value
    while (ADCSRA & (1<<ADSC)) {}; // wait for measurement
    return ADC>>6;
}

void ADC_Init(){
    // ADC Enable, Prescaler 128
    ADCSRA = (1<<ADEN)  | 0b111;
}

int main(void){
    //DDRD=255;
    USART_Init();
    ADC_Init();
    for(;;){
        sendNum(readADC(5));
        USART_Transmit('n');
        _delay_ms(100);
    }
}
```

Here is the Python code to receive the data and log it to disk:

```python
import serial, time
import numpy
ser = serial.Serial("COM15", 38400, timeout=100)

line=ser.readline()[:-1]
t1=time.time()
lines=0

data=[]

while True:
    line=ser.readline()[:-1]

    if "," in line:
        line=line.split(",")
        for i in range(len(line)):
            line[i]=line[i][::-1]
    else:
        line=[line[::-1]]
    temp=int(line[0])
    lines+=1
    data.append(temp)
    print "#",
    if lines%1000==999:
        numpy.save("DATA.npy",data)
        print
        print line
        print "%d lines in %.02f sec (%.02f vals/sec)"%(lines,
                time.time()-t1,lines/(time.time()-t1))
```

Here is the Python code to plot the data that has been saved:

```python
import numpy
import pylab

data=numpy.load("DATA.npy")
print data
data=data*.008 #convert to F
xs=numpy.arange(len(data))/9.95  #vals/sec
xs=xs/60.0# minutes
xs=xs/60.0# hours

pylab.plot(xs,data)
pylab.grid(alpha=.5)
pylab.axis([None,None,0*.008,1024*.008])
pylab.ylabel(r'$Delta$ Fahrenheit')
pylab.xlabel("hours")
pylab.show()
```