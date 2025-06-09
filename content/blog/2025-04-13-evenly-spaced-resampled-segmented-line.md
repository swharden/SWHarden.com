---
title: Resampling Segmented Lines for Evenly Spaced Points
description: How to create a collection of points along a segmented line evenly spaced in line distance or 2D space
Date: 2025-04-13 16:12:00
tags: ["csharp", "graphics"]
---

**I recently had the need to convert a segmented line (polyline) with arbitrary node points to one with evenly spaced points.** After exploring a few solutions I settled on the following two strategies because of their simplicity and performance. Code on this page avoids trigonometric functions and square root operations to enhance performance.

## Resampling for Equal Distance Along the Length of the Line

**Simple linear interpolation may be employed to place points at specific distances along the length of the line.** This method minimizes computations but it may place points closer together in 2D space than the specified distance, a phenomenon which is exacerbated when original polyline contains very sharp angles.

<a href="https://swharden.com/static/2025/04/13/spacing-line-1.png">
<img src="https://swharden.com/static/2025/04/13/spacing-line-1.png">
</a>

```cs
// Start with a segmented line with arbitrary points
List<Vector2> polyline1 = [new(1, 1), new(3, 8), new(5, 2), new(9, 9)];

// Generate a new segmented line with evenly spaced points
double spacing = 1;
List<Vector2> polyline2 = ResampleAlongLine(polyline1, spacing);
```

```cs
List<Vector2> ResampleAlongLine(List<Vector2> polyline1, float spacing)
{
    List<Vector2> polyline2 = [];
    
    // start at the same first point as the original line
    polyline2.Add(new(polyline1[0].X, polyline1[0].Y));

    float distanceToNextPoint2 = spacing;
    for (int i = 1; i < polyline1.Count; i++)
    {
        Vector2 p0 = polyline1[i - 1];
        Vector2 p1 = polyline1[i];

        float dx = p0.X - p1.X;
        float dy = p0.Y - p1.Y;
        float distanceToNextPoint1 = (float)Math.Sqrt(dx * dx + dy * dy);

        while (distanceToNextPoint2 <= distanceToNextPoint1)
        {
            float t = distanceToNextPoint2 / distanceToNextPoint1;
            float x = p0.X + t * (p1.X - p0.X);
            float y = p0.Y + t * (p1.Y - p0.Y);
            polyline2.Add(new Vector2(x, y));

            // consider the point we just placed p0 and re-evaluate
            p0 = polyline2.Last();
            distanceToNextPoint1 -= distanceToNextPoint2;
            distanceToNextPoint2 = spacing;
        }

        // move backwards as needed before advancing to the next given pair
        distanceToNextPoint2 -= distanceToNextPoint1;
    }

    return polyline2;
}
```

## Resampling for Equal Euclidean Distance in 2D Space

**This implementation walks along the interpolated polyline segments in short steps and places new points when the target distance in 2D space has been exceeded.** This strategy can be significantly slower than the linear interpolation only method described above, but this it ensures that sequential points are the desired distance apart in 2D space (equal Euclidean spacing on a Cartesian coordinate system) and may be preferred for some applications. The accuracy can be increased by reducing the epsilon at the expense of increased computing time. Performance may be improved by starting with a large epsilon and decreasing it dynamically as the calculated distance between the test point and previous point approaches the target separation.

<a href="https://swharden.com/static/2025/04/13/spacing-2d-1.png">
<img src="https://swharden.com/static/2025/04/13/spacing-2d-1.png">
</a>

```cs
// Start with a segmented line with arbitrary points
List<Vector2> polyline1 = [new(1, 1), new(3, 8), new(5, 2), new(9, 9)];

// Generate a new segmented line with evenly spaced points
double spacing = 1;
List<Vector2> polyline2 = ResampleIn2D(polyline1, spacing);
```

