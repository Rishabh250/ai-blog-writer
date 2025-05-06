import markdown
from bs4 import BeautifulSoup

class Helpers:
    @staticmethod
    def markdown_to_text(md_content):
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text(), html
