"""
This script attempts to fix the majority of relative URLs by modifying
them to point to the full static location based on the page name.
"""

import pathlib
from article import Article


def fix(file: pathlib.Path):
    article = Article(file)
    lines = article.get_lines()

    for i in range(len(lines)):
        line = lines[i]
        if "_thumb.jpg" in line and "[![](" in line:
            url = line.split("(")[-1].split(")")[0]
            print(url)
            lines[i] = f"![]({url})"

    article.set_lines(lines)
    article.save()


if __name__ == "__main__":
    for file in pathlib.Path("content/blog/").glob("*.md"):
        print(file)
        fix(file)
