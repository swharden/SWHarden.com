---
title: GitHub Repository Badge
description: What I learned creating a github repo stats badge using HTML and Vanilla JS
date: 2022-04-12 23:00:00
tags: ["JavaScript", "GitHub"]
---

# GitHub Repository Badge

**I created a badge to dynamically display stats for any public GitHub repository using HTML and Vanilla JavaScript.** I designed it so anyone can have their own badge by copying two lines of HTML into their website. 

I don't write web frontend code often, so after getting this idea I decided to see how far I could take it. I treated this little project as an opportunity to get some experience exploring a stack I don't interact with often, and to see if I could take it all the way to something that would look nice and scale infinitely for free. This article documents what I learned along the way

<div class="text-center my-5">

<a href="http://github.com/ScottPlot/ScottPlot" id="github-stats-badge">GitHub</a>
<script src="https://swharden.github.io/repo-badge/badge.js" defer></script>

<a href='https://swharden.github.io/repo-badge/'>swharden.github.io/repo-badge</a>

</div>

```html
<!-- paste anywhere in your site -->
<a href="http://github.com/USER/REPO" id="github-stats-badge">GitHub</a>
<script src="https://swharden.github.io/repo-badge/badge.js" defer></script>
```

## How it Works

* Because [`defer` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-defer) is defined in the `script` element, the JavaScript will not run until after the page loads. This ensures all the elements it will interact with are present in memory before it starts editing the DOM. Note that the HTML added by the user is a link to the GitHub project, so even if the JS fails completely this link is still functional and useful.

* The `a` with id `github-stats-badge` is identified and the `href` is read to determine the user and name of the repository to display on the badge

* CSS is assembled in a `style` element and appended to the `head`

* JavaScript deletes the content of the original `a` and replaces it with nested `div`, `a`, and `span` elements to build the badge in the DOM dynamically. Each stats block is hidden by settings its `opacity` to zero, preventing the user from seeing elements before they are filled with real data. This also fills-out the dimensions of the badge to prevent the page from shifting as its components are loaded individually.

* Asynchronous requests are sent to [GitHub's RESTful API](https://docs.github.com/en/rest) endpoints using [`fetch()`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) and the JSON responses are parsed to get the latest release tag, star count, and number of forks
  * https://api.github.com/repos/USER/REPO
  * https://api.github.com/repos/USER/REPO/releases/latest

* Information from the API is loaded into `span` elements and the `opacity` is set to one (with [CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions)) so it fades in _after_ the HTTP request returns a valid result. The fade-in effect makes the delayed appearance seem intentional, when in reality it's just buying time for the HTTP request to complete its round-trip. Without this fade, the rapid appearance of text (or the replacement of dummy text with real values) is much more jarring.

### Example Fetch

I expect the HTTP request to return a JSON document with a `tag_name` element, but if not I build my own object containing this object (filed with dummy data) and pass it along. 

The display code (which sets the text, increases opacity, and sets the link) doesn't actually know whether the request succeeded or failed.

This is how I ensure the badge is always left in a presentable state.

```js
fetch(`https://api.github.com/repos/${user}/${repo}/releases/latest`)
    .then(response => { 
        return response.ok ? response.json() : { "tag_name": "none" };
    })
    .then(data => {
        const tag = document.getElementById('github-stats-badge--tag');
        tag.getElementsByTagName("span")[0].innerText = data.tag_name;
        tag.style.opacity = 1;
        tag.href = repoLinkUrl + "/releases";
    });
```

### Fading

I don't use CSS fading that often, but I found it produced a fantastic result here. Here's the magic bit of CSS that enables fading effects as JavaScript twiddles the `opacity`

```css
#github-stats-badge a {
    color: black;
    text-decoration: none;
    opacity: 0;
    transition: opacity .5s ease-in-out;
}

#github-stats-badge a:hover {
    color: #003366;
}
```

## SVG Icons

GitHub has official MIT-licensed icons available as SVG files. These are fantastic because you can view their source and it's plain text! You can copy that plain text directly into a HTML document, or in my case wrap it in JavaScript so I can serve it dynamically.

* https://github.com/primer/octicons/

I store the `path` attribute contents as a JavaScript string like this

```js
const githubStatusBadge_tagPath = "M2.5 7.775V2.75a.25.25 0 01.25-.25h5.025a.25.25 0 01.177.073l6.25 \
    6.25a.25.25 0 010 .354l-5.025 5.025a.25.25 0 01-.354 0l-6.25-6.25a.25.25 0 01-.073-.177zm-1.5 0V2.75C1 \
    1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 010 2.474l-5.026 5.026a1.75 \
    1.75 0 01-2.474 0l-6.25-6.25A1.75 1.75 0 011 7.775zM6 5a1 1 0 100 2 1 1 0 000-2z";
