---
title: Play Audio from SPI Flash with a Microcontroller
description: How to use a microcontroller to drive a speaker using PWM from audio levels stored in a SPI flash chip
Date: 2023-08-26 20:00:00
tags: ["circuit", "microcontroller"]
---

**This project uses a microcontroller's PWM output to drive a speaker and play audio stored in a SPI flash chip.** This article combines what was learned in my two previous articles: [play audio with a microcontroller](https://swharden.com/blog/2023-08-19-speaking-microcontroller/) and [use a FT232H to program a SPI flash chip](https://swharden.com/blog/2023-08-24-ft232h-spi-flash/) which go into more detail about the circuitry and code behind each of these major steps. By encoding audio at 8-bit resolution with an 8 kHz sample rate, 32 Mb (4 MB) of memory is sufficient to store approximately 8 minutes of raw audio. In this project I'm using a [W25Q32](https://www.elinux.org/images/f/f5/Winbond-w25q32.pdf) breakout board available on Amazon for about $2 each. Although many similar projects online demonstrate audio playback using SD cards, I find the strategies demonstrated here favorable for simple projects because it can be achieved with the addition of only a single inexpensive component.

<a href="https://swharden.com/static/2023/08/25/arduino-audio-1.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/25/arduino-audio-1.jpg">
</a>

## Play Audio from SPI Flash with Arduino

**Audio levels are stored in the SPI flash memory, so by reading each address and setting the PWM level to that value at a rate of 8 kHz, the sounds stored in flash memory can be played back in real time.** Here are the important parts of the Arduino code I used to achieve continuous audio playback, and the full source code can be reviewed in [`audio.ino`](https://github.com/swharden/AVR-projects/blob/master/Arduino%20SPI%20audio/test1/test1.ino) on GitHub.

```c
char spi_transfer(char data) {
  SPDR = data;
  while (!(SPSR & (1 << SPIF))) {};
  return SPDR;
}

volatile long SOURCE_ADDRESS;

void loop() {
  digitalWrite(CS, LOW);
  spi_transfer(0x03);
  spi_transfer(SOURCE_ADDRESS >> 16);
  spi_transfer(SOURCE_ADDRESS >> 8);
  spi_transfer(SOURCE_ADDRESS >> 0);
  OCR2B = spi_transfer(255);
  digitalWrite(CS, HIGH);

  SOURCE_ADDRESS++;

  delayMicroseconds(88); // determined experimentally
}
```

The additional circuitry on the breadboard is for power supply filtering and audio amplification using a LM386 as described in [my previous article](http://localhost:1313/blog/2023-08-19-speaking-microcontroller/).

The delay between each cycle of the main loop (88 µs) was determined experimentally to achieve approximately 8 kHz playback. Ideally another timer's interrupt could manage playback, but the Arduino's primary timer is occupied with systems tasks (like timing) and the secondary timer is used for PWM (to generate the analog audio output waveform), so this was the simplest option. An alternative approach could probably be to slow down the PWM timer's period and use its overflow interrupt and a counter to manage frame advancement and flash memory reads outside the main program loop, but this code works well for demonstration purposes.

It's worth noting that accessing the flash memory at 8 kHz is also excessive. A more sophisticated approach is to use a buffer in memory to store chunks of audio data which can be tactically loaded from the SPI chip without requiring a full transaction on every PWM update. Building large buffers can be slow though, so managing the buffer should be performed carefully so as not to require more time than the 8 kHz interrupt needs to complete its cycle. 

### Arduino Audio Playback Demo

This video clip shows an Arduino using the strategy described above to play 8-bit audio stored in the SPI flash chip at 8 kHz. The song is [NIVIRO - The Guardian Of Angels](https://www.youtube.com/watch?v=yHU6g3-35IU) (NCS Release) provided by NoCopyrightSounds.

<div class="text-center my-5">
    <video playsinline controls class="border border-dark bg-dark shadow" style="width: 100%">
        <source src="https://swharden.com/static/2023/08/25/arduino-audio.webm" type="video/webm">
    </video>
</div>

## Play Audio from SPI Flash with AVR

**Let's leave Arduino behind and use a more sophisticated 8-bit AVR microcontroller.** The AVR64DD32 is one of most advanced 8-bit AVR microcontrollers currently on the market. Modern AVR microcontrollers cannot be programmed with a traditional ICSP programmer but instead [require a UPDI programmer](https://swharden.com/blog/2022-12-09-avr-programming/). However, these newer microcontrollers sport three timers (two 16-bit and one 12-bit) and even the ability to clock them asynchronously from the main clock. We won't need all these advanced features, but we will do a better job than the Arduino can simultaneously managing the PWM level with one timer and managing interrupts at 8 kHz with another timer, keeping the main loop unblocked. Here's the gist of how I achieved this, and the full source code can be reviewed in [`main.c`](https://github.com/swharden/AVR-projects/blob/master/AVR64DD32%20SPI%20audio/main.c) on GitHub.

The additional circuitry on the breadboard is for power supply filtering and audio amplification using a LM386 as described in [my previous article](http://localhost:1313/blog/2023-08-19-speaking-microcontroller/).

```cs
volatile long AUDIO_ADDRESS;

uint8_t SPI_SEND(uint8_t data){
	SPI0.DATA = data;
	while (!(SPI0.INTFLAGS & SPI_IF_bm));
	return SPI0.DATA;
}

ISR(TCA0_OVF_vect)
{
    // read the level from an address in flash memory
    SPI_CS_LOW();
    SPI_SEND(0x03);
    SPI_SEND(AUDIO_ADDRESS >> 16);
    SPI_SEND(AUDIO_ADDRESS >> 8);
    SPI_SEND(AUDIO_ADDRESS >> 0);
    uint8_t level = SPI_SEND(0xFF);
    SPI_CS_HIGH();

    // set PWM duty update after the next rollover
    while(TCB0.CNT > 0){}
    TCB0.CCMPH = level;
    AUDIO_ADDRESS++;
    TCA0.SINGLE.INTFLAGS = TCA_SINGLE_OVF_bm;
}
```

<a href="https://swharden.com/static/2023/08/25/avr64-dd-audio-3.jpg">
<img  class="border border-dark shadow" src="https://swharden.com/static/2023/08/25/avr64-dd-audio-3.jpg">
</a>

### AVR Playback Demo

This video clip shows an AVR64DD32 using the strategy described above to play 8-bit audio stored in the SPI flash chip at 8 kHz. The song is [NIVIRO - The Guardian Of Angels](https://www.youtube.com/watch?v=yHU6g3-35IU) (NCS Release) provided by NoCopyrightSounds. The LED blinking is the result of an infinite loop running inside `main()` demonstrating that the main program is not blocked during playback.

<div class="text-center my-5">
    <video playsinline controls class="border border-dark bg-dark shadow" style="width: 100%">
        <source src="https://swharden.com/static/2023/08/25/avr-audio.webm" type="video/webm">
    </video>
</div>

## Conclusions

**For short audio clips [a microcontroller's program memory can be used to store audio](https://swharden.com/blog/2023-08-19-speaking-microcontroller/), but for minutes of audio SPI flash memory can be used to source the audio waveform.** On the upper extreme SD cards can be used to store audio, but there are [plenty](https://www.arduino.cc/reference/en/libraries/audiozero/) of online resources describing how to achieve this. My last few days exploring using in-chip program memory and SPI-accessible flash memory for audio playback in 8-bit microcontrollers with minimal external circuitry has been an interesting journey, and I look forward to using these techniques in upcoming embedded projects that require playback of stored audio.

## Resources

* [Program SPI Flash with a FT232H](https://swharden.com/blog/2023-08-24-ft232h-spi-flash/)

* [Play Audio Stored in a Microcontroller's Program Memory](https://swharden.com/blog/2023-08-19-speaking-microcontroller/)

* Source code (Arduino) [`audio.ino`](https://github.com/swharden/AVR-projects/blob/master/Arduino%20SPI%20audio/test1/test1.ino) on GitHub

* Source code (AVR64DD32) [`main.c`](https://github.com/swharden/AVR-projects/blob/master/AVR64DD32%20SPI%20audio/main.c) on GitHub

* [AVR64DD32 datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/AVR64DD32-28-Prelim-DataSheet-DS40002315B.pdf)

* The speakers featured in this project are convenient because they come in their own small resonant cavity. I found them [on Amazon](https://www.amazon.com/gp/aw/d/B0BGWY5PM9) for about $2 each.

* [NIVIRO - The Guardian Of Angels](https://www.youtube.com/watch?v=yHU6g3-35IU) (NCS Release) provided by [NoCopyrightSounds](https://ncs.io/)