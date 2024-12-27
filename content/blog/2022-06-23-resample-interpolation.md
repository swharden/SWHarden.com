---
title: Resample Time Series Data using Cubic Spline Interpolation
description: Signal resampling with spline interpolation in pure C#
Date: 2022-06-23 21:15:00
tags: ["csharp", "graphics"]
featured_image: https://swharden.com/static/2022/06/23/3-comparison.png
---

**Cubic spline interpolation can be used to modify the sample rate of time series data.** This page describes how I achieve signal resampling with spline interpolation in pure C# without any external dependencies. This technique can be used to:

* Convert unevenly-sampled data to a series of values with a fixed sample rate

* Convert time series data from one sample rate to another sample rate

* Fill-in missing values from a collection of measurements

### Simulating Data Samples

To simulate unevenly-sampled data I create a theoretical signal then sample it at 20 random time points.

```cs
// this function represents the signal being measured
static double f(double x) => Math.Sin(x * 10) + Math.Sin(x * 13f);

// randomly sample values from 20 time points
Random rand = new(123);
double[] sampleXs = Enumerable.Range(0, 20)
    .Select(x => rand.NextDouble())
    .OrderBy(x => x)
    .ToArray();
double[] sampleYs = sampleXs.Select(x => f(x)).ToArray();
```

<img src="https://swharden.com/static/2022/06/23/1-samples-only.png" class="mx-auto d-block mb-5">

### Resample for Evenly-Spaced Data

I then generate an interpolated spline using my sampled data points as the input. 

* I can control the sample rate by defining the number of points generated in the output signal. 

* Full source code is at the bottom of this article.

```cs
(double[] xs, double[] ys) = Cubic.Interpolate1D(sampleXs, sampleYs, count: 50);
```

<img src="https://swharden.com/static/2022/06/23/2-resample-only.png" class="mx-auto d-block mb-5">

The generated points line-up perfectly with the sampled data.

<img src="https://swharden.com/static/2022/06/23/2-resample.png" class="mx-auto d-block mb-5">

