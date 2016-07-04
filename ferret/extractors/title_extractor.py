# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from ferret.analysers.title_analyser import DEFAULT_TITLE_WEIGHTS, calculate_title_weight_by_tag, \
    calculate_title_weight_by_keyword_matching
from ferret.util.url_parser import extract_sorted_keywords_from_url


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
            title_weight[candidate] += calculate_title_weight_by_keyword_matching(candidate, keywords)

        ordered_candidates = list(sorted(title_weight, key=title_weight.__getitem__, reverse=True))
        return ordered_candidates[0]


class TagTitleExtractor(object):
    def extract(self, html):
        doc = BeautifulSoup(html, 'html.parser')
        doc_body = doc.body
        if not doc_body:
            return None

        title_candidates = doc_body.select(",".join(DEFAULT_TITLE_WEIGHTS.keys()))
        title_weight = calculate_title_weight_by_tag(title_candidates)
        if title_weight:
            return list(title_weight)[0]
        return None
