# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from ferret.util.url_parser import extract_sorted_keywords_from_url
import requests
from pprint import pprint as pp


DEFAULT_TITLE_WEIGHTS = {
    'h1': 8,
    'h2': 7,
    'h3': 6,
    'h4': 5,
    'h5': 4,
    'h6': 3,
    'b': 0,
    'strong': 0
}


def calculate_title_weight_by_tag(title_candidates):
    title_weight = {}
    for candidate in title_candidates:
        if candidate.get_text() and DEFAULT_TITLE_WEIGHTS[candidate.name]:
            title_weight[candidate.get_text().strip()] = DEFAULT_TITLE_WEIGHTS.get(candidate.name)
    return title_weight


class UrlTitleExtractor(object):

    def extract(self, html, url):
        url = urllib.unquote(url).decode('utf8')
        keywords = extract_sorted_keywords_from_url(url)
        if keywords is None:
            return None

        doc = BeautifulSoup(html, 'html.parser')
        doc_body = doc.body
        if not doc_body:
            return None

        title_candidates = doc_body.select(",".join(DEFAULT_TITLE_WEIGHTS.keys()))
        title_weight = calculate_title_weight_by_tag(title_candidates)

        # stop words tend to have less characters
        keywords.sort(key=len, reverse=True)
        for candidate in title_weight.keys():
            title_weight[candidate] += self._calculate_title_weight_by_keyword_matching(candidate, keywords)

        ordered_candidates = list(sorted(title_weight, key=title_weight.__getitem__, reverse=True))
        return ordered_candidates[0]

    def _calculate_title_weight_by_keyword_matching(self, title, keywords):
        title_words = title.lower().split(" ")
        keywords = [x.lower() for x in keywords]
        weight = 0
        for i, key in enumerate(keywords):
            if key in title_words:
                weight += 1
        return weight