```cs
List<Vector2> ResampleIn2D(List<Vector2> polyline, float spacing, float epsilon = 0.0001f)
{
    List<Vector2> polyline2 = [];

    // start at the same first point as the original line
    polyline2.Add(new(polyline[0].X, polyline[0].Y));

    // compare this because calculating square roots is very costly
    float spacingSquared = spacing * spacing;

    // consider each line segment between pairs of points in the given polyline
    for (int i = 1; i < polyline.Count; i++)
    {
        Vector2 p1 = polyline[i - 1];
        Vector2 p2 = polyline[i];

        // use epsilon to determine how many points along the line to try
        float sdx = p1.X - p2.X;
        float sdy = p1.X - p2.X;
        float segLength = (float)Math.Sqrt(sdx * sdx + sdy * sdy);
        int stepCount = (int)(segLength / epsilon);

        // check the distance at each step along the segment
        for (int j = 0; j <= stepCount; j++)
        {
            // decide the test point using linear interpolation
            float fraction = (float)j / stepCount;
            float lx = p1.X + (p2.X - p1.X) * fraction;
            float ly = p1.Y + (p2.Y - p1.Y) * fraction;
            Vector2 pTest = new(lx, ly);

            // add the test point if it's the right distance from the last one
            float dx = polyline2.Last().X - pTest.X;
            float dy = polyline2.Last().Y - pTest.Y;
            float pTestDistanceSquared = (dx * dx + dy * dy);
            if (pTestDistanceSquared >= spacingSquared)
            {
                polyline2.Add(pTest);
            }
        }
    }

    return polyline2;
}
```

### Full Source Code

