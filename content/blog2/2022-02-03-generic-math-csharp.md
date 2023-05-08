---
Title: Generic Math in C# with .NET 6
Description: How to perform math on generic types in C# with .NET 6
Date: 2022-02-03 23:55:00
tags: ["csharp"]
---

# Generic Math in C# with .NET 6

**Generic types are great, but it has traditionally been difficult to do math with them.** Consider the simple task where you want to accept a generic array and return its sum. With .NET 6 (and features currently still in preview), this got much easier!

```cs
public static T Sum<T>(T[] values) where T : INumber<T>
{
    T sum = T.Zero;
    for (int i = 0; i < values.Length; i++)
        sum += values[i];
    return sum;
}
```

To use this feature today you must:
1. Install the [System.Runtime.Experimental ](https://www.nuget.org/packages/System.Runtime.Experimental/6.0.2-mauipre.1.22054.8) NuGet package
2. Add these lines to the `PropertyGroup` in your csproj file:

```xml
<langversion>preview</langversion>
<EnablePreviewFeatures>true</EnablePreviewFeatures>
```

Note that the generic math function above is equivalent in speed to one that accepts and returns `double[]`, while a method which accepts a generic but calls `Convert.ToDouble()` every time is about 3x slower than both options:

```cs
// this code works on older versions of .NET but is about 3x slower
public static double SumGenericToDouble<T>(T[] values)
{
    double sum = 0;
    for (int i = 0; i < values.Length; i++)
        sum += Convert.ToDouble(values[i]);
    return sum;
}
```

## Resources
* [Preview Features in .NET 6 – Generic Math](https://devblogs.microsoft.com/dotnet/preview-features-in-net-6-generic-math/)
* [Generic Math in .NET 6](https://dunnhq.com/posts/2021/generic-math/)
* [Code Notes: Benchmark Generic Math](https://github.com/swharden/code-notes/tree/master/Csharp/misc/projects/BenchmarkGenericMath)