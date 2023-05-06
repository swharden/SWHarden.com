---
Title: Draw with Maui.Graphics and Skia in a C# Console Application
Description: This page describes how to draw graphics in a console application with Maui Graphics and Skia
Date: 2021-08-01 19:15:00
tags: ["csharp", "maui"]
---

# Draw with Maui.Graphics and Skia in a C# Console Application

**Microsoft's `System.Drawing.Common` package is commonly used for cross-platform graphics in .NET Framework and .NET Core applications, but according to the dotnet roadmap [System.Drawing will soon only support Windows](https://github.com/dotnet/designs/blob/main/accepted/2021/system-drawing-win-only/system-drawing-win-only.md).** As Microsoft sunsets cross-platform support for `System.Drawing` they will be simultaneously developing [`Microsoft.Maui.Graphics`](https://github.com/dotnet/Microsoft.Maui.Graphics), a cross-platform graphics library for iOS, Android, Windows, macOS, Tizen and Linux completely in C#.

**The `Maui.Graphics` library can be used in any .NET application (not just MAUI applications).** This page documents how I used the Maui.Drawing package to render graphics in memory (using a Skia back-end) and save them as static images from a console application.

**I predict `Maui.Graphics` will eventually evolve to overtake `System.Drawing` in utilization.** It has many advantages for performance and memory management (discussed extensively elsewhere on the internet), but it is still early in development. As of today (July 2021) [the Maui.Graphics GitHub page](https://github.com/dotnet/Microsoft.Maui.Graphics) warns "This is an experimental library ... There is no official support. Use at your own Risk."

<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
  </symbol>
  <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
  </symbol>
  <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
  </symbol>
</svg>

<div class="alert alert-primary d-flex align-items-center" role="alert">
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>
  <div>
    <strong>UPDATE:</strong> This article was written when <code>Microsoft.Maui.Graphics</code> was still in preview. See <a href="https://swharden.com/blog/2022-05-25-maui-graphics/" class="fw-bold">Drawing with Maui Graphics (blog post)</a> and <a href="https://swharden.com/csdv/" class="fw-bold">C# Data Visualization (website)</a> for updated code examples and information about using this library.
  </div>
</div>

## Maui Graphics Skia Console Quickstart

This program will create an image, fill it with blue, add 1,000 random lines, then draw some text. It is written as a .NET 5 top-level console application and requires the [Microsoft.Maui.Graphics](https://www.nuget.org/packages/Microsoft.Maui.Graphics) and [Microsoft.Maui.Graphics.Skia](https://www.nuget.org/packages/Microsoft.Maui.Graphics.Skia) NuGet packages (both are currently in preview). 

We use SkiaSharp to create a canvas, but importantly that canvas implements `Microsoft.Maui.Graphics.ICanvas` (it's not Skia-specific) so all the methods that draw on it can be agnostic to which rendering system was used. This makes it easy to write generic rendering methods now and have the option to switch the rendering system later.

<div class="text-center">

![](maui-graphics-quickstart.jpg)

</div>

### Program.cs
```cs
using System;
using System.IO;
using Microsoft.Maui.Graphics;
using Microsoft.Maui.Graphics.Skia;

// Use Skia to create a Maui graphics context and canvas
BitmapExportContext bmpContext = SkiaGraphicsService.Instance.CreateBitmapExportContext(600, 400);
SizeF bmpSize = new(bmpContext.Width, bmpContext.Height);
ICanvas canvas = bmpContext.Canvas;

// Draw on the canvas with abstract methods that are agnostic to the renderer
ClearBackground(canvas, bmpSize, Colors.Navy);
DrawRandomLines(canvas, bmpSize, 1000);
DrawBigTextWithShadow(canvas, "This is Maui.Graphics with Skia");
SaveFig(bmpContext, Path.GetFullPath("quickstart.jpg"));

static void ClearBackground(ICanvas canvas, SizeF bmpSize, Color bgColor)
{
    canvas.FillColor = Colors.Navy;
    canvas.FillRectangle(0, 0, bmpSize.Width, bmpSize.Height);
}

static void DrawRandomLines(ICanvas canvas, SizeF bmpSize, int count = 1000)
{
    Random rand = new();
    for (int i = 0; i < count; i++)
    {
        canvas.StrokeSize = (float)rand.NextDouble() * 10;

        canvas.StrokeColor = new Color(
            red: (float)rand.NextDouble(),
            green: (float)rand.NextDouble(),
            blue: (float)rand.NextDouble(),
            alpha: .2f);

        canvas.DrawLine(
            x1: (float)rand.NextDouble() * bmpSize.Width,
            y1: (float)rand.NextDouble() * bmpSize.Height,
            x2: (float)rand.NextDouble() * bmpSize.Width,
            y2: (float)rand.NextDouble() * bmpSize.Height);
    }
}

static void DrawBigTextWithShadow(ICanvas canvas, string text)
{
    canvas.FontSize = 36;
    canvas.FontColor = Colors.White;
    canvas.SetShadow(offset: new SizeF(2, 2), blur: 1, color: Colors.Black);
    canvas.DrawString(text, 20, 50, HorizontalAlignment.Left);
}

static void SaveFig(BitmapExportContext bmp, string filePath)
{
    bmp.WriteToFile(filePath);
    Console.WriteLine($"WROTE: {filePath}");
}
```

### MauiGraphicsDemo.csproj
```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net5.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Maui.Graphics" Version="6.0.100-preview.6.299" />
    <PackageReference Include="Microsoft.Maui.Graphics.Skia" Version="6.0.100-preview.6.299" />
  </ItemGroup>

</Project>
```

## Resources
* [Animated Rendering with SkiaSharp and OpenGL](https://swharden.com/CsharpDataVis/)
* [Microsoft.Maui.Graphics on GitHub](https://github.com/dotnet/Microsoft.Maui.Graphics)
* [Microsoft.Maui.Graphics on NuGet](https://www.nuget.org/packages/Microsoft.Maui.Graphics/)
* [SkiaSharp Graphics in Xamarin.Forms](https://docs.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/graphics/skiasharp/)
* [Maui.Graphics](https://maui.graphics)