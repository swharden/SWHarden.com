---
Title: NDepend Status Badges
Description: How I used C# and Maui.Graphics to generate status badges for NDepend static analysis metrics
Date: 2021-10-17 13:20:00
tags: ["csharp", "maui"]
---

# NDepend Status Badges

**Many project websites and readmes have status badges** that display build status, project details, or code metrics. [badgen.net](https://badgen.net/) and [shields.io](https://shields.io/) are popular services for dynamically generating status badges as SVG files using HTTP requests. This article demonstrates how I use C# and `Microsoft.Maui.Graphics` to build status badges from [**NDepend**](https://www.ndepend.com/) static analysis reports. Source code for this project is [available on GitHub](https://github.com/swharden/NDepend-Badges).

<div class='text-center'>

<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/classes.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-types.svg' />

</div>

## NDepend Trend Data XML

NDepend can analyze a code base at different points in time and display code metric trends. See [NDepend: Trend Monitoring](https://www.ndepend.com/features/trend-monitoring#Trend) for a full description. These metrics are stored in an XML file available in the HTML build folder.

### Metric Index

The XML file contains many `Root/MetricIndex/Metric` elements that describe each metric and its units. This can be parsed to obtain the `Name` and `Unit` for each metric.

```xml
<Root>
  <MetricIndex>
    <Metric Name="# New Issues since Baseline" Unit="issues" />
    <Metric Name="# Issues Fixed since Baseline" Unit="issues" />
    <Metric Name="# Issues Worsened since Baseline" Unit="issues" />
    <Metric Name="# Issues with severity Blocker" Unit="issues" />
    <Metric Name="# Issues with severity Critical" Unit="issues" />
    <Metric Name="# Issues with severity High" Unit="issues" />
    <Metric Name="# Issues with severity Medium" Unit="issues" />
    ...
  </MetricIndex>
</Root>
```

### Metrics by DateTime

The XML file contains multiple `Root/M/R` elements that contain the value of each metric at a distinct time point. Numerical metrics have been converted to strings separated by the `|` character. Metric values for each time point are in the same order as the metric index.

```xml
<Root>
  <M>
    <R D="10/16/2021 11:58:04 AM" V="0|0|0|0|1|598|2177|...|19|133" />
    <R D="10/03/2021 04:15:24 PM" V="0|0|0|0|1|593|2160|...|19|132" />
	...
  </M>
</Root>
```

## Read NDepend Trend XML with C# 

To read timestamped metrics from the NDepend XML I started by creating a C# record to hold an individual timestamped metric:

```cs
public record Metric
{
    public DateTime DateTime { get; init; }
    public string Name { get; init; }
    public string Unit { get; init; }
    public string Value { get; init; }
}
```

I then reached for `using System.Xml.Linq` and `using System.Xml.XPath` to extract a big list of timestamped metrics from the NDepend XML file:

```cs
Metric[] GetMetricsFromXML(string xmlFilePath)
{
    XDocument doc = XDocument.Load(xmlFilePath);
    List<Metric> baseMetrics = new();
    foreach (var el in doc.XPathSelectElement("/Root/MetricIndex").Elements())
    {
        string name = el.Attribute("Name").Value;
        string unit = el.Attribute("Unit").Value;
        baseMetrics.Add(new Metric() { Name = name, Unit = unit });
    }

    List<Metric> allMetrics = new();
    foreach (var runElement in doc.XPathSelectElement("/Root/M").Elements())
    {
        DateTime runDateTime = DateTime.Parse(runElement.Attribute("D").Value);
        string[] values = runElement.Attribute("V").Value.Split("|");

        List<Metric> runMetrics = new();
        for (int i = 0; i < baseMetrics.Count; i++)
            runMetrics.Add(baseMetrics[i] with { DateTime = runDateTime, Value = values[i] });

        allMetrics.AddRange(runMetrics);
    }

    return allMetrics.ToArray();
}
```

I found it convenient to make a helper function to get only the latest metrics:

```cs
Metric[] GetLatestMetrics(Metric[] metrics)
{
    DateTime latestDateTime = metrics.Select(x => x.DateTime).Distinct().OrderBy(x => x).Last();
    return metrics.Where(x => x.DateTime == latestDateTime).ToArray();
}
```

## Generate NDepend Status Badges

I've already written [how to make status badges with C# and Maui.Graphics](https://swharden.com/blog/2021-11-16-maui-graphics-badges/), but that strategy only generates PNG files. For this project I also chose to generate SVG files. Rather than discuss that in detail, I'll just show to the source code for an example SVG file. 

It is important to note that in order to know the image width I must measure the string width. In HTML environments this could be done with vanilla Javascript, but in a C# environment I reached for `Microsoft.Maui.Graphics` (see [how to MeasureString() with Maui.Graphics](https://swharden.com/blog/2021-10-16-maui-graphics-measurestring)).

<div class='text-center'>

<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-types.svg' />

</div>

```xml
<svg xmlns='http://www.w3.org/2000/svg'
    xmlns:xlink='http://www.w3.org/1999/xlink' width='237' height='20' role='img' aria-label='languages: 5'>
    <title>Average # Lines of Code for Types: 25.96</title>
    <linearGradient id='s' x2='0' y2='100%'>
        <!-- linear gradient to use for the background shadow -->
        <stop offset='0' stop-color='#bbb' stop-opacity='.1'/>
        <stop offset='1' stop-opacity='.1'/>
    </linearGradient>
    <clipPath id='r'>
        <!-- clip to a rectangle with rounded edges -->
        <rect width='237' height='20' rx='3' fill='#fff'/>
    </clipPath>
    <g clip-path='url(#r)'>
        <!-- left background -->
        <rect width='195' height='20' fill='#555'/>
        <!-- right background -->
        <rect x='195' width='42' height='20' fill='#007ec6'/>
        <!-- background shadow -->
        <rect width='237' height='20' fill='url(#s)'/>
    </g>
    <g fill='#FFF' text-anchor='center' font-family='Verdana,Geneva,DejaVu Sans,sans-serif' text-rendering='geometricPrecision' font-size='110'>
        <!-- left text semitransparent shadow then white text -->
        <text aria-hidden='true' x='40' y='150' fill='#010101' fill-opacity='.3' transform='scale(.1)' textLength='1854'>Average # Lines of Code for Types</text>
        <text x='40' y='140' transform='scale(.1)' fill='#FFF' textLength='1854'>Average # Lines of Code for Types</text>
        <!-- right text semitransparent shadow then white text -->
        <text aria-hidden='true' x='1994' y='150' fill='#010101' fill-opacity='.3' transform='scale(.1)' textLength='300'>25.96</text>
        <text x='1994' y='140' transform='scale(.1)' fill='#FFF' textLength='300'>25.96</text>
    </g>
</svg>
```

One day Maui.Graphics may offer SVG export support ([issue #103](https://github.com/dotnet/Microsoft.Maui.Graphics/issues/103)) but for now generating these files discretely isn't too bad.

## Badges

After putting it all together these are the badges generated by analyzing the current [ScottPlot](https://scottplot.net) code base:

### SVG

<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/new-issues-since-baseline.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-fixed-since-baseline.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-worsened-since-baseline.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-blocker.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-critical.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-high.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-medium.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-low.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/blocker-critical-high-issues.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/suppressed-issues.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules-violated.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules-violated.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates-warn.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates-fail.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/percentage-debt-metric.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/debt-metric.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/annual-interest-metric.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/breaking-point.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/breaking-point-of-blocker-critical-high-issues.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-justmycode.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-notmycode.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/source-files.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/il-instructions.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/il-instructions-notmycode.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/assemblies.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/namespaces.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/types.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/public-types.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/classes.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/abstract-classes.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/interfaces.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/structures.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/abstract-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/concrete-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/fields.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-lines-of-code-for-methods-justmycode.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-methods-with-at-least-3-lines-of-code.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-lines-of-code-for-types-justmycode.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-types.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-cyclomatic-complexity-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-cyclomatic-complexity-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-il-cyclomatic-complexity-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-il-cyclomatic-complexity-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-il-nesting-depth-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-il-nesting-depth-for-methods.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-of-methods-for-types.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-methods-for-types.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-of-methods-for-interfaces.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-methods-for-interfaces.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-uncoverable.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-assemblies-used.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-namespaces-used.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-types-used.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-methods-used.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-fields-used.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules-violations.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules.svg' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules-violations.svg' />

### PNG

<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/new-issues-since-baseline.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-fixed-since-baseline.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-worsened-since-baseline.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-blocker.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-critical.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-high.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-medium.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues-with-severity-low.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/blocker-critical-high-issues.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/issues.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/suppressed-issues.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules-violated.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules-violated.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates-warn.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/quality-gates-fail.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/percentage-debt-metric.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/debt-metric.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/annual-interest-metric.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/breaking-point.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/breaking-point-of-blocker-critical-high-issues.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-justmycode.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-notmycode.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/source-files.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/il-instructions.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/il-instructions-notmycode.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/assemblies.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/namespaces.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/types.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/public-types.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/classes.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/abstract-classes.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/interfaces.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/structures.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/abstract-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/concrete-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/fields.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-lines-of-code-for-methods-justmycode.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-methods-with-at-least-3-lines-of-code.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-lines-of-code-for-types-justmycode.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-lines-of-code-for-types.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-cyclomatic-complexity-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-cyclomatic-complexity-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-il-cyclomatic-complexity-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-il-cyclomatic-complexity-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-il-nesting-depth-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-il-nesting-depth-for-methods.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-of-methods-for-types.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-methods-for-types.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/max-of-methods-for-interfaces.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/average-methods-for-interfaces.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/lines-of-code-uncoverable.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-assemblies-used.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-namespaces-used.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-types-used.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-methods-used.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/third-party-fields-used.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/rules-violations.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules.png' />
<img style='margin-top: .1em; margin-bottom: .1em;' src='https://swharden.com/blog/2021-11-17-ndepend-badges/badges/critical-rules-violations.png' />


## Resources
* Source code on GitHub: https://github.com/swharden/NDepend-Badges
* NDepend website: https://www.ndepend.com/
* NDepend sample reports: https://www.ndepend.com/sample-reports/
* [How to MeasureString() with Maui.Graphics](https://swharden.com/blog/2021-10-16-maui-graphics-measurestring/)
* [Status Badges with Maui.Graphics](https://swharden.com/blog/2021-11-16-maui-graphics-badges/)
* [Draw with Maui.Graphics and Skia in a C# Console Application](https://swharden.com/blog/2021-08-01-maui-skia-console/)