from html.parser import HTMLParser
import markdown


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.allowed_tags = {'a', 'b', 'strong', 'i', 'em', 'code', 'pre'}
        self.sanitized_data = []

    def handle_starttag(self, tag, attrs):
        if "h" in tag or "strong" in tag:
            self.sanitized_data.append("<b>")
        elif "li" in tag:
            self.sanitized_data.append("* ")
        elif tag not in self.allowed_tags:
            self.sanitized_data.append('')

    def handle_endtag(self, tag):
        if "h" in tag or "strong" in tag:
            self.sanitized_data.append("</b>")

    def handle_data(self, data):
        self.sanitized_data.append(data)


def sanitize_html(text):
    html_text = markdown.markdown(text)
    parser = MyHTMLParser()
    parser.feed(html_text)
    return ''.join(parser.sanitized_data)
