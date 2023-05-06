---
title: DIY ECG Machine On The Cheap
date: 2009-08-14 21:15:00
tags: ["diyECG", "old"]
---

# DIY ECG Machine On The Cheap

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

## Background

__You've probably seen somebody in a hospital hooked up to a bunch of wires used to analyze their heartbeat.__ The machine that visualizes heartbeat is called an [electrocardiograph, or ECG](http://en.wikipedia.org/wiki/Electrocardiography). It amplifies, measures, and records the natural electrical potential created by the heart. Note that cardiac electrical signals are different than [heart sounds](http://en.wikipedia.org/wiki/Heart_sounds), which are listened to with a [stethoscope](http://en.wikipedia.org/wiki/Stethoscope). The intrinsic cardiac pacemaker system is responsible for generating these electrical signals which serve to command and coordinate contraction of the four chambers at the heart at the appropriate intervals: atria (upper chambers) first, then the ventricles (lower chambers) a fraction of a second later. Analysis of these signals reveals a wealth of information about cardiac regulation, as well insights into pathological conditions.

<div class="text-center img-small">

[![](ecgman_thumb.jpg)](ecgman.png)
![](ecg_principle_slow.gif)

</div>

__Each heartbeat produces a little squiggle with unique properties.__ The squiggle is called the PQRST wave. The smooth curve in the ECG (P) is caused by the stimulation of the atria via the [Sinoatrial (SA) node](http://en.wikipedia.org/wiki/Sinoatrial_node) in the right atrium. There is a brief pause, as the electrical impulse is slowed by the [Atrioventricular (AV) node](http://en.wikipedia.org/wiki/Atrioventricular_node) and [Purkinje fibers](http://en.wikipedia.org/wiki/Purkinje_fibers) in the [bundle of His](http://en.wikipedia.org/wiki/Bundle_of_His). The prominent spike in the ECG (the _QRS complex_) is caused by this step, where the electrical impulse travels through the inter-ventricular septum and up through the outer walls of the ventricles. The sharp peak is the _R_ component, and exact heart rate can be calculated as the inverse of the R-to-R interval (RRi).

<blockquote class="wp-block-quote"><p><strong>WARNING:</strong> This page documents how I made a simple ECG machine with a minimum of parts to view the electrical activity of my own heart. Feel free to repeat my experiment, but do so at your own risk. </p></blockquote>

## Project Goal

The goal of this project is to generate an extremely cheap, functional ECG machine made from common parts, most of which can be found around your house. This do-it-yourself (DIY) ECG project is different than many others on the internet in that it greatly simplifies the circuitry by eliminating noise reduction components, accomplishing this via software-based data post-processing. Additionally, this writeup is intended for those without any computer, electrical, or biomedical experience, and should be far less convoluted than the suspiciously-cryptic write-ups currently available online. In short, I want to give everybody the power to visualize and analyze their own heartbeat!

## My ECG:

<div class="text-center">

[![](ecg31_thumb.jpg)](ecg31.png)

</div>

## Videos

#### ECG Introduction

![](https://www.youtube.com/embed/6-zNMup_pgk)

#### Recording my ECG

![](https://www.youtube.com/embed/izet7cgtMjU)

#### Video 3/3: Analyzing my ECG

![](https://www.youtube.com/embed/Q4y20Lu3rn0)

## ECG Theory

__Measurement:__ The electrical signals which command cardiac musculature can be detected on the surface of the skin. In theory one could grab the two leads of a standard volt meter, one with each hand, and see the voltage change as their heart beats, but the fluctuations are rapid and by the time these signals reach the skin they are extremely weak (a few millionths of a volt) and difficult to detect with simple devices. Therefore, amplification is needed.

__Amplification:__ A simple way to amplify the electrical difference between two points is to use a [operational amplifier](http://en.wikipedia.org/wiki/Operational_amplifier), otherwise known as an op-amp. The gain (multiplication factor) of an op-amp is controlled by varying the resistors attached to it, and an op-amp with a gain of 1000 will take a 1 millivolt signal and amplify it to 1 volt. There are many different types of microchip op-amps, and they're often packaged with multiple op-amps in one chip (such as the quad-op-amp [lm324](http://www.mcu.hk/GIF/LM324.gif), or the dual-op-amp [lm358n](http://www4.zero.ad.jp/electronics/stdata/lm358/LM358N.gif)). Any op-amp designed for low voltage will do for our purposes, and we only need one.

__Noise:__ Unfortunately, the heart is not the only source of voltage on the skin. Radiation from a variety of things (computers, cell phones, lights, and especially the wiring in your walls) is absorbed by your skin and is measured with your ECG, in many cases masking your ECG in a sea of electrical noise. The traditional method of eliminating this noise is to use complicated analog circuitry, but since this noise has a characteristic, repeating, high-frequency wave pattern, it can be separated from the ECG (which is much slower in comparison) using digital signal processing computer software!

__Digitization:__ Once amplified, the ECG signal along with a bunch of noise is in analog form. You could display the output with an [oscilloscope](http://en.wikipedia.org/wiki/Oscilloscope), but to load it into your PC you need an analog-to-digital converter. Don't worry! If you've got a sound card with a microphone input, you've already got one! It's just that easy. We'll simply wire the output of our ECG circuit to the input of our sound card, record the output of the op-amp using standard sound recording software, remove the noise from the ECG digitally, and output gorgeous ECG traces ready for visualization and analysis!

## Parts/Cost

I'll be upfront and say that I spent $0.00 making my ECG machine, because I was able to salvage all the parts I needed from a pile of old circuit boards. If you need specific components, check your local RadioShack. If that's a no-go, hit-up [Digikey](http://www.DigiKey.com) (it's probably cheaper too). Also, resistor values are flexible. Use mine as a good starter set, and vary them to suit your needs. If you buy everything from [Digikey](www.DigiKey.com), the total cost of this project would be about $1. For now, here's a list of all the parts you need:

*   1x low voltage op-amp [LM358N](http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&name=LM358NFS-ND) $0.40
*   1x 100kOhm resistor (brn,blk,yel) virtually free
*   1x 1kOhm resistor (brn,blk,red) virtually free
*   1x 0.1uF capacitor (104Z) virtually free
*   Microphone cable to get from the op-amp to your PC
*   Electrodes [3 pennies](http://www.ustreas.gov/) should do. ($0.03)

## Making the Device

__Keep in mind that I'm not an electrical engineer__ (I have a masters in molecular biology but I'm currently a dental student if you must know) and I'm only reporting what worked well for _me_. I don't claim this is perfect, and I'm certainly open for (and welcome) suggestions for improvement. With that in mind, here's what I did!

<div class="text-center img-border">

[![](img_2694_thumb.jpg)](img_2694.jpg)

</div>

__This is pretty much it.__ First off is a power source. If you want to be safe, use three AAA batteries in series. If you're a daredevil and enjoy showing off your ghettorigging skills, do what I did and grab 5v from a free USB plug! Mua ha ha ha. The power goes into the circuit and so do the leads/electrodes connected to the body. You can get pretty good results with only two leads, but if you want to experiment try hooking up an extra ground lead and slap it on your foot. More on the electrodes later. The signal from the leads is amplified by the circuit and put out the headphone cable, ready to enter your PC's sound card through the microphone jack!

<div class="text-center img-border">

[![](img_2686_thumb.jpg)](img_2686.jpg)

</div>

__Note how I left room in the center of the circuit board.__ That was intentional! I wanted to expand this project by adding a microcontroller to do some on-board, real-time analysis. Specifically, an [ATMega8](http://thinklabs.in/shop/images/mega8.jpg)! I never got around to it though. Its purpose would be to analyze the output of the op-amp and graph the ECG on a LCD screen, or at least measure the time between beats and display HR on a screen. (More ideas are at the bottom of this document.) Anyway, too much work for now, maybe I'll do it one day in the future.

## ECG circuit diagram:

<div class="text-center">

[![](simple_ecg_circuit_thumb.jpg)](simple_ecg_circuit.png)

</div>

__This is the circuit diagram.__ This is a classical high-gain analog differential amplifier. It just outputs the multiplied difference of the inputs. The 0.1uF capacitor helps stabilize the signal and reduce high frequency noise (such as the audio produced by a nearby AM radio station). Use Google if you're interested in learning exactly how it works.

## ECG schematic:

<div class="text-center">

[![](simple_ecg_circuit2_thumb.jpg)](simple_ecg_circuit2.png)

</div>

__This is how I used my LM358N__ to create the circuit above. Note that there is a small difference in my board from the photos and this diagram. This diagram is correct, but the circuit in some of the pictures is not. Briefly, when I built it I accidentally connected the (-) lead directly to ground, rather than to the appropriate pin on the microchip. This required me to place a 220kOhm between the leads to stabilize the signal. I imagine if you wire it CORRECTLY (as shown in these circuit diagrams) it will work fine, but if you find it too finicky (jumping quickly from too loud to too quiet), try tossing in a high-impedance resistor between the leads like I did. Overall, this circuit is extremely flexible and I encourage you to build it on a breadboard and try different things. Use this diagram as a starting point and experiment yourself!

## The Electrodes:

<div class="text-center img-border">

[![](img_2704_thumb.jpg)](img_2704.jpg)

</div>

__You can make electrodes out of anything conductive.__ The most recent graphs were created from wires with gator clips on them clamping onto pennies (pictured). Yeah, I know I could solder directly to the pennies (they're copper) but gator clips are fast, easy, and can be clipped to different materials (such as aluminum foil) for testing. A dot of moisturizing lotion applied to the pennies can be used to improve conduction between the pennies and the skin, but I didn't find this to be very helpful. If pressed firmly on the body, conduction seems to be fine. Oh! I just remembered. __USE ELECTRICAL TAPE TO ATTACH LEADS TO YOUR BODY!__ I tried a million different things, from rubber bands to packaging tape. The bottom line is that electrical tape is stretchy enough to be flexible, sticky enough not to fall off (even when moistened by the natural oils/sweat on your skin), and doesn't hurt that bad to peel off.

<div class="text-center img-border">

![](diy_ecg7.jpg)

</div>

__Some of the best electrodes__ I used were made from aluminum cans! Rinse-out a soda can, cut it into "pads", and use the sharp edge of a razor blade or pair of scissors to _scrape off the wax coating on all contact surfaces_. Although a little unconformable and prone to cut skin due to their sharp edges, these little guys work great!

## Hooking it Up

__This part is the most difficult part of the project!__ This circuit is extremely finicky. The best way to get it right is to open your sound editor (In Windows I use [GoldWave](http://www.goldwave.com/) because it's simple, powerful, and free, but similar tools exist for Linux and other Unix-based OSes) and view the low-frequency bars in live mode while you set up. When neither electrode is touched, it should be relatively quiet. When only the + electrode is touched, it should go crazy with noise. When you touch both (one with each hand) the noise should start to go away, possibly varying by how much you squeeze (how good of a connection you have). The whole setup process is a game between too much and too little conduction. You'll find that somewhere in the middle, you'll see (and maybe hear) a low-frequency burst of noise once a second corresponding to your heartbeat. \[note: Did you know that's how the second was invented? I believe it was \] Once you get that good heartbeat, tape up your electrodes and start recording. __If you can't get it no matter what you do, start by putting the ground electrode in your mouth (yeah, I said it) and pressing the + electrode firmly and steadily on your chest. If that works (it almost always does), you know what to look for, so keep trying on your skin.__ For short recordings (maybe just a few beats) the mouth/chest method works _beautifully_, and requires far less noise reduction (if any), but is simply impractical for long-term recordings. I inside vs. outside potential is less susceptible to noise-causing electrical radiation. Perhaps other orifices would function similarly? I'll leave it at that. I've also found that adding a third electrode (another ground) somewhere else on my body helps a little, but not significantly. Don't give up at this step if you don't get it right away! If you hear noise when + is touched, your circuit is working. Keep trying and you'll get it eventually.

## Recording the ECG

__This is the easy part.__ Keep an eye on your "bars" display in the audio program to make sure something you're doing (typing, clicking, etc) isn't messing up the recording. If you want, try surfing the net or playing computer games to see how your heart varies. Make sure that as you tap the keyboard and click the mouse, you're not getting noise back into your system. If this is a problem, try powering your device by batteries (a good idea for safety's sake anyway) rather than another power source (such as USB power). Record as long as you want! Save the file as a standard, mono, wave file.

## Digitally Eliminating Noise

__Now it's time to clean-up the trace.__ Using GoldWave, first apply a lowpass filter at 30 Hz. This kills most of your electrical noise (> 30hz), while leaving the ECG intact (< 15Hz). However, it dramatically decreases the volume (potential) of the audio file. Increase the volume as necessary to maximize the window with the ECG signal. You should see clear heartbeats at this point. You may want to apply an auto-gain filter to normalize the heartbeats potentials. Save the file as a raw sound file (.snd) at 1000 Hz (1 kHz) resolution.

## Presentation and Analysis

__Now you're ready to analyze!__ Plop your .snd file in the same folder as my \[[ecg.py script](http://www.SWHarden.com/blog/images/ecg.py)\], edit the end of the script to reflect your .snd filename, and run the script by double-clicking it. (Keep in mind that my script was written for [python 2.5.4](http://www.python.org/download/releases/2.5.4/) and requires [numpy 1.3.0rc2 for python 2.5](http://sourceforge.net/projects/numpy/files/NumPy/), and [matplotlib 0.99 for python 2.5](http://sourceforge.net/projects/matplotlib/files/) - make sure you get the versions right!) Here's what you'll see!

<div class="text-center">

[![](diy_ecg_sample_trace_thumb.jpg)](diy_ecg_sample_trace.png)

</div>

__This is a small region of the ECG trace.__ The "R" peak is most obvious, but the details of the other peaks are not as visible. If you want more definition in the trace (such as the blue one at the top of the page), consider applying a small collection of customized band-stop filters to the audio file rather than a single, sweeping lowpass filter. Refer to [earlier posts in the DIY ECG category](http://www.swharden.com/blog/category/diy-ecg-home-made-electrocardiogram/) for details. Specifically, code on [Circuits vs. Software for noise reduction](http://www.swharden.com/blog/2009-01-15-circuits-vs-software/) entry can help. For our purposes, calculating heart rate from R-to-R intervals (RRIs) can be done accurately with traces such as this.

<div class="text-center">

[![](diy_ecg_heart_rate_over_time_thumb.jpg)](diy_ecg_heart_rate_over_time.png)

</div>

__Your heart rate fluctuates a lot over time!__ By plotting the inverse of your RRIs, you can see your heart rate as a function of time. Investigate what makes it go up, go down, and how much. You'd be surprised by what you find. I found that checking my email raises my heart rate more than first-person-shooter video games. I get incredibly anxious when I check my mail these days, because I fear bad news from my new university (who knows why, I just get nervous about it). I wonder if accurate RRIs could be used to assess nervousness for the purposes of lie detection?

<div class="text-center">

[![](diy_ecg_rr_beat_interval_thumb.jpg)](diy_ecg_rr_beat_interval.png)

</div>

__This is the RRI plot__ where the value of each RRI (in milliseconds) is represented for each beat. It's basically the inverse of heart rate. Miscalculated heartbeats would show up as extremely high or extremely low dots on this graph. However, excluding points above or below certain bounds means that if your heart did double-beat, or skip a beat, you wouldn't see it. Note that I just realized my axis label is wrong (it should be sec, not ms).

<div class="text-center">

[![](diy_ecg_poincare_plot_thumb.jpg)](diy_ecg_poincare_plot.png)

</div>

__A [Poincare Plot](http://en.wikipedia.org/wiki/Poincar%C3%A9_plot)__ is a commonly-used method to visually assess heart rate variability as a function of RRIs. In this plot, each RRI is plotted against the RRI of the next subsequent beat. In a heart which beats at the same speed continuously, only a single dot would be visible in the center. In a heart which beats mostly-continuously, and only changes its rate very slowly, a linear line of dots would be visible in a 1:1 ratio. However, in real life the heart varies RRIs greatly from beat to beat, producing a small cloud of dots. The size of the cloud corresponds to the speed at which the autonomic nervous system can modulate heart rate in the time frame of a single beat.

<div class="text-center">

[![](diy_ecg_rr_deviation_histogram_thumb.jpg)](diy_ecg_rr_deviation_histogram.png)

</div>

__The frequency of occurrence__ of various RRIs can be expressed by a histogram. The center peak corresponds to the standard heart rate. Peaks to the right and left of the center peak correspond to increased and decreased RRIs, respectively. A gross oversimplification of the interpretation of such data would be to state that the upper peak represents the cardio-inhibitory parasympathetic autonomic nervous system component, and the lower peak represents the cardio-stimulatory sympathetic autonomic nervous system component.

<div class="text-center">

[![](diy_ecg_power_spectrum_raw_thumb.jpg)](diy_ecg_power_spectrum_raw.png)

</div>

__Taking the [Fast Fourier Transformation](http://en.wikipedia.org/wiki/Fast_Fourier_transform) of the data__ produces a unique trace whose significance is extremely difficult to interpret. Near 0Hz (infinite time) the trace heads toward ∞ (infinite power). To simplify the graph and eliminate the near-infinite, low-frequency peak we will normalize the trace by multiplying each data point by its frequency, and dividing the vertical axis units by Hz to compensate. This will produce the following graph...

<div class="text-center">

[![](diy_ecg_power_spectrum_weighted_thumb.jpg)](diy_ecg_power_spectrum_weighted.png)

</div>

__This is the power spectrum density (PSD) plot__ of the ECG data we recorded. Its physiological interpretation is extraordinarily difficult to understand and confirm, and is the subject of great debate in the field of autonomic neurological cardiac regulation. An oversimplified explanation of the significance of this graph is that the parasympathetic (cardio-inhibitory) branch of the autonomic nervous system works faster than the sympathetic (cardio-stimulatory) branch. Therefore, the lower peak corresponds to the sympathetic component (combined with persistent parasympathetic input, it's complicated), while the higher-frequency peak corresponds to the parasympathetic component, and the sympathetic/parasympathetic relationship can be assessed by the ratio of the integrated areas of these peaks after a complicated [curve fitting](http://en.wikipedia.org/wiki/Curve_fitting) processes which completely separates overlapping peaks. To learn more about power spectral analysis of heart rate over time in the frequency domain, I recommend skimming [this introduction to heart rate variability website](http://www.macses.ucsf.edu/Research/Allostatic/notebook/heart.rate.html) and the article on [Heart Rate Variability following Myocardial Infarction](http://www.swharden.com/blog/wp-admin/post.php?action=edit&post=1512) (heart attack). Also, National Institute of Health (NIH) funded studies on HRV should be available from [pubmed.org](http://www.ncbi.nlm.nih.gov/pubmed/). If you want your head to explode, read [Frequency-Domain Characteristics and Filtering of Blood Flow Following the Onset of Exercise: Implications for Kinetics Analysis](http://jap.physiology.org/cgi/reprint/100/3/817.pdf) for a lot of good frequency-domain-analysis-related discussion and rationalization.

## Encouraging Words:

__Please, if you try this don't die.__ The last thing I want is to have some kid calling me up and yelling at me that he nearly electrocuted himself when he tried to plug my device directly into a wall socket and now has to spend the rest of his life with two Abraham Lincolns tattooed onto his chest resembling a second set of nipples. Please, if you try this use common sense, and of course you're responsible for your own actions. I provide this information as a description of what I did and what worked for me. If you make something similar that works, I've love to see it! Send in your pictures of your circuit, charts of your traces, improved code, or whatever you want and I'll feature it on the site. __GOOD LUCK!__

## More Complex Circuit:

<div class="text-center">

[![](diy_ecg_circuit_thumb.jpg)](diy_ecg_circuit.png)

</div>

__If you want to try this, go for it!__ Briefly, this circuit uses 6 op-amps to help eliminate effects of noise. It's also safer, because of the diodes interconnecting the electrodes. It's the same circuit as on \[[this page](http://www.eng.utah.edu/~jnguyen/ecg/ecg_index.html)\].

## Last minute thoughts:

*   More homemade ECG information can be found on my [earlier posts in the DIY ECG category](http://www.swharden.com/blog/category/diy-ecg-home-made-electrocardiogram/), however this page is the primary location of my most recent thoughts and ideas.
*   You can use moisturizing lotion between the electrodes and your skin to increase conduction. However, keep in mind that _better conduction is not always what you want_. You'll have to experiment for yourself.
*   Variation in location of electrodes will vary the shape of the ECG. I usually place electrodes on each side of my chest near my arms. If your ECG appears upside-down, reverse the leads!
*   Adding extra leads can improve grounding. Try grounding one of your feet with a third lead to improve your signal. Also, if you're powering your device via USB power consider trying battery power - it should be less noisy.
*   While recording, be aware of what you do! I found that if I'm not well-grounded, my ECG is fine as long as I don't touch my keyboard. If I start typing, every keypress shows up as a giant spike, bigger than my heartbeat!
*   If you get reliable results, I wonder if you could make the device portable? Try using a portable tape recorder, voice recorder, or maybe even minidisc recorder to record the output of the ECG machine for an entire day. I haven't tried it, but why wouldn't it work? If you want to get fancy, have a [microcontroller](http://www.swharden.com/blog/category/microcontrollers/) handle the signal processing and determine RRIs (should be easy) and save this data to a [SD card](http://www.instructables.com/id/Cheap-DIY-SD-card-breadboard-socket/) or [fancy flash logger](http://www.4dsystems.com.au/prod.php?id=22).
*   The microcontroller could output heart rate [via the serial port](http://www.swharden.com/blog/2009-05-14-simple-case-avrpc-serial-communication-via-max232/).
*   If you have a microcontroller on board, why not [display heart rate on a character LCD?](http://www.swharden.com/blog/2009-05-17-attiny2313-controlling-a-hd44780-lcd-via-avr-gcc/)
*   While you have a LCD on there, display the ECG _graphically_!
*   Perhaps a wireless implementation would be useful.
*   Like, I said, there are other, more complicated analog circuits which reduce noise of the outputted signal. I actually built [Jason Nguyen's fancy circuit](http://www.eng.utah.edu/~jnguyen/ecg/ecg_index.html) which [used 6 op-amps](http://www.eng.utah.edu/~jnguyen/ecg/bigsch.gif) but the result wasn't much better than the simple, 1 op-amp circuit I describe here once digital filtering was applied.
*   Arrhythmic heartbeats (where your heart screws-up and misfires, skips a beat, double-beats, or beats awkwardly) are physiological (normal) and surprisingly common. Although shocking to hear about, sparse, single arrhythmic heartbeats are normal and are a completely different ball game than chronic, potentially deadly heart arrhythmias in which every beat is messed-up. If you're in tune with your body, you might actually _feel_ these occurrences happening. About three times a week I feel my heart screw up a beat (often when it's quiet), and it feels like a sinking feeling in my chest. I was told by a doctor that it's totally normal and happens many times every day without me noticing, and that most people _never_ notice these single arrhythmic beats. I thought it was my heart skipping a beat, but I wasn't sure. That was my motivation behind building this device - I wanted to _see_ what my arrhythmic beats looked like. It turns out that it's more of a double-beat than a skipped beat, as observed when I [captured a single arrhythmic heartbeat](http://www.swharden.com/blog/images/murm2.png) with my ECG machine, as described in [this entry](http://www.swharden.com/blog/2009-01-20-653-diy-ecg-detected-an-irregular-heartbeat/).
*   You can improve the safety of this device by attaching diodes between leads, similar to [the more complicated circuit](http://www.swharden.com/blog/images/diy_ecg_circuit.png). Theory is that if a huge surge of energy _does_ for whatever reason get into the ECG circuit, it'll short itself out at the circuit level (conducting through the diodes) rather than at your body (across your chest / through your heart).
*   Alternatively, use an AC [opto-isolator](http://en.wikipedia.org/wiki/Opto-isolator) between the PC sound card and the ECG circuit to eliminate the possibility of significant current coming back from the PC.
*   On the [Hackaday post](http://hackaday.com/2009/08/22/collect-and-analyze-ecg-data/), [Flemming Frandsen](http://dren.dk/) noted that an improperly grounded PC could be dangerous because the stored charge would be manifest in the ground of the microphone jack. If you were to ground yourself to true ground (using a bench power supply or sticking your finger in the ground socket of an AC wall plug) this energy could travel through _you_! So be careful to only ground yourself with respect to the circuit using only battery power to minimize this risk.
*   Do not attempt anything on this page. Ever. Don't even read it. You read it already! You're sill reading it aren't you? Yeah. You don't follow directions well do you?

## SAMPLE FILTERED RECORDING:

I think this is the same one I used in the 3rd video from my single op-amp circuit. \[[scottecg.snd](http://www.SWHarden.com/blog/images/scottecg.snd)\] It's about an hour long, and in raw sound format (1000 Hz). It's already been filtered (low-pass filtered at 30Hz). You can use it with my code below!

## CODE

```python
print "importing libraries..."
import numpy, pylab
print "DONE"

class ECG:

    def trim(self, data,degree=100):
        print 'trimming'
        i,data2=0,[]
        while i<len(data):
            data2.append(sum(data[i:i+degree])/degree)
            i+=degree
        return data2

    def smooth(self,list,degree=15):
        mults=[1]
        s=[]
        for i in range(degree): mults.append(mults[-1]+1)
        for i in range(degree): mults.append(mults[-1]-1)
        for i in range(len(list)-len(mults)):
            small=list[i:i+len(mults)]
            for j in range(len(small)):
                small[j]=small[j]*mults[j]
            val=sum(small)/sum(mults)
            s.append(val)
        return s

    def smoothWindow(self,list,degree=10):
        list2=[]
        for i in range(len(list)):
            list2.append(sum(list[i:i+degree])/float(degree))
        return list2

    def invertYs(self):
        print 'inverting'
        self.ys=self.ys*-1

    def takeDeriv(self,dist=5):
        print 'taking derivative'
        self.dys=[]
        for i in range(dist,len(self.ys)):
            self.dys.append(self.ys[i]-self.ys[i-dist])
        self.dxs=self.xs[0:len(self.dys)]

    def genXs(self, length, hz):
        print 'generating Xs'
        step = 1.0/(hz)
        xs=[]
        for i in range(length): xs.append(step*i)
        return xs

    def loadFile(self, fname, startAt=None, length=None, hz=1000):
        print 'loading',fname
        self.ys = numpy.memmap(fname, dtype='h', mode='r')*-1
        print 'read %d points.'%len(self.ys)
        self.xs = self.genXs(len(self.ys),hz)
        if startAt and length:
            self.ys=self.ys[startAt:startAt+length]
            self.xs=self.xs[startAt:startAt+length]

    def findBeats(self):
        print 'finding beats'
        self.bx,self.by=[],[]
        for i in range(100,len(self.ys)-100):
          if self.ys[i]<15000: continue # SET THIS VISUALLY
          if self.ys[i]<self.ys[i+1] or self.ys[i]<self.ys[i-1]: continue
          if self.ys[i]-self.ys[i-100]>5000 and self.ys[i]-self.ys[i+100]>5000:
              self.bx.append(self.xs[i])
              self.by.append(self.ys[i])
        print "found %d beats"%(len(self.bx))

    def genRRIs(self,fromText=False):
        print 'generating RRIs'
        self.rris=[]
        if fromText: mult=1
        else: 1000.0
        for i in range(1,len(self.bx)):
            rri=(self.bx[i]-self.bx[i-1])*mult
            #if fromText==False and len(self.rris)>1:
                #if abs(rri-self.rris[-1])>rri/2.0: continue
            #print i, "%.03ft%.03ft%.2f"%(bx[i],rri,60.0/rri)
            self.rris.append(rri)

    def removeOutliers(self):
        beatT=[]
        beatRRI=[]
        beatBPM=[]
        for i in range(1,len(self.rris)):
            #CHANGE THIS AS NEEDED
            if self.rris[i]<0.5 or self.rris[i]>1.1: continue
            if abs(self.rris[i]-self.rris[i-1])>self.rris[i-1]/5: continue
            beatT.append(self.bx[i])
            beatRRI.append(self.rris[i])
        self.bx=beatT
        self.rris=beatRRI

    def graphTrace(self):
        pylab.plot(self.xs,self.ys)
        #pylab.plot(self.xs[100000:100000+4000],self.ys[100000:100000+4000])
        pylab.title("Electrocardiograph")
        pylab.xlabel("Time (seconds)")
        pylab.ylabel("Potential (au)")

    def graphDeriv(self):
        pylab.plot(self.dxs,self.dys)
        pylab.xlabel("Time (seconds)")
        pylab.ylabel("d/dt Potential (au)")

    def graphBeats(self):
        pylab.plot(self.bx,self.by,'.')

    def graphRRIs(self):
        pylab.plot(self.bx,self.rris,'.')
        pylab.title("Beat Intervals")
        pylab.xlabel("Beat Number")
        pylab.ylabel("RRI (ms)")

    def graphHRs(self):
        #HR TREND
        hrs=(60.0/numpy.array(self.rris)).tolist()
        bxs=(numpy.array(self.bx[0:len(hrs)])/60.0).tolist()
        pylab.plot(bxs,hrs,'g',alpha=.2)
        hrs=self.smooth(hrs,10)
        bxs=bxs[10:len(hrs)+10]
        pylab.plot(bxs,hrs,'b')
        pylab.title("Heart Rate")
        pylab.xlabel("Time (minutes)")
        pylab.ylabel("HR (bpm)")

    def graphPoincare(self):
        #POINCARE PLOT
        pylab.plot(self.rris[1:],self.rris[:-1],"b.",alpha=.5)
        pylab.title("Poincare Plot")
        pylab.ylabel("RRI[i] (sec)")
        pylab.xlabel("RRI[i+1] (sec)")

    def graphFFT(self):
        #PSD ANALYSIS
        fft=numpy.fft.fft(numpy.array(self.rris)*1000.0)
        fftx=numpy.fft.fftfreq(len(self.rris),d=1)
        fftx,fft=fftx[1:len(fftx)/2],abs(fft[1:len(fft)/2])
        fft=self.smoothWindow(fft,15)
        pylab.plot(fftx[2:],fft[2:])
        pylab.title("Raw Power Sprectrum")
        pylab.ylabel("Power (ms^2)")
        pylab.xlabel("Frequency (Hz)")

    def graphFFT2(self):
        #PSD ANALYSIS
        fft=numpy.fft.fft(numpy.array(self.rris)*1000.0)
        fftx=numpy.fft.fftfreq(len(self.rris),d=1)
        fftx,fft=fftx[1:len(fftx)/2],abs(fft[1:len(fft)/2])
        fft=self.smoothWindow(fft,15)
        for i in range(len(fft)):
            fft[i]=fft[i]*fftx[i]
        pylab.plot(fftx[2:],fft[2:])
        pylab.title("Power Sprectrum Density")
        pylab.ylabel("Power (ms^2)/Hz")
        pylab.xlabel("Frequency (Hz)")

    def graphHisto(self):
        pylab.hist(self.rris,bins=20,ec='none')
        pylab.title("RRI Deviation Histogram")
        pylab.ylabel("Frequency (count)")
        pylab.xlabel("RRI (ms)")
        #pdf, bins, patches = pylab.hist(self.rris,bins=100,alpha=0)
        #pylab.plot(bins[1:],pdf,'g.')
        #y=self.smooth(list(pdf[1:]),10)
        #x=bins[10:len(y)+10]
        #pylab.plot(x,y)

    def saveBeats(self,fname):
        print "writing to",fname
        numpy.save(fname,[numpy.array(self.bx)])
        print "COMPLETE"

    def loadBeats(self,fname):
        print "loading data from",fname
        self.bx=numpy.load(fname)[0]
        print "loadded",len(self.bx),"beats"
        self.genRRIs(True)

def snd2txt(fname):
    ## SND TO TXT ##
    a=ECG()
    a.loadFile(fname)#,100000,4000)
    a.invertYs()
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphTrace()
    a.findBeats()
    a.graphBeats()
    a.saveBeats(fname)
    pylab.show()

def txt2graphs(fname):
    ## GRAPH TXT ##
    a=ECG()
    a.loadBeats(fname+'.npy')
    a.removeOutliers()
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphHRs();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Heart_Rate_Over_Time.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphFFT();pylab.subplots_adjust(left=.13,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Power_Spectrum_Raw.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphFFT2();pylab.subplots_adjust(left=.13,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Power_Spectrum_Weighted.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphPoincare();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_Poincare_Plot.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphRRIs();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_RR_Beat_Interval.png");
    pylab.figure(figsize=(7,4),dpi=100);pylab.grid(alpha=.2)
    a.graphHisto();pylab.subplots_adjust(left=.1,bottom=.12,right=.96)
    pylab.savefig("DIY_ECG_RR_Deviation_Histogram.png");
    pylab.show();

fname='publish_05_10min.snd' #CHANGE THIS AS NEEDED
#raw_input("npress ENTER to analyze %s..."%(fname))
snd2txt(fname)
#raw_input("npress ENTER to graph %s.npy..."%(fname))
txt2graphs(fname)
```