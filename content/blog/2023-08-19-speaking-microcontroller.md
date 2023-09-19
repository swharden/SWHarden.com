---
title: Speaking Numbers with a Microcontroller
description: How to encode WAV files into C code that can be replayed from memory
Date: 2023-08-19 23:00:00
tags: ["circuit", "microcontroller"]
featured_image: https://swharden.com/static/2023/08/19/arduino-speaker-speech-2.jpg
---

**This page describes the technique I used to get a microcontroller to speak numbers out loud.** Reading numbers from a speaker is an interesting and simple alternative to displaying numbers on a display, which often requires complex multiplexing circuitry and/or complex software to drive the display. This page describes the techniques I used to extract audio waveforms from MP3 files and encode them into data that can be stored in the microcontroller's flash memory. 

<a href="https://swharden.com/static/2023/08/19/arduino-speaker-speech-2.jpg">
<img class="border-dark border shadow" src="https://swharden.com/static/2023/08/19/arduino-speaker-speech-2.jpg">
</a>

**Because microcontrollers have a limited amount of flash memory this method is not suitable for long recordings, but it is fine for storing a few seconds of audio at a limited sample rate.** Unlike more common methods for playing audio with a microcontroller, playing audio from program memory does not require a SD card, special hardware, or complex audio decoding software. Although this technique works best when a speaker is driven with a amplifier circuit, I found acceptable audio can be produced by driving a speaker directly from a microcontroller pin. This technique makes it possible to play surprisingly good audio without requiring any components other than a speaker.

## NumberSpeaker Arduino Library

