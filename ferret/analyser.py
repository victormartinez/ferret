# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from ferret.extractors.published_date_extractor import OpenGraphPublishedDateExtractor, UrlPublishedDateExtractor, \
    MetaTagsPublishedDateExtractor, PatternPublishedDateExtractor
from ferret.extractors.title_extractor import UrlTitleExtractor, OpenGraphTitleExtractor, TitleElementExtractor


class TitleAnalyser:
    def __init__(self, url, raw_html):
        self.url = url
        self.raw_html = raw_html
        self.soup = BeautifulSoup(raw_html, 'lxml')

    def get_title_extractor(self):
        if self._html_complies_with_og_protocol():
            return OpenGraphTitleExtractor(self.soup)

        if self._url_follows_cms_pattern():
            return UrlTitleExtractor(self.url, self.soup)

        return TitleElementExtractor(self.soup)

    def _url_follows_cms_pattern(self):
        """
        Check if url follows the pattern used by many CMS: domain/[categories/]/[words-]
        e.g. http://edition.cnn.com/2016/09/16/politics/donald-trump-cuba
        """
        title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', self.url, re.M | re.I)
        if len(title_by_hyphens or ''):
            return True
        return False

    def _html_complies_with_og_protocol(self):
        title = self.soup.select('meta[property=og:title]')
        return title or len(title) > 0


class PublishedDateAnalyser:
    def __init__(self, url, raw_html):
        self.url = url
        self.raw_html = raw_html
        self.soup = BeautifulSoup(raw_html, 'lxml')

    def get_published_date_extractor(self):
        if self._html_complies_with_og_protocol():
            yield OpenGraphPublishedDateExtractor()

        yield UrlPublishedDateExtractor()
        yield MetaTagsPublishedDateExtractor()
        yield PatternPublishedDateExtractor()

    def _html_complies_with_og_protocol(self):
        return len(self.soup.select('meta[property=article:published_time]')) > 0

    def _url_contains_date(self):
        published_date = re.search(r'(\d{4}/\d{2}/\d{2})/?', self.url)
