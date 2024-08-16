---
title: GitHub License Checker
description: A tool for checking the license key for all of your GitHub repositories
Date: 2024-08-17 19:45:00
tags: ["github", "JavaScript"]
---

**Adding a permissive license to your open source projects makes it easy for others to benefit from reusing your code.** I typically recommend the MIT license for most projects because it's simple, well understood, and allows the code to be used for essentially any purpose. Using code from websites and GitHub repositories without a license is difficult, because as I understand it the default terms are "all rights reserved" by the copyright holder unless explicitly stated otherwise. Since not having a license puts restrictions on how others may use your code, I created the [**GitHub License Checker**](https://swharden.com/github-license-checker/) tool to help identify GitHub repositories with missing license files.

**Launch: https://swharden.com/github-license-checker/**

[![](https://swharden.com/static/2024/08/29/checker.png)](https://swharden.com/github-license-checker/)

**It's a Vanilla JavaScript app that works by hitting the paginated "repos" GitHub API for a given username.** Because a page has up to 100 repositories and most users are unlikely to have more than a few hundred repositories, the API rate limiting is rarely engaged so a GitHub API key is not required.

```
https://api.github.com/users/<USER>/repos?per_page=100&page=1
```

**The GitHub repositories API returns a lot of useful information.** Because it's so easy to use client-side without an API key, I'm curious what other useful tools could be created using it. Perhaps <a href='https://scottplot.net'>ScottPlot</a> could be used to generate some interesting charts. Ideas that jump out are plotting every repo's star count vs size, or date vs number of commits. I'll leave that for another day, but C# developers should note that the [Octokit NuGet Package](https://www.nuget.org/packages/Octokit) is an official .NET package for interacting with the GitHub API.

### Resources
* [ChooseALicense.com](https://choosealicense.com/)
* GitHub License Checker [Source on GitHub](https://github.com/swharden/GitHub-License-Checker)