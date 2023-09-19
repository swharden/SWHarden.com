---
title: Signal Filtering in Python
description: How to apply low-pass, high-pass, and band-pass filters with Python
date: 2020-09-23 21:46:00
tags: ["python"]
featured_image: https://swharden.com/static/2023/08/27/filter.png
---

**This page describes how to perform low-pass, high-pass, and band-pass filtering in Python.** I favor SciPy's [`filtfilt`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html) function because the filtered data it produces is the same length as the source data and it has no phase offset, so the output always aligns nicely with the input. The [`sosfiltfilt`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html) function is even more convenient because it consumes filter parameters as a single object which makes them easier work with.

<a href="https://swharden.com/static/2023/08/27/filter.png">
<img src="https://swharden.com/static/2023/08/27/filter.png">
</a>

### Low-Pass Filter

```py
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt

def lowpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, cutoff, 'lowpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# Apply a 50 Hz low-pass filter to the original data
filtered = lowpass(data, 50, sample_rate)
```

<a href="https://swharden.com/static/2023/08/27/lowpass.png">
<img src="https://swharden.com/static/2023/08/27/lowpass.png">
</a>

```py
# Code used to display the result
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), sharex=True, sharey=True)
ax1.plot(times, data)
ax1.set_title("Original Signal")
ax1.margins(0, .1)
ax1.grid(alpha=.5, ls='--')
ax2.plot(times, filtered)
ax2.set_title("Low-Pass Filter (50 Hz)")
ax2.grid(alpha=.5, ls='--')
plt.tight_layout()
plt.show()
```

### High-Pass Filter

```py
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt

def highpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, cutoff, 'highpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# Apply a 20 Hz high-pass filter to the original data
filtered = highpass(data, 20, sample_rate)
```

<a href="https://swharden.com/static/2023/08/27/highpass.png">
<img src="https://swharden.com/static/2023/08/27/highpass.png">
</a>

```py
# Code used to display the result
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), sharex=True, sharey=True)
ax1.plot(times, data)
ax1.set_title("Original Signal")
ax1.margins(0, .1)
ax1.grid(alpha=.5, ls='--')
ax2.plot(times, filtered)
ax2.set_title("High-Pass Filter (20 Hz)")
ax2.grid(alpha=.5, ls='--')
plt.tight_layout()
plt.show()
```

### Band-Pass Filter

```py
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt

def bandpass(data: np.ndarray, edges: list[float], sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, edges, 'bandpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# Apply a 10-50 Hz high-pass filter to the original data
filtered = bandpass(data, [10, 50], sample_rate)
```

<a href="https://swharden.com/static/2023/08/27/bandpass.png">
<img src="https://swharden.com/static/2023/08/27/bandpass.png">
</a>

```py
# Code used to display the result
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), sharex=True, sharey=True)
ax1.plot(times, data)
ax1.set_title("Original Signal")
ax1.margins(0, .1)
ax1.grid(alpha=.5, ls='--')
ax2.plot(times, filtered)
ax2.set_title("Band-Pass Filter (10-50 Hz)")
ax2.grid(alpha=.5, ls='--')
plt.tight_layout()
plt.show()
```

### Low-Pass Cutoff Frequency

This code evaluates the same signal low-pass filtered using different cutoff frequencies:

```py
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# Plot the original signal
plt.plot(times, data, '.-', alpha=.5, label="original signal")

# Plot the signal low-pass filtered using different cutoffs
for cutoff in [10, 20, 30, 50]:
    sos = scipy.signal.butter(5, cutoff, 'lowpass', fs=sample_rate, output='sos')
    filtered = scipy.signal.sosfiltfilt(sos, data)
    plt.plot(times, filtered, label=f"low-pass {cutoff} Hz")

plt.legend()
plt.grid(alpha=.5, ls='--')
plt.axis([0.35, 0.5, None, None])
plt.show()
```

<a href="https://swharden.com/static/2023/08/27/lowpass-freqs.png">
<img src="https://swharden.com/static/2023/08/27/lowpass-freqs.png">
</a>

## Use Gustafsson's Method to Reduce Edge Artifacts

**Artifacts may appear in the smooth signal if the first or last data point differs greatly from their adjacent points.** This is because, in an effort to ensure the filtered signal length is the same as the input signal, the input signal is "padded" with data on each side prior to filtering. The default behavior is to pad the data by duplicating the first and last data points, but this causes artifacts in the smoothed signal if the first or last points contain an extreme value. An alternative strategy is _Gustafsson's Method_, described in [a 1996 paper by Fredrik Gustafsson](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=492552) in which "initial conditions are chosen for the forward and backward passes so that the forward-backward filter gives the same result as the backward-forward filter." Interestingly, the original publication demonstrates the method by filtering noise out of an ECG recording.

