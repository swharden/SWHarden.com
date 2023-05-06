---
title: Linear Data Smoothing in Python
date: 2008-11-17 18:50:10
tags: ["old", "python"]
---

# Linear Data Smoothing in Python

> **⚠️ SEE UPDATED POST:** [**Signal Filtering in Python**](https://swharden.com/blog/2020-09-23-signal-filtering-in-python/)

```python
def smoothListGaussian(list, degree=5):
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
    return smoothed
```

Provide a list and it will return a smoother version of the data. The Gaussian smoothing function I wrote is leagues better than a moving window average method, for reasons that are obvious when viewing the chart below. Surprisingly, the moving triangle method appears to be very similar to the Gaussian function at low degrees of spread. However, for large numbers of data points, the Gaussian function should perform better.

<div class="text-center">

[![](https://swharden.com/static/2008/11/17/smooth_thumb.jpg)](https://swharden.com/static/2008/11/17/smooth.png)

</div>

```python
import pylab
import numpy

def smoothList(list, strippedXs=False, degree=10):
    if strippedXs == True:
        return Xs[0:-(len(list)-(len(list)-degree+1))]
    smoothed = [0]*(len(list)-degree+1)
    for i in range(len(smoothed)):
        smoothed[i] = sum(list[i:i+degree])/float(degree)
    return smoothed

def smoothListTriangle(list, strippedXs=False, degree=5):
    weight = []
    window = degree*2-1
    smoothed = [0.0]*(len(list)-window)
    for x in range(1, 2*degree):
        weight.append(degree-abs(degree-x))
    w = numpy.array(weight)
    for i in range(len(smoothed)):
        smoothed[i] = sum(numpy.array(list[i:i+window])*w)/float(sum(w))
    return smoothed

def smoothListGaussian(list, strippedXs=False, degree=5):
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
    return smoothed

### DUMMY DATA ###
data = [0]*30  # 30 "0"s in a row
data[15] = 1  # the middle one is "1"

### PLOT DIFFERENT SMOOTHING FUNCTIONS ###
pylab.figure(figsize=(550/80, 700/80))
pylab.suptitle('1D Data Smoothing', fontsize=16)
pylab.subplot(4, 1, 1)
p1 = pylab.plot(data, ".k")
p1 = pylab.plot(data, "-k")
a = pylab.axis()
pylab.axis([a[0], a[1], -.1, 1.1])
pylab.text(2, .8, "raw data", fontsize=14)
pylab.subplot(4, 1, 2)
p1 = pylab.plot(smoothList(data), ".k")
p1 = pylab.plot(smoothList(data), "-k")
a = pylab.axis()
pylab.axis([a[0], a[1], -.1, .4])
pylab.text(2, .3, "moving window average", fontsize=14)
pylab.subplot(4, 1, 3)
p1 = pylab.plot(smoothListTriangle(data), ".k")
p1 = pylab.plot(smoothListTriangle(data), "-k")
pylab.axis([a[0], a[1], -.1, .4])
pylab.text(2, .3, "moving triangle", fontsize=14)
pylab.subplot(4, 1, 4)
p1 = pylab.plot(smoothListGaussian(data), ".k")
p1 = pylab.plot(smoothListGaussian(data), "-k")
pylab.axis([a[0], a[1], -.1, .4])
pylab.text(2, .3, "moving gaussian", fontsize=14)
# pylab.show()
pylab.savefig("smooth.png", dpi=80)
```

This data needs smoothing. Below is a visual representation of the differences in the methods of smoothing.

<div class="text-center">

[![](https://swharden.com/static/2008/11/17/smooth2_thumb.jpg)](https://swharden.com/static/2008/11/17/smooth2.png)

</div>

The degree of window coverage for the moving window average, moving triangle, and Gaussian functions are 10, 5, and 5 respectively. Also note that (due to the handling of the "degree" variable between the different functions) the actual number of data points assessed in these three functions are 10, 9, and 9 respectively. The degree for the last two functions represents "spread" from each point, whereas the first one represents the total number of points to be averaged for the moving average.