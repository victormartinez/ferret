import requests
from ferret.analyser import TitleAnalyser, PublishedDateAnalyser


class Ferret:
    def __init__(self, url, html=None):
        self.url = url
        self.html = html
        if html is None:
            self.html = self._get_html(url)
        self.title_analyser = TitleAnalyser(url, self.html)
        self.date_analyser = PublishedDateAnalyser(url, self.html)

    def _get_html(self, url):
        response = requests.get(url)
        return response.content

    def get_article(self):
        return self._extract_title()

    def _extract_title(self):
        extractor = self.title_analyser.get_title_extractor()
        return extractor.extract()
