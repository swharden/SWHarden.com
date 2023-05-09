---
title: MeasureString() with Maui.Graphics
description: How to measure the pixel dimensions of a string using Microsoft.Maui.Graphics
Date: 2021-10-16 16:15:00
tags: ["csharp", "maui", "graphics"]
---



Starting with .NET 6 Microsoft is [sunsetting cross-platform support](https://github.com/dotnet/designs/blob/main/accepted/2021/system-drawing-win-only/system-drawing-win-only.md) for [`System.Drawing.Common`](https://www.nuget.org/packages/System.Drawing.Common/). [`Microsoft.Maui.Graphics`](https://github.com/dotnet/Microsoft.Maui.Graphics) is emerging as an excellent replacement and it can be used in any app (not just MAUI apps).

Code here demonstrates how I measure the pixel size of a string using `Maui.Graphics` in a console application.


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
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="https://swharden.com/static/2021/10/16/#info-fill"/></svg>
  <div>
    <strong>UPDATE:</strong> This article was written when <code>Microsoft.Maui.Graphics</code> was still in preview. See <a href="https://swharden.com/blog/2022-05-25-maui-graphics/" class="fw-bold">Drawing with Maui Graphics (blog post)</a> and <a href="https://swharden.com/csdv/" class="fw-bold">C# Data Visualization (website)</a> for updated code examples and information about using this library.
  </div>
</div>

```cs
/* Updated on 2022-02-19 */
using Microsoft.Maui.Graphics; // 6.0.200-preview.13.935
using Microsoft.Maui.Graphics.Skia; // 6.0.200-preview.13.935

// setup a canvas with a blue background
using BitmapExportContext bmp = new SkiaBitmapExportContext(450, 150, 1.0f);
ICanvas canvas = bmp.Canvas;
canvas.FillColor = Colors.Navy;
canvas.FillRectangle(0, 0, bmp.Width, bmp.Height);

// define and measure a string
PointF stringLocation = new(50, 50);
string stringText = "Hello, Maui.Graphics!";
Font font = new();
float fontSize = 32;
SizeF stringSize = canvas.GetStringSize(stringText, font, fontSize);
Rectangle stringRect = new(stringLocation, stringSize);

// draw the string and its outline
canvas.StrokeColor = Colors.White;
canvas.DrawRectangle(stringRect);
canvas.FontColor = Colors.Yellow;
canvas.Font = font;
canvas.FontSize = fontSize - 1; // NOTE: reduce to prevent clipping
canvas.DrawString(
    value: stringText,
    x: stringLocation.X,
    y: stringLocation.Y,
    width: stringSize.Width,
    height: stringSize.Height,
    horizontalAlignment: HorizontalAlignment.Left,
    verticalAlignment: VerticalAlignment.Top,
    textFlow: TextFlow.OverflowBounds,
    lineSpacingAdjustment: 0);

// save the result
string filePath = Path.GetFullPath("Issue279.png");
using FileStream fs = new(filePath, FileMode.Create);
bmp.WriteToStream(fs);
Console.WriteLine(filePath);
```

<div class="text-center">

![](https://swharden.com/static/2021/10/16/2022-02-19-maui-graphics-measure-string.png)

</div>

Note that in this example `GetStringSize()` respects font but `DrawString()` does not.

## Resources

* [Maui.Graphics on GitHub](https://github.com/dotnet/Microsoft.Maui.Graphics)

* [Maui.Graphics on NuGet](https://www.nuget.org/packages?q=Maui.Graphics)

* [https://Maui.Graphics](https://Maui.Graphics)

* [dotnet/Microsoft.Maui.Graphics issue #279](https://github.com/dotnet/Microsoft.Maui.Graphics/issues/279)