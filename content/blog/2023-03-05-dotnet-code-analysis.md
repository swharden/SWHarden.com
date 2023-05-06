---
Title: .NET Source Code Analysis
Description: How to analyze source code metrics of .NET assemblies from a console application
Date: 2023-03-05 15:20:00
tags: ["csharp"]
---

**This page describes how to use the [Microsoft.CodeAnalysis.Metrics](https://www.nuget.org/packages/Microsoft.CodeAnalysis.Metrics/) package to perform source code analysis of .NET assemblies from a console application.** Visual Studio users can perform source code analysis by clicking the "Analyze" dropdown menu and selecting "Calculate Code Metrics", but I sought to automate this process so I can generate custom code analysis reports from console applications as part of my CI pipeline.

## Performing Code Analysis

**Step 1:** Add the [`Microsoft.CodeAnalysis.Metrics`](https://www.nuget.org/packages/Microsoft.CodeAnalysis.Metrics/) package to your project:

```bash
dotnet add package Microsoft.CodeAnalysis.Metrics
```

**Step 2:** Perform code analysis:

```bash
dotnet build -target:Metrics
```

Note that multi-targeted projects must append `--framework net6.0` to specify a single platform target to use for code analysis.

**Step 3:** Inspect analysis results in `ProjectName.Metrics.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<CodeMetricsReport Version="1.0">
  <Targets>
    <Target Name="ScottPlot.csproj">
      <Assembly Name="ScottPlot, Version=4.1.61.0">
        <Metrics>
          <Metric Name="MaintainabilityIndex" Value="81" />
          <Metric Name="CyclomaticComplexity" Value="6324" />
          <Metric Name="ClassCoupling" Value="664" />
          <Metric Name="DepthOfInheritance" Value="3" />
          <Metric Name="SourceLines" Value="35360" />
          <Metric Name="ExecutableLines" Value="10208" />
        </Metrics>
        <Namespaces>
        ...
```

## Parsing the Analysis XML File

The code analysis XML contains information about every assembly, namespace, type, and function in the whole code base! There is a lot of possible information to extract, but the code below is enough to get us started extracting basic metric information for every type in the code base.

```cs
using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Collections.Generic;

/// <summary>
/// Display a particular metric for every type in an assembly.
/// </summary>
void RankTypes(string xmlFilePath, string metricName = "CyclomaticComplexity", bool highToLow = true)
{
    string xmlText = File.ReadAllText(xmlFilePath);
    XDocument doc = XDocument.Parse(xmlText);
    XElement assembly = doc.Descendants("Assembly").First();

    var rankedTypes = GetMetricByType(assembly, metricName).OrderBy(x => x.Value).ToArray();
    if (highToLow)
        Array.Reverse(rankedTypes);

    Console.WriteLine($"Types ranked by {metricName}:");
    foreach (var type in rankedTypes)
        Console.WriteLine($"{type.Value:N0}\t{type.Key}");
}

Dictionary<string, int> GetMetricByType(XElement assembly, string metricName)
{
    Dictionary<string, int> metricByType = new();

    foreach (XElement namespaceElement in assembly.Element("Namespaces")!.Elements("Namespace"))
    {
        foreach (XElement namedType in namespaceElement.Elements("Types").Elements("NamedType"))
        {
            XElement metric = namedType.Element("Metrics")!.Elements("Metric")
                .Where(x => x.Attribute("Name")!.Value == metricName)
                .Single();
            string typeName = namedType.Attribute("Name")!.Value;
            string namespaceName = namespaceElement.Attribute("Name")!.Value;
            string fullTypeName = $"{namespaceName}.{typeName}";
            metricByType[fullTypeName] = int.Parse(metric.Attribute("Value")!.Value!.ToString());
        }
    }

    return metricByType;
}
```

## Querying Code Analysis Results

**Specific metrics of interest will vary, but here are some code examples demonstrating how to parse the code metrics file to display useful information.** For these examples I run the code analysis command above to generate [ScottPlot.Metrics.xml](ScottPlot.Metrics.xml.zip) from the [ScottPlot](https://scottplot.net) code base and use the code above to generate various reports.

### Rank Types by Cyclomatic Complexity

[Cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) is a measure of the number of different paths that can be taken through a computer program, and it is often used as an indicator for difficult-to-maintain code. Some CI systems even prevent the merging of pull requests if their cyclomatic complexity exceeds a predefined threshold! Although I don't intend to gate pull requests by complexity at this time, I would like to gain insight into which classes are the most complex as a way to quantitatively target my code maintenance and efforts.

```cs
RankTypes("ScottPlot.Metrics.xml", "CyclomaticComplexity");
```

```txt
517     ScottPlot.Plot
218     ScottPlot.Plottable.SignalPlotBase<T>
173     ScottPlot.Plottable.ScatterPlot
139     ScottPlot.Settings
120     ScottPlot.Ticks.TickCollection
118     ScottPlot.Renderable.Axis
114     ScottPlot.Drawing.Colormap
113     ScottPlot.Control.ControlBackEnd
109     ScottPlot.DataGen
99      ScottPlot.Plottable.AxisLineVector
98      ScottPlot.Plottable.Heatmap
95      ScottPlot.Tools
93      ScottPlot.Plottable.RepeatingAxisLine
91      ScottPlot.Plottable.PopulationPlot
85      ScottPlot.Plottable.AxisLine
83      ScottPlot.Plottable.AxisSpan
77      ScottPlot.Plottable.RadialGaugePlot
...
```

### Rank Types by Lines of Code
Similarly, ranking all my project's types by how many lines of code they contain can give me insight into which types may benefit most from refactoring.

```cs
RankTypes("ScottPlot.Metrics.xml", "SourceLines");
```

```txt
Types ranked by SourceLines:
4,155   ScottPlot.Plot
1,182   ScottPlot.DataGen
954     ScottPlot.Plottable.SignalPlotBase<T>
726     ScottPlot.Control.ControlBackEnd
670     ScottPlot.Ticks.TickCollection
670     ScottPlot.Settings
630     ScottPlot.Plottable.ScatterPlot
600     ScottPlot.Renderable.Axis
477     ScottPlot.Statistics.Common
454     ScottPlot.Tools
451     ScottPlot.Plottable.PopulationPlot
432     ScottPlot.Drawing.GDI
343     ScottPlot.Plottable.SignalPlotXYGeneric<TX, TY>
336     ScottPlot.Plottable.RepeatingAxisLine
335     ScottPlot.Drawing.Colormap
332     ScottPlot.Plottable.AxisLineVector
...
```

### Rank Types by Maintainability

The [Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning) is a value between 0 (worst) and 100 (best) that represents the relative ease of maintaining the code. It's calculated from a combination of [Halstead complexity](https://en.wikipedia.org/wiki/Halstead_complexity_measures) (size of the compiled code), [Cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) (number of paths that can be taken through the code), and the total number of lines of code.

```cs
MaintainabilityIndex = 171 
  - 5.2 * Math.Log(HalsteadVolume) 
  - 0.23 * CyclomaticComplexity
  - 16.2 * Math.Log(LinesOfCCode);
```

The maintainability index is calculated by `Microsoft.CodeAnalysis.Metrics` so we don't have to. I don't know how Microsoft arrived at their weights for this formula, but the overall idea is described [here](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning).

```cs
RankTypes("ScottPlot.Metrics.xml", "MaintainabilityIndex", highToLow: false);
```

```txt
43      ScottPlot.Drawing.Tools
48      ScottPlot.Statistics.Interpolation.Cubic
48      ScottPlot.Statistics.Interpolation.PeriodicSpline
49      ScottPlot.Statistics.Interpolation.EndSlopeSpline
49      ScottPlot.Statistics.Interpolation.NaturalSpline
50      ScottPlot.Renderable.AxisTicksRender
54      ScottPlot.Statistics.Interpolation.CatmullRom
55      ScottPlot.Statistics.Interpolation.SplineInterpolator
57      ScottPlot.DataGen
58      ScottPlot.DataStructures.SegmentedTree<T>
58      ScottPlot.MarkerShapes.Hashtag
58      ScottPlot.Ticks.TickCollection
59      ScottPlot.MarkerShapes.Asterisk
59      ScottPlot.Plottable.SignalPlotXYGeneric<TX, TY>
59      ScottPlot.Statistics.Interpolation.Bezier
60      ScottPlot.Statistics.Interpolation.Chaikin
61      ScottPlot.Generate
61      ScottPlot.Plot
61      ScottPlot.Statistics.Finance
...
```

### Create Custom HTML Reports

With a little more effort you can generate HTML reports that use tables and headings to highlight useful code metrics and draw attention to types that could benefit from refactoring to improve maintainability.

* View the sample report: [report.html](report.html)
* Download the code used to generate it: [CodeAnalysisReport.zip](https://swharden.com/static/2023/03/05/CodeAnalysisReport.zip)

<a href="https://swharden.com/static/2023/03/05/report.html"><img src="https://swharden.com/static/2023/03/05/report.png" class="border shadow"></a>

## Conclusions

Microsoft's official [Microsoft.CodeAnalysis.Metrics](https://www.nuget.org/packages/Microsoft.CodeAnalysis.Metrics/) NuGet package is a useful tool for analyzing assemblies, navigating through namespaces, types, properties, and methods, and evaluating their metrics. Since these analyses can be performed using console applications, they can be easily integrated into CI pipelines or used to create standalone code analysis applications. Future projects can build on the concepts described here to create graphical visualizations of code metrics in large projects.

## Resources

* [Code metrics values](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-values) - official documentation of the code metrics analysis system

* [Visual Studio source code analysis](https://learn.microsoft.com/en-us/visualstudio/code-quality/roslyn-analyzers-overview)

* [Microsoft.CodeAnalysis.Metrics NuGet Package](https://www.nuget.org/packages/Microsoft.CodeAnalysis.Metrics/)

* [Code metrics: Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning)

* [NDepend](https://www.ndepend.com/) is commercial software for performing code analysis on .NET code bases and has many advanced features that make it worth considering for organizations that wish to track code quality and who can afford the cost. The [NDepend Sample Reports](https://www.ndepend.com/sample-reports/) demonstrate useful ways to report code analysis metrics.

* This page documents findings originally discussed in [ScottPlot issue #2454](https://github.com/ScottPlot/ScottPlot/issues/2454)