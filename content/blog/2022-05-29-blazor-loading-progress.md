---
title: Show A Progress Bar as your Blazor App Loads
description: How to add a progress bar to your client-side Blazor WebAssembly app to indicate page load progress.
date: 2022-05-29 16:05:00
tags: ["blazor", "csharp"]
featured_image: https://swharden.com/static/2022/05/29/blazor-load-progress-v2.gif
---



**Today I created a Blazor WebAssembly app that shows a progress bar while the page loads.** This is especially useful for users on slow connections because Blazor apps typically require several megabytes of DLL and DAT files to be downloaded before meaningful content appears on the page.

Live Demo: [LJPcalc](https://swharden.com/LJPcalc/) ([source code](https://github.com/swharden/LJPcalc))

<img src="https://swharden.com/static/2022/05/29/blazor-load-progress-v2.gif" class="mx-auto d-block border shadow my-5">

## Step 1: Add a progress bar

Edit index.html and identify your app's main div:

```html
<div id="app">Loading...</div>
```

Add a progress bar inside it:
```html
<div id="app">
	<h2>Loading...</h2>
	<div class="progress mt-2" style="height: 2em;">
		<div id="progressbar" class="progress-bar progress-bar-striped progress-bar-animated"
			style="width: 10%; background-color: #204066;"></div>
	</div>
	<div>
		<span id="progressLabel" class="text-muted">Downloading file list</span>
	</div>
</div>
```

See [Bootstrap's progressbar page](https://getbootstrap.com/docs/5.2/components/progress/) for extensive customization and animation options and best practices when working with progress indicators. Also ensure the version of Bootstrap in your Blazor app is consistent with the documentation/HTML you are referencing.

## Step 2: Disable Blazor AutoStart

Edit index.html and identify where your app loads Blazor resources:

```html
<script src="https://swharden.com/static/2022/05/29/_framework/blazor.webassembly.js"></script>
```

Update that script so it does _not_ download automatically:
```html
<script src="https://swharden.com/static/2022/05/29/_framework/blazor.webassembly.js" autostart="false"></script>
```

## Step 3: Create a Blazor Startup Script

Add a script to the bottom of the page to start Blazor manually, identifying all the resources needed and incrementally downloading them while updating the progressbar along the way.

```html
<script>
	function StartBlazor() {
		let loadedCount = 0;
		const resourcesToLoad = [];
		Blazor.start({
			loadBootResource:
				function (type, filename, defaultUri, integrity) {
					if (type == "dotnetjs")
						return defaultUri;

					const fetchResources = fetch(defaultUri, {
						cache: 'no-cache',
						integrity: integrity,
						headers: { 'MyCustomHeader': 'My custom value' }
					});

					resourcesToLoad.push(fetchResources);

					fetchResources.then((r) => {
						loadedCount += 1;
						if (filename == "blazor.boot.json")
							return;
						const totalCount = resourcesToLoad.length;
						const percentLoaded = 10 + parseInt((loadedCount * 90.0) / totalCount);
						const progressbar = document.getElementById('progressbar');
						progressbar.style.width = percentLoaded + '%';
						const progressLabel = document.getElementById('progressLabel');
						progressLabel.innerText = `Downloading ${loadedCount}/${totalCount}: ${filename}`;
					});

					return fetchResources;
				}
		});
	}

	StartBlazor();
</script>
```

## Resources

* [ASP.NET Core Blazor startup](https://docs.microsoft.com/en-us/aspnet/core/blazor/fundamentals/startup) describes the `Blazor.start()` process and `loadBootResource()`.

* Code here inspired by [@EdmondShtogu's comment](https://github.com/dotnet/aspnetcore/issues/25165#issuecomment-781683925) on [dotnet/aspnetcore #25165](https://github.com/dotnet/aspnetcore/issues/25165) from Feb 18, 2021