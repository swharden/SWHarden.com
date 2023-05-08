---
title: Graphing Computer Usage
date: 2009-05-20 08:44:57
tags: ["python", "old"]
---

# Graphing Computer Usage

__I enjoy writing Python scripts to analyze and display linear data.__ One of my favorite blog entries is [Linear Data Smoothing with Python](http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/), developed for my [homemade electrocardiogram](http://www.swharden.com/blog/category/diy-ecg-home-made-electrocardiogram/) project. I installed a program called TimeTrack.exe on my work computer. It basically logs whenever you open or close a program. The data output looks like this:

```
"Firefox","Prototype of a Digital Biopsy Device - Mozilla Firefox","05/19/2009  9:45a","05/19/2009  9:45a","766ms","0.0"
"Firefox","Dual-Channel Mobile Surface Electromyograph - Mozilla Firefox","05/19/2009  9:46a","05/19/2009  9:46a","797ms","0.0"
"Windows Explorer","","03/24/2008  9:30a","05/19/2009  9:48a","49d 6h 9m","20.7"
"Windows Explorer","09_04_07_RA_SA_AV","05/19/2009  8:48a","05/19/2009  8:48a","1.0s","0.0"
"Windows Explorer","Image003.jpg - Windows Picture and Fax Viewer","05/18/2009  4:03p","05/18/2009  4:03p","1.2s","0.0"
```

__I have a 13 MB file containing lines like this__ which I parse, condense, analyze, and display with Python. The script finds the first and last entry time and creates a dictionary where keys are the hours between the 1st and last log lines, parses the log, determines which time block each entry belongs to, and increments the integer (value of the dictionary) for its respective key. Something similar is repeated, but with respect to days rather than hours. The result is:

<div class="text-center">

![](https://swharden.com/static/2009/05/20/compusage_white.png)

</div>

The code I used to generate this graph is:

```python
# This script analyzes data exported from "TimeTrack" (a free computer usage
# monitoring program for windows) and graphs the data visually.

import time, pylab, datetime, numpy

# This is my computer usage data.  Generate yours however you want.
allHours = ['2008_10_29 0', '2009_03_11 5', '2009_04_09 5', '2008_07_04 10',
'2008_12_18 9', '2009_01_30 12', '2008_09_04 7', '2008_05_17 1',
'2008_05_11 5', '2008_11_03 3', '2008_05_21 3', '2009_02_19 11',
'2008_08_15 13', '2008_04_02 4', '2008_07_16 5', '2008_09_16 8',
'2008_04_10 5', '2009_05_10 1', '2008_12_30 4', '2008_06_07 2',
'2008_11_23 0', '2008_08_03 0', '2008_04_30 4', '2008_07_28 9',
'2008_05_19 0', '2009_03_30 7', '2008_06_19 3', '2009_01_24 3',
'2008_08_23 6', '2008_12_01 0', '2009_02_23 6', '2008_11_27 0',
'2008_05_02 5', '2008_10_20 13', '2008_03_27 5', '2009_04_02 9',
'2009_02_21 0', '2008_09_13 1', '2008_12_13 0', '2009_04_14 11',
'2009_01_31 7', '2008_11_04 10', '2008_07_09 6', '2008_10_24 10',
'2009_02_22 0', '2008_09_25 12', '2008_12_25 0', '2008_05_26 4',
'2009_05_01 10', '2009_04_26 11', '2008_08_10 8', '2008_11_08 6',
'2008_07_21 12', '2009_04_21 3', '2009_05_13 8', '2009_02_02 8',
'2008_10_07 2', '2008_06_10 6', '2008_09_21 0', '2009_03_17 9',
'2008_08_30 7', '2008_11_28 4', '2009_02_14 0', '2009_01_22 6',
'2008_10_11 0', '2008_06_22 8', '2008_12_04 0', '2008_03_28 0',
'2009_04_07 2', '2008_09_10 0', '2008_05_15 5', '2008_08_18 12',
'2008_10_31 5', '2009_03_09 7', '2009_02_25 8', '2008_07_02 4',
'2008_12_16 7', '2008_09_06 2', '2009_01_26 5', '2009_04_19 0',
'2008_07_14 13', '2008_11_01 5', '2009_01_18 0', '2009_05_04 0',
'2008_08_13 10', '2009_02_27 3', '2009_01_16 12', '2008_09_18 8',
'2009_02_03 7', '2008_06_01 0', '2008_12_28 0', '2008_07_26 0',
'2008_11_21 1', '2008_08_01 8', '2008_04_28 3', '2009_05_16 0',
'2008_06_13 5', '2008_10_02 11', '2009_03_28 6', '2008_08_21 7',
'2009_01_13 6', '2008_11_25 4', '2008_06_25 1', '2008_10_22 11',
'2008_03_25 6', '2009_02_07 6', '2008_12_11 4', '2009_01_01 4',
'2008_09_15 2', '2009_02_05 12', '2008_07_07 9', '2009_04_12 0',
'2008_04_11 5', '2008_10_26 4', '2008_05_28 3', '2008_09_27 14',
'2009_05_03 0', '2008_12_23 5', '2009_05_12 10', '2008_11_14 3',
'2008_07_19 0', '2009_04_24 8', '2008_04_07 1', '2008_08_08 11',
'2008_06_04 0', '2009_05_15 12', '2009_03_23 13', '2009_02_01 10',
'2008_09_23 11', '2009_02_08 3', '2008_08_28 4', '2008_11_18 9',
'2008_07_31 7', '2008_10_13 0', '2008_06_16 9', '2009_03_27 6',
'2008_12_02 0', '2008_05_01 7', '2009_04_05 1', '2008_08_16 9',
'2009_03_15 0', '2008_04_16 6', '2008_10_17 4', '2008_06_28 5',
'2009_01_28 10', '2008_04_18 0', '2008_12_14 0', '2008_11_07 6',
'2009_04_17 7', '2008_04_14 7', '2008_07_12 0', '2009_01_15 7',
'2009_05_06 8', '2008_12_26 0', '2008_06_03 7', '2008_09_28 0',
'2008_05_25 4', '2008_08_07 8', '2008_04_26 7', '2008_07_24 1',
'2008_04_20 0', '2008_11_11 4', '2009_04_29 0', '2008_10_04 0',
'2009_05_18 9', '2009_03_18 4', '2008_06_15 8', '2009_02_13 6',
'2008_05_04 5', '2009_03_04 2', '2009_03_06 3', '2008_05_06 0',
'2008_08_27 11', '2008_04_22 0', '2009_03_26 6', '2008_03_31 9',
'2008_06_27 5', '2008_10_08 4', '2008_09_09 4', '2008_12_09 3',
'2008_05_10 0', '2008_05_14 5', '2009_04_10 0', '2009_01_11 0',
'2008_07_05 8', '2009_01_05 7', '2008_10_28 0', '2009_02_18 11',
'2009_03_10 7', '2008_05_30 3', '2008_09_05 7', '2008_12_21 6',
'2009_03_02 6', '2008_08_14 5', '2008_11_12 5', '2008_07_17 8',
'2008_04_05 6', '2009_04_22 11', '2009_05_09 0', '2008_06_06 0',
'2009_01_03 0', '2008_09_17 6', '2009_03_21 3', '2009_02_10 7',
'2008_05_08 4', '2008_08_02 0', '2008_11_16 0', '2008_07_29 12',
'2008_10_15 5', '2008_06_18 5', '2009_03_25 2', '2009_01_10 0',
'2009_04_03 5', '2008_08_22 7', '2009_03_13 11', '2008_10_19 0',
'2008_06_30 8', '2008_09_02 9', '2008_05_23 4', '2008_12_12 7',
'2008_07_10 11', '2008_11_05 8', '2008_04_12 4', '2009_04_15 7',
'2008_12_24 1', '2008_09_30 0', '2008_05_27 2', '2008_08_05 10',
'2008_04_24 6', '2009_04_27 6', '2008_07_22 3', '2008_11_09 1',
'2008_06_09 6', '2008_10_06 14', '2009_03_16 7', '2008_05_22 5',
'2009_01_29 12', '2008_11_29 4', '2008_04_09 7', '2008_08_25 12',
'2009_02_15 0', '2008_03_29 7', '2008_06_21 7', '2008_10_10 9',
'2008_05_12 6', '2009_02_16 10', '2008_09_11 11', '2008_12_07 0',
'2008_07_03 6', '2009_04_08 3', '2009_01_23 7', '2009_01_27 5',
'2008_10_30 0', '2009_03_08 0', '2009_01_21 8', '2008_12_19 0',
'2008_05_16 2', '2009_01_25 1', '2009_02_26 5', '2008_09_07 2',
'2008_04_03 1', '2008_08_12 6', '2008_04_13 10', '2008_11_02 0',
'2008_07_15 0', '2009_04_20 3', '2009_02_24 10', '2009_05_11 8',
'2008_12_31 8', '2008_04_15 7', '2008_09_19 10', '2009_01_19 0',
'2008_11_22 3', '2008_07_27 2', '2009_02_04 7', '2009_03_31 1',
'2008_05_24 3', '2008_10_01 8', '2008_06_12 6', '2009_01_12 11',
'2008_11_26 8', '2009_04_01 10', '2009_02_28 0', '2008_08_20 6',
'2008_10_21 10', '2008_06_24 4', '2008_03_26 4', '2008_12_10 0',
'2008_09_12 0', '2008_05_09 7', '2009_02_17 7', '2008_07_08 6',
'2008_10_25 5', '2009_04_13 9', '2009_05_02 0', '2008_12_22 8',
'2008_09_24 9', '2009_01_20 5', '2008_11_15 6', '2009_04_25 10',
'2008_08_11 9', '2008_04_06 8', '2008_07_20 1', '2009_03_22 3',
'2008_06_11 6', '2008_09_20 3', '2009_05_14 10', '2008_11_19 0',
'2008_08_31 2', '2009_02_09 8', '2008_10_12 0', '2008_04_25 5',
'2008_06_23 4', '2009_01_07 8', '2008_08_19 0', '2008_12_05 2',
'2008_07_01 8', '2008_10_16 6', '2009_04_06 3', '2009_03_14 5',
'2008_09_01 2', '2008_12_17 14', '2008_05_18 7', '2008_04_01 2',
'2009_04_18 0', '2008_04_17 0', '2008_07_13 0', '2008_06_02 10',
'2008_09_29 6', '2008_12_29 0', '2009_05_05 8', '2008_04_19 0',
'2009_04_30 8', '2008_08_06 4', '2008_11_20 0', '2008_07_25 6',
'2009_02_06 6', '2009_03_29 3', '2009_05_17 0', '2009_03_19 7',
'2008_10_03 1', '2008_06_14 3', '2008_05_07 5', '2008_08_26 3',
'2008_11_24 9', '2008_04_21 8', '2008_04_23 4', '2008_10_23 11',
'2008_06_26 4', '2008_03_24 8', '2008_12_08 5', '2008_09_14 2',
'2009_01_02 6', '2008_04_08 0', '2008_10_27 6', '2009_04_11 0',
'2008_07_06 0', '2008_12_20 3', '2009_04_23 6', '2008_09_26 9',
'2008_05_31 0', '2008_07_18 4', '2008_11_13 6', '2008_08_09 2',
'2008_04_04 0', '2009_03_20 5', '2008_09_22 7', '2009_05_08 9',
'2008_06_05 7', '2008_07_30 7', '2008_11_17 10', '2008_05_03 0',
'2008_08_29 3', '2009_02_11 12', '2009_01_08 8', '2008_06_17 0',
'2008_10_14 7', '2009_03_24 11', '2008_08_17 6', '2008_12_03 0',
'2009_01_09 4', '2008_05_29 5', '2008_06_29 9', '2008_10_18 5',
'2009_04_04 0', '2008_12_15 10', '2009_03_12 0', '2009_03_05 7',
'2008_05_20 4', '2008_09_03 7', '2009_03_07 8', '2009_01_14 6',
'2008_05_05 5', '2008_11_06 7', '2008_07_11 6', '2009_04_16 9',
'2009_02_20 0', '2008_12_27 0', '2009_01_17 0', '2009_05_07 7',
'2008_11_10 5', '2008_07_23 11', '2009_04_28 0', '2008_04_27 2',
'2008_08_04 0', '2009_03_01 11', '2008_10_05 0', '2008_06_08 8',
'2009_05_19 5', '2008_04_29 4', '2008_11_30 0', '2009_01_06 8',
'2009_02_12 3', '2008_08_24 2', '2009_03_03 10', '2008_10_09 6',
'2008_06_20 2', '2008_05_13 10', '2008_12_06 0', '2008_03_30 7']

def genTimes():
    ## opens  exported timetrack data (CSV) and re-saves a compressed version.
    print "ANALYZING..."
    f=open('timetrack.txt')
    raw=f.readlines()
    f.close()
    times=["05/15/2009 12:00am"] #start time
    for line in raw[1:]:
        if not line.count('","') == 5: continue
        test = line.strip("n")[1:-1].split('","')[-3].replace("  "," ")+"m"
        test = test.replace(" 0:"," 12:")
        times.append(test) #end time
        test = line.strip("n")[1:-1].split('","')[-4].replace("  "," ")+"m"
        test = test.replace(" 0:"," 12:")
        times.append(test) #start time

    times.sort()
    print "WRITING..."
    f=open('times.txt','w')
    f.write(str(times))
    f.close()

def loadTimes():
    ## loads the times from the compressed file.
    f=open("times.txt")
    times = eval(f.read())
    newtimes=[]
    f.close()
    for i in range(len(times)):
        if "s" in times[i]: print times[i]
        newtimes.append(datetime.datetime(*time.strptime(times[i],
                                        "%m/%d/%Y %I:%M%p")[0:5]))
        #if i&gt;1000: break #for debugging
    newtimes.sort()
    return newtimes

def linearize(times):
    ## does all the big math to calculate hours per day.
    for i in range(len(times)):
        times[i]=times[i]-datetime.timedelta(minutes=times[i].minute,
                                             seconds=times[i].second)
    hr = datetime.timedelta(hours=1)
    pos = times[0]-hr
    counts = {}
    days = {}
    lasthr=pos
    lastday=None
    while pos1:counts[pos]=1 #flatten
        if not daypos in days: days[daypos]=0
        if not lasthr == pos:
            if counts[pos]&gt;0:
                days[daypos]=days[daypos]+1
                lasthr=pos
        pos+=hr
    return days #[counts,days]

def genHours(days):
    ## outputs the hours per day as a file.
    out=""
    for day in days:
        print day
        out+="%s %in"%(day.strftime("%Y_%m_%d"),days[day])
    f=open('hours.txt','w')
    f.write(out)
    f.close()
    return

def smoothListGaussian(list,degree=7):
    ## (from an article I wrote) - Google "linear data smoothing with python".
    firstlen=len(list)
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
    pad_before = [smoothed[0]]*((firstlen-len(smoothed))/2)
    pad_after  = [smoothed[-1]]*((firstlen-len(smoothed))/2+1)
    return pad_before+smoothed+pad_after

### IF YOU USE MY DATA, YOU ONLY USE THE FOLLOWING CODE ###

def graphIt():
    ## Graph the data!
    #f=open('hours.txt')
    #data=f.readlines()
    data=allHours
    data.sort()
    f.close()
    days,hours=[],[]
    for i in range(len(data)):
        day = data[i].split(" ")
        if int(day[1])&lt;4: continue
        days.append(datetime.datetime.strptime(day[0], "%Y_%m_%d"))
        hours.append(int(day[1]))
    fig=pylab.figure(figsize=(14,5))
    pylab.plot(days,smoothListGaussian(hours,1),'.',color='.5',label="single day")
    pylab.plot(days,smoothListGaussian(hours,1),'-',color='.8')
    pylab.plot(days,smoothListGaussian(hours,7),color='b',label="7-day gausian average")
    pylab.axhline(8,color='k',ls=":")
    pylab.title("Computer Usage at Work")
    pylab.ylabel("hours (rounded)")
    pylab.legend()
    pylab.show()
    return

#times = genTimes()
#genHours(linearize(loadTimes()))
graphIt()
```