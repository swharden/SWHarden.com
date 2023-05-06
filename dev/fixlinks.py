"""
This script attempts to fix the majority of relative URLs by modifying
them to point to the full static location based on the page name.
"""

import pathlib
from article import Article


def fix(file: pathlib.Path):
    year = file.name.split("-")[0]
    month = file.name.split("-")[1]
    day = file.name.split("-")[2]
    base = f"https://swharden.com/static/{year}/{month}/{day}/"

    article = Article(file)

    article.replace("src=\"http", 'IMAGE_IS_OK')
    article.replace("src=\"", "src=\""+base)
    article.replace('IMAGE_IS_OK', "src=\"http")

    article.replace("href=\"http", 'HREF_IS_OK')
    article.replace("href=\"", "href=\""+base)
    article.replace('HREF_IS_OK', "href=\"http")

    article.replace('](http', 'MD_IS_OK')
    article.replace('](', ']('+base)
    article.replace('MD_IS_OK', '](http')

    article.save()


if __name__ == "__main__":
    for file in pathlib.Path("content/blog/").glob("*.md"):
        print(file)
        fix(file)
