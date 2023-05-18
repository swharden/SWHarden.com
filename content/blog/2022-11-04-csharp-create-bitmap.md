---
title: Creating Bitmaps from Scratch in C#
description: How to create a bitmap and set pixel colors in memory and save the result to disk or convert it to a traditional image format
Date: 2022-11-07 18:45:00
tags: ["csharp", "graphics"]
---

**This project how to represent bitmap data in a plain old C object (POCO) to create images from scratch using C# and no dependencies.** 
Common graphics libraries like [SkiaSharp](https://swharden.com/csdv/skiasharp/), [ImageSharp](https://swharden.com/csdv/platforms/imagesharp/), [System.Drawing](https://swharden.com/csdv/system.drawing/), and [Maui.Graphics](https://swharden.com/csdv/maui.graphics/) can read and write bitmaps in memory, so a [POCO](https://en.wikipedia.org/wiki/POCO) that stores image data and converts it to a bitmap byte allows creation of platform-agnostic APIs that can be interfaced from any graphics library.

**This page demonstrates how to use C# (.NET 6.0) to create bitmap images from scratch.** Bitmap images can then be saved to disk and viewed with any image editing program, or they can consumed as a byte array in memory by a graphics library. There are various [bitmap image formats](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/advanced/types-of-bitmaps?view=netframeworkdesktop-4.8) (grayscale, indexed colors, 16-bit, 32-bit, transparent, etc.) but code here demonstrates the simplest common case (8-bit RGB color).

## Representing Color

The following `struct` represents RGB color as 3 `byte` values and has helper methods for creating new colors. 

```cs
public struct RawColor
{
    public readonly byte R, G, B;

    public RawColor(byte r, byte g, byte b)
    {
        (R, G, B) = (r, g, b);
    }

    public static RawColor Random(Random rand)
    {
        byte r = (byte)rand.Next(256);
        byte g = (byte)rand.Next(256);
        byte b = (byte)rand.Next(256);
        return new RawColor(r, g, b);
    }

    public static RawColor Gray(byte value)
    {
        return new RawColor(value, value, value);
    }
}
```

A color class like this could be extended to support additional niceties. Refer to [SkiaSharp's `SKColor.cs`](https://github.com/mono/SkiaSharp/blob/main/binding/Binding/SKColor.cs), [System.Drawing's `Color.cs`](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Drawing.Primitives/src/System/Drawing/Color.cs), and [Maui.Graphics' `Color.cs`](https://github.com/dotnet/maui/blob/main/src/Graphics/src/Graphics/Color.cs) for examples and implementation details. I commonly find the following features useful include when writing a color class:

* A static class with named colors e.g., `RawColors.Blue`
* Conversion to/from ARGB e.g., `RawColor.FromAGRB(123456)`
* Conversion to/from HTML e.g., `RawColor.FromHtml(#003366)`
* Conversion between RGB and [HSL/HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)
* Helper functions to `Lighten()` and `Darken()`
* Helper functions to `ShiftHue()`
* Extension methods to convert to common other formats like `SKColor`

## Representing the Bitmap Image

This is the entire image class and it serves a few specific roles:

* Store image data in a byte array arranged identically to how it will be exported in the bitmap
* Provide helper methods to get/set pixel color
* Provide a method to return the image as a bitmap by adding a minimal header

```cs
public class RawBitmap
{
    public readonly int Width;
    public readonly int Height;
    private readonly byte[] ImageBytes;

    public RawBitmap(int width, int height)
    {
        Width = width;
        Height = height;
        ImageBytes = new byte[width * height * 4];
    }

    public void SetPixel(int x, int y, RawColor color)
    {
        int offset = ((Height - y - 1) * Width + x) * 4;
        ImageBytes[offset + 0] = color.B;
        ImageBytes[offset + 1] = color.G;
        ImageBytes[offset + 2] = color.R;
    }

    public byte[] GetBitmapBytes()
    {
        const int imageHeaderSize = 54;
        byte[] bmpBytes = new byte[ImageBytes.Length + imageHeaderSize];
        bmpBytes[0] = (byte)'B';
        bmpBytes[1] = (byte)'M';
        bmpBytes[14] = 40;
        Array.Copy(BitConverter.GetBytes(bmpBytes.Length), 0, bmpBytes, 2, 4);
        Array.Copy(BitConverter.GetBytes(imageHeaderSize), 0, bmpBytes, 10, 4);
        Array.Copy(BitConverter.GetBytes(Width), 0, bmpBytes, 18, 4);
        Array.Copy(BitConverter.GetBytes(Height), 0, bmpBytes, 22, 4);
        Array.Copy(BitConverter.GetBytes(32), 0, bmpBytes, 28, 2);
        Array.Copy(BitConverter.GetBytes(ImageBytes.Length), 0, bmpBytes, 34, 4);
        Array.Copy(ImageBytes, 0, bmpBytes, imageHeaderSize, ImageBytes.Length);
        return bmpBytes;
    }

    public void Save(string filename)
    {
        byte[] bytes = GetBitmapBytes();
        File.WriteAllBytes(filename, bytes);
    }
}
```

## Generate Images from Scratch

The following code uses the bitmap class and color struct above to create test images

### Random Colors

```cs
RawBitmap bmp = new(400, 300);
Random rand = new();
for (int x = 0; x < bmp.Width; x++)
    for (int y = 0; y < bmp.Height; y++)
        bmp.SetPixel(x, y, RawColor.Random(rand));
bmp.Save("random-rgb.bmp");
```

![](https://swharden.com/static/2022/11/04/SkiaSharp-random-rgb.jpg)

### Rainbow
```cs
RawBitmap bmp = new(400, 300);
Random rand = new();
for (int x = 0; x < bmp.Width; x++)
{
    for (int y = 0; y < bmp.Height; y++)
    {
        byte r = (byte)(255.0 * x / bmp.Width);
        byte g = (byte)(255.0 * y / bmp.Height);
        byte b = (byte)(255 - 255.0 * x / bmp.Width);
        RawColor color = new(r, g, b);
        bmp.SetPixel(x, y, color);
    }
}
bmp.Save("rainbow.bmp");
```

![](https://swharden.com/static/2022/11/04/SkiaSharp-rainbow.jpg)

### Rectangles
```cs
RawBitmap bmp = new(400, 300);
Random rand = new();
for (int i = 0; i < 1000; i++)
{
    int rectX = rand.Next(bmp.Width);
    int rectY = rand.Next(bmp.Height);
    int rectWidth = rand.Next(50);
    int rectHeight = rand.Next(50);
    RawColor color = RawColor.Random(rand);

    for (int x = rectX; x < rectX + rectWidth; x++)
    {
        for (int y = rectY; y < rectY + rectHeight; y++)
        {
            if (x < 0 || x >= bmp.Width) continue;
            if (y < 0 || y >= bmp.Height) continue;
            bmp.SetPixel(x, y, color);
        }
    }
}
bmp.Save("rectangles.bmp");
```

![](https://swharden.com/static/2022/11/04/SkiaSharp-rectangles.jpg)

## Drawing Operations

The following functions can be added to the `RawBitmap` class to add drawing common operations

### Draw Line

Here's a simple (not optimized) method for drawing lines. Users interested in high quality drawing methods will find [Bresenham's line algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm) and [Bresenham's circle algorithm](https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/) useful. There's also [A Rasterizing Algorithm for Drawing Curves](http://members.chello.at/~easyfilter/Bresenham.pdf) which has extensive information about anti-aliasing and drawing Bézier splines.

```cs
public void DrawLine(int x1, int y1, int x2, int y2, Color color)
{
    int xMin = Math.Min(x1, x2);
    int xMax = Math.Max(x1, x2);
    int yMin = Math.Min(y1, y2);
    int yMax = Math.Max(y1, y2);

    int xSpan = xMax - xMin;
    int ySpan = yMax - yMin;

    if (xSpan == 0)
    {
        for (int y = yMin; y <= yMax; y++)
            SetPixel(xMin, y, color);
    }
    else if (ySpan == 0)
    {
        for (int x = xMin; x <= xMax; x++)
            SetPixel(x, yMin, color);
    }
    else if (ySpan > xSpan)
    {
        for (int y = yMin; y <= yMax; y++)
        {
            double frac = (y - yMin) / (double)ySpan;
            if (y2 < y1)
                frac = 1 - frac;
            int x = (int)(frac * xSpan + xMin);
            SetPixel(x, y, color);
        }
    }
    else
    {
        for (int x = xMin; x <= xMax; x++)
        {
            double frac = (x - xMin) / (double)xSpan;
            if (x2 < x1)
                frac = 1 - frac;
            int y = (int)(frac * ySpan + yMin);
            SetPixel(x, y, color);
        }
    }
}
```

### Draw Rectangle
```cs
public void DrawRect(Rectangle rect, Color color)
{
    DrawLine(rect.Left, rect.Top, rect.Right, rect.Top, color);
    DrawLine(rect.Right, rect.Top, rect.Right, rect.Bottom, color);
    DrawLine(rect.Right, rect.Bottom, rect.Left, rect.Bottom, color);
    DrawLine(rect.Left, rect.Bottom, rect.Left, rect.Top, color);
}
```

### Fill Rectangle

```cs
public void FillRect(Rectangle rect, Color color)
{
    for (int y = rect.YMin; y < rect.YMax; y++)
    {
        for (int x = rect.XMin; x < rect.XMax; x++)
        {
            SetPixel(x, y, color);
        }
    }
}
```

## Interfacing Graphics Libraries

**The following code demonstrates how to load the bitmap byte arrays generated above into common graphics libraries and save the result as a JPEG file.** Although the bitmap byte array can be written directly to disk as a .bmp file, these third-party libraries are required to encode images in additional formats like JPEG.


### System.Drawing

```cs
using System.Drawing;

static void SaveBitmap(byte[] bytes, string filename = "demo.jpg")
{
    using MemoryStream ms = new(bytes);
    using Image img = Bitmap.FromStream(ms);
    img.Save(filename);
}
```

### SkiaSharp

```cs
using SkiaSharp;

static void SaveBitmap(byte[] bytes, string filename = "demo.jpg")
{
    using SKBitmap bmp = SKBitmap.Decode(bytes);
    using SKFileWStream fs = new(filename);
    bmp.Encode(fs, SKEncodedImageFormat.Jpeg, quality: 95);
}
```

### ImageSharp

```cs
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats.Jpeg;

static void SaveBitmap(byte[] bytes, string filename = "demo.jpg")
{
    using Image img = Image.Load(bytes);
    JpegEncoder encoder = new() { Quality = 95 };
    img.Save(filename, encoder);
}
```

# Resources

* [C# Data Visualization](https://swharden.com/csdv/) - Resources for visualizing data using C# and the .NET platform

* [SkiaSharp: `SKColor.cs`](https://github.com/mono/SkiaSharp/blob/main/binding/Binding/SKColor.cs)

* [System.Drawing: `Color.cs`](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Drawing.Primitives/src/System/Drawing/Color.cs)

* [Maui.Graphics: `Color.cs`](https://github.com/dotnet/maui/blob/main/src/Graphics/src/Graphics/Color.cs)

* [Bresenham's line algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm) 

* [Bresenham's circle algorithm](https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/) 

* [A Rasterizing Algorithm for Drawing Curves](http://members.chello.at/~easyfilter/Bresenham.pdf) by Alois Zingl
