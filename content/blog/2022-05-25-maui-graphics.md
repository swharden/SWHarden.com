---
title: Use Maui.Graphics to Draw 2D Graphics in Any .NET Application
description: How to use Microsoft.Maui.Graphics to draw graphics in a .NET console application and save the output as an image file using SkiaSharp
date: 2022-05-25 22:13:00
tags: ["csharp", "graphics", "maui"]
---

# Use Maui.Graphics to Draw 2D Graphics in Any .NET Application

**This week Microsoft officially released .NET Maui and the new `Microsoft.Maui.Graphics` library which can draw 2D graphics in any .NET application (not just Maui apps).** This page offers a quick look at how to use this new library to draw graphics using SkiaSharp in a .NET 6 console application. The [C# Data Visualization](https://swharden.com/csdv/) site has additional examples for drawing and animating graphics using `Microsoft.Maui.Graphics` in Windows Forms and WPF applications.

<img src="https://swharden.com/static/2022/05/25/maui-graphics-quickstart.png" class="mx-auto my-5 d-block shadow">

The code below is a full .NET 6 console application demonstrating common graphics tasks (setting colors, drawing shapes, rendering text, etc.) and was used to generate the image above.

```cs
// These packages are available on NuGet
using Microsoft.Maui.Graphics;
using Microsoft.Maui.Graphics.Skia;

// Create a bitmap in memory and draw on its Canvas
SkiaBitmapExportContext bmp = new(600, 400, 1.0f);
ICanvas canvas = bmp.Canvas;

// Draw a big blue rectangle with a dark border
Rect backgroundRectangle = new(0, 0, bmp.Width, bmp.Height);
canvas.FillColor = Color.FromArgb("#003366");
canvas.FillRectangle(backgroundRectangle);
canvas.StrokeColor = Colors.Black;
canvas.StrokeSize = 20;
canvas.DrawRectangle(backgroundRectangle);

// Draw circles randomly around the image
for (int i = 0; i < 100; i++)
{
    float x = Random.Shared.Next(bmp.Width);
    float y = Random.Shared.Next(bmp.Height);
    float r = Random.Shared.Next(5, 50);

    Color randomColor = Color.FromRgb(
        red: Random.Shared.Next(255),
        green: Random.Shared.Next(255),
        blue: Random.Shared.Next(255));

    canvas.StrokeSize = r / 3;
    canvas.StrokeColor = randomColor.WithAlpha(.3f);
    canvas.DrawCircle(x, y, r);
}

// Measure a string
string myText = "Hello, Maui.Graphics!";
Font myFont = new Font("Impact");
float myFontSize = 48;
canvas.Font = myFont;
SizeF textSize = canvas.GetStringSize(myText, myFont, myFontSize);

// Draw a rectangle to hold the string
Point point = new(
    x: (bmp.Width - textSize.Width) / 2,
    y: (bmp.Height - textSize.Height) / 2);
Rect myTextRectangle = new(point, textSize);
canvas.FillColor = Colors.Black.WithAlpha(.5f);
canvas.FillRectangle(myTextRectangle);
canvas.StrokeSize = 2;
canvas.StrokeColor = Colors.Yellow;
canvas.DrawRectangle(myTextRectangle);

// Daw the string itself
canvas.FontSize = myFontSize * .9f; // smaller than the rectangle
canvas.FontColor = Colors.White;
canvas.DrawString(myText, myTextRectangle, 
    HorizontalAlignment.Center, VerticalAlignment.Center, TextFlow.OverflowBounds);

// Save the image as a PNG file
bmp.WriteToFile("console2.png");
```

## Multi-Platform Graphics Abstraction

**The `Microsoft.Maui.Graphics` namespace a small collection of interfaces which can be implemented by many different rendering technologies** (SkiaSharp, SharpDX, GDI, etc.), making it possible to create drawing routines that are totally abstracted from the underlying graphics rendering system.

I really like that I can now create a .NET Standard 2.0 project that exclusively uses interfaces from `Microsoft.Maui.Graphics` to write code that draws complex graphics, then reference that code from other projects that use platform-specific graphics libraries to render the images.

When I write scientific simulations or data visualization code I frequently regard my graphics drawing routines as business logic, and drawing with Maui.Graphics lets me write this code to an abstraction that keeps rendering technology dependencies out of my business logic - a big win!

## Rough Edges

After working with this library while it was being developed over the last few months, these are the things I find most limiting in my personal projects which made it through the initial release this week. Some of them are [open issues](https://github.com/dotnet/Microsoft.Maui.Graphics/issues) so they may get fixed soon, and depending on how the project continues to evolve many of these rough edges may improve with time. I'm listing them here now so I can keep track of them, and I intend to update this list if/as these topics improve:

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
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="https://swharden.com/static/2022/05/25/#info-fill"/></svg>
  <div>
    <strong>Note:</strong> This section was last reviewed on April 25, 2022 and improvements may have been made since this text was written.
  </div>
</div>

* **Strings cannot be accurately measured:** The size returned by `GetStringSize()` is inaccurate and does not respect font. There's an issue tracking this ([#279](https://github.com/dotnet/Microsoft.Maui.Graphics/issues/279)), but it's been open for more than three months and the library was released this week in its broken state.

  * EDIT: I concede multi-platform font support is a very hard problem, but this exactly the type of problem that .NET Maui was created to solve.<br><br>

* **Missing XML documentation:** Intellisense can really help people who are new to a library. The roll-out of a whole new application framework is a good example of a time when a lot of people will be exploring a new library. Let's take the [`Color` class](https://github.com/dotnet/Microsoft.Maui.Graphics/blob/main/src/Microsoft.Maui.Graphics/Color.cs) for example (which 100% of people will interact with) and consider misunderstandings that could be prevented by XML documentation and intellisense: If `new Color()` accepts 3 floats, should they be 0-255 or 0-1? I need to make a color from the RGB web value `#003366`, why does `Color.FromHex()` tell me to use `FromArgb`? Web colors are RGBA, should I use `FromRrgba()`? But wait, that string is RGB, not ARGB or RGBA, so will it throw an exception? What does `Color.Parse()` do?

  * Edit 1: Some of these answers are [documented in source code](https://github.com/dotnet/Microsoft.Maui.Graphics/blob/e15f2d552d851c28771e7fe092895e908395f8a4/src/Microsoft.Maui.Graphics/Color.cs#L574-L590), but they are not XML docs, so this information is not available to library users.

  * Edit 2: Is it on the open-source community to contribute XML documentation? If so, fair enough, but it is a very extensive effort (to write _and_ to review), so a call should be put out for this job to ensure someone doesn't go through all the effort then have their open PR sit unmerged for months while it falls out of sync with the main branch.

* **The library has signs of being incomplete:** There remain a good number of [NotImplementedException](https://github.com/dotnet/Microsoft.Maui.Graphics/search?q=NotImplementedException) and [// todo](https://github.com/dotnet/Microsoft.Maui.Graphics/search?q=todo) in sections of the code base that indicate additional work is still required.

Again, I'm pointing these things out the very first week .NET Maui was released, so there's plenty of time and opportunity for improvements in the coming weeks and months.

**I'm optimistic this library will continue to improve, and I am very excited to watch it progress!** I'm not aware of the internal pressures and constraints that led to the library being released like it was this week, but I want to end by complimenting the team on their great job so far and encourage everyone (at Microsoft and in the open-source community at large) to keep moving this library forward. The .NET Maui team undertook an ambitious challenge by setting-out to implement cross-platform graphics support, but achieving this goal elegantly will be a huge accomplishment for the .NET community!

## Resources
* [Source code for this project](https://github.com/swharden/Csharp-Data-Visualization/tree/main/projects/maui-graphics)
* [Maui.Graphics WinForms Quickstart](https://swharden.com/csdv/maui.graphics/quickstart-winforms/)
* [Maui.Graphics WPF Quickstart](https://swharden.com/csdv/maui.graphics/quickstart-wpf/)
* [Maui.Graphics Console Quickstart](https://swharden.com/csdv/maui.graphics/quickstart-console/)
* [Maui.Graphics .NET Maui Quickstart](https://swharden.com/csdv/maui.graphics/quickstart-maui/)
* [https://maui.graphics](https://maui.graphics)