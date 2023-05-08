---
title: DIY ECG Trial 1
date: 2009-01-15 00:39:45
tags: ["diyECG", "python", "obsolete"]
---

# DIY ECG Trial 1

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__I've succeeded in building my own electrocardiograph (ECG) to record the electrical activity of my own heart!__ Briefly, I built a micropotential amplifier using an op-amp and attached it to makeshift electrodes on my chest (pennies and shampoo), fed the amplified signal into my sound card, and recorded it as a WAV. The signal is very noisy though. I was able to do a great job at removing this noise using band/frequency filters in GoldWave (audio editing software designed to handle WAV files). I band-blocked 50-70 Hz (which removed the oscillations from the 60 Hz AC lines running around my apartment). I then wrote the Python code (at the bottom of this entry) to load this WAV file as a single list of numbers (voltage potentials). I performed a data condensation algorithm (converting 100 points of raw WAV data into a single, averaged point, lessening my processing load by 100x), followed by two consecutive moving window averages (20-point window, performed on the condensed data). The result was a voltage reading that had most of the noise removed and a beautiful ECG signal emerged! I also tossed in some code to determine the peak of the R wave, label it (yellow dot), and use the inverse R-R time distance to calculate heart rate.

<div class="text-center">

![](https://swharden.com/static/2009/01/15/diy_ecg2.png)

</div>

__This is my actual ECC signal__ as record by a circuit similar to the one in the previous entry, recorded through my sound card, and processed with the Python script below. You can start to see the Q, R, S, and T components. I can't wait to solder-up a prototype (it's currently breadboarded) and try to analyze hours of data rather than just a few seconds. I'll take pictures of this device soon.

<div class="text-center">

![](https://swharden.com/static/2009/01/15/diy_ecg1.png)

</div>

__And here's the code I used:__ note that it relies on the WAV file I recorded. This code has extra functions not required to produce the image above, but I left them in in case they may be useful.

```python
import wave, struct, numpy, pylab, scipy

def readwave(wavfilename):
    """load raw data directly from a WAV file."""
    global rate
    w=wave.open(wavfilename,'rb')
    (nchannel, width, rate, length, comptype, compname) = w.getparams()
    print "[%s] %d HZ (%0.2fsec)" %(wavfilename, rate, length/float(rate))
    frames = w.readframes(length)
    return numpy.array(struct.unpack("%sh" %length*nchannel,frames))

def shrink(data,deg=100):
    """condense a linear data array by a multiple of [deg]."""
    global rate
    small=[]
    print "starting with", len(data)
    for i in range(len(data)/deg):
        small.append(numpy.average(data[i*deg:(i+1)*deg]))
    print "ending with", len(small)
    rate = rate/deg
    return small

def normalize(data):
    """make all data fit between -.5 and +.5"""
    data=data-numpy.average(data)
    big=float(max(data))
    sml=float(min(data))
    data=data/abs(big-sml)
    data=data+float(abs(min(data)))-.47
    return data

def smooth(data,deg=20):
    """moving window average (deg = window size)."""
    for i in range(len(data)-deg):
        if i==0: cur,smooth=sum(data[0:deg]),[]
        smooth.append(cur/deg)
        cur=cur-data[i]+data[i+deg]
    return smooth

def makeabs(data):
    """center linear data to its average value."""
    for i in range(len(data)): data[i]=abs(data[i])
    return data

def invert(data):
    """obviously."""
    for i in range(len(data)): data[i]=-data[i]
    return data

def loadwav(fname='./wavs/bandpassed.wav'):
    """a do-everything function to get usable, smoothed data from a WAV."""
    wav=readwave(fname)
    wav=shrink(wav)
    wav=invert(wav)
    wav=smooth(wav)
    wav=smooth(wav,10)
    wav=normalize(wav)
    Xs=getXs(wav)
    return Xs,wav

def getXs(datalen):
    """calculate time positions based on WAV frequency resolution."""
    Xs=[]
    for i in range(len(datalen)):
        Xs.append(i*(1/float(rate)))
    print len(datalen), len(Xs)
    return Xs

def integrate(data):
    """integrate the function with respect to its order."""
    inte=[]
    for i in range(len(data)-1):
        inte.append(abs(data[i]-data[i+1]))
    inte.append(inte[-1])
    return inte

def getPoints(Xs,data,res=10):
    """return X,Y coordinates of R peaks and calculate R-R based heartrate."""
    pXs,pYs,pHRs=[],[],[]
    for i in range(res,len(data)-res):
        if data[i]&gt;data[i-res]+.1 and data[i]&gt;data[i+res]+.1:
            if data[i]&gt;data[i-1] and data[i]&gt;data[i+1]:
                pXs.append(Xs[i])
                pYs.append(data[i])
                if len(pXs)&gt;1:
                    pHRs.append((1.0/(pXs[-1]-pXs[-2]))*60.0)
    pHRs.append(pHRs[-1])
    return pXs,pYs,pHRs

Xs,Ys=loadwav()
px,py,pHR=getPoints(Xs,Ys)

pylab.figure(figsize=(12,6))
pylab.subplot(2,1,1)
#pylab.axhline(color='.4',linestyle=':')
pylab.plot(Xs,Ys,'b-')
pylab.plot(px,py,'y.')
pylab.axis([None,None,-.6,.6])
pylab.title("DIY Electrocardiogram - Trial 1",fontsize=26)
pylab.ylabel("Normalized Potential",fontsize=16)
#pylab.xlabel("Time (sec)")
ax=pylab.axis()
pylab.subplot(2,1,2)
pylab.plot(px,pHR,'k:')
pylab.plot(px,pHR,'b.')
pylab.axis([ax[0],ax[1],None,None])
pylab.ylabel("Heart Rate (BPM)",fontsize=16)
pylab.xlabel("Time (seconds)",fontsize=16)
pylab.savefig("test.png",dpi=120)
pylab.show()
print "DONE"
```

