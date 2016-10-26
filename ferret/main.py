import re
from ferret.analyser import TitleAnalyser, PublishedDateAnalyser
from ferret.util.http import get_html


class Ferret:
    def __init__(self, url, html=None):
        if html is not None and not isinstance(html, str):
            raise ValueError("HTML must be a string.")
        self.url = url
        self.raw_html = self._get_html(url, html)
        self.title_analyser = TitleAnalyser(url, self.raw_html)
        self.date_analyser = PublishedDateAnalyser(url, self.raw_html)

    def _get_html(self, url, html):
        if html is None:
            self.raw_html = get_html(url)
        return html

    def get_article(self):
        return {
            'title': self.extract_title(),
            'published_date': self.extract_published_date(),
            'html_content': self.extract_html_content()
        }

    def extract_title(self):
        extractors = self.title_analyser.next_extractor()
        for e in extractors:
            title = e.extract()
            if title:
                return title
        return ''

    def extract_published_date(self):
        extractors = self.date_analyser.next_extractor()
        for e in extractors:
            datetime = e.extract()
            if self._is_date_valid(datetime):
                return str(datetime)
        return ''

    def _is_date_valid(self, date):
        return re.search(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})/?', str(date))

    def extract_html_content(self):
        return ''
