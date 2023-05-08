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
        if lines[i].startswith("---") and i > 0:
            break
        if lines[i].startswith("Title:"):
            lines[i] = lines[i].replace("Title:", "title:")
        if lines[i].startswith("Tags:"):
            lines[i] = lines[i].replace("Tags:", "tags:")
        if lines[i].startswith("Description:"):
            lines[i] = lines[i].replace("Description:", "description:")

    article.set_lines(lines)
    article.save()


if __name__ == "__main__":
    for file in pathlib.Path("content/blog2/").glob("*.md"):
        # print(file)
        fix(file)