**The code described on this page has been packaged into the [`NumberSpeaker`](https://www.arduino.cc/reference/en/libraries/numberspeaker/) library that can be installed from the Arduino library manager.** Users who just wish to have some numbers read out loud can use this library and not hassle with the complex techniques described lower on this page. Source code is [available on GitHub](https://github.com/swharden/NumberSpeaker), but to get started using it you can perform the following steps:

* Connect a speaker to `pin 11`
* Open the Arduino IDE and create a new sketch
* Press `CTRL+SHIFT+i` to open the library manager
* Search for `NumberSpeaker` and select `Install`
* Paste the following into your sketch

```cpp
#include "NumberSpeaker.h"

NumberSpeaker numberSpeaker = NumberSpeaker();

void setup() {
  numberSpeaker.begin();  // speaker on pin 11
}

void loop() {
  unsigned int count = 0;
  for (;;) {
    numberSpeaker.speak_int(count++);
    delay(500);
  }
}
```

## Theory of Operation

* Start with a folder of mp3 files, one per spoken number
* Band-pass the audio between 100 Hz and 2.5 kHz
* Resample the audio (with interpolation) to 5 kHz
* Convert the 16-bit signed waveform to 8-bit unsigned values
* Store the values as a byte array in the microcontroller's memory
* Setup the microcontroller to drive a pin using 8-bit PWM at high frequency
* Set the PWM level from the stored waveform, advancing every 200 µs (5 kHz)
* Use a hardware low-pass filter create an analog waveform from the digital PWM output
* Pass the waveform through an audio amplifier (optional)
* Drive a speaker

<div class="text-center my-5">
    <video playsinline controls class="border border-dark bg-dark shadow" style="width: 100%">
        <source src="https://swharden.com/static/2023/08/19/numbers.webm" type="video/webm">
    </video>
</div>

## Encoding the Audio

**After some trial and error I found that 5 kHz 8-bit data is a good balance of quality vs. size for storing a human voice in program memory.** The 5kHz sample rate has a 2.5 kHz Nyquist frequency, meaning it can reproduce audio from 0-2.5 kHz which I found acceptable for voice. For music I found it helps to increase sample rate to 8 kHz. To reduce encoding artifacts that may result from such an aggressive reduction in sample rate, a low-pass filter is useful to apply to the audio before resampling it. Resampling should also be performed using interpolation, allowing the smooth reduction of sample rate by an arbitrary scale factor.

Full source code is available on the [NumberSpeaker GitHub project](https://github.com/swharden/NumberSpeaker).

Here's a slimmed-down version of the Python code I used to perform these operations:

```py
# read audio values from file
ys, sample_rate = librosa.load("zero.mp3")

# lowpass filter
new_sample_rate = 5_000
freq_low = 150
freq_high = new_sample_rate/2
sos = scipy.signal.butter(6, [freq_low, freq_high], 'bandpass', fs=sample_rate, output='sos')
ys = scipy.signal.sosfilt(sos, ys)

# resample with interpolation
xs_new = numpy.arange(len(ys)) / new_sample_rate
xs = numpy.arange(len(ys)) / sample_rate
ys = numpy.interp(xs_new, xs, ys)

# scale to [0, 255] and quantize
ys = ys / max(abs(min(ys)), abs(max(ys)))
ys = ys / 2 + .5
ys = ys * 255
ys = ys.astype(numpy.int16)
```

I then used python to loop across a folder of MP3 files and generate a C header file containing the waveforms for each recording stored as a byte array:

```c
const uint8_t AUDIO_1[] PROGMEM = { 129, 125, ..., 130, 132 };
const uint8_t AUDIO_2[] PROGMEM = { 127, 123, ..., 134, 130 };
const uint8_t AUDIO_3[] PROGMEM = { 122, 124, ..., 137, 135 };
```

**Waveforms are stored in program memory** using the `PROGMEM` keyword and later retrieved using `pgm_read_byte()` function. See AVR-GCC's [Program Space Utilities documentation](https://www.nongnu.org/avr-libc/user-manual/group__avr__pgmspace.html) for additional information.

## Playing the Audio

**An 8-bit timer is used to generate the PWM signal that creates the audio waveform.** I used Timer2 to generate this signal because Arduino uses Timer0 for its own tasks. I also setup the Timer2 settings myself to ensure it would run at maximum speed (ideal for generating waveforms using a simple R/C lowpass filter). Running with the 16 MHz system clock with no prescaler, the 8-bit timer overflows at a rate of 62.5 kHz.

```cs
// Use Timer2 to generate an analog voltage using PWM on pin 11
pinMode(11, OUTPUT); 

// Set OC2A on BOTTOM, clear OC2A on compare match
TCCR2A |= bit(COM2A1);

// Clock at CPU rate without prescaling.
TCCR2B = bit(CS20);

// Set the initial level to half the positive rail voltage
OCR2A = 127;
```

**Playback is achieved by setting PWM duty from the stored audio data.** Playback speed can be customized by adjusting the delay between sample advancements.

```c
for (int i = 0; i < sizeof(AUDIO_1); i++) {
    uint8_t value = pgm_read_byte(&AUDIO_1[i]);
    OCR2A = value; // 8-bit timer generating the PWM signal
    delayMicroseconds(200); // approximate delay for 5 kHz sample rate
}
```

## Memory Management

**Using the strategies above I was able to encode numbers 0-9 and the word "point" using a total of 16,720 bytes** (about half of the 32k program memory). I could save space by speeding-up the recordings (reading the numbers faster), but I found the present settings to be a good balance between comfort and memory consumption.

**I experimented with strategies that used 4 bytes instead of 8 to store the waveform,** but I found them unacceptably noisy. It may be possible to use 4-byte frames to store the difference between each point and the next, effectively halving memory required to store these waveforms. There are many signal compression algorithms we could employ to reduce the memory footprint, but for now the present strategy is working satisfactorily and has the benefit of minimal code complexity.

**External memory could be used to store more audio.** Arduino (ATMega328P) has 32 KB program memory and it must be shared with the main program code, so this places a restrictive upper limit on the total amount of audio data that may be stored on the chip itself. Users demanding more storage may benefit from interfacing a SPI flash memory IC. For example, [W25Q32JV](https://www.mouser.com/datasheet/2/949/w25q32jv_revg_03272018_plus-1489806.pdf) has 4 MB of flash memory and is [available on Mouser](https://www.mouser.com/ProductDetail/Winbond/W25Q32JVSSIQ?qs=qSfuJ%252Bfl%2Fd4PGZSN0WxfCA%3D%3D) for $0.76 each. At 5 kHz, a 4 MB flash memory chip could store over thirteen minutes of 8-bit audio. There's even a [SPIMemory](https://www.arduino.cc/reference/en/libraries/spimemory/) library for Arduino. However, some thought must be placed into [how to program the flash memory](https://learn.adafruit.com/programming-spi-flash-prom-with-an-ft232h-breakout/overview) with the audio waveform on your computer.

## Audio Amplification

**Driving headphones or a speaker directly with a PWM output pin works, but amplifying the signal substantially improves the quality of the sound.** The [LM386 single chip audio amplifier](https://www.ti.com/lit/ds/symlink/lm386.pdf) is technically obsolete (discontinued in 2016), but it's commonly used in hobby circles because clones are ubiquitously available in DIP packages which make them convenient for breadboarding. The [LM4862](https://www.ti.com/lit/ds/symlink/lm4862.pdf) is a better choice for serious designs as it is currently in production and does not require large electrolytic capacitors. I'm using the old LM386 here with the minimum of components and the default 20x gain experienced when pins 1 and 8 are left floating. 

**This is audio amplifier circuit I ended-up using for this project.** The combination of a 10 kΩ resistor and 0.1 µF capacitor formed a low-pass filter with -3 dB cutoff of about 160 Hz. This seems extremely aggressive since the 8-bit PWM frequency is 62.5 kHz, but I found this setup worked pretty well on my bench.

<a href="https://swharden.com/static/2023/08/19/schematic.jpg">
<img class="" src="https://swharden.com/static/2023/08/19/schematic.jpg">
</a>

<a href="https://swharden.com/static/2023/08/19/arduino-speaker-speech-1.jpg">
<img class="border-dark border shadow" src="https://swharden.com/static/2023/08/19/arduino-speaker-speech-1.jpg">
</a>

## Arduino Demo

**Here you can observe the digital PWM waveform (yellow) next to the low-pass filtered analog signal (blue).** I acknowledge that the oscilloscope demonstrates high frequency noise all over the place, but for the present application it doesn't really matter.

<div class="text-center my-5">
    <video playsinline controls class="border border-dark bg-dark shadow" style="width: 100%">
        <source src="https://swharden.com/static/2023/08/19/waveform.webm" type="video/webm">
    </video>
</div>

## Playing Audio from Newer AVR Chips

**Let's leave Arduino behind and switch to one of the more modern AVR microcontroller chips.** These newer 8-bit AVR microcontrollers offer a superior set of peripherals at lower cost and have greater availability. Unlike older AVR chips, these new AVR microcontrollers cannot be flashed using ICSP programmers. See my [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming/) page to learn how to use inexpensive gear to program the latest family of AVR chips with a UDPI programmer.

<a href="https://swharden.com/static/2023/08/19/arduino-meme.jpg">
<img class="mx-auto d-block border border-dark shadow" src="https://swharden.com/static/2023/08/19/arduino-meme.jpg">
</a>

**The [AVR64DD32 microcontroller](https://www.microchip.com/en-us/product/avr64dd32) is one of the highest-end 8-bit AVRs currently on the market.** It has 64 KB flash memory, and this increased size allowed me to experiment with storing longer recordings and at a higher sample rate. It's worth noting that the DA and DB family of chips has products with 128 KB of flash memory. Array lengths are limited to 32 KB, but I was able to circumvent this restriction by storing audio across multiple arrays and adding extra logic to ensure the correct source array is sampled.

<a href="https://swharden.com/static/2023/08/19/avr-wav-sound-1.jpg">
<img class="border-dark border shadow" src="https://swharden.com/static/2023/08/19/avr-wav-sound-1.jpg">
</a>

**These chips do not come in DIP packages,** but QFP/DIP breakout boards make them easy to experiment with in a breadboard.

<a href="https://swharden.com/static/2023/08/19/avr-wav-sound-2.jpg">
<img class="border-dark border shadow" src="https://swharden.com/static/2023/08/19/avr-wav-sound-2.jpg">
</a>

## AVR64 DD Code

**Two timers can be configured to achieve audio playback that does not block the main program.** This strategy uses two clocks to achieve asynchronous audio playback using interrupts to advance the waveform so it does not block main program execution.

Use the 24 MHz internal clock for the fastest PWM possible:

```c
#define F_CPU 24000000UL
```

```c
CCP = CCP_IOREG_gc; // Protected write
CLKCTRL.OSCHFCTRLA = CLKCTRL_FRQSEL_24M_gc; // Set clock to 24MHz
```

Setup the 8-bit TimerB to produce the PWM signal:
```c
// Enable PWM output on pin 32
// (don't forget to set the PORT direction)
TCB0.CTRLA |= TCB_ENABLE_bm;

// Make waveform output available on the pin
TCB0.CTRLB |= TCB_CCMPEN_bm;

// Enable 8-bit PWM mode
TCB0.CTRLB |= TCB_CNTMODE_PWM8_gc;

// Set period and duty
TCB0.CCMPL = 255; // top value
TCB0.CCMPH = 50; // flip value
```

Setup the 16-bit TimerA to advance the waveform at 5 kHz:

```c
// enable Timer A
TCA0.SINGLE.CTRLA |= TCA_SINGLE_ENABLE_bm;

// Overflow triggers interrupt
TCA0.SINGLE.INTCTRL |= TCA_SINGLE_OVF_bm;

// Set period and duty
TCA0.SINGLE.PER = F_CPU/5000; // 5 kHz audio
```

Populate the overflow event code:

```c
ISR(TCA0_OVF_vect)
{
    // read next level from program memory
    uint8_t level = pgm_read_byte(&AUDIO_SAMPLES[AUDIO_INDEX++]);
    
    // wait until next rollover to reduce static
    while(TCB0.CNT > 0){}

    // update the PWM level
	TCB0.CCMPH = level;

    // rollover the index to loop the audio
	if (AUDIO_INDEX >= sizeof(AUDIO_SAMPLES))
        AUDIO_INDEX = 0;

    // indicate the interrupt was handled
	TCA0.SINGLE.INTFLAGS = TCA_SINGLE_OVF_bm;
}
```

Enable global interrupts:

```c
sei();
```

Full source code is on GitHub:

* TinyAVR 2 series: ATTiny286 [ATTiny286 `main.c`](https://github.com/swharden/AVR-projects/blob/master/ATTiny826%20speech/main.c)

* AVR DD series: [AVR64DD32 `main.c`](https://github.com/swharden/AVR-projects/blob/master/AVR64DD32%20audio%20speech/main.c)

### Use the AVR's DAC for Audio Playback

**Modern 8-bit AVRs have a 10-bit digital-to-analog converter (DAC) built in.** It's simpler to setup and use than a discrete timer/counter in PWM mode. Although the code above uses the AVR's timer/counter B (TCB) to generate the analog waveform, this method is recommended when a DAC is available:

```c
// Enable the DAC and output on pin 16
DAC0.CTRLA = DAC_OUTEN_bm | DAC_ENABLE_bm;

// Set the DAC level
uint8_t level = 123; // Retrieved from memory
DAC0.DATA = level << 8; // Shift to use the highest bits
```

## Playing Music from an AVR DD Series Microcontroller

**YouTube has a surprisingly large number of videos of people beeping the [Coffin Dance](https://www.youtube.com/watch?v=j9V78UbdzWI) song from an Arduino,** so here's my video response playing the actual song audio encoded as an 8 kHz 8-bit waveform on an AVR64DD32 microcontroller. The original song is [Astronomia](https://www.youtube.com/watch?v=iLBBRuVDOo4) by Vicetone and Tony Igy. Refer to [Know Your Meme: Coffin Dance](https://knowyourmeme.com/memes/coffin-dance-dancing-pallbearers) for more information about internet culture.

<div class="text-center my-5">
    <video playsinline controls class="border border-dark bg-dark shadow" style="width: 100%">
        <source src="https://swharden.com/static/2023/08/19/music.webm" type="video/webm">
    </video>
</div>

## Additional Resources

* [NumberSpeaker Arduino Library](https://www.arduino.cc/reference/en/libraries/numberspeaker/)

* [@swharden/NumberSpeaker](https://github.com/swharden/NumberSpeaker) - Source code for this project on GitHub

* [@swharden/AVR-projects](https://github.com/swharden/AVR-projects/) - A collection of standalone projects for AVR microcontrollers (including Arduino) on GitHub. Refer to [ATTiny826 speech](https://github.com/swharden/AVR-projects/tree/master/ATTiny826%20speech) and [AVR64DD32 speech](https://github.com/swharden/AVR-projects/tree/master/AVR64DD32%20speech) folders.

* The speakers featured in this project are convenient because they come in their own small resonant cavity. I found them [on Amazon](https://www.amazon.com/gp/aw/d/B0BGWY5PM9) for about $2 each.

* [Talkie](https://www.arduino.cc/reference/en/libraries/talkie/) is an official Arduino speech synthesis library. It is a software implementation of the [Texas Instruments speech synthesis architecture](https://en.wikipedia.org/wiki/Texas_Instruments_LPC_Speech_Chips) from the late 1970s. I found the voice to be poor quality for reading numbers, but it may be useful to users seeking more complex phrases or who are concerned about demands on program memory.

* [Adding speech to your Embedded Project](https://skinnysatan.com/2014/01/30/adding-speech-to-your-embedded-project/) - A similar blog post from 2014

* [Voicemaker](https://voicemaker.in/) - A text-to-audio tool that allows several runs for free

* [wave2c](https://github.com/olleolleolle/wav2c) - A WAV file to C source converter by [Olle Jonsson](http://ollehost.dk/). There is a really interesting [web interface](https://guilhermerodrigues680.github.io/wav2c-online/) by [Guilherme Rodrigues](https://github.com/guilhermerodrigues680)

* [WAVToCode](https://colinjs.com/wavtocode/wavtocode.htm) - A WAV File to C Code Converter by [Colin Seymour](https://colinjs.com/)

* [AVR Memory](https://microchipdeveloper.com/8avr:memory) - Official documentation for AVR microcontrollers

* [Arduino Memory Guide](https://docs.arduino.cc/learn/programming/memory-guide) - Official documentation for the Arduino platform

* [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming/) - How to program modern series AVR using Atmel-ICS or MPLAB Snap UPDI programmers.

* [Migration from the megaAVR to AVR Dx Microcontroller Families](https://ww1.microchip.com/downloads/en/Appnotes/Migration-from-megaAVR-to-AVR-DxMCU-Fam-DS00003731A.pdf) - Microchip application note

* This article was featured in the official Arduino blog: [Arduino speaks without any special hardware](https://blog.arduino.cc/2023/08/24/arduino-speaks-without-any-special-hardware/)