There is slight deviation from the theoretical signal (and it's larger where there is more missing data) but this is an unsurprising result considering the original samples had large gaps of missing data.

<img src="https://swharden.com/static/2022/06/23/3-comparison.png" class="mx-auto d-block mb-5">

## Source Code

### Interpolation.cs

```cs
public static class Interpolation
{
    public static (double[] xs, double[] ys) Interpolate1D(double[] xs, double[] ys, int count)
    {
        if (xs is null || ys is null || xs.Length != ys.Length)
            throw new ArgumentException($"{nameof(xs)} and {nameof(ys)} must have same length");

        int inputPointCount = xs.Length;
        double[] inputDistances = new double[inputPointCount];
        for (int i = 1; i < inputPointCount; i++)
            inputDistances[i] = inputDistances[i - 1] + xs[i] - xs[i - 1];

        double meanDistance = inputDistances.Last() / (count - 1);
        double[] evenDistances = Enumerable.Range(0, count).Select(x => x * meanDistance).ToArray();
        double[] xsOut = Interpolate(inputDistances, xs, evenDistances);
        double[] ysOut = Interpolate(inputDistances, ys, evenDistances);
        return (xsOut, ysOut);
    }

    private static double[] Interpolate(double[] xOrig, double[] yOrig, double[] xInterp)
    {
        (double[] a, double[] b) = FitMatrix(xOrig, yOrig);

        double[] yInterp = new double[xInterp.Length];
        for (int i = 0; i < yInterp.Length; i++)
        {
            int j;
            for (j = 0; j < xOrig.Length - 2; j++)
                if (xInterp[i] <= xOrig[j + 1])
                    break;

            double dx = xOrig[j + 1] - xOrig[j];
            double t = (xInterp[i] - xOrig[j]) / dx;
            double y = (1 - t) * yOrig[j] + t * yOrig[j + 1] +
                t * (1 - t) * (a[j] * (1 - t) + b[j] * t);
            yInterp[i] = y;
        }

        return yInterp;
    }

    private static (double[] a, double[] b) FitMatrix(double[] x, double[] y)
    {
        int n = x.Length;
        double[] a = new double[n - 1];
        double[] b = new double[n - 1];
        double[] r = new double[n];
        double[] A = new double[n];
        double[] B = new double[n];
        double[] C = new double[n];

        double dx1, dx2, dy1, dy2;

        dx1 = x[1] - x[0];
        C[0] = 1.0f / dx1;
        B[0] = 2.0f * C[0];
        r[0] = 3 * (y[1] - y[0]) / (dx1 * dx1);

        for (int i = 1; i < n - 1; i++)
        {
            dx1 = x[i] - x[i - 1];
            dx2 = x[i + 1] - x[i];
            A[i] = 1.0f / dx1;
            C[i] = 1.0f / dx2;
            B[i] = 2.0f * (A[i] + C[i]);
            dy1 = y[i] - y[i - 1];
            dy2 = y[i + 1] - y[i];
            r[i] = 3 * (dy1 / (dx1 * dx1) + dy2 / (dx2 * dx2));
        }

        dx1 = x[n - 1] - x[n - 2];
        dy1 = y[n - 1] - y[n - 2];
        A[n - 1] = 1.0f / dx1;
        B[n - 1] = 2.0f * A[n - 1];
        r[n - 1] = 3 * (dy1 / (dx1 * dx1));

        double[] cPrime = new double[n];
        cPrime[0] = C[0] / B[0];
        for (int i = 1; i < n; i++)
            cPrime[i] = C[i] / (B[i] - cPrime[i - 1] * A[i]);

        double[] dPrime = new double[n];
        dPrime[0] = r[0] / B[0];
        for (int i = 1; i < n; i++)
            dPrime[i] = (r[i] - dPrime[i - 1] * A[i]) / (B[i] - cPrime[i - 1] * A[i]);

        double[] k = new double[n];
        k[n - 1] = dPrime[n - 1];
        for (int i = n - 2; i >= 0; i--)
            k[i] = dPrime[i] - cPrime[i] * k[i + 1];

        for (int i = 1; i < n; i++)
        {
            dx1 = x[i] - x[i - 1];
            dy1 = y[i] - y[i - 1];
            a[i - 1] = k[i - 1] * dx1 - dy1;
            b[i - 1] = -k[i] * dx1 + dy1;
        }

        return (a, b);
    }
}
```

### Program.cs

This is the source code I used to generate the figures on this page. 

Plots were generated using [ScottPlot.NET](https://scottplot.net).

```cs
// this function represents the signal being measured
static double f(double x) => Math.Sin(x * 10) + Math.Sin(x * 13f);

// create points representing randomly sampled time points of a smooth curve
Random rand = new(123);
double[] sampleXs = Enumerable.Range(0, 20)
    .Select(x => rand.NextDouble())
    .OrderBy(x => x)
    .ToArray();
double[] sampleYs = sampleXs.Select(x => f(x)).ToArray();

// use 1D interpolation to create an evenly sampled curve from unevenly sampled data
(double[] xs, double[] ys) = Interpolation.Interpolate1D(sampleXs, sampleYs, count: 50);

var plt = new ScottPlot.Plot(600, 400);

double[] theoreticalXs = ScottPlot.DataGen.Range(xs.Min(), xs.Max(), .01);
double[] theoreticalYs = theoreticalXs.Select(x => f(x)).ToArray();
var perfectPlot = plt.AddScatterLines(theoreticalXs, theoreticalYs);
perfectPlot.Label = "theoretical signal";
perfectPlot.Color = plt.Palette.GetColor(2);
perfectPlot.LineStyle = ScottPlot.LineStyle.Dash;

var samplePlot = plt.AddScatterPoints(sampleXs, sampleYs);
samplePlot.Label = "sampled points";
samplePlot.Color = plt.Palette.GetColor(0);
samplePlot.MarkerSize = 10;
samplePlot.MarkerShape = ScottPlot.MarkerShape.openCircle;
samplePlot.MarkerLineWidth = 2;

var smoothPlot = plt.AddScatter(xs, ys);
smoothPlot.Label = "interpolated points";
smoothPlot.Color = plt.Palette.GetColor(3);
smoothPlot.MarkerShape = ScottPlot.MarkerShape.filledCircle;

plt.Legend();
plt.SaveFig("output.png");
```

## 2D and 3D Spline Interpolation

**The interpolation method described above only considered the horizontal axis** when generating evenly-spaced time points (1D interpolation). For information and code examples regarding 2D and 3D cubic spline interpolation, see my previous blog post: [Spline Interpolation with C#](https://swharden.com/blog/2022-01-22-spline-interpolation/) 

<a href="https://swharden.com/blog/2022-01-22-spline-interpolation/"><img src="https://swharden.com/static/2022/01/22/screenshot.gif" class="mx-auto d-block mb-5"></a>

## Resources

* [2D and 3D Spline Interpolation with C#](https://swharden.com/blog/2022-01-22-spline-interpolation/) - Blog post from Jan, 2022

* [Spline Interpolation with ScottPlot](https://scottplot.net/cookbook/4.1/category/misc/#spline-interpolation) - Demonstrates additional types of interpolation: Bezier, Catmull-Rom, Chaikin, Cubic, etc. The project is open source under a MIT license.

* [Programmer's guide to polynomials and splines](https://wordsandbuttons.online/programmers_guide_to_polynomials_and_splines.html)
