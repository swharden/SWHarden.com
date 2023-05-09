---
title: Display Build Details in Client-Size Blazor Apps
date: 2020-12-29 19:54:00
tags: ["csharp", "blazor"]
---



I find it useful to add build date and .NET version to the bottom of my client-side applications. Something like:

> MyApp version 1.2.3 | Built on December 29, 2020 | Running on .NET 5.0.1

I'm documenting how I do this so I can refer to it later, and also so it may be helpful to others.

```cs
@page "/"

<h1>New Blazor App</h1>
<div>App version @AppVersion</div>
<div>Running on .NET @Environment.Version</div>

@code{
	private string AppVersion
	{
		get
		{
			Version version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version;
			return $"{version.Major}.{version.Minor}.{version.Build}";
		}
	}
}
```

## Build Date

You can't access build date entirely from code, but you _can_ create a file containing the build date on every build then consume that file as a resource.

**Step1: Add a pre-build instruction**
* Right-click the project and select "Properties"
* Navigate to the "Build Events" section
* Add a pre-build command: `echo %date% %time% > "$(ProjectDir)\Resources\BuildDate.txt"`
* Rebuild the application

> ⚠️ This command assumes you are building on Windows

**Step2: Add the date file as a resource**
* Right-click the project and select "Properties"
* Navigate to the "Resources" section
* Click "Add Resource", select "Add existing file", and choose the new text file

**Step3: Reference the build date resource in code**

```cs
private string BuildDateString => 
    DateTime.Parse(Properties.Resources.BuildDate).ToString("MMMM dd, yyyy");
```
