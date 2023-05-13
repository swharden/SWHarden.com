---
title: Status Badges with Maui.Graphics
description: How to use Microsoft.Maui.Graphics to render status badges
Date: 2021-10-16 20:40:00
tags: ["csharp", "maui", "graphics"]
---



**Status badges are popular decorators on GitHub readme pages and project websites.** [Badgen.net](https://badgen.net) and [shields.io](https://shields.io) are popular HTTP APIs for dynamically generating SVG status badges. In this article we will use the new `Microsoft.Maui.Graphics` package to generate status badges from a C# console application. This application can be downloaded: [**BadgeApp.zip**](https://swharden.com/static/2021/11/16/BadgeApp.zip)

<div class="text-center">

![](https://swharden.com/static/2021/11/16/demo1.png)
![](https://swharden.com/static/2021/11/16/demo1b.png)

</div>


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
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="https://swharden.com/static/2021/11/16/#info-fill"/></svg>
  <div>
    <strong>UPDATE:</strong> This article was written when <code>Microsoft.Maui.Graphics</code> was still in preview. See <a href="https://swharden.com/blog/2022-05-25-maui-graphics/" class="fw-bold">Drawing with Maui Graphics (blog post)</a> and <a href="https://swharden.com/csdv/" class="fw-bold">C# Data Visualization (website)</a> for updated code examples and information about using this library.
  </div>
</div>

## Badge.cs

The `Badge` class contains all the logic needed to render and save a badge as a PNG file. 

This code demonstrates a few advanced topics which are worth considering:
* image scaling
* state management (save/restore)
* clipping
* rounded rectangles
* string measurement

```cs
using Microsoft.Maui.Graphics;
using Microsoft.Maui.Graphics.Skia;

public class Badge
{
    readonly string Name;
    readonly string Value;
    readonly SizeF NameSize;
    readonly SizeF ValueSize;

    // Customize these to change the style of the button
    public Color BackgroundLeft = Color.FromArgb("#666");
    public Color BackgroundRight = Color.FromArgb("#08C");
    public Color BackgroundLiner = Colors.White.WithAlpha(.15f);
    public Color FontColor = Colors.White;
    public Color FontShadow = Colors.Black.WithAlpha(.5f);
    public Color OverlayTop = Colors.Black.WithAlpha(0);
    public Color OverlayBottom = Colors.Black.WithAlpha(.25f);

    public Badge(string name, string value)
    {
        Name = name;
        Value = value;
        NameSize = MeasureString(name);
        ValueSize = MeasureString(value);
    }

    public void SavePng(string pngFilePath, float scale = 1)
    {
        float totalWidth = NameSize.Width + ValueSize.Width;
        int imageWidth = (int)totalWidth + 22;
        RectangleF imageRect = new(0, 0, imageWidth, 20);

        int scaledWidth = (int)(imageRect.Width * scale);
        int scaledHeight = (int)(imageRect.Height * scale);
        BitmapExportContext bmp = SkiaGraphicsService.Instance.CreateBitmapExportContext(scaledWidth, scaledHeight);
        ICanvas canvas = bmp.Canvas;
        canvas.Scale(scale, scale);

        // left background
        canvas.FillColor = BackgroundLeft;
        canvas.FillRoundedRectangle(imageRect, 5);

        // right background
        float bg2x = 10 + NameSize.Width;
        canvas.SaveState();
        canvas.ClipRectangle(bg2x, 0, bmp.Width, bmp.Height);
        canvas.FillColor = BackgroundRight;
        canvas.FillRoundedRectangle(imageRect, 5);
        canvas.RestoreState();

        // vertical line
        canvas.StrokeColor = BackgroundLiner;
        canvas.DrawLine(bg2x, 0, bg2x, bmp.Height);

        // background overlay shadow
        var pt = new LinearGradientPaint() { StartColor = OverlayTop, EndColor = OverlayBottom };
        canvas.SetFillPaint(pt, new Point(0, 0), new Point(0, bmp.Height));
        canvas.FillRoundedRectangle(imageRect, 5);

        // draw text backgrounds
        canvas.FontSize = 12;
        float offsetY = 14;
        float offsetX1 = 5;
        float offsetX2 = 15;
        float shadowOffset = 1;

        // text shadow
        canvas.FontColor = FontShadow;
        canvas.DrawString(Name, offsetX1 + shadowOffset, offsetY + shadowOffset, HorizontalAlignment.Left);
        canvas.DrawString(Value, offsetX2 + NameSize.Width + shadowOffset, offsetY + shadowOffset, HorizontalAlignment.Left);

        // text foreground
        canvas.FontColor = FontColor;
        canvas.DrawString(Name, offsetX1, offsetY, HorizontalAlignment.Left);
        canvas.DrawString(Value, offsetX2 + NameSize.Width, offsetY, HorizontalAlignment.Left);

        // save the output
        bmp.WriteToFile(pngFilePath);
    }

    SizeF MeasureString(string text, string fontName = "Arial", float fontSize = 12)
    {
        var fontService = new SkiaFontService("", "");
        using SkiaSharp.SKTypeface typeFace = fontService.GetTypeface(fontName);
        using SkiaSharp.SKPaint paint = new() { Typeface = typeFace, TextSize = fontSize };
        float width = paint.MeasureText(text);
        float height = fontSize;
        return new SizeF(width, height);
    }
}
```

## Program.cs

This simple program is all it takes to render and save a badge.

```cs
Badge myBadge = new("Maui", "Graphics");
myBadge.SavePng("demo.png");
```

<div class="text-center">

![](https://swharden.com/static/2021/11/16/demo1.png)

</div>

### Customization

You can reach into the `Badge` class and customize styles as desired.

```cs
Badge myBadge = new("Maui", "Graphics")
{
    BackgroundRight = Microsoft.Maui.Graphics.Color.FromArgb("#3cc51d"),
};
myBadge.SavePng("demo1b.png");
```

<div class="text-center">

![](https://swharden.com/static/2021/11/16/demo1b.png)

</div>

### Image Scaling

`Microsoft.Maui.Graphics` natively supports image scaling. This allows you to create large badges without any loss in quality that would come from creating a small badge and resizing the bitmap.

```cs
Badge myBadge = new("Maui", "Graphics");
myBadge.SavePng("demo1.png", scale: 1);
myBadge.SavePng("demo2.png", scale: 2);
myBadge.SavePng("demo5.png", scale: 5);
```

<div class="text-center">

![](https://swharden.com/static/2021/11/16/demo1.png)
![](https://swharden.com/static/2021/11/16/demo2.png)
![](https://swharden.com/static/2021/11/16/demo5.png)

</div>

## Resources

* Download this application: [**BadgeApp.zip**](https://swharden.com/static/2021/11/16/BadgeApp.zip)

* [How to `MeasureString()` with Maui.Graphics](https://swharden.com/blog/2021-10-16-maui-graphics-measurestring/)

* [Maui.Graphics on GitHub](https://github.com/dotnet/Microsoft.Maui.Graphics)

* [Maui.Graphics Issue #103 - SVG support](https://github.com/dotnet/Microsoft.Maui.Graphics/issues/103)

* [Maui.Graphics on NuGet](https://www.nuget.org/packages?q=Maui.Graphics)

* [Maui.Graphics WPF Quickstart](https://maui.graphics/quickstart/wpf/)

* [Maui.Graphics WinForms Quickstart](https://maui.graphics/quickstart/winforms/)