---
title: Treemapping with C#
description: How to create a treemap diagram using C#
Date: 2023-03-28 00:32:00
tags: ["csharp", "graphics"]
---

**Treemap diagrams display a series of positive numbers using rectangles sized proportional to the value of each number.** This page demonstrates how to calculate the size and location of rectangles to create a tree map diagram using C#. Although the following uses System.Drawing to save the tree map as a Bitmap image, these concepts may be combined with information on the [C# Data Visualization](https://swharden.com/csdv/) page to create treemap diagrams using SkiaSharp, WPF, or other graphics technologies.

<img src="https://swharden.com/static/2023/03/07/treemap.png" class="shadow my-5">

The tree map above was generated from random data using the following C# code:

```cs
// Create sample data. Data must be sorted large to small.
double[] sortedValues = Enumerable.Range(0, 40)
    .Select(x => (double)Random.Shared.Next(10, 100))
    .OrderByDescending(x => x)
    .ToArray();

// Create an array of labels in the same order as the sorted data.
string[] labels = sortedValues.Select(x => x.ToString()).ToArray();

// Calculate the size and position of all rectangles in the tree map
int width = 600;
int height = 400;
RectangleF[] rectangles = TreeMap.GetRectangles(sortedValues, width, height);

// Create an image to draw on (with 1px extra to make room for the outline)
using Bitmap bmp = new(width + 1, height + 1);
using Graphics gfx = Graphics.FromImage(bmp);
using Font fnt = new("Consolas", 8);
using SolidBrush brush = new(Color.Black);
gfx.Clear(Color.White);

// Draw and label each rectangle
for (int i = 0; i < rectangles.Length; i++)
{
    brush.Color = Color.FromArgb(
        red: Random.Shared.Next(150, 250),
        green: Random.Shared.Next(150, 250),
        blue: Random.Shared.Next(150, 250));

    gfx.FillRectangle(brush, rectangles[i]);
    gfx.DrawRectangle(Pens.Black, rectangles[i]);
    gfx.DrawString(labels[i], fnt, Brushes.Black, rectangles[i].X, rectangles[i].Y);
}

// Save the output
bmp.Save("treemap.bmp");
```

## Treemap Logic

The previous code block focuses on data generation and display, but hides the tree map calculations behind the `TreeMap` class. Below is the code for that class. It is self-contained static class and exposes a single static method which takes a pre-sorted array of values and returns tree map rectangles ready to display on an image.

