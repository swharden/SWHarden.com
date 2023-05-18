---
title: Representing Images in Memory
description: quick reference for programmers interested in working with image data in memory (byte arrays)
Date: 2021-06-03 00:03:00
tags: ["csharp"]
---



**This page is a quick reference for programmers interested in working with image data in memory (byte arrays).** This topic is straightforward overall, but there are a few traps that aren't necessarily intuitive so I try my best to highlight those here. 

> 💡 See my newer article, [Creating Bitmaps from Scratch in C#](https://swharden.com/blog/2022-11-04-csharp-create-bitmap/)

This article assumes you have some programming experience working with byte arrays in a C-type language and have an understanding of what is meant by 32-bit, 24-bit, 16-bit, and 8-bit integers.

## Pixel Values

**An image is composed of a 2D grid of square pixels,** and the type of image greatly influences how much memory each pixel occupies and what format its data is in.

**Bits per pixel (bpp)** is the number of bits it takes to represent the value a single pixel. This is typically a multiple of 8 bits (1 byte).

### Common Pixel Formats

* **8-bit (1 byte)  Pixel Formats**
  * **`Gray 8`** - Specifies one of 2^8 (256) shades of gray.
  * **`Indexed 8`** - The pixel data contains color-indexed values, which means the values are an index to colors in the system color table, as opposed to individual color values.
* **16-bit (2-byte) Pixel Formats**
  * **`ARGB 1555`** - Specifies one of 2^15 (32,768) shades of color (5 bits each for red, green, and blue) and 1 bit for alpha.
  * **`Gray 16`** - Specifies one of 2^16 (65,536) shades of gray.
  * **`RGB 555`** - 5 bits each are used for the red, green, and blue components. The remaining bit is not used.
  * **`RGB 565`** - 5 bits are used for the red component, 6 bits are used for the green component, and 5 bits are used for the blue component. The additional green bit doubles the number of gradations and improves image perception in most humans.
* **24-bit (3 byte) Pixel Formats**
  * **`RGB 888`** - 8 bits each are used for the red, green, and blue components.
* **32-bit (4-byte) Pixel Formats**
  * **`ARGB`** - 8 bits each are used for the alpha, red, green, and blue components. This is the most common pixel format.

There are others (e.g., 64-bit RGB images), but these are the most typically encountered pixel formats.

### Endianness

[Endianness](https://en.wikipedia.org/wiki/Endianness) describes the order of bytes in a multi-byte value uses to store its data:

* **big-endian:** the smallest address contains the most significant byte

* **little-endian:** the smallest address contains the least significant byte

Assuming array index values ascend from left to right, 32-bit (4-byte) pixel data can be represented using either of these two formats in memory:

* 4 bpp little-endian: **`[A, B, G, R]`** (most common)

* 4 bpp big-endian: **`[R, G, B, A]`**

**Bitmap images use little-endian integer format!** New programmers may expect the bytes that contain "RGB" values to be sequenced in the order "R, G, B", but this is not the case.

### Premultiplied Alpha

**Premultiplication refers to the relationship between color (R, G, B) and transparency (alpha).** In transparent images the alpha channel may be straight (unassociated) or premultiplied (associated).

With **straight alpha**, the RGB components represent the full-intensity color of the object or pixel, disregarding its opacity. Later R, G, and B will each be multiplied by the alpha to adjust intensity and transparency.

With **premultiplied alpha**, the RGB components represent the emission (color and intensity) of each pixel, and the alpha only represents transparency (occlusion of what is behind it). This reduces the computational performance for image processing if transparency isn't actually used.

**In C# using `System.Drawing` premultiplied alpha is not enabled by default.** This must be defined when creating new `Bitmap` as seen here:

```cs
var bmp = new Bitmap(400, 300, PixelFormat.Format32bppPArgb);
```

**Benchmarking reveals the performance enhancement** of drawing on bitmaps in memory using premultiplied alpha pixel format. In this test I'm using .NET 5 with the [System.Drawing.Common](https://www.nuget.org/packages/System.Drawing.Common) NuGet package. Anti-aliasing is off in this example, but similar results were obtained with it enabled.

```cs
Random rand = new(0);
int width = 600;
int height = 400;
var bmp = new Bitmap(600, 400, PixelFormat.Format32bppPArgb);
var gfx = Graphics.FromImage(bmp);
var pen = new Pen(Color.Black);
gfx.Clear(Color.Magenta);
var sw = Stopwatch.StartNew();
for (int i = 0; i < 1e6; i++)
{
    pen.Color = Color.FromArgb(rand.Next());
    gfx.DrawLine(pen, rand.Next(width), rand.Next(height), rand.Next(width), rand.Next(height));
}
Console.WriteLine(sw.Elapsed);
bmp.Save("benchmark.png", ImageFormat.Png);
```

Time to render 1 million frames:
* Standard ARGB: 6.77 ± 0.02 sec
* Premultiplied ARGB: 5.83 ± 0.03 sec (14% faster)

At the end you have a beautiful figure:

<div class="text-center img-border">

![](https://swharden.com/static/2021/06/03/benchmark.png)

</div>

## Pixel Locations in Space and Memory

**A 2D image is composed of pixels, but addressing them in memory isn't as trivial as it may seem.** The dimensions of bitmaps are stored in their header, and the arrangement of pixels forms rows (left-to-right) then columns (top-to-bottom). 

**Width** and **height** are the dimensions (in pixels) of the visible image, but...

⚠️ **Image size in memory is _not_ just `width * height * bytesPerPixel`**

Because of old hardware limitations, bitmap widths _in memory_ (also called the **stride**) must be multiplies of 4 bytes. This is effortless when using ARGB formats because each pixel is already 4 bytes, but when working with RGB images it's possible to have images with an odd number of bytes in each row, requiring data to be **padded** such that the stride length is a multiple of 4.

<div class="text-center">

![](https://swharden.com/static/2021/06/03/image-byte-position.png)

</div>

```cs
// calculate stride length of a bitmap row in memory
int stride = 4 * ((imageWidth * bytesPerPixel + 3) / 4);
```

### Working with Bitmap Bytes in C# 

**This example demonstrates how to convert a 3D array (X, Y, C) into a flat byte array ready for copying into a bitmap.** Notice this code adds padding to the image width to ensure the stride is a multiple of 4 bytes. Notice also the integer encoding is little endian.

```cs
public static byte[] GetBitmapBytes(byte[,,] input)
{
    int height = input.GetLength(0);
    int width = input.GetLength(1);
    int bpp = input.GetLength(2);
    int stride = 4 * ((width * bpp + 3) / 4);

    byte[] pixelsOutput = new byte[height * stride];
    byte[] output = new byte[height * stride];

    for (int y = 0; y < height; y++)
        for (int x = 0; x < width; x++)
            for (int z = 0; z < bpp; z++)
                output[y * stride + x * bpp + (bpp - z - 1)] = input[y, x, z];

    return output;
}
```

For completeness, here's the complimentary code that converts a flat byte array from bitmap memory to a 3D array (assuming we know the image dimensions and bytes per pixel from reading the image header):

```cs
public static byte[,,] GetBitmapBytes3D(byte[] input, int width, int height, int bpp)
{
    int stride = 4 * ((width * bpp + 3) / 4);

    byte[,,] output = new byte[height, width, bpp];
    for (int y = 0; y < height; y++)
        for (int x = 0; x < width; x++)
            for (int z = 0; z < bpp; z++)
                output[y, x, z] = input[stride * y + x * bpp + (bpp - z - 1)];

    return output;
}
```

### Marshalling Bytes in and out of Bitmaps

The code examples above are intentionally simple to focus on the location of pixels in memory and the endianness of their values. To actually convert between `byte[]` and `System.Drawing.Bitmap` you must use `Marshall.Copy` as shown:

```cs
public static byte[] BitmapToBytes(Bitmap bmp)
{
    Rectangle rect = new(0, 0, bmp.Width, bmp.Height);
    BitmapData bmpData = bmp.LockBits(rect, ImageLockMode.ReadWrite, bmp.PixelFormat);
    int byteCount = Math.Abs(bmpData.Stride) * bmp.Height;
    byte[] bytes = new byte[byteCount];
    Marshal.Copy(bmpData.Scan0, bytes, 0, byteCount);
    bmp.UnlockBits(bmpData);
    return bytes;
}
```

```cs
public static Bitmap BitmapFromBytes(byte[] bytes, PixelFormat bmpFormat)
{
    Bitmap bmp = new(width, height, bmpFormat);
    var rect = new Rectangle(0, 0, width, height);
    BitmapData bmpData = bmp.LockBits(rect, ImageLockMode.ReadOnly, bmpFormat);
    Marshal.Copy(bytes, 0, bmpData.Scan0, bytes.Length);
    bmp.UnlockBits(bmpData);
    return bmp;
}
```

## How to Create a Bitmap in Memory Without a Graphics Library

The code examples above use `System.Drawing.Common` to create graphics, but creating bitmaps in a `byte[]` array is not difficult and can be done in any language. See the [Creating Bitmaps from Scratch](https://swharden.com/blog/2022-11-04-csharp-create-bitmap/) article for more information.

* https://swharden.com/blog/2022-11-04-csharp-create-bitmap/

## Reference
* [Array to Image with System.Drawing](https://swharden.com/csdv/system.drawing/array-to-image/)
* [C# Data Visualization: Resources for visualizing data using C# and the .NET platform](https://swharden.com/csdv/)
* [A programmer's view on digital images: the essentials](https://www.collabora.com/news-and-blog/blog/2016/02/16/a-programmers-view-on-digital-images-the-essentials/)
* [Microsoft: `System.Drawing.PixelFormat` Enumeration](https://docs.microsoft.com/en-us/dotnet/api/system.drawing.imaging.pixelformat?view=net-5.0) - describes pixel formats supported by this common drawing library
* [Creighton University: Tip of the week (June 2014) - ](https://medschool.creighton.edu/fileadmin/user/medicine/Departments/Biomedical_Sciences/CUIBIF/Tip_of_the_week/June_2014/4096_Shades_of_Gray.pdf) inspired the title of this article.
* [8, 12, 14 vs 16-Bit Depth: What Do You Really Need?!](https://petapixel.com/2018/09/19/8-12-14-vs-16-bit-depth-what-do-you-really-need/)
* [Premultiplied alpha](https://shawnhargreaves.com/blog/premultiplied-alpha.html) by Shawn Hargreaves (2009)
* [Straight versus premultiplied alpha](https://en.wikipedia.org/wiki/Alpha_compositing#Straight_versus_premultiplied) on Wikipedia
* [Creating Bitmaps from Scratch](https://swharden.com/blog/2022-11-04-csharp-create-bitmap/) 
