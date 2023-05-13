import pathlib
from article import Article


def fix(file: pathlib.Path):
    article = Article(file)
    article.replace_ignore_case("http://swharden.com", "https://swharden.com")
    article.save()


if __name__ == "__main__":
    for file in pathlib.Path("content/blog2/").glob("*.md"):
        # print(file)
        fix(file)
