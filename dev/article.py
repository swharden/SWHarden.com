import pathlib
import chardet
import re


class Article:
    def __init__(self, file: pathlib.Path):
        self.file = file
        with open(self.file, 'rb') as f:
            bytes = f.read()
        self.encoding = chardet.detect(bytes)["encoding"]
        try:
            with open(self.file, 'r', encoding=self.encoding) as f:
                self.text = f.read()
        except UnicodeDecodeError:
            self.encoding = "utf8"
            with open(self.file, 'r', encoding=self.encoding) as f:
                self.text = f.read()

    def replace(self, search, replace):
        self.text = self.text.replace(search, replace)

    def replace_ignore_case(self, search, replace):
        pattern = re.compile(search, re.IGNORECASE)
        self.text = pattern.sub(replace, self.text)

    def get_lines(self):
        return self.text.split("\n")

    def set_lines(self, lines):
        self.text = "\n".join(lines)

    def save(self):
        with open(self.file, 'w', encoding=self.encoding) as f:
            f.write(self.text)


if __name__ == "__main__":
    for file in pathlib.Path("content/blog/").glob("*.md"):
        print(file)
        article = Article(file)
