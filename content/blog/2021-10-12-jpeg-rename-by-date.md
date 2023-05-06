---
title: Rename Image Files by Capture Date with C#
description: How to rename a folder of JPEGs by the creation date stored in their metadata
date: 2021-10-12 20:28:00
tags: ["csharp"]
---

# Rename Image Files by Capture Date with C# 

**I have hundreds of folders containing thousands of photographs I wish to move to a single directory.** Images are all JPEG format, but unfortunately they have filenames like `DSC_0123.JPG`. This means there are many identical filenames (e.g., every folder has a `DSC_0001.JPG`) and also the sorted list of filenames would not be in chronological order.

**JPEG files have an [Exif header](https://en.wikipedia.org/wiki/Exif) and most cameras store the acquisition date of photographs as metadata.** I wrote a C# application to scan a folder of images and rename them all by the date and time in their header. This problem has been solved many ways (googling reveals many solutions), but I thought I'd see what it looks like to solve this problem with C#. I reached for the [MetadataExtractor package](https://www.nuget.org/packages/MetadataExtractor/) on NuGet. My solution isn't fancy but it gets the job done.

```cs
foreach (string sourceImage in System.IO.Directory.GetFiles("../sourceFolder", "*.jpg"))
{
    DateTime dt = GetJpegDate(sourceImage);
    string fileName = $"{dt:yyyy-MM-dd HH.mm.ss}.jpg";
    string filePath = Path.Combine("../outputFolder", fileName);
    System.IO.File.Copy(sourceImage, filePath, true);
    Console.WriteLine($"{sourceImage} -> {filePath}");
}

DateTime GetJpegDate(string filePath)
{
    var directories = MetadataExtractor.ImageMetadataReader.ReadMetadata(filePath);

    foreach (var directory in directories)
    {
        foreach (var tag in directory.Tags)
        {
            if (tag.Name == "Date/Time Original")
            {
                if (string.IsNullOrEmpty(tag.Description))
                    continue;
                string d = tag.Description.Split(" ")[0].Replace(":", "-");
                string t = tag.Description.Split(" ")[1];
                return DateTime.Parse($"{d} {t}");
            }
        }
    }

    throw new InvalidOperationException($"Date not found in {filePath}");
}
```

```text
> dotnet run
DSC_0121.JPG -> 2016-09-30 21.51.25.jpg
DSC_0122.JPG -> 2016-10-03 21.42.05.jpg
DSC_0123.JPG -> 2016-10-09 23.04.05.jpg
DSC_0124.JPG -> 2016-10-09 23.05.48.jpg
DSC_0125.JPG -> 2016-11-30 23.07.56.jpg
DSC_0126.JPG -> 2017-01-01 19.16.56.jpg
DSC_0127.JPG -> 2017-01-01 19.17.09.jpg
```

## Resources
* [MetadataExtractor](https://www.nuget.org/packages/MetadataExtractor/)
* [ExifTool](https://exiftool.org/) seems to be a common solution
  * `exiftool -d '%Y%m%d-%H%M%%-03.c.%%e' '-filename<CreateDate' .`
* [JHead](https://www.sentex.ca/~mwandel/jhead/) is another common solution
  * `jhead -n%Y%m%d-%H%M%S *.jpg`