```py
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# Isolate a small portion of data to inspect
segment = data[350:400]

# Create a 5-pole low-pass filter with an 80 Hz cutoff
b, a = scipy.signal.butter(5, 80, fs=sample_rate)

# Apply the filter using the default edge method (padding)
filtered_pad = scipy.signal.filtfilt(b, a, segment)

# Apply the filter using Gustafsson's method
filtered_gust = scipy.signal.filtfilt(b, a, segment, method="gust")
```

<a href="https://swharden.com/static/2023/08/27/lowpass-gustafsson.png">
<img src="https://swharden.com/static/2023/08/27/lowpass-gustafsson.png">
</a>

```py
# Display the Results
plt.plot(segment, '.-', alpha=.5, label="data")
plt.plot(filtered_pad, 'k--', label="Default (Padding)")
plt.plot(filtered_gust, 'k', label="Gustafsson's Method")
plt.legend()
plt.grid(alpha=.5, ls='--')
plt.title("Padded Data vs. Gustafsson’s Method")
plt.show()
```

## Filter Using Convolution

**An alternative strategy to low-pass a signal is to use convolution.** In this method you create a kernel (typically a bell-shaped curve) and _convolve_ the kernel with the signal. The wider the window is the smoother the output signal will be. Also, the window must be normalized so its sum is 1 to preserve the amplitude of the input signal. Note that this method exclusively uses NumPy and does not require SciPy.

**There are different for handling data at the edges of the signal,** but setting `mode` to `valid` deletes insufficiently filtered points at the edges to produce an output signal that is fully filtered but slightly shorter than the input signal. See [`numpy.convolve`](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html) documentation for additional information.

**The kernel shape affects the spectral properties of the filter.** Commonly called [_window functions_](https://en.wikipedia.org/wiki/Window_function), these different shapes produce filtered signals with different frequency response characteristics. The [Hanning window](https://en.wikipedia.org/wiki/Hann_function) is preferred for most general purpose signal processing applications. See [FftSharp](https://github.com/swharden/FftSharp) for additional information about the pros and cons of common window functions.

```python
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

# Load sample data from a WAV file
sample_rate, data = scipy.io.wavfile.read('ecg.wav')
times = np.arange(len(data))/sample_rate

# create a Hanning kernel 1/50th of a second wide
kernel_width_seconds = 1.0/50
kernel_size_points = int(kernel_width_seconds * sample_rate)
kernel = np.hanning(kernel_size_points)

# normalize the kernel
kernel = kernel / kernel.sum()

# Create a filtered signal by convolving the kernel with the original data
filtered = np.convolve(kernel, data, mode='valid')
```

<a href="https://swharden.com/static/2023/08/27/lowpass-convolution.png">
<img src="https://swharden.com/static/2023/08/27/lowpass-convolution.png">
</a>

```python
# Display the result
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3))

ax1.plot(np.arange(len(kernel))/sample_rate, kernel, '.-')
ax1.set_title("Kernel (1/50 sec wide)")
ax1.grid(alpha=.5, ls='--')

ax2.plot(np.arange(len(data))/sample_rate, data)
ax2.set_title("Original Signal")
ax2.margins(0, .1)
ax2.grid(alpha=.5, ls='--')

ax3.plot(np.arange(len(filtered))/sample_rate, filtered)
ax3.set_title("Convolved Signal")
ax3.margins(0, .1)
ax3.grid(alpha=.5, ls='--')

plt.tight_layout()
plt.show()
```

## History of this Article
* In 2008 I started blogging about different ways to filter signals using Python 2. These now-obsolete blog posts are still accessible: [Linear Data Smoothing in Python (2008)](https://swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/), [Signal Filtering with Python (2009)](https://swharden.com/blog/2009-01-21-signal-filtering-with-python/), [Smoothing Window Data Averaging with Python (2010)](https://swharden.com/blog/2010-06-20-smoothing-window-data-averaging-in-python-moving-triangle-tecnique/), and [Detrending Data in Python with Numpy (2010)](https://swharden.com/blog/2010-06-24-detrending-data-in-python-with-numpy/).

* In 2020 I created this page to showcase SciPy's signal processing package `scipy.signal` and used `filtfilt` to create low-pass filtered signals with no phase offset from the input data.

* In 2023 I updated this article to add Python 3 type hints, use more idiomatic Python naming schemes, favor `sosfiltfilt` over `filtfilt`, and create matplotlib plots and subplots using its more modern API.

## Resources

* Example data: [ecg.wav](https://swharden.com/static/2020/09/23/ecg.wav)

* [scipy.signal.filtfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html)

* [scipy.signal.sosfiltfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html)

* [numpy.convolve](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)

* [Window Functions](https://en.wikipedia.org/wiki/Window_function) (Wikipedia)

* [FftSharp](https://github.com/swharden/FftSharp)

* [Determining the initial states in forward-backward filtering](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=492552) (Gustafsson, 1996)