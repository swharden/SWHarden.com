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
        if not line.startswith("tags:"):
            continue
        lines[i] = line.replace('"old"', '"obsolete"')

    article.set_lines(lines)
    article.save()

if __name__ == "__main__":
    for file in pathlib.Path("content/blog2/").glob("*.md"):
        # print(file)
        fix(file)
