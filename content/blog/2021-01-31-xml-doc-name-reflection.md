---
Title: Reflection and XML Documentation in C# 
Description: How to access XML documentation from within a C# application
Date: 2021-01-31 13:57:00
tags: ["csharp"]
---

# Reflection and XML Documentation in C# 

**In C#, you can document your code using XML directly before code blocks.** This XML documentation is used by Visual Studio to display tooltips and provide autocomplete suggestions. 

```cs
/// <summary>
///  This method performs an important function.
/// </summary>
public void MyMethod() {}
```

**To enable automatic generation of XML documentation** on every build, add the following to your csproj file:

```xml
<PropertyGroup>
  <DocumentationFile>MyProgram.xml</DocumentationFile>
</PropertyGroup>
```

**However, XML documentation is not actually metadata, so it is not available in the compiled assembly.** In this post I'll show how you can use `System.Reflection` to gather information about methods and combine it with documentation from an XML file read with `System.Xml.Linq.XDocument`. 

**I find this useful for writing code which automatically generates documentation.** Reflection alone cannot provide comments, and XML documentation alone cannot provide parameter names (just their types). By combining reflection with XML documentation, we can more completely describe methods in C# programs.

> **⚠️ WARNING: These code examples are intentionally simple.** They only demonstrate how to read summary comments from XML documentation for methods found using reflection. Additional functionality can be added as needed, and my intent here is to provide a simple starting point rather than overwhelmingly complex examples that support all features and corner cases.

> **💡 Source code** can be downloaded at the bottom of this article

> **✔️ The "hack" described on this page is aimed at overcoming limitations of partially-documented XML. A better solution is to fully document your code, in which case the XML document is self-sufficient.** The primary goal of these efforts is to use XML documentation where it is present, but use Reflection to fill in the blanks about methods which are undocumented or only partially documented. Perhaps a better strategy would be to have a fully documented code base, with an XML file containing `<summary>`, `<returns>`, and `<param>` for every parameter. Tests can ensure this is and remains the case.

## What does the XML Documentation look like?

There are some nuances here you might not expect, especially related to arrays, generics, and nullables. Let's start with a demo class with documented summaries. Keep in mind that the goal of this project is to help use Reflection to fill in the blanks about undocumented or partially-documented code, so this example will only add a `<summary>` but no `<param>` descriptions.

### DemoClass.cs

```cs
/// <summary>
/// Display a name
/// </summary>
public static void ShowName(string name)
{
    Console.WriteLine($"Hi {name}");
}

/// <summary>
/// Display a name a certain number of times
/// </summary>
public static void ShowName(string name, byte repeats)
{
    for (int i = 0; i < repeats; i++)
        Console.WriteLine($"Hi {name}");
}

/// <summary>
/// Display the type of the variable passed in
/// </summary>
public static void ShowGenericType<T>(T myVar)
{
    Console.WriteLine($"Generic type {myVar.GetType()}");
}

/// <summary>
/// Display the value of a nullable integer
/// </summary>
public static void ShowNullableInt(int? myInt)
{
    Console.WriteLine(myInt);
}
```

### XML Documentation File

There are a few important points to notice here:

* Each method is a `member` with a `name` starting with `M:`
* Parameter _types_ are in the member name, but not parameter _names_!
* Parameters might be listed in the XML, but they will be missing if only `<summary>` was added in code
* 💡 The key step required to connect a reflected method with its XML documentation is being able to determine the XML method name of that method. How to do this is discussed below...

```xml
<?xml version="1.0"?>
<doc>
    <assembly>
        <name>XmlDocDemo</name>
    </assembly>
    <members>
        <member name="M:XmlDocDemo.DemoClass.ShowName(System.String)">
            <summary>
            Display a name
            </summary>
        </member>
        <member name="M:XmlDocDemo.DemoClass.ShowName(System.String,System.Byte)">
            <summary>
            Display a name a certain number of times
            </summary>
        </member>
        <member name="M:XmlDocDemo.DemoClass.ShowGenericType``1(``0)">
            <summary>
            Display the type of the variable passed in
            </summary>
        </member>
        <member name="M:XmlDocDemo.DemoClass.ShowNullableInt(System.Nullable{System.Int32})">
            <summary>
            Display the value of a nullable integer
            </summary>
        </member>
    </members>
</doc>
```

### XML Name Details

* Generics from types have a single <code>`</code> character 
* Generics from methods have double <code>``</code> characters
* If the parameter is by "ref" then you need to pre-pend the `@` character
* If the parameter is a pointer you need to pre-pend it with the <code>*</code> character
* If the parameter is an array, you need to add `[]` characters and the appropriate number of commas
* If the parameter is Nullable it will be wrapped in `System.Nullable{}`
* If the method is MethodInfo is a casing operator, then you need to pre-pend it with `~` character

_Thanks [Zachary Patten](https://github.com/ZacharyPatten) for sharing these details in an [MSDN article](https://docs.microsoft.com/en-us/archive/msdn-magazine/2019/october/csharp-accessing-xml-documentation-via-reflection) and e-mail correspondence_

## Read XML Documentation File

This code reads the XML documentation file (using the modern [XDocument](https://docs.microsoft.com/en-us/dotnet/api/system.xml.linq.xdocument)) and stores method summaries in a Dictionary using the XML method name as a key. This dictionary will be accessed later to look-up documentation for methods found using Reflection.

```cs
private readonly Dictionary<string, string> MethodSummaries = new Dictionary<string, string>();

