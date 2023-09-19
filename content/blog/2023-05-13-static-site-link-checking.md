---
title: Static Site Broken Link Detection
description: How to check for broken links and images across large static websites
Date: 2023-05-13 13:39:00
tags: ["python", "hugo"]
featured_image: https://swharden.com/static/2023/05/13/report2.png
---

**This website is a static site containing thousands of pages, and I recently had the desire to check all of them for broken links and images.** Although it would be a tedious task to perform manually, I was able to automate the process using Python. This page describes the process I used to identify broken links and images and may be helpful to others using static site generator tools like [Jekyll](https://jekyllrb.com/), [Hugo](https://gohugo.io/), [Eleventy](https://www.11ty.dev/), [Pelican](https://getpelican.com/), [Gatsby](https://www.gatsbyjs.com/), other [Jamstack site generators](https://jamstack.org/generators/), or hand-written HTML files.

## Scraping Link and Image URLs

**Although my website content is stored as markdown files, I found it most convenient to check the generated HTML files for broken link and image URLs.** I generated my static site locally, then manually removed pagination folders so only article HTML files were present. I then wrote the following Python script which uses [`pathlib`](https://docs.python.org/3/library/pathlib.html) to locate HTML files and [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to analyze `a href` and `img src` attributes and saves all URLs identified as a CSV file.

```py
import pathlib
from bs4 import BeautifulSoup


def get_urls(file: pathlib.Path) -> list:
    """Return link and image URLs in a HTML file"""
    with open(file, errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith("#"):
            continue
        if "#" in href:
            href = href.split("#")[0]
        href = str(href).strip('/')
        urls.add(href)

    for image in soup.find_all('img'):
        src = image.get('src')
        urls.add(str(src))

    return sorted(list(urls))


def get_urls_by_page(folder: pathlib.Path) -> dict:
    """Return link and image URLs for all HTML files in a folder"""
    html_files = list(folder.rglob("*.html"))
    urls_by_page = {}
    for i, html_file in enumerate(html_files):
        urls = get_urls(html_file)
        urls_by_page[html_file] = urls
        print(f"{i+1} of {len(html_files)}: {len(urls)} URLs found in {html_file}")
    return urls_by_page


def write_csv(urls_by_page: dict, csv_file: pathlib.Path):
    txt = 'URL, Page\n'
    for page, urls in urls_by_page.items():
        for url in urls:
            txt += f'{url}, {page}\n'
    csv_file.write_text(txt)


if __name__ == "__main__":
    folder = pathlib.Path("public")
    urls_by_page = get_urls_by_page(folder)
    write_csv(urls_by_page, pathlib.Path("urls.csv"))
```

**Running the script generated a CSV report** showing every link on my website, organized by which page it's on. It looks like my blog has over 7,000 links! That would be a lot to check by hand.

![](https://swharden.com/static/2023/05/13/report.png)

## Checking URLs

**Each URL from the report was checked using `HEAD` requests.** Note that a [`HEAD`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD) request to a file path only returns HTTP headers but does not actually download the file, allowing it to consume far less bandwidth [`GET`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) requests. Inspecting the HTTP response code indicates whether the URL is a valid path to a file ([code 200](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200)).

**I used [python sets](https://realpython.com/python-sets/) to prevent checking the same URL twice.** I logged good and broken URLs as they were checked, and consumed these log files at startup to allow the program to be stopped and restarted without causing it to check the same URL twice.

```py
import pathlib
import urllib.request
import time


def is_url_valid(url: str) -> bool:
    """Check if a URL exists without downloading its contents"""
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request, timeout=5)
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == "__main__":

    # load URLs from report
    urls = [x.split(", ")[0] for x
            in pathlib.Path("urls.csv").read_text().split("\n")
            if x.startswith("http")]

    # load previously checked URLs
    url_file_good = pathlib.Path("urls-good.txt")
    url_file_good.touch()
    url_file_bad = pathlib.Path("urls-bad.txt")
    url_file_bad.touch()
    checked = set()
    for url in url_file_good.read_text().split("\n"):
        checked.add(url)
    for url in url_file_bad.read_text().split("\n"):
        checked.add(url)

    # check each URL
    for i, url in enumerate(urls):
        print(f"{i+1} of {len(urls)}", end=" ")
        if url in checked:
            print(f"SKIPPING {url}")
            continue
        time.sleep(.2)
        print(f"CHECKING {url}")
        log_file = url_file_good if is_url_valid(url) else url_file_bad
        with open(log_file, 'a') as f:
            f.write(url+"\n")
        checked.add(url)
```

## Generating a Broken Link Report

**I wrote a Python script to generate a HTML report of all the broken links on my website.** The script shows every broken link found on the website and lists all the pages on which each broken link appears. 

```py
import pathlib

urls_and_pages = [x.split(", ") for x
                    in pathlib.Path("urls.csv").read_text().split("\n")
                    if x.startswith("http")]

urls_broken = [x for x
                in pathlib.Path("urls-bad.txt").read_text().split("\n")
                if x.startswith("http")]

urls_broken = set(urls_broken)

html = "<h1>Broken Links</h1>"
for url_broken in urls_broken:
    html += f"<div class='mt-4'><a href='{url_broken}'>{url_broken}</a></div>"
    pages = [x[1] for x in urls_and_pages if x[0] == url_broken]
    for page in pages:
        html += f"<div><code>{page}</code></div>"
```

I wrapped the output in [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) to make the report look pretty and appear properly on mobile devices:

```py
html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <div class='container'>
      {html}
    </div>
  </body>
</html>"""

pathlib.Path("report.html").write_text(html)
```

**The generated report lets me focus my effort** narrowly to tactically fix the broken URLs I think are most important (e.g., image URLs, URLs pointing  domain names).

![](https://swharden.com/static/2023/05/13/report2.png)

## Conclusions

* Testing URLs extracted from a folder of HTML files proved to be an effective method for identifying broken links and images across a large static website with thousands of pages.

* This method could be employed in a CI/CD pipeline to ensure links and image paths are valid on newly created pages.

* If the goal is to validate internal links only, HTTP requests could be replaced with path existence checks if the entire website is present in the local filesystem.