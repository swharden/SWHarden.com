---
title: Smoothing Window Data Averaging in Python - Moving Triangle Tecnique
date: 2010-06-20 22:12:03
tags: ["python", "old"]
---

# Smoothing Window Data Averaging in Python - Moving Triangle Tecnique

> **⚠️ SEE UPDATED POST:** [**Signal Filtering in Python**](https://swharden.com/blog/2020-09-23-signal-filtering-in-python/)

__While I wrote a pervious post on linear data smoothing with python,__ those scripts were never fully polished. Fred (KJ4LFJ) asked me about this today and I felt bad I had nothing to send him. While I might add that the script below isn't polished, at least it's clean. I've been using this method for all of my smoothing recently. Funny enough, none of my code was clean enough to copy and paste, so I wrote this from scratch tonight. It's a function to take a list in (any size) and smooth it with a triangle window (of any size, given by "degree") and return the smoothed data with or without flanking copies of data to make it the identical length as before. The script also graphs the original data vs. smoothed traces of varying degrees. The output is below. I hope it helps whoever wants it!

<div class="text-center">

![](https://swharden.com/static/2010/06/20/moving-triangle-python-data-smoothing.png)

</div>

```python
import numpy
import pylab


def smoothTriangle(data, degree, dropVals=False):
    """
    performs moving triangle smoothing with a variable degree.
    note that if dropVals is False, output length will be identical
        to input length, but with copies of data at the flanking regions
    """
    triangle = numpy.array(range(degree)+[degree]+range(degree)[::-1])+1
    smoothed = []
    for i in range(degree, len(data)-degree*2):
        point = data[i:i+len(triangle)]*triangle
        smoothed.append(sum(point)/sum(triangle))
    if dropVals:
        return smoothed
    smoothed = [smoothed[0]]*(degree+degree/2)+smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed


### CREATE SOME DATA ###
data = numpy.random.random(100)  # make 100 random numbers from 0-1
data = numpy.array(data*100, dtype=int)  # make them integers from 1 to 100
for i in range(100):
    data[i] = data[i]+i**((150-i)/80.0)  # give it a funny trend

### GRAPH ORIGINAL/SMOOTHED DATA ###
pylab.plot(data, "k.-", label="original data", alpha=.3)
pylab.plot(smoothTriangle(data, 3), "-", label="smoothed d=3")
pylab.plot(smoothTriangle(data, 5), "-", label="smoothed d=5")
pylab.plot(smoothTriangle(data, 10), "-", label="smoothed d=10")
pylab.title("Moving Triangle Smoothing")
pylab.grid(alpha=.3)
pylab.axis([20, 80, 50, 300])
pylab.legend()
pylab.show()

```

