---
title: DIY ECG Progress
date: 2009-01-16 12:41:40
tags: ["diyECG"]
---



> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__Last night I finished building my DIY ECG as a prototype__ (I finally got the circuit off the breadboard and onto a plastic sheet). This is a similar circuit to the one used to record data from the last entry (resister values are now identical to the crude circuit described several posts ago). I left-in the crude band-pass filter (made by grounding my primary electrode sensor through a 0.1µF capacitor) because it seemed to help a great deal, and wasn't hard to implement. I picked up all of my parts (including the LM324 quad op-amp microchip) at RadioShack. Of note, the quad-op-amp is overkill because I'm only using one of the 4 op-amps. Theoretically I could add 3 more electrodes to this circuit (which would allow for multi-sensor recording) but this would require multiple microphone jacks, which isn't very common. I guess I could use 2 microphone jacks, and differentiate right/left channels.

<div class="text-center img-border">

![](https://swharden.com/static/2009/01/16/diy_ecg5.jpg)

</div>

__I made the prototype__ by drilling holes in a small rectangular piece of a non-conductive plastic material. I picked up a stack of these rectangular sections for a quarter at a local electrical surplus store and they're perfect for prototyping. The two green wires coming out the left side attach to a power supply (either a plugged in AC-&gt;DC transformer, 3 or 4 AA batteries, or even a 9V should work). The blue wires on the right attach to the electrodes I put on my chest. The black wires go to a headphone-jack which I plug into the microphone hole of my PC to record the signal.

<div class="text-center img-border">

![](https://swharden.com/static/2009/01/16/diy_ecg6.jpg)

</div>

__This is the back of the device__ which shows my crummy soldering. I'm a molecular biologist not an electrical engineer. The white/yellow wires correspond to the left/right channels of the microphone connector. I only use the left one (white), but attached the right channel (yellow) to the op-amp just in case I decide to add another sensor later - this is not required.

<div class="text-center img-border">

![](https://swharden.com/static/2009/01/16/diy_ecg7.jpg)

</div>

__Here's the full device:__ You can see the circuit (note its small size - easy to mount inside of a tictac box or something) with the green wires leading to a power supply, black cable being the microphone connector, and the blue wires leading to electrodes made... from... Fanta... cans...? Yes, in the spirit of rigging electronics (my specialty) I found that surprisingly nice chest electrodes can be made from aluminum soda cans! If you go this route, cut them delicately so you don't get metal shards in your skin like I did at first. Also, note that you have to firmly scrape each side of the aluminum to get the insulating waxy-plastic stuff off or it just won't work. I guess it's coated with something to prevent the soda from tasting like metal. Aluminum rapidly transfers heat and it's nearly impossible to solder leads onto these pads, so I wrapped a wire (tipped with a bead of solder) with the edge of the aluminum several times and crushed the heck out of it with pliers and it seems to stay on well and make a good connection. Also, before taping these onto your skin, it helps to put a conductive goo on it to make the connection better. I added skin moisturizer to each electrode and taped the gooey electrode directly onto my chest.

__I recorded ~20 minutes of data__ last night with this rig and it looked pretty good. I went to analyze it with Python and it kept crashing! The python script I gave you previously loads the entire wave file into an array of numbers, but with a 20 minute wave file (at over 40,000 samples a second) it is too big for memory. I wrote an updated wave loader which loads large wave files in parts which is much more efficient. It also performs the condensation method at load time. Basically, it loads 100 data points (or whatever deg is set to), averages them, and adds this value to a list. The result is a smoothed trace with a resolution of 400 Hz instead of 40 kHz. I'd test this on the wave file I recorded last night but that's on my laptop which is in the car and I've got to get back to work. Here's that function:

```python
def loadWav(fname,deg=100):
     global hz
     w=wave.open(fname)
     nchannel, width, rate, length, comptype, compname = w.getparams()
     print "[%s] rate: %d Hz frames: %d length: %.02f sec" %
           (fname, rate, length, float(length)/rate)
     hz=rate/deg
     chunks=int(length/deg)
     data=[]
     for i in range(chunks):
         if i%7777==0:
             print "processing chunk %d of %d (%0.02f%%)" %
                   (i,chunks,100.0*i/chunks)
         vals = struct.unpack("%sh" %deg,w.readframes(deg))
         data.append(sum(vals)/float(deg))
     print "complete!"
     return data
```