**Below is the single file .NET 9 Console Application I used to generate the figures on this page.** [ScottPlot.net](https://scottplot.net) was used to generate the images. Note that `Vector2` has a `Lerp()` method for linear interpolation and `Distance()` and `DistanceSquared()` methods for measuring distances between points, but I chose to implement these functions discretely to make the code on this page easier to translate to other languages.

<details>
<summary>View the full source code</summary>

```cs
using System.Numerics;

List<Vector2> polyline1 = [new(1, 1), new(3, 8), new(5, 2), new(9, 9)];

for (int i = 1; i <= 10; i++)
{
    List<Vector2> polyline2 = ResampleAlongLine(polyline1, i);
    Plotting.Plot(polyline1, polyline2, i, "line", "Even Spacing Along Polyline", ScottPlot.Colors.Black.WithAlpha(.5));

    List<Vector2> polyline3 = ResampleIn2D(polyline1, i);
    Plotting.Plot(polyline1, polyline3, i, "2d", "Even Spacing in 2D Space", ScottPlot.Colors.Magenta.WithAlpha(.5));
    ShowDistances(i, polyline3);
}

static void ShowDistances(float expected, List<Vector2> polyline)
{
    var distances = Enumerable.Range(0, polyline.Count - 1)
        .Select(i => Vector2.Distance(polyline[i], polyline[i + 1]));

    Console.WriteLine($"[{expected}] " + string.Join(", ", distances));
}

static List<Vector2> ResampleAlongLine(List<Vector2> polyline1, float spacing)
{
    if (polyline1.Count < 2)
        throw new InvalidDataException("need at least 2 points");

    if (spacing <= 0)
        throw new InvalidDataException("spacing must be positive");

    List<Vector2> polyline2 = []; // will be filled with evenly-spaced points
    polyline2.Add(new(polyline1[0].X, polyline1[0].Y)); // start at the same first point

    float distanceToNextPoint2 = spacing;
    for (int i = 1; i < polyline1.Count; i++)
    {
        Vector2 p0 = polyline1[i - 1];
        Vector2 p1 = polyline1[i];

        float dx = p0.X - p1.X;
        float dy = p0.Y - p1.Y;
        float distanceToNextPoint1 = (float)Math.Sqrt(dx * dx + dy * dy);

        while (distanceToNextPoint2 <= distanceToNextPoint1)
        {
            float t = distanceToNextPoint2 / distanceToNextPoint1;
            float x = p0.X + t * (p1.X - p0.X);
            float y = p0.Y + t * (p1.Y - p0.Y);
            polyline2.Add(new Vector2(x, y));

            // consider the point we just placed p0 and re-evaluate
            p0 = polyline2.Last();
            distanceToNextPoint1 -= distanceToNextPoint2;
            distanceToNextPoint2 = spacing;
        }

        // move backwards as needed before advancing to the next given pair
        distanceToNextPoint2 -= distanceToNextPoint1;
    }

    return polyline2;
}

static List<Vector2> ResampleIn2D(List<Vector2> polyline, float spacing, float epsilon = 0.0001f)
{
    List<Vector2> polyline2 = [];

    // start at the same first point as the original line
    polyline2.Add(new(polyline[0].X, polyline[0].Y));

    // compare this because calculating square roots is very costly
    float spacingSquared = spacing * spacing;

    // consider each pair of points in the given polyline
    for (int i = 1; i < polyline.Count; i++)
    {
        Vector2 p1 = polyline[i - 1];
        Vector2 p2 = polyline[i];

        // use epsilon to determine how many points along the line to try
        int stepCount = (int)(Vector2.Distance(p1, p2) / epsilon);
        for (int j = 0; j <= stepCount; j++)
        {
            // decide the test point using linear interpolation
            float fraction = (float)j / stepCount;
            float lx = p1.X + (p2.X - p1.X) * fraction;
            float ly = p1.Y + (p2.Y - p1.Y) * fraction;
            Vector2 pTest = new(lx, ly);

            // add the test point if it's the right distance from the last one
            float dx = polyline2.Last().X - pTest.X;
            float dy = polyline2.Last().Y - pTest.Y;
            float pTestDistanceSquared = (dx * dx + dy * dy);
            if (pTestDistanceSquared >= spacingSquared)
            {
                polyline2.Add(pTest);
            }
        }
    }

    return polyline2;
}

public static class Extensions
{
    public static ScottPlot.Coordinates[] ToCoordinates(this List<Vector2> points)
    {
        return [.. points.Select(x => new ScottPlot.Coordinates(x.X, x.Y))];
    }
}

static class Plotting
{
    public static void Plot(List<Vector2> points1, List<Vector2> points2, int spacing, string name, string legend, ScottPlot.Color color)
    {
        ScottPlot.Plot plot = new();
        var sp1 = plot.Add.Scatter(points1.ToCoordinates());
        sp1.Color = ScottPlot.Colors.C1;
        sp1.LineWidth = 2;
        sp1.MarkerSize = 7;
        sp1.LegendText = "Original Polyline";

        var markers = plot.Add.Markers(points2.ToCoordinates());
        markers.Color = color;
        markers.MarkerShape = ScottPlot.MarkerShape.OpenCircle;
        markers.MarkerSize = 13;
        markers.MarkerLineWidth = 2;
        markers.LegendText = legend;

        plot.Axes.SetLimits(0, 10, 0, 10);
        plot.SavePng($"spacing-{name}-{spacing}.png", 700, 400);
    }
}
```

</details>

## Additional Resources
* [Resample Time Series Data using Cubic Spline Interpolation](https://swharden.com/blog/2022-06-23-resample-interpolation/)
* [Spline Interpolation with C#](https://swharden.com/blog/2022-01-22-spline-interpolation/)
* [2D and 3D Spline Interpolation with C#](https://swharden.com/blog/2022-01-22-spline-interpolation/) - Blog post from Jan, 2022
* [Spline Interpolation with ScottPlot](https://scottplot.net/cookbook/4.1/category/misc/#spline-interpolation) - Demonstrates additional types of interpolation: Bezier, Catmull-Rom, Chaikin, Cubic, etc. The project is open source under a MIT license.
* [Programmer's guide to polynomials and splines](https://wordsandbuttons.online/programmers_guide_to_polynomials_and_splines.html)
* [Bézier Spline Interpolation](http://scaledinnovation.com/analytics/splines/aboutSplines.html)