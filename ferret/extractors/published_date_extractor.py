# -*- coding: utf-8 -*-
import dateparser
from bs4 import BeautifulSoup
from ferret.util.url_parser import extract_date_from_url
import re


class UrlPublishedDateExtractor(object):

    def extract(self, html, url):
        return extract_date_from_url(url)


class MetaTagsPublishedDateExtractor(object):

    def extract(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        meta_tags = soup.select('meta')
        if not meta_tags:
            return None

        for tag in meta_tags:
            content = tag.attrs['content']
            if content:
                match = re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', content)
                if match:
                    return dateparser.parse(match.group())
        return None
