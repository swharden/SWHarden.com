---
title: Merge External Repositories into GitHub Contribution Graph
description: How I import anonymized commits from untracked repositories to keep my green squares current
Date: 2026-03-05 01:15:00
tags: ["csharp", "git", "github"]
---

**I enjoy gazing at the green squares in my GitHub Contribution Graph as a way to visualize the ebbs and flows of my development efforts [over the last decade](https://github.com/swharden).** However, I've been working more in repositories on other platforms (GitLab, Azure, and locally) which are not tracked by GitHub and do not contribute to their activity graph. I sought a solution to reclaim those hard-earned green squares!

**This page documents how I created an anonymized git activity aggregator** that integrates commits across various untracked git repositories into a single private repo that can be used to accurately reflect my total development effort as green squares on GitHub's Contribution Graph.

## Results

<div class="my-4">
<strong>Before Merge:</strong> There is a sharp decrease in commits in April when I started committing to untracked repositories.
<a href="https://swharden.com/static/2026/03/05/2025-before.png" target="_blank">
<img src="https://swharden.com/static/2026/03/05/2025-before.png" class="my-0 py-0">
</a>
</div>

<strong>After Merge:</strong> Activity continues through April, and the high effort near the end of the year is visible.
<a href="https://swharden.com/static/2026/03/05/2025-after.png" target="_blank">
<img src="https://swharden.com/static/2026/03/05/2025-after.png" class="my-0 py-0">
</a>

## Implementation Overview
The code itself isn't too complex, leaned heavily on the [libgit2sharp](https://github.com/libgit2/libgit2sharp) .NET package, and its [source code is available](https://github.com/swharden/Git-Commit-Aggregator) so I'll describe what it does at a high level:

* Scan a folder of git repositories to identify all repos to analyze
* Scan the commit history of each git repo to generate an array of `DateTime`
* Optionally restrict commits to those matching a given name or email address
* Merge all commit `DateTime` values across all repos into a single collection
* I used an intermediate step where commit dates were stored as text files
* Create a new git repo locally and add one empty commit per `DateTime` value
* Create a new git repo in GitHub, set it as the origin for the local one, and push to it
* Anonymity is preserved by only extracting commit timestamps and storing them in a private repo
* The GitHub activity graph will now include squares for the aggregated commits
* To update the graph, re-run the application and force push the repo with the empty commits

## Future Directions
**This strategy could be extended to provide extensive analytics for multiple users working across large multi-project code bases.** Although the present implementation aimed to preserve anonymity of the analyzed source code, extending commit analysis records to include repository name, commit messages, and author details could facilitate generation of fascinating reports where users can be seen working across different projects at different times. Consider what an activity graph would look like for a single user if each square were colored according to the repo they were working in, or a graph that shows a single repo with different authors represented by different squares. The simplicity of the git analysis methods described here make graphs like these feasible to realize without much additional effort.

## Additional Resources
* Although I wrote a C# app to analyze git repos and create them from scratch, the heavy lifting was performed by the [libgit2sharp](https://github.com/libgit2/libgit2sharp) .NET package
* [Git-Commit-Aggregator](https://github.com/swharden/Git-Commit-Aggregator) (source code on GitHub)
* Multi-Year activity graphs: [before](https://swharden.com/static/2026/03/05/before.png) and [after](https://swharden.com/static/2026/03/05/after.png)
* https://github.com/swharden (my GitHub page showing my contribution graph)