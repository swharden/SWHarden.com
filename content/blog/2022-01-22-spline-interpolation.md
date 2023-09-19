---
title: Spline Interpolation with C# 
description: How to smooth X/Y data using spline interpolation in Csharp
Date: 2022-01-22 16:00:00
tags: ["csharp"]
featured_image: https://swharden.com/static/2022/01/22/interpolation.png
---



**I recently had the need to create a smoothed curve from a series of X/Y data points in a C# application.** I achieved this using cubic [spline interpolation](https://en.wikipedia.org/wiki/Spline_interpolation). I prefer this strategy because I can control the exact number of points in the output curve, and the generated curve (given sufficient points) will pass through the original data making it excellent for data smoothing applications.

<div class='text-center'>

![](https://swharden.com/static/2022/01/22/screenshot.gif)

</div>

The code below is an adaptation of original work by Ryan Seghers (links below) that I modified to narrow its scope, support `double` types, use modern language features, and operate statelessly in a functional style with all `static` methods.

* It targets `.NET Standard 2.0` so it can be used in .NET Framework and .NET Core applications.

* Input `Xs` and `Ys` must be the same length but do not need to be ordered.

* The interpolated curve may have any number of points (not just even multiples of the input length), and may even have fewer points than the original data.

* Users cannot define start or end slopes so the curve generated is a _natural_ spline.

```cs
public static class Cubic
{
    /// <summary>
    /// Generate a smooth (interpolated) curve that follows the path of the given X/Y points
    /// </summary>
    public static (double[] xs, double[] ys) InterpolateXY(double[] xs, double[] ys, int count)
    {
        if (xs is null || ys is null || xs.Length != ys.Length)
            throw new ArgumentException($"{nameof(xs)} and {nameof(ys)} must have same length");

        int inputPointCount = xs.Length;
        double[] inputDistances = new double[inputPointCount];
        for (int i = 1; i < inputPointCount; i++)
        {
            double dx = xs[i] - xs[i - 1];
            double dy = ys[i] - ys[i - 1];
            double distance = Math.Sqrt(dx * dx + dy * dy);
            inputDistances[i] = inputDistances[i - 1] + distance;
        }

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

## Usage

This sample .NET 6 console application uses the class above to create a smoothed (interpolated) curve from a set of random X/Y points. It then plots the original data and the interpolated curve using [ScottPlot](https://scottplot.net).

```cs
// generate sample data using a random walk
Random rand = new(1268);
int pointCount = 20;
double[] xs1 = new double[pointCount];
double[] ys1 = new double[pointCount];
for (int i = 1; i < pointCount; i++)
{
    xs1[i] = xs1[i - 1] + rand.NextDouble() - .5;
    ys1[i] = ys1[i - 1] + rand.NextDouble() - .5;
}

// Use cubic interpolation to smooth the original data
(double[] xs2, double[] ys2) = Cubic.InterpolateXY(xs1, ys1, 200);

// Plot the original vs. interpolated data
var plt = new ScottPlot.Plot(600, 400);
plt.AddScatter(xs1, ys1, label: "original", markerSize: 7);
plt.AddScatter(xs2, ys2, label: "interpolated", markerSize: 3);
plt.Legend();
plt.SaveFig("interpolation.png");
```

<div class='text-center'>

![](https://swharden.com/static/2022/01/22/interpolation.png)

</div>

## Additional Interpolation Methods

There are many different methods that can smooth data. Common methods include [Bézier splines](https://en.wikipedia.org/wiki/B%C3%A9zier_curve), [Catmull-Rom splines](https://www.cs.cmu.edu/~fp/courses/graphics/asst5/catmullRom.pdf), [corner-cutting Chaikin curves](https://www.cs.unc.edu/~dm/UNC/COMP258/LECTURES/Chaikins-Algorithm.pdf), and [Cubic splines](https://en.wikipedia.org/wiki/Spline_interpolation). I recently implemented these strageies to include with ScottPlot (a MIT-licensed 2D plotting library for .NET). Visit [ScottPlot.net](https://ScottPlot.NET) to find the source code for that project and search for the `Interpolation` namespace.

<div class='text-center'>

![](https://swharden.com/static/2022/01/22/csharp-spline-interpolation.png)

</div>

## 1D Interpolation

A set of X/Y points can be interpolated such that they are evenly spaced on the X axis. This 1D interpolation can be used to change the sampling rate of time series data. For more information about 1D interpolation see my other blog post: [Resample Time Series Data using Cubic Spline Interpolation](https://swharden.com/blog/2022-06-23-resample-interpolation/)

<a href="https://swharden.com/blog/2022-06-23-resample-interpolation/">
<img src="https://swharden.com/static/2022/06/23/2-resample.png" class="mx-auto d-block mb-5">
</a>

## Resources
* [Cubic Spline Interpolation source code](https://github.com/SCToolsfactory/SCJMapper-V2/blob/master/OGL/CubicSpline.cs) by Ryan Seghers (MIT license)
* [C# Cubic Spline Interpolation article](https://www.codeproject.com/Articles/560163/Csharp-Cubic-Spline-Interpolation) by Ryan Seghers (Code Project)
* [Numerical Recipes in C++: Cubic Spline Interpolation
](http://www.foo.be/docs-free/Numerical_Recipe_In_C/c3-3.pdf)
* [Fast Cubic Spline Interpolation
](https://arxiv.org/pdf/2001.09253.pdf) by Haysn Hornbeck
* Download this project from [C# Data Visualization](https://github.com/swharden/Csharp-Data-Visualization) on GitHub
* [Bézier Spline Interpolation](http://scaledinnovation.com/analytics/splines/aboutSplines.html)
