---
title: Serial Port Multi-Channel Temperature Measurement
date: 2010-11-24 08:17:03
tags: ["circuit", "microcontroller", "python", "old"]
---

# ATMega48 + LM335 + MAX232 = Serial Port Multi-Channel Temperature Measurement

__While working to perfect my temperature-controlled manned experimental propagation transmitter (MEPT), I developed the need to accurately measure temperature inside my Styrofoam enclosure (to assess drift) and compare it to external temperature (to assess insulation effects).__ I accomplished this utilizing the 8 ADC channels of the ATMega48 and used its in-chip USART capabilities to send this data to a PC for logging.  I chose the ATMega48 over the ATTiny2313 (which has USART but no ADCs) and the ATTiny44a (which has ADCs but no USART).  From when I see, no ATTiny series ATMEL AVR has both!  Lucky for me, the [ATMega48 is cheap](http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&name=ATMEGA48-20PU-ND) at $2.84 USD. Here's my basic circuit idea: 

<div class="text-center img-border"> 

[![](https://swharden.com/static/2010/11/24/IMG_4559_thumb.jpg)](https://swharden.com/static/2010/11/24/IMG_4559.jpg)

</div>

EDIT: the voltage reference diagram is wrong at the bottom involving the zener diode. Reference the picture to the right for the CORRECT way to use such a diode as a voltage reference. (stupid me!)

<div class="text-center"> 

![](https://swharden.com/static/2010/11/24/aref.jpg)

</div>

__MULTIPLE SENSORS__ - Although in this demonstration post I only show a single sensor, it's possible to easily have 8 sensors in use simultaneously since the ATMega48 has 8 ADC pins, and even more (infinitely) if you want to design a clever way to switch between them.

__LM335 Temperature Sensor__ - selected because it's pretty cheap (< $1) and quantitative. In other words, every 10mV drop in voltage corresponds to a change of 1ºC.  If I wanted to be even cheaper, I would use thermistors (<$0.10) which are more qualitative, but can be calibrated I guess.

Notes on power stability  - The output of the sensor is measured with the ADC (analog to digital converter) of the microcontroller. The ADC has a 10-bit resolution, so readings are from 0 to 2^10 (1024).  AREF and AVCC can be selected as a voltage reference to set what the maximum value (1024) should be.  If the ADC value is 1V (for example) and AREF is 1V, the reading will be 1024.  If AREF becomes 5V, the reading will be 1024/5. Make sense?  If AREF is fluctuating like crazy, the same ADC voltage will be read as differing vales which is not what we want, therefore care should be taken to ensure AREF is ripple-free and constant.  Although I did it by adding a few capacitors to the lines of the power supply (not very precise), a better way would be to use a <a href="http://en.wikipedia.org/wiki/Zener_diode">zener diode (perhaps 4.1V?) as a voltage reference.

<div class="text-center img-border">

[![](https://swharden.com/static/2010/11/24/IMG_4575_thumb.jpg)](https://swharden.com/static/2010/11/24/IMG_4575.jpg)

</div>

<b>Here is my circuit.</b> I'm clocking the chip at 9.21MHz which works well for 19200 baud for serial communication. Refer to my other MAX232 posts for a more detailed explanation of how I chose this value. The temperature sensor (blurry) is toward the camera, and the max232 is near the back. Is that an eyelash on the right? Gross!

<div class="text-center img-border"> 

![](https://swharden.com/static/2010/11/24/logger.jpg)

</div>

<b>The data is read by a Python script</b> which watches the serial port for data and averages 10 ADC values together to produce a value with one more significant digit. This was my way of overcoming continuously-fluctuating values.

<div class="text-center img-border"> 

[![](https://swharden.com/static/2010/11/24/IMG_4564_thumb.jpg)](https://swharden.com/static/2010/11/24/IMG_4564.jpg)

</div>

<b>Here you can see me testing the device</b> by placing an ice cube on the temperature sensor. I had to be careful to try to avoid getting water in the electrical connections. I noticed that when I pressed the ice against the sensor firmly, it cooled at a rate different than if I simply left the ice near it.<b>NOTICE THE PROGRAMMER</b> in the background (slightly blurry). The orange wires connect the AVR programmer to my circuit, and after the final code is completed and loaded onto the microcontroller these orange wires will be cut away.

<div class="text-center"> 

[![](https://swharden.com/static/2010/11/24/lm335-microcontroller-graph-annotated_thumb.jpg)](https://swharden.com/static/2010/11/24/lm335-microcontroller-graph-annotated.png)

</div>

<b>Here is some actual data from the device.</b> The LM335 readout is in Kelvin, such that 3.00V implies 300K = 80ºF = 27ºC (room temperature). The data is smooth until I touch it with the soldering iron (spike), then it gets cool again and I touch it with a cold piece of metal (wimpy dip), then later I put an ice cube on it (bigger dip). Pretty good huh? Remember, 0.01V change = 1ºC change. The bottom of the dip is about 2.8V = 280K = 44ºF = 7ºC. If I left the cube on longer, I imagine it would reach 0ºC (273K, or 2.73V).<b>For everyone's reference, here's the pinout diagram of the ATMega48:</b>

<div class="text-center img-medium"> 

[![](https://swharden.com/static/2010/11/24/atmega48pinout_thumb.jpg)](https://swharden.com/static/2010/11/24/atmega48pinout.png)

</div>

```python
import socket
import sys
import serial

ser = serial.Serial('COM1', 19200, timeout=1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

chunk=""
i=0
data = ser.readline()
while True:
    i+=1
    data = ser.readline()
    data=data.replace("n","")
    data=data.replace("r","")
    data="["+data[:-1]+"]"
    data=eval(data)
    val=sum(data)/float(len(data))
    print i,data,val
    chunk=chunk+"%.01f,"%val
    if i==100:
        print "nSAVING"
        i=0
        f=open("data.txt","a")
        f.write(chunk)
        f.close()
        chunk=""

```

<b>and the code to PLOT the data file:</b>

```python

import matplotlib.pyplot as plt
import numpy

def smoothTriangle(data,degree,dropVals=False):
        """performs moving triangle smoothing with a variable degree."""
        """note that if dropVals is False, output length will be identical
        to input length, but with copies of data at the flanking regions"""
        triangle=numpy.array(range(degree)+[degree]+range(degree)[::-1])+1
        smoothed=[]
        for i in range(degree,len(data)-degree*2):
                point=data[i:i+len(triangle)]*triangle
                smoothed.append(sum(point)/sum(triangle))
        if dropVals: return smoothed
        smoothed=[smoothed[0]]*(degree+degree/2)+smoothed
        while len(smoothed)<len(data):smoothed.append(smoothed[-1])
        return smooth

print "loading..."
f=open("data.txt")
raw="["+f.read()+"]"
f.close()
data=eval(raw)

print "converting..."
data=numpy.array(data)
data=data/1024.0*5 #10-bit resolution, 5V max

print "graphing"
plt.plot(data)

plt.grid(alpha=.5)
plt.title("ATMega48 LM335 Temperature Sensor")
plt.ylabel("Voltage (V)")
plt.xlabel("Time (5/sec)")
plt.show()
```

<b>Also, the AVR-GCC code loaded on the ATMega48:</b>

```c
#define F_CPU 9210000UL

#include <avr/io.h>
#include <util/delay.h>

void init_usart(unsigned long);

unsigned int readADC(char times){
    unsigned long avg=0;
    for (char i=0; i<times; i++){
        ADCSRA |= (1<<ADSC); // reset value
        while (ADCSRA & ( 1<<ADSC)) {}; // wait for measurement
        avg=avg+ADC;
    }
    avg=avg/times;
    return avg;
}

int main (void){

    ADMUX = 0b0100101; // AVCC ref on ADC5
    ADCSRA = 0b10000111; //ADC Enable, Manual Trigger, Prescaler 128
    ADCSRB = 0;

    DDRD=255;

    init_usart(19200);
    for(;;){
        for(char j=0;j<10;j++){
            sendNum(readADC(10)>>6); // shift to offset 10bit 16bit
            send(44); // COMMA
            PORTD=255;_delay_ms(10);
            PORTD=0;_delay_ms(10);
            }
        send(10);send(13); // LINE BREAK
        }
    }

void sendNum(unsigned int num){
        char theIntAsString[7];
        int i;
        sprintf( theIntAsString, "%u", num );
        for (i=0; i < strlen(theIntAsString); i++)
        {send(theIntAsString[i]);}
}

void send (unsigned char c){
        while((UCSR0A & (1<<UDRE0)) == 0) {}
        UDR0 = c;
}

void init_usart (unsigned long baud)
{
    /////////////////////////
    //        Baud Generation
    unsigned int UBRR_2x_off;
    unsigned int UBRR_2x_on;
    unsigned long closest_match_2x_off;
    unsigned long closest_match_2x_on;
    unsigned char off_2x_error;
    unsigned char on_2x_error;

    UBRR_2x_off = F_CPU/(16*baud) - 1;
    UBRR_2x_on = F_CPU/(8*baud) - 1;

    closest_match_2x_off = F_CPU/(16*(UBRR_2x_off + 1));
    closest_match_2x_on = F_CPU/(8*(UBRR_2x_on + 1));

    off_2x_error = 255*(closest_match_2x_off/baud - 1);
    if (off_2x_error <0) {off_2x_error *= (-1);}
    on_2x_error = 255*(closest_match_2x_on/baud -1);
    if (on_2x_error <0) {on_2x_error *= (-1);}

    if(baud > F_CPU / 16)
    {
        UBRR0L = 0xff & UBRR_2x_on;
        UBRR0H = 0xff & (UBRR_2x_on>>8);
        UCSR0A |= (1<<U2X0);
    } else {

        if (off_2x_error > on_2x_error)
        {
            UBRR0L = 0xff & UBRR_2x_on;
            UBRR0H = 0xff & (UBRR_2x_on>>8);
            UCSR0A |= (1<<U2X0);
        } else {
            UBRR0L = 0xff & UBRR_2x_off;
            UBRR0H = 0xff & (UBRR_2x_off>>8);
            UCSR0A &= ~(1<<U2X0);
        }
    }
    /////////////////////////
    //    Configuration Registers
    UCSR0B = (0<<RXCIE0) |//We don't want this interrupt
    (0<<TXCIE0) |//We don't want this interrupt
    (0<<UDRIE0) |//We don't want this interrupt
    (1<<RXEN0) |//Enable RX, we wont use it here but it can't hurt
    (1<<TXEN0) |//Enable TX, for Talkin'
    (0<<UCSZ02);//We want 8 data bits so set this low

    UCSR0A |= (0<<U2X0) |//already set up, so don't mess with it
    (0<<MPCM0) ;//We wont need this

    UCSR0C = (0<<UMSEL01) | (0<<UMSEL00) |//We want UART mode
    (0<<UPM01) | (0<<UPM00) |//We want no parity bit
    (0<<USBS0) |//We want only one stop bit
    (1<<UCSZ01) | (1<<UCSZ00) |//We want 8 data bits
    (0<<UCPOL0) ;//This doesn't effect UART mode
}

```

<b>UPDATE:</b> A day later I added multiple sensors to the device. I calibrated one of them by putting it in a plastic bag and letting it set in ice water, then I calibrated the rest to that one. You can see as my room temperature slowly falls for the night, the open air sensor (red) drops faster than the insulated one in a Styrofoam box. Also, I did a touch of math to convert voltage to kelvin to Fahrenheit. You can also see spikes where it quickly approached 90+ degrees from the heat of my fingers as I handled the sensor. Cool!

<div class="text-center"> 

[![](https://swharden.com/static/2010/11/24/3traces_thumb.jpg)](https://swharden.com/static/2010/11/24/3traces.png)

</div>

<b>UPDATE:</b> a day and a half later, here's what the fluctuations look like. Notice the cooling of night, the heating of day, and now (near the end of the graph) the scattered rain causes more rapid fluctuations. Also, although one sensor is in an insulated styrofoam box, it still fluctuates considerably. This measurement system is prepped and ready to go for crystal oven tests!

<div class="text-center"> 

[![](https://swharden.com/static/2010/11/24/insulated3_thumb.jpg)](https://swharden.com/static/2010/11/24/insulated3.png)

</div>