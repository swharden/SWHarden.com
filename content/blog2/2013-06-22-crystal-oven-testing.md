---
title: Crystal Oven Testing
date: 2013-06-22 15:14:37
tags: ["circuit", "obsolete"]
---



__To maintain high frequency stability, RF oscillator circuits are sometimes "ovenized" where their temperature is raised slightly above ambient room temperature and held precisely at one temperature.__ Sometimes just the crystal is heated (with a "crystal oven"), and other times the entire oscillator circuit is heated. The advantage of heating the circuit is that other components (especially metal core instructors) are temperature sensitive. Googling for the phrase "crystal oven", you'll find no shortage of recommended circuits. Although a more complicated[ PID (proportional-integral-derivative) controller](http://en.wikipedia.org/wiki/PID_controller) may seem enticing for these situations, the fact that the enclosure is so well insulated and drifts so little over vast periods of time suggests that it might not be the best application of a PID controller. One of my favorite write-ups is from [M0AYF's site](http://www.qsl.net/m0ayf/Crystal-Ovens.html) which describes how to build a crystal oven for QRSS purposes. He demonstrates the MK1 and then the next design the MK2 crystal oven controller.

__Briefly, desired temperature is set with a potentiometer.__ An operational amplifier (op-amp) compares the target temperature with measured temperature (using a thermistor - a resistor which varies resistance by tempearture). If the measured temperature is below the target, the op-amp output goes high, and current flows through heating resistors. There are a few differences between the two circuits, but one of the things that struck me as different was the use of negative feedback with the operational amplifier. This means that rather than being on or off (like the air conditioning in your house), it can be on a little bit. I wondered if this would greatly affect frequency stability. In the original circuit, he mentions

The oven then cycles on and off roughly every thirty or forty seconds and hovers around 40 degrees-C thereafter to within better than one degree-C.
__I wondered how much this on/off heater cycle affected temperature. Is it negligible, or could it affect frequency of an oscillator circuit?__ Indeed his application heats [an entire enclosure](http://www.qsl.net/m0ayf/Crystal-Ovens/OCXO.jpg) so small variations get averaged-out by the large thermal mass. However in crystal oven designs where only the crystal is heated, such as [described by Bill (W4HBK)](http://pensacolasnapper.blogspot.com/2011_03_01_archive.html), I'll bet the effect is much greater. Compare the thermal mass of these two concepts.

<div class="text-center img-border img-small">

![](https://swharden.com/static/2013/06/22/m0ayf-enclosure-oven.jpg)
![](https://swharden.com/static/2013/06/22/w4hbk-crystal-oven.jpg)

</div>

__How does the amount of thermal mass relate to how well it can be controlled?__ How important is negative feedback for partial-on heater operation? Can simple ON/OFF heater regulation adequately stabalize a crystal or enclosure? I'd like to design my own heater, pulling the best elements from the rest I see on the internet. My goals are:

1.   use inexpensive thermistors instead of linear temperature sensors (like [LM335](http://www.ti.com/lit/ds/symlink/lm335.pdf))
2.   use inexpensive quarter-watt resistors as heaters instead of power resistors
3.   be able to set temperature with a knob
4.   be able to monitor temperature of the heater
5.   be able to monitor power delivered to the heater
6.   maximum long-term temperature stability

__Right off the bat, I realized that this requires a PC interface.__ Even if it's not used to adjust temperature (an ultimate goal), it will be used to log temperature and power for analysis. I won't go into the details about how I did it, other than to say that I'm using an ATMEL ATMega8 AVR microcontroller and ten times I second I sample voltage on each of it's six 10-bit ADC pins (PC0-PC5), and send that data to the computer with USART using an eBay special serial/USB adapter based on FTDI. They're <$7 (shipped) and come with the USB cable. Obviously in a consumer application I'd etch boards and use the SMT-only FTDI chips, but for messing around at home I a few a few of these little adapters. They're convenient as heck because I can just add a heater to my prototype boards and it even supplies power and ground. Convenient, right? Power is messier than it could be because it's being supplied by the PC, but for now it gets the job done. On the software side, Python with PySerial listens to the serial port and copies data to a large numpy array, saving it every once and a while. Occasionally a bit is sent wrong and a number is received incorrectly (maybe one an hour), but the error is recognized and eliminated by the checksum (just the sum of all transmitted numbers). Plotting is done with numpy and matpltolib. Code for all of that is at the bottom of this post.

<div class="text-center img-border img-micro">

![](https://swharden.com/static/2013/06/22/IMG_0278.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0279.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0280.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0282.jpg)

</div>

__That's the data logger circuit I came up with.__ Reading six channels ten times a second, it's more than sufficient for voltage measurement. I went ahead and added an op-amp to the board too, since I knew I'd be using one. I dedicated one of the channels to serve as ambient temperature measurement. See the little red thermistor by the blue resistor? I also dedicated another channel to the output of the op-amp. This way I can measure drive to whatever temperature controller circuity I choose to use down the road. For my first test, I'm using a small thermal mass like one would in a crystal oven. Here's how I made that:

<div class="text-center img-border img-micro">

![](https://swharden.com/static/2013/06/22/IMG_0265.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0264.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0263.jpg)
![](https://swharden.com/static/2013/06/22/IMG_0262.jpg)

</div>

__I then build the temperature controller part of the circuit.__ It's pretty similar to that previously published. it uses a thermistor in a voltage divider configuration to sense temperature. It uses a trimmer potentiometer to set temperature. An LED indicator light gives some indication of on/off, but keep in mind that a fraction of a volt will turn the Darlington transistor (TIP122) on slightly although it doesn't reach a level high enough to drive the LED. The amplifier by default is set to high gain (55x), but can be greatly lowered (negative gain actually) with a jumper. This lets me test how important gain is for the circuitry.

<div class="text-center img-medium">

![](https://swharden.com/static/2013/06/22/controller.png)

</div>

<div class="text-center img-border">

![](https://swharden.com/static/2013/06/22/IMG_0261.jpg)

</div>

__When using a crystal oven configuration, I concluded high high gain (cycling the heater on/off) is a BAD idea.__ While average temperature is held around the same, the crystal oscillates. This is what is occurring above when M0AYF indicates his MK1 heater turns on and off every 40 seconds. While you might be able to get away with it while heating a chassis or something, I think it's easy to see it's not a good option for crystal heaters. Instead, look at the low gain (negative gain) configuration. It reaches temperature surprisingly quickly and locks to it steadily. Excellent.

<div class="text-center">

![](https://swharden.com/static/2013/06/22/high-gain.png)

</div>

high gain configuration tends to oscillate every 30 seconds

<div class="text-center">

![](https://swharden.com/static/2013/06/22/low-gain.png)

</div>

low gain / negative gain configuration is extremely stable (fairly high temperature)

<div class="text-center">

![](https://swharden.com/static/2013/06/22/low-gain1.png)

</div>

Here's a similar experiment with a lower target temperature. Noise is due to unregulated USB power supply / voltage reference. Undeniably, this circuit does not oscillate much if any

__Clearly low (or negative) gain is best for crystal heaters.__ What about chassis / enclosure heaters? Let's give that a shot. I made an enclosure heater with the same 2 resistors. Again, I'm staying away from expensive components, and that includes power resistors. I used epoxy (gorilla glue) to cement them to the wall of one side of the enclosure.

__I put a "heater sensor" thermistor near the resistors on the case so I could get an idea of the heat of the resistors, and a "case sensor" on the opposite side of the case.__ This will let me know how long it takes the case to reach temperature, and let me compare differences between using near vs. far sensors (with respect to the heating element) to control temperature. I ran the same experiments and this is what I came up with!

<div class="text-center">

![](https://swharden.com/static/2013/06/22/case.png)

</div>

heater temperature (blue) and enclosure temperature (green) with low gain (first 20 minutes), then high gain (after) operation. High gain sensor/feedback loop is sufficient to induce oscillation, even with the large thermal mass of the enclosure

__CLOSE SENSOR CONTROL, LOW/HIGH GAIN:__ TOP: heater temperature (blue) and enclosure temperature (green) with low gain (first 20 minutes), then high gain (after) operation. High gain sensor/feedback loop is sufficient to induce oscillation, even with the large thermal mass of the enclosure. BOTTOM: power to the heater (voltage off the op-amp output going into the base of the Darlington transistor). Although I didn't give the low-gain configuration time to equilibrate, I doubt it would have oscillated on a time scale I am patient enough to see. Future, days-long experimentation will be required to determine if it oscillates significantly.[/caption]

<div class="text-center">

![](https://swharden.com/static/2013/06/22/case-far-in-control.png)

</div>

Even with the far sensor (opposite side of the enclosure as the heater) driving the operational amplifier in high gain mode, oscillations occur. Due to the larger thermal mass and increased distance the heat must travel to be sensed they take much longer to occur, leading them to be slower and larger than oscillations seen earlier when the heater was very close to the sensor.

__FAR SENSOR CONTROL, HIGH GAIN:__ Even with the far sensor (opposite side of the enclosure as the heater) driving the operational amplifier in high gain mode, oscillations occur. Blue is the far sensor temperature. Green is the sensor near the heater temperature. Due to the larger thermal mass and increased distance the heat must travel to be sensed they take much longer to occur, leading them to be slower and larger than oscillations seen earlier when the heater was very close to the sensor.

__Right off the bat, we observe that even with the increased thermal mass of the entire enclosure (being heated with two dinky 100 ohm 1/4 watt resistors) the system is prone to temperature oscillation if gain is set too high.__ For me, this is the final nail in the coffin - I will never use a comparator-type high gain sensor/regulation loop to control heater current. With that out, the only thing to compare is which is better: placing the sensor near the heating element, or far from it. In reality, with a well-insulated device like I seem to have, it seems like it doesn't make much of a difference! The idea is that by placing it near the heater, it can stabilize quickly. However, placing it far from the heater will give it maximum sensation of "load" temperature. Anywhere in-between should be fine. As long as it's somewhat thermally coupled to the enclosure, enclosure temperature will pull it slightly away from heater temperature regardless of location. Therefore, I conclude it's not that critical where the sensor is placed, as long as it has good contact with the enclosure. Perhaps with long-term study (on the order of hours to days) slow oscillations may emerge, but I'll have to build it in a more permanent configuration to test it out. Lucky, that's exactly what I plan to do, so check back a few days from now!

__Since the data speaks for itself, I'll be concise with my conclusions:__

*   two 1/4 watt 100 Ohm resistors in parallel (50 ohms) are suitable to heat an insulated enclosure with 12V
*   two 1/4 watt 100 Ohm resistors in parallel (50 ohms) are suitable to heat a crystal with 5V
*   low gain or negative gain is preferred to prevent oscillating tempeartures
*   Sensor location on an enclosure is not critical as long as it's well-coupled to the enclosure and the entire enclosure is well-insulated.

I feel satisfied with today's work. Next step is to build this device on a larger scale and fix it in a more permanent configuration, then leave it to run for a few weeks and see how it does. On to making the oscillator! If you have any questions or comments, feel free to email me. If you recreate this project, email me! I'd love to hear about it.

__Here's the code that went on the ATMega8 AVR (it continuously transmits voltage measurements on 6 channels).__

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

int readADC(char adcn){
    ADMUX = 0b0100000+adcn;
    ADCSRA |= (1<<ADSC); // reset value
    while (ADCSRA & (1<<ADSC)) {}; // wait for measurement
    return ADC>>6;
}

int sendADC(char adcn){
    int val;
    val=readADC(adcn);
    sendNum(val);
    USART_Transmit(',');
    return val;
}

int main(void){
    ADCSRA = (1<<ADEN)  | 0b111;
    DDRB=255;
    USART_Init();
    int checksum;

    for(;;){
        PORTB=255;
        checksum=0;
        checksum+=sendADC(0);
        checksum+=sendADC(1);
        checksum+=sendADC(2);
        checksum+=sendADC(3);
        checksum+=sendADC(4);
        checksum+=sendADC(5);
        sendNum(checksum);
        USART_Transmit('n');
        PORTB=0;
        _delay_ms(200);
    }
}
```

__Here's the command I used to compile the code, set the AVR fuse bits, and load it to the AVR.__

```bash
del *.elf
del *.hex
avr-gcc -mmcu=atmega8 -Wall -Os -o main.elf main.c -w
pause
cls
avr-objcopy -j .text -j .data -O ihex main.elf main.hex
avrdude -c usbtiny -p m8 -F -U flash:w:"main.hex":a -U lfuse:w:0xe4:m -U hfuse:w:0xd9:m
```

__Here's the code that runs on the PC to listen to the microchip, match the data to the checksum, and log it occasionally. __

```python
import serial, time
import numpy
ser = serial.Serial("COM16", 38400, timeout=100)

line=ser.readline()[:-1]
t1=time.time()
lines=0

data=[]

def adc2R(adc):
    Vo=adc*5.0/1024.0
    Vi=5.0
    R2=10000.0
    R1=R2*(Vi-Vo)/Vo
    return R1

while True:
    line=ser.readline()[:-1]
    lines+=1
    if "," in line:
        line=line.split(",")
        for i in range(len(line)):
            line[i]=int(line[i][::-1])

    if line[-1]==sum(line[:-1]):
        line=[time.time()]+line[:-1]
        print lines, line
        data.append(line)
    else:
        print  lines, line, "<-- FAIL"

    if lines%50==49:
        numpy.save("data.npy",data)
        print "nSAVINGn%d lines in %.02f sec (%.02f vals/sec)n"%(lines,
            time.time()-t1,lines/(time.time()-t1))
```

__Here's the code that runs on the PC to graph data.__

```python
import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import numpy
import pylab
import datetime
import time

def adc2F(adc):
    Vo=adc*5.0/1024.0
    K=Vo*100
    C=K-273
    F=C*(9.0/5)+32
    return F

def adc2R(adc):
    Vo=adc*5.0/1024.0
    Vi=5.0
    R2=10000.0
    R1=R2*(Vi-Vo)/Vo
    return R1

def adc2V(adc):
    Vo=adc*5.0/1024.0
    return Vo

if True:
    print "LOADING DATA"
    data=numpy.load("data.npy")
    data=data
    print "LOADED"

    fig=pylab.figure()
    xs=data[:,0]
    tempAmbient=data[:,1]
    tempPower=data[:,2]
    tempHeater=data[:,3]
    tempCase=data[:,4]
    dates=(xs-xs[0])/60.0
    #dates=[]
    #for dt in xs: dates.append(datetime.datetime.fromtimestamp(dt))

    ax1=pylab.subplot(211)
    pylab.title("Temperature Controller - Low Gain")
    pylab.ylabel('Heater (ADC)')
    pylab.plot(dates,tempHeater,'b-')
    pylab.plot(dates,tempCase,'g-')
    #pylab.axhline(115.5,color="k",ls=":")

    #ax2=pylab.subplot(312,sharex=ax1)
    #pylab.ylabel('Case (ADC)')
    #pylab.plot(dates,tempCase,'r-')
    #pylab.plot(dates,tempAmbient,'g-')
    #pylab.axhline(0,color="k",ls=":")

    ax2=pylab.subplot(212,sharex=ax1)
    pylab.ylabel('Heater Power')
    pylab.plot(dates,tempPower)

    #fig.autofmt_xdate()
    pylab.xlabel('Elapsed Time (min)')

    pylab.show()

print "DONE"
```
