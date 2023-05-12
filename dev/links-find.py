"""
This script parses HTML files in the output folder,
extracts link href and image src urls, and requests
their header to identify broken links/images.
"""

import pathlib
from bs4 import BeautifulSoup
from article import Article
import urllib.request
import time


def get_local_urls(file: pathlib.Path) -> list:
    article = Article(file)
    soup = BeautifulSoup(article.text, 'html.parser')
    urls = set()

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith("#"):
            continue
        if "#" in href:
            href = href.split("#")[0]
        if not "://swharden.com/" in href.lower():
            continue
        href = str(href).strip('/')
        urls.add(href)

    for image in soup.find_all('img'):
        src = image.get('src')
        if not "://swharden.com/" in src.lower():
            continue
        urls.add(str(src))

    return sorted(list(urls))


def check_exists(url: str):
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


if __name__ == "__main__":

    urls_checked = set()

    article_files = [x.joinpath("index.html").absolute()
                     for x in pathlib.Path("public/blog/").glob("*-*")]

    article_files = sorted(list(article_files))

    article_names = set([x.parent.name for x in article_files])

    for i, article_file in enumerate(article_files):
        print()
        print(
            f"Checking article {i+1} of {len(article_files)}: {article_file.parent.name}")
        for url in get_local_urls(article_file):
            if url in urls_checked:
                continue
            if pathlib.Path(url).name in article_names:
                continue
            print(f"  {url}")
            if not check_exists(url):
                print("BROKEN")
                with open("broken.txt", "a") as f:
                    f.write(f"{article_file}, {url}")
            urls_checked.add(url)
            time.sleep(1)
