---
title: Performant Data Smoothing in C#
description: Exploring the Halving Bidirectional Simple Moving Average (HBSMA) strategy for generating progressively smoothed curves from noisy datasets
Date: 2024-12-27 15:36:00
tags: ["csharp"]
---

## Optimized Simple Moving Average Algorithm

**The simple moving average (SMA) for an array of length `N` using a window of size `W` can be efficiently calculated using a running sum maintained in memory.** 
As the window moves along the data, new values are shifted into it by adding their value to the running sum, and old values are shifted out by subtracting their value from the running sum.

![](https://swharden.com/static/2024/12/27/Test_Continuous_ForwardMovingAverage.png)

**This strategy reduces the number of operations** from approximately `O(N*W)` to `O(N*2)` which offers considerable performance enhancement for applications requiring large smoothing windows.

```cs
double[] SmoothForward(double[] data, int windowSize)
{
    double[] smooth = new double[data.Length];
    double runningSum = 0;
    int pointsInSum = 0;
    for (int i = 0; i < smooth.Length; i++)
    {
        runningSum += data[i];
        if (pointsInSum < windowSize)
        {
            pointsInSum++;
            smooth[i] += runningSum / pointsInSum;
            continue;
        }
        runningSum -= data[i - windowSize];
        smooth[i] += runningSum / windowSize;
    }
    return smooth;
}
```

## Optimized Bidirectional Simple Moving Average Algorithm

**Applying two successive moving window averages in opposite directions** is a quick way to achieve bidirectional smoothing and prevents the "trailing" effect caused by a lagging running average which can be seen in the example above. 

![](https://swharden.com/static/2024/12/27/Test_Continuous_BidirectionalMovingAverage.png)

**Bidirectional smoothing doubles the number of operations** from `O(N*2)` to `O(N*4)` but this strategy used here is still far more performant than `O(N*W)` realized by convolution with a triangular kernel which is expected to produce a similar result.

```cs
double[] SmoothBidirectional(double[] data, int windowSize)
{
    double[] smooth = new double[data.Length];

    // smooth from left to right
    double runningSum = 0;
    int pointsInSum = 0;
    for (int i = 0; i < smooth.Length; i++)
    {
        runningSum += data[i];
        if (pointsInSum < windowSize)
        {
            pointsInSum++;
            smooth[i] += runningSum / pointsInSum;
            continue;
        }
        runningSum -= data[i - windowSize];
        smooth[i] += runningSum / windowSize;
    }

    // smooth from right to left
    runningSum = 0;
    pointsInSum = 0;
    for (int i = smooth.Length - 1; i >= 0; i--)
    {
        runningSum += data[i];
        if (pointsInSum < windowSize)
        {
            pointsInSum++;
            smooth[i] += runningSum / pointsInSum;
            continue;
        }
        runningSum -= data[i + windowSize];
        smooth[i] += runningSum / windowSize;
    }

    // average the two directions
    for (int i = 0; i < smooth.Length; i++)
        smooth[i] /= 2;

    return smooth;
}
```

## Halving Bidirectional Simple Moving Average (HBSMA)

**Successively smoothing data using repeatedly halved window sizes** is a strategy I have recently found to be extremely useful for aggressively smoothing large amounts of signal data over long timescales. This HBSMA strategy is especially good at smoothing discontinuous data with "jumps" in the signal. With a performance approximating `O(N*log(W))` it offers vastly superior performance over convolution with a Gaussian kernel, while producing roughly similar output.

**I think of this strategy has having three primary functions** that each act according to the size of the window:

* Large windows: smooth jumps in discontinuous data
* Small windows: smooth high frequency noise
* Intermediate windows: smooth transitions between jumps

<div class='row'>
<div class='col-md'><a href='https://swharden.com/static/2024/12/27/Test_Discontinuous_BidirectionalMovingAverage.png'><img src='https://swharden.com/static/2024/12/27/Test_Discontinuous_BidirectionalMovingAverage.png'></a></div>
<div class='col-md'><a href='https://swharden.com/static/2024/12/27/Test_Discontinuous_HalvingBidirectionalMovingAverage.png'><img src='https://swharden.com/static/2024/12/27/Test_Discontinuous_HalvingBidirectionalMovingAverage.png'></a></div>
</div>

**A looping strategy is demonstrated here,** but a recursive algorithm could also be realized to achieve the same effect.

```cs
public static double[] SmoothBidirectionalHalving(double[] data, int windowSize)
{
    double[] smooth = data;
    while (windowSize > 0)
    {
        smooth = SmoothBidirectional(smooth, windowSize);
        windowSize /= 2;
    }
    return smooth;
}
```

## Faster than Gaussian Convolution with Similar Results

**Let's compare results of the halving bidirectional simple moving average (HBSMA) with a traditional convolution strategy using a Gaussian kernel.**
In this strategy our rectangular window is replaced with a bell-shaped window (a kernel) which is used to produce a weighted moving average for each point in the original dataset.
A [Gaussian window](https://en.wikipedia.org/wiki/Window_function#Gaussian_window) provides bidirectional smoothing, 
but since it never reaches zero on the edges I prefer using 
a [Hanning window](https://en.wikipedia.org/wiki/Window_function#Hann_and_Hamming_windows) for applications like this.

![](https://swharden.com/static/2024/12/27/Test_Discontinuous_HalvingBidirectionalMovingAverageVsConvolution.png)

**The HBSMA strategy produces a result strikingly similar with the Gaussian convolution,** but in less than one tenth of the time. 
Performance benchmarking on my system revealed a 10x improvement in speed for the data above, 
but demonstrated over 130x performance improvement for larger signals (10,000 points) smoothed with a bigger window (100 points).

## Moving Window Padding Strategies

**It is worth noting that moving window averaging strategies must account for the situation at the ends of the original data where
there are not enough data points to fill the window.** In these cases a "padding" strategy may be used to fill the window to ensure
the same number of data points are averaged to create each value on the smoothed curve. 
The examples in this article do not use fancy padding (their behavior is best described by the "None" option below), 
but it is worth being aware of common padding strategies:

* **None** - Calculated the average from fewer values at the edge of the data
* **Constant** - Pad with a repeated user-defined value
* **Mirror** - Pad with data values mirrored at the ege of the data
* **Nearest** - Pad with repeated copies of the value at the edge of the data
* **Wrap** - Wrap data values around so one end is averaged with the opposite end

## Conclusion

**The Halving Bidirectional Simple Moving Average (HBSMA) strategy enables data smoothing with results similar to Gaussian convolution 
but in a small fraction of the time.** The performance of HBSMA is approximately `O(N*log(M)*2)` whereas the convolution strategy is approximately
`O(N*M)`, and the larger the smoothing window size is the more gains may be had by this data smoothing strategy.

## Additional Resources
* [Data Smoothing in C#](https://github.com/swharden/csharp-data-smoothing) - GitHub repository used to create graphics and benchmarks for this article
* [Spline Interpolation: How to smooth X/Y data](https://swharden.com/blog/2022-01-22-spline-interpolation/) - Article from 2022
* [Resample Time Series Data using Cubic Spline Interpolation](https://swharden.com/blog/2022-06-23-resample-interpolation/) - Article from 2022
* [Exponential Smoothing](https://en.wikipedia.org/wiki/Exponential_smoothing) - Wikipedia
* [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter) - Wikipedia
* [Convolution](https://en.wikipedia.org/wiki/Convolution) - Wikipedia
* [Common Window Functions](https://en.wikipedia.org/wiki/Window_function#Examples_of_window_functions) - Wikipedia
* [Window Functions Provided with FFTsharp](https://github.com/swharden/FftSharp?tab=readme-ov-file#windowing) - NuGet Package