```

Then I create a function to build a SVG image from a `path`

```js
function githubStatusBadge_createSVG(svgPath) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    svg.setAttribute('width', '16');
    svg.setAttribute('height', '16');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.style.verticalAlign = 'bottom';
    svg.style.marginRight = "2px";

    const path = document.createElementNS("http://www.w3.org/2000/svg", 'path');
    path.setAttribute('fill-rule', 'evenodd');
    path.setAttribute('d', svgPath);
    svg.appendChild(path);

    return svg;
}
```

Note that the `NS` method and `xmlns` attribute are critical for SVG elements to work in the browser. For more information check out Mozilla's [Namespaces crash course
](https://developer.mozilla.org/en-US/docs/Web/SVG/Namespaces_Crash_Course).

## Minification

The non-minified plain-text JavaScript file is less than 8kb. This could be improved by minification and/or gzip compression, but I may continue to choose not to do this.

I appreciate HTML and JS which is human readable, especially when it was human-written by hand. Perhaps a good compromise would be to offer `badge.js` and `badge.min.js`, but even this would add complexity by necessitating a build step which is not currently required.

## GitHub Pages

I organized this project so it could be served using [GitHub Pages](https://pages.github.com/). Basically you just check a box on the GitHub repository settings page, then `docs/index.html` will be displayed when you go to `USER.github.io/REPO` in a browser. Building/publishing is performed automatically using GitHub Actions, and it works immediately without having to manually create a workflow yaml file.

Although GitHub pages supports a fancy markdown-based flat-file static website generation using [Jekyll](https://jekyllrb.com/), I chose to create a project page using hand-crafted HTML, CSS, and Vanilla JS with no framework of build system. [Web0](https://web0.small-web.org/) for the win!

GitHub stores and serves the content (with edge caching) so I'm protected in the unlikely case where this project goes viral and millions of people start downloading my JavaScript file. GitHub will scale horizontally as needed to infinity to meet the demand from increased traffic, and all the services I'm using are free.

## New Website Checklist

Although the project page is simple, I wanted it to look nice. There are so many things to consider when making a new webpage! Here are a few that make my list, and most of them don't apply to this small one-page website but I thought I'd share my whole list anyway.

* ✔️ Populate `title` and `meta description`
* ✔️ Add metric analysis (Google Analytics)
* ❌ Add ads where appropriate (Google AdSense)
* ❌ Add a RSS feed
* ❌ Add a sitemap
* ❌ Create a custom 404 page
* ❌ Place `noindex` attributes on special pages
* ✔️ Create a 32x32 transparent `favicon.ico`
* ❌ Create [additional favicons](https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs)
* ✔️ Create a 1200 x 630 px [Open Graph image](https://ogp.me/)
* ✔️ Add twitter and facebook cards
* ✔️ Verify OG previews look good using [opengraph.xyz](https://www.opengraph.xyz/)
* ✔️ Confirm the site looks good on mobile (chrome dev tools)
* ✔️ Set the meta `theme-color` to color the mobile address bar
* ❌ Define 404 and permissions in `.htaccess`
* ✔️ Check accessibility and performance in LightHouse

Here's the Open Graph banner I came up with:

<img src="banner.png" class="d-inline-block mx-auto">

## Conclusions

**Altogether the project page looks great and the badge seems to function as expected!** I'll continue to watch the repository so if anyone opens an issue or creates a pull request offering improvements I will be happy to review it.

This little Vanilla JS project touched a lot of interesting corners of web frontend development, and I'm happy I got to explore them today!

If you like this project, [give it a star! 🌟](https://github.com/swharden/repo-badge)

## Resources
* [GitHub Repo Badge Website](https://swharden.github.io/repo-badge/)
* [GitHub Repo Badge GitHub Project](https://github.com/swharden/repo-badge)
* This project was inspired by [GitHub Buttons](https://buttons.github.io)