---
title: Using DataFrames in C#
description: How to use the DataFrame class from the Microsoft.Data.Analysis package to interact with tabular data
date: 2022-05-01 23:00:00
tags: ["csharp"]
---



**The DataFrame is a data structure designed for manipulation, analysis, and visualization of tabular data, and it is the cornerstone of many data science applications.** One of the most famous implementations of the data frame is provided by the Pandas package for Python. An equivalent data structure is available for C# using Microsoft's data analysis package. Although data frames are commonly used in Jupyter notebooks, they can be used in standard .NET applications as well. This article surveys Microsoft's Data Analysis package and introduces how to interact with with data frames using C# and the .NET platform.

## DataFrame Quickstart

* A DataFrame is a 2D matrix that stores data values in named columns.
* Each column has a distinct data type.
* Rows represent observations.

Add the [Microsoft.Data.Analysis package](https://www.nuget.org/packages/Microsoft.Data.Analysis/) to your project, then you can create a DataFrame like this:

```cs
using Microsoft.Data.Analysis;

string[] names = { "Oliver", "Charlotte", "Henry", "Amelia", "Owen" };
int[] ages = { 23, 19, 42, 64, 35 };
double[] heights = { 1.91, 1.62, 1.72, 1.57, 1.85 };

DataFrameColumn[] columns = {
    new StringDataFrameColumn("Name", names),
    new PrimitiveDataFrameColumn<int>("Age", ages),
    new PrimitiveDataFrameColumn<double>("Height", heights),
};

DataFrame df = new(columns);
```

Contents of a DataFrame can be previewed using `Console.WriteLine(df)` but the formatting isn't pretty.

```text
Name  Age   Height
Oliver23    1.91
Charlotte19    1.62
Henry 42    1.72
Amelia64    1.57
Owen  35    1.85
```

## Pretty DataFrame Formatting

**A custom `PrettyPrint()` extension method can improve DataFrame readability.** Implementing this as an extension method allows me to call `df.PrettyPrint()` anywhere in my code.

<details>
<summary>💡 View the full <code>PrettyPrinters.cs</code> source code</summary>

```cs
using Microsoft.Data.Analysis;
using System.Text;

internal static class PrettyPrinters
{
    public static void PrettyPrint(this DataFrame df) => Console.WriteLine(PrettyText(df));
    public static string PrettyText(this DataFrame df) => ToStringArray2D(df).ToFormattedText();

    public static string ToMarkdown(this DataFrame df) => ToStringArray2D(df).ToMarkdown();

    public static void PrettyPrint(this DataFrameRow row) => Console.WriteLine(Pretty(row));
    public static string Pretty(this DataFrameRow row) => row.Select(x => x?.ToString() ?? string.Empty).StringJoin();
    private static string StringJoin(this IEnumerable<string> strings) => string.Join(" ", strings.Select(x => x.ToString()));

    private static string[,] ToStringArray2D(DataFrame df)
    {
        string[,] strings = new string[df.Rows.Count + 1, df.Columns.Count];

        for (int i = 0; i < df.Columns.Count; i++)
            strings[0, i] = df.Columns[i].Name;

        for (int i = 0; i < df.Rows.Count; i++)
            for (int j = 0; j < df.Columns.Count; j++)
                strings[i + 1, j] = df[i, j]?.ToString() ?? string.Empty;

        return strings;
    }

    private static int[] GetMaxLengthsByColumn(this string[,] strings)
    {
        int[] maxLengthsByColumn = new int[strings.GetLength(1)];

        for (int y = 0; y < strings.GetLength(0); y++)
            for (int x = 0; x < strings.GetLength(1); x++)
                maxLengthsByColumn[x] = Math.Max(maxLengthsByColumn[x], strings[y, x].Length);

        return maxLengthsByColumn;
    }

    private static string ToFormattedText(this string[,] strings)
    {
        StringBuilder sb = new();
        int[] maxLengthsByColumn = GetMaxLengthsByColumn(strings);

        for (int y = 0; y < strings.GetLength(0); y++)
        {
            for (int x = 0; x < strings.GetLength(1); x++)
            {
                sb.Append(strings[y, x].PadRight(maxLengthsByColumn[x] + 2));
            }
            sb.AppendLine();
        }

        return sb.ToString();
    }


    private static string ToMarkdown(this string[,] strings)
    {
        StringBuilder sb = new();
        int[] maxLengthsByColumn = GetMaxLengthsByColumn(strings);

        for (int y = 0; y < strings.GetLength(0); y++)
        {
            for (int x = 0; x < strings.GetLength(1); x++)
            {
                sb.Append(strings[y, x].PadRight(maxLengthsByColumn[x]));
                if (x < strings.GetLength(1) - 1)
                    sb.Append(" | ");
            }
            sb.AppendLine();

            if (y == 0)
            {
                for (int i = 0; i < strings.GetLength(1); i++)
                {
                    int bars = maxLengthsByColumn[i] + 2;
                    if (i == 0)
                        bars -= 1;
                    sb.Append(new String('-', bars));

                    if (i < strings.GetLength(1) - 1)
                        sb.Append("|");
                }
                sb.AppendLine();
            }
        }

        return sb.ToString();
    }
}
```

</details>

```cs
Name       Age  Height
Oliver     23   1.91
Charlotte  19   1.62
Henry      42   1.72
Amelia     64   1.57
Owen       35   1.85
```

I can create similar methods to format a DataFrame as Markdown or HTML.

```text
Name      | Age | Height
----------|-----|--------
Oliver    | 23  | 1.91
Charlotte | 19  | 1.62
Henry     | 42  | 1.72
Amelia    | 64  | 1.57
Owen      | 35  | 1.85
```


Name      | Age | Height
----------|-----|--------
Oliver    | 23  | 1.91
Charlotte | 19  | 1.62
Henry     | 42  | 1.72
Amelia    | 64  | 1.57
Owen      | 35  | 1.85

## Using DataFrames in Interactive Notebooks

To get started using .NET workbooks, install the [.NET Interactive Notebooks extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.dotnet-interactive-vscode), create a new `demo.ipynb` file, then add your code.

Previously users had to create custom HTML formatters to properly display DataFrames in .NET Interactive Notebooks, but these days it works right out of the box.

> 💡 See [demo.html](https://swharden.com/static/2022/05/01/demo.html) for a full length demonstration notebook

```cs
// visualize the DataFrame
df
```

![](https://swharden.com/static/2022/05/01/dataframe-notebook.jpg)

## Append a Row

Build a new row using key/value pair then append it to the DataFrame

```cs
List<KeyValuePair<string, object>> newRowData = new()
{
    new KeyValuePair<string, object>("Name", "Scott"),
    new KeyValuePair<string, object>("Age", 36),
    new KeyValuePair<string, object>("Height", 1.65),
};

df.Append(newRowData, inPlace: true);
```

## Add a Column

Build a new column, populate it with data, and add it to the DataFrame

```cs
int[] weights = { 123, 321, 111, 121, 131 };
PrimitiveDataFrameColumn<int> weightCol = new("Weight", weights);
df.Columns.Add(weightCol);
```

## Sort and Filter

**The DataFrame class has numerous operations available** to sort, filter, and analyze data in many different ways. A popular pattern when working with DataFrames is to use _method chaining_ to combine numerous operations together into a single statement. See the [DataFrame Class API](https://docs.microsoft.com/en-us/dotnet/api/microsoft.data.analysis.dataframe) for a full list of available operations.

```cs
df.OrderBy("Name")
    .Filter(df["Age"].ElementwiseGreaterThan(30))
    .PrettyPrint();
```

```text
Name    Age  Height
Henry   42   1.72
Oliver  23   1.91
Owen    35   1.85
```

## Mathematical Operations

It's easy to perform math on columns or across multiple DataFrames. In this example we will perform math using two columns and create a new column to hold the output.

```cs
DataFrameColumn iqCol = df["Age"] * df["Height"] * 1.5;

double[] iqs = Enumerable.Range(0, (int)iqCol.Length)
    .Select(x => (double)iqCol[x])
    .ToArray();

df.Columns.Add(new PrimitiveDataFrameColumn<double>("IQ", iqs));
df.PrettyPrint();
```

```text
Name       Age  Height  IQ
Oliver     23   1.91    65.9
Charlotte  19   1.62    46.17
Henry      42   1.72    108.36
Amelia     64   1.57    150.72
Owen       35   1.85    97.12
```

## Statistical Operations

You can iterate across every row of a column to calculate population statistics

```cs
foreach (DataFrameColumn col in df.Columns.Skip(1))
{
    // warning: additional care must be taken for datasets which contain null
    double[] values = Enumerable.Range(0, (int)col.Length).Select(x => Convert.ToDouble(col[x])).ToArray();
    (double mean, double std) = MeanAndStd(values);
    Console.WriteLine($"{col.Name} = {mean} +/- {std:N3} (n={values.Length})");
}
```

```text
Age = 36.6 +/- 15.982 (n=5)
Height = 1.734 +/- 0.130 (n=5)
```


<details>
<summary>💡 View the full <code>MeanAndStd()</code> source code</summary>

```cs
private static (double mean, double std) MeanAndStd(double[] values)
{
	if (values is null)
		throw new ArgumentNullException(nameof(values));

	if (values.Length == 0)
		throw new ArgumentException($"{nameof(values)} must not be empty");

	double sum = 0;
	for (int i = 0; i < values.Length; i++)
		sum += values[i];

	double mean = sum / values.Length;

	double sumVariancesSquared = 0;
	for (int i = 0; i < values.Length; i++)
	{
		double pointVariance = Math.Abs(mean - values[i]);
		double pointVarianceSquared = Math.Pow(pointVariance, 2);
		sumVariancesSquared += pointVarianceSquared;
	}

	double meanVarianceSquared = sumVariancesSquared / values.Length;
	double std = Math.Sqrt(meanVarianceSquared);

	return (mean, std);
}
```

</details>

## Plot Values from a DataFrame

**I use [ScottPlot.NET](https://scottplot.net) to visualize data from DataFrames in .NET applications and .NET Interactive Notebooks.** ScottPlot can generate a variety of plot types and has many options for customization. See [the ScottPlot Cookbook](https://scottplot.net/cookbook/4.1/) for examples and API documentation.

```cs
// Register a custom formatter to display ScottPlot plots as images
using Microsoft.DotNet.Interactive.Formatting;
Formatter.Register(typeof(ScottPlot.Plot), (plt, writer) => 
    writer.Write(((ScottPlot.Plot)plt).GetImageHTML()), HtmlFormatter.MimeType);
```

```cs
// Get the data you wish to display in double arrays
double[] ages = Enumerable.Range(0, (int)df.Rows.Count).Select(x => Convert.ToDouble(df["Age"][x])).ToArray();
double[] heights = Enumerable.Range(0, (int)df.Rows.Count).Select(x => Convert.ToDouble(df["Height"][x])).ToArray();
```

```cs
// Create and display a plot
var plt = new ScottPlot.Plot(400, 300);
plt.AddScatter(ages, heights);
plt.XLabel("Age");
plt.YLabel("Height");
plt
```

![](https://swharden.com/static/2022/05/01/scottplot-notebook.png)

> 💡 See [demo.html](https://swharden.com/static/2022/05/01/demo.html) for a full length demonstration notebook

If you are only working inside a Notebook and you want all your plots to be HTML and JavaScript, [XPlot.Plotly](https://towardsdatascience.com/getting-started-with-c-dataframe-and-xplot-ploty-6ea6ce0ce8e3) is a good tool to use.

## Data may contain null

I didn't demonstrate it in the code examples above, but note that all column data types are nullable. While null-containing data requires extra considerations when writing mathematical routes, it's a convenient way to model missing data which is a common occurrence in the real world. 

## Why not just use LINQ?

I see this question asked frequently, often with an aggressive and condescending tone. LINQ (Language-Integrated Query) is fantastic for performing logical operations on simple collections of data. When you have large 2D datasets of _labeled_ data, advantages of data frames over flat LINQ statements start to become apparent. It is also easy to perform logical operations across multiple data frames, allowing users to write simpler and more readable code than could be achieved with LINQ statements. Data frames also make it much easier to visualize complex data too. In the data science world where complex labeled datasets are routinely compared, manipulated, merged, and visualized, often in an interactive context, the data frames are much easier to work with than raw LINQ statements.

## Conclusions

Although I typically reach for Python to perform exploratory data science, it's good to know that C# has a DataFrame available and that it can be used to inspect and manipulate tabular data. DataFrames pair well with [ScottPlot](https://scottplot.net) figures in interactive notebooks and are a great way to inspect and communicate complex data. I look forward to watching Microsoft's Data Analysis namespace continue to evolve as part of their machine learning / ML.NET platform.

## Resources

* [Example notebook for this project](https://swharden.com/static/2022/05/01/demo.html)

* [Source code for this project](https://github.com/swharden/Csharp-Data-Visualization/tree/main/projects/dataframe)

* [Official `Microsoft.Data.Analysis.DataFrame` Class Documentation](https://docs.microsoft.com/en-us/dotnet/api/microsoft.data.analysis.dataframe)

* [Microsoft.Data.Analysis source code](https://github.com/dotnet/machinelearning/tree/main/src/Microsoft.Data.Analysis) 

* [An Introduction to DataFrame](https://devblogs.microsoft.com/dotnet/an-introduction-to-dataframe/) (.NET Blog)

* [ExtremeOptimization DataFrame Quickstart](https://www.extremeoptimization.com/QuickStart/CSharp/DataFrames.aspx)

* [`Microsoft.Data.Analysis` on NuGet](https://www.nuget.org/packages/Microsoft.Data.Analysis/)

* [Getting Started With C# DataFrame and XPlot.Plotly](https://towardsdatascience.com/getting-started-with-c-dataframe-and-xplot-ploty-6ea6ce0ce8e3)

* [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)