---
title: Circuits vs. Software
date: 2009-01-15 17:47:52
tags: ["diyECG", "old", "python"]
---

# Circuits vs. Software

> **⚠️ Check out my newer ECG designs:** 
* [**Sound Card ECG with AD8232**](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)
* [**Single op-amp ECG**](https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/)

__Would I rather design circuits or software?__ I'm a software guy (or at least I know more about software than circuits) so I'd rather record noisy signals and write software to eliminate the noise, rather than assembling circuits to eliminate the noise in hardware. In the case of my DIY ECG machine, I'd say I've done a surprisingly good job of eliminating noise using software. Most DIY ECG circuits on the net use multiple op-amps and filters to do this. Instead of all that fancy stuff, I made a crude circuit (a single op-amp and two resisters) that is capable of record my ECG and filtered it in software. The output is pretty good!

__The first step in removing noise is understanding it.__ Most of the noise in my signal came from sine waves caused by my electrodes picking up radiated signals in the room. Since this type of interference is consistent through the entire recording, power-spectral analysis could be applied to determine the frequencies of the noise so I could selectively block them out. I used the [fast Fourier transform algorithm (FFT)](http://en.wikipedia.org/wiki/Fft) on the values to generate a plot of the spectral components of my signal (mostly noise) seen as sharp peaks. I manually band-stopped certain regions of the spectrum that I thought were noise-related (colored bands). This is possible to do electronically with a more complicated circuit, but is interesting to do in software. I think performed an inverse FFT on the trace. The result was a trace with greatly reduced noise. After a moving window smoothing algorithm was applied the signal was even better! Note that I recorded the WAV file with "sound recorder" (not GoldWave) and did all of the processing (including band-pass filtering) within Python.

<div class="text-center">

[![](https://swharden.com/static/2009/01/15/diy_ecg4_thumb.jpg)](https://swharden.com/static/2009/01/15/diy_ecg4.png)

</div>

__The ECG came out better than expected!__ The graph above shows the power spectral analysis with band-stop filters applied at the colored regions. Below is the trace of the original signal (light gray), the inverse-FFT-filtered trace (dark gray), and the smoothed filtered trace (black) - the final ECG signal I intend to use.

<div class="text-center">

[![](https://swharden.com/static/2009/01/15/diy_ecg3_thumb.jpg)](https://swharden.com/static/2009/01/15/diy_ecg3.png)

</div>

__This is a magnified view of a few heartbeats__. It looks pretty good! Here's the code I used to do all the calculations:

```python
import wave, struct, numpy, pylab, scipy

fname='./success3.wav'

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
    #return small[40000:50000]
    return small

def normalize(data):
    """make all data fit between -.5 and +.5"""
    data=data-numpy.average(data)
    big=float(max(data))
    sml=float(min(data))
    data=data/abs(big-sml)
    data=data+float(abs(min(data)))-.47
    return data

def smooth(data,deg=20,expand=False):
    """moving window average (deg = window size)."""
    for i in range(len(data)-deg):
        if i==0: cur,smooth=sum(data[0:deg]),[]
        smooth.append(cur/deg)
        cur=cur-data[i]+data[i+deg]
    if expand:
        for i in range(deg):
            smooth.append(smooth[-1])
    return smooth

def smoothListGaussian(list,degree=10,expand=False):
    window=degree*2-1
    weight=numpy.array([1.0]*window)
    weightGauss=[]
    for i in range(window):
        i=i-degree+1
        frac=i/float(window)
        gauss=1/(numpy.exp((4*(frac))**2))
        weightGauss.append(gauss)
    weight=numpy.array(weightGauss)*weight
    smoothed=[0.0]*(len(list)-window)
    for i in range(len(smoothed)):
        smoothed[i]=sum(numpy.array(list[i:i+window])*weight)/sum(weight)
    if expand:
        for i in range((degree*2)-1):
            smoothed.append(smoothed[-1])
    return smoothed

def goodSmooth(data):
    #data=smooth(fix,20,True)
    data=smooth(fix,100,True)
    #data=smooth(fix,20,True)
    return data

def makeabs(data):
    """center linear data to its average value."""
    for i in range(len(data)): data[i]=abs(data[i])
    return data

def invert(data):
    """obviously."""
    for i in range(len(data)): data[i]=-data[i]
    return data

def loadwav(fname):
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

def bandStop(fft,fftx,low,high,show=True):
    lbl="%d-%d"%(low,high)
    print "band-stopping:",lbl
    if show:
        col=pylab.cm.spectral(low/1200.)
        pylab.axvspan(low,high,alpha=.4,ec='none',label=lbl,fc=col)
        #pylab.axvspan(-low,-high,fc='r',alpha=.3)
    for i in range(len(fft)):
        if abs(fftx[i])&gt;low and abs(fftx[i])&lt;high :
            fft[i]=0
    return fft

def getXs(data):
    xs=numpy.array(range(len(data)))
    xs=xs*(1.0/rate)
    return xs

def clip(x,deg=1000):
    return numpy.array(x[deg:-deg])

pylab.figure(figsize=(12,8))
raw = invert(shrink(readwave(fname),10))
xs = getXs(raw)
fftr = numpy.fft.fft(raw)
fft = fftr[:]
fftx= numpy.fft.fftfreq(len(raw), d=(1.0/(rate)))

pylab.subplot(2,1,1)
pylab.plot(fftx,abs(fftr),'k')

fft=bandStop(fft,fftx,30,123)
fft=bandStop(fft,fftx,160,184)
fft=bandStop(fft,fftx,294,303)
fft=bandStop(fft,fftx,386,423)
fft=bandStop(fft,fftx,534,539)
fft=bandStop(fft,fftx,585,610)
fft=bandStop(fft,fftx,654,660)
fft=bandStop(fft,fftx,773,778)
fft=bandStop(fft,fftx,893,900)
fft=bandStop(fft,fftx,1100,max(fftx))
pylab.axis([0,1200,0,2*10**6])
pylab.legend()
pylab.title("Power Spectral Analysis",fontsize=28)
pylab.ylabel("Power",fontsize=20)
pylab.xlabel("Frequency (Hz)",fontsize=20)

pylab.subplot(2,1,2)
pylab.title("Original Trace",fontsize=28)
pylab.ylabel("Potential",fontsize=20)
pylab.xlabel("Time (sec)",fontsize=20)
pylab.plot(clip(xs),clip(raw),color='.8',label='1: raw')

fix = scipy.ifft(fft)
pylab.plot(clip(xs),clip(fix)+5000,color='.6',label='2: band-stop')
pylab.plot(clip(xs),clip(goodSmooth(fix))-5000,'k',label='3: smoothed')
pylab.legend()
pylab.title("Band-Stop Filtered Trace",fontsize=28)
pylab.ylabel("Potential",fontsize=20)
pylab.xlabel("Time (sec)",fontsize=20)

pylab.subplots_adjust(hspace=.5)
pylab.savefig('out.png',dpi=100)
pylab.show()
print "COMPLETE"
```