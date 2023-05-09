---
title: Detrending Data in Python with Numpy
date: 2010-06-24 08:38:52
tags: ["python", "obsolete"]
---



> **⚠️ SEE UPDATED POST:** [**Signal Filtering in Python**](https://swharden.com/blog/2020-09-23-signal-filtering-in-python/)

__While continuing my quest__ into the world of linear data analysis and signal processing, I came to a point where I wanted to emphasize variations in FFT traces. While I am keeping my original data for scientific reference, visually I want to represent it emphasizing variations rather than concentrating on trends. I wrote a detrending function which I'm sure will be useful for many applications:

```python
def detrend(data,degree=10):
	detrended=[None]*degree
	for i in range(degree,len(data)-degree):
		chunk=data[i-degree:i+degree]
		chunk=sum(chunk)/len(chunk)
		detrended.append(data[i]-chunk)
	return detrended+[None]*degree
```

<div class="text-center">

![](https://swharden.com/static/2010/06/24/detrend_fft.png)

</div>

However, this method is extremely slow. I need to think of a way to accomplish this same thing much faster. \[ponders\]

__UPDATE:__ It looks like I've once again re-invented the wheel. All of this has been done already, and FAR more efficiently I might add. For more see [scipy.signal.detrend.html](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html)

```python
import scipy.signal
ffty=scipy.signal.detrend(ffty)
```

