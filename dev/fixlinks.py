"""
This script attempts to fix the majority of relative URLs by modifying
them to point to the full static location based on the page name.
"""

import pathlib
from article import Article


def fix(file: pathlib.Path):
    article = Article(file)
    lines = article.get_lines()

    afterFrontMatter = False
    for i in range(len(lines)):
        if lines[i].startswith("---") and i > 0:
            afterFrontMatter = True
            continue
        if not afterFrontMatter:
            continue
        if len(lines[i].strip()) == 0:
            continue
        firstLine = lines[i]
        if firstLine.startswith("# ") or firstLine.startswith("## "):
            lines[i] = ""
        break

    article.set_lines(lines)
    article.save()


if __name__ == "__main__":
    for file in pathlib.Path("content/blog2/").glob("*.md"):
        # print(file)
        fix(file)
