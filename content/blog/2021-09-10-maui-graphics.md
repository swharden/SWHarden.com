---
title: Drawing with Maui.Graphics
description: How to use Maui.Graphics to draw and create animations in a Windows Forms and WPF applications
Date: 2021-09-10 22:30:00
tags: ["csharp", "maui", "graphics"]
---



**[.NET MAUI](https://docs.microsoft.com/en-us/dotnet/maui/what-is-maui) (Multi-Platform Application User Interface) is a new framework for creating cross-platform apps using C#.** MAUI will be released as part of .NET 6 in November 2021 and it is expected to come with [`Maui.Graphics`](https://github.com/dotnet/Microsoft.Maui.Graphics), a cross-platform drawing library superior to [`System.Drawing`](https://docs.microsoft.com/en-us/dotnet/api/system.drawing?view=net-5.0#remarks) in many ways. Although [`System.Drawing.Common`](https://www.nuget.org/packages/System.Drawing.Common) currently supports rendering in Linux and MacOS, [cross-platform support for System.Drawing will sunset](https://github.com/dotnet/designs/blob/main/accepted/2021/system-drawing-win-only/system-drawing-win-only.md) over the next few releases and begin throwing a `PlatformNotSupportedException` in .NET 6.

By creating a graphics model using only `Maui.Graphics` dependencies, users can share drawing code across multiple rendering technologies (GDI, Skia, SharpDX, etc.), operating systems (Windows, Linux, MacOS, etc.), and application frameworks (WinForms, WPF, Maui, WinUI, etc.). **This page demonstrates how to create a platform-agnostic graphics model and render it using Windows Forms and WPF.** Resources in the `Maui.Graphics` namespace can be used by any modern .NET application (not just Maui apps).

<div class="text-center">

![](https://swharden.com/static/2021/09/10/maui-graphics-balls.gif)

</div>

> ⚠️ **WARNING:** `Maui.Graphics` is still a pre-release experimental library (as noted on [their GitHub page](https://github.com/dotnet/Microsoft.Maui.Graphics)). Although the code examples on this page work presently, the API may change between now and the official release.


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
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="https://swharden.com/static/2021/09/10/#info-fill"/></svg>
  <div>
    <strong>UPDATE:</strong> This article was written when <code>Microsoft.Maui.Graphics</code> was still in preview. See <a href="https://swharden.com/blog/2022-05-25-maui-graphics/" class="fw-bold">Drawing with Maui Graphics (blog post)</a> and <a href="https://swharden.com/csdv/" class="fw-bold">C# Data Visualization (website)</a> for updated code examples and information about using this library.
  </div>
</div>

## 1. Create a new Project

For this example I will start by creating a a .NET 5.0 WinForms project from scratch. Later we will extend the solution to include a WPF project that uses the same graphics model.

## 2. Add References to Maui.Graphics

We need to get the windows forms MAUI control and all its dependencies. At the time of writing (September, 2021) these packages are not yet available on NuGet, but they can be downloaded from the [Microsoft.Maui.Graphics GitHub page](https://github.com/dotnet/Microsoft.Maui.Graphics).

> 💡 **Tip:** If you're developing a desktop application you can improve the "rebuild all" time by editing the csproj files of your dependencies so `TargetFrameworks` only includes .NET Standard targets.

* Add the `Microsoft.Maui.Graphics` project to your solution and add a reference to it from your project.

* **Windows Forms:** Add the `Microsoft.Maui.Graphics.GDI.Winforms` project to your solution and add a reference to it in your WinForms project. A `GDIGraphicsView` control should appear in the toolbox.

* **WPF:** Add the `Microsoft.Maui.Graphics.Skia.WPF` project to your solution and add a reference to it in your WPF project. A `WDSkiaGraphicsView` control should appear in the toolbox.

<div class="text-center img-border">

![](https://swharden.com/static/2021/09/10/vs-maui.png)

</div>

## 3. Create a Drawable Object

**A _drawable_ is a class that implements `IDrawable`, has a `Draw()` method, and can be rendered anywhere Maui.Graphics is supported.** By only depending on `Maui.Graphics` it's easy to create a graphics model that can be used on any operating system using any supported graphical framework.

```cs
using Microsoft.Maui.Graphics;
```

This _drawable_ fills the image blue and renders 1,000 randomly-placed anti-aliased semi-transparent white lines on it. Note that the location of the lines depends on the size of the render field (passed-in as an argument).

```cs
public class RandomLines : IDrawable
{
    public void Draw(ICanvas canvas, RectangleF dirtyRect)
    {
        canvas.FillColor = Color.FromArgb("#003366");
        canvas.FillRectangle(dirtyRect);

        canvas.StrokeSize = 1;
        canvas.StrokeColor = Color.FromRgba(255, 255, 255, 100);
        Random Rand = new();
        for (int i = 0; i < 1000; i++)
        {
            canvas.DrawLine(
                x1: (float)Rand.NextDouble() * dirtyRect.Width,
                y1: (float)Rand.NextDouble() * dirtyRect.Height,
                x2: (float)Rand.NextDouble() * dirtyRect.Width,
                y2: (float)Rand.NextDouble() * dirtyRect.Height);
        }
    }
}
```

## 4. Add a GraphicsView Control

Drag/drop a GraphicsView control from the Toolbox onto your application and assign your graphics model to its `Drawable` field.

For animations you can use a timer to invalidate the control (forcing a redraw) automatically every 20 ms.

### Windows Forms (Rendering with GDI)

Windows Forms applications may also want to intercept SizeChanged events to force redraws as the window is resized.

```cs
public partial class Form1 : Form
{
    public Form1()
    {
        InitializeComponent();
        gdiGraphicsView1.Drawable = new RandomLines();
    }

    private void GdiGraphicsView1_SizeChanged(object? sender, EventArgs e) =>
        gdiGraphicsView1.Invalidate();

    private void timer1_Tick(object sender, EventArgs e) =>
        gdiGraphicsView1.Invalidate();
}
```

<div class="text-center">

![](https://swharden.com/static/2021/09/10/maui-graphics-winforms.gif)

</div>

**I found performance to be quite adequate.** On my system 1,000 lines rendered on an 800x600 window at ~60 fps. Like `System.Drawing` this system slows down as a function of image size, so full-screen 1920x1080 animation was much slower (~10 fps).

### WPF  (Rendering with SkiaSharp)

```xml
<Skia:WDSkiaGraphicsView Name="MyGraphicsView" />
```

```cs
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        MyGraphicsView.Drawable = new RandomLines();

        DispatcherTimer timer = new();
        timer.Interval = TimeSpan.FromMilliseconds(20);
        timer.Tick += Timer_Tick; ;
        timer.Start();
    }

    private void Timer_Tick(object sender, EventArgs e) =>
        MyGraphicsView.Invalidate();
}
```

<div class="text-center">

![](https://swharden.com/static/2021/09/10/maui-graphics-wpf.gif)

</div>

## Extend the Graphics Model

Since our project is configured to display the same graphics model with both WinForms and WPF, it's easy to edit the model in one place and it's updated everywhere. We can replace the random lines model with one that manages randomly colored and sized balls that bounce off the edges of the window as the model advances.

<div class="text-center">

![](https://swharden.com/static/2021/09/10/maui-graphics-balls.gif)

</div>

### BallField.cs

```cs
public class BallField : IDrawable
{
    private readonly Ball[] Balls;

    public BallField(int ballCount)
    {
        Balls = new Ball[ballCount];
    }

    public void Draw(ICanvas canvas, RectangleF dirtyRect)
    {
        canvas.FillColor = Colors.Navy;
        canvas.FillRectangle(dirtyRect);

        foreach (Ball ball in Balls)
        {
            ball?.Draw(canvas);
        }
    }

    public void Randomize(double width, double height)
    {
        Random rand = new();
        for (int i = 0; i < Balls.Length; i++)
        {
            Balls[i] = new()
            {
                X = rand.NextDouble() * width,
                Y = rand.NextDouble() * height,
                Radius = rand.NextDouble() * 5 + 5,
                XVel = rand.NextDouble() - .5,
                YVel = rand.NextDouble() - .5,
                R = (byte)rand.Next(50, 255),
                G = (byte)rand.Next(50, 255),
                B = (byte)rand.Next(50, 255),
            };
        }
    }

    public void Advance(double timeDelta, double width, double height)
    {
        foreach (Ball ball in Balls)
        {
            ball?.Advance(timeDelta, width, height);
        }
    }
}
```

### Ball.cs

```cs
public class Ball
{
    public double X;
    public double Y;
    public double Radius = 5;
    public double XVel;
    public double YVel;
    public byte R, G, B;

    public void Draw(ICanvas canvas)
    {
        canvas.FillColor = Color.FromRgb(R, G, B);
        canvas.FillCircle((float)X, (float)Y, (float)Radius);
    }

    public void Advance(double timeDelta, double width, double height)
    {
        MoveForward(timeDelta);
        Bounce(width, height);
    }

    private void MoveForward(double timeDelta)
    {
        X += XVel * timeDelta;
        Y += YVel * timeDelta;
    }

    private void Bounce(double width, double height)
    {
        double minX = Radius;
        double minY = Radius;
        double maxX = width - Radius;
        double maxY = height - Radius;

        if (X < minX)
        {
            X = minX + (minX - X);
            XVel = -XVel;
        }
        else if (X > maxX)
        {
            X = maxX - (X - maxX);
            XVel = -XVel;
        }

        if (Y < minY)
        {
            Y = minY + (minY - Y);
            YVel = -YVel;
        }
        else if (Y > maxY)
        {
            Y = maxY - (Y - maxY);
            YVel = -YVel;
        }
    }
}
```

## Download This Project 

* **Source Code:** [**Balls.zip**](https://swharden.com/static/2021/09/10/2021-09-12-Balls.zip) (10 kB)

* **WinForms (GDI) Demo:** [**Balls-WinForms.exe**](https://swharden.com/static/2021/09/10/2021-09-12-Balls.exe-WinForms.zip) (237 kB)

* **WPF (Skia) Demo:** [**Balls-WPF.exe**](https://swharden.com/static/2021/09/10/2021-09-12-Balls.exe-WPF.zip) (13 MB)

> To build this project from source code you currently have to download [Maui.Graphics source from GitHub](https://github.com/dotnet/Microsoft.Maui.Graphics) and edit the solution file to point to the correct directory containing these projects. This will get a lot easier after Microsoft puts their WinForms and WPF controls on NuGet.

## Coding Challenge

**Can you recreate this classic screensaver using Maui.Graphics?** Bonus points if the user can customize the number of shapes, the number of corners each shape has, and the number of lines drawn in each shape's history. It's a fun problem and I encourage you to give it a go! Here's how I did it: [mystify-maui.zip](https://swharden.com/static/2021/09/10/2021-09-13-mystify-maui.zip)

![](https://swharden.com/static/2021/09/10/maui-mystify.mp4)

## Resources

* [Draw with Maui.Graphics and Skia in a C# Console Application](https://swharden.com/blog/2021-08-01-maui-skia-console/)

* [Microsoft.Maui.Graphics on GitHub](https://github.com/dotnet/Microsoft.Maui.Graphics)

* [Maui.Graphics on NuGet](https://www.nuget.org/packages?q=Maui.Graphics)

* [Maui on GitHub](https://github.com/dotnet/maui)

* [C# Data Visualization](https://swharden.com/CsharpDataVis)

* [https://Maui.Graphics](https://maui.graphics)

* [Maui.Graphics WPF Quickstart](https://maui.graphics/quickstart/wpf)

* [Maui.Graphics WinForms Quickstart](https://maui.graphics/quickstart/winforms)