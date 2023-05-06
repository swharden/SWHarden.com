---
title: pySquelch - Frequency Activity Reports via Python
date: 2009-06-18 22:59:01
tags: ["amateur radio", "python", "old"]
---

# pySquelch - Frequency Activity Reports via Python

<p class="has-background has-light-green-cyan-background-color"><strong>Update:</strong> this project is now on GitHub  <a href="https://github.com/FredEckert/pySquelch">https://github.com/FredEckert/pySquelch</a> </p>

__I've been working on the pySquelch project__ which is basically a method to graph frequency usage with respect to time. The code I'm sharing below listens to the microphone jack on the sound card (hooked up to a radio) and determines when transmissions begin and end. I ran the code below for 24 hours and this is the result:

<div class="text-center img-border">

[![](https://swharden.com/static/2009/06/18/1png_thumb.jpg)](https://swharden.com/static/2009/06/18/1png.png)

</div>

__This graph represents frequency activity with respect to time. __The semi-transparent gray line represents the raw frequency usage in fractional minutes the frequency was tied-up by transmissions. The solid blue line represents the same data but smoothed by 10 minutes (in both directions) by the Gaussian smoothing method modified slightly from my [linear data smoothing with Python page](http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/).

<div class="text-center img-border">

[![](https://swharden.com/static/2009/06/18/2png_thumb.jpg)](https://swharden.com/static/2009/06/18/2png.png)

</div>

__I used the code below to generate the log, and the code further below to create the graph from the log file.__ Assuming your microphone is enabled and everything else is working, this software will require you to determine your own threshold for talking vs. no talking. Read the code and you'll figure out how test your sound card settings.

__If you want to try this yourself__ you need a Linux system (a Windows system version could be created simply by replacing _getVolEach()_ with a Windows-based audio level detection system) with Python and the alsaaudio, numpy, and matplotlib libraries. Try running the code on your own, and if it doesn't recognize a library "aptitude search" for it. Everything you need can be installed from packages in the common repository.

```python

# pySquelchLogger.py
import time
import random
import alsaaudio
import audioop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
inp.setchannels(2)
inp.setrate(1000)
inp.setformat(alsaaudio.PCM_FORMAT_S8)
inp.setperiodsize(100)
addToLog = ""
lastLogTime = 0

testLevel = False  # SET THIS TO 'True' TO TEST YOUR SOUNDCARD


def getVolEach():
    # this is a quick way to detect activity.
    # modify this function to use alternate methods of detection.
    while True:
        l, data = inp.read()  # poll the audio device
        if l > 0:
            break
    vol = audioop.max(data, 1)  # get the maximum amplitude
    if testLevel:
        print vol
    if vol > 10:
        return True  # SET THIS NUMBER TO SUIT YOUR NEEDS ###
    return False


def getVol():
    # reliably detect activity by getting 3 consistant readings.
    a, b, c = True, False, False
    while True:
        a = getVolEach()
        b = getVolEach()
        c = getVolEach()
        if a == b == c:
            if testLevel:
                print "RESULT:", a
            break
    if a == True:
        time.sleep(1)
    return a


def updateLog():
    # open the log file, append the new data, and save it again.
    global addToLog, lastLogTime
    # print "UPDATING LOG"
    if len(addToLog) > 0:
        f = open('log.txt', 'a')
        f.write(addToLog)
        f.close()
        addToLog = ""
    lastLogTime = time.mktime(time.localtime())


def findSquelch():
    # this will record a single transmission and store its data.
    global addToLog
    while True:  # loop until we hear talking
        time.sleep(.5)
        if getVol() == True:
            start = time.mktime(time.localtime())
            print start,
            break
    while True:  # loop until talking stops
        time.sleep(.1)
        if getVol() == False:
            length = time.mktime(time.localtime())-start
            print length
            break
    newLine = "%d,%d " % (start, length)
    addToLog += newLine
    if start-lastLogTime > 30:
        updateLog()  # update the log


while True:
    findSquelch()
```

__The logging code (above) produces a log file like this (below).__ The values represent the start time of each transmission (in [seconds since epoch](http://en.wikipedia.org/wiki/Unix_time)) followed by the duration of the transmission.

```
#log.txt
1245300044,5 1245300057,4 1245300063,16 1245300094,13 1245300113,4 1245300120,14 1245300195,4 1245300295,4 1245300348,4 1245300697,7 1245300924,3 1245301157,4 1245301207,12 1245301563,4 1245302104,6 1245302114,6 1245302192,3 1245302349,4 1245302820,4 1245304812,13 1245308364,10 1245308413,14 1245312008,14 1245313953,11 1245314008,6 1245314584,4 1245314641,3 1245315212,5 1245315504,6 1245315604,13 1245315852,3 1245316255,6 1245316480,5 1245316803,3 1245316839,6 1245316848,11 1245316867,5 1245316875,12 1245316893,13 1245316912,59 1245316974,12 1245316988,21 1245317011,17 1245317044,10 1245317060,6 1245317071,7 1245317098,33 1245317140,96 1245317241,15 1245317259,14 1245317277,8 1245317298,18 1245317322,103 1245317435,40 1245317488,18 1245317508,34 1245317560,92 1245317658,29 1245317697,55 1245317755,33 1245317812,5 1245317818,7 1245317841,9 1245317865,25 1245317892,79 1245317972,30 1245318007,8 1245318021,60 1245318083,28 1245318114,23 1245318140,25 1245318167,341 1245318512,154 1245318670,160 1245318834,22 1245318859,9 1245318870,162 1245319042,57 1245319102,19 1245319123,30 1245319154,18 1245319206,5 1245319214,13 1245319229,6 1245319238,6 1245319331,9 1245319341,50 1245319397,71 1245319470,25 1245319497,40 1245319540,8 1245319551,77 1245319629,4 1245319638,36 1245319677,158 1245319837,25 1245319865,40 1245319907,33 1245319948,92 1245320043,26 1245320100,9 1245320111,34 1245320146,8 1245320159,6 1245320167,8 1245320181,12 1245320195,15 1245320212,14 1245320238,18 1245320263,46 1245320310,9 1245320326,22 1245320352,27 1245320381,15 1245320398,24 1245320425,57 1245320483,16 1245320501,40 1245320543,43 1245320589,65 1245320657,63 1245320722,129 1245320853,33 1245320889,50 1245320940,1485 1245322801,7 1245322809,103 1245322923,5 1245322929,66 1245323553,4 1245324203,15 1245324383,5 1245324570,7 1245324835,4 1245325200,8 1245325463,5 1245326414,12 1245327340,12 1245327836,4 1245327973,4 1245330006,12 1245331244,11 1245331938,11 1245332180,5 1245332187,81 1245332573,5 1245333609,12 1245334447,10 1245334924,9 1245334945,4 1245334971,4 1245335031,9 1245335076,11 1245335948,16 1245335965,27 1245335993,113 1245336107,79 1245336187,64 1245336253,37 1245336431,4 1245336588,5 1245336759,7 1245337048,3 1245337206,13 1245337228,4 1245337309,4 1245337486,6 1245337536,8 1245337565,38 1245337608,100 1245337713,25 1245337755,169 1245337930,8 1245337941,20 1245337967,6 1245337978,7 1245337996,20 1245338019,38 1245338060,127 1245338192,30 1245338227,22 1245338250,15 1245338272,15 1245338310,3 1245338508,4 1245338990,5 1245339136,5 1245339489,8 1245339765,4 1245340220,5 1245340233,6 1245340266,10 1245340278,22 1245340307,7 1245340315,28 1245340359,32 1245340395,4 1245340403,41 1245340446,46 1245340494,58 1245340554,17 1245340573,21 1245340599,3 1245340604,5 1245340611,46 1245340661,26 1245340747,4 1245340814,14 1245341043,4 1245341104,4 1245341672,4 1245341896,5 1245341906,3 1245342301,3 1245342649,6 1245342884,5 1245342929,4 1245343314,6 1245343324,10 1245343335,16 1245343353,39 1245343394,43 1245343439,62 1245343561,3 1245343790,4 1245344115,3 1245344189,5 1245344233,4 1245344241,6 1245344408,12 1245344829,3 1245345090,5 1245345457,5 1245345689,4 1245346086,3 1245347112,12 1245348006,14 1245348261,10 1245348873,4 1245348892,3 1245350303,11 1245350355,4 1245350766,5 1245350931,3 1245351605,14 1245351673,55 1245351729,23 1245351754,5 1245352123,37 1245352163,21 1245352186,18 1245352209,40 1245352251,49 1245352305,8 1245352315,5 1245352321,6 1245352329,22 1245352353,48 1245352404,77 1245352483,58 1245352543,17 1245352570,19 1245352635,5 1245352879,3 1245352899,5 1245352954,4 1245352962,6 1245352970,58 1245353031,21 1245353055,14 1245353071,52 1245353131,37 1245353170,201 1245353373,56 1245353431,18 1245353454,47 1245353502,13 1245353519,106 1245353627,10 1245353647,12 1245353660,30 1245353699,42 1245353746,28 1245353776,29 1245353806,9 1245353818,21 1245353841,10 1245353853,6 1245353862,224 1245354226,4 1245354964,63 1245355029,4 1245355036,142 1245355180,148 1245355330,7 1245355338,23 1245355363,9 1245355374,60 1245355437,142 1245355581,27 1245355609,5 1245355615,2 1245355630,64 1245355700,7 1245355709,73 1245355785,45 1245355834,85 1245355925,9 1245356234,5 1245356620,6 1245356629,12 1245356643,29 1245356676,120 1245356798,126 1245356937,62 1245357001,195 1245357210,17 1245357237,15 1245357258,24 1245357284,53 1245357339,2 1245357345,27 1245357374,76 1245357452,28 1245357482,42 1245357529,14 1245357545,35 1245357582,74 1245357661,30 1245357693,19 1245357714,38 1245357758,11 1245357777,37 1245357817,49 1245357868,19 1245357891,31 1245357931,48 1245357990,49 1245358043,24 1245358082,22 1245358108,17 1245358148,18 1245358168,7 1245358179,6 1245358186,19 1245358209,17 1245358229,5 1245358240,9 1245358252,10 1245358263,6 1245358272,9 1245358296,26 1245358328,49 1245358381,6 1245358389,38 1245358453,19 1245358476,24 1245358504,21 1245358533,76 1245358628,24 1245358653,10 1245358669,105 1245358781,20 1245358808,14 1245358836,6 1245358871,61 1245358933,0 1245358936,44 1245358982,11 1245358996,25 1245359023,15 1245359040,32 1245359076,19 1245359099,13 1245359117,16 1245359138,12 1245359161,33 1245359215,32 1245359249,14 1245359272,7 1245359314,10 1245359333,36 1245359371,21 1245359424,10 1245359447,61 1245359514,32 1245359560,42 1245359604,87 1245359700,60 1245359762,23 1245359786,4 1245359791,8 1245359803,6 1245359813,107 1245359922,29 1245359953,22 1245359978,86 1245360069,75 1245360147,22 1245360170,0 1245360184,41 1245360239,15 1245360256,34 1245360301,37 1245360339,1 1245360342,28 1245360372,20 1245360394,32 1245360440,24 1245360526,3 1245360728,3 1245361011,4 1245361026,35 1245361064,137 1245361359,5 1245362172,11 1245362225,21 1245362248,51 1245362302,20 1245362334,42 1245362418,12 1245362468,7 1245362557,9 1245362817,3 1245363175,4 1245363271,4 1245363446,3 1245363539,4 1245363573,4 1245363635,1 1245363637,3 1245363740,5 1245363875,3 1245364075,4 1245364354,14 1245364370,19 1245364391,49 1245364442,34 1245364478,23 1245364502,80 1245364633,15 1245364650,8 1245364673,16 1245364691,47 1245364739,53 1245364795,39 1245364836,25 1245365353,4 1245365640,11 1245365665,5 1245365726,8 1245365778,7 1245365982,4 1245366017,13 1245366042,6 1245366487,4 1245366493,4 1245366500,4 1245366507,3 1245366622,5 1245366690,5 1245366946,4 1245366953,16 1245366975,8 1245366996,7 1245367005,7 1245367031,6 1245367040,9 1245367051,7 1245367059,23 1245367084,76 1245367166,158 1245367740,4 1245367804,3 1245367847,4 1245367887,9 1245369300,10 1245369611,12 1245370038,10 1245370374,8 1245370668,5 1245370883,5 1245370927,7 1245370945,9 1245370961,16 1245370978,414 1245371398,135 1245371535,252 1245371791,238 1245372034,199 1245372621,4 1245372890,5 1245373043,7 1245373060,9 1245373073,6 1245373081,68 1245373151,10 1245373162,49 1245373212,79 1245373300,12 1245373313,38 1245373353,20 1245373374,59 1245373435,28 1245373465,94 1245373560,11 1245373574,53 1245373629,22 1245373654,6 1245373662,334 1245373998,169 1245374176,41 1245374219,26 1245374246,51 1245374299,31 1245374332,57 1245374391,55 1245374535,4 1245374759,7 1245374769,200 1245374971,215 1245375188,181 1245375371,81 1245375455,59 1245375516,33 1245375552,19 1245375572,56 1245375629,220 1245375850,32 1245375884,26 1245375948,7 1245375964,114 1245376473,4 1245376810,13 1245378296,10 1245378950,12 1245379004,3 1245379569,4 1245379582,4 1245379615,6 1245380030,3 1245380211,4 1245380412,14 1245380727,4 1245380850,4
```

__This log file__ is only 7.3 KB. At this rate, a years' worth of log data can be stored in less than 3MB of plain text files. The data presented here can be graphed (producing the image at the top of the page) using the following code:

```python
# pySquelchGrapher.py
import numpy
import datetime
import pylab
print "loading libraries...",
print "complete"


def loadData(fname="log.txt"):
    print "loading data...",
    # load signal/duration from log file
    f = open(fname)
    raw = f.read()
    f.close()
    raw = raw.replace('n', ' ')
    raw = raw.split(" ")
    signals = []
    for line in raw:
        if len(line) < 3:
            continue
        line = line.split(',')
        sec = datetime.datetime.fromtimestamp(int(line[0]))
        dur = int(line[1])
        signals.append([sec, dur])
    print "complete"
    return signals


def findDays(signals):
    # determine which days are in the log file
    print "finding days...",
    days = []
    for signal in signals:
        day = signal[0].date()
        if not day in days:
            days.append(day)
    print "complete"
    return days


def genMins(day):
    # generate an array for every minute in a certain day
    print "generating bins...",
    mins = []
    startTime = datetime.datetime(day.year, day.month, day.day)
    minute = datetime.timedelta(minutes=1)
    for i in xrange(60*60):
        mins.append(startTime+minute*i)
    print "complete"
    return mins


def fillMins(mins, signals):
    print "filling bins...",
    vals = [0]*len(mins)
    dayToDo = signals[0][0].date()
    for signal in signals:
        if not signal[0].date() == dayToDo:
            continue
        sec = signal[0]
        dur = signal[1]
        prebuf = sec.second
        minOfDay = sec.hour*60+sec.minute
        if dur+prebuf < 60:  # simple case, no rollover seconds
            vals[minOfDay] = dur
        else:  # if duration exceeds the minute the signal started in
            vals[minOfDay] = 60-prebuf
            dur = dur+prebuf
            while (dur > 0):  # add rollover seconds to subsequent minutes
                minOfDay += 1
                dur = dur-60
                if dur <= 0:
                    break
                if dur >= 60:
                    vals[minOfDay] = 60
                else:
                    vals[minOfDay] = dur
    print "complete"
    return vals


def normalize(vals):
    print "normalizing data...",
    divBy = float(max(vals))
    for i in xrange(len(vals)):
        vals[i] = vals[i]/divBy
    print "complete"
    return vals


def smoothListGaussian(list, degree=10):
    print "smoothing...",
    window = degree*2-1
    weight = numpy.array([1.0]*window)
    weightGauss = []
    for i in range(window):
        i = i-degree+1
        frac = i/float(window)
        gauss = 1/(numpy.exp((4*(frac))**2))
        weightGauss.append(gauss)
    weight = numpy.array(weightGauss)*weight
    smoothed = [0.0]*(len(list)-window)
    for i in range(len(smoothed)):
        smoothed[i] = sum(numpy.array(list[i:i+window])*weight)/sum(weight)
    while len(list) > len(smoothed)+int(window/2):
        smoothed.insert(0, smoothed[0])
    while len(list) > len(smoothed):
        smoothed.append(smoothed[0])
    print "complete"
    return smoothed


signals = loadData()
days = findDays(signals)
for day in days:
    mins = genMins(day)
    vals = normalize(fillMins(mins, signals))
    fig = pylab.figure()
    pylab.grid(alpha=.2)
    pylab.plot(mins, vals, 'k', alpha=.1)
    pylab.plot(mins, smoothListGaussian(vals), 'b', lw=1)
    pylab.axis([day, day+datetime.timedelta(days=1), None, None])
    fig.autofmt_xdate()
    pylab.title("147.120 MHz Usage for "+str(day))
    pylab.xlabel("time of day")
    pylab.ylabel("fractional usage")
    pylab.show()

```

