import markdown


class Helpers:
    @staticmethod
    def markdown_to_text(md_content):
        html = markdown.markdown(md_content)
        return html