> 💡 Although the `System.Drawing.Common` is a Windows-only library ([as of .NET 7](https://github.com/dotnet/designs/blob/main/accepted/2021/system-drawing-win-only/system-drawing-win-only.md)), `System.Drawing.Primitives` is a cross-platform package that provides the `RectangleF` structure used in the tree map class. See the [SkiaSharp Quickstart](https://swharden.com/csdv/skiasharp/quickstart-console/) to learn how to create image files using cross-platform .NET code.

```cs
public static class TreeMap
{
    public static RectangleF[] GetRectangles(double[] values, int width, int height)
    {
        for (int i = 1; i < values.Length; i++)
            if (values[i] > values[i - 1])
                throw new ArgumentException("values must be ordered large to small");

        var slice = GetSlice(values, 1, 0.35);
        var rectangles = GetRectangles(slice, width, height);
        return rectangles.Select(x => x.ToRectF()).ToArray();
    }

    private class Slice
    {
        public double Size { get; }
        public IEnumerable<double> Values { get; }
        public Slice[] Children { get; }

        public Slice(double size, IEnumerable<double> values, Slice sub1, Slice sub2)
        {
            Size = size;
            Values = values;
            Children = new Slice[] { sub1, sub2 };
        }

        public Slice(double size, double finalValue)
        {
            Size = size;
            Values = new double[] { finalValue };
            Children = Array.Empty<Slice>();
        }
    }

    private class SliceResult
    {
        public double ElementsSize { get; }
        public IEnumerable<double> Elements { get; }
        public IEnumerable<double> RemainingElements { get; }

        public SliceResult(double elementsSize, IEnumerable<double> elements, IEnumerable<double> remainingElements)
        {
            ElementsSize = elementsSize;
            Elements = elements;
            RemainingElements = remainingElements;
        }
    }

    private class SliceRectangle
    {
        public Slice Slice { get; set; }
        public float X { get; set; }
        public float Y { get; set; }
        public float Width { get; set; }
        public float Height { get; set; }
        public SliceRectangle(Slice slice) => Slice = slice;
        public RectangleF ToRectF() => new(X, Y, Width, Height);
    }

    private static Slice GetSlice(IEnumerable<double> elements, double totalSize, double sliceWidth)
    {
        if (elements.Count() == 1)
            return new Slice(totalSize, elements.Single());

        SliceResult sr = GetElementsForSlice(elements, sliceWidth);
        Slice child1 = GetSlice(sr.Elements, sr.ElementsSize, sliceWidth);
        Slice child2 = GetSlice(sr.RemainingElements, 1 - sr.ElementsSize, sliceWidth);
        return new Slice(totalSize, elements, child1, child2);
    }

    private static SliceResult GetElementsForSlice(IEnumerable<double> elements, double sliceWidth)
    {
        var elementsInSlice = new List<double>();
        var remainingElements = new List<double>();
        double current = 0;
        double total = elements.Sum();

        foreach (var element in elements)
        {
            if (current > sliceWidth)
                remainingElements.Add(element);
            else
            {
                elementsInSlice.Add(element);
                current += element / total;
            }
        }

        return new SliceResult(current, elementsInSlice, remainingElements);
    }

    private static IEnumerable<SliceRectangle> GetRectangles(Slice slice, int width, int height)
    {
        SliceRectangle area = new(slice) { Width = width, Height = height };

        foreach (var rect in GetRectangles(area))
        {
            if (rect.X + rect.Width > area.Width)
                rect.Width = area.Width - rect.X;

            if (rect.Y + rect.Height > area.Height)
                rect.Height = area.Height - rect.Y;

            yield return rect;
        }
    }

    private static IEnumerable<SliceRectangle> GetRectangles(SliceRectangle sliceRectangle)
    {
        var isHorizontalSplit = sliceRectangle.Width >= sliceRectangle.Height;
        var currentPos = 0;
        foreach (var subSlice in sliceRectangle.Slice.Children)
        {
            var subRect = new SliceRectangle(subSlice);
            int rectSize;

            if (isHorizontalSplit)
            {
                rectSize = (int)Math.Round(sliceRectangle.Width * subSlice.Size);
                subRect.X = sliceRectangle.X + currentPos;
                subRect.Y = sliceRectangle.Y;
                subRect.Width = rectSize;
                subRect.Height = sliceRectangle.Height;
            }
            else
            {
                rectSize = (int)Math.Round(sliceRectangle.Height * subSlice.Size);
                subRect.X = sliceRectangle.X;
                subRect.Y = sliceRectangle.Y + currentPos;
                subRect.Width = sliceRectangle.Width;
                subRect.Height = rectSize;
            }

            currentPos += rectSize;

            if (subSlice.Values.Count() > 1)
            {
                foreach (var sr in GetRectangles(subRect))
                {
                    yield return sr;
                }
            }
            else if (subSlice.Values.Count() == 1)
            {
                yield return subRect;
            }
        }
    }
}
```

## Source Code Complexity Analysis

A few days ago I wrote an article describing how to [programmatically generate .NET source code analytics using C#](https://swharden.com/blog/2023-03-05-dotnet-code-analysis/). Using these tools I analyzed the source code for all classes in a large project ([ScottPlot.NET](https://scottplot.net)). The following tree map displays every class in the project as a rectangle sized according to number of lines of code and colored according to maintainability. 

<img src="https://swharden.com/static/2023/03/07/code-report.png" class="shadow">

<img src="https://swharden.com/static/2023/03/07/turbo.png" class="shadow">

In this diagram large rectangles represent classes with the most code, and red color indicates classes that are difficult to maintain. 

> 💡 I'm using a perceptually uniform colormap (similar to [Turbo](https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html))provided by the [ScottPlot](https://scottplot.net) provided by the [ScottPlot](https://scottplot.net) NuGet package. See ScottPlot's [colormaps gallery](https://scottplot.net/cookbook/4.1/colormaps/) for all available colormaps.

> 💡 The [Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning) is a value between 0 (worst) and 100 (best) that represents the relative ease of maintaining the code. It's calculated from a combination of [Halstead complexity](https://en.wikipedia.org/wiki/Halstead_complexity_measures) (size of the compiled code), [Cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) (number of paths that can be taken through the code), and the total number of lines of code.

## Conclusions

* Generation of tree map diagrams can be achieved using recursive programming

* The static class above makes it easy to generate tree maps in C#

* ScottPlot's AxisTicksRender class may be difficult to maintain

## References

* This blog post is spillover from ScottPlot issues [#1479](https://github.com/ScottPlot/ScottPlot/issues/1479) and [#2454](https://github.com/ScottPlot/ScottPlot/issues/2454).

* Code here was heavily influenced by [The Never Ending Journey](http://pascallaurin42.blogspot.com/2013/12/implementing-treemap-in-c.html) (Dec 29, 2013)

* [Treemapping](https://en.wikipedia.org/wiki/Treemapping) (Wikipedia)

* [D3 Treemap](https://d3-graph-gallery.com/treemap.html)

* [Squarified Treemaps](https://www.win.tue.nl/~vanwijk/stm.pdf) (Bruls et al.)

* StackOverflow question [32548949](https://stackoverflow.com/questions/32548949/from-c-sharp-serverside-is-there-anyway-to-generate-a-treemap-and-save-as-an-im/37154938#37154938)

* [C# Data Visualization](https://swharden.com/csdv/)