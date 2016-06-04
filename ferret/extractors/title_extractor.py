# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ferret.util.url_parser import extract_sorted_keywords_in_url

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


class UrlTitleExtractor(object):

    def extract(self, html, url):
        keywords = extract_sorted_keywords_in_url(url)
        if keywords is None:
            return None

        doc = BeautifulSoup(html, 'html.parser')
        doc_body = doc.body
        if not doc_body:
            return None

        title_candidates = doc_body.select(",".join(DEFAULT_TITLE_WEIGHTS.keys()))
        title_weight = self._calculate_title_weight_by_tag(title_candidates)
        for candidate in title_candidates:
            title_weight[candidate.get_text()] += self._calculate_title_weight_by_keyword_matching(candidate.get_text(), keywords)

        ordered_candidates = list(sorted(title_weight, key=title_weight.__getitem__, reverse=True))
        return ordered_candidates[0]

    def _calculate_title_weight_by_tag(self, title_candidates):
        title_weight = {}
        for candidate in title_candidates:
            if candidate.get_text() and DEFAULT_TITLE_WEIGHTS[candidate.name]:
                title_weight[candidate.get_text()] = DEFAULT_TITLE_WEIGHTS.get(candidate.name)
        return title_weight

    def _calculate_title_weight_by_keyword_matching(self, title, keywords):
        title_words = title.lower().split(" ")
        keywords = [x.lower() for x in keywords]
        max_weight = len(keywords)
        weight = 0
        for i, key in enumerate(keywords):
            if key in title_words:
                weight += max_weight - i
        return weight
