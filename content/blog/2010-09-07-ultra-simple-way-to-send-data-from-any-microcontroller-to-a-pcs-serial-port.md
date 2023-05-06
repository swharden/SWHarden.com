---
title: Simple method to send data from ANY microcontroller to a serial port
date: 2010-09-07 08:37:13
tags: ["microcontroller", "old"]
---

# Simple method to send data from ANY microcontroller to a serial port

__This weekend I had a need, and I met it with parts I had on hand.__ Simply put, I wanted to assess whether or not my temperature-controlled crystal heater is doing its job in keeping temperature rock-stable. I wanted to measure temperature by measuring the ADC (analog-to-digital) value at the middle of a voltage divider with a resistor and a thermistor. Using a computer to plot this data, I can see if temperature fluctuates as my apartment AC turns on/off, or if it's perfectly stable (my goal).  The problem is that my only MCU (micro-controller unit) with USART (universal asynchronous receiver/transmitter) built-in is an ATTiny2313, which has no ADC capabilities.  I had a lot of ATTiny44A chips on hand, so I had to figure out a way to get the data from my an ATTiny44A to an ATTiny2313 then to a MAX232 chip (voltage driver) so it can be sent to a PC's serial port.

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2010/09/07/IMG_3919.jpg)

</div>

This is my bare-bones solution to easily sending data from ANY microcontroller to a PC's serial port using 3 pins to send data to an ATTiny2313 which is interpreted, converted to decimal, then sent to my PC's serial port. I will keep this little board and use it often to peek at variables inside my microcontroller projects in real time, with minimal coding!

<div class="text-center img-medium">

