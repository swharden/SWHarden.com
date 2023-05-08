---
title: PC/microcontroller “wireless” data transfer (part 2)
date: 2011-07-31 22:35:12
tags: ["circuit", "microcontroller", "old"]
---

# PC/microcontroller “wireless” data transfer (part 2)

This is one part of a multi-post project

__Last week I had the crazy idea__ of sending data from a PC to a microchip through the monitor, using javascript and a web interface as a ridiculously simple data transfer platform that would work on virtually any computer! While I quickly hacked together the hardware, I struggled with the web interface (I'm a little slow with javascript) and I got a lot of help from people around the internet, especially after my project (and need for assistance) was mentioned on [Hack-A-Day](http://hackaday.com/2011/07/28/microcontroller-communications-using-flashing-lights/)!


<div class="text-center img-border">

![](https://swharden.com/static/2011/07/31/DSCN1657.jpg)

</div>

__This is part two of a multi-page project.__ To fully understand what I'm trying to accomplish and why I want to accomplish it, read [the first part of the project](http://www.swharden.com/blog/2011-07-26-pcmicrocontroller-wireless-data-transfer/).

{{<youtube wMHR3j4EDQ4>}}

__Finally, I have a working javascript!__ I'd like to thank Tom, Riskable, Ben, and Mike for their input on this script. We got it to a point where we think it's friendly to the majority of browsers and platforms. The idea is simple - enter two bytes to send the chip, it generates it's own checksum (an XOR of the two bytes), and it flashes it out. Here's a photo of the interface, click it for a live demo:


<div class="text-center img-border">

![](https://swharden.com/static/2011/07/31/flasher_interface.jpg)

</div>

<strong>Here's the code that goes on the microchip:</strong>

```c

#include <stdlib.h>
#include <avr/io.h>
#include <avr/pgmspace.h>
#define F_CPU 12000000UL
#include <util/delay.h>
#include "lcd.h"
#include "lcd.c"

volatile int times=1000;

char readADC(char pin){
  ADMUX = 0b1100000+pin; // AVCC ref on ADC5
  ADCSRA = 0b10000111; //ADC Enable, Manual Trigger, Prescaler 128
  ADCSRA |= (1<<ADSC); // reset value
  while (ADCSRA & ( 1<<ADSC)) {}; // wait for measurement
  return ADCH;
}

int main(void)
{
  lcd_init(LCD_DISP_ON);
  char lastClock=0;
  char thisClock=0;
  char thisClock2=0;
  char thisData=0;
  char buffer[8];

  char lastNum=0;
  char bitsGotten=0;

  int msInactive=0;

  /*for(;;){
    itoa(readADC(5), buffer, 10);
    lcd_gotoxy(0,15);
    lcd_puts(buffer);

    itoa(readADC(4), buffer, 10);
    lcd_gotoxy(8,0);
    lcd_puts(buffer);
  }*/

  for(;;){
    thisClock = readADC(5);
    if (thisClock<250){
      _delay_ms(1);
      if (readADC(5)>250) {break;}

      _delay_ms(1);
      if (readADC(4)<250) {thisData=1;}
      else {thisData=0;}
      lastNum=lastNum*2+thisData; // left shift, add data
      itoa(thisData, buffer, 10);
      lcd_puts(buffer);
      msInactive=0;

      bitsGotten++;
      if (bitsGotten==8){
        lcd_gotoxy(1,1);
        lcd_puts("=   ");
        lcd_gotoxy(2,1);
        itoa(lastNum, buffer, 10);
        lcd_puts(buffer);
        bitsGotten=0;
        lastNum=0;
        lcd_gotoxy(0,0);
      }

      while (1) {
        if (readADC(5)>250){
          _delay_ms(10);
          if (readADC(5)>250){break;}
        }
      }
    }
    else{
      msInactive++;
      if (msInactive==400){
        bitsGotten=0;
        lastNum=0;
        lcd_clrscr();
        lcd_puts(" TIMEOUT");
        _delay_ms(1000);
        lcd_clrscr();
        lcd_gotoxy(0,0);
        lcd_puts("________ =");
        lcd_gotoxy(0,0);
      }
    }
    _delay_ms(1);
  }
}
```

<strong>Here's the javascript in a web page:</strong>

```html
<html>
<head>
<style>
.flasher {
  font-weight: bold;
  text-align: center;
  color: #888888;
  width: 200px;
  height: 200px;
  background-color: black;
  float: left;
  -webkit-transform: translateZ(0);
  border-right-style:dotted;
  border-color:#888888;
  border-width:1px;
}
</style>
<script type="text/javascript">

/* Copyright 2011, Tom Hayward <tom@tomh.us>, MIT License */

var ms = 50,
  bytes = 0,
  leftblock = null,
  rightblock = null,
  statustext = null;

function sendBit(bit) {
  if (bit) {rightblock.style.backgroundColor = 'white';}
  else {rightblock.style.backgroundColor = 'black';}
  leftblock.style.backgroundColor = 'white';
  setTimeout(function() {
  leftblock.style.backgroundColor = 'black';
  rightblock.style.backgroundColor = 'black';
  }, ms);
}

function sendByte(byte) {
  var bits = 8;
  setTimeout(function() {
  var timer = setInterval(function() {
    bits--;
    sendBit(byte >> bits & 1);
    if (bits == 0) {clearInterval(timer);return;}
  }, ms * 2);
  }, ms * 2 * bits * bytes++);
}

function Pause() {
timer = setTimeout("endpause()",5000); // 3 secs
return false;
}

function endpause() {
sendData();
return false;
}

function sendData() {

  var button = document.getElementById('sendnow'),
    byte1 = parseInt(document.getElementById('b1').value),
    byte2 = parseInt(document.getElementById('b2').value),
    checksum = byte1 ^ byte2;
  leftblock = document.getElementById('leftblock');
  rightblock = document.getElementById('rightblock');
  statustext = document.getElementById('status');
  bytes = 0; // reset byte counter

  document.getElementById('b3').value = checksum;
  button.disabled = true;
  statustext.innerHTML = "Writing data...";

  sendByte(byte1);
  sendByte(byte2);
  sendByte(checksum);

  setTimeout(function() {
  statustext.innerHTML = "done";
  button.disabled = false;
  }, ms * 2 * 8 * bytes);

}

</script>
</head>
<body bgcolor="#666">

<h1>PC/MCU Flasher Interface</h1>
<code>
Byte 1: <input id="b1" type="text" name="b1" size="3" value="255" /> <br>
Byte 2: <input id="b2" type="text" name="b2" size="3" value="0" />  <br>
CHKsum: <input id="b3" type="text" name="b3" size="3" value="" disabled="disabled" />  <br>
<br>
<input id="sendnow" type="button" value="SEND NOW" onClick="javascript:Pause();" />
<br><br><br>
<p>Status: <span id="status"></span></p>
</code>
<div id="leftblock" class="flasher"> CLOCK</div>
<div id="rightblock" class="flasher"> DATA</div>

</body>
</html>
```