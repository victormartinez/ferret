# -*- coding: utf-8 -*-
import unicodedata

import re
from bs4 import BeautifulSoup
from ferret.cleaner.text import normalize_text
from ferret.extractors.content_extractor import simple_clean
from ferret.util.title import get_score_candidates
from toolz import dicttoolz, itertoolz


class TwitterTitleExtractor:
    def __init__(self, context):
        self.soup = BeautifulSoup(context.get('html'), 'lxml')

    def is_suitable(self):
        title_tag = self.soup.select_one('meta[name=twitter:title]')
        return title_tag and title_tag.get('content')

    def extract(self):
        title = self.soup.select_one('meta[name=twitter:title]')
        if self._is_title_tag_valid(title):
            return title.get('content').strip()
        return None

    def _is_title_tag_valid(self, title_tag):
        site_name_tag = self.soup.select_one('meta[property=og:site_name]')
        if title_tag and site_name_tag and title_tag.get('content') and site_name_tag.get('content'):
            return title_tag.get('content') != site_name_tag.get('content')
        return title_tag and title_tag.get('content')


class OpenGraphTitleExtractor:
    def __init__(self, context):
        self.soup = BeautifulSoup(context.get('html'), 'lxml')

    def is_suitable(self):
        title_tag = self.soup.select_one('meta[property=og:title]')
        return title_tag and title_tag.get('content')

    def extract(self):
        title = self.soup.select_one('meta[property=og:title]')
        if self._is_title_tag_valid(title):
            return title.get('content').strip()
        return None

    def _is_title_tag_valid(self, title_tag):
        site_name_tag = self.soup.select_one('meta[property=og:site_name]')
        if title_tag and site_name_tag and title_tag.get('content') and site_name_tag.get('content'):
            return title_tag.get('content') != site_name_tag.get('content')
        return title_tag and title_tag.get('content')


class UrlTitleExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', self.url, re.M | re.I)
        return len(title_by_hyphens or '')

    def extract(self):
        keywords = self._break_url_into_keywords(self.url)
        if not keywords or not str(self.raw_html):
            return None

        relevant_candidates = self._get_relevant_candidates(keywords)
        if not relevant_candidates:
            return None

        title = self._choose_candidate(relevant_candidates)
        return normalize_text(title)

    def _break_url_into_keywords(self, url):
        title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', url, re.M | re.I)
        if len(title_by_hyphens or '') == 0:
            return None

        keywords = []
        for index, tuple in enumerate(title_by_hyphens):
            (first_match, second_match) = tuple
            words = first_match.split('-')
            cleaned_keywords = [x for x in words if x != '-' and x != '']  # the list might have empty entries
            keywords.extend(cleaned_keywords)

        return keywords

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
        self.html = context.get('html')
        self.soup = BeautifulSoup(context.get('html'), 'lxml')

    def is_suitable(self):
        title = self._get_text_from_title_tag()
        return title is not None

    def _get_text_from_title_tag(self):
        title = self.soup.select_one("title")
        if title:
            return title.text
        return None

    def extract(self):
        return self._get_text_from_title_tag()


class TitleCandidateExtractor:
    def __init__(self, context):
        self.url = context.get('url')
        self.raw_html = context.get('html')

    def is_suitable(self):
        score_candidates = get_score_candidates(self.raw_html)
        return score_candidates is not None and len(score_candidates) > 0

    def extract(self):
        cleaned_html = simple_clean(self.raw_html)
        score_candidates = get_score_candidates(cleaned_html)
        if not score_candidates:
            return None

        score_candidates = dicttoolz.keyfilter(lambda title: len(title) > 3, score_candidates)
        score_candidates = dicttoolz.keyfilter(lambda title: len(title.split()) > 1, score_candidates)
        score_candidates = self._filter_highest_candidates(score_candidates)
        return self._choose_best_candidate(score_candidates)

    def _filter_by_text_similarity(self, score_candidates, html):
        soup = BeautifulSoup(html, 'lxml').body
        text = soup.get_text()
        for title, score in score_candidates.items():
            title_words = title.split()
            keywords_by_length = itertoolz.filter(lambda title: len(title) > 3, title_words)
            ordered_keyword_list = list(sorted(keywords_by_length, key=len, reverse=True))
            score = len([k for k in ordered_keyword_list if k in text])
            score_candidates[title] += score
        return score_candidates

    def _filter_highest_candidates(self, candidate_scores):
        candidates = list(sorted(candidate_scores, key=candidate_scores.__getitem__, reverse=True))
        max_value = candidate_scores[candidates[0]]
        return dicttoolz.valfilter(lambda x: x == max_value, candidate_scores)

    def _choose_best_candidate(self, score_candidates):
        # If x > 0 then it means there is not evidence of title
        filtered_candidates = dicttoolz.valfilter(lambda x: x > 0, score_candidates)
        if not filtered_candidates:
            return None

        if len(filtered_candidates) == 1:
            return itertoolz.first(filtered_candidates)

        c = list(sorted(filtered_candidates, key=len, reverse=True))
        if len(filtered_candidates) == 2:
            if len(c) == 2:
                return c[1] if c[1] in c[0] else c[0]
        return c[0]