![](https://swharden.com/static/2010/09/07/schematic_fixed2.jpg)

</div>

__Above is the bare-bones__ schematic required to send data from an ATTiny2313 to a PC via a serial port.  This schematic is improved and documented better on this page than on my previous post [Simple Case AVR/PC Serial Communication via MAX232](http://www.swharden.com/blog/2009-05-14-simple-case-avrpc-serial-communication-via-max232/). Note that I'm designing this to be functional, perhaps not well enough to be used in mission-critical systems. Although some schematics suggest extra capacitors, I found that the only one required is between pins 4 and 5 of the MAX232.  The role of the [MAX232 chip](http://en.wikipedia.org/wiki/MAX232) is to act as a voltage pump and relay the incoming signal at increased voltage which the PC's serial port can read. It doesn't actually change the data.

UPDATE: in a later project working with an ATMega48 I found that a capacitor was needed between pin 6 and ground - don't know why! If it's not working for you (you're getting garbage) start adding capacitors as shown in <a href="http://www.coolcircuit.com/circuit/rs232_driver/max232.gif">this MAX232 circuit</a>

__Power supply:__ Since the thing runs on 5V, we're golden!  Just grab a USB cable, hook up the black (ground) and red (+5V) wires, and you're good to go!  If you want you can add a few capacitors of different values in parallel to the power supply to stabilize fluctuations in voltage, but I've been doing just fine without this extra precaution.

__Display:__ The two LEDs are totally optional, but they let me see what's going on. One of them flashes when the device is waiting for data (to let me know it's on), and the other one turns on every time a [CLOCK] signal is detected (which is any time data is being sent)

__Notes on frequency and crystals.__ The UBRRL value in the code must be set depending on your micro-controller speed and desired baud rate. I set-up an Excel spreadsheet and did some math determining UBRRL for a combination of different frequencies/rates.  The UBRRL values closest to whole numbers are those which should be used to minimize errors.  External crystals are often used to increase and stabalize the clock speed of micro-controllers, but I was able to send serial data without a crystal.  I set the fuse for "internal 8mhz" clocking, and enabled the "div8" fuse so it actually ran at 1mhz. With these settings at 4800 baud, UBRR [according to the equation UBRR=(freq/(16*baud))-1] is 12.02 (pretty close to 12), so I set UBRRL=12 in the code and it sent data to a PC beautifully without a crystal. However, I had the desire to run the MCU faster to watch for incoming signals.  I therefore used a 9.21MHz crystal (I had to set the fuses to enable the external crystal), which can send serial data to a PC reliably at 19200 baud.

__Sending data to the ATTiny2313 to be relayed to the PC:__ Not every MCU has SPI, USI, I2C, TWI, USART, or other "standard" communication methods.  If I want to have a Texas Instruments or PIC or PICaxe chip send data to a PC, I have to decipher the datasheet and spend half a day to figure out how (yuk!).  Therefore, I developed an ULTRA-SIMPLE protocol of data transfer which can be used by ANY microcontroller.  Here's an example of a sensor microcontroller.  Although it's not shown, there's a thermistor (or some analog voltage being measured) somewhere.  It reads the sensor, then sends its data over the 3 wires [CLOCK], [A], and [B].

__Pulling-down the clock:__ Note that the 100k resistor shown pulling the [CLOCK] line to ground is critical.  It doesn't have to be 100k, it can be virtually any value, it just makes sure that if current is not being sent on the clock line, it quickly goes to 0V.  Without this resistor, the clock line might flicker on and off even though no data is being sent.

<div class="text-center">

![](https://swharden.com/static/2010/09/07/serial_example.jpg)

</div>

<div class="text-center img-border">

![](https://swharden.com/static/2010/09/07/IMG_3907.jpg)

</div>

<strong>Sending data this way is easy!</strong> The clock line is almost always low. When \[clock\] goes high, data is read. When data is read, the ATTiny2313 determines the state of \[A\] and \[B\]. If A=0 and B=0, a ZERO is sent. If A=1 and B=0, a ONE is sent. If A=0 and B=1, a SPACE is sent (between values). If A=1 and B=1, a LINE BREAK is sent. Values are sent in binary, and when a space or line break is detected, the binary value is converted to decimal and sent to the PC's serial port. It's not dependent on speed, so send data as fast (within reason) or slowly as you want from any microcontroller and it will end-up on your computer screen! It's that easy!</blockquote>

__FLAME ALERT:__ A lot of people will be mad at me for suggesting this method. There are fancier, faster, and more stable ways to data transfer between micro-controllers, but this works well at moderate speeds (maybe 10 measurements a second?) and I can implement this on any microcontroller in seconds, without puzzling over the datasheet.

## BREADBOARDED PROTOTYPE

Remember that I'm powering this entirely from USB power. The layout is simple: ATTiny44A measuring ADC of a thermistor on the left (see the little red thing?) sending data with 3 wires (top 3) to an ATTiny2313 intermediate chip (center), which converts this binary data to decimal and sends it to a MAX232 chip (right) where it gets converted to levels suitable for transmission to a serial port.


<div class="text-center img-border img-micro">

![](https://swharden.com/static/2010/09/07/IMG_3905.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3891.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3899.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3904.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3907.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3922.jpg)
![](https://swharden.com/static/2010/09/07/IMG_3919.jpg)

</div>

### CODE (AVR-GCC)

This is what runs on the ATTiny2313 intermediate chip:

```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define B PB2
#define A PB1
#define clk PB0
unsigned int times = 0;

// THIS RUNS ON THE ATTINY2313
// FUSES SET FOR INTERNAL 8MHZ, DIV/8=TRUE
// LISTENS ON PINS 12 (CLOCK), 13 (DATA), AND 14 (TRANSMIT)
// OUTPUTS TO A MAX232 THEN TO SERIAL PORT
// PC TERMINAL SET TO LISTEN AT 4800 BAUD

int main(void)
{
    UBRRL = 29;                          // value determined for 9.21MHz crystal at 19200 baud
    UCSRB = (1 << RXEN) | (1 << TXEN);   // fire-up USART
    UCSRC = (1 << UCSZ1) | (1 << UCSZ0); // fire-up USART
    DDRB = 0;                            // set all of port b to input
    DDRD = 255;                          // set all of port d to output
    char last = 255;
    int var = 0;
    char pos = 0;
    char i = 0;
    for (;;)
    {
        while
            bit_is_clear(PINB, clk) { blink(); }
        PORTD |= (1 << PD5);
        PORTD &= ~(1 << PD4);
        if (bit_is_set(PINB, A) && bit_is_clear(PINB, B))
        {
            var = (var << 1) + 1;
        } //ONE
        if (bit_is_clear(PINB, A) && bit_is_clear(PINB, B))
        {
            var = (var << 1);
        } //ZERO
        if (bit_is_clear(PINB, A) && bit_is_set(PINB, B))
        {
            show(var);
            var = 0;
            send(32);
        } //SPACE
        if (bit_is_set(PINB, A) && bit_is_set(PINB, B))
        {
            show(var);
            var = 0;
            send(10);
            send(13);
        } //BREAK
        while
            bit_is_set(PINB, clk) { blink(); }
        PORTD &= ~(1 << PD5);
        PORTD |= (1 << PD4);
    }
}
void blink()
{
    // just hanging out
    times++;
    if (times == 10000)
    {
        times == 0;
        PORTD |= (1 << PD3);
    }
    if (times == 20000)
    {
        times == 0;
        PORTD &= ~(1 << PD3);
        times = 0;
    }
}

unsigned int rev(unsigned int b)
{
    unsigned char result = 0;
    while (b)
    {
        result <<= 1;
        result |= b % 2;
        b >>= 1;
    }
    return result;
}

void show(unsigned int val)
{
    // SHOW INDIVIDUAL 1s and 0s?
    // for (char i=0;i<16;i++){
    //   if (val&(1<<i)){send(49);}
    //   else {send(48);}
    // }
    // send(61);

    val = rev(val);
    if (val == 0)
    {
        send(48);
    }
    else
    {
        char started = 0;
        int div = 10000;
        for (char i = 0; i < 5; i++)
        {
            if (val > div)
            {
                started = 1;
            }
            if (started)
            {
                send(val / div + 48);
                val = val - (val / div) * div;
            }
            div = div / 10;
        }
    }
    return;
}

void send(unsigned char data)
{
    while (!(UCSRA & (1 << UDRE)))
        ;       // wait for buffer to be empty
    UDR = data; // send that sucker
}
```

**This is what runs on my ATTiny44a sensor chip.** This is what you can replace with ANYTHING, as long as it twiddles the [clock], [a], and [b] pins similarly.

```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define dtaprt PORTA
#define clk PA1
#define A PA2
#define B PA0
#define delayms 100 // increase to slow it down

void wait() { _delay_ms(delayms); }
void clockNow()
{
    dtaprt |= (1 << clk);
    wait();
    dtaprt &= ~(1 << clk);
    wait();
}
void sendSpace()
{
    dtaprt = (1 << B);
    clockNow();
}
void sendLine()
{
    dtaprt = (1 << B) | (1 << A);
    clockNow();
}
void sendOne()
{
    dtaprt = (1 << A);
    clockNow();
}
void sendZero()
{
    dtaprt = 0;
    clockNow();
}

// TAKE A READING FROM ADC7 AND SEND IT TO SERIAL CHIP

int main(void)
{
    DDRA |= (1 << clk);
    DDRA |= (1 << A);
    DDRA |= (1 << B);
    ADMUX = (1 << REFS1) | (1 << MUX2) | (1 << MUX1) | (1 << MUX0);    // ADC on ADC7 to 1.1v ref
    ADCSRA = (1 << ADEN) | (1 << ADPS0) | (1 << ADPS1) | (1 << ADPS2); // enable, prescale
    for (;;)
    {
        int data = ReadADC();
        sendData(data);
        sendSpace();
        sendData(data);
        sendLine();
        _delay_ms(1000);
    }
}

void sendData(int data)
{
    char datalen = 16;
    for (char pos = 0; pos < datalen; pos++)
    {
        if ((data >> pos) & 1)
        {
            sendOne();
        }
        else
        {
            sendZero();
        }
    }
}

int ReadADC()
{
    ADCSRA |= (1 << ADSC); // reset value
    while (ADCSRA & (1 << ADSC))
        ; // wait for measurement
    return ADC;
}
```

### UPDATE

I found a simpler way to convert binary numbers into strings ready to be sent in ASCII via USART serial port:

```c
void sendNum(unsigned int num)
{
    char theIntAsString[7];
    int i;
    sprintf(theIntAsString, "%u", num);
    for (i = 0; i < strlen(theIntAsString); i++)
    {
        send(theIntAsString[i]);
    }
}
```