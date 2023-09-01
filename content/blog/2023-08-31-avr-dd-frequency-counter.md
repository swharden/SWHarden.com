---
title: Frequency Measurement with Modern AVR Microcontrollers
description: How to use the AVR64DD32's asynchronous counter to measure frequencies beyond 100 MHz
Date: 2023-08-31 18:40:00
tags: ["circuit", "microcontroller"]
---

**Modern AVR microcontrollers have asynchronous counters that can be externally driven to count pulses from 1 Hz to beyond 100 MHz.** Over the years I've explored various methods for building frequency counters typically using the [SN74LV8154 32-bit counter](https://www.ti.com/lit/ds/symlink/sn74lv8154.pdf), but my new favorite method uses the [AVR64DD32 microcontroller](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR64DD32-28-Prelim-DataSheet-DS40002315A.pdf) ($1.52 on Mouser) to directly measure a signal and report its frequency to a PC using a USB serial adapter. I'm working on a special frequency counter project which builds upon this strategy, but I found the core concept to be interesting enough that I decided to write about it in its own article. The following information is a summary of how the strategy can be achieved, but additional information and source code is [available on GitHub](https://github.com/swharden/AVR-projects/tree/master/AVR64DD32%20counter).

<a href="https://swharden.com/static/2023/08/31/small/counter-50-angle-1.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/31/small/counter-50-angle-1.jpg">
</a>

## Theory of Operation
* Count frequency on an input pin
    * Connect the signal to be measured to the `EXTCLK` pin<sup>1</sup>
    * Setup the 12-bit Timer/Counter D to asynchronously count `EXTCLK` pulses
    * Use an overflow interrupt to track total pulse count
* Gate the counter to measure the count exactly once per second
    * Setup the 16-bit Timer/Counter A to interrupt 5 times per second
    * Divide-down the 24 MHz system clock to achieve 5 Hz
    * Alternatively divide-down a 10 MHz reference on the `XTAL32K1` pin<sup>2</sup> to 5 Hz
    * On every 5th interrupt, display the measured frequency

<sup>1</sup> The [AVR64DD32 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR64DD32-28-Prelim-DataSheet-DS40002315A.pdf) suggests `EXTCLK` can be driven via `XTALHF1` pin to a maximum frequency of 32 MHz (Section 12.3.4.2.1, page 93), but [this article](https://sm6vfz.wordpress.com/2022/10/10/150-mhz-frequency-counter-with-attiny817/) by sm6vfz demonstrates this strategy produces results accurate to the single Hz up to 150 MHz.

<sup>2</sup> The [AVR64DD32 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR64DD32-28-Prelim-DataSheet-DS40002315A.pdf) says "an external digital clock can be connected to the XTAL32K1 pin" (section 26.3, page 344) but my read doesn't clearly indicate what the upper limit of the frequency is that may be clocked in. Although the `XTAL32K1` pin in combination with `XTAL32K2` are designed for a 32 kHz crystal oscillator, my read does not indicate that 32 kHz is intended to be an upper limit of what may be clocked in externally.

## Basic Setup

**Microcontroller:** The AD64DD32 8-bit AVR does not come in a DIP package, but the VQFN32 package is easy to hand solder to a QFN32/DIP breakout board. It also cannot be programmed with a ICSP programmer, but instead requires a UDPI programmer. See my [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming/) article for more information about programming these chips.

**Code:** Full source code for this project is [on GitHub](https://github.com/swharden/AVR-projects/tree/master/AVR64DD32%20counter), and the code highlights are shown at the bottom of this article.

**PC Connection:** I'm using an RS232 breakout board as a USB/serial adapter. It's `Rx` pin is connected to the microcontroller's `Tx` pin (pin 2).

**Test Signal:** I'm using a 50 MHz can oscillator as a test signal. It's been in my junk box for years and it doesn't surprise me if it has drifted a few kHz from 50 MHz. Note too that there may be some inaccuracy in the gating time base due to the imprecise nature of the AVR's 24 MHz internal oscillator.

<a href="https://swharden.com/static/2023/08/31/small/counter-50.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/31/small/counter-50.jpg">
</a>

**Serial Monitor:** I'm using RealTerm to monitor the output of the microcontroller. The code below gates the counter once per second (1 PPS) then displays the count, so the number displayed is the frequency in Hz. This value would be easy to read in a language like Python for applications requiring frequency measurement over time.

<a href="https://swharden.com/static/2023/08/31/screenshot-50b.png">
<img src="https://swharden.com/static/2023/08/31/screenshot-50b.png">
</a>

**Code:** Counting `EXTCLK` pulses with Timer/Counter D

```c
void setup_extclk_counter()
{
	// Enable the highest frequency external clock on pin 30
	CCP = CCP_IOREG_gc; // protected write
	CLKCTRL.XOSCHFCTRLA = CLKCTRL_FRQRANGE_32M_gc | CLKCTRL_SELHF_bm | CLKCTRL_ENABLE_bm;
	
	// Setup TCD to count the external clock
	TCD0.CMPBCLR = 0x0FFF; // count to max (12-bit)
	TCD0.CTRLA = TCD_CLKSEL_EXTCLK_gc; // count external clock input
	TCD0.INTCTRL = TCD_OVF_bm; // Enable overflow interrupt
	while (!(TCD0.STATUS & 0x01)); // Wait for ENRDY before enabling
	TCD0.CTRLA |= TCD_ENABLE_bm; // Enable the counter
}

// Increments the counter every time TCD0 overflows
volatile uint32_t COUNTER;
ISR(TCD0_OVF_vect)
{
	COUNTER+=4096;
	TCD0.INTFLAGS = TCD_OVF_bm;
}

volatile uint32_t COUNT_DISPLAY = 0;
volatile uint32_t COUNT_NOW = 0;
volatile uint32_t COUNT_PREVIOUS = 0;

// Call this method once per second to update the display frequency
void update_display_count()
{
    TCD0.CTRLE = TCD_SCAPTUREA_bm;
    while ((TCD0.STATUS & TCD_CMDRDY_bm) == 0); // synchronized read
    COUNT_NOW = COUNTER + TCD0.CAPTUREA;
    COUNT_DISPLAY = COUNT_NOW - COUNT_PREVIOUS;
    COUNT_PREVIOUS = COUNT_NOW;
}
```

**Code:** Gating at 1 Hz using the system clock as a time base
```c
void setup_gate_sysclk(){
	// 24 MHz clock div 256 is 93,750 ticks/second
	TCA0.SINGLE.CTRLA = TCA_SINGLE_CLKSEL_DIV256_gc | TCA_SINGLE_ENABLE_bm;
	
	// enable overflow interrupt
	TCA0.SINGLE.INTCTRL |= TCA_SINGLE_OVF_bm;
	
	// overflow 5 times per second
	TCA0.SINGLE.PER = 18750-1;
}

// this interrupt is called 5 times per second
uint8_t GATE_TICKS = 0;
ISR(TCA0_OVF_vect){
	GATE_TICKS++;
	if (GATE_TICKS == 5){
		GATE_TICKS = 0;
		update_display_count();
	}
	TCA0.SINGLE.INTFLAGS = TCA_SINGLE_OVF_bm;
}
```

**Code:** The main block runs an infinite loop and displays the frequency if an updated number is detected. Sending text to the serial port and formatting large numbers to add commas is outside the scope of this article, but see [this project's code on GitHub](https://github.com/swharden/AVR-projects/blob/master/AVR64DD32%20counter) for more information about how I did it. I did find this function helpful:

```c
void print_with_commas(unsigned long freq){
	int millions = freq / 1000000;
	freq -= millions * 1000000;
	int thousands = freq / 1000;
	freq -= thousands * 1000;
	int ones = freq;
	printf("%d,%03d,%03d\r\n", millions, thousands, ones);
}
```

## Amplify Small Signals

**Using an RF amplifier module, I was able to count radios signals using an antenna.** I found a convenient RF buffer amplifier board on Amazon based on a [TLV3501](https://www.ti.com/lit/ds/symlink/tlv3501.pdf) comparator. It is powered with 5V and has SMA connectors for RF input and TTL output, and I was able to use this device to measure frequency of various transmitters including my 144 MHz handheld VHF radio.

<a href="https://swharden.com/static/2023/08/31/small/counter-antenna-1.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/31/small/counter-antenna-1.jpg">
</a>

## Use a Prescaler to Measure Higher Frequencies

**There are many inexpensive single chip prescalers which can divide-down high frequency input to produce a waveform that slower counters can measure.** It appears there are several [RF prescaler modules on Amazon](https://www.amazon.com/s?k=prescaler+module) with SMA connectors, making them easy to pair with the preamplifier module above. Most of them seem to use a [MB506](https://www.qsl.net/n9zia/900/mb506.pdf) 2.4 GHz prescaler which is not currently available on Mouser.

<a href="https://swharden.com/static/2023/08/31/prescaler2.jpg">
<img class="w-75" src="https://swharden.com/static/2023/08/31/prescaler2.jpg">
</a>

**I'm also noticing a lot of people using the [MC12080 1.1 GHz Prescaler](https://www.mouser.com/datasheet/2/308/1/MC12080_D-2315407.pdf) for custom frequency counter designs.** It's a little over $4 on Mouser and doesn't require much supporting circuitry, although I haven't personally used this chip yet. I also found recommendations [MC12093](https://www.onsemi.com/pub/Collateral/MC12093-D.PDF). If you have experience creating a frequency counter using a prescaler, send me an email and let me know which chip you recommend and why!

## Gate with an External 10 MHz Reference

**The examples above use the AVR's system clock to generate the 1 Hz gate, but accuracy can be improved by gating based upon a 10 MHz frequency reference.** This strategy passes the 10 MHz into the `XTAL32K1` pin and counts it with the RTC counter, generating 5 hz interrupts that can trigger the gating logic.

<a href="https://swharden.com/static/2023/08/31/small/counter-10-angle-1.jpg">
<img class="border border-dark shadow" src="https://swharden.com/static/2023/08/31/small/counter-10-angle-1.jpg">
</a>

**In this example I'm measuring the 10 MHz signal** which is also responsible for the gating, so because of the chick-and-egg problem the measured frequency will always appear to be exactly 10 MHz even if the oscillator drifts. However, this strategy is useful for ensuring the software is written correctly. If the software is incorrect (e.g., the overflow period is off by one) this number will not read exactly 10 Mhz. Note also that the displayed frequency is ±1 which I presume can be attributed to variations in synchronization alignment while reading the asynchronous counter. No counts are "missed", so a deficit by 1 in one reading will self-correct as a surplus by 1 in a future reading.

<a href="https://swharden.com/static/2023/08/31/screenshot-10.png">
<img src="https://swharden.com/static/2023/08/31/screenshot-10.png">
</a>

**Code:** Gate by dividing-down an external 10 Mhz reference to 5 Hz

```c
void setup_gate_rtc(){
	// Enable the RTC
	CCP = CCP_IOREG_gc;

    // External clock on the XTAL32K1 pin, enable
	CLKCTRL.XOSC32KCTRLA = CLKCTRL_SEL_bm | CLKCTRL_ENABLE_bm;
	
	// Setup the RTC at 10 MHz to interrupt periodically
	// 10 MHz with 128 prescaler is 78,125 ticks/sec
	RTC.CTRLA = RTC_PRESCALER_DIV128_gc | RTC_RTCEN_bm;
	RTC.PER = 15624; // 5 overflows per second (78125/5-1)
	RTC.INTCTRL = RTC_OVF_bm;
	RTC.CLKSEL = RTC_CLKSEL_XTAL32K_gc; // clock in XOSC23K pin
}

// this interrupt is called 5 times per second
ISR(RTC_CNT_vect){
	/* same logic as above */
	RTC.INTFLAGS = 0x11;
}
```

## Conclusion

**The AVR64DD32 is a versatile chip with an impressive set of peripherals that is currently offered at low cost with high availability.** The asynchronous peripherals make it easy to measure frequency independent of the system clock, and in practice frequencies well into the VHF band can be directly measured with this chip. Although it isn't available in a DIP package, it's easy to experiment with on a breadboard using a QFN/DIP breakout board, and I hope more people get the opportunity to experiment with this interesting line of modern AVR microcontrollers.

## Resources

* [AVR64DD32 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR64DD32-28-Prelim-DataSheet-DS40002315A.pdf)

* [SN74LV8154 datasheet](https://www.ti.com/lit/ds/symlink/sn74lv8154.pdf) - Dual 16-Bit Binary Counters With 3-State Output Registers

* [attiny-freqcount](https://github.com/danupp/attiny-freqcount) - a GitHub project [and article](https://sm6vfz.wordpress.com/2022/10/10/150-mhz-frequency-counter-with-attiny817/) by Daniel U featured on Hackaday: [To Turn an ATTiny817 into a 150 MHz Counter, First Throw out the Spec Sheet](https://hackaday.com/2022/10/14/to-turn-an-attiny817-into-a-150mhz-counter-first-throw-out-the-spec-sheet/) that does essentially the same thing using an ATTiny instead of AVR DD series microcontroller.

* [megaTinyCore / PWM and Timer usage](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/extras/PWMandTimers.md) - fantastic notes about modern AVR microcontrollers by Spence Konde

* [AVR-Projects / AVR64DD32 counter](https://github.com/swharden/AVR-projects/tree/master/AVR64DD32%20counter) - Source code for this project on GitHub

* [Programming Modern AVR Microcontrollers](https://swharden.com/blog/2022-12-09-avr-programming/) - How to program modern AVR chips using Atmel ICE or MPLAB Snap UPDI programmers.