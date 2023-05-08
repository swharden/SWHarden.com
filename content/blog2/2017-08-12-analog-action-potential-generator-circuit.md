---
title: Action Potential Generator Circuit
date: 2017-08-12 23:04:32
tags: ["science", "circuit", "microcontroller", "python"]
---

# Action Potential Generator Circuit

__Few biological cells are as interesting to the electrical engineer as the neuron. Neurons are essentially capacitors (with a dielectric cell membrane separating conductive fluid on each side) with parallel charge pumps, leak currents, and nonlinear voltage-dependent currents. __When massively parallelized, these individual functional electrical units yield complex behavior and underlie consciousness. The study of the electrical properties of neurons ([neurophysiologically](https://en.wikipedia.org/wiki/Neurophysiology), a subset of [electrophysiology](https://en.wikipedia.org/wiki/Electrophysiology)) often involves the development and use of sensitive electrical equipment aimed at studying these small potentials produced by neurons and currents which travel through channels embedded in their membranes. It seems neurophysiology has gained an emerging interest from the hacker community, as evidenced by the success of [Back Yard Brains](https://backyardbrains.com/), projects like the [OpenEEG](http://openeeg.sourceforge.net/doc/hw/), and Hack-A-Day's recent feature [_The Neuron - a Hacker's Perspective_](http://hackaday.com/2017/06/02/the-neuron-a-hackers-perspective/).

While contemplating designs for action potential detection and analysis circuitry, I realized that it would be beneficial to be able to _generate_ action-potential-like waveforms on my workbench. The circuit I came up with to do this is a fully analog (technically mixed signal) action potential generator which produces lifelike action potentials.

{{<youtube MBwQrIVJqfs>}}

__Cellular Neurophysiology for Electrical Engineers (in 2 sentences):__ Neuron action potentials (self-propagating voltage-triggered depolarizations) in individual neurons are measured in scientific environments using single cell recording tools such as [sharp microelectrodes](http://www.scholarpedia.org/article/Intracellular_recording) and [patch-clamp pipettes](https://en.wikipedia.org/wiki/Patch_clamp). Neurons typically rest around -70mV and when depolarized (typically by external excitatory input) above a threshold they engage in a self-propagating depolarization until they reach approximately +40mV, at which time a self-propagating repolarization occurs (often over-shooting the initial rest potential by several mV), then the cell slowly returns to the rest voltage so after about 50ms the neuron is prepared to fire another action potential. Impassioned budding electrophysiologists may enjoy further reading _[Active Behavior of the Cell Membrane](http://www.bem.fi/book/04/04.htm) _and [_Introduction to Computational Neuroscience_.](http://ecee.colorado.edu/~ecen4831/cnsweb/cns1.html)

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/a.gif)

</div>

__The circuit I describe here produces waveforms which visually mimic action potentials__ rather than serve to replicate the exact conductances real neurons employ to exhibit their complex behavior. It is worth noting that numerous scientists and engineers have designed more physiological electrical representations of neuronal circuitry using discrete components. In fact, the [_Hodgkin-Huxley model_](https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model) of the initiation and propagation of action potentials earned Alan Hodgkin and Andrew Huxley the Nobel Prize in Physiology and Medicine in 1936. Some resources on the internet describe how to design lifelike action potential generating circuits by mimicking the endogenous ionic conductances which underlie them, notably _[Analog and Digital Hardware Neural Models](https://people.ece.cornell.edu/land/PROJECTS/NeuralModels/)_, [_Active Cell Model_](https://courses.cit.cornell.edu/bionb442/labs/f2007/lab6.html), and [_Neuromorphic Silicon Neuron Circuits_](http://journal.frontiersin.org/article/10.3389/fnins.2011.00073/full). My goal for this project is to create waveforms which _resemble_ action potentials, rather than waveforms which truly _model_ them. I suspect it is highly unlikely I will earn a Nobel Prize for the work presented here.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/circuit_hand.jpg)

</div>

__The analog action potential simulator circuit I came up with creates a continuous series action potentials.__ This is achieved using a [555 timer](https://en.wikipedia.org/wiki/555_timer_IC) (specifically the [NE555](http://www.ti.com/lit/ds/slfs022i/slfs022i.pdf)) in an astable configuration to provide continuous square waves (about 6 Hz at about 50% duty). The rising edge of each square wave is isolated with a diode and used to charge a capacitor*. While the charge on the capacitor is above a certain voltage, an [NPN transistor](https://en.wikipedia.org/wiki/Bipolar_junction_transistor) (the [2N3904](https://www.onsemi.com/pub/Collateral/2N3903-D.PDF)) allows current to flow, amplifying this transient input current. The capacitor* discharges predictably ([as an RC circuit](https://en.wikipedia.org/wiki/RC_circuit)) through a leak resistor. A large value leak resistor slows the discharge and allows that signal's transistor to flow current for a longer duration. By having two signals (fast and slow) using RC circuits with different resistances (smaller and larger), the transistors are on for different durations (shorter and longer). By making the short pulse positive (using the NPN in [common collector configuration](https://en.wikipedia.org/wiki/Common_collector)) and the longer pulse negative (using the NPN in [common emitter configuration](https://en.wikipedia.org/wiki/Common_emitter)), a [resistor voltage divider](https://en.wikipedia.org/wiki/Voltage_divider) can be designed to scale and combine these signals into an output waveform a few hundred mV in size with a 5V power supply. Pictured below is the output of this circuit realized on a breadboard. The blue trace is the output of the 555 timer.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/scope_b.jpg)
![](https://swharden.com/static/2017/08/12/scope_a.jpg)

</div>

Between the capacitance of the rectification diode, input capacitance of the transistor, and stray parasitic capacitance from the physical construction of my wires and the rails on my breadboard, there is sufficient capacitance to accumulate charge which can be modified by changing the value of the leak resistor.


<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/breadboard.jpg)

</div>

__This circuit produces similar output when simulated.__ I'm using [LTspice](http://www.linear.com/designtools/software/) (free) to simulate this circuit. The circuit shown is identical to the one hand-drawn and built on the breadboard, with the exception that an additional 0.1 µF capacitor to ground is used on the output to smooth the signal. On the breadboard this capacitance-based low-pass filtering already exists due to the capacitive nature of the components, wires, and rails.

<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/circuit.png)
![](https://swharden.com/static/2017/08/12/sim_trace2.png)
![](https://swharden.com/static/2017/08/12/sim_trace.png)

</div>

__A few improvements naturally come to mind__ when considering this completed, functional circuit:

* **Action potential frequency:** The resistor/capacitor network on the 555 timer determines the rate of square pulses which trigger action potentials. Changing these values will cause a different rate of action potential firing, but I haven't attempted to push it too fast and suspect the result would not be stable is the capacitors are not given time to fully discharge before re-initiating subsequent action potentials.

* **Microcontroller-triggered action potentials:** Since action potentials are triggered by any 5V rising edge signal, it is trivially easy to create action potentials from microcontrollers! You could create some very complex firing patterns, or even "reactive" firing patterns which respond to inputs. 

For example, add a <a href="https://www.adafruit.com/product/439">TSL2561 I2C digital light sensor</a> and you can have a light-to-frequency action potential generator!

* **Adjusting size and shape of action potentials:** Since the waveform is the combination of two waveforms, you can really only adjust the duration (width) or amplitude (height) of each individual waveform, as well as the relative proportion of each used in creating the summation. Widths are adjusted by changing the leak resistor on the base of each transistor, or by adding additional capacitance. Amplitude and the ratio of each signal may be adjusted by changing the ratio of resistors on the output resistor divider.

* **Producing -70 mV (physiological) output:** The current output is electirically decoupled (through a series capacitor) so it can float at whatever voltage you bias it to. Therefore, it is easy to "pull" in either direction. Adding a 10k potentiometer to bias the output is an easy way to let you set the voltage. A second potentiometer gating the magnitude of the output signal will let you adjust the height of the output waveform as desired.

* **The 555 could be replaced by an inverted ramp (sawtooth):** An inverted ramp / sawtooth pattern which produces rapid 5V rising edges would drive this circuit equally well. A <a href="http://www.learningaboutelectronics.com/Articles/Ramp-generator-circuit-with-transistors.php">fully analog ramp generator circuit</a> can be realized with 3 transistors: essentially a constant current capacitor charger with a threshold-detecting PNP/NPN discharge component.

* **This action potential is not all-or-nothing:** In real life, small excitatory inputs which fail to reach the action potential threshold do not produce an action potential voltage waveform. This circuit uses 5V rising edges to produce action potential waveforms. However, feeding a 1V rising edge would produce an action potential 1/5 the size. This is not a physiological effect. However, it is unlikely (if not impossible) for many digital signal sources (i.e., common microcontrollers) to output anything other than sharp rising edge square waves of fixed voltages, so this is not a concern for my application.

* **Random action potentials:** When pondering how to create randomly timed action potentials, the issue of how to generate random numbers arises. This is surprisingly difficult, especially in embedded devices. If a microcontroller is already being used, consider <a href="http://makezine.com/projects/really-really-random-number-generator/">Make's write-up on the subject</a>, and I think personally I would go with a <a href="http://holdenc.altervista.org/avalanche/">transistor-based avalanche nosie generator</a> to create the randomness.

* **A major limitation is that irregularly spaced action potentials have slightly different amplitudes.**I found this out the next day when I created a hardware random number generator (yes, that happened) to cause it to fire regularly, missing approximately half of the action potentials. When this happens, breaks in time result in a larger subsequent action potential. There are several ways to get around this, but it's worth noting that the circuit shown here is best operated around 6 Hz with only continuous regularly-spaced action potentials.

<div class="text-center img-border img-medium">

![](https://swharden.com/static/2017/08/12/File_000-2.jpeg)

</div>

__In the video I also demonstrate how to record the output of this circuit using a high-speed (44.1 kHz) 16-bit analog-to-digital converter you already have (the microphone input of your sound card).__ I won't go into all the details here, but below is the code to read data from a WAV file and plot it as if it were a real neuron. The graph below is an _actual recording_ of the circuit described here using the microphone jack of my sound card.

```python
import numpy as np
import matplotlib.pyplot as plt
Ys = np.memmap("recording.wav", dtype='h', mode='r')[1000:40000]
Ys = np.array(Ys)/max(Ys)*150-70
Xs = np.arange(len(Ys))/44100*1000
plt.figure(figsize=(6,3))
plt.grid(alpha=.5,ls=':')
plt.plot(Xs,Ys)
plt.margins(0,.1)
plt.title("Action Potential Circuit Output")
plt.ylabel("potential (mV)")
plt.xlabel("time (ms)")
plt.tight_layout()
plt.savefig("graph.png")
#plt.show()

```

<div class="text-center img-medium">

![](https://swharden.com/static/2017/08/12/graph.png)

</div>

__Let's make some noise!__ Just to see what it would look like, I created a circuit to generate slowly drifting random noise. I found this was a non-trivial task to achieve in hardware. Most noise generation circuits create random signals on the RF scale (white noise) which when low-pass filtered rapidly approach zero. I wanted something which would slowly drift up and down on a time scale of seconds. I achieved this by creating 4-bit pseudo-random numbers with a shift register ([74HC595](https://www.sparkfun.com/datasheets/IC/SN74HC595.pdf)) clocked at a relatively slow speed (about 200 Hz) having essentially random values on its input. I used a [74HC14](https://assets.nexperia.com/documents/data-sheet/74HC_HCT14.pdf) inverting buffer (with Schmidt trigger inputs) to create the low frequency clock signal (about 200 Hz) and an extremely fast and intentionally unstable square wave (about 30 MHz) which was sampled by the shift register to generate the "random" data. The schematic illustrates these points, but note that I accidentally labeled the 74HC14 as a 74HC240. While also an inverting buffer the [74HC240](https://assets.nexperia.com/documents/data-sheet/74HC_HCT240.pdf) will not serve as a good RC oscillator buffer because it does not have Schmidt trigger inputs.

An inverting buffer created a fast and a slow clock to produce 4-bit pseudo-random numbers:
<div class="text-center img-border img-medium">

![](https://swharden.com/static/2017/08/12/File_000-5.jpeg)

</div>

reminder how an inverting buffer can act as an oscillator:
<div class="text-center">

![](https://swharden.com/static/2017/08/12/schmitt-trigger-osc.png)

</div>

the full circuit realized on the breadboard:
<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/File_004.jpeg)

</div>

output of the 4-bit pseudo-random number generator:
<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/File_001.jpeg)

</div>

4-bit output smoothed through a single-stage RC filter:
<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/File_002.jpeg)

</div>

noise combined with action potential waveforms:
<div class="text-center img-border">

![](https://swharden.com/static/2017/08/12/File_003.jpeg)

</div>

__The addition of noise was a success, from an electrical and technical sense.__ It isn't particularly physiological. Neurons would fire differently based on their resting membrane potential, and the peaks of action potential should all be about the same height regardless of the resting potential. _However_ if one were performing an electrical recording through a patch-clamp pipette in perforated patch configuration (with high resistance between the electrode and the internal of the cell), a sharp microelectrode (with high resistance due to the small size of the tip opening), or were using electrical equipment or physical equipment with amplifier limitations, one could imagine that capacitance in the recording system would overcome the rapid swings in cellular potential and result in "noisy" recordings similar to those pictured above. They're not physiological, but perhaps they're a good electrical model of what it's like trying to measure a physiological voltage in a messy and difficult to control experimental environment.

__This project was an interesting exercise in analog land,__ and is completed sufficiently to allow me to move toward my initial goal: creating advanced action potential detection and measurement circuitry. There are many tweaks which may improve this circuit, but as it is good enough for my needs I am happy to leave it right where it is. If you decide to build a similar circuit (or a vastly different circuit to serve a similar purpose), send me an email! I'd love to see what you came up with.

## UPDATE: add a microcontroller

I enhanced this project by creating a [microcontroller controlled action potential generator](https://www.swharden.com/wp/2017-08-20-microcontroller-action-potential-generator/). That article is here: <https://www.swharden.com/wp/2017-08-20-microcontroller-action-potential-generator/>