public XmlDoc(string xmlFile)
{
    XDocument doc = XDocument.Load(xmlFile);
    foreach (XElement element in doc.Element("doc").Element("members").Elements())
    {
        string xmlName = element.Attribute("name").Value;
        string xmlSummary = element.Element("summary").Value.Trim();
        MethodSummaries[xmlName] = xmlSummary;
    }
}
```

## Determine XML Method Name for a Reflected Method

This example code returns the XML member name for a method found by reflection. **This is the key step** required to connect reflected methods with their descriptions in XML documentation files.

**⚠️ Warning: This code sample may not support all corner-cases**, but in practice I found it supports all of the ones I typically encounter in my code bases and it's a pretty good balance between functionality and simplicity.

```cs
public static string GetXmlName(MethodInfo info)
{
	string declaringTypeName = info.DeclaringType.FullName;

	if (declaringTypeName is null)
		throw new NotImplementedException("inherited classes are not supported");

	string xmlName = "M:" + declaringTypeName + "." + info.Name;
	xmlName = string.Join("", xmlName.Split(']').Select(x => x.Split('[')[0]));
	xmlName = xmlName.Replace(",", "");

	if (info.IsGenericMethod)
		xmlName += "``#";

	int genericParameterCount = 0;
	List<string> paramNames = new List<string>();
	foreach (var parameter in info.GetParameters())
	{
		Type paramType = parameter.ParameterType;
		string paramName = GetXmlNameForMethodParameter(paramType);
		if (paramName.Contains("#"))
			paramName = paramName.Replace("#", (genericParameterCount++).ToString());
		paramNames.Add(paramName);
	}
	xmlName = xmlName.Replace("#", genericParameterCount.ToString());

	if (paramNames.Any())
		xmlName += "(" + string.Join(",", paramNames) + ")";

	return xmlName;
}

private static string GetXmlNameForMethodParameter(Type type)
{
	string xmlName = type.FullName ?? type.BaseType.FullName;
	bool isNullable = xmlName.StartsWith("System.Nullable");
	Type nullableType = isNullable ? type.GetGenericArguments()[0] : null;

	// special formatting for generics (also Func, Nullable, and ValueTulpe)
	if (type.IsGenericType)
	{
		var genericNames = type.GetGenericArguments().Select(x => GetXmlNameForMethodParameter(x));
		var typeName = type.FullName.Split('`')[0];
		xmlName = typeName + "{" + string.Join(",", genericNames) + "}";
	}

	// special case for generic nullables
	if (type.IsGenericType && isNullable && type.IsArray == false)
		xmlName = "System.Nullable{" + nullableType.FullName + "}";

	// special case for multidimensional arrays
	if (type.IsArray && (type.GetArrayRank() > 1))
	{
		string arrayName = type.FullName.Split('[')[0].Split('`')[0];
		if (isNullable)
			arrayName += "{" + nullableType.FullName + "}";
		string arrayContents = string.Join(",", Enumerable.Repeat("0:", type.GetArrayRank()));
		xmlName = arrayName + "[" + arrayContents + "]";
	}

	// special case for generic arrays
	if (type.IsArray && type.FullName is null)
		xmlName = "``#[]";

	// special case for value types
	if (xmlName.Contains("System.ValueType"))
		xmlName = "`#";

	return xmlName;
}
```

## Get XML Documentation for a Reflected Method

Now that we have `XmlName()`, we can easily iterate through reflected methods and get their XML documentation.

```cs
// use Reflection to get info from custom methods
var infos = typeof(DemoClass).GetMethods()
                             .Where(x => x.DeclaringType.FullName != "System.Object")
                             .ToArray();

// display XML info about each reflected method
foreach (MethodInfo mi in infos)
{
    string xmlName = XmlName(mi);
    Console.WriteLine("");
    Console.WriteLine("Method: " + XmlDoc.MethodSignature(mi));
    Console.WriteLine("XML Name: " + xmlName);
    Console.WriteLine("XML Summary: " + MethodSummaries[xmlName]);
}
```

### Output

```
Method: XmlDocDemo.DemoClass.ShowName(string name)
XML Name: M:XmlDocDemo.DemoClass.ShowName(System.String)
XML Summary: Display a name

Method: XmlDocDemo.DemoClass.ShowName(string name, byte repeats)
XML Name: M:XmlDocDemo.DemoClass.ShowName(System.String,System.Byte)
XML Summary: Display a name a certain number of times

Method: XmlDocDemo.DemoClass.ShowGenericType<T>(T myVar)
XML Name: M:XmlDocDemo.DemoClass.ShowGenericType``1(``0)
XML Summary: Display the type of the variable passed in

