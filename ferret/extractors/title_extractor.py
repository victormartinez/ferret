# -*- coding: utf-8 -*-
import unicodedata

import re
from bs4 import BeautifulSoup
from ferret.cleaner.text import normalize_text
from ferret.util.parser.parser import break_url_into_keywords
from ferret.util.parser.title import get_open_graph_title_text, get_text_from_title_tag, get_score_candidates, \
    get_text_from_meta_title, get_text_from_dc_title_tag
from toolz import dicttoolz, itertoolz


class OpenGraphTitleExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        soup = BeautifulSoup(self.raw_html, 'lxml')
        title_tag = soup.select_one('meta[property=og:title]')
        site_name_tag = soup.select_one('meta[property=og:site_name]')

        if title_tag and site_name_tag and title_tag.get('content') and site_name_tag.get('content'):
            return title_tag.get('content') != site_name_tag.get('content')
        return title_tag and title_tag.get('content')

    def extract(self):
        return get_open_graph_title_text(self.raw_html)


class UrlTitleExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', self.url, re.M | re.I)
        return len(title_by_hyphens or '')

    def extract(self):
        keywords = break_url_into_keywords(self.url)
        if not keywords or not str(self.raw_html):
            return None

        relevant_candidates = self._get_relevant_candidates(keywords)
        if not relevant_candidates:
            return None

        title = self._choose_candidate(relevant_candidates)
        return normalize_text(title)

    def _get_relevant_candidates(self, keywords):
        score_candidates = get_score_candidates(self.raw_html)
        for candidate, score in score_candidates.items():
            score_candidates[candidate] += self._calculate_score_by_matching(candidate, keywords)
        return dicttoolz.valfilter(lambda score: score, score_candidates)

    def _calculate_score_by_matching(self, candidate, keywords):
        strip_words = [t.lower() for t in unicodedata.normalize('NFKD', candidate).split(" ")]
        strip_keywords = [unicodedata.normalize('NFKD', k.strip()) for k in keywords]
        intersection = set(strip_words).intersection(strip_keywords)
        return len(intersection)

    def _choose_candidate(self, candidate_scores):
        candidates = list(sorted(candidate_scores, key=candidate_scores.__getitem__, reverse=True))
        if len(candidates) == 1:
            return candidates[0]

        highest_scored_candidates = self._filter_highest_candidates(candidate_scores)
        c = sorted(highest_scored_candidates, key=len, reverse=True)
        if len(c) == 2:
            return c[1] if c[1] in c[0] else c[0]
        return c[0]

    def _filter_highest_candidates(self, candidate_scores):
        candidates = list(sorted(candidate_scores, key=candidate_scores.__getitem__, reverse=True))
        max_value = candidate_scores[candidates[0]]
        return dicttoolz.valfilter(lambda x: x == max_value, candidate_scores)


class TitleTagExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        title = get_text_from_title_tag(self.raw_html)
        return title is not None and title != ''

    def extract(self):
        return get_text_from_title_tag(self.raw_html)


class TitleCandidateExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        score_candidates = get_score_candidates(self.raw_html)
        return score_candidates is not None and len(score_candidates) > 0

    def extract(self):
        score_candidates = get_score_candidates(self.raw_html)
        score_candidates = self._score_candidates_by_keywords(score_candidates)
        score_candidates = self._score_candidates_by_length(score_candidates)
        score_candidates = self._filter_highest_candidates(score_candidates)
        return self._choose_best_candidate(score_candidates)

    def _score_candidates_by_keywords(self, candidates):
        keywords = self._get_keywords()
        if not keywords:
            return candidates

        for candidate, score in candidates.items():
            title_keywords = candidate.split()
            occurence_score = len(set(title_keywords).intersection(keywords))
            candidates[candidate] += occurence_score

        return candidates

    def _score_candidates_by_length(self, candidates):
        for candidate, score in candidates.items():
            if len(candidate) > 3:
                candidates[candidate] += 1
        return candidates

    def _get_keywords(self):
        title1 = get_text_from_title_tag(self.raw_html)
        title2 = get_open_graph_title_text(self.raw_html)
        title3 = get_text_from_meta_title(self.raw_html)
        title4 = get_text_from_dc_title_tag(self.raw_html)

        keywords1 = title1.split() if title1 else []
        keywords2 = title2.split() if title2 else []
        keywords3 = title3.split() if title3 else []
        keywords4 = title4.split() if title3 else []

        return list(itertoolz.concatv(keywords1, keywords2, keywords3, keywords4))

    def _filter_highest_candidates(self, candidate_scores):
        candidates = list(sorted(candidate_scores, key=candidate_scores.__getitem__, reverse=True))
        max_value = candidate_scores[candidates[0]]
        return dicttoolz.valfilter(lambda x: x == max_value, candidate_scores)

    def _choose_best_candidate(self, score_candidates):
        if len(score_candidates) == 1:
            return itertoolz.first(score_candidates)

        c = list(sorted(score_candidates, key=len, reverse=True))
        if len(score_candidates) == 2:
            if len(c) == 2:
                return c[1] if c[1] in c[0] else c[0]
        return c[0]
