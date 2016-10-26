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

    def next_extractor(self):
        if self._contains_valid_og_meta_tag():
            yield OpenGraphTitleExtractor(self.raw_html)

        if self._url_follows_cms_pattern():
            yield UrlTitleExtractor(self.url, self.raw_html)

        yield TitleElementExtractor(self.raw_html)

    def _url_follows_cms_pattern(self):
        """
        Check if url follows the pattern used by many CMS: domain/[categories/]/[words-]
        e.g. http://edition.cnn.com/2016/09/16/politics/donald-trump-cuba
        """
        title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', self.url, re.M | re.I)
        if len(title_by_hyphens or ''):
            return True
        return False

    def _contains_valid_og_meta_tag(self):
        title_tag = self.soup.select_one('meta[property=og:title]')
        return title_tag and title_tag.get('content')


class PublishedDateAnalyser:
    def __init__(self, url, raw_html):
        self.url = url
        self.raw_html = raw_html
        self.soup = BeautifulSoup(raw_html, 'lxml')

    def next_extractor(self):
        if self._contains_valid_og_meta_tag():
            yield OpenGraphPublishedDateExtractor(self.raw_html)

        if self._url_contains_date():
            yield UrlPublishedDateExtractor(self.url)

        yield PatternPublishedDateExtractor(self.raw_html)
        yield MetaTagsPublishedDateExtractor(self.raw_html)

    def _contains_valid_og_meta_tag(self):
        date_tag = self.soup.select_one('meta[property=article:published_time]')
        return date_tag and date_tag.get('content')

    def _url_contains_date(self):
        published_date = re.search(r'(\d{4}/\d{2}/\d{2})/?', self.url)
        return published_date is not None