Method: XmlDocDemo.DemoClass.ShowNullableInt(int? myInt)
XML Name: M:XmlDocDemo.DemoClass.ShowNullableInt(System.Nullable{System.Int32})
XML Summary: Display the value of a nullable integer
```

## Resources

### Source Code

A simple-case working demo of these concepts can be downloaded here:

* [**XmlDocDemo.zip**](XmlDocDemo.zip) (4kb)

### Documentation Generators

* [DocFX](https://dotnet.github.io/docfx/) - An extensible and scalable static documentation generator.

* [Sandcastle](https://github.com/EWSoftware/SHFB) - Sandcastle Help File Builder (SHFB). A standalone GUI, Visual Studio integration package, and MSBuild tasks providing full configuration and extensibility for building help files with the Sandcastle tools.

### Zachary Patten's Useful Article

There is an extensive article on this topic in the October 2019 issue of MSDN Magazine, [Accessing XML Documentation via Reflection](https://docs.microsoft.com/en-us/archive/msdn-magazine/2019/october/csharp-accessing-xml-documentation-via-reflection) by [Zachary Patten](https://github.com/ZacharyPatten). The code examples there provide a lot of advanced features, but are technically incomplete and some critical components are only shown using pseudocode. The reader is told that full code is available as part of the author's library [Towel](https://github.com/ZacharyPatten/Towel), but this library is extensive and provides many functions unrelated to reflection and XML documentation making it difficult to navigate. The method to convert a method to its XML documentation name is [Towel/Meta.cs#L1026-L1092](https://github.com/ZacharyPatten/Towel/blob/360b4ae695c5f95ca9b8e1ec3c466092eeff972e/Sources/Towel/Meta.cs#L1026-L1092), but it's coupled to other code which requires hash maps to be pre-formed in order to use it. My post here is intended to be self-contained simple reference for how to combine XML documentation with Reflection, but users interested in reading further on this topic are encouraged to read Zachary's article.

## Update: Potentially Useful Libraries

**Update (Feb 21, 2021):** I continued to do research on this topic. I thought I'd find a "golden bullet" library that could help me do this perfectly. The code above does a pretty good job, but I would feel more confident using something designed/tested specifically for this task. I looked and found some helpful libraries, but none of them met all me needs. For my projects, I decided just to use the code above.

### DocXml

[DocXml](https://github.com/loxsmoke/DocXml) is a small .NET standard 2.0 library of helper classes and methods for compiler-generated XML documentation retrieval. Its API is very simple and easy to use with a predictive IDE. Out of the box though it was unable to properly identify the XML name of one of my functions. I think it got stuck on the generic method with a multi-dimensional generic array as an argument, but don't recall for sure. For basic code bases, this looks like a fantastic library.

### NuDoq

[NuDoq](https://github.com/devlooped/NuDoq) (previously NuDoc?) is a standalone API to read and write .NET XML documentation files and optionally augment it with reflection information. According to the [releases](https://github.com/devlooped/NuDoq/releases) it was actively worked on around 2014, then rested quietly for a few years and new releases began in 2021. NuDoq looks quite extensive, but takes some studying before it can be used effectively. "Given the main API to traverse and act on the documentation elements is through the visitor pattern, the most important part of the API is knowing the types of nodes/elements in the visitable model."

### Towel

[Towel](https://github.com/ZacharyPatten/Towel) is a .NET library intended to add core functionality and make advanced topics as clean and simple as possible. Towel has tools for working with data structures, algorithms, mathematics, metadata, extensions, console, and more. Towel favors newer coding practices over maintaining backwards compatibility, and at the time of writing Towel only supports .NET 5 and newer. One of Towel's `Meta` module has methods to get XML names for reflected objects. It's perfect, but requires .NET 5.0 or newer so I could not use it in my project.

### Washcloth

I tried to create a version of Towel that isolated just the XML documentation reflection module so I could back-port it to .NET Standard. I created [Washcloth](https://github.com/swharden/Washcloth) which largely achieved this and wrapped Towel behind a simple API. This task proved extremely difficult to accomplish cleanly though, because most modules in the Towel code base are highly coupled to one another so it was very difficult to isolate the `Meta` module and I never achieved this goal to my satisfaction. I named the project Washcloth because a washcloth is really just a small towel with less functionality. Washcloth technically works (and can be used in projects back to .NET Core 2.0 and .NET Framework 4.6.1), but so much coupled code from the rest of Towel came along with it that I decided not to use this project for my application.

## Final Thoughts

After a month poking around at this, here's where I landed:

* Reading XML documentation is easy with `System.Xml.Linq.XDocument`

* Getting XML names for fields, properties, classes, constructors, and enumerations is easy

* Getting XML names for methods can be very hard

* If you're creating something special, consider a custom solution like that shown above (~50 lines and you're done).

* If you can target the latest .NET platform, consider the `Meta` module in [Towel](https://github.com/ZacharyPatten/Towel)

* If you want a package that targets .NET Standard, consider [DocXml](https://github.com/loxsmoke/DocXml) (simple) or [NuDoq](https://github.com/devlooped/NuDoq) (complex)