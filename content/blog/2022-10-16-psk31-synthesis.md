---
title: Experiments in PSK-31 Synthesis
description: How to encode and decode PSK-31 messages using C#
Date: 2022-10-16 23:26:00
tags: ["amateur radio", "csharp"]
featured_image: https://swharden.com/static/2022/10/16/modulation.png
---



**PSK-31 is a narrow-bandwidth digital mode which encodes text as an audio tone that varies phase at a known rate.** To learn more about this digital mode and solve a challenging programming problem, I'm going to write a PSK-31 encoder and decoder from scratch using the C# programming language. All code created for this project is open-source, available from my [PSK Experiments GitHub Repository](https://github.com/swharden/psk-experiments), and released under the permissive MIT license. This page documents my progress and notes things I learn along the way.

<a href="https://swharden.com/static/2022/10/16/psk-waterfall2.jpg"><img src="https://swharden.com/static/2022/10/16/psk-waterfall2.jpg"></a>

## Encoding Bits as Phase Shifts

<!--
<img src="https://swharden.com/static/2022/10/16/bpsk.png" class="w-75 d-block mx-auto my-3">
-->

* PSK31 messages have a continuous carrier tone

* Symbols are represented by "symbols", each 1/31.25 seconds long

* If a symbol changes phase from its previous symbol it is a `0`, otherwise it is a `1`

<a href="https://swharden.com/static/2022/10/16/theory.png"><img src="https://swharden.com/static/2022/10/16/theory.png" class="d-block mx-auto"></a>

## Amplitude Modulation Silences Phase Transitions

Although a continuous phase-shifting tone of constant amplitude can successfully transmit PSK31 data, the abrupt phase transitions will cause splatter. If you transmit this you will be heard, but those trying to communicate using adjacent frequencies will be highly disappointed.

<div class="text-center">

Hard phase transitions (splatter) | Soft phase transitions (cleaner)
---|---
<img src="https://swharden.com/static/2022/10/16/splatter.png">|<img src="https://swharden.com/static/2022/10/16/no-splatter.png">

</div>

To reduce spectral artifacts that result from abruptly changing phase, phase transitions are silenced by shaping the waveform envelope as a sine wave so it is silent at the transition. This way the maximum rate of phase shifts is a sine wave with a period of half the baud rate. This is why the opening of a PSK31 message (a series of logical `0` bits) sounds like two tones: It's the carrier sine wave with an envelope shaped like a sine wave with a period of 31.25/2 Hz. These two tones separated by approximately 15 Hz are visible in the spectrogram (waterfall).

