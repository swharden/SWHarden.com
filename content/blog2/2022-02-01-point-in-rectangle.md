---
title: Point Inside Rectangle
description: How to determine if a point is inside a rotated rectangle with C#
Date: 2022-02-01 00:10:00
tags: ["csharp", "graphics"]
---



**I recently had the need to determine if a point is inside a rotated rectangle.** This need arose when I wanted to make a rotated rectangular textbox draggable, but I wanted to determine if the mouse was over the rectangle. I know the rectangle's location, size, and rotation, and the position of the mouse cursor, and my goal is to tell if the mouse is inside the rotated rectangle. In this example I'll use [`Maui.Graphics`](https://maui.graphics) to render a test image in a Windows Forms application (with SkiaSharp and OpenGL), but the same could be achieved with `System.Drawing` or other similar 2D graphics libraries.

<div class="text-center">

![](https://swharden.com/static/2022/02/01/point-inside-rotated-rectangle.gif)

</div>

I started just knowing the width and height of my rectangle. I created an array of points representing its corners.

```cs
float rectWidth = 300;
float rectHeight = 150;

PointF[] rectCorners =
{
    new(0, 0),
    new(rectWidth, 0),
    new(rectWidth, rectHeight),
    new(0, rectHeight),
};
```

I then rotated the rectangle around an origin point by applying a rotation transformation to each corner.

```cs
PointF origin = new(200, 300); // center of rotation
double angleRadians = 1.234;
PointF[] rotatedCorners = rectCorners.Select(x => Rotate(origin, x, angleRadians)).ToArray();
```

```cs
private PointF Rotate(PointF origin, PointF point, double radians)
{
	double dx = point.X * Math.Cos(radians) - point.Y * Math.Sin(radians);
	double dy = point.X * Math.Sin(radians) + point.Y * Math.Cos(radians);
	return new PointF(origin.X + (float)dx, origin.Y + (float)dy);
}
```

To determine if a given point is inside the rotated rectangle I called this method which accepts the point of interest and an array containing the four corners of the rotated rectangle.

```cs
public bool IsPointInsideRectangle(PointF pt, PointF[] rectCorners)
{
    double x1 = rectCorners[0].X;
    double x2 = rectCorners[1].X;
    double x3 = rectCorners[2].X;
    double x4 = rectCorners[3].X;

    double y1 = rectCorners[0].Y;
    double y2 = rectCorners[1].Y;
    double y3 = rectCorners[2].Y;
    double y4 = rectCorners[3].Y;

    double a1 = Math.Sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
    double a2 = Math.Sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3));
    double a3 = Math.Sqrt((x3 - x4) * (x3 - x4) + (y3 - y4) * (y3 - y4));
    double a4 = Math.Sqrt((x4 - x1) * (x4 - x1) + (y4 - y1) * (y4 - y1));

    double b1 = Math.Sqrt((x1 - pt.X) * (x1 - pt.X) + (y1 - pt.Y) * (y1 - pt.Y));
    double b2 = Math.Sqrt((x2 - pt.X) * (x2 - pt.X) + (y2 - pt.Y) * (y2 - pt.Y));
    double b3 = Math.Sqrt((x3 - pt.X) * (x3 - pt.X) + (y3 - pt.Y) * (y3 - pt.Y));
    double b4 = Math.Sqrt((x4 - pt.X) * (x4 - pt.X) + (y4 - pt.Y) * (y4 - pt.Y));

    double u1 = (a1 + b1 + b2) / 2;
    double u2 = (a2 + b2 + b3) / 2;
    double u3 = (a3 + b3 + b4) / 2;
    double u4 = (a4 + b4 + b1) / 2;

    double A1 = Math.Sqrt(u1 * (u1 - a1) * (u1 - b1) * (u1 - b2));
    double A2 = Math.Sqrt(u2 * (u2 - a2) * (u2 - b2) * (u2 - b3));
    double A3 = Math.Sqrt(u3 * (u3 - a3) * (u3 - b3) * (u3 - b4));
    double A4 = Math.Sqrt(u4 * (u4 - a4) * (u4 - b4) * (u4 - b1));

    double difference = A1 + A2 + A3 + A4 - a1 * a2;
    return difference < 1;
}
```

## How does it work?

Consider 4 triangles formed by lines between the point and the 4 corners...

**If the point is _inside_ the rectangle,** the area of the four triangles will _equal_ the area of the rectangle.

<div class="text-center">

![](https://swharden.com/static/2022/02/01/rectangle-point-inside.png)

</div>

**If the point is _outside_ the rectangle,** the area of the four triangles will be _greater_ than the area of the rectangle.

<div class="text-center">

![](https://swharden.com/static/2022/02/01/rectangle-point-outside.png)

</div>

**The code above calculates the area of the 4 rectangles** and returns `true` if it is approximately equal to the area of the rectangle.

## Notes

* In practice you'll probably want to use a more intelligent data structure than a 4-element `Pointf[]` when calling these functions.

* The points in the array are clockwise, but I assume this method will work regardless of the order of the points in the array.

* At the very end of `IsPointInsideRectangle()` the final decision is made based on a distance being less than a given value. It's true that the cursor will be inside the rectangle if the distance is exactly zero, but with the possible accumulation of floating-point math errors this seemed like a safer option.

## Resources
* Source code for this application: [Form1.cs](https://github.com/swharden/Csharp-Data-Visualization/blob/203e024253a2545fc325d1f68d2861a1b9fac74d/projects/rotated-rectangle-intersection/Form1.cs)

* Thanks [@BambOoxX](https://github.com/BambOoxX) for suggesting this in [ScottPlot/PR#1616](https://github.com/ScottPlot/ScottPlot/pull/1616)

* [How to check if a point is inside a rectangle?](https://math.stackexchange.com/q/190403) (StackExchange)

* [swharden / C# Data Visualization](https://github.com/swharden/Csharp-Data-Visualization)