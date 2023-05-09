---
title: Working with 16-bit Images in CSharp
description: A summary of how I work with 16-bit TIF file data in C# (using ImageMagick and LibTiff).
Date: 2021-06-08 23:00:00
tags: ["csharp"]
---



**Scientific image analysis frequently involves working with 12-bit and 14-bit sensor data stored in 16-bit TIF files.** Images commonly encountered on the internat are 24-bit or 32-bit RGB images (where each pixel is represented by 8 bits each for red, green, blue, and possibly alpha). Typical image analysis libraries and documentation often lack information about how to work with 16-bit image data. 

**This page summarizes how I work with 16-bit TIF file data in C#.** I prefer [Magick.NET](https://www.nuget.org/packages?q=magick) (an ImageMagick wrapper) when working with many different file formats, and [LibTiff.Net](https://bitmiracle.com/libtiff) whenever I know my source files will all be identically-formatted TIFs or multidimensional TIFs (stacks).

[](https://github.com/swharden/Csharp-Image-Analysis/blob/main/dev/notes.md)

## ImageMagick

[ImageMagick](https://imagemagick.org/index.php) is a free and open-source cross-platform software suite for displaying, creating, converting, modifying, and editing raster images. Although ImageMagick is commonly used at the command line, .NET wrappers exist to make it easy to use ImageMagick from within C# applications.

ImageMagick has [many packages on NuGet](https://www.nuget.org/packages?q=imagemagick) and they are described on ImageMagick's [documentation](https://github.com/dlemstra/Magick.NET/tree/main/docs) GitHub page. **TLDR: Install the Q16 package (not HDRI)** to allow you to work with 16-bit data without losing precision.

ImageMagick is free and distributed under the Apache 2.0 license, so it can easily be used in commercial projects.

An advantage of loading images with ImageMagick is that it will work easily whether the source file is a JPG, PNG, GIF, TIF, or something different. ImageMagick supports over 100 file formats!

### Load a 16-bit TIF File as a Pixel Value Array

```cs
// Load pixel values from a 16-bit TIF using ImageMagick (Q16)
MagickImage image = new MagickImage("16bit.tif");
ushort[] pixelValues = image.GetPixels().GetValues();
```

That's it! The `pixelValues` array will contain one value per pixel from the original image. The length of this array will equal the image's height times its width.

### Load an 8-bit TIF File as a Pixel Value Array
Since the `Q16` package was installed, 2 bytes will be allocated for each pixel (16-bit) even if it only requires one byte (8-bit). In this case you must collect just the bytes you are interested in:

```cs
MagickImage image = new MagickImage("8bit.tif");
ushort[] pixelValues = image.GetPixels().GetValues();
int[] values8 = Enumerable.Range(0, pixelValues.Length / 2).Select(x => (int)pixelValues[x * 2 + 1]).ToArray();
```

### Load a 32-bit TIF File as a Pixel Value Array

For this you'll have to install the high dynamic range (HDRI) Q16 package, then your `GetValues()` method will return a `float[]` instead of a `ushort[]`. Convert these values to proper pixel intensity values by dividing by 2^16.

```cs
MagickImage image = new MagickImage("32bit.tif");
float[] pixels = image.GetPixels().GetValues();
for (int i = 0; i < pixels.Length; i++)
    pixels[i] = (long)pixels[i] / 65535;
```

## LibTiff

**LibTiff is a pure C# (.NET Standard) TIF file reader.** Although it doesn't support all the image formats that ImageMagick does, it's really good at working with TIFs. It has a more intuitive interface for working with TIF-specific features such as multi-dimensional images (color, Z position, time, etc.). 

LibTiff gives you a lower-level access to the bytes that underlie image data, so it's on you to perform the conversion from a byte array to the intended data type. Note that some TIFs are little-endian encoded and others are big-endian encoded, and endianness can be read from the header.

LibTiff is distributed under a BSD 3-clause license, so it too can be easily used in commercial projects.

### Load a 16-bit TIF as a Pixel Value Array

```cs
// Load pixel values from a 16-bit TIF using LibTiff
using Tiff image = Tiff.Open("16bit.tif", "r");

// get information from the header
int width = image.GetField(TiffTag.IMAGEWIDTH)[0].ToInt();
int height = image.GetField(TiffTag.IMAGELENGTH)[0].ToInt();
int bytesPerPixel = image.GetField(TiffTag.BITSPERSAMPLE)[0].ToInt() / 8;

// read the image data bytes
int numberOfStrips = image.NumberOfStrips();
byte[] bytes = new byte[numberOfStrips * image.StripSize()];
for (int i = 0; i < numberOfStrips; ++i)
    image.ReadRawStrip(i, bytes, i * image.StripSize(), image.StripSize());

// convert the data bytes to a double array
if (bytesPerPixel != 2)
    throw new NotImplementedException("this is only for 16-bit TIFs");
double[] data = new double[bytes.Length / bytesPerPixel];
for (int i = 0; i < data.Length; i++)
{
    if (image.IsBigEndian())
        data[i] = bytes[i * 2 + 1] + (bytes[i * 2] << 8);
    else
        data[i] = bytes[i * 2] + (bytes[i * 2 + 1] << 8);
}
```

Routines for detecting and converting data from 8-bit, 24-bit, and 32-bit TIF files can be created by inspecting `bytesPerPixel`. LibTiff has [documentation](https://bitmiracle.com/libtiff/) describing how to work with RGB TIF files and multi-frame TIFs.

## Convert a Pixel Array to a 2D Array

I often prefer to work with scientific image data as a 2D arrays of `double` values. I write my analysis routines to pass `double[,]` between methods so the file I/O can be encapsulated in a static class.

```cs
// Load pixel values from a 16-bit TIF using ImageMagick (Q16)
MagickImage image = new MagickImage("16bit.tif");
ushort[] pixelValues = image.GetPixels().GetValues();

// create a 2D array of pixel values
double[,] imageData = new double[image.Height, image.Width];
for (int i = 0; i < image.Height; i++)
    for (int j = 0; j < image.Width; j++)
        imageData[i, j] = pixelValues[i * image.Width + j];
```

## Other Libraries

### ImageProcessor

According to [ImageProcessor's GitHub page](https://github.com/JimBobSquarePants/ImageProcessor), "ImageProcessor is, and will **only ever be supported on the .NET Framework running on a Windows OS**" ... it doesn't appear to be actively maintained and is effectively labeled as deprecated, so I won't spend much time looking further into it.

### ImageSharp

As of the time of writing, [ImageSharp](https://docs.sixlabors.com/articles/imagesharp/imageformats.html) does not support TIF format, but it appears likely to be supported in a future release.

### System.Drawing

Although this library can _save_ images at different depths, it can only _load_ image files with 8-bit depths. System.Drawing does not support loading 16-bit TIFs, so another library must be used to work with these file types.

## Resources

* [C# Image Analysis](https://github.com/swharden/Csharp-Image-Analysis) (GitHub) - a collection of code examples for working with image data as 2D arrays
* [LibTiff.Net](https://bitmiracle.com/libtiff/) - The .NET version of original libtiff library
* [dlemstra/Magick.NET](https://github.com/dlemstra/Magick.NET) - The .NET library for ImageMagick
* [ImageSharp](https://docs.sixlabors.com/articles/imagesharp/imageformats.html) - Supported image formats