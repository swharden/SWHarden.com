---
title: Simple Exponential Fit with C#
description: How to fit an exponential curve to data points using pure csharp
Date: 2024-08-24 20:09:00
tags: ["csharp"]
---

**This article describes how to perform a simple exponential fit using pure C#.** Exponential curves which pass through 0 can be described using two variables, so data can be translated from into linear space, fitted using a linear least squares strategy, then translated back into exponential space. 


```cs
// These are the data points we wish to fit
double[] xs = [1, 2, 3, 4, 5, 6, 7];
double[] ys = [258, 183, 127, 89, 65, 48, 35];

// Log-transform values, then perform a linear fit
double[] logYs = ys.Select(x => Math.Log(x)).ToArray();
(double slope, double intercept) = LeastSquaresFit(xs, logYs);

// Convert back to exponential form and display the result
double a = Math.Exp(intercept);
Console.WriteLine($"y = {a}*e^({slope}*x)");
```

![](https://swharden.com/static/2024/08/24/fit.png)

Here's the [Linear Least Squares](https://en.wikipedia.org/wiki/Linear_least_squares) implementation used by the code sample above:

```cs
static (double slope, double intercept) LeastSquaresFit(double[] xs, double[] ys)
{
    double sumX = 0, sumY = 0, sumX2 = 0, sumXY = 0;

    for (int i = 0; i < xs.Length; i++)
    {
        sumX += xs[i];
        sumY += ys[i];
        sumX2 += xs[i] * xs[i];
        sumXY += xs[i] * ys[i];
    }

    double avgX = sumX / xs.Length;
    double avgY = sumY / xs.Length;
    double avgX2 = sumX2 / xs.Length;
    double avgXY = sumXY / xs.Length;
    double slope = (avgXY - avgX * avgY) / (avgX2 - avgX * avgX);
    double intercept = (avgX2 * avgY - avgXY * avgX) / (avgX2 - avgX * avgX);
    return (slope, intercept);
}
```

### Plotting Data

The graphs above were made using [ScottPlot.NET](https://ScottPlot.net) using the following code:

```cs
ScottPlot.Plot plot = new();

// plot the original data and the fitted curve
var dataMarkers = plot.Add.ScatterPoints(xs, ys);
dataMarkers.MarkerSize = 10;
dataMarkers.LegendText = "Raw Data";

// generate and plot the fitted curve
double[] fitXs = Enumerable.Range(0, 100).Select(x => x * .1).ToArray();
double[] fitYs = fitXs.Select(x => a * Math.Exp(slope * x)).ToArray();
var fitLine = plot.Add.ScatterLine(fitXs, fitYs);
fitLine.LineWidth = 2;
fitLine.LinePattern = ScottPlot.LinePattern.DenselyDashed;
fitLine.LegendText = "Fitted Curve";

// decorate the plot and save it
plot.Legend.Alignment = ScottPlot.Alignment.UpperRight;
plot.Title($"y = {a:N2}*e^({slope:N2}*x)");
plot.SavePng("fit.png", 400, 300);
```

### Optimizing Curves for Other Formulas

The code above is ideal for calculating two terms to generate a fitted curve according to the formula:

<div class='text-center fs-5 my-3 fw-light'>
Y = A * e<sup>B * x</sup>
</div>

...but what about fitting to a curve with third term describing a Y offset?

<div class='text-center fs-5 my-3 fw-light'>
Y = C + A * e<sup>B * x</sup>
</div>

...or a forth term describing an X offset too?

<div class='text-center fs-5 my-3 fw-light'>
Y = C + A * e<sup>B * x + D</sup>
</div>

**The linear least squares fitting strategy described above is not sufficient for fitting data to these complex curves.** The linear least squares strategy can be applied in higher dimensional space using gradient descent to seek optimized curves for more advanced equations. This strategy is summarized by _The Math Coffeeshop_ in a fantastic YouTube video about using [Linear Least Squares to Solve Nonlinear Problems
](https://www.youtube.com/watch?v=jezAWd6GFRg). However, formulas representing the partial derivative of each unknown in the error function must be calculated which may be difficult. An alternative strategy is to use [Particle swarm optimization](https://en.wikipedia.org/wiki/Particle_swarm_optimization) to iteratively work toward an optimal solution for a fitted curve even if the derivative of the error function cannot be calculated. These strategies will be described in a future article, but a work in progress demonstration may currently be found in the [SwarmFit](https://github.com/swharden/SwarmFit) GitHub repository.

## Resources
* [Source Code for these examples](https://github.com/swharden/Exponential-Fit-CSharp) on GitHub
* [Linear Least Squares optimization](https://en.wikipedia.org/wiki/Linear_least_squares) (Wikipedia)
* [SwarmFit](https://github.com/swharden/SwarmFit) - A .NET package for fitting curves to X/Y data using particle swarm optimization
* [Linear Least Squares to Solve Nonlinear Problems](https://www.youtube.com/watch?v=jezAWd6GFRg) - A fantastic YouTube video describing how to use least squares strategy to fit nonlinear functions.
* [C# Helper](http://www.csharphelper.com/howtos/howto_exponential_curve_fit.html) - A legacy .NET WinForms app which uses gradient descent of the least squares error function to seek the best fit of an exponential curve
* [Exponential Fit with Python](https://swharden.com/blog/2020-09-24-python-exponential-fit/)