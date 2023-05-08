---
title: Create a new .NET 5 Blazor Project
date: 2021-01-06 19:39:00
tags: ["blazor", "csharp"]
---



**When Visual Studio 2019 creates a new Blazor app it defaults to .NET Standard 2.1**. A few months ago .NET 5 was released, and upgrading Blazor apps to use .NET 5 has many strong performance improvements. I'm sure a Visual Studio update will soon make this easier, but for now to create a new .NET Blazor app running .NET 5 I use these steps:

* Create a new .NET core 3.1 Blazor App
* Edit the csproj file
  * Change SDK from `Microsoft.NET.Sdk.Web` to `Microsoft.NET.Sdk.BlazorWebAssembly`
  * Remove `RazorLangVersion` 
  * Update `TargetFramework` from `netstandard2.1` to `net5.0`
  * Remove the `Microsoft.AspNetCore.Components.WebAssembly.Build` package reference
* update all NuGet packages to their latest versions

Extensive details can be found on Microsoft's official [Migrate from ASP.NET Core 3.1 to 5.0](https://docs.microsoft.com/en-us/aspnet/core/migration/31-to-50?view=aspnetcore-5.0&tabs=visual-studio#update-blazor-webassembly-projects) documentation page, but I find this short list of steps easier to refer to.

## Download a New .NET 5.0.1 Blazor App

Here is a new project running .NET 5.0.1 with Bootstrap 5.0 alpha:

* [**NewBlazorApp-net5.0.1.zip**](https://swharden.com/static/2021/01/06/NewBlazorApp-net5.0.1.zip)

To change the project name/namespace:
* Rename the `.sln` and `.csproj` files
* Update the `.sln` file in a text editor to match the new filenames
* Update the namespace in `Program.cs`
* Update the namespaces in `_Imports.razor`