![](https://swharden.com/static/2022/10/16/modulation.png)

## Encoding Text as Bits

**Unlike ASCII (8 bits per character) and RTTY (5 bits per character), BPSK uses [Varicode](https://en.wikipedia.org/wiki/Varicode) (1-10 bits per character) to encode text.** Consecutive zeros `00` separate characters, so character codes must not contain `00` and they must start ane end with a `1` bit. Messages are flanked by a preamble (repeated `0` bits) and a postamble (repeated `1` bits).

<table cellpadding=30 style="white-space: nowrap; font-size: .8em;" class="m-0 p-0 mx-auto"><tr><td valign=top>
<TT>NUL 1010101011</TT>
<BR><TT>SOH 1011011011</TT>
<BR><TT>STX 1011101101</TT>
<BR><TT>ETX 1101110111</TT>
<BR><TT>EOT 1011101011</TT>
<BR><TT>ENQ 1101011111</TT>
<BR><TT>ACK 1011101111</TT>
<BR><TT>BEL 1011111101</TT>
<BR><TT>BS&nbsp; 1011111111</TT>
<BR><TT>HT&nbsp; 11101111</TT>
<BR><TT>LF&nbsp; 11101</TT>
<BR><TT>VT&nbsp; 1101101111</TT>
<BR><TT>FF&nbsp; 1011011101</TT>
<BR><TT>CR&nbsp; 11111</TT>
<BR><TT>SO&nbsp; 1101110101</TT>
<BR><TT>SI&nbsp; 1110101011</TT>
<BR><TT>DLE 1011110111</TT>
<BR><TT>DC1 1011110101</TT>
<BR><TT>DC2 1110101101</TT>
<BR><TT>DC3 1110101111</TT>
<BR><TT>DC4 1101011011</TT>
<BR><TT>NAK 1101101011</TT>
<BR><TT>SYN 1101101101</TT>
<BR><TT>ETB 1101010111</TT>
<BR><TT>CAN 1101111011</TT>
<BR><TT>EM&nbsp; 1101111101</TT>
<BR><TT>SUB 1110110111</TT>
<BR><TT>ESC 1101010101</TT>
<BR><TT>FS&nbsp; 1101011101</TT>
<BR><TT>GS&nbsp; 1110111011</TT>
<BR><TT>RS&nbsp; 1011111011</TT>
<BR><TT>US&nbsp; 1101111111</TT>
<BR><TT>SP&nbsp; 1</TT>
<BR><TT>!&nbsp;&nbsp; 111111111</TT>
<BR><TT>"&nbsp;&nbsp; 101011111</TT>
<BR><TT>#&nbsp;&nbsp; 111110101</TT>
<BR><TT>$&nbsp;&nbsp; 111011011</TT>
<BR><TT>%&nbsp;&nbsp; 1011010101</TT>
<BR><TT>&amp;&nbsp;&nbsp; 1010111011</TT>
<BR><TT>'&nbsp;&nbsp; 101111111</TT>
<BR><TT>(&nbsp;&nbsp; 11111011</TT>
<BR><TT>)&nbsp;&nbsp; 11110111</TT>
<BR><TT>*&nbsp;&nbsp; 101101111</TT>
</td><td valign=top width="33%" >
<TT>+&nbsp;&nbsp; 111011111</TT>
<BR><TT>,&nbsp;&nbsp; 1110101</TT>
<BR><TT>-&nbsp;&nbsp; 110101</TT>
<BR><TT>.&nbsp;&nbsp; 1010111</TT>
<BR><TT>/&nbsp;&nbsp; 110101111</TT>
<BR><TT>0&nbsp;&nbsp; 10110111</TT>
<BR><TT>1&nbsp;&nbsp; 10111101</TT>
<BR><TT>2&nbsp;&nbsp; 11101101</TT>
<BR><TT>3&nbsp;&nbsp; 11111111</TT>
<BR><TT>4&nbsp;&nbsp; 101110111</TT>
<BR><TT>5&nbsp;&nbsp; 101011011</TT>
<BR><TT>6&nbsp;&nbsp; 101101011</TT>
<BR><TT>7&nbsp;&nbsp; 110101101</TT>
<BR><TT>8&nbsp;&nbsp; 110101011</TT>
<BR><TT>9&nbsp;&nbsp; 110110111</TT>
<BR><TT>:&nbsp;&nbsp; 11110101</TT>
<BR><TT>;&nbsp;&nbsp; 110111101</TT>
<BR><TT>&lt;&nbsp;&nbsp; 111101101</TT>
<BR><TT>=&nbsp;&nbsp; 1010101</TT>
<BR><TT>>&nbsp;&nbsp; 111010111</TT>
<BR><TT>?&nbsp;&nbsp; 1010101111</TT>
<BR><TT>@&nbsp;&nbsp; 1010111101</TT>
<BR><TT>A&nbsp;&nbsp; 1111101</TT>
<BR><TT>B&nbsp;&nbsp; 11101011</TT>
<BR><TT>C&nbsp;&nbsp; 10101101</TT>
<BR><TT>D&nbsp;&nbsp; 10110101</TT>
<BR><TT>E&nbsp;&nbsp; 1110111</TT>
<BR><TT>F&nbsp;&nbsp; 11011011</TT>
<BR><TT>G&nbsp;&nbsp; 11111101</TT>
<BR><TT>H&nbsp;&nbsp; 101010101</TT>
<BR><TT>I&nbsp;&nbsp; 1111111</TT>
<BR><TT>J&nbsp;&nbsp; 111111101</TT>
<BR><TT>K&nbsp;&nbsp; 101111101</TT>
<BR><TT>L&nbsp;&nbsp; 11010111</TT>
<BR><TT>M&nbsp;&nbsp; 10111011</TT>
<BR><TT>N&nbsp;&nbsp; 11011101</TT>
<BR><TT>O&nbsp;&nbsp; 10101011</TT>
<BR><TT>P&nbsp;&nbsp; 11010101</TT>
<BR><TT>Q&nbsp;&nbsp; 111011101</TT>
<BR><TT>R&nbsp;&nbsp; 10101111</TT>
<BR><TT>S&nbsp;&nbsp; 1101111</TT>
<BR><TT>T&nbsp;&nbsp; 1101101</TT>
<BR><TT>U&nbsp;&nbsp; 101010111</TT>
</td><td valign=top width="33%" >
<TT>V&nbsp;&nbsp; 110110101</TT>
<BR><TT>X&nbsp;&nbsp; 101011101</TT>
<BR><TT>Y&nbsp;&nbsp; 101110101</TT>
<BR><TT>Z&nbsp;&nbsp; 101111011</TT>
<BR><TT>[&nbsp;&nbsp; 1010101101</TT>
<BR><TT>\&nbsp;&nbsp; 111110111</TT>
<BR><TT>]&nbsp;&nbsp; 111101111</TT>
<BR><TT>^&nbsp;&nbsp; 111111011</TT>
<BR><TT>_&nbsp;&nbsp; 1010111111</TT>
<BR><TT>.&nbsp;&nbsp; 101101101</TT>
<BR><TT>/&nbsp;&nbsp; 1011011111</TT>
<BR><TT>a&nbsp;&nbsp; 1011</TT>
<BR><TT>b&nbsp;&nbsp; 1011111</TT>
<BR><TT>c&nbsp;&nbsp; 101111</TT>
<BR><TT>d&nbsp;&nbsp; 101101</TT>
<BR><TT>e&nbsp;&nbsp; 11</TT>
<BR><TT>f&nbsp;&nbsp; 111101</TT>
<BR><TT>g&nbsp;&nbsp; 1011011</TT>
<BR><TT>h&nbsp;&nbsp; 101011</TT>
<BR><TT>i&nbsp;&nbsp; 1101</TT>
<BR><TT>j&nbsp;&nbsp; 111101011</TT>
<BR><TT>k&nbsp;&nbsp; 10111111</TT>
<BR><TT>l&nbsp;&nbsp; 11011</TT>
<BR><TT>m&nbsp;&nbsp; 111011</TT>
<BR><TT>n&nbsp;&nbsp; 1111</TT>
<BR><TT>o&nbsp;&nbsp; 111</TT>
<BR><TT>p&nbsp;&nbsp; 111111</TT>
<BR><TT>q&nbsp;&nbsp; 110111111</TT>
<BR><TT>r&nbsp;&nbsp; 10101</TT>
<BR><TT>s&nbsp;&nbsp; 10111</TT>
<BR><TT>t&nbsp;&nbsp; 101</TT>
<BR><TT>u&nbsp;&nbsp; 110111</TT>
<BR><TT>v&nbsp;&nbsp; 1111011</TT>
<BR><TT>w&nbsp;&nbsp; 1101011</TT>
<BR><TT>x&nbsp;&nbsp; 11011111</TT>
<BR><TT>y&nbsp;&nbsp; 1011101</TT>
<BR><TT>z&nbsp;&nbsp; 111010101</TT>
<BR><TT>{&nbsp;&nbsp; 1010110111</TT>
<BR><TT>|&nbsp;&nbsp; 110111011</TT>
<BR><TT>}&nbsp;&nbsp; 1010110101</TT>
<BR><TT>~&nbsp;&nbsp; 1011010111</TT>
<BR><TT>DEL 1110110101</TT>
</td></tr></table>

## How to Generate a PSK Waveform

Now that we've covered the major steps of PSK31 message composition and modulation, let's go through the steps ot generate a PSK31 message in code.

### Step 1: Convert a Message to Varicode

Here's the gist of how I store my varicode table in code. Note that the `struct` has an additional `Description` field which is useful for decoding and debugging.

```cs
public struct VaricodeSymbol
{
    public readonly string Symbol;
    public string BitString;
    public int[] Bits;
    public readonly string Description;

    public VaricodeSymbol(string symbol, string bitString, string? description = null)
    {
        Symbol = symbol;
        BitString = bitString;
        Bits = bitString.ToCharArray().Select(x => x == '1' ? 1 : 0).ToArray();
        Description = description ?? string.Empty;
    }
}
```

```cs
static VaricodeSymbol[] GetAllSymbols() => new VaricodeSymbol[]
{
    new("NUL", "1010101011", "Null character"),
    new("LF", "11101", "Line feed"),
    new("CR", "11111", "Carriage return"),
    new("SP", "1", "Space"),
    new("a", "1011"),
    new("b", "1011111"),
    new("c", "101111"),
    // etc...
};
```

I won't show how I do the message-to-varicode lookup, but it's trivial. Here's the final function I use to generate Varicode bits from a string:

```cs
static int[] GetVaricodeBits(string message)
{
    List<int> bits = new();

    // add a preamble of repeated zeros
    for (int i=0; i<20; i++)
        bits.Add(0);

    // encode each character of a message
    foreach (char character in message)
    {
        VaricodeSymbol symbol = Lookup(character);
        bits.AddRange(symbol.Bits);
        bits.AddRange(CharacterSeparator);
    }

    // add a postamble of repeated ones
    for (int i=0; i<20; i++)
        bits.Add(1);

    return bits.ToArray();
}
```

### Step 2: Determine Phase Shifts

Now that we have our Varicode bits, we need to generate an array to indicate phase transitions. A transition occurs every time a bit changes value form the previous bit. This code returns phase as an array of `double` given the bits from a Varicode message.

```cs
public static double[] GetPhaseShifts(int[] bits, double phase1 = 0, double phase2 = Math.PI)
{
    double[] phases = new double[bits.Length];
    for (int i = 0; i < bits.Length; i++)
    {
        double previousPhase = i > 0 ? phases[i - 1] : phase1;
        double oppositePhase = previousPhase == phase1 ? phase2 : phase1;
        phases[i] = bits[i] == 1 ? previousPhase : oppositePhase;
    }
    return phases;
}
```

### Step 3: Generate the Waveform

These constants will be used to define the shape of the waveform:

```cs
public const int SampleRate = 8000;
public const double Frequency = 1000;
public const double BaudRate = 31.25;
```

This minimal code generates a decipherable PSK-31 message, but it does not silence the phase transitions so it produces a lot of splatter. This function must be refined to shape the waveform such that phase transitions are silenced.

```cs
public double[] GetWaveformBPSK(double[] phases)
{
    int totalSamples = (int)(phases.Length * SampleRate / BaudRate);
    double[] wave = new double[totalSamples];
    for (int i = 0; i < wave.Length; i++)
    {
        double time = (double)i / SampleRate;
        int frame = (int)(time * BaudRate);
        double phaseShift = phases[frame];
        wave[i] = Math.Cos(2 * Math.PI * Frequency * time + phaseShift);
    }
    return wave;
}
```

### Step 4: Generate the Waveform with Amplitude Modulation

This is the same function as above, but with extra logic for amplitude-modulating the waveform in the shape of a sine wave to silence phase transitions.

```cs
public double[] GetWaveformBPSK(double[] phases)
{
    int baudSamples = (int)(SampleRate / BaudRate);
    double samplesPerBit = SampleRate / BaudRate;
    int totalSamples = (int)(phases.Length * SampleRate / BaudRate);
    double[] wave = new double[totalSamples];

    // create the amplitude envelope sized for a single bit
    double[] envelope = new double[(int)samplesPerBit];
    for (int i = 0; i < envelope.Length; i++)
        envelope[i] = Math.Sin((i + .5) * Math.PI / envelope.Length);

    for (int i = 0; i < wave.Length; i++)
    {
        // phase modulated carrier
        double time = (double)i / SampleRate;
        int frame = (int)(time * BaudRate);
        double phaseShift = phases[frame];
        wave[i] = Math.Cos(2 * Math.PI * Frequency * time + phaseShift);

        // envelope at phase transitions
        int firstSample = (int)(frame * SampleRate / BaudRate);
        int distanceFromFrameStart = i - firstSample;
        int distanceFromFrameEnd = baudSamples - distanceFromFrameStart + 1;
        bool isFirstHalfOfFrame = distanceFromFrameStart < distanceFromFrameEnd;
        bool samePhaseAsLast = frame == 0 ? false : phases[frame - 1] == phases[frame];
        bool samePhaseAsNext = frame == phases.Length - 1 ? false : phases[frame + 1] == phases[frame];
        bool rampUp = isFirstHalfOfFrame && !samePhaseAsLast;
        bool rampDown = !isFirstHalfOfFrame && !samePhaseAsNext;

        if (rampUp)
            wave[i] *= envelope[distanceFromFrameStart];

        if (rampDown)
            wave[i] *= envelope[distanceFromFrameEnd];
    }

    return wave;
}
```

## PSK31 Encoder Program

I wrapped the functionality above in a Windows Forms GUI that allows the user to type a message, specify frequency, baud rate, and whether or not to refine the envelope to reduce splatter, then either play or save the result. An interactive [ScottPlot Chart](https://scottplot.net) allows the user to inspect the waveform.

* **Download PSK31 Encoder: [PSK31-encoder.zip](https://swharden.com/static/2022/10/16/PSK31-encoder.zip)**

* **PSK31 Encoder Source Code: [PSK Experiments on GitHub](https://github.com/swharden/psk-experiments)**

![](https://swharden.com/static/2022/10/16/screenshot.png)

## Sample PSK-31 Transmissions

These audio files encode the text _The Quick Brown Fox Jumped Over The Lazy Dog 1234567890 Times!_ in 1kHz BPSK at various baud rates.

* PSK-31: [dog31.wav](https://swharden.com/static/2022/10/16/dog31.wav)
* PSK-63: [dog63.wav](https://swharden.com/static/2022/10/16/dog63.wav)
* PSK-125: [dog125.wav](https://swharden.com/static/2022/10/16/dog125.wav)
* PSK-256: [dog256.wav](https://swharden.com/static/2022/10/16/dog250.wav)

### Non-Standard Baud Rates

**Let's see what PSK-3 sounds like.** This mode encodes data at a rate of 3 bits per second. Note that Varicode characters may require up to ten bits, so this is pretty slow. On the other hand the side tones are closer to the carrier and the total bandwidth is much smaller. The message here has been shortened to just my callsign, AJ4VD.

* PSK-3: [psk3.wav](https://swharden.com/static/2022/10/16/psk3.wav)

## Encode PSK-31 In Your Browser

After implementing the C# encoder described above I created a JavaScript version (as per <a href="https://en.wikipedia.org/wiki/Jeff_Atwood">Atwood's Law</a>).

* Try it on your phone or computer! [**Launch PskJS**](https://swharden.com/static/2022/10/16/pskjs)

<a href="https://swharden.com/static/2022/10/16/pskjs"><img src="https://swharden.com/static/2022/10/16/pskjs.png" class="d-block mx-auto my-3"></a>

## Decoding PSK-31

Considering all the steps for _encoding_ PSK-31 transmissions are already described on this page, it doesn't require too much additional effort to create a _decoder_ using basic software techniques. Once symbol phases are detected it's easy to work backwards: detect phase transitions (logical 0s) or repeats (logical 1s), treat consecutive zeros as a character separator, then look-up characters according to the Varicode table. The tricky bit is analyzing the source audio to generate the array of phase offsets.

The simplest way to decode PSK-31 transmissions leans on the fact that we already know the baud rate: 31.25 symbols per second, or one symbol every 256 samples at 8kHz sample rate. The audio signal can be segregated into many 256-sample bins, and processed by FFT. Once the center frequency is determined, the FFT power at this frequency can be calculated for each bin. Signal offset can be adjusted to minimize the imaginary component of the FFTs at the carrier frequency, then the real component will be strongly positive or negative, allowing phase transitions to be easily detected.

<div class="row">
	<div class="col">
		<a href="https://swharden.com/static/2022/10/16/psk31-receiver.html"><img src="https://swharden.com/static/2022/10/16/py-fft.png" class="img-fluid"></a>
	</div>
	<div class="col">
		<a href="https://swharden.com/static/2022/10/16/psk31-receiver.html"><img src="https://swharden.com/static/2022/10/16/py-iq.png" class="img-fluid"></a>
	</div>
	<div class="col">
		<a href="https://swharden.com/static/2022/10/16/psk31-receiver.html"><img src="https://swharden.com/static/2022/10/16/py-eyediagram.png" class="img-fluid"></a>
	</div>
</div>

There are more advanced techniques to improve BPSK decoding, such as continuously adjusting frequency and phase alignment (synchronization). A [Costas loop](https://en.wikipedia.org/wiki/Costas_loop) can help lock onto the carrier frequency while preserving its phase. Visit [**Simple BPSK31 Decoding with Python**](https://swharden.com/static/2022/10/16/psk31-receiver.html) for an excellent demonstration of how to decode BPSK31 using these advanced techniques.

A crude C# implementation of a BPSK decoded is available on GitHub in the [PSK Experiments](https://github.com/swharden/psk-experiments) repository

![](https://swharden.com/static/2022/10/16/psk-decode.png)

## Encoding PSK-31 in Hardware

Since BPSK is just a carrier that applies periodic 180º phase-shifts, it's easy to generate in hardware by directly modulating the signal source. A good example of this is [KA7OEI's PSK31 transmitter](http://www.ka7oei.com/psk_bm_tx.html) which feeds the output of an oscillator through an even or odd number of NAND gates (from a [74HC00](https://www.mouser.com/datasheet/2/308/74HC00-105628.pdf)) to produce two signals of opposite phase.

![](https://swharden.com/static/2022/10/16/pic-psk31.png)

## Quadrature Phase Shift Keying (QPSK)

**Unlike the 0º and 180º phases of binary phase shift keying (BPSK), quadrature phase shift keying (QPSK) encodes extra data into each symbol by uses a larger number of phases.** When QPSK-31 is used in amateur radio these extra bits aren't used to send messages faster but instead send them more reliably using convolutional coding and error correction. These additional features come at a cost (an extra 3 dB SNR is required), and in practice QPSK is not used as much by amateur radio operators.

QPSK encoding/decoding and convolutional encoding/decoding are outside the scope of this page, but excellent information exists on the [Wikipedia: QPSK](https://en.wikipedia.org/wiki/Phase-shift_keying) and in the US Naval Academy's [EC314 Lesson 23: Digital Modulation](https://www.projectfpga.com/resources/EC312_Lesson_23_Digital_Modulation_Course_Notes.pdf) document.

<a href="https://swharden.com/static/2022/10/16/qpsk.png"><img src="https://swharden.com/static/2022/10/16/qpsk.png" class="mx-auto d-block"></a>

## PSK-31 in 2022

After all that, it turns out PSK-31 isn't that popular anymore. These days it seems the [FT-8 digital mode](https://en.wikipedia.org/wiki/FT8) with [WSJT-X software](https://physics.princeton.edu/pulsar/k1jt/wsjtx.html) is orders of magnitude more popular ??

## Resources

* [PSK Experiments](https://github.com/swharden/psk-experiments) (GitHub) - Source code for the project shown on this page

* Software: [digipan](https://www.apkfollow.com/articles/2020/06/digipan.net.html) - A Freeware Program for PSK31 and PSK63

* Software: [fldigi](http://www.w1hkj.com/) - Supports PSK31 and other digital modes

* Software: [WinPSK](https://www.moetronix.com/ae4jy/winpsk.htm) - open source PSK31 software for Windows

* Software: [PSKCore DLL](http://www.moetronix.com/ae4jy/pskcoredll.htm) - A Windows DLL that can be included in other software to add support for PSK31

* Software: [jacobwgillespie/psk31](https://github.com/jacobwgillespie/psk31) - Example PSK31 message generate using JavaScript

* [Digital Modulation](https://www.projectfpga.com/resources/EC312_Lesson_23_Digital_Modulation_Course_Notes.pdf) (US Naval Academy, EC314 Lesson 23) - A good description of quadrature PSK and higher order phase-shift encoding.

* [PSK-31 Specification](http://www.arrl.org/psk31-spec) (ARRL) - theory, varicode table, and convolutional code table.

* [PSK31 Description](http://aintel.bi.ehu.es/psk31.html) by G3PLX is the original / official description of the digital mode.

* [PSK31: A New Radio-Teletype Mode](http://www.arrl.org/files/file/Technology/tis/info/pdf/x9907003.pdf) (1999) by Peter Martinez, G3PLX

* [PSK31 The Easy Way](https://www.vic.wicen.org.au/wp-content/uploads/2012/05/psk31.pdf) (1999) by Alan Gibbs, VK6PG

* [Wikipedia: Varicode](https://en.wikipedia.org/wiki/Varicode) includes a table of all symbols

* [Wikipedia: QPSK](https://en.wikipedia.org/wiki/Phase-shift_keying)

* [PSK31 Fundamentals](http://aintel.bi.ehu.es/psk31theory.html) and [PSK31 Setup](https://myplace.frontier.com/~nb6z/psk31.htm) by Peter Martinez, G3PLX

* [Varicode](http://math0.wvstateu.edu/~baker/cs240/info/varicode.html) - West Virginia State University CS240

* [Introduction to PSK31](http://fweb.wallawalla.edu/class-wiki/index.php/PSK31_Demodulation) by engineering students at Walla Walla University

* [GNURadio PSK31 Decoder](https://sdradventure.wordpress.com/2011/10/15/gnuradio-psk31-decoder-part-1/) by VA7STH

* [Simple BPSK31](https://swharden.com/static/2022/10/16/psk31-receiver.html) - a fantastic Jupyter notebook demonstrating BPSK decoding with Python

* [PySDR: Digital Modulation](https://pysdr.org/content/digital_modulation.html) - a summary of signal modulation types

* [A PIC-Based PSK31 exciter using a Balanced Modulator](http://www.ka7oei.com/psk_bm_tx.html) by Clint Turner, KA7OEI
