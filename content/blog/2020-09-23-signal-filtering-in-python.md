---
title: Signal Filtering in Python
date: 2020-09-23 21:46:00
tags: ["python"]
---

# Signal Filtering in Python

**Over a decade ago I posted code demonstrating how to filter data in Python, but there have been many improvements since then.** My original posts ([1](https://swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/), [2](https://swharden.com/blog/2009-01-21-signal-filtering-with-python/), [3](https://swharden.com/blog/2010-06-20-smoothing-window-data-averaging-in-python-moving-triangle-tecnique/), [4](https://swharden.com/blog/2010-06-24-detrending-data-in-python-with-numpy/)) required creating discrete filtering functions, but modern approaches can leverage Numpy and Scipy to do this more easily and efficiently. In this article we will use [`scipy.signal.filtfilt`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html) to apply low-pass, high-pass, and band-pass filters to reduce noise in an ECG signal (stored in [ecg.wav](ecg.wav) (created as part of my [Sound Card ECG](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/) project).

<div class="text-center">

![](signal-lowpass-filter.png)

</div>

Moving-window filtering methods often result in a filtered signal that lags behind the original data (a _phase shift_). By filtering the signal twice in opposite directions `filtfilt` cancels-out this phase shift to produce a filtered signal which is nicely aligned with the input data.

```python
import scipy.io.wavfile
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

# read ECG data from the WAV file
sampleRate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sampleRate

# apply a 3-pole lowpass filter at 0.1x Nyquist frequency
b, a = scipy.signal.butter(3, 0.1)
filtered = scipy.signal.filtfilt(b, a, data)
```

<div class="text-center">

![](signal-lowpass-ecg.png)

</div>

```python
# plot the original data next to the filtered data

plt.figure(figsize=(10, 4))

plt.subplot(121)
plt.plot(times, data)
plt.title("ECG Signal with Noise")
plt.margins(0, .05)

plt.subplot(122)
plt.plot(times, filtered)
plt.title("Filtered ECG Signal")
plt.margins(0, .05)

plt.tight_layout()
plt.show()
```

## Cutoff Frequency

The second argument passed into the `butter` method customizes the cut-off frequency of the Butterworth filter. This value (Wn) is a number between 0 and 1 representing the _fraction of the Nyquist frequency_ to use for the filter. Note that [Nyquist frequency](https://en.wikipedia.org/wiki/Nyquist_frequency) is half of the sample rate. As this fraction increases, the cutoff frequency increases. You can get fancy and express this value as 2 * Hz / sample rate.

```python
plt.plot(data, '.-', alpha=.5, label="data")

for cutoff in [.03, .05, .1]:
    b, a = scipy.signal.butter(3, cutoff)
    filtered = scipy.signal.filtfilt(b, a, data)
    label = f"{int(cutoff*100):d}%"
    plt.plot(filtered, label=label)
    
plt.legend()
plt.axis([350, 500, None, None])
plt.title("Effect of Different Cutoff Values")
plt.show()
```

<div class="text-center">

![](signal-lowpass-cutoff.png)

</div>

## Improve Edges with Gustafsson’s Method

Something weird happens at the edges. There's not enough data "off the page" to know how to smooth those points, so what should be done? 

**Padding is the default behavior,** where edges are padded with with duplicates of the edge data points and smooth the trace as if those data points existed. The drawback of this is that one stray data point at the edge will greatly affect the shape of your smoothed data.

**Gustafsson’s Method may be superior to padding.** The advantage of this method is that stray points at the edges do not greatly influence the smoothed curve at the edges. This technique is described in [a 1994 paper by Fredrik Gustafsson](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=492552). "Initial conditions are chosen for the forward and backward passes so that the forward-backward filter gives the same result as the backward-forward filter." Interestingly this paper demonstrates the method by filtering noise out of an EKG recording.

```python
# A small portion of data will be inspected for demonstration
segment = data[350:400]

filtered = scipy.signal.filtfilt(b, a, segment)
filteredGust = scipy.signal.filtfilt(b, a, segment, method="gust")

plt.plot(segment, '.-', alpha=.5, label="data")
plt.plot(filtered, 'k--', label="padded")
plt.plot(filteredGust, 'k', label="Gustafsson")
plt.legend()
plt.title("Padded Data vs. Gustafsson’s Method")
plt.show()
```

<div class="text-center">

![](signal-method-gust.png)

</div>

## Band-Pass Filter

Low-pass and high-pass filters can be selected simply by customizing the third argument passed into the filter. The second argument indicates frequency (as fraction of Nyquist frequency, half the sample rate). Passing a list of two values in for the second argument allows for band-pass filtering of a signal.

```python
b, a = scipy.signal.butter(3, 0.05, 'lowpass')
filteredLowPass = scipy.signal.filtfilt(b, a, data)

b, a = scipy.signal.butter(3, 0.05, 'highpass')
filteredHighPass = scipy.signal.filtfilt(b, a, data)

b, a = scipy.signal.butter(3, [.01, .05], 'band')
filteredBandPass = scipy.signal.lfilter(b, a, data)
```

<div class="text-center">

![](signal-lowpass-highpass-bandpass.png)

</div>

## Filter using Convolution

**Another way to low-pass a signal is to use convolution.** In this method you create a window (typically a bell-shaped curve) and _convolve_ the window with the signal. The wider the window is the smoother the output signal will be. Also, the window must be normalized so its sum is 1 to preserve the amplitude of the input signal.

There are different ways to handle what happens to data points at the edges (see [`numpy.convolve`](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html) for details), but setting `mode` to `valid` delete these points to produce an output signal slightly smaller than the input signal.

```python
# create a normalized Hanning window
windowSize = 40
window = np.hanning(windowSize)
window = window / window.sum()

# filter the data using convolution
filtered = np.convolve(window, data, mode='valid')
```

<div class="text-center">

![](signal-convolution-filter.png)

</div>

```python
plt.subplot(131)
plt.plot(kernel)
plt.title("Window")

plt.subplot(132)
plt.plot(data)
plt.title("Data")

plt.subplot(133)
plt.plot(filtered)
plt.title("Filtered")
```

**Different window functions filter the signal in different ways.** Hanning windows are typically preferred because they have a mostly Gaussian shape but touch zero at the edges. For a discussion of the pros and cons of different window functions for spectral analysis using the FFT, see my notes on [FftSharp](https://github.com/swharden/FftSharp).

## Resources

* Sample data: [ecg.wav](ecg.wav)

* [Sound Card ECG](https://swharden.com/blog/2019-03-15-sound-card-ecg-with-ad8232/)

* Jupyter notebook for this page: [signal-filtering.ipynb](signal-filtering.ipynb)

* SciPy Cookbook: [Filtfilt](https://scipy-cookbook.readthedocs.io/items/FiltFilt.html), [Buterworth Bandpass Filter](https://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html)

* SciPy Documentation: [scipy.signal.filtfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html), [scipy.signal.butter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html)

* Numpy Documentation: [numpy.convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)

* [Savitzky Golay Filtering](https://scipy-cookbook.readthedocs.io/items/SavitzkyGolay.html) - The Savitzky Golay filter is a particular type of low-pass filter, well adapted for data